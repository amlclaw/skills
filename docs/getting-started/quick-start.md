# Quick Start Guide

Get started with AML address screening in minutes!

## Your First Address Screening

### Basic Python Usage

```python
from aml_address_screening import screen_address, format_result

# Screen a Tron address
result = screen_address(
    chain="Tron",
    address="THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt"
)

# Print formatted result
print(format_result(result))
```

### Command Line Usage

```bash
# Basic screening
python3 -m aml_address_screening Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt

# With verbose output
python3 -m aml_address_screening Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt --verbose
```

## Understanding the Results

### Risk Scores

The skill returns a risk score from 0-100:

| Score | Risk Level | Recommendation |
|-------|------------|----------------|
| 0-25 | LOW | Normal processing |
| 26-50 | MEDIUM_LOW | Enhanced monitoring |
| 51-75 | MEDIUM | Manual review required |
| 76-90 | HIGH | Restricted processing |
| 91-100 | CRITICAL | Reject and report |

### Sample Output

```
============================================================
AML ADDRESS SCREENING RESULT
============================================================
Chain: Tron
Address: THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt
Address Valid: ✅ Yes
Validation: Valid Tron address
------------------------------------------------------------
Risk Score: 15/100
Risk Level: LOW
Recommendation: 🟢 Normal processing - No restrictions needed
------------------------------------------------------------
Data Source: TrustIn KYA API
Screening Time: 0:00:01.234567
API Used: ✅ Yes
============================================================
```

## Common Use Cases

### 1. Batch Screening

```python
addresses = [
    ("Tron", "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt"),
    ("Ethereum", "0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b"),
]

for chain, address in addresses:
    result = screen_address(chain, address)
    print(f"{chain}: {result['risk_score']}/100 - {result['risk_level']}")
```

### 2. Decision Making

```python
result = screen_address("Tron", "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt")

if result["risk_score"] < 25:
    decision = "APPROVE"
elif result["risk_score"] < 75:
    decision = "REVIEW"
else:
    decision = "REJECT"

print(f"Decision: {decision}")
```

### 3. Export Results

```python
import json

result = screen_address("Ethereum", "0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b")

# Save to JSON
with open("screening_result.json", "w") as f:
    json.dump(result, f, indent=2, default=str)
```

## Next Steps

- [Configuration Guide](configuration.md) - Customize risk thresholds and settings
- [User Guide](../guide/address-screening.md) - Learn about all features
- [Examples](../examples/index.md) - More code examples and use cases

## Need Help?

- Check the [Troubleshooting Guide](../development/troubleshooting.md)
- Report issues on [GitHub](https://github.com/amlclaw/skills/issues)
- Join our [Discord community](https://discord.gg/clawd)