"""
Test configuration and environment setup.
"""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestEnvironment(unittest.TestCase):
    """Test environment configuration."""
    
    def test_environment_variables(self):
        """Test that environment variables can be set."""
        # Test with mock environment
        with patch.dict(os.environ, {"TRUSTIN_API_KEY": "test_key"}):
            from trustin_api import TrustInAPI
            
            # Should not raise error with env var set
            try:
                api = TrustInAPI()
                self.assertEqual(api.api_key, "test_key")
            except ValueError:
                self.fail("TrustInAPI should work with env var set")
    
    def test_missing_api_key(self):
        """Test error when API key is missing."""
        # Clear environment
        with patch.dict(os.environ, {}, clear=True):
            from trustin_api import TrustInAPI
            
            # Should raise error without API key
            with self.assertRaises(ValueError) as context:
                TrustInAPI()
            
            self.assertIn("No TrustIn API key", str(context.exception))
    
    def test_api_key_parameter(self):
        """Test API key passed as parameter."""
        from trustin_api import TrustInAPI
        
        # Clear environment
        with patch.dict(os.environ, {}, clear=True):
            # Should work with parameter
            api = TrustInAPI(api_key="param_key")
            self.assertEqual(api.api_key, "param_key")

class TestImport(unittest.TestCase):
    """Test module imports."""
    
    def test_import_screening(self):
        """Test screening module import."""
        try:
            from screening import (
                screen_address,
                validate_chain,
                SUPPORTED_CHAINS
            )
            self.assertTrue(callable(screen_address))
            self.assertTrue(callable(validate_chain))
            self.assertIsInstance(SUPPORTED_CHAINS, list)
        except ImportError as e:
            self.fail(f"Failed to import screening module: {e}")
    
    def test_import_trustin_api(self):
        """Test trustin_api module import."""
        try:
            from trustin_api import (
                TrustInAPI,
                KYAResult,
                screen_with_trustin
            )
            self.assertTrue(callable(TrustInAPI))
            self.assertTrue(callable(screen_with_trustin))
        except ImportError as e:
            self.fail(f"Failed to import trustin_api module: {e}")

if __name__ == "__main__":
    unittest.main()