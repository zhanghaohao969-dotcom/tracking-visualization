# Full Workflow / 完整工作流

## English

### 1. Scope and source branch

Confirm the page, journey, repository, feature version/branch, images and permitted data sources. Inspect the target branch without switching or overwriting the user's working tree unnecessarily. Do not guess that the newest branch is the right one. If ambiguous, ask.

Inventory business component calls and shared/global instrumentation. Record event/action, dimensions, parameter types and requiredness, trigger timing, file/line or permalink evidence, deployment/environment qualifiers and whether the registry agrees. Do not publish proprietary source evidence to a public report without permission.

### 2. Verify reporting

Use existing dashboards and datasets first, raw events last. Record event count and deduplicated users over one agreed period and population. A verified zero becomes `empty` with count/users 0; a source not checked, unavailable or insufficient becomes `unverified` with absent counts. A implemented event with verified nonzero observations may use `ok`. Do not infer the reason for zero from zero alone.

### 3. Analyze gaps

Compare coverage with entry attribution, intermediate states, submission/results, error recovery and external-system return. Existing global events may already answer the question. A missing custom action is not automatically a tracking gap.

Write a proposed event/action, trigger, parameter contract, purpose/hypothesis, potential decision and priority rationale. P0/P1/P2 remain in the configuration for analysis; `showPriority` is false unless explicitly requested. Keep raw personal input, secrets and unnecessary identifiers out of proposed tracking.

### 4. Build from templates

Copy the single or multi template with its texture, add permitted PNG/JPEG/GIF/WebP screenshots and fill JSON CONFIG. Single-screen image lives in `img#screenshot`; multi-screen images are `pages[].img`. JSON has no comments, functions or trailing commas. Preserve renderer logic and its glass visual, color contract and spacing.

Use semantic names and per-screen percentage coordinates. Map every pin by `pinLoc` to exactly one inventory row; a row can refer to several pins. Include inventory-only events. Keep unknown data unknown. For gap prose, separate observation purpose (`desc`) from decision supported (`data`).

### 5. Validate, inspect and deliver

Run `validate_annotation.py`, then open the generated file in a browser. Check both templates when modifying the shared renderer: pin/row toggle; filter behavior in all three regions; hidden-pin single selection; popups at bottom/right edges; language selector; error/zero/unverified badges; priority hidden by default; all images readable.

Run `embed_images.py input.html output-standalone.html`. Revalidate the standalone output. Local screenshots are encoded without conversion, preserving clarity, transparency and animated GIF bytes. The tool refuses remote URLs, unsupported image types, path traversal, missing images and overwriting. Keep images within the report's directory; copy only user-approved files there.

Share the standalone artifact through the host's file delivery mechanism. Public publishing is separate from a local report and needs explicit authorization. No hosting API is bundled. Supply the screenshot source, evidence source, reporting period, unknowns and limitations; do not reveal priorities in summaries unless requested.

### Public adaptation notes

This public version replaces executable JavaScript CONFIG with non-executing JSON, renders configuration text as text rather than HTML, adds explicit unknown-data handling and strictly checks pin/row mapping. It does not support legacy orange/purple category colors, remote/SVG screenshots or platform-specific deployment commands. The visual texture and glass layout are retained.

## 简体中文

### 1. 定范围与分支

确认页面/关键路径、仓库、功能版本/分支、底图和授权渠道。尽量只读目标分支，不随意切换或覆盖用户工作树；不把最近更新的分支猜成目标。业务代码和公共 SDK、路由、全局埋点都要覆盖，记录事件、维度、参数类型/必填性、时机、源码证据、部署/环境条件与注册表一致性。专有源码证据未经允许不公开。

### 2. 核实上报

优先看板/数据集，原始事件兜底。统一周期人群下记录次数和去重人数；已核实零值是 `empty`（0/0），未查/无权限/信息不足是 `unverified`（不填数）；已有实现且核实非零可用 `ok`。零值本身不能解释成没人用。

### 3. 找缺口

看入口、过程、提交/结果、错误恢复和外部返回；先核对全局事件是否已覆盖，不把缺自定义事件直接等同缺口。新增建议写清 action、时机、参数契约、用途/假设、可能支持的决策和分级依据。默认不展示优先级，不采集原始个人输入、秘密或不必要标识。

### 4. 填模板

复制单/多屏模板、纹理和授权截图，填 JSON；单屏 src 在 `img#screenshot`，多屏在 `pages[].img`。JSON 不支持注释、函数或尾逗号；报告生成只改配置，不改渲染。语义命名、屏内百分比定位，通过 `pinLoc` 精确关联，一行可挂多个 pin；未配图事件仍进全量清单。缺口 desc 写观察目的，data 写支撑决策，未知数不补零。

### 5. 校验与交付

先跑校验，再浏览器检查联动/重复点击关闭、三处筛选、隐藏态单点、边缘气泡、语言切换、错误/零值/待核实标签、优先级默认隐藏、图片可见。用内嵌工具生成单文件再校验，图片不转码，保留清晰度/透明/GIF 原字节；拒绝远程/SVG/越界/丢图/覆盖。通过宿主文件机制交付，公开发布另需授权；没有内置托管接口。注明底图、证据、周期、未知项和限制，未要求时摘要也不展示优先级。

公开版保留原玻璃纹理布局，改用非执行 JSON、文本安全渲染、明确未知状态与严格映射，不支持旧橙/紫分类、SVG/远程底图或专用平台发布指令。
