# AML Address Screening Skill

**OpenClaw skill for blockchain address AML risk assessment using TrustIn KYA API**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TrustIn API](https://img.shields.io/badge/TrustIn-API-green.svg)](https://trustin.info)

## 🎯 Features

- **🔍 Real-time Address Screening**: Instant AML risk assessment for blockchain addresses
- **🌐 Multi-chain Support**: Tron, Ethereum, Bitcoin, Solana (extensible)
- **🤖 Smart Risk Scoring**: 0-100 risk score with 5-level classification
- **🔄 TrustIn API Integration**: Seamless integration with KYA Lite and KYA Pro APIs
- **⚡ Offline Capability**: Basic pattern analysis when API unavailable
- **📊 Detailed Reporting**: Comprehensive risk assessment with recommendations
- **🧪 Complete Test Suite**: Unit tests for all major functionality

## 🚀 Quick Start

### Installation

```bash
# Clone the skill
git clone https://github.com/amlclaw/skills/aml-address-screening.git
cd aml-address-screening

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your TrustIn API key
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

### Command Line Usage

```bash
# Basic screening
python3 -m aml_address_screening Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt

# With API key
TRUSTIN_API_KEY=your_key python3 -m aml_address_screening Ethereum 0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b

# Verbose output
python3 -m aml_address_screening Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt --verbose
```

## 📊 Risk Assessment

### Risk Levels

| Score | Level | Color | Action |
|-------|-------|-------|--------|
| 0-25 | LOW | 🟢 | Normal processing |
| 26-50 | MEDIUM_LOW | 🟡 | Enhanced monitoring |
| 51-75 | MEDIUM | 🟡 | Manual review required |
| 76-90 | HIGH | 🔴 | Restricted processing |
| 91-100 | CRITICAL | 🔴 | Reject and report |

### Assessment Factors

1. **Address Format Validation**: Valid blockchain address structure
2. **Pattern Analysis**: Suspicious character patterns and anomalies
3. **TrustIn KYA Assessment**: Professional risk scoring from TrustIn API
4. **Historical Context**: Transaction history and association analysis

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required: TrustIn API key from https://www.trustin.info
TRUSTIN_API_KEY=your_api_key_here

# Optional: Risk thresholds
RISK_THRESHOLD_LOW=25
RISK_THRESHOLD_MEDIUM=50
RISK_THRESHOLD_HIGH=75

# Optional: Logging
LOG_LEVEL=INFO
```

### API Integration

The skill automatically:
- Falls back to basic analysis if TrustIn API is unavailable
- Handles rate limiting and authentication errors
- Provides detailed error messages for troubleshooting
- Caches results when appropriate

## 📁 Project Structure

```
aml-address-screening/
├── SKILL.md              # Skill documentation for OpenClaw
├── __init__.py           # Main entry point and CLI interface
├── screening.py          # Core screening logic and risk assessment
├── trustin_api.py        # TrustIn API client and integration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment configuration template
├── setup.py              # Package installation configuration
├── tests/               # Test suite
│   ├── test_screening.py
│   └── test_config.py
└── examples/            # Usage examples
    └── basic_usage.py
```

## 🧪 Testing

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test module
python3 -m pytest tests/test_screening.py

# Run with coverage
python3 -m pytest tests/ --cov=aml_address_screening
```

## 🔌 Integration

### As an OpenClaw Skill

```bash
# Install as OpenClaw skill
openclaw skills install aml-address-screening

# Use within OpenClaw
aml-screen-address Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt
```

### In Python Applications

```python
import aml_address_screening

# Batch screening
addresses = [
    ("Tron", "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt"),
    ("Ethereum", "0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b"),
]

for chain, address in addresses:
    result = aml_address_screening.screen_address(chain, address)
    # Process based on risk score
    if result["risk_score"] < 25:
        print(f"✅ {address[:12]}...: Approved")
    else:
        print(f"⚠️  {address[:12]}...: Requires review")
```

## 📈 Performance

- **Single screening**: < 2 seconds (with API), < 100ms (basic)
- **Concurrent requests**: Thread-safe API client
- **Error handling**: Graceful degradation on API failure
- **Memory usage**: Minimal footprint, suitable for batch processing

## 🔄 Development

### Prerequisites

```bash
# Clone and set up development environment
git clone https://github.com/amlclaw/skills/aml-address-screening.git
cd aml-address-screening
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions
- Add tests for new functionality

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📚 Documentation

- [API Reference](docs/api.md) - Detailed API documentation
- [Integration Guide](docs/integration.md) - How to integrate with other systems
- [Deployment Guide](docs/deployment.md) - Production deployment instructions
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [TrustIn](https://trustin.info) for providing the KYA API
- [OpenClaw](https://openclaw.ai) for the amazing AI assistant ecosystem
- All contributors and early adopters

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/amlclaw/skills/issues)
- **Documentation**: [Complete documentation](https://github.com/amlclaw/docs)
- **Community**: Join our [Discord server](https://discord.gg/clawd)

---

**Built with ❤️ by the amlclaw community**