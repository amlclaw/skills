"""
AML Address Screening Skill for OpenClaw

This skill screens blockchain addresses for AML risks using TrustIn KYA API.
"""

import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .screening import (
    screen_address,
    validate_address,
    get_risk_assessment,
    format_result,
    SUPPORTED_CHAINS
)

__version__ = "0.1.0"
__author__ = "amlclaw"
__description__ = "AML Address Screening using TrustIn KYA API"

def main():
    """Main entry point for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Screen blockchain addresses for AML risks"
    )
    parser.add_argument(
        "chain",
        choices=SUPPORTED_CHAINS,
        help="Blockchain network (e.g., Tron, Ethereum)"
    )
    parser.add_argument(
        "address",
        help="Wallet address to screen"
    )
    parser.add_argument(
        "--api-key",
        help="TrustIn API key (optional, can use TRUSTIN_API_KEY env var)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    try:
        result = screen_address(
            chain=args.chain,
            address=args.address,
            api_key=args.api_key,
            verbose=args.verbose
        )
        
        formatted = format_result(result, verbose=args.verbose)
        print(formatted)
        
        # Return exit code based on risk level
        if result["risk_score"] >= 75:  # High risk
            sys.exit(2)
        elif result["risk_score"] >= 50:  # Medium risk
            sys.exit(1)
        else:  # Low risk
            sys.exit(0)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(3)

if __name__ == "__main__":
    main()