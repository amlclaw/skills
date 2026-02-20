"""
Tests for the address screening functionality.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screening import (
    validate_chain,
    validate_address_format,
    get_risk_level,
    get_recommendation,
    SUPPORTED_CHAINS,
    RISK_THRESHOLDS
)

class TestAddressValidation(unittest.TestCase):
    """Test address validation functions."""
    
    def test_validate_chain(self):
        """Test chain validation."""
        self.assertTrue(validate_chain("Tron"))
        self.assertTrue(validate_chain("Ethereum"))
        self.assertTrue(validate_chain("Bitcoin"))
        self.assertTrue(validate_chain("Solana"))
        self.assertFalse(validate_chain("UnsupportedChain"))
    
    def test_validate_tron_address(self):
        """Test Tron address validation."""
        # Valid Tron address (34 chars, starts with T)
        valid_tron = "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt"
        is_valid, message = validate_address_format("Tron", valid_tron)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid Tron address")
        
        # Invalid Tron address (wrong starting char)
        invalid_tron = "1HaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt"
        is_valid, message = validate_address_format("Tron", invalid_tron)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid Tron address format")
        
        # Invalid Tron address (wrong length)
        invalid_tron = "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAm"
        is_valid, message = validate_address_format("Tron", invalid_tron)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid Tron address format")
    
    def test_validate_ethereum_address(self):
        """Test Ethereum address validation."""
        # Valid Ethereum address (0x + 40 hex chars)
        valid_eth = "0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b"
        is_valid, message = validate_address_format("Ethereum", valid_eth)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid Ethereum address")
        
        # Invalid Ethereum address (no 0x)
        invalid_eth = "742d35Cc6634C0532925a3b844Bc9eC0C17B1b0b"
        is_valid, message = validate_address_format("Ethereum", invalid_eth)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid Ethereum address format")
        
        # Invalid Ethereum address (wrong length)
        invalid_eth = "0x742d35Cc6634C0532925a3b844Bc9eC0C17B1b0"
        is_valid, message = validate_address_format("Ethereum", invalid_eth)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid Ethereum address format")

class TestRiskAssessment(unittest.TestCase):
    """Test risk assessment functions."""
    
    def test_get_risk_level(self):
        """Test risk level calculation."""
        self.assertEqual(get_risk_level(0), "LOW")
        self.assertEqual(get_risk_level(25), "LOW")
        self.assertEqual(get_risk_level(26), "MEDIUM_LOW")
        self.assertEqual(get_risk_level(50), "MEDIUM_LOW")
        self.assertEqual(get_risk_level(51), "MEDIUM")
        self.assertEqual(get_risk_level(75), "MEDIUM")
        self.assertEqual(get_risk_level(76), "HIGH")
        self.assertEqual(get_risk_level(90), "HIGH")
        self.assertEqual(get_risk_level(91), "CRITICAL")
        self.assertEqual(get_risk_level(100), "CRITICAL")
        self.assertEqual(get_risk_level(150), "UNKNOWN")  # Out of range
    
    def test_get_recommendation(self):
        """Test recommendation generation."""
        self.assertIn("Normal processing", get_recommendation("LOW"))
        self.assertIn("Enhanced monitoring", get_recommendation("MEDIUM_LOW"))
        self.assertIn("Manual review", get_recommendation("MEDIUM"))
        self.assertIn("Restricted processing", get_recommendation("HIGH"))
        self.assertIn("Reject and report", get_recommendation("CRITICAL"))
        self.assertIn("Insufficient data", get_recommendation("UNKNOWN"))

class TestScreeningIntegration(unittest.TestCase):
    """Test integration of screening functions."""
    
    @patch('screening.TrustInAPI')
    def test_screen_address_with_api(self, mock_api_class):
        """Test address screening with mocked TrustIn API."""
        # Mock the API response
        mock_api_instance = MagicMock()
        mock_api_class.return_value = mock_api_instance
        
        mock_result = MagicMock()
        mock_result.risk_score = 75
        mock_result.risk_level = "MEDIUM"
        mock_result.recommendation = "Manual review required"
        mock_result.details = {"test": "data"}
        
        mock_api_instance.kya_lite_detect.return_value = mock_result
        
        # Import after mocking
        from screening import screen_address
        
        # Test screening
        result = screen_address("Tron", "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt", verbose=False)
        
        # Verify result
        self.assertEqual(result["chain"], "Tron")
        self.assertEqual(result["risk_score"], 75)
        self.assertEqual(result["risk_level"], "MEDIUM")
        self.assertTrue(result["api_used"])
        self.assertIn("Manual review", result["recommendation"])
    
    def test_screen_address_without_api(self):
        """Test address screening without API (fallback)."""
        # Mock TrustInAPI to be unavailable
        with patch('screening.TRUSTIN_AVAILABLE', False):
            from screening import screen_address
            
            # Test with valid address
            result = screen_address(
                "Tron", 
                "THaUuZZ6PMHnLong9GTnpNFi6BGo5BaAmt",
                verbose=False
            )
            
            # Verify fallback result
            self.assertEqual(result["chain"], "Tron")
            self.assertIn(result["risk_score"], range(101))  # 0-100
            self.assertFalse(result["api_used"])
            self.assertEqual(result["data_source"], "Basic pattern analysis")

if __name__ == "__main__":
    unittest.main()