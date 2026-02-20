---
name: aml-address-screening
description: AML地址筛查技能。使用TrustIn KYA Lite API筛查区块链地址的洗钱风险。支持Tron、Ethereum等主流区块链网络。
---

# AML Address Screening — 区块链地址洗钱风险筛查

## 核心理念

> 地址是链上活动的起点。筛查地址风险是AML合规的第一道防线。
> 基于TrustIn KYA (Know Your Address) API，提供实时的地址风险评估。

## 快速使用

```bash
# 安装依赖
pip install requests

# 使用技能
python3 skills/aml-address-screening/scripts/screen_address.py <链名> <地址>

# 示例
python3 skills/aml-address-screening/scripts/screen_address.py Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt
python3 skills/aml-address-screening/scripts/screen_address.py Ethereum 0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b
```

**依赖安装**:
```bash
pip install requests python-dotenv
```

## 四步风险评估框架

### 第一步: 基础信息检查
- 地址格式有效性验证
- 链类型识别 (Tron, Ethereum, 等)
- 地址类型检查 (外部地址、合约地址)

### 第二步: 交易行为分析
- 历史交易数量统计
- 交易频率分析
- 大额交易识别
- 资金流向模式

### 第三步: 关联风险评分
- 关联地址风险传导
- 黑名单地址匹配
- 高风险模式识别
- 监管关注地址检测

### 第四步: 综合风险评级
- 低风险 (Low Risk): 正常交易行为
- 中风险 (Medium Risk): 需要进一步监控
- 高风险 (High Risk): 建议限制或拒绝
- 极高风险 (Critical Risk): 立即采取行动

## 风险评估标准

| 风险等级 | 分数范围 | 建议行动 |
|----------|----------|----------|
| ⭐⭐⭐⭐⭐ 低风险 | 0-25 | 🟢 正常处理 |
| ⭐⭐⭐⭐ 中低风险 | 26-50 | 🟡 加强监控 |
| ⭐⭐⭐ 中等风险 | 51-75 | 🟡 人工审核 |
| ⭐⭐ 高风险 | 76-90 | 🔴 限制交易 |
| ⭐ 极高风险 | 91-100 | 🔴 拒绝并报告 |

## 支持的网络

### 已支持
- **Tron**: TRC-20 USDT, TRX
- **Ethereum**: ERC-20, ETH

### 计划支持
- **Bitcoin**: BTC
- **Solana**: SOL, SPL代币
- **BNB Chain**: BEP-20

## 配置要求

### API密钥配置
1. 获取TrustIn API密钥: https://www.trustin.info
2. 创建`.env`文件:
   ```bash
   TRUSTIN_API_KEY=your_api_key_here
   ```

### 环境变量
```bash
# 可选: 自定义风险阈值
RISK_THRESHOLD_LOW=25
RISK_THRESHOLD_MEDIUM=50
RISK_THRESHOLD_HIGH=75
```

## 使用后的决策流程

运行筛查后，基于输出做决策:

1. **低风险地址** → 正常处理，记录筛查结果
2. **中等风险地址** → 加强监控，定期复查
3. **高风险地址** → 人工审核，收集额外信息
4. **极高风险地址** → 拒绝交易，提交可疑交易报告

## 集成到OpenClaw工作流

### 作为OpenClaw技能使用
```bash
# 安装技能
openclaw skills install aml-address-screening

# 使用技能
aml-screen-address Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt
```

### 自动化筛查工作流
1. 交易前自动筛查发送方/接收方地址
2. 定期筛查客户地址列表
3. 实时监控高风险地址活动
4. 生成合规报告和审计追踪

## 性能考虑

- **API调用频率**: 遵守TrustIn API速率限制
- **缓存策略**: 对已筛查地址实施缓存
- **批量处理**: 支持批量地址筛查
- **异步处理**: 支持异步API调用

## 参考资料

- `docs/api-integration.md` — TrustIn API集成指南
- `docs/risk-scoring.md` — 风险评分算法详解
- `examples/` — 使用示例和集成代码

## 数据源

- **TrustIn KYA Lite API**: 快速地址风险评估
- **TrustIn KYA Pro API**: 深度地址分析 (需要额外权限)
- **公开链上数据**: 区块链浏览器数据补充

## 合规性

- **数据隐私**: 不存储敏感地址信息
- **审计追踪**: 完整的筛查记录
- **监管要求**: 符合MAS、SFC、VARA等监管框架

---

**最后更新**: 2026-02-20  
**版本**: 0.1.0-beta  
**状态**: 开发中