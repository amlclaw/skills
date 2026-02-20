"""
Basic usage examples for aml-address-screening skill.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screening import screen_address, format_result

def example_basic_screening():
    """Example: Basic address screening."""
    print("Example 1: Basic Address Screening")
    print("=" * 50)
    
    # Screen a Tron address
    result = screen_address(
        chain="Tron",
        address="THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt",
        verbose=True
    )
    
    print(format_result(result, verbose=True))
    print("\n")

def example_without_api():
    """Example: Screening without TrustIn API (fallback)."""
    print("Example 2: Screening Without TrustIn API (Fallback)")
    print("=" * 50)
    
    # This will use fallback pattern analysis
    result = screen_address(
        chain="Ethereum",
        address="0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b",
        verbose=False
    )
    
    print(format_result(result, verbose=True))
    print("\n")

def example_command_line_usage():
    """Example: How to use from command line."""
    print("Example 3: Command Line Usage")
    print("=" * 50)
    print("""
# Basic usage:
python3 -m aml_address_screening Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt

# With API key:
TRUSTIN_API_KEY=your_key python3 -m aml_address_screening Ethereum 0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b

# Verbose output:
python3 -m aml_address_screening Tron THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt --verbose

# Using as a module:
import aml_address_screening
result = aml_address_screening.screen_address("Tron", "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt")
    """)
    print("\n")

def example_risk_interpretation():
    """Example: Interpreting risk scores."""
    print("Example 4: Risk Score Interpretation")
    print("=" * 50)
    
    risk_examples = [
        (10, "LOW", "🟢 Normal processing"),
        (35, "MEDIUM_LOW", "🟡 Enhanced monitoring"),
        (65, "MEDIUM", "🟡 Manual review required"),
        (85, "HIGH", "🔴 Restricted processing"),
        (95, "CRITICAL", "🔴 Reject and report"),
    ]
    
    for score, level, action in risk_examples:
        print(f"Score {score}/100: {level} -> {action}")
    
    print("\n")

def example_integration():
    """Example: Integration with other systems."""
    print("Example 5: Integration with Compliance Workflow")
    print("=" * 50)
    
    # Simulate a compliance workflow
    addresses_to_screen = [
        ("Tron", "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt"),
        ("Ethereum", "0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b"),
        ("Tron", "TZ73Ue3KUP4PZwZJoj9v71skBShdCXksSw"),
    ]
    
    print("Screening multiple addresses:")
    for chain, address in addresses_to_screen:
        result = screen_address(chain, address, verbose=False)
        
        # Make decision based on risk
        risk_score = result["risk_score"]
        if risk_score < 25:
            decision = "APPROVE"
        elif risk_score < 50:
            decision = "MONITOR"
        elif risk_score < 75:
            decision = "REVIEW"
        else:
            decision = "REJECT"
        
        print(f"  {chain}: {address[:12]}... -> Score: {risk_score} -> Decision: {decision}")
    
    print("\n")

if __name__ == "__main__":
    print("AML Address Screening - Usage Examples")
    print("=" * 60)
    print("\n")
    
    example_basic_screening()
    example_without_api()
    example_command_line_usage()
    example_risk_interpretation()
    example_integration()
    
    print("=" * 60)
    print("End of examples. Refer to documentation for more details.")