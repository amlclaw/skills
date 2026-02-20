# amlclaw Skills

OpenClaw skills for AML compliance - Address screening, transaction monitoring, and reporting.

## 🎯 Available Skills

### 1. AML Address Screening
- **Description**: Screen blockchain addresses for AML risks
- **Usage**: `aml-screen-address <chain> <address>`
- **Features**: Real-time KYA (Know Your Address) integration

### 2. AML Transaction Monitoring
- **Description**: Monitor transactions for suspicious activity
- **Usage**: `aml-monitor-transactions <chain> [--threshold]`
- **Features**: KYT (Know Your Transaction) with customizable rules

### 3. AML Compliance Reporting
- **Description**: Generate regulatory compliance reports
- **Usage**: `aml-generate-report <regulator> [--period]`
- **Features**: MAS, SFC, VARA templates

## 🚀 Installation

```bash
# Install a skill
openclaw skills install aml-address-screening

# Or install from this repository
openclaw skills install https://github.com/amlclaw/skills/aml-address-screening
```

## 🔧 Development

### Skill Structure
```
aml-address-screening/
├── SKILL.md              # Skill documentation
├── __init__.py           # Skill entry point
├── screening.py          # Main logic
├── requirements.txt      # Dependencies
└── tests/               # Skill tests
```

### Creating a New Skill
1. Create a new directory in `skills/`
2. Add `SKILL.md` with documentation
3. Implement skill logic in Python
4. Add tests
5. Submit a Pull Request

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing skills.

## 📞 Support

For skill-related questions:
- Open an issue in this repository
- Join our Discord community
- Email skills@amlclaw.com
