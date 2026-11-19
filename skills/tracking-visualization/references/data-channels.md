# Evidence Channels / 证据渠道

## English

This is a project-neutral guide. It contains no organization-specific dashboard IDs, project numbers, source branches, private URLs or connectors. Fill in the current project's permitted sources rather than reuse examples from another product.

### Looking for instrumentation

1. The project's event registry or instrumentation specification: declared event names, parameters, ownership and intended triggers.
2. The verified source branch: actual page/component calls plus shared SDK, router and delegated global interaction/exposure handlers. Check event dimensions and environment/version gates.
3. Observed reporting through an authorized analytics source: verify that a deployed version actually emits the intended event.
4. Product requirement and measurement-definition documents: explain why it was added and how it should be interpreted.

Registration is not proof of implementation; implementation is not proof of deployed reporting. Preserve these distinctions in the report.

### Looking for metric values

1. Existing dashboard with known definitions and refresh time.
2. Curated dataset with the required dimensions and agreed measurement definitions.
3. Raw events if the prior sources do not cover the question.
4. Data pipeline health, delivery delays or service logs only when necessary to explain abnormal reporting, within authorization.
5. Source code to clarify trigger behavior, filters or missing coverage.

Confirm period, time zone, population, environment, version, aggregation, deduplication and denominator. Do not recompute a published metric with a different definition and treat the result as equivalent.

### Access unavailable

Use a user-provided, de-identified export or leave the event `unverified`. Do not request credentials, infer zero values, or bypass permission limits. An event might have zero observations because of environment filters, rollout, low traffic, delivery delays or trigger failure; investigation is needed before concluding inactivity.

## 简体中文

这是项目无关的查询指南，不包含企业看板 ID、项目号、分支、内部链接或连接器。使用当前项目允许访问的渠道，不照搬其他产品资源。

### 想检索埋点

1. 团队事件注册表/埋点设计：事件名、参数、负责人、预期触发。
2. 已确认的源码分支：业务页面/组件调用，加上共享 SDK、路由、全局点击/曝光。检查维度、环境开关与版本。
3. 授权分析渠道的实际数据：确认部署版本确实上报。
4. 产品需求与口径文档：补充用途及解释规则。

注册不等于实现，实现不等于线上上报。报告要把这几类证据分开。

### 想核数

依次找现成看板 → 加工数据集 → 原始事件；异常时按授权补充任务延迟、数据链路和服务日志；最后用代码澄清触发、过滤与覆盖。

对齐周期、时区、人群、环境、版本、汇总、去重和分母。不要用不同口径重算再当作现成指标的等价结果。

### 无权限/查不到

接收用户允许分享的脱敏汇总导出，或保留 `unverified`。不索要凭证、不把未查到改成零、不绕过权限。零值可能来自过滤、灰度、低流量、延迟或触发失败，需要进一步调查后才讨论原因。
