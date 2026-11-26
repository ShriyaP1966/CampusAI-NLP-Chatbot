# Sample campus documents

Everything in this folder is **sample data for a fictional university** ("Northfield University"). Names, dates, fees, phone numbers and e-mail addresses are made up and do not describe any real institution.

## Format

One Markdown file per document and language: `<doc_id>.<lang>.md`.

```
---
doc_id: fees
title: Fees and payments
lang: en
---
## Tuition fees {#tuition}
Body text of the section.
```

- `doc_id` is shared by every translation of a document.
- Each `## Heading {#id}` starts a section. The id is shared across languages, so `fees#tuition` points at the same content in English, Hindi and Marathi.
- A section is the unit that is indexed, retrieved and cited. Keep each one short and about a single topic.

To use your own documents, put files in the same format in a separate folder and point `CAMPUSAI_DOCS_DIR` at it. Plain Markdown or text files without front matter are also accepted: the file name becomes the document id and the language defaults to English.
