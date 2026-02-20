---
name: aml-rule-engine
description: 规则引擎驱动的AML检测技能。自动从法规文件提取SG/HK/Dubai规则，支持用户规则管理，对地址+链+规则集进行智能检测。
---

# AML规则引擎技能

当用户需要检测地址的AML合规风险时，使用此技能。

## 使用场景

1. **单地址检测**: 用户提供链名和地址，分析该地址的交易图谱是否符合法规要求
2. **批量检测**: 用户提供地址列表，批量分析合规风险
3. **规则管理**: 用户需要添加、修改或删除自定义规则
4. **法规更新**: 当法规文件更新时，重新提取规则

## 技能命令

### 检测命令
- `aml check <chain> <address>` - 检测单个地址
- `aml check --file <address_list.txt>` - 批量检测地址列表
- `aml check --interactive` - 进入交互式检测模式

### 规则管理命令
- `aml rules extract --jurisdiction <all|singapore|hongkong|dubai>` - 提取法规规则
- `aml rules list` - 列出所有规则
- `aml rules add <rule_json>` - 添加自定义规则
- `aml rules disable <rule_id>` - 禁用规则
- `aml rules enable <rule_id>` - 启用规则

### 系统命令
- `aml test` - 运行集成测试
- `aml status` - 查看系统状态
- `aml update` - 更新法规库

## 实现说明

此技能基于`aml-advisor`仓库开发，包含以下核心组件：

### 1. 数据获取层 (graph_api.py)
- 集成TrustIn Investigate API
- 支持Tron和Ethereum链
- 异步任务提交和轮询

### 2. 规则提取层 (extract_rules.py)
- 从Markdown法规文件自动提取结构化规则
- 支持新加坡(MAS)和香港(SFC)法规
- 输出JSON格式规则数据库

### 3. 规则引擎层 (rule_engine.py)
- 规则加载和匹配引擎
- 多种规则类型支持 (阈值、筛查、合规)
- 违规检测和风险分级

### 4. 用户界面层 (demo_cli.py)
- 交互式命令行界面
- 报告生成和导出
- 规则管理功能

## 配置要求

### 环境变量
```bash
export TRUSTIN_API_KEY="ce02a019-722b-48ba-864d-71071c2c0ebd"
```

### 目录结构
```
~/.openclaw/workspace/aml-rule-engine/
├── scripts/           # 核心脚本
├── references/        # 法规文件
├── rules/            # 规则数据库
└── reports/          # 生成报告
```

## 错误处理

1. **API错误**: 当TrustIn API不可用时，返回错误信息并提供离线模式
2. **地址格式错误**: 验证地址格式，提供正确示例
3. **规则解析错误**: 当法规文件格式不标准时，记录警告并继续
4. **数据不足**: 当交易图谱数据不足时，说明限制并提供建议

## 性能优化

1. **缓存**: 对频繁检测的地址进行结果缓存
2. **批量处理**: 批量地址检测使用异步并行处理
3. **增量更新**: 规则数据库支持增量更新
4. **内存管理**: 大型图谱数据的流式处理

## 测试覆盖率

- ✅ 单元测试: 规则提取、规则匹配、API调用
- ✅ 集成测试: 端到端工作流 (地址→API→规则→报告)
- ✅ 性能测试: 并发检测、大数据集处理
- ✅ 兼容性测试: 不同链、不同法规管辖区