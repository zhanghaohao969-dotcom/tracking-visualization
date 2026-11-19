# Tracking Visualization

English | [简体中文](README.zh-CN.md)

**See existing analytics events and tracking gaps directly on the product screen.**

An Agent Skill that turns verified instrumentation, observed reporting and proposed gaps into an interactive HTML annotation report: clickable colored pins, event details, screen-level lists and a complete inventory.

## What It Includes

- Single-screen and multi-screen templates, retaining a light textured-glass layout.
- Blue for page exposure, green for user interactions, red for missing instrumentation.
- Pin/table highlighting, repeated-click closing, category filters and a per-screen show/hide switch.
- English and Simplified Chinese interface labels; event prose follows the content you provide.
- Independent per-screen popups and single focused pins when other pins are hidden.
- Gap priorities retained for analysis but **hidden by default**; show them only on explicit request.
- Explicit `unverified` data separate from verified zero (`empty`) and missing tracking.
- Python validation and standalone-image embedding tools.

## Install

Import the complete `skills/tracking-visualization/` folder into a Skill-compatible client according to that client's installation instructions. Keep the assets, references and scripts; `SKILL.md` alone is not enough. Cross-client triggering is not guaranteed or benchmarked.

The default instructions are in English, with a [Chinese reading version](docs/tracking-visualization.zh-CN.md). All three reference guides include English and Chinese. Install one Skill, not the reading document as another Skill.

## Try It

```text
Use tracking-visualization to review this checkout page. Use the verified feature branch, inspect both page and global events, compare the inventory with this authorized reporting export, and show tracking gaps without priorities.
```

Provide the page screenshot/design frames, repository and target branch or source excerpts, important user journey, permitted data sources/export, reporting period and definitions. If you only have screenshots or an event list, the Agent must label the result as a supplied-material review and leave unavailable evidence unverified.

## Workflow

1. Verify the source branch; inspect declared events, actual business calls and shared/global instrumentation.
2. Prefer existing dashboards, then curated datasets, then raw events. Use project-authorized sources only.
3. Identify gaps against the user journey; distinguish missing implementation from zero or unavailable data.
4. Fill the supplied single/multi template's JSON CONFIG; keep renderer logic unchanged per report.
5. Validate, inspect in a browser, embed local images, revalidate and share the standalone HTML.

The package contains **no analytics connectors or hosting API**. Repository access, browser operation and authorized analytics retrieval are host/client capabilities. It does not grant permissions or automatically connect to your business systems.

## Open the Demos

Open `skills/tracking-visualization/assets/template-single.html` or `template-multi.html` locally in a browser, keeping the supplied image files beside them. A language selector changes interface labels between English and Chinese; configured descriptions are not auto-translated.

The sample events, counts and pin positions are **fictional**. `placeholder.png` is a neutral illustration, not a product screenshot. Replace it and the data before presenting a real audit.

## Requirements and Commands

- Python 3.10+ for the scripts; no third-party Python packages.
- Node.js 18+ for JavaScript syntax validation.
- A modern browser for the interactive report.

From the Skill directory:

```bash
python3 scripts/validate_annotation.py assets/template-single.html
python3 scripts/embed_images.py assets/template-single.html report-standalone.html
python3 scripts/validate_annotation.py report-standalone.html
```

Embedding preserves original PNG/JPEG/GIF/WebP bytes; it does not downsample or convert animated GIFs. Use a fresh output filename: existing files are not overwritten. Keep referenced images within the input HTML directory. Remote image URLs and SVG screenshots are not supported by this public version.

## Configuration and Migration

See [CONFIG specification](skills/tracking-visualization/references/config-spec.md), [workflow](skills/tracking-visualization/references/workflow.md) and [evidence channels](skills/tracking-visualization/references/data-channels.md).

The public adaptation uses `<script type="application/json" id="annotation-config">` rather than executable `const CONFIG = {...}`. Strings are plain text, not HTML; JSON does not accept comments, functions or trailing commas. The runtime parses JSON into CONFIG. This is an intentional safety change, not drop-in support for legacy files.

Other public-version changes:

- Organization-specific resources, private URLs, dashboard/project IDs and deployment commands were removed.
- Pin/row mapping, action/color consistency, missing-event flags and verified zero/unknown states are checked more strictly.
- Legacy orange/purple event categories are not supported; use `mark:"error"` for orange error-state markers.
- Existing textured glass visuals are retained; dynamic text is rendered with text-safe DOM APIs.

## Privacy and Limits

Only include screenshots, source references and aggregate data you are permitted to share. Redact credentials, personal records and proprietary content. Tracking suggestions should favor necessary bounded categories over raw user-entered text.

The validator reads JSON and checks JavaScript syntax; it **does not execute page code** or query analytics. It is not a full sanitizer for hostile HTML: inspect unknown HTML before opening it. Image helpers refuse traversal outside the report directory and do not fetch remote files.

A zero result is not proof that nobody used a feature. Rollout, environment filters, delays or instrumentation failures may also explain it. Distinguish registered, implemented, deployed and observed evidence.

Publishing the Skill does not authorize publishing future customer screenshots, business data or generated reports.

## Repository Structure

```text
tracking-visualization/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── docs/tracking-visualization.zh-CN.md
├── tests/test_scripts.py
└── skills/tracking-visualization/
    ├── SKILL.md
    ├── references/   # Bilingual method and CONFIG guides
    ├── assets/       # Two templates, placeholder and texture
    └── scripts/      # JSON/path helpers, validator and embedder
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests cover both templates, missing images, invalid coordinates, inconsistent mapping, priority labels, unknown-data states, embedding integrity and refusal to overwrite or read outside the report directory. Browser smoke checks cover pin/row toggling, filtering, language labels, hidden-pin selection and popup placement. No live analytics integration, cross-client trigger benchmark or production security audit is claimed.

## Contributing

Keep bilingual documentation aligned. Preserve color meanings, default-hidden priorities, evidence distinctions, full inventories and pin/row linkage. Include a small fictional reproduction for bug reports, never real private data. Changes to the renderer need tests for both templates.

## License

[MIT License](LICENSE). Copyright notice uses `Tracking Visualization contributors`.
