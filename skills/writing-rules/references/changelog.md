# How to write a changelog

The changelog of a published tool (CHANGELOG, release notes) tells people who use the tool, and people who are considering it, about the new version. Readers read only the changelog to decide whether to update the tool to the new version and whether they must change how they use it. So each entry states what changed for the reader: what became possible, how behavior changed, and what the reader must do.

Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) for how to write it, and [Semantic Versioning](https://semver.org/) for version numbers. If you can read files or the web, open the two originals to check when in doubt. Agents tend to miss the following points.

- Write in an entry the changes the reader notices when using the tool. As Keep a Changelog requires, do not list commits or work records. The reader does not use the following to decide on an update, so leave them out: how the tool was built, what was compared to decide, and which sentence in which file was fixed. After writing an entry, check that the reader does not have to ask what changes for them.
- Give the detailed usage of a change as a link to the relevant section of the tool's README or guide. Do not copy the usage into the changelog.
- Divide one version's entries under subheadings by the Keep a Changelog types of change. Do not add a subheading for a type that has no entries.
- Write one change per entry, in the reader's terms. Name something inside the tool (a function, a file, an internal name) only when it is a name the reader uses (a command, a skill, a setting).
- When a change prevents the reader from continuing to use the tool unless they do something (rewrite settings, reinstall, stop using a feature), state in the entry what the reader must do.
- Collect changes before release under an "Unreleased" heading. When you release, change that heading to one with the version number and release date. Follow the heading form if the top of the changelog or the development guide defines one. If neither defines one, match how the previous versions in the changelog are written.

Use the subheading names, section wording, and phrasing that human-maintained changelogs in the document's language use. Use the language pack's `conventions.md` when it defines them.
