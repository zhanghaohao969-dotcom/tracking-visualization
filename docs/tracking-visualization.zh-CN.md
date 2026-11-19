# Tracking Visualization · 埋点可视化

[English instructions](../skills/tracking-visualization/SKILL.md) | 简体中文

把「代码中有哪些埋点、实际是否上报、还缺什么」用可点击标注点和全量清单讲清楚，交付自包含 HTML。回复语言跟随用户；模板支持 `CONFIG.lang` 和界面语言切换，但事件描述仍使用配置中填写的语言。本文件是阅读版，安装时只导入 `skills/tracking-visualization/`。

## 五步工作流

1. **确认分支、盘点埋点**：检索前确认仓库、功能版本和目标分支，不默认在 main/master 搜新功能；确认目标已合入时才使用主分支。业务页面/组件调用与公共 SDK、路由、全局点击/曝光都要覆盖，检查 `area`、`target` 等维度。查团队事件注册表与实际调用。先读 Skill 内的 `references/data-channels.md` 和 `references/workflow.md`。
2. **核实实际上报**：优先现成看板，其次加工数据集，最后原始事件。记录周期、人群、环境、分母、去重与来源。只使用用户提供或授权的本项目渠道；本包没有平台连接器。零值必须来自核实，不能把缺权限或查不到当成零。
3. **分析缺口**：围绕入口、过程、提交、成功/失败、恢复和跨系统返回，找缺失埋点。P0/P1/P2 是分析分类，默认报告不展示，只有用户明确要求才显示。不能仅凭零值或权限不足判断没有实现。
4. **填模板**：读 `references/config-spec.md`；单屏用 `template-single.html`，多屏/多状态用 `template-multi.html`，一起带上纹理与允许分享的截图。只改 `script#annotation-config` 中的 JSON；单屏还需替换 `img#screenshot` 的 `src`。运行时解析 JSON 得到 CONFIG，不执行配置，不为每份报告修改渲染器。
5. **校验、走查、分享**：运行 `validate_annotation.py`，浏览器检查标注/表行联动、重复点击关闭、筛选、语言切换、边缘气泡和隐藏态单点显示。分享前运行 `embed_images.py`，再校验单文件输出。通过宿主 Agent 的文件/链接展示能力交付；公开发布报告需要另行明确授权。

## 输入与证据

只补齐缺失的产品/页面、仓库与分支、截图或设计状态帧、关键路径、授权数据渠道和周期。适当时可默认 14 天并注明，不虚构日期或数据。

仅有截图/事件清单时，可做「基于提供材料」的评审，但不能假装查过源码或实时数据。核实不了的项保留 `unverified` 并说明原因。

## 颜色与状态

- `blue`：已有页面/系统曝光；`green`：已有用户交互。
- `red`：缺失埋点建议，需 `suggest: true` 和一致的缺口清单行。
- `ok`：已核实有上报；`empty`：已核实零次数/零人数；`unverified`：未核实或无权限。
- `p0/p1/p2`：缺口，默认统一「缺失」，不展示优先级。
- `mark: "error"`：橙色错误态角标，不等于红色缺口。
- 仅用户明确要求时设 `showPriority: true`。action 名不添加优先级标记。
- P0：阻断关键漏斗解释；P1：支撑体验假设；P2：次要/长尾或跨系统回归。分类取决于本项目目标，不套统一严重度。

## 配图与上报契约

- pin 编号屏内唯一，清单编号全局唯一；`table[].pinLoc` 用 `S1-1 / S2-1` 关联，一张 pin 恰好对应一行。无底图事件可仅出现在清单。
- pin/row 的 action、颜色、缺口描述与状态标记一致；`pos.x/y` 为本屏底图的 0–100 百分比，不跨屏照搬。
- 每个 pin 包含 action/title/desc/params/data。缺口 desc 写「为什么埋、观察什么」，data 写「支撑什么决策」，不复制重复。
- 参数格式 `参数名: 类型(required|optional) = 枚举1|枚举2`，保留真实代码键；建议契约与未知枚举明确标注，不编造源码位置。
- meta、data、描述和建议全部为纯文本，使用换行而非 HTML。渲染器通过文本安全 DOM API 显示。

## 安全与分享

仅用有权分享的图；遮盖个人记录、凭证、账号细节和专有源代码信息。缺口建议不默认采集用户原始输入内容，优先必要的有界分类与汇总信号。

脚本不执行页面 JS、不联网查数。内嵌图片保留原始栅格字节，拒绝目录越界、不抓远程图、不覆盖已有输出。公开版不支持 SVG 底图、远程图片地址和旧版可执行 CONFIG；用户提供 HTML 打开前仍需检查，语义校验不是完整安全审计。

示例事件和数字为虚构，`placeholder.png` 不是真实产品。实际审计必须换图换数据，低次数本身不证明没人用或埋点缺失。

## 资源与命令

Skill 内的三份 reference 均有中英文说明；assets 包含单/多屏模板、占位图和纹理；scripts 包含 `annotation_common.py`、`validate_annotation.py` 和 `embed_images.py`。校验需要 Python 3.10+ 与 Node.js，内嵌工具只需要 Python 标准库。

```text
python3 scripts/validate_annotation.py report.html
python3 scripts/embed_images.py report.html report-standalone.html
python3 scripts/validate_annotation.py report-standalone.html
```

准备开源副本不改变本机原 Skill，安装时使用完整的 Skill 目录，中文阅读版不是第二个 Skill。
