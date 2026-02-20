"""
TrustIn API integration for AML address screening.

This module provides integration with TrustIn's KYA (Know Your Address) API
for blockchain address risk assessment.
"""

import os
import json
import requests
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class KYAResult:
    """Result from TrustIn KYA API."""
    risk_score: int
    risk_level: str
    recommendation: str
    details: Dict[str, Any]
    raw_response: Optional[Dict] = None
    error: Optional[str] = None

class TrustInAPI:
    """Client for TrustIn API."""
    
    BASE_URL = "https://api.trustin.info/api/v2/detect"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TrustIn API client.
        
        Args:
            api_key: TrustIn API key. If not provided, will try TRUSTIN_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("TRUSTIN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No TrustIn API key provided. "
                "Set TRUSTIN_API_KEY environment variable or pass api_key parameter."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "amlclaw-address-screening/0.1.0"
        })
    
    def _make_request(self, endpoint: str, data: Dict) -> Dict:
        """Make request to TrustIn API."""
        url = f"{self.BASE_URL}/{endpoint}?apikey={self.api_key}"
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("TrustIn API request timed out")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to TrustIn API")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid TrustIn API key")
            elif e.response.status_code == 403:
                raise Exception("Insufficient API key permissions")
            elif e.response.status_code == 429:
                raise Exception("API rate limit exceeded")
            else:
                raise Exception(f"TrustIn API error: {e}")
        except json.JSONDecodeError:
            raise Exception("Invalid response from TrustIn API")
    
    def kya_lite_detect(self, chain_name: str, address: str) -> KYAResult:
        """
        Perform KYA Lite detection (quick address screening).
        
        Args:
            chain_name: Blockchain name (e.g., "Tron", "Ethereum")
            address: Wallet address to screen
        
        Returns:
            KYAResult with risk assessment
        """
        # Map chain names to TrustIn format
        chain_mapping = {
            "Tron": "Tron",
            "Ethereum": "Ethereum",
            "Bitcoin": "Bitcoin",
            "Solana": "Solana"
        }
        
        if chain_name not in chain_mapping:
            raise ValueError(f"Unsupported chain for TrustIn API: {chain_name}")
        
        data = {
            "chain_name": chain_mapping[chain_name],
            "address": address
        }
        
        try:
            response = self._make_request("kya_lite_detect", data)
            
            # Parse response
            if response.get("code") == 200:
                result_data = response.get("data", {})
                
                # Extract risk score (TrustIn returns 0-100)
                risk_score = result_data.get("risk_score", 50)
                
                # Convert to risk level
                if risk_score < 25:
                    risk_level = "LOW"
                    recommendation = "Low risk - Normal processing"
                elif risk_score < 50:
                    risk_level = "MEDIUM_LOW"
                    recommendation = "Medium-low risk - Enhanced monitoring"
                elif risk_score < 75:
                    risk_level = "MEDIUM"
                    recommendation = "Medium risk - Manual review"
                elif risk_score < 90:
                    risk_level = "HIGH"
                    recommendation = "High risk - Restrict transactions"
                else:
                    risk_level = "CRITICAL"
                    recommendation = "Critical risk - Reject and report"
                
                return KYAResult(
                    risk_score=risk_score,
                    risk_level=risk_level,
                    recommendation=recommendation,
                    details=result_data,
                    raw_response=response
                )
            else:
                error_msg = response.get("msg", "Unknown TrustIn API error")
                return KYAResult(
                    risk_score=50,  # Default medium risk
                    risk_level="UNKNOWN",
                    recommendation=f"API Error: {error_msg} - Manual review required",
                    details={"error": error_msg, "response": response},
                    error=error_msg
                )
                
        except Exception as e:
            # Return fallback result on API failure
            return KYAResult(
                risk_score=50,  # Default medium risk
                risk_level="UNKNOWN",
                recommendation=f"API Unavailable: {str(e)} - Using fallback analysis",
                details={"api_error": str(e), "fallback": True},
                error=str(e)
            )
    
    def kya_pro_detect(self, chain_name: str, address: str, **kwargs) -> KYAResult:
        """
        Perform KYA Pro detection (deep address analysis).
        
        Args:
            chain_name: Blockchain name
            address: Wallet address to screen
            **kwargs: Additional parameters for KYA Pro:
                - inflow_hops: Inflow trace hops (1-5)
                - outflow_hops: Outflow trace hops (1-5)
                - min_timestamp: Minimum timestamp in milliseconds
                - max_timestamp: Maximum timestamp in milliseconds
                - is_penetrate_contracts: Whether to penetrate contracts
        
        Returns:
            KYAResult with detailed risk assessment
        """
        # Default parameters for KYA Pro
        params = {
            "chain_name": chain_name,
            "address": address,
            "inflow_hops": kwargs.get("inflow_hops", 3),
            "outflow_hops": kwargs.get("outflow_hops", 3),
            "min_timestamp": kwargs.get("min_timestamp", 0),
            "max_timestamp": kwargs.get("max_timestamp", int(datetime.now().timestamp() * 1000)),
            "is_penetrate_contracts": kwargs.get("is_penetrate_contracts", True)
        }
        
        try:
            response = self._make_request("kya_detect", params)
            
            if response.get("code") == 200:
                result_data = response.get("data", {})
                
                # KYA Pro provides more detailed risk assessment
                risk_score = result_data.get("risk_score", 50)
                risk_tags = result_data.get("risk_tags", [])
                
                # Build recommendation based on risk tags
                if not risk_tags:
                    recommendation = "No specific risk tags identified"
                else:
                    recommendation = f"Risk tags: {', '.join(risk_tags[:3])}"
                
                # Enhanced risk level calculation
                if risk_score < 20:
                    risk_level = "LOW"
                elif risk_score < 40:
                    risk_level = "MEDIUM_LOW"
                elif risk_score < 60:
                    risk_level = "MEDIUM"
                elif risk_score < 80:
                    risk_level = "HIGH"
                else:
                    risk_level = "CRITICAL"
                
                return KYAResult(
                    risk_score=risk_score,
                    risk_level=risk_level,
                    recommendation=recommendation,
                    details=result_data,
                    raw_response=response
                )
            else:
                error_msg = response.get("msg", "Unknown TrustIn API error")
                return KYAResult(
                    risk_score=50,
                    risk_level="UNKNOWN",
                    recommendation=f"KYA Pro Error: {error_msg}",
                    details={"error": error_msg, "response": response},
                    error=error_msg
                )
                
        except Exception as e:
            return KYAResult(
                risk_score=50,
                risk_level="UNKNOWN",
                recommendation=f"KYA Pro Unavailable: {str(e)}",
                details={"api_error": str(e), "fallback": True},
                error=str(e)
            )

# Helper functions for direct usage
def screen_with_trustin(
    chain: str,
    address: str,
    api_key: Optional[str] = None,
    use_pro: bool = False,
    **kwargs
) -> Dict:
    """
    Convenience function to screen address with TrustIn API.
    
    Args:
        chain: Blockchain network
        address: Wallet address
        api_key: TrustIn API key (optional)
        use_pro: Use KYA Pro instead of KYA Lite
        **kwargs: Additional parameters for KYA Pro
    
    Returns:
        Dictionary with screening results
    """
    api = TrustInAPI(api_key=api_key)
    
    if use_pro:
        result = api.kya_pro_detect(chain, address, **kwargs)
    else:
        result = api.kya_lite_detect(chain, address)
    
    return {
        "risk_score": result.risk_score,
        "risk_level": result.risk_level,
        "recommendation": result.recommendation,
        "details": result.details,
        "api_used": True,
        "api_error": result.error,
        "timestamp": datetime.now().isoformat()
    }

# Export for easy import
__all__ = [
    "TrustInAPI",
    "KYAResult",
    "screen_with_trustin"
]