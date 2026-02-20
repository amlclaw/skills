# Installation Guide

This guide will help you install and set up the AML Address Screening skill.

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (for cloning the repository)
- TrustIn API key (optional, for full functionality)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/amlclaw/skills.git
cd skills/aml-address-screening
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred editor
nano .env  # or vim, code, etc.
```

Add your TrustIn API key to the `.env` file:

```bash
TRUSTIN_API_KEY=your_api_key_here
```

### 5. Verify Installation

```bash
# Test basic functionality
python3 -c "from screening import screen_address; print('Installation successful!')"
```

## Optional: Install as OpenClaw Skill

If you're using OpenClaw, you can install this as a skill:

```bash
openclaw skills install aml-address-screening
```

## Troubleshooting

### Python Version Issues

If you encounter version compatibility issues:

```bash
# Check your Python version
python3 --version

# Ensure it's 3.9 or higher
```

### Dependency Conflicts

If you have dependency conflicts:

```bash
# Use a fresh virtual environment
python3 -m venv --clear venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Import Errors

If you get import errors:

```bash
# Ensure you're in the skill directory
cd skills/aml-address-screening

# Check PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## Next Steps

- [Quick Start Guide](quick-start.md) - Get started with your first screening
- [Configuration](configuration.md) - Configure advanced options
- [User Guide](../guide/address-screening.md) - Learn about all features