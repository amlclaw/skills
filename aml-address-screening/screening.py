"""
Core address screening logic for AML compliance.
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Try to import TrustIn API module
try:
    from .trustin_api import TrustInAPI, KYAResult
    TRUSTIN_AVAILABLE = True
except ImportError:
    TRUSTIN_AVAILABLE = False
    # Define placeholder types
    class KYAResult:
        """Placeholder for KYA result."""
        def __init__(self):
            self.risk_score = 0
            self.risk_level = "UNKNOWN"
            self.recommendation = "No data available"
            self.details = {}

    class TrustInAPI:
        """Placeholder for TrustIn API."""
        def __init__(self, api_key=None):
            self.api_key = api_key
        
        def kya_lite_detect(self, chain_name, address):
            """Placeholder method."""
            result = KYAResult()
            result.risk_score = 50  # Default medium risk
            result.risk_level = "MEDIUM"
            result.recommendation = "No TrustIn API available, using simulation"
            result.details = {"simulated": True}
            return result

# Supported blockchain networks
SUPPORTED_CHAINS = ["Tron", "Ethereum", "Bitcoin", "Solana"]

# Risk level thresholds
RISK_THRESHOLDS = {
    "LOW": (0, 25),
    "MEDIUM_LOW": (26, 50),
    "MEDIUM": (51, 75),
    "HIGH": (76, 90),
    "CRITICAL": (91, 100)
}

def validate_chain(chain: str) -> bool:
    """Validate if chain is supported."""
    return chain in SUPPORTED_CHAINS

def validate_address_format(chain: str, address: str) -> Tuple[bool, str]:
    """Validate address format for specific chain."""
    address = address.strip()
    
    if chain == "Tron":
        # Tron addresses start with T and are 34 chars
        pattern = r"^T[a-zA-Z0-9]{33}$"
        if re.match(pattern, address):
            return True, "Valid Tron address"
        return False, "Invalid Tron address format"
    
    elif chain == "Ethereum":
        # Ethereum addresses are 0x followed by 40 hex chars
        pattern = r"^0x[a-fA-F0-9]{40}$"
        if re.match(pattern, address):
            return True, "Valid Ethereum address"
        return False, "Invalid Ethereum address format"
    
    elif chain == "Bitcoin":
        # Bitcoin addresses vary (P2PKH, P2SH, Bech32)
        # Simplified check
        if len(address) >= 26 and len(address) <= 35:
            return True, "Plausible Bitcoin address"
        return False, "Invalid Bitcoin address format"
    
    elif chain == "Solana":
        # Solana addresses are base58, 32-44 chars
        if 32 <= len(address) <= 44:
            return True, "Plausible Solana address"
        return False, "Invalid Solana address format"
    
    return False, f"Unsupported chain: {chain}"

def calculate_basic_risk_score(chain: str, address: str) -> Dict:
    """Calculate basic risk score based on address characteristics."""
    risk_score = 0
    risk_factors = []
    
    # Check address format
    is_valid, message = validate_address_format(chain, address)
    if not is_valid:
        risk_score += 30
        risk_factors.append(f"Invalid address format: {message}")
    
    # Check for suspicious patterns
    suspicious_patterns = [
        (r"(?i)phish|hack|scam|fraud", 25, "Contains suspicious keywords"),
        (r"1111{4,}|0000{4,}", 15, "Repeating character pattern"),
        (r"^(0x)?0{10,}", 20, "Many leading zeros"),
    ]
    
    for pattern, points, reason in suspicious_patterns:
        if re.search(pattern, address):
            risk_score += points
            risk_factors.append(reason)
    
    # Check length anomalies
    if chain == "Ethereum" and len(address) != 42:
        risk_score += 10
        risk_factors.append("Non-standard Ethereum address length")
    
    return {
        "risk_score": min(risk_score, 100),
        "risk_factors": risk_factors,
        "basic_check": True
    }

def get_risk_level(score: int) -> str:
    """Convert numeric score to risk level."""
    for level, (low, high) in RISK_THRESHOLDS.items():
        if low <= score <= high:
            return level
    return "UNKNOWN"

def get_recommendation(risk_level: str) -> str:
    """Get action recommendation based on risk level."""
    recommendations = {
        "LOW": "🟢 Normal processing - No restrictions needed",
        "MEDIUM_LOW": "🟡 Enhanced monitoring - Review transaction patterns",
        "MEDIUM": "🟡 Manual review required - Collect additional information",
        "HIGH": "🔴 Restricted processing - Limit transaction amounts",
        "CRITICAL": "🔴 Reject and report - High risk of illicit activity",
        "UNKNOWN": "⚠️ Insufficient data - Manual investigation needed"
    }
    return recommendations.get(risk_level, recommendations["UNKNOWN"])

def screen_address(
    chain: str,
    address: str,
    api_key: Optional[str] = None,
    verbose: bool = False
) -> Dict:
    """
    Screen a blockchain address for AML risks.
    
    Args:
        chain: Blockchain network (e.g., "Tron", "Ethereum")
        address: Wallet address to screen
        api_key: TrustIn API key (optional, uses env var if not provided)
        verbose: Show detailed output
    
    Returns:
        Dictionary with screening results
    """
    start_time = datetime.now()
    
    # Validate inputs
    if not validate_chain(chain):
        raise ValueError(f"Unsupported chain: {chain}. Supported: {SUPPORTED_CHAINS}")
    
    # Basic validation and risk scoring
    basic_result = calculate_basic_risk_score(chain, address)
    is_valid, validation_msg = validate_address_format(chain, address)
    
    # TrustIn API integration
    trustin_result = None
    api_used = False
    
    if TRUSTIN_AVAILABLE:
        try:
            api = TrustInAPI(api_key=api_key)
            trustin_result = api.kya_lite_detect(chain, address)
            api_used = True
            
            if verbose:
                print(f"[DEBUG] TrustIn API call successful: {trustin_result.risk_score}")
                
        except Exception as e:
            if verbose:
                print(f"[DEBUG] TrustIn API error: {str(e)}")
            # Fall back to basic scoring
            trustin_result = None
    
    # Combine results
    if trustin_result and api_used:
        risk_score = trustin_result.risk_score
        risk_details = trustin_result.details
        recommendation = trustin_result.recommendation
        data_source = "TrustIn KYA API"
    else:
        risk_score = basic_result["risk_score"]
        risk_details = {"basic_checks": basic_result["risk_factors"]}
        recommendation = get_recommendation(get_risk_level(risk_score))
        data_source = "Basic pattern analysis"
    
    # Prepare final result
    result = {
        "chain": chain,
        "address": address,
        "risk_score": risk_score,
        "risk_level": get_risk_level(risk_score),
        "recommendation": recommendation,
        "data_source": data_source,
        "address_valid": is_valid,
        "validation_message": validation_msg,
        "screening_time": str(datetime.now() - start_time),
        "timestamp": datetime.now().isoformat(),
        "details": risk_details,
        "api_used": api_used
    }
    
    return result

def format_result(result: Dict, verbose: bool = False) -> str:
    """Format screening result for display."""
    lines = []
    
    # Header
    lines.append("=" * 60)
    lines.append(f"AML ADDRESS SCREENING RESULT")
    lines.append("=" * 60)
    
    # Basic info
    lines.append(f"Chain: {result['chain']}")
    lines.append(f"Address: {result['address']}")
    lines.append(f"Address Valid: {'✅ Yes' if result['address_valid'] else '❌ No'}")
    if result['validation_message']:
        lines.append(f"Validation: {result['validation_message']}")
    
    lines.append("-" * 60)
    
    # Risk assessment
    lines.append(f"Risk Score: {result['risk_score']}/100")
    lines.append(f"Risk Level: {result['risk_level']}")
    lines.append(f"Recommendation: {result['recommendation']}")
    
    lines.append("-" * 60)
    
    # Technical details
    lines.append(f"Data Source: {result['data_source']}")
    lines.append(f"Screening Time: {result['screening_time']}")
    lines.append(f"API Used: {'✅ Yes' if result['api_used'] else '❌ No (fallback)'}")
    
    if verbose and result['details']:
        lines.append("-" * 60)
        lines.append("DETAILED ANALYSIS:")
        for key, value in result['details'].items():
            if isinstance(value, dict):
                lines.append(f"  {key}:")
                for subkey, subvalue in value.items():
                    lines.append(f"    {subkey}: {subvalue}")
            else:
                lines.append(f"  {key}: {value}")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)

# Export for easy import
__all__ = [
    "screen_address",
    "validate_address",  # Alias for validate_address_format
    "validate_address_format",
    "validate_chain",
    "get_risk_assessment",  # Alias for screen_address
    "format_result",
    "SUPPORTED_CHAINS",
    "RISK_THRESHOLDS",
    "get_risk_level",
    "get_recommendation"
]

# Aliases for backward compatibility
validate_address = validate_address_format
get_risk_assessment = screen_address