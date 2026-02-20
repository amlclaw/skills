from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aml-address-screening",
    version="0.1.0",
    author="amlclaw",
    author_email="contact@amlclaw.com",
    description="AML Address Screening Skill for OpenClaw - Blockchain address risk assessment using TrustIn KYA API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amlclaw/skills/aml-address-screening",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "aml-screen-address=aml_address_screening:main",
        ],
    },
    include_package_data=True,
    package_data={
        "aml_address_screening": [".env.example", "*.md"],
    },
    keywords="aml compliance blockchain address screening tron ethereum trustin",
    project_urls={
        "Bug Reports": "https://github.com/amlclaw/skills/issues",
        "Source": "https://github.com/amlclaw/skills/aml-address-screening",
        "Documentation": "https://github.com/amlclaw/docs",
    },
)