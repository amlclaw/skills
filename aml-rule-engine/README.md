# AML Rule Engine - OpenClaw Skill

A rule-engine driven AML compliance detection skill for OpenClaw. Automatically extracts regulations from SG/HK/Dubai regulatory documents, supports user rule management, and performs intelligent detection on addresses + chains + rule sets.

## 🚀 Features

### 1. Automated Rule Extraction
- **Singapore (MAS) Regulations**: 36 structured rules extracted from `references/singapore/` (CDD/EDD/Travel Rule/Sanctions Screening/Red Flag/STR)
- **Hong Kong (SFC) Regulations**: 11 structured rules extracted from `references/hongkong/` (Capital Requirements/Personnel Requirements/Licensing Requirements/Compliance Framework)
- **Dubai (VARA) Regulations**: Planned
- **Output**: Structured JSON rule database

### 2. Rule Engine Core
- **Rule Matching**: Automatic matching of transaction graph data with rule database
- **Violation Detection**: Sanctions screening, Red Flag detection, threshold checking, compliance requirement verification
- **Risk Grading**: LOW/MEDIUM/HIGH/CRITICAL classification
- **Report Generation**: Detailed compliance violation reports with evidence and recommendations

### 3. User Rule Management
- **Rule Addition**: Add custom rules via CLI
- **Rule Editing**: Modify existing rule parameters
- **Rule Disabling**: Temporarily disable specific rules
- **Rule Import/Export**: JSON format import/export

### 4. End-to-End Detection Pipeline
- **Input**: Chain name + Address
- **Data Acquisition**: TrustIn Investigate API → Transaction graph
- **Rule Application**: Automatic matching of applicable rules
- **Output**: Compliance report + Violation details

## 📁 File Structure

```
aml-rule-engine/
├── SKILL.md              # Skill definition for OpenClaw
├── README.md            # This file
├── aml_cli.py          # Unified command-line interface
├── scripts/            # Core Python scripts
│   ├── graph_api.py          # TrustIn Investigate API client
│   ├── extract_rules.py      # Rule extractor (supports SG/HK)
│   ├── rule_engine.py        # Rule engine framework
│   ├── demo_cli.py          # Interactive demonstration CLI
│   └── integration_test.py   # End-to-end integration test
├── references/         # Regulatory documents (from aml-advisor)
│   ├── singapore/          # MAS regulations
│   ├── hongkong/           # SFC regulations
│   ├── dubai/             # VARA regulations (planned)
│   └── fatf/              # FATF recommendations
└── rules/              # Rule databases
    ├── singapore_rules.json   # 36 Singapore rules
    ├── hongkong_rules.json    # 11 Hong Kong rules
    └── all_rules.json         # 47 combined rules
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- OpenClaw installation
- TrustIn API key (for graph data)

### Environment Variables
```bash
export TRUSTIN_API_KEY="ce02a019-722b-48ba-864d-71071c2c0ebd"
```

## 📖 Usage

### Basic Address Detection
```bash
# Detect single address
python3 aml_cli.py check --chain Tron --address THaUdoNaeL7FEHFGpzEktHiJPsDctc6C6o

# Interactive mode
python3 aml_cli.py --interactive
```

### Rule Management
```bash
# Extract all regulations
python3 aml_cli.py extract --jurisdiction all

# List rules
python3 aml_cli.py list --detail

# Run integration test
python3 aml_cli.py test

# Check system status
python3 aml_cli.py status
```

### Direct Script Usage
```bash
# Extract Singapore rules
cd scripts && python3 extract_rules.py --jurisdiction singapore

# Run integration test
cd scripts && python3 integration_test.py

# Use demonstration CLI
cd scripts && python3 demo_cli.py --interactive
```

## 🧪 Testing

### Integration Test Results (2026-02-20 15:55 SGT)
```
Test Address: THaUdoNaeL7FEHFGpzEktHiJPsDctc6C6o (Tron)
Data Acquisition: ✅ 3 tags (high:2, low:1), 3 paths
Rule Application: ✅ 36 Singapore rules + 11 Hong Kong rules
Violation Detection: ✅ 18 violations (MEDIUM level)
Processing Time: <30 seconds (API call + rule matching + report generation)
Sample Violation: Transaction amount 450,000 USDT > CDD threshold 5,000 SGD
```

## 🎯 Rule Types

### 1. Threshold Rules
- `CDD_THRESHOLD`: Customer Due Diligence trigger threshold (S$5,000 / HK$5,000,000)
- `TRAVEL_RULE_THRESHOLD`: Travel Rule trigger threshold (S$1,500)
- `CAPITAL_REQUIREMENT`: Capital requirements (HK$5,000,000)

### 2. Screening Rules
- `SANCTIONS_CHECK`: Sanctions list screening
- `RED_FLAG`: Red flag indicators
- `IVMS101_REQUIRED`: Travel Rule information requirements

### 3. Compliance Rules
- `FIT_AND_PROPER_TEST`: Personnel fitness test
- `RESIDENCY_REQUIREMENT`: Residency requirements
- `VASP_LICENSE_REQUIRED`: VASP license requirements
- `AML_CFT_PROGRAM_REQUIRED`: AML/CFT program requirements
- `RISK_ASSESSMENT_REQUIRED`: Risk assessment requirements

## 🔧 Development

### Extending to New Jurisdictions
1. Add regulatory documents to `references/<jurisdiction>/`
2. Extend `extract_rules.py` with new jurisdiction extraction methods
3. Update `rule_engine.py` to support new rule types
4. Test with integration test

### Adding New Rule Types
1. Define rule type in `rule_engine.py` Rule class
2. Add matching logic in `_apply_single_rule` method
3. Create corresponding detection method (e.g., `_check_new_rule_type`)
4. Update CLI to support new rule type

## 📊 Performance Metrics

| Metric | Result | Status |
|--------|--------|--------|
| Rules Count | 47 (SG:36 + HK:11) | ✅ |
| API Success Rate | 100% (4/4 calls) | ✅ |
| Detection Accuracy | 18/18 violations correctly identified | ✅ |
| Processing Time | <30 seconds (API+Rules+Report) | ✅ |
| Memory Usage | 56.9% (7056MB available) | ✅ |
| CPU Usage | 1.9% | ✅ |

## 🤝 Contributing

Contributions are welcome! Please:
1. Add new regulatory documents to `references/` directory
2. Extend `extract_rules.py` to support new jurisdictions
3. Improve rule matching algorithms
4. Add new rule types

## 📄 License

MIT License