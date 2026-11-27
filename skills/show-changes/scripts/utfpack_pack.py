#!/usr/bin/env python3
# Source: https://github.com/kulikala/utfpack (python/utfpack_pack.py)
# Version: 0.1.0
# License: MIT, Kaz Namba
"""utfpack_pack.py - pack files into one JavaScript-safe string (Python side of utfpack).

Packs files (or whole folders) into a compressed string that the utfpack
decoders unpack in the browser.  The output is data only: an ES module that
exports the string, the plain string, a classic script, or an HTML fragment.
The page loads a utfpack decoder itself (from any host) and combines it with
the data; with --embed-decoder the decoder of the chosen format goes into the
output.  Only the encoder lives here; decoding runs in the browser (or in Node
with the utfpack package).  The output is character-for-character the same
format as the Node side (`utfpack pack`).

The first character of a string is a marker for the codec and the format:
deflate A base91, B base64, C dense; lzma D base91, E base64, F dense.

Requirements: Python 3.8 or newer and the standard library only.  The lzma
module is optional; without it only the deflate codec is offered.

Usage:
    python3 utfpack_pack.py pack <paths...> [-o out] [--base dir]
        [--codec auto|deflate|lzma] [--format auto|base91|base64|dense]
        [--ascii] [--emit module|string|script|html] [--string]
        [--name ident] [--global ident] [--sync] [--embed-decoder] [--csp]
    python3 utfpack_pack.py pack --scene name=path --scene name=path ...
        [-o out] [--emit script|html] [--global ident] [--sync]
        [--embed-decoder] [--csp] [--codec ...] [--format ...] [--ascii]
    python3 utfpack_pack.py decoder --entry <entry> [--emit script|html]
        [--global ident] [-o out]

Library use:
    import utfpack_pack
    result = utfpack_pack.pack({'a.txt': 'text', 'b.bin': b'\\x00\\x01'})
    module = utfpack_pack.emit(result, 'module')  # export default "<string>";
    html = utfpack_pack.emit(result, 'html')      # <script>globalThis.utfpackData=...
    scenes = utfpack_pack.pack_scenes({'one': {...}, 'two': {...}})
    page = utfpack_pack.emit_scenes(scenes, 'html')
    inline = utfpack_pack.pack(files, emit='html', embed_decoder=True)
    inline_page = utfpack_pack.emit(inline, 'html', embed_decoder=True)
    hashes = utfpack_pack.csp_hashes(inline_page)  # "'sha256-...'" per inline script

Differences from the Node side:
  * deflate comes from zlib (level 9) instead of zopfli, so deflate output is
    a little larger.
  * the "as-is" size on stderr is the unminified size (reported as
    "(not minified)").

License: MIT
"""

import base64
import hashlib
import json
import os
import re
import sys

try:
    import zlib
except ImportError:  # pragma: no cover - depends on how Python was built
    zlib = None

try:
    import lzma
except ImportError:  # liblzma was not available when this Python was built
    lzma = None

__all__ = [
    'DECODER_BYTES',
    'GLOBAL_DECODER_BYTES',
    'VERSION',
    'csp_hashes',
    'decoder_script',
    'decoder_sri',
    'emit',
    'emit_scenes',
    'pack',
    'pack_scenes',
]

# Minified decoder sizes in bytes per entry; the same values as DECODER_BYTES
# (ES modules) and GLOBAL_DECODER_BYTES (classic scripts) in src/pack.ts.
# 'utfpack' decodes all six formats, the other entries one each.
DECODER_BYTES = {
    'utfpack': 6436,
    'utfpack/base91': 1447,
    'utfpack/base64': 1143,
    'utfpack/dense': 3238,
    'utfpack/lzma': 3894,
    'utfpack/lzma-base64': 3590,
    'utfpack/lzma-dense': 5713,
}

GLOBAL_DECODER_BYTES = {
    'utfpack': 6650,
    'utfpack/base91': 1493,
    'utfpack/base64': 1189,
    'utfpack/dense': 3284,
    'utfpack/lzma': 3954,
    'utfpack/lzma-base64': 3650,
    'utfpack/lzma-dense': 5773,
}

# The package version (package.json).
VERSION = "0.1.0"

# Global-version decoders (the files in dist/global), keyed by entry name.
_DECODERS = {
    "utfpack": "var utfpack=(()=>{\"use strict\";function Y(e){let t=new Uint8Array(e.length),n=0,o=0,r=-1,c=0;for(let u of e){let f=u.charCodeAt(0);if(f<32||f>126||'\"<\\\\`'.includes(u))throw Error(\"utfpack: invalid character\");let i=f-32-+(f>34)-+(f>60)-+(f>92)-+(f>96);if(r<0)r=i;else{r+=i*91,n|=r<<o,o+=(r&8191)>88?13:14;do t[c++]=n&255,n>>=8,o-=8;while(o>7);r=-1}}return r>=0&&(t[c++]=(n|r<<o)&255),t.subarray(0,c)}function I(){throw Error(\"utfpack: corrupt data\")}function X(e){let t=0,n=()=>{let s=0,l=1,a;do t>=e.length&&I(),a=e[t++],s+=(a&127)*l,l*=128;while(a>127);return s},o=s=>{s>e.length-t&&I()},r=new TextDecoder(\"utf-8\",{ignoreBOM:!0,fatal:!0}),c=s=>{try{return r.decode(s)}catch{return I()}},u=[],f=n();o(f);for(let s=f;s>0;s--){let l=n();o(l);let a=c(e.subarray(t,t+=l));u.push([a,n()])}let i={};for(let[s,l]of u){let a=Math.floor(l/2);o(a),Object.hasOwn(i,s)&&I();let k=e.subarray(t,t+=a);Object.defineProperty(i,s,{value:l%2?c(k):k.slice(),enumerable:!0,writable:!0,configurable:!0})}return t!==e.length&&I(),i}var y=class extends Error{code;constructor(t,n){super(n??`utfpack: ${t}`),this.name=\"UtfpackError\",this.code=t}};var _=new WeakMap,N=new WeakMap,tt=new WeakMap;function bt(e){return e.toString(2).length}function ot(e){return bt(e)-1>>3}function yt(e){let t=tt.get(e);if(t===void 0){let n=e.length>>1;t=new Uint32Array(n+1);for(let o=0;o<n;o++)t[o+1]=t[o]+e[o*2+1];tt.set(e,t)}return t}function kt(e,t){let n=e.ranges,o=yt(n),r=0,c=(n.length>>1)-1;for(;r<=c;){let u=r+c>>1,f=n[u*2],i=n[u*2+1];if(t<f)c=u-1;else if(t>=f+i)r=u+1;else return o[u]+(t-f)}return-1}function rt(e){let t=_.get(e);if(t!==void 0)return t;let n=e.classes,o=n.length,r=e.L,c=new Array(r+1);c[0]=1n;for(let i=1;i<=r;i++){let s=0n;for(let l=0;l<o;l++){let a=n[l].width;i>=a&&(s+=BigInt(n[l].count)*c[i-a])}c[i]=s}let u=new Array(r+1);for(let i=0;i<=r;i++){let s=new Array(o+1),l=0n;s[0]=0n;for(let a=0;a<o;a++){let k=n[a].width;i>=k&&(l+=BigInt(n[a].count)*c[i-k]),s[a+1]=l}u[i]=s}let f={L:r,K:ot(c[r]),a:c,off:u};return _.set(e,f),N.set(e,{counts:n.map(i=>BigInt(i.count)),widths:n.map(i=>i.width)}),f}function et(e){let t=N.get(e);return t===void 0&&(rt(e),t=N.get(e)),t}function At(e,t){if(t===0)return new Uint8Array(0);let n=new Uint8Array(t),o=e.toString(16);o=o.padStart(t*2,\"0\");for(let r=0;r<t;r++)n[r]=parseInt(o.slice(r*2,r*2+2),16);return n}function nt(e,t){if(e>=1n<<BigInt(8*t))throw new y(\"bad-value\");return At(e,t)}function st(e,t){if(t.length===0)throw new y(\"bad-length\");let n=rt(e),o=e.classes,r=o.length,c=et(e).counts,u=et(e).widths,f=n.L,i=n.K,s=[],l=0n,a=0;for(let A=0;A<t.length;){let T=t.codePointAt(A);A+=T>65535?2:1;let M=-1,O=-1;for(let U=0;U<r;U++){let D=kt(o[U],T);if(D>=0){M=U,O=D;break}}if(M<0)throw new y(\"invalid-char\");let R=a+u[M];if(R>f)throw new y(\"bad-length\");l=n.off[R][M]+l*c[M]+BigInt(O),a=R,a===f&&(s.push(nt(l,i)),l=0n,a=0)}a>0&&s.push(nt(l,ot(n.a[a])));let k=0;for(let A of s)k+=A.length;let P=new Uint8Array(k),K=0;for(let A of s)P.set(A,K),K+=A.length;return P}var it=\"ABCDEF\";async function ct(e){let t=new Response(e).body.pipeThrough(new DecompressionStream(\"deflate-raw\"));return new Uint8Array(await new Response(t).arrayBuffer())}function ft(e){return Uint8Array.from(atob(e),t=>t.charCodeAt(0))}var Bt=\"utfpack: corrupt LZMA data\";function L(){throw new Error(Bt)}function p(e){return new Uint16Array(e).fill(1024)}var Z=class{src;pos;range;code;constructor(t){(t.length<5||t[0]!==0)&&L(),this.src=t,this.pos=5,this.range=4294967295,this.code=(t[1]<<24|t[2]<<16|t[3]<<8|t[4])>>>0}byte(){return this.pos>=this.src.length&&L(),this.src[this.pos++]}normalize(){this.range<16777216&&(this.range=this.range<<8>>>0,this.code=(this.code<<8|this.byte())>>>0)}bit(t,n){let o=t[n],r=(this.range>>>11)*o;return this.code<r?(this.range=r,t[n]=o+(2048-o>>5),this.normalize(),0):(this.range=this.range-r>>>0,this.code=this.code-r>>>0,t[n]=o-(o>>5),this.normalize(),1)}direct(t){let n=0;for(;t-- >0;)this.range>>>=1,this.code>=this.range?(this.code=this.code-this.range>>>0,n=n<<1|1):n<<=1,this.normalize();return n}};function j(e,t,n,o){let r=1;for(let c=0;c<o;c++)r=r<<1|e.bit(t,n+r);return r-(1<<o)}function at(e,t,n,o){let r=1,c=0;for(let u=0;u<o;u++){let f=e.bit(t,n+r);r=r<<1|f,c|=f<<u}return c}function $(e){e.length<13&&L();let t=e[0];t>=225&&L();let n=t%9,o=Math.floor(t/9)%5,r=Math.floor(t/45),c=(e[5]|e[6]<<8|e[7]<<16|e[8]<<24)>>>0,u=(e[9]|e[10]<<8|e[11]<<16|e[12]<<24)>>>0,f=!(c===4294967295&&u===4294967295),i=u*4294967296+c,s=new Z(e.subarray(13)),l=p(192),a=p(12),k=p(12),P=p(12),K=p(12),A=p(192),T=p(256),M=p(114),O=p(16),R=p(2),U=p(128),D=p(128),ht=p(256),pt=p(2),dt=p(128),wt=p(128),gt=p(256),G=p(768<<n+o),mt=(1<<r)-1,xt=(1<<o)-1,q=(B,b,S,g,z)=>s.bit(B,0)===0?j(s,b,z<<3,3):s.bit(B,1)===0?8+j(s,S,z<<3,3):16+j(s,g,0,8),x,H=!1;if(f)try{x=new Uint8Array(i)}catch{L()}else x=new Uint8Array(65536),H=!0;let w=0,J=B=>{if(w+B<=x.length)return;H||L();let b=x.length;for(;b<w+B;)b*=2;let S=new Uint8Array(b);S.set(x),x=S},h=0,m=0,E=0,v=0,W=0;for(;!(f&&w===i);){let B=w&mt;if(s.bit(l,(h<<4)+B)===0){let g=w===0?0:x[w-1],C=(((w&xt)<<n)+(g>>>8-n))*768,d=1;if(h<7)do d=d<<1|s.bit(G,C+d);while(d<256);else{m>=w&&L();let F=x[w-m-1];do{let Q=F>>>7&1;F=F<<1&255;let V=s.bit(G,C+(1+Q<<8)+d);if(d=d<<1|V,Q!==V){for(;d<256;)d=d<<1|s.bit(G,C+d);break}}while(d<256)}J(1),x[w++]=d,h=h<4?0:h<10?h-3:h-6;continue}let b;if(s.bit(a,h)!==0){if(b=0,s.bit(k,h)===0)s.bit(A,(h<<4)+B)===0&&(h=h<7?9:11,b=1);else{let g;s.bit(P,h)===0?g=E:(s.bit(K,h)===0?g=v:(g=W,W=v),v=E),E=m,m=g}b===0&&(b=q(pt,dt,wt,gt,B)+2,h=h<7?8:11)}else{W=v,v=E,E=m;let g=q(R,U,D,ht,B);b=g+2,h=h<7?7:10;let z=g<4?g:3,C=j(s,T,z<<6,6);if(C<4)m=C;else{let d=(C>>>1)-1;m=(2|C&1)*2**d,C<14?m+=at(s,M,m-C-1,d):(m+=s.direct(d-4)*16,m+=at(s,O,0,4))}if(m===4294967295){f&&w!==i&&L();break}}m>=w&&L(),J(b);let S=w-m-1;for(let g=0;g<b;g++)x[w++]=x[S++]}return H?x.slice(0,w):x}var lt={name:\"dense\",classes:[{count:91,width:1,ranges:[32,2,35,25,61,31,93,3,97,30]},{count:1878,width:2,ranges:[160,13,174,1362,1542,22,1565,192,1758,49,1808,240]},{count:61371,width:3,ranges:[2048,144,2194,80,2275,3883,6159,2044,8208,24,8239,49,8293,1,8304,46992,57344,7632,65008,271,65280,249,65532,2]}],L:1024};function ut(e){let t=typeof e==\"string\"&&e!==\"\"?it.indexOf(e[0]):-1;if(t<0)throw new y(\"bad-format\",\"utfpack: not a utfpack string (unknown marker)\");let n=e.slice(1),o=t%3;return[t>2,o===0?Y(n):o===1?ft(n):st(lt,n)]}function jt(e){let[t,n]=ut(e);if(!t)throw new y(\"bad-format\",\"utfpack: unpackSync needs an lzma string; use unpack for a deflate string\");return X($(n))}async function Gt(e){let[t,n]=ut(e);return X(t?$(n):await ct(n))}return{UtfpackError:y,unpack:Gt,unpackSync:jt}})();",
    "utfpack/base91": "var utfpack=(()=>{\"use strict\";function m(t){let e=new Uint8Array(t.length),o=0,a=0,n=-1,i=0;for(let l of t){let c=l.charCodeAt(0);if(c<32||c>126||'\"<\\\\`'.includes(l))throw Error(\"utfpack: invalid character\");let s=c-32-+(c>34)-+(c>60)-+(c>92)-+(c>96);if(n<0)n=s;else{n+=s*91,o|=n<<a,a+=(n&8191)>88?13:14;do e[i++]=o&255,o>>=8,a-=8;while(a>7);n=-1}}return n>=0&&(e[i++]=(o|n<<a)&255),e.subarray(0,i)}function p(){throw Error(\"utfpack: corrupt data\")}function w(t){let e=0,o=()=>{let r=0,f=1,u;do e>=t.length&&p(),u=t[e++],r+=(u&127)*f,f*=128;while(u>127);return r},a=r=>{r>t.length-e&&p()},n=new TextDecoder(\"utf-8\",{ignoreBOM:!0,fatal:!0}),i=r=>{try{return n.decode(r)}catch{return p()}},l=[],c=o();a(c);for(let r=c;r>0;r--){let f=o();a(f);let u=i(t.subarray(e,e+=f));l.push([u,o()])}let s={};for(let[r,f]of l){let u=Math.floor(f/2);a(u),Object.hasOwn(s,r)&&p();let h=t.subarray(e,e+=u);Object.defineProperty(s,r,{value:f%2?i(h):h.slice(),enumerable:!0,writable:!0,configurable:!0})}return e!==t.length&&p(),s}var d=class extends Error{code;constructor(e,o){super(o??`utfpack: ${e}`),this.name=\"UtfpackError\",this.code=e}};function x(t,e){if(typeof t!=\"string\"||t[0]!==e)throw new d(\"bad-format\");return t.slice(1)}async function k(t){let e=new Response(t).body.pipeThrough(new DecompressionStream(\"deflate-raw\"));return new Uint8Array(await new Response(e).arrayBuffer())}async function y(t){return w(await k(t))}async function R(t){return y(m(x(t,\"A\")))}return{UtfpackError:d,unpack:R}})();",
    "utfpack/base64": "var utfpack=(()=>{\"use strict\";function c(){throw Error(\"utfpack: corrupt data\")}function m(t){let e=0,a=()=>{let r=0,n=1,o;do e>=t.length&&c(),o=t[e++],r+=(o&127)*n,n*=128;while(o>127);return r},f=r=>{r>t.length-e&&c()},x=new TextDecoder(\"utf-8\",{ignoreBOM:!0,fatal:!0}),i=r=>{try{return x.decode(r)}catch{return c()}},p=[],l=a();f(l);for(let r=l;r>0;r--){let n=a();f(n);let o=i(t.subarray(e,e+=n));p.push([o,a()])}let s={};for(let[r,n]of p){let o=Math.floor(n/2);f(o),Object.hasOwn(s,r)&&c();let d=t.subarray(e,e+=o);Object.defineProperty(s,r,{value:n%2?i(d):d.slice(),enumerable:!0,writable:!0,configurable:!0})}return e!==t.length&&c(),s}var u=class extends Error{code;constructor(e,a){super(a??`utfpack: ${e}`),this.name=\"UtfpackError\",this.code=e}};function h(t,e){if(typeof t!=\"string\"||t[0]!==e)throw new u(\"bad-format\");return t.slice(1)}async function k(t){let e=new Response(t).body.pipeThrough(new DecompressionStream(\"deflate-raw\"));return new Uint8Array(await new Response(e).arrayBuffer())}async function w(t){return m(await k(t))}function y(t){return Uint8Array.from(atob(t),e=>e.charCodeAt(0))}async function R(t){return w(y(h(t,\"B\")))}return{UtfpackError:u,unpack:R}})();",
    "utfpack/dense": "var utfpack=(()=>{\"use strict\";var h=class extends Error{code;constructor(n,e){super(e??`utfpack: ${n}`),this.name=\"UtfpackError\",this.code=n}};var I=new WeakMap,y=new WeakMap,L=new WeakMap;function j(t){return t.toString(2).length}function S(t){return j(t)-1>>3}function O(t){let n=L.get(t);if(n===void 0){let e=t.length>>1;n=new Uint32Array(e+1);for(let s=0;s<e;s++)n[s+1]=n[s]+t[s*2+1];L.set(t,n)}return n}function T(t,n){let e=t.ranges,s=O(e),a=0,f=(e.length>>1)-1;for(;a<=f;){let u=a+f>>1,l=e[u*2],c=e[u*2+1];if(n<l)f=u-1;else if(n>=l+c)a=u+1;else return s[u]+(n-l)}return-1}function E(t){let n=I.get(t);if(n!==void 0)return n;let e=t.classes,s=e.length,a=t.L,f=new Array(a+1);f[0]=1n;for(let c=1;c<=a;c++){let o=0n;for(let i=0;i<s;i++){let r=e[i].width;c>=r&&(o+=BigInt(e[i].count)*f[c-r])}f[c]=o}let u=new Array(a+1);for(let c=0;c<=a;c++){let o=new Array(s+1),i=0n;o[0]=0n;for(let r=0;r<s;r++){let d=e[r].width;c>=d&&(i+=BigInt(e[r].count)*f[c-d]),o[r+1]=i}u[c]=o}let l={L:a,K:S(f[a]),a:f,off:u};return I.set(t,l),y.set(t,{counts:e.map(c=>BigInt(c.count)),widths:e.map(c=>c.width)}),l}function U(t){let n=y.get(t);return n===void 0&&(E(t),n=y.get(t)),n}function W(t,n){if(n===0)return new Uint8Array(0);let e=new Uint8Array(n),s=t.toString(16);s=s.padStart(n*2,\"0\");for(let a=0;a<n;a++)e[a]=parseInt(s.slice(a*2,a*2+2),16);return e}function K(t,n){if(t>=1n<<BigInt(8*n))throw new h(\"bad-value\");return W(t,n)}function M(t,n){if(n.length===0)throw new h(\"bad-length\");let e=E(t),s=t.classes,a=s.length,f=U(t).counts,u=U(t).widths,l=e.L,c=e.K,o=[],i=0n,r=0;for(let p=0;p<n.length;){let B=n.codePointAt(p);p+=B>65535?2:1;let w=-1,A=-1;for(let x=0;x<a;x++){let C=T(s[x],B);if(C>=0){w=x,A=C;break}}if(w<0)throw new h(\"invalid-char\");let m=r+u[w];if(m>l)throw new h(\"bad-length\");i=e.off[m][w]+i*f[w]+BigInt(A),r=m,r===l&&(o.push(K(i,c)),i=0n,r=0)}r>0&&o.push(K(i,S(e.a[r])));let d=0;for(let p of o)d+=p.length;let k=new Uint8Array(d),b=0;for(let p of o)k.set(p,b),b+=p.length;return k}var P={name:\"dense\",classes:[{count:91,width:1,ranges:[32,2,35,25,61,31,93,3,97,30]},{count:1878,width:2,ranges:[160,13,174,1362,1542,22,1565,192,1758,49,1808,240]},{count:61371,width:3,ranges:[2048,144,2194,80,2275,3883,6159,2044,8208,24,8239,49,8293,1,8304,46992,57344,7632,65008,271,65280,249,65532,2]}],L:1024};function g(){throw Error(\"utfpack: corrupt data\")}function v(t){let n=0,e=()=>{let o=0,i=1,r;do n>=t.length&&g(),r=t[n++],o+=(r&127)*i,i*=128;while(r>127);return o},s=o=>{o>t.length-n&&g()},a=new TextDecoder(\"utf-8\",{ignoreBOM:!0,fatal:!0}),f=o=>{try{return a.decode(o)}catch{return g()}},u=[],l=e();s(l);for(let o=l;o>0;o--){let i=e();s(i);let r=f(t.subarray(n,n+=i));u.push([r,e()])}let c={};for(let[o,i]of u){let r=Math.floor(i/2);s(r),Object.hasOwn(c,o)&&g();let d=t.subarray(n,n+=r);Object.defineProperty(c,o,{value:i%2?f(d):d.slice(),enumerable:!0,writable:!0,configurable:!0})}return n!==t.length&&g(),c}function D(t,n){if(typeof t!=\"string\"||t[0]!==n)throw new h(\"bad-format\");return t.slice(1)}async function F(t){let n=new Response(t).body.pipeThrough(new DecompressionStream(\"deflate-raw\"));return new Uint8Array(await new Response(n).arrayBuffer())}async function R(t){return v(await F(t))}async function Z(t){return R(M(P,D(t,\"C\")))}return{UtfpackError:h,unpack:Z}})();",
    "utfpack/lzma": "var utfpack=(()=>{\"use strict\";function F(e){let t=new Uint8Array(e.length),n=0,i=0,r=-1,a=0;for(let m of e){let f=m.charCodeAt(0);if(f<32||f>126||'\"<\\\\`'.includes(m))throw Error(\"utfpack: invalid character\");let w=f-32-+(f>34)-+(f>60)-+(f>92)-+(f>96);if(r<0)r=w;else{r+=w*91,n|=r<<i,i+=(r&8191)>88?13:14;do t[a++]=n&255,n>>=8,i-=8;while(i>7);r=-1}}return r>=0&&(t[a++]=(n|r<<i)&255),t.subarray(0,a)}function E(){throw Error(\"utfpack: corrupt data\")}function K(e){let t=0,n=()=>{let o=0,x=1,g;do t>=e.length&&E(),g=e[t++],o+=(g&127)*x,x*=128;while(g>127);return o},i=o=>{o>e.length-t&&E()},r=new TextDecoder(\"utf-8\",{ignoreBOM:!0,fatal:!0}),a=o=>{try{return r.decode(o)}catch{return E()}},m=[],f=n();i(f);for(let o=f;o>0;o--){let x=n();i(x);let g=a(e.subarray(t,t+=x));m.push([g,n()])}let w={};for(let[o,x]of m){let g=Math.floor(x/2);i(g),Object.hasOwn(w,o)&&E();let S=e.subarray(t,t+=g);Object.defineProperty(w,o,{value:x%2?a(S):S.slice(),enumerable:!0,writable:!0,configurable:!0})}return t!==e.length&&E(),w}var z=class extends Error{code;constructor(t,n){super(n??`utfpack: ${t}`),this.name=\"UtfpackError\",this.code=t}};function Z(e,t){if(typeof e!=\"string\"||e[0]!==t)throw new z(\"bad-format\");return e.slice(1)}var ct=\"utfpack: corrupt LZMA data\";function A(){throw new Error(ct)}function c(e){return new Uint16Array(e).fill(1024)}var L=class{src;pos;range;code;constructor(t){(t.length<5||t[0]!==0)&&A(),this.src=t,this.pos=5,this.range=4294967295,this.code=(t[1]<<24|t[2]<<16|t[3]<<8|t[4])>>>0}byte(){return this.pos>=this.src.length&&A(),this.src[this.pos++]}normalize(){this.range<16777216&&(this.range=this.range<<8>>>0,this.code=(this.code<<8|this.byte())>>>0)}bit(t,n){let i=t[n],r=(this.range>>>11)*i;return this.code<r?(this.range=r,t[n]=i+(2048-i>>5),this.normalize(),0):(this.range=this.range-r>>>0,this.code=this.code-r>>>0,t[n]=i-(i>>5),this.normalize(),1)}direct(t){let n=0;for(;t-- >0;)this.range>>>=1,this.code>=this.range?(this.code=this.code-this.range>>>0,n=n<<1|1):n<<=1,this.normalize();return n}};function v(e,t,n,i){let r=1;for(let a=0;a<i;a++)r=r<<1|e.bit(t,n+r);return r-(1<<i)}function $(e,t,n,i){let r=1,a=0;for(let m=0;m<i;m++){let f=e.bit(t,n+r);r=r<<1|f,a|=f<<m}return a}function q(e){e.length<13&&A();let t=e[0];t>=225&&A();let n=t%9,i=Math.floor(t/9)%5,r=Math.floor(t/45),a=(e[5]|e[6]<<8|e[7]<<16|e[8]<<24)>>>0,m=(e[9]|e[10]<<8|e[11]<<16|e[12]<<24)>>>0,f=!(a===4294967295&&m===4294967295),w=m*4294967296+a,o=new L(e.subarray(13)),x=c(192),g=c(12),S=c(12),I=c(12),J=c(12),N=c(192),Q=c(256),V=c(114),W=c(16),X=c(2),Y=c(128),_=c(128),tt=c(256),et=c(2),ot=c(128),nt=c(128),rt=c(256),B=c(768<<n+i),it=(1<<r)-1,st=(1<<i)-1,P=(y,b,M,h,C)=>o.bit(y,0)===0?v(o,b,C<<3,3):o.bit(y,1)===0?8+v(o,M,C<<3,3):16+v(o,h,0,8),d,D=!1;if(f)try{d=new Uint8Array(w)}catch{A()}else d=new Uint8Array(65536),D=!0;let u=0,G=y=>{if(u+y<=d.length)return;D||A();let b=d.length;for(;b<u+y;)b*=2;let M=new Uint8Array(b);M.set(d),d=M},s=0,p=0,R=0,U=0,O=0;for(;!(f&&u===w);){let y=u&it;if(o.bit(x,(s<<4)+y)===0){let h=u===0?0:d[u-1],k=(((u&st)<<n)+(h>>>8-n))*768,l=1;if(s<7)do l=l<<1|o.bit(B,k+l);while(l<256);else{p>=u&&A();let T=d[u-p-1];do{let H=T>>>7&1;T=T<<1&255;let j=o.bit(B,k+(1+H<<8)+l);if(l=l<<1|j,H!==j){for(;l<256;)l=l<<1|o.bit(B,k+l);break}}while(l<256)}G(1),d[u++]=l,s=s<4?0:s<10?s-3:s-6;continue}let b;if(o.bit(g,s)!==0){if(b=0,o.bit(S,s)===0)o.bit(N,(s<<4)+y)===0&&(s=s<7?9:11,b=1);else{let h;o.bit(I,s)===0?h=R:(o.bit(J,s)===0?h=U:(h=O,O=U),U=R),R=p,p=h}b===0&&(b=P(et,ot,nt,rt,y)+2,s=s<7?8:11)}else{O=U,U=R,R=p;let h=P(X,Y,_,tt,y);b=h+2,s=s<7?7:10;let C=h<4?h:3,k=v(o,Q,C<<6,6);if(k<4)p=k;else{let l=(k>>>1)-1;p=(2|k&1)*2**l,k<14?p+=$(o,V,p-k-1,l):(p+=o.direct(l-4)*16,p+=$(o,W,0,4))}if(p===4294967295){f&&u!==w&&A();break}}p>=u&&A(),G(b);let M=u-p-1;for(let h=0;h<b;h++)d[u++]=d[M++]}return D?d.slice(0,u):d}function ft(e){return K(q(F(Z(e,\"D\"))))}async function gt(e){return ft(e)}return{UtfpackError:z,unpack:gt,unpackSync:ft}})();",
    "utfpack/lzma-base64": "var utfpack=(()=>{\"use strict\";function C(){throw Error(\"utfpack: corrupt data\")}function F(e){let t=0,o=()=>{let n=0,b=1,m;do t>=e.length&&C(),m=e[t++],n+=(m&127)*b,b*=128;while(m>127);return n},s=n=>{n>e.length-t&&C()},c=new TextDecoder(\"utf-8\",{ignoreBOM:!0,fatal:!0}),d=n=>{try{return c.decode(n)}catch{return C()}},x=[],y=o();s(y);for(let n=y;n>0;n--){let b=o();s(b);let m=d(e.subarray(t,t+=b));x.push([m,o()])}let M={};for(let[n,b]of x){let m=Math.floor(b/2);s(m),Object.hasOwn(M,n)&&C();let S=e.subarray(t,t+=m);Object.defineProperty(M,n,{value:b%2?d(S):S.slice(),enumerable:!0,writable:!0,configurable:!0})}return t!==e.length&&C(),M}var E=class extends Error{code;constructor(t,o){super(o??`utfpack: ${t}`),this.name=\"UtfpackError\",this.code=t}};function K(e,t){if(typeof e!=\"string\"||e[0]!==t)throw new E(\"bad-format\");return e.slice(1)}function Z(e){return Uint8Array.from(atob(e),t=>t.charCodeAt(0))}var ct=\"utfpack: corrupt LZMA data\";function k(){throw new Error(ct)}function i(e){return new Uint16Array(e).fill(1024)}var P=class{src;pos;range;code;constructor(t){(t.length<5||t[0]!==0)&&k(),this.src=t,this.pos=5,this.range=4294967295,this.code=(t[1]<<24|t[2]<<16|t[3]<<8|t[4])>>>0}byte(){return this.pos>=this.src.length&&k(),this.src[this.pos++]}normalize(){this.range<16777216&&(this.range=this.range<<8>>>0,this.code=(this.code<<8|this.byte())>>>0)}bit(t,o){let s=t[o],c=(this.range>>>11)*s;return this.code<c?(this.range=c,t[o]=s+(2048-s>>5),this.normalize(),0):(this.range=this.range-c>>>0,this.code=this.code-c>>>0,t[o]=s-(s>>5),this.normalize(),1)}direct(t){let o=0;for(;t-- >0;)this.range>>>=1,this.code>=this.range?(this.code=this.code-this.range>>>0,o=o<<1|1):o<<=1,this.normalize();return o}};function B(e,t,o,s){let c=1;for(let d=0;d<s;d++)c=c<<1|e.bit(t,o+c);return c-(1<<s)}function $(e,t,o,s){let c=1,d=0;for(let x=0;x<s;x++){let y=e.bit(t,o+c);c=c<<1|y,d|=y<<x}return d}function q(e){e.length<13&&k();let t=e[0];t>=225&&k();let o=t%9,s=Math.floor(t/9)%5,c=Math.floor(t/45),d=(e[5]|e[6]<<8|e[7]<<16|e[8]<<24)>>>0,x=(e[9]|e[10]<<8|e[11]<<16|e[12]<<24)>>>0,y=!(d===4294967295&&x===4294967295),M=x*4294967296+d,n=new P(e.subarray(13)),b=i(192),m=i(12),S=i(12),I=i(12),J=i(12),N=i(192),Q=i(256),V=i(114),W=i(16),X=i(2),Y=i(128),_=i(128),tt=i(256),et=i(2),nt=i(128),ot=i(128),rt=i(256),O=i(768<<o+s),it=(1<<c)-1,st=(1<<s)-1,v=(w,h,R,l,z)=>n.bit(w,0)===0?B(n,h,z<<3,3):n.bit(w,1)===0?8+B(n,R,z<<3,3):16+B(n,l,0,8),p,D=!1;if(y)try{p=new Uint8Array(M)}catch{k()}else p=new Uint8Array(65536),D=!0;let a=0,G=w=>{if(a+w<=p.length)return;D||k();let h=p.length;for(;h<a+w;)h*=2;let R=new Uint8Array(h);R.set(p),p=R},r=0,u=0,A=0,U=0,T=0;for(;!(y&&a===M);){let w=a&it;if(n.bit(b,(r<<4)+w)===0){let l=a===0?0:p[a-1],g=(((a&st)<<o)+(l>>>8-o))*768,f=1;if(r<7)do f=f<<1|n.bit(O,g+f);while(f<256);else{u>=a&&k();let L=p[a-u-1];do{let j=L>>>7&1;L=L<<1&255;let H=n.bit(O,g+(1+j<<8)+f);if(f=f<<1|H,j!==H){for(;f<256;)f=f<<1|n.bit(O,g+f);break}}while(f<256)}G(1),p[a++]=f,r=r<4?0:r<10?r-3:r-6;continue}let h;if(n.bit(m,r)!==0){if(h=0,n.bit(S,r)===0)n.bit(N,(r<<4)+w)===0&&(r=r<7?9:11,h=1);else{let l;n.bit(I,r)===0?l=A:(n.bit(J,r)===0?l=U:(l=T,T=U),U=A),A=u,u=l}h===0&&(h=v(et,nt,ot,rt,w)+2,r=r<7?8:11)}else{T=U,U=A,A=u;let l=v(X,Y,_,tt,w);h=l+2,r=r<7?7:10;let z=l<4?l:3,g=B(n,Q,z<<6,6);if(g<4)u=g;else{let f=(g>>>1)-1;u=(2|g&1)*2**f,g<14?u+=$(n,V,u-g-1,f):(u+=n.direct(f-4)*16,u+=$(n,W,0,4))}if(u===4294967295){y&&a!==M&&k();break}}u>=a&&k(),G(h);let R=a-u-1;for(let l=0;l<h;l++)p[a++]=p[R++]}return D?p.slice(0,a):p}function ft(e){return F(q(Z(K(e,\"E\"))))}async function wt(e){return ft(e)}return{UtfpackError:E,unpack:wt,unpackSync:ft}})();",
    "utfpack/lzma-dense": "var utfpack=(()=>{\"use strict\";function z(){throw Error(\"utfpack: corrupt data\")}function Q(e){let t=0,n=()=>{let o=0,l=1,c;do t>=e.length&&z(),c=e[t++],o+=(c&127)*l,l*=128;while(c>127);return o},r=o=>{o>e.length-t&&z()},s=new TextDecoder(\"utf-8\",{ignoreBOM:!0,fatal:!0}),f=o=>{try{return s.decode(o)}catch{return z()}},a=[],u=n();r(u);for(let o=u;o>0;o--){let l=n();r(l);let c=f(e.subarray(t,t+=l));a.push([c,n()])}let i={};for(let[o,l]of a){let c=Math.floor(l/2);r(c),Object.hasOwn(i,o)&&z();let y=e.subarray(t,t+=c);Object.defineProperty(i,o,{value:l%2?f(y):y.slice(),enumerable:!0,writable:!0,configurable:!0})}return t!==e.length&&z(),i}var C=class extends Error{code;constructor(t,n){super(n??`utfpack: ${t}`),this.name=\"UtfpackError\",this.code=t}};var V=new WeakMap,X=new WeakMap,Y=new WeakMap;function gt(e){return e.toString(2).length}function et(e){return gt(e)-1>>3}function wt(e){let t=Y.get(e);if(t===void 0){let n=e.length>>1;t=new Uint32Array(n+1);for(let r=0;r<n;r++)t[r+1]=t[r]+e[r*2+1];Y.set(e,t)}return t}function xt(e,t){let n=e.ranges,r=wt(n),s=0,f=(n.length>>1)-1;for(;s<=f;){let a=s+f>>1,u=n[a*2],i=n[a*2+1];if(t<u)f=a-1;else if(t>=u+i)s=a+1;else return r[a]+(t-u)}return-1}function nt(e){let t=V.get(e);if(t!==void 0)return t;let n=e.classes,r=n.length,s=e.L,f=new Array(s+1);f[0]=1n;for(let i=1;i<=s;i++){let o=0n;for(let l=0;l<r;l++){let c=n[l].width;i>=c&&(o+=BigInt(n[l].count)*f[i-c])}f[i]=o}let a=new Array(s+1);for(let i=0;i<=s;i++){let o=new Array(r+1),l=0n;o[0]=0n;for(let c=0;c<r;c++){let y=n[c].width;i>=y&&(l+=BigInt(n[c].count)*f[i-y]),o[c+1]=l}a[i]=o}let u={L:s,K:et(f[s]),a:f,off:a};return V.set(e,u),X.set(e,{counts:n.map(i=>BigInt(i.count)),widths:n.map(i=>i.width)}),u}function _(e){let t=X.get(e);return t===void 0&&(nt(e),t=X.get(e)),t}function mt(e,t){if(t===0)return new Uint8Array(0);let n=new Uint8Array(t),r=e.toString(16);r=r.padStart(t*2,\"0\");for(let s=0;s<t;s++)n[s]=parseInt(r.slice(s*2,s*2+2),16);return n}function tt(e,t){if(e>=1n<<BigInt(8*t))throw new C(\"bad-value\");return mt(e,t)}function ot(e,t){if(t.length===0)throw new C(\"bad-length\");let n=nt(e),r=e.classes,s=r.length,f=_(e).counts,a=_(e).widths,u=n.L,i=n.K,o=[],l=0n,c=0;for(let k=0;k<t.length;){let T=t.codePointAt(k);k+=T>65535?2:1;let U=-1,O=-1;for(let M=0;M<s;M++){let D=xt(r[M],T);if(D>=0){U=M,O=D;break}}if(U<0)throw new C(\"invalid-char\");let I=c+a[U];if(I>u)throw new C(\"bad-length\");l=n.off[I][U]+l*f[U]+BigInt(O),c=I,c===u&&(o.push(tt(l,i)),l=0n,c=0)}c>0&&o.push(tt(l,et(n.a[c])));let y=0;for(let k of o)y+=k.length;let E=new Uint8Array(y),K=0;for(let k of o)E.set(k,K),K+=k.length;return E}function rt(e,t){if(typeof e!=\"string\"||e[0]!==t)throw new C(\"bad-format\");return e.slice(1)}var st={name:\"dense\",classes:[{count:91,width:1,ranges:[32,2,35,25,61,31,93,3,97,30]},{count:1878,width:2,ranges:[160,13,174,1362,1542,22,1565,192,1758,49,1808,240]},{count:61371,width:3,ranges:[2048,144,2194,80,2275,3883,6159,2044,8208,24,8239,49,8293,1,8304,46992,57344,7632,65008,271,65280,249,65532,2]}],L:1024};var bt=\"utfpack: corrupt LZMA data\";function L(){throw new Error(bt)}function p(e){return new Uint16Array(e).fill(1024)}var N=class{src;pos;range;code;constructor(t){(t.length<5||t[0]!==0)&&L(),this.src=t,this.pos=5,this.range=4294967295,this.code=(t[1]<<24|t[2]<<16|t[3]<<8|t[4])>>>0}byte(){return this.pos>=this.src.length&&L(),this.src[this.pos++]}normalize(){this.range<16777216&&(this.range=this.range<<8>>>0,this.code=(this.code<<8|this.byte())>>>0)}bit(t,n){let r=t[n],s=(this.range>>>11)*r;return this.code<s?(this.range=s,t[n]=r+(2048-r>>5),this.normalize(),0):(this.range=this.range-s>>>0,this.code=this.code-s>>>0,t[n]=r-(r>>5),this.normalize(),1)}direct(t){let n=0;for(;t-- >0;)this.range>>>=1,this.code>=this.range?(this.code=this.code-this.range>>>0,n=n<<1|1):n<<=1,this.normalize();return n}};function j(e,t,n,r){let s=1;for(let f=0;f<r;f++)s=s<<1|e.bit(t,n+s);return s-(1<<r)}function it(e,t,n,r){let s=1,f=0;for(let a=0;a<r;a++){let u=e.bit(t,n+s);s=s<<1|u,f|=u<<a}return f}function ct(e){e.length<13&&L();let t=e[0];t>=225&&L();let n=t%9,r=Math.floor(t/9)%5,s=Math.floor(t/45),f=(e[5]|e[6]<<8|e[7]<<16|e[8]<<24)>>>0,a=(e[9]|e[10]<<8|e[11]<<16|e[12]<<24)>>>0,u=!(f===4294967295&&a===4294967295),i=a*4294967296+f,o=new N(e.subarray(13)),l=p(192),c=p(12),y=p(12),E=p(12),K=p(12),k=p(192),T=p(256),U=p(114),O=p(16),I=p(2),M=p(128),D=p(128),ft=p(256),lt=p(2),at=p(128),ut=p(128),ht=p(256),F=p(768<<n+r),pt=(1<<s)-1,dt=(1<<r)-1,Z=(B,b,S,w,v)=>o.bit(B,0)===0?j(o,b,v<<3,3):o.bit(B,1)===0?8+j(o,S,v<<3,3):16+j(o,w,0,8),m,G=!1;if(u)try{m=new Uint8Array(i)}catch{L()}else m=new Uint8Array(65536),G=!0;let g=0,$=B=>{if(g+B<=m.length)return;G||L();let b=m.length;for(;b<g+B;)b*=2;let S=new Uint8Array(b);S.set(m),m=S},h=0,x=0,R=0,P=0,W=0;for(;!(u&&g===i);){let B=g&pt;if(o.bit(l,(h<<4)+B)===0){let w=g===0?0:m[g-1],A=(((g&dt)<<n)+(w>>>8-n))*768,d=1;if(h<7)do d=d<<1|o.bit(F,A+d);while(d<256);else{x>=g&&L();let H=m[g-x-1];do{let q=H>>>7&1;H=H<<1&255;let J=o.bit(F,A+(1+q<<8)+d);if(d=d<<1|J,q!==J){for(;d<256;)d=d<<1|o.bit(F,A+d);break}}while(d<256)}$(1),m[g++]=d,h=h<4?0:h<10?h-3:h-6;continue}let b;if(o.bit(c,h)!==0){if(b=0,o.bit(y,h)===0)o.bit(k,(h<<4)+B)===0&&(h=h<7?9:11,b=1);else{let w;o.bit(E,h)===0?w=R:(o.bit(K,h)===0?w=P:(w=W,W=P),P=R),R=x,x=w}b===0&&(b=Z(lt,at,ut,ht,B)+2,h=h<7?8:11)}else{W=P,P=R,R=x;let w=Z(I,M,D,ft,B);b=w+2,h=h<7?7:10;let v=w<4?w:3,A=j(o,T,v<<6,6);if(A<4)x=A;else{let d=(A>>>1)-1;x=(2|A&1)*2**d,A<14?x+=it(o,U,x-A-1,d):(x+=o.direct(d-4)*16,x+=it(o,O,0,4))}if(x===4294967295){u&&g!==i&&L();break}}x>=g&&L(),$(b);let S=g-x-1;for(let w=0;w<b;w++)m[g++]=m[S++]}return G?m.slice(0,g):m}function yt(e){return Q(ct(ot(st,rt(e,\"F\"))))}async function Et(e){return yt(e)}return{UtfpackError:C,unpack:Et,unpackSync:yt}})();",
}

_GLOBAL_PREFIX = 'var utfpack='
_ENTRIES = tuple(DECODER_BYTES)
_CODECS = ('deflate', 'lzma')
_FORMATS = ('base91', 'base64', 'dense')
# The first character of a string: _MARKERS[codec index * 3 + format index].
_MARKERS = 'ABCDEF'
_EMIT_MODES = ('module', 'string', 'script', 'html')


def _error(message):
    return ValueError('utfpack: ' + message)


# ---------------------------------------------------------------- identifiers

# Names that are valid JS identifiers but not usable as --name, a scene name or
# --global (the same list as RESERVED_NAMES in src/pack.ts).
_RESERVED_NAMES = (
    # ECMAScript reserved words
    'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
    'default', 'delete', 'do', 'else', 'enum', 'export', 'extends', 'false',
    'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'new',
    'null', 'return', 'super', 'switch', 'this', 'throw', 'true', 'try',
    'typeof', 'var', 'void', 'while', 'with', 'yield',
    # strict-mode reserved words and contextual keywords
    'let', 'static', 'implements', 'interface', 'package', 'private',
    'protected', 'public', 'await',
    # window properties
    'globalThis', 'window', 'self', 'top', 'parent', 'frames', 'opener',
    'document', 'location', 'name', 'history', 'navigator', 'screen',
    'origin', 'closed', 'length', 'status', 'frameElement', 'customElements',
    'localStorage', 'sessionStorage', 'indexedDB', 'crypto', 'performance',
    'caches',
    # built-in objects and functions of JavaScript and of the browser, which an
    # assignment would replace for the whole page (including the decoder)
    'Object', 'Function', 'Array', 'Number', 'String', 'Boolean', 'Symbol',
    'BigInt', 'Math', 'JSON', 'Reflect', 'Proxy', 'Promise', 'Date', 'RegExp',
    'Error', 'TypeError', 'RangeError', 'SyntaxError', 'ReferenceError',
    'EvalError', 'URIError', 'AggregateError', 'Map', 'Set', 'WeakMap',
    'WeakSet', 'WeakRef', 'FinalizationRegistry', 'ArrayBuffer',
    'SharedArrayBuffer', 'DataView', 'Atomics', 'Int8Array', 'Uint8Array',
    'Uint8ClampedArray', 'Int16Array', 'Uint16Array', 'Int32Array',
    'Uint32Array', 'Float16Array', 'Float32Array', 'Float64Array',
    'BigInt64Array', 'BigUint64Array', 'Intl', 'Iterator', 'isFinite', 'isNaN',
    'parseFloat', 'parseInt', 'encodeURI', 'encodeURIComponent', 'decodeURI',
    'decodeURIComponent', 'escape', 'unescape', 'console', 'fetch', 'Response',
    'Request', 'Headers', 'URL', 'URLSearchParams', 'TextDecoder', 'TextEncoder',
    'DecompressionStream', 'CompressionStream', 'ReadableStream',
    'WritableStream', 'TransformStream', 'Blob', 'File', 'FileReader', 'atob',
    'btoa', 'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval',
    'queueMicrotask', 'structuredClone', 'requestAnimationFrame', 'alert',
    'confirm', 'prompt', 'open', 'close', 'print', 'postMessage', 'event',
    'external', 'module', 'require', 'exports', 'define',
    # global values and special names
    'undefined', 'NaN', 'Infinity', 'eval', 'arguments', '__proto__',
    'constructor', 'prototype', 'hasOwnProperty', 'toString', 'valueOf',
)
_RESERVED = frozenset(_RESERVED_NAMES)


def _is_identifier(value):
    # Same rule as the Node side: /^[A-Za-z_$][A-Za-z0-9_$]*$/ (ASCII only).
    if not value:
        return False
    first = value[0]
    if not (('a' <= first <= 'z') or ('A' <= first <= 'Z') or first in '_$'):
        return False
    for ch in value[1:]:
        if not (('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9')
                or ch in '_$'):
            return False
    return True


def _check_identifier(value, label):
    if not isinstance(value, str) or not _is_identifier(value):
        raise _error('%s is not a JS identifier: %s' % (label, value))
    if value in _RESERVED:
        raise _error('%s is a reserved name: %s' % (label, value))


def _check_not_global(value, global_name, label):
    if value == global_name:
        raise _error('%s is the same as the decoder global name: %s'
                     % (label, value))


# ----------------------------------------------------------------- base91

_ALPHABET = ''.join(
    chr(cp) for cp in range(0x20, 0x7F) if cp not in (0x22, 0x3C, 0x5C, 0x60)
)


def encode_base91(data):
    b = 0
    n = 0
    out = []
    for byte in data:
        b |= byte << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out.append(_ALPHABET[v % 91])
            out.append(_ALPHABET[v // 91])
    if n:
        out.append(_ALPHABET[b % 91])
        if n > 7 or b > 90:
            out.append(_ALPHABET[b // 91])
    return ''.join(out)


def encode_base64(data):
    return base64.b64encode(bytes(data)).decode('ascii')


# ------------------------------------------------------------------ dense
#
# Enumerative coding over three character classes (1, 2 and 3 UTF-8 bytes
# wide) in blocks of L = 1024 bytes of output; the same profile as `dense` in
# src/profiles.ts.

# The 2-byte and 3-byte classes leave out the format characters (general
# category Cf) as fixed ranges: U+00AD, U+0600-0605, U+061C, U+06DD, U+070F;
# U+0890, U+0891, U+08E2, U+180E, U+200B-200F, U+202A-202E, U+2060-2064,
# U+2066-206F, U+FFF9-FFFB.
_DENSE_COUNTS = (91, 1878, 61371)
_DENSE_WIDTHS = (1, 2, 3)
_DENSE_RANGES = (
    (0x20, 2, 0x23, 25, 0x3D, 31, 0x5D, 3, 0x61, 30),
    (0xA0, 13, 0xAE, 1362, 0x606, 22, 0x61D, 192, 0x6DE, 49, 0x710, 240),
    (
        0x800, 144,
        0x892, 80,
        0x8E3, 3883,
        0x180F, 2044,
        0x2010, 24,
        0x202F, 49,
        0x2065, 1,
        0x2070, 46992,
        0xE000, 7632,
        0xFDF0, 271,
        0xFF00, 249,
        0xFFFC, 2,
    ),
)
_DENSE_L = 1024


def _log256_floor(value):
    if value <= 0:
        raise _error('log256 of a non-positive value')
    return (value.bit_length() - 1) // 8


class _Dense(object):
    def __init__(self):
        counts = _DENSE_COUNTS
        widths = _DENSE_WIDTHS
        n = len(counts)
        L = _DENSE_L

        self.chars = []
        for ranges, count in zip(_DENSE_RANGES, counts):
            table = []
            for i in range(0, len(ranges), 2):
                start = ranges[i]
                table.extend(chr(start + k) for k in range(ranges[i + 1]))
            if len(table) != count:
                raise _error('dense range total %d != count %d'
                             % (len(table), count))
            self.chars.append(table)

        a = [0] * (L + 1)
        a[0] = 1
        for m in range(1, L + 1):
            total = 0
            for i in range(n):
                if m >= widths[i]:
                    total += counts[i] * a[m - widths[i]]
            a[m] = total
        self.a = a
        self.K = _log256_floor(a[L])

        off = []
        for m in range(L + 1):
            row = [0] * (n + 1)
            running = 0
            for i in range(n):
                if m >= widths[i]:
                    running += counts[i] * a[m - widths[i]]
                row[i + 1] = running
            off.append(row)
        self.off = off

    def tail_length(self, r):
        target = 256 ** r
        lo, hi = 1, _DENSE_L
        if self.a[hi] < target:
            raise _error('no tail length for r=%d' % r)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.a[mid] >= target:
                hi = mid
            else:
                lo = mid + 1
        return lo, _log256_floor(self.a[lo])

    def encode_block(self, X, m):
        counts = _DENSE_COUNTS
        widths = _DENSE_WIDTHS
        chars = self.chars
        off = self.off
        out = []
        while m > 0:
            row = off[m]
            i = 0
            while i < 2 and X >= row[i + 1]:
                i += 1
            X, idx = divmod(X - row[i], counts[i])
            m -= widths[i]
            out.append(chars[i][idx])
        if m != 0 or X != 0:
            raise _error('leftover value while encoding')
        out.reverse()
        return ''.join(out)

    def encode(self, data):
        K = self.K
        blocks = []
        pos = 0
        n = len(data)
        while n - pos >= K:
            X = int.from_bytes(data[pos:pos + K], 'big')
            blocks.append(self.encode_block(X, _DENSE_L))
            pos += K
        r = n - pos
        if r > 0:
            Lp, k = self.tail_length(r)
            X = int.from_bytes(bytes(data[pos:]) + b'\x00' * (k - r), 'big')
            blocks.append(self.encode_block(X, Lp))
        return ''.join(blocks)


_dense_engine = None


def encode_dense(data):
    global _dense_engine
    if _dense_engine is None:
        _dense_engine = _Dense()
    return _dense_engine.encode(bytes(data))


def _encode_format(data, codec, fmt):
    # the marker of the codec and format, then the encoded bytes
    marker = _MARKERS[_CODECS.index(codec) * 3 + _FORMATS.index(fmt)]
    if fmt == 'base91':
        return marker + encode_base91(data)
    if fmt == 'base64':
        return marker + encode_base64(data)
    return marker + encode_dense(data)


# -------------------------------------------------------------- container

def _varint(value):
    out = bytearray()
    while value >= 0x80:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def _is_text(data):
    try:
        data.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def _prepare_entries(files):
    entries = []
    for name, data in files.items():
        if not isinstance(name, str):
            raise _error('file name must be a string: %r' % (name,))
        if isinstance(data, str):
            try:
                data = data.encode('utf-8')
            except UnicodeEncodeError:
                raise _error('malformed file data (lone surrogate): %s' % name)
        elif isinstance(data, (bytes, bytearray, memoryview)):
            data = bytes(data)
        else:
            raise _error('file data must be a str or bytes')
        entries.append((name, data))
    # UTF-16 code unit order of the names, the same order as the Node packer.
    entries.sort(key=lambda item: _utf16_key(item[0]))
    return entries


def pack_container(entries):
    """Container (D-1): varint(count), then per entry varint(name bytes), the
    name (UTF-8), varint(length * 2 + text flag), then all data."""
    seen = set()
    head = [_varint(len(entries))]
    body = []
    for name, data in entries:
        if name in seen:
            raise _error('duplicate entry name: %s' % name)
        seen.add(name)
        try:
            raw_name = name.encode('utf-8')
        except UnicodeEncodeError:
            raise _error('malformed file name: %s' % name)
        head.append(_varint(len(raw_name)))
        head.append(raw_name)
        head.append(_varint(len(data) * 2 + (1 if _is_text(data) else 0)))
        body.append(data)
    return b''.join(head) + b''.join(body)


# ------------------------------------------------------------ compression

def _need_zlib():
    if zlib is None:
        raise _error('the zlib module is required (this Python was built '
                     'without zlib)')


def _compress_deflate(data):
    _need_zlib()
    c = zlib.compressobj(9, zlib.DEFLATED, -15, 9)
    return c.compress(data) + c.flush()


def _compress_lzma(data):
    if lzma is None:
        raise _error('this Python has no lzma module (it was built without '
                     'liblzma); use --codec deflate')
    raw = lzma.compress(
        data,
        format=lzma.FORMAT_RAW,
        filters=[{'id': lzma.FILTER_LZMA1, 'preset': 9 | lzma.PRESET_EXTREME}],
    )
    lc, lp, pb = 3, 0, 2
    header = bytes([(pb * 5 + lp) * 9 + lc]) \
        + (64 * 1024 * 1024).to_bytes(4, 'little') \
        + len(data).to_bytes(8, 'little')
    return header + raw


def _compress(data, codec):
    if codec == 'deflate':
        return _compress_deflate(data)
    return _compress_lzma(data)


def _entry_of(codec, fmt):
    # the package entry of the decoder for one codec and format
    if codec == 'deflate':
        return 'utfpack/' + fmt
    return 'utfpack/lzma' if fmt == 'base91' else 'utfpack/lzma-' + fmt


def _decoder_size(table, entry):
    if entry not in table:
        raise _error('no decoder size for %s' % entry)
    return table[entry]


def _validate_options(codec, fmt, emit_mode='module'):
    if codec not in ('auto',) + _CODECS:
        raise _error('unknown codec: %s' % (codec,))
    if fmt not in ('auto',) + _FORMATS:
        raise _error('unknown format: %s' % (fmt,))
    if emit_mode not in _EMIT_MODES:
        raise _error('unknown emit mode: %s' % (emit_mode,))


def _candidates(codec, fmt, ascii_only):
    if codec == 'auto':
        codecs = ['deflate'] + (['lzma'] if lzma is not None else [])
    else:
        codecs = [codec]
    formats = list(_FORMATS) if fmt == 'auto' else [fmt]
    if ascii_only and fmt == 'dense':
        raise _error('ascii cannot be combined with the dense format')
    allow_dense = not ascii_only
    return codecs, formats, allow_dense


def _select(containers, codec, fmt, ascii_only, table, embed_decoder):
    # Encode every container with each allowed codec and format and keep the
    # smallest candidate: the sum of the strings in UTF-8 bytes, plus the
    # decoder of the entry with embed_decoder.  The first candidate wins a tie.
    codecs, formats, allow_dense = _candidates(codec, fmt, ascii_only)
    best = None
    for c in codecs:
        # compress once per container and codec (not once per format)
        data = [_compress(container, c) for container in containers]
        for f in formats:
            if f == 'dense' and not allow_dense:
                continue
            entry = _entry_of(c, f)
            strings = [_encode_format(d, c, f) for d in data]
            size = _decoder_size(table, entry) if embed_decoder else 0
            for s in strings:
                size += len(s.encode('utf-8'))
            if best is None or size < best['size']:
                best = {'codec': c, 'format': f, 'entry': entry,
                        'strings': strings, 'size': size}
    if best is None:
        raise _error('no candidate format')
    return best


def pack(files, codec='auto', format='auto', ascii=False, emit='module',
         embed_decoder=False):
    """Pack `files` (name -> str or bytes) into one string.

    ascii=True leaves the dense format out, so the string is printable ASCII.
    By default the output is data only, the page loads a decoder itself, and
    the smallest string (in UTF-8 bytes) is chosen.  embed_decoder=True says
    the decoder of the chosen format goes into the output or the bundle:
    `emit` 'script' and 'html' then add GLOBAL_DECODER_BYTES to each
    candidate, 'module' and 'string' DECODER_BYTES.

    Returns {'string', 'codec', 'format', 'entry', 'module'}; 'entry' is the
    package entry of the decoder for this codec and format alone.
    """
    _validate_options(codec, format, emit)
    table = GLOBAL_DECODER_BYTES if emit in ('script', 'html') \
        else DECODER_BYTES
    container = pack_container(_prepare_entries(files))
    best = _select([container], codec, format, ascii, table, embed_decoder)
    string = best['strings'][0]
    return {
        'string': string,
        'codec': best['codec'],
        'format': best['format'],
        'entry': best['entry'],
        'module': _module_text(string,
                               best['entry'] if embed_decoder else None),
    }


def pack_scenes(scenes, codec='auto', format='auto', ascii=False,
                emit='script', embed_decoder=False):
    """Pack several scenes (name -> files) with one shared codec and format.

    Returns {'codec', 'format', 'entry', 'strings'} where strings maps each
    scene name to its string.  Scenes are always rendered as script or html, so
    with embed_decoder=True the candidates count GLOBAL_DECODER_BYTES (`emit`
    is accepted for symmetry with pack()).
    """
    _validate_options(codec, format, emit)
    names = list(scenes)
    if not names:
        raise _error('no scenes')
    for n in names:
        if not scenes[n]:
            raise _error('empty scene: %s' % (n,))
    containers = [pack_container(_prepare_entries(scenes[n])) for n in names]
    best = _select(containers, codec, format, ascii, GLOBAL_DECODER_BYTES,
                   embed_decoder)
    return {
        'codec': best['codec'],
        'format': best['format'],
        'entry': best['entry'],
        'strings': dict(zip(names, best['strings'])),
    }


# ------------------------------------------------------------------- emit

def _json_string(s):
    # Same as JS JSON.stringify for a well-formed string: escapes ", \,
    # control characters; leaves U+2028, U+2029 and non-ASCII as they are.
    return json.dumps(s, ensure_ascii=False)


def decoder_script(entry, global_name='utfpack'):
    """The global-version decoder for `entry` (no trailing newline)."""
    text = _DECODERS.get(entry)
    if text is None:
        raise _error('unknown entry: %s' % (entry,))
    if global_name is not None:
        _check_identifier(global_name, 'global')
    if not text.startswith(_GLOBAL_PREFIX):
        raise _error('decoder for %s does not start with %s'
                     % (entry, _GLOBAL_PREFIX))
    if global_name is None or global_name == 'utfpack':
        return text
    return 'var %s=%s' % (global_name, text[len(_GLOBAL_PREFIX):])


def decoder_sri(entry):
    """`sha384-<base64>` of the classic decoder of an entry (UTF-8); equals the
    value in dist/cdn/sri.json for `<name>.js`, whatever host serves the file."""
    digest = hashlib.sha384(decoder_script(entry).encode('utf-8')).digest()
    return 'sha384-' + base64.b64encode(digest).decode('ascii')


_INLINE_SCRIPT = re.compile(r'<script>(.*?)</script>', re.S)


def csp_hashes(html):
    """The CSP source expressions ("'sha256-...'") of the inline scripts in an
    html output, in order."""
    return ["'sha256-%s'" % base64.b64encode(
        hashlib.sha256(body.encode('utf-8')).digest()).decode('ascii')
        for body in _INLINE_SCRIPT.findall(html)]


def _module_text(string, entry=None):
    # data only, or with `entry` a module that imports that package entry
    if entry is None:
        return 'export default %s;\n' % _json_string(string)
    return 'import{unpack}from%s;export default unpack(%s);\n' % (
        _json_string(entry), _json_string(string))


def _emit_text(string, mode, name, global_name, sync):
    fn = 'unpackSync' if sync else 'unpack'
    script = 'globalThis.%s=%s.%s(%s);\n' % (
        name, global_name, fn, _json_string(string))
    if mode == 'script':
        return script
    return '<script>' + script[:-1] + '</script>\n'


def _check_emit_options(codec, global_name, sync):
    global_name = 'utfpack' if global_name is None else global_name
    _check_identifier(global_name, 'global')
    sync = bool(sync)
    if sync and codec != 'lzma':
        raise _error('sync needs the lzma codec')
    return global_name, sync


def _decoder_prefix(entry, mode, global_name):
    text = decoder_script(entry, global_name)
    return text + '\n' if mode == 'script' \
        else '<script>' + text + '</script>\n'


def emit(result, mode, name='utfpackData', global_name='utfpack', sync=False,
         embed_decoder=False):
    """Render a pack() result as 'module', 'string', 'script' or 'html'.

    The output is data only: 'module' is `export default "<string>";`,
    'script' and 'html' hold the data script that calls the decoder global,
    which the page loads before it.  embed_decoder=True puts the decoder of
    the chosen format into the output: 'script' and 'html' start with the
    inline classic decoder, 'module' imports the package entry
    ('utfpack/lzma') for a bundler and exports the unpacked data.
    """
    if mode not in _EMIT_MODES:
        raise _error('unknown emit mode: %s' % (mode,))
    embed = bool(embed_decoder)
    if mode == 'module':
        return _module_text(result['string'],
                            result['entry'] if embed else None)
    if mode == 'string':
        return result['string']
    name = 'utfpackData' if name is None else name
    _check_identifier(name, 'name')
    global_name, sync = _check_emit_options(
        result['codec'], global_name, sync)
    _check_not_global(name, global_name, 'name')
    prefix = _decoder_prefix(result['entry'], mode, global_name) \
        if embed else ''
    return prefix + _emit_text(result['string'], mode, name, global_name, sync)


def emit_scenes(result, mode, global_name='utfpack', sync=False,
                embed_decoder=False):
    """Render a pack_scenes() result: one data script per scene (mode 'script'
    or 'html'), after the inline decoder with embed_decoder=True."""
    if mode not in ('script', 'html'):
        raise _error('unknown emit mode: %s' % (mode,))
    global_name, sync = _check_emit_options(
        result['codec'], global_name, sync)
    names = list(result['strings'])
    for name in names:
        _check_identifier(name, 'scene name')
        _check_not_global(name, global_name, 'scene name')
    out = [_decoder_prefix(result['entry'], mode, global_name)
           if embed_decoder else '']
    for name in names:
        out.append(_emit_text(result['strings'][name], mode, name,
                              global_name, sync))
    return ''.join(out)


# -------------------------------------------------------------------- CLI

class _CliError(Exception):
    pass


def _fail(message):
    raise _CliError(message)


def _utf16_key(s):
    # JS compares strings by UTF-16 code unit; this key sorts the same way.
    return s.encode('utf-16-be', 'surrogatepass')


def _skip_symlink(path):
    sys.stderr.write('utfpack: skipping symlink: %s\n' % path)


def _file_id(path):
    try:
        stat = os.stat(path)
    except OSError:
        return None
    return (stat.st_dev, stat.st_ino)


def _make_exclude(output):
    # The output file, so that a later run does not pack its own output. The
    # device and inode also catch symlinks and case-insensitive paths.
    if output is None:
        return None
    return (os.path.abspath(output), _file_id(output))


def _is_excluded(path, exclude):
    if exclude is None:
        return False
    if os.path.abspath(path) == exclude[0]:
        return True
    return exclude[1] is not None and _file_id(path) == exclude[1]


def _walk(directory, out, exclude):
    with os.scandir(directory) as it:
        entries = sorted(it, key=lambda e: _utf16_key(e.name))
    for entry in entries:
        path = os.path.join(directory, entry.name)
        if entry.is_symlink():
            _skip_symlink(path)
        elif entry.is_dir(follow_symlinks=False):
            _walk(path, out, exclude)
        elif entry.is_file(follow_symlinks=False):
            if not _is_excluded(path, exclude):
                out.append(path)


def _collect(paths, base_option, exclude=None):
    if not paths:
        _fail('no input paths')
    explicit_base = None if base_option is None else os.path.abspath(base_option)
    found = []
    for given in paths:
        absolute = os.path.abspath(given)
        if not os.path.exists(absolute):
            _fail('no such file or directory: %s' % given)
        if os.path.islink(absolute):
            _skip_symlink(given)
            continue
        base = explicit_base if explicit_base is not None \
            else os.path.dirname(absolute)
        files = []
        if os.path.isdir(absolute):
            _walk(absolute, files, exclude)
        elif os.path.isfile(absolute):
            if _is_excluded(absolute, exclude):
                _fail('the output file is also an input: %s' % given)
            files.append(absolute)
        else:
            _fail('not a regular file or directory: %s' % given)
        for file in files:
            name = os.path.relpath(file, base).replace(os.sep, '/')
            if name in ('', '.', '..') or name.startswith('../'):
                _fail('%s is outside the base directory' % file)
            with open(file, 'rb') as handle:
                found.append((name, handle.read()))
    found.sort(key=lambda item: _utf16_key(item[0]))
    for i in range(1, len(found)):
        if found[i][0] == found[i - 1][0]:
            _fail('duplicate name: %s' % found[i][0])
    return found


def _as_is_size(files):
    texts = {}
    for name, data in files:
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            return None
        if text.startswith('\ufeff'):
            text = text[1:]
        texts[name] = text
    source = 'export default %s;' % json.dumps(
        texts, ensure_ascii=False, separators=(',', ':'))
    return len(source.encode('utf-8'))


def _write_output(output, content):
    raw = content.encode('utf-8')
    if output is None:
        sys.stdout.flush()
        sys.stdout.buffer.write(raw)
        sys.stdout.buffer.flush()
    else:
        with open(output, 'wb') as handle:
            handle.write(raw)


def _pack_codec(args, script_output):
    # --sync works for lzma strings only: for script / html output a missing
    # --codec becomes lzma, and deflate with --sync is refused before packing.
    # With module / string output --sync is not used.
    sync = script_output and args.sync
    codec = args.codec if args.codec is not None \
        else ('lzma' if sync else 'auto')
    if sync and codec == 'deflate':
        _fail('--sync needs the lzma codec')
    return codec


def _check_output_args(args, mode):
    # same rules as the Node CLI
    if args.csp and mode != 'html':
        _fail('--csp needs --emit html, not %s' % mode)
    if args.ascii and args.format == 'dense':
        _fail('--ascii cannot be combined with --format dense')


def _write_csp(args, content):
    if args.csp:
        for value in csp_hashes(content):
            sys.stderr.write(value + '\n')


def _command_pack_scenes(args, output):
    if args.paths:
        _fail('--scene cannot be combined with input paths')
    if args.base is not None:
        _fail('--scene cannot be combined with --base')
    if args.name is not None:
        _fail('--scene cannot be combined with --name')
    if args.string:
        _fail('--scene cannot be combined with --string')
    emit_mode = args.emit if args.emit is not None else 'html'
    if emit_mode not in ('script', 'html'):
        _fail('--scene needs --emit script or html, not %s' % emit_mode)
    codec = _pack_codec(args, True)
    if args.global_name is not None:
        _check_identifier(args.global_name, '--global')
    _check_output_args(args, emit_mode)

    exclude = _make_exclude(output)
    record = {}
    for spec in args.scene:
        eq = spec.find('=')
        if eq <= 0:
            _fail('--scene needs <name>=<path>: %s' % spec)
        name, path = spec[:eq], spec[eq + 1:]
        _check_identifier(name, 'scene name')
        _check_not_global(name, args.global_name or 'utfpack', 'scene name')
        if name in record:
            _fail('duplicate scene name: %s' % name)
        if path == '':
            _fail('--scene needs <name>=<path>: %s' % spec)
        is_directory = os.path.isdir(path)
        files = _collect([path], path if is_directory else None, exclude)
        record[name] = dict(files)

    result = pack_scenes(record, codec=codec, format=args.format,
                         ascii=args.ascii, emit=emit_mode,
                         embed_decoder=args.embed_decoder)
    content = emit_scenes(result, emit_mode, global_name=args.global_name,
                          sync=args.sync, embed_decoder=args.embed_decoder)
    _write_output(output, content)

    decoder_bytes = GLOBAL_DECODER_BYTES[result['entry']] \
        if args.embed_decoder else 0
    scene_bytes = ' '.join(
        '%s=%d' % (name, len(string.encode('utf-8')))
        for name, string in result['strings'].items())
    sys.stderr.write(
        'codec=%s format=%s entry=%s decoder=%d scenes: %s output=%d\n' % (
            result['codec'], result['format'], result['entry'],
            decoder_bytes, scene_bytes, len(content.encode('utf-8'))))
    _write_csp(args, content)


def _command_pack(args):
    output = args.output
    if args.scene:
        _command_pack_scenes(args, output)
        return
    if args.string and args.emit is not None and args.emit != 'string':
        _fail('--string conflicts with --emit ' + args.emit)
    mode = 'string' if args.string else (args.emit or 'module')
    script_output = mode in ('script', 'html')
    codec = _pack_codec(args, script_output)
    _check_output_args(args, mode)
    # --name and --global are used (and checked) for script and html only
    name = args.name if args.name is not None else 'utfpackData'
    global_name = args.global_name if args.global_name is not None \
        else 'utfpack'
    if script_output:
        _check_identifier(name, '--name')
        _check_identifier(global_name, '--global')
        _check_not_global(name, global_name, '--name')

    files = _collect(args.paths, args.base, _make_exclude(output))
    if not files:
        _fail('no files to pack')
    result = pack(dict(files), codec=codec, format=args.format,
                  ascii=args.ascii, emit=mode,
                  embed_decoder=args.embed_decoder)
    content = emit(result, mode, name=name, global_name=global_name,
                   sync=args.sync, embed_decoder=args.embed_decoder)
    _write_output(output, content)

    size = _as_is_size(files)
    as_is = 'n/a' if size is None else '%d (not minified)' % size
    sys.stderr.write('codec=%s format=%s entry=%s output=%d as-is=%s\n' % (
        result['codec'], result['format'], result['entry'],
        len(content.encode('utf-8')), as_is))
    _write_csp(args, content)


def _command_decoder(args):
    if args.paths:
        _fail('decoder takes no input paths')
    if args.entry is None:
        _fail('decoder needs --entry <entry>')
    if args.entry not in _ENTRIES:
        _fail('unknown entry: %s' % args.entry)
    mode = args.emit if args.emit is not None else 'script'
    if mode not in ('script', 'html'):
        _fail('decoder needs --emit script or html, not %s' % mode)
    if args.global_name is not None:
        _check_identifier(args.global_name, '--global')
    text = decoder_script(args.entry, args.global_name)
    content = text + '\n' if mode == 'script' \
        else '<script>' + text + '</script>\n'
    _write_output(args.output, content)


def _build_parser():
    import argparse

    class Parser(argparse.ArgumentParser):
        def error(self, message):
            # usage errors look like every other error: one line, exit code 1
            sys.stderr.write('utfpack: %s\n' % message)
            raise SystemExit(1)

    parser = Parser(
        prog='utfpack_pack.py',
        description=('Pack files into one JavaScript-safe string for the '
                     'utfpack decoders (encoder only; decoding runs in the '
                     'browser).'),
        epilog=('Notes: deflate uses zlib level 9. The "as-is" size on stderr '
                'is not minified.'),
        allow_abbrev=False,
    )
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('command', choices=('pack', 'decoder'),
                        help='pack: pack files or scenes; decoder: print a '
                             'bundled global-version decoder')
    parser.add_argument('paths', nargs='*', help='files or folders to pack')
    parser.add_argument('-o', '--output', metavar='OUT',
                        help='output file (default: stdout)')
    parser.add_argument('--base', metavar='DIR',
                        help='names are relative to DIR (default: the parent '
                             'of each path)')
    parser.add_argument('--codec', choices=('auto', 'deflate', 'lzma'),
                        help='default auto; with --sync default lzma')
    parser.add_argument('--format',
                        choices=('auto', 'base91', 'base64', 'dense'),
                        default='auto')
    parser.add_argument('--ascii', action='store_true',
                        help='leave out the dense format, so the output is '
                             'printable ASCII')
    parser.add_argument('--emit', choices=_EMIT_MODES,
                        help='module (default), string, script or html; with '
                             '--scene or decoder: script or html')
    parser.add_argument('--string', action='store_true',
                        help='same as --emit string')
    parser.add_argument('--name', metavar='IDENT',
                        help='global variable that receives the data '
                             '(script and html output; default utfpackData)')
    parser.add_argument('--global', dest='global_name', metavar='IDENT',
                        help='global name of the decoder (default utfpack)')
    parser.add_argument('--sync', action='store_true',
                        help='use unpackSync (script and html output; lzma only)')
    parser.add_argument('--scene', action='append', metavar='NAME=PATH',
                        help='one scene; give it twice or more')
    parser.add_argument('--embed-decoder', action='store_true',
                        help='put the decoder of the chosen format into the '
                             'output and count its size when choosing (script '
                             'and html: the inline decoder; module: an import '
                             'of the package entry for a bundler)')
    parser.add_argument('--csp', action='store_true',
                        help='html output: print the sha256 of each inline '
                             'script to stderr (for CSP script-src)')
    parser.add_argument('--entry', choices=_ENTRIES, metavar='ENTRY',
                        help='decoder: one of ' + ', '.join(_ENTRIES))
    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_intermixed_args(argv)
    try:
        if args.command == 'pack':
            _command_pack(args)
        else:
            _command_decoder(args)
    except (_CliError, ValueError, OSError) as error:
        message = str(error)
        if message.startswith('utfpack: '):
            message = message[len('utfpack: '):]
        sys.stderr.write('utfpack: %s\n' % message)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
