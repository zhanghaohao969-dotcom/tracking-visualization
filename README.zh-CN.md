# Tracking Visualization · 埋点可视化

[English](README.md) | 简体中文

**把已有埋点与缺口直接贴到产品页面上，让埋点现状一眼可见。**

这是一个 Agent Skill：把已核实的埋点实现、实际上报和缺口建议，变成可点击的 HTML 标注页。图上彩色 pin、详情气泡、本屏清单和全量清单一起帮助评审与研发理解覆盖情况。

## 包含什么

- 单屏/多屏模板，保留浅色噪点玻璃布局。
- 蓝色页面曝光、绿色用户交互、红色缺失埋点；错误态用橙色角标。
- pin/表行高亮联动、重复点击关闭、分类筛选、每屏显示开关。
- 中英文界面标签；事件描述使用你填写的语言，不自动翻译。
- 每屏独立气泡，隐藏态只显示当前选择的一个 pin。
- 缺口 P0/P1/P2 保留分析分类，**默认不显示优先级**，明确要求才展示。
- `unverified` 未核实、`empty` 已核实零值和缺口严格区分。
- Python 校验和图片内嵌单文件工具。

## 安装

按客户端规范导入完整 `skills/tracking-visualization/` 文件夹，不能只装 SKILL.md，模板、参考和脚本都要保留。不承诺所有客户端已验证自动触发兼容。

默认执行指令为英文，提供[中文阅读版](docs/tracking-visualization.zh-CN.md)，三份 reference 都包含中英文。只安装一个 Skill，不把中文文档装成第二个 Skill。

## 试一试

```text
用 tracking-visualization 盘点这个结算页：先确认正确功能分支，同时查业务和全局埋点，用我提供的授权汇总数据核实上报，把缺口标到截图上，默认不展示优先级。
```

提供页面截图/设计状态帧、仓库和分支或源码片段、关键用户路径、允许使用的数据渠道/导出、周期和口径。只有截图/清单时应明确标为「基于提供材料」，不能假装查过源码/实时数据，证据不足保留待核实。

## 五步流程

1. 确认分支，查注册定义、业务调用和共享/全局事件。
2. 优先现成看板，其次加工数据集，原始事件兜底，只用授权来源。
3. 围绕关键路径找缺口，不把零上报/无权限当成没有实现。
4. 填单/多屏模板的 JSON CONFIG，每份报告不改渲染器。
5. 校验 → 浏览器抽查 → 图片内嵌 → 再校验 → 分享单文件 HTML。

本包**没有分析平台连接器或托管 API**；代码检索、浏览器和授权查数能力来自宿主客户端，不授予权限、不自动连业务系统。

## 打开演示

本地浏览器打开 `skills/tracking-visualization/assets/template-single.html` 或 `template-multi.html`，让图片和纹理保持同目录。语言选择器切换中英文标签，配置描述不自动翻译。

示例事件、数字、位置均为**虚构**，`placeholder.png` 不是产品截图；实际审计要换图换数据。

## 依赖与命令

Python 3.10+（无第三方 Python 包），Node.js 18+（JS 语法检查），现代浏览器（交互）。在 Skill 目录运行：

```bash
python3 scripts/validate_annotation.py assets/template-single.html
python3 scripts/embed_images.py assets/template-single.html report-standalone.html
python3 scripts/validate_annotation.py report-standalone.html
```

内嵌保留 PNG/JPEG/GIF/WebP 原始字节，不压缩/转码导致模糊或 GIF 丢动画；使用新的输出名，不覆盖已有文件。底图必须在报告目录内，公开版不支持远程地址/SVG 底图。

## 配置与迁移

见[配置规范](skills/tracking-visualization/references/config-spec.md)、[工作流](skills/tracking-visualization/references/workflow.md)、[证据渠道](skills/tracking-visualization/references/data-channels.md)。

公开版将原可执行 `const CONFIG = {...}` 改成 `script#annotation-config` 的 JSON，由运行时解析；字符串为纯文本，不写 HTML，JSON 不支持注释、函数、尾逗号。安全调整意味着旧产物不能直接按原格式迁移。

还移除了企业专用资源、内部链接/ID/部署指令，强化映射/颜色/缺口/零值/未知值一致性校验，不支持旧橙/紫分类（错误用 mark:error）。保留原玻璃视觉，动态文本通过安全 DOM 显示。

## 隐私与限制

只使用有权分享的截图、源码引用和汇总数据，遮盖凭证、个人记录和专有内容。参数建议优先必要的有界分类，不默认采集原始用户输入。

校验器读 JSON、查 JS 语法，**不执行页面代码、不联网查数**；它不是完整恶意 HTML 清洗器，未知 HTML 打开前仍应检查。图片工具拒绝目录越界、不抓远程文件。

零值不能证明没人用，还可能是灰度、过滤、延迟或埋点失败；注册、实现、部署、观察要分开。发布这个 Skill 不授权公开未来客户截图、业务数据或生成报告。

## 目录与测试

仓库包含双语 README、MIT、中文阅读 docs、tests，完整 Skill 下含 SKILL.md、三份双语 references、两个模板/占位图/纹理、JSON/路径 helper、校验器、内嵌工具。

```bash
python3 -m unittest discover -s tests -v
```

测试覆盖两模板、丢图、越界、映射不一致、action 优先级标记、未知数据、内嵌字节和拒绝覆盖/目录越界；浏览器抽查联动、筛选、语言标签、隐藏态单点、气泡位置。不宣称完成实时数据集成、跨客户端触发基准或生产安全审计。

## 参与改进与许可

保持中英文一致，保留三色语义、默认隐藏优先级、证据状态区分、全量清单和联动；Bug 示例用虚构数据，不带真实私密资料，渲染器修改需测两模板。

采用 [MIT License](LICENSE)，署名 `Tracking Visualization contributors`。
