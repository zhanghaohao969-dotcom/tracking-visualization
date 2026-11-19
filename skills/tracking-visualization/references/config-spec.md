# CONFIG Specification / 配置规范

## English

Edit JSON in `<script type="application/json" id="annotation-config">`. The renderer parses this as CONFIG; never use executable code. Escape `<` as `\u003c` if it occurs inside strings. All textual fields are plain text: use `\n` for line breaks, not HTML markup.

### Top level

- `title`, `meta`: required non-empty text; state page and evidence/period definitions.
- `lang`: `en` (default) or `zh-CN`; controls interface labels. The selector changes labels, not configured prose.
- `showPriority`: boolean, default false; true only on explicit user request.
- `note`: optional text with image source, caveats, unknowns and fictional-example disclosure.
- `legend`: unique `{color,label}` items, using blue/green/red.
- Exactly one of `pins` (single-screen) or `pages` (multi-screen).
- `table`: complete inventory, including events with no pins.

### Pin

`id`: positive integer unique within a screen; `pos`: `{x,y}` percentages between 0 and 100; `color`: blue exposure, green interaction, red missing.

Required text: `action`, `title`, `desc`, `params`, `data`. `suggest:true` is required for red. Optional `tier:p0|p1|p2` must agree with the mapped row. Optional booleans `empty` and `unverified` must agree with the row's status. Optional `mark:"error"` adds an orange error marker, not a missing event.

For gaps, `desc` states purpose and hypothesis, while `data` states the decision supported. Use the same gap description in pin and row. Do not insert priorities into action names.

### Page

`name`: required title; `badge:{text,bg}`: label and six-digit hex color; `img`: safe relative raster path or embedded PNG/JPEG/GIF/WebP data URI; `pins`: non-empty array.

Single-screen images are specified in the HTML's hidden `img#screenshot` source, outside CONFIG. Every copied report needs its texture and local images until embedded.

### Inventory row

Required: globally unique positive `id`, `action`, `loc`, `params`, explicit `color`, `status`.

`status`: `ok`, `empty`, `unverified`, `p0`, `p1`, `p2`. For gaps, `color:red` and non-empty `timing`, `desc`, `suggestion` are required; count/users must be absent. `empty` requires count/users exactly zero. `unverified` requires absent counts. Observed values must be non-negative integers.

`pinLoc`: screen/pin references such as `S1-1 / S2-1`. Each reference belongs to exactly one row and must exist; every pin must be mapped. It is required for pinned events but absent for inventory-only events. Pin/table action and color must agree. Table IDs and screen-local pin IDs do not need to be equal.

`mark:"error"`: optional error-state annotation. The renderer derives status from the mapped row, not from arbitrary badge prose.

### Parameter contracts

`parameter: type(required|optional) = value1|value2`; types are string/number/boolean/array/object, with structure for arrays/objects. Preserve verified code keys and confirmed enums. Proposed fields are proposals, not existing implementation claims. Avoid free-text user content and personal identifiers unless strictly necessary and permitted.

### Example (fictional)

```json
{
  "id": 2,
  "pos": {"x": 30, "y": 50},
  "color": "red",
  "suggest": true,
  "tier": "p0",
  "action": "demo_submit_result",
  "title": "Submission result",
  "desc": "Observe failures between submission and completion.",
  "params": "result: string(required) = success|failure",
  "data": "Decision supported: choose whether recovery or flow simplification needs investigation."
}
```

Templates retain glass surfaces, #4250a0 exposure, #21918c interaction, #cd5973 missing, independent per-screen popups, 28px group spacing, pin/row toggle, hidden-pin single focus and full inventory filtering. Do not repurpose red as an error color. Text is safely displayed rather than interpreted as HTML; the validator is not a full hostile-HTML sanitizer.

## 简体中文

编辑 `script#annotation-config` 的 JSON，运行时解析为 CONFIG，不放可执行 JS；字符串的 `<` 可写 `\u003c`，文本换行用 `\n`，不写 HTML。

顶层必填 title/meta/legend/table，单屏 pins 与多屏 pages 二选一。lang 为 en/zh-CN，切换仅改变界面标签；描述仍保持填写语言。showPriority 默认 false，仅明确要求展示分级时 true。note 写底图、口径、未知项或虚构声明。

pin 的 id 屏内唯一正整数；pos x/y 为 0–100；blue 曝光、green 交互、red 缺口。必填 action/title/desc/params/data；red 需 suggest:true。tier 与清单分级一致，empty/unverified 布尔与清单状态一致，mark:error 是橙色错误态。缺口 desc 与 data 不重复，pin.desc 与 row.desc 相同，action 不含分级标记。

多屏 page 需 name、badge（text 和六位十六进制 bg）、img 和 pins；支持相对栅格图或内嵌 PNG/JPEG/GIF/WebP，不支持远程/SVG。单屏图在 HTML 的 `img#screenshot` src；内嵌前需连纹理和本地图一起保存。

清单 id 全局唯一，action/loc/params/color/status 必填。ok 已核实上报；empty 必须核实 0 次/0 人；unverified 不填数；p0/p1/p2 必须 red，补 timing/desc/suggestion 且不填数。pinLoc 为 `S1-1 / S2-1`，每个标注点恰好映射一行，列表引用必须存在；无图事件不填 pinLoc。pin/table action 与颜色一致，清单 ID 不必等于屏内 pin ID。

参数写 `参数名: 类型(required|optional) = 枚举`，保留真实键和已确认枚举，建议字段明确只是建议，不默认采集用户原始内容/个人标识。

保留玻璃视觉、三色语义、每屏独立气泡、28px 分组间距、重复行点击关闭、隐藏态单点显示、三处筛选。红色不当错误色；文本安全显示不等于完整 HTML 安全审计。
