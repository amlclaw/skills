# AML Address Screening Skill

Welcome to the documentation for the AML Address Screening skill - an OpenClaw skill for blockchain address AML risk assessment using TrustIn KYA API.

## 🎯 Overview

The AML Address Screening skill provides comprehensive Anti-Money Laundering (AML) risk assessment for blockchain addresses across multiple networks including Tron, Ethereum, Bitcoin, and Solana.

### Key Features

- **🔍 Multi-Chain Support**: Screen addresses on Tron, Ethereum, Bitcoin, and Solana
- **🤖 Smart Risk Scoring**: 0-100 risk score with 5-level classification
- **🔄 TrustIn API Integration**: Seamless integration with KYA Lite and KYA Pro APIs
- **⚡ Offline Capability**: Basic pattern analysis when API unavailable
- **📊 Detailed Reporting**: Comprehensive risk assessment with recommendations
- **🧪 Complete Test Suite**: Unit tests for all major functionality

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/amlclaw/skills.git
cd skills/aml-address-screening

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your TrustIn API key
```

### Basic Usage

```python
from aml_address_screening import screen_address, format_result

# Screen a blockchain address
result = screen_address(
    chain="Tron",
    address="THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt",
    verbose=True
)

print(format_result(result, verbose=True))
```

## 📚 Documentation Structure

- **[Getting Started](getting-started/installation.md)**: Installation and setup guides
- **[User Guide](guide/address-screening.md)**: How to use the skill effectively
- **[API Reference](api/screening.md)**: Detailed API documentation
- **[Development](development/contributing.md)**: Contributing and development guides
- **[Examples](examples/index.md)**: Code examples and use cases

## 🔗 Links

- [GitHub Repository](https://github.com/amlclaw/skills)
- [Report Issues](https://github.com/amlclaw/skills/issues)
- [Join Community](https://discord.gg/clawd)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/amlclaw/skills/blob/main/LICENSE) file for details.