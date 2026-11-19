---
name: tracking-visualization
description: >-
  Visualize existing analytics instrumentation and proposed tracking gaps on
  screenshots or design frames as a clickable, self-contained HTML report.
  Use for instrumentation inventories, event coverage reviews, tracking audits,
  gap analysis and developer-ready event specifications. Verify the correct source
  branch, inspect both business and global instrumentation, prefer existing
  dashboards and curated datasets before raw events, then populate and validate
  the supplied single-screen or multi-screen templates. Distinguish verified zero
  reports from missing events and unverified data. Hide gap priorities by default.
---

# Tracking Visualization

Explain what is implemented, what is actually reported and what is missing through clickable pins and a complete event inventory. Follow the user's language. The templates support English and Simplified Chinese via `CONFIG.lang` and a language selector; configured event descriptions remain in the language you write them in.

## Five-Step Workflow

1. **Identify the correct branch and inventory instrumentation.** Confirm the repository, feature version and branch before searching. Do not assume `main` or `master` contains new feature code; use it only when it is the verified target. Inspect both page/component calls and global SDK/router/delegated click instrumentation, including dimensions such as `area` and `target`. Consult the team's event registry and source implementation. Read [data channels](references/data-channels.md) and [workflow](references/workflow.md).
2. **Verify observed data.** Prefer existing dashboards, then curated datasets, then raw events. Record the period, population, environment, denominator, deduplication rule and provenance. Use only authorized sources supplied or approved for this project; this package contains no platform connectors. Zero is a verified query result, not a synonym for unavailable data.
3. **Identify gaps.** Compare instrumentation with the user's important tasks: entry, progress, submission, success/failure, recovery and cross-system return. Treat P0/P1/P2 as analytical categories; hide them in the report unless explicitly requested. Do not infer missing implementation merely because a query returned zero events or access was unavailable.
4. **Populate the supplied template.** Read [CONFIG specification](references/config-spec.md). Copy `assets/template-single.html` for one screen, or `assets/template-multi.html` for multiple screens/states, with `texture.jpg` and permitted raster screenshots. Edit only JSON inside `script#annotation-config` (`type="application/json"`). In the single-screen template also replace `img#screenshot`'s `src`. The runtime parses this JSON as `CONFIG`; do not insert executable configuration or change renderer logic per report.
5. **Validate, inspect and share.** Run `scripts/validate_annotation.py`; inspect pin/table toggle behavior, filtering, language switch, edge popups and hidden-pin single selection in a browser. Run `scripts/embed_images.py` before sharing a single HTML file and validate the resulting standalone file again. Deliver using the host Agent's file/link presentation mechanism. Publishing a report is a separate, explicitly authorized action.

## Required Inputs and Evidence

Confirm missing inputs only: product/page, repository and target branch, screenshot/design frames, important user journey, permitted analytics sources and reporting period. Default to 14 days only when appropriate and state that choice; do not invent date ranges or data.

When the user only has screenshots or an event list, produce a clearly labeled supplied-material review rather than pretend to have inspected code or live data. Keep unavailable evidence as `unverified` and state the limitation.

## Color and Status Contract

- `blue`: implemented page/system exposure events; `green`: implemented user interactions.
- `red`: proposed missing instrumentation only, with `suggest: true` and a matching gap row.
- `ok`: reporting verified; `empty`: verified zero events and users; `unverified`: not checked or inaccessible.
- `p0`, `p1`, `p2`: missing events. Render "Missing" by default, not the priority.
- `mark: "error"`: orange error-state badge, separate from missing tracking.
- Set `showPriority: true` only if the user explicitly asks for displayed priorities. Do not embed P0/P1/P2 tags in `action` names.
- P0: blocks a critical funnel explanation; P1: supports an experience hypothesis; P2: secondary/long-tail or cross-system return. Assign from this project's goals, not a universal severity rule.

## Pins, Inventory and Reporting Contracts

- Use screen-local positive pin IDs and globally unique inventory row IDs. Use `table[].pinLoc` (for example `S1-1 / S2-1`) to map a row to its screen-local pins; every pin needs exactly one corresponding row.
- Keep pin and row `action`, `color`, gap description and status flags consistent. Inventory-only events may omit `pinLoc`.
- `pos.x/y` are 0–100 percentages of the relevant image. Do not reuse one screen's coordinates for another.
- Each pin needs `action`, `title`, `desc`, `params`, `data`. For gaps, `desc` explains why and what to observe; `data` explains the decision that evidence could support. Do not repeat the same prose.
- Write developer-ready contracts: `parameter: type(required|optional) = enum1|enum2`; preserve verified code keys. Explicitly label proposed contracts and unknown enums; do not invent source locations.
- `meta`, `data`, descriptions and suggestions are plain text, not HTML. Use line breaks, not HTML tags. The renderer uses text-safe DOM APIs.

## Sharing and Safety

Use only images you are permitted to distribute. Redact personal records, credentials, account details and proprietary source information from reports. Do not collect raw user-entered text as a proposed parameter by default; prefer bounded categories or aggregate signals appropriate to the task.

The scripts do not execute page JavaScript or access network analytics. Image embedding preserves raster bytes, refuses traversal outside the report directory, does not fetch external images and never overwrites an existing output. SVG screenshots, remote image URLs and legacy executable CONFIG are not supported by this public version. Review user-supplied HTML before opening it: semantic validation is not a full security audit.

Bundled sample events/counts are fictional; `placeholder.png` is not a real product screenshot. Replace both before presenting an actual audit. Low counts alone do not establish inactivity or missing instrumentation.

## Resources

- `references/data-channels.md`: project-neutral evidence channels and authorization boundaries (English/Chinese).
- `references/workflow.md`: complete workflow, limitations and checks (English/Chinese).
- `references/config-spec.md`: JSON fields, consistency rules and examples (English/Chinese).
- `assets/template-single.html`, `assets/template-multi.html`: bilingual renderer and fictional examples.
- `assets/placeholder.png`, `assets/texture.jpg`: neutral placeholder and visual texture.
- `scripts/annotation_common.py`: shared JSON parsing and image path helpers.
- `scripts/validate_annotation.py`: non-executing JSON/path/JS syntax validation; Python 3.10+ and Node.js required.
- `scripts/embed_images.py`: standalone HTML exporter; Python 3.10+ standard library only.

```text
python3 scripts/validate_annotation.py report.html
python3 scripts/embed_images.py report.html report-standalone.html
python3 scripts/validate_annotation.py report-standalone.html
```

Keep the original installed Skill unchanged when preparing an open-source adaptation. Use the full Skill directory when installing; a Chinese reading document is documentation, not a second Skill.
