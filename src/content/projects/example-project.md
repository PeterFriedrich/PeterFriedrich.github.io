---
title: "Example project"
description: "The shape of a project entry — copy this file, replace everything, delete the original."
year: 2026
period: "2026"
status: "complete"
tags: ["python", "template"]
repo: "https://github.com/PeterFriedrich/cc-data-project-template"
featured: true
order: 10
draft: true
---

A project entry is a markdown file in `src/content/projects/`. The filename is
the URL: this one would serve at `/projects/example-project`.

## What it does

One or two paragraphs. Lead with what the thing is and who it was for, not with
the stack.

## How it works

The interesting decisions. What you tried that didn't work is usually the part
worth reading.

## What it gets wrong

The limits — the assumption the numbers rest on, the data quality issue you
worked around, the thing you'd do differently. A portfolio entry that claims no
weaknesses reads as one that hasn't been looked at closely.

## Frontmatter fields

| Field | Notes |
|---|---|
| `year` | Sort key for the index (number) |
| `period` | Optional display string, e.g. `"2021–2022"` — shown instead of `year` |
| `status` | `active` / `complete` / `archived` / `paused` |
| `featured` | `true` puts it on the home page |
| `order` | Tie-break within featured; lower sorts first |
| `repo`, `url` | Optional links, rendered in the header |
