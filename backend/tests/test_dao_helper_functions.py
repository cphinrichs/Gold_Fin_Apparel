"""
Test suite for DAO helper functions in dao_helper_functions.py

Tests the utility functions used by the database access layer including
price calculations, data conversions, and connection management.
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# Add the src directory to the path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock the ibm_db modules before any imports
sys.modules['ibm_db'] = Mock()
sys.modules['ibm_db_dbi'] = Mock()

# Now we can import the helper functions
from database import dao_helper_functions as helper  # pylint: disable=wrong-import-position
from order_validation.order_validator import Order  # pylint: disable=wrong-import-position


class TestGetItemPrice(unittest.TestCase):
    """Test cases for get_item_price() function"""

    def test_get_item_price_basic_calculation(self):
        """Test basic price calculation without gold trim"""
        item_data = {
            "Size_Factor": 1.0,
            "Style_Price": 25.0,
            "Material_Price": 15.0,
            "Design_Price": 10.0,
            "Gold_Trim": False
        }
        
        price = helper.get_item_price(item_data)
        
        # (Style_Price * Size_Factor) + Material_Price + Design_Price
        # (25.0 * 1.0) + 15.0 + 10.0 = 50.0
        self.assertEqual(price, 50.0)

    def test_get_item_price_with_size_factor(self):
        """Test price calculation with size factor multiplier"""
        item_data = {
            "Size_Factor": 1.5,
            "Style_Price": 20.0,
            "Material_Price": 10.0,
            "Design_Price": 5.0,
            "Gold_Trim": False
        }
        
        price = helper.get_item_price(item_data)
        
        # (20.0 * 1.5) + 10.0 + 5.0 = 45.0
        self.assertEqual(price, 45.0)

    @patch('database.dao_helper_functions.backend_settings', {'Gold_Trim_Price': 20.0})
    def test_get_item_price_with_gold_trim(self):
        """Test price calculation with gold trim option"""
        item_data = {
            "Size_Factor": 1.0,
            "Style_Price": 25.0,
            "Material_Price": 15.0,
            "Design_Price": 10.0,
            "Gold_Trim": True
        }
        
        price = helper.get_item_price(item_data)
        
        # (25.0 * 1.0) + 15.0 + 10.0 + 20.0 = 70.0
        self.assertEqual(price, 70.0)

    def test_get_item_price_without_gold_trim_key(self):
        """Test price calculation when Gold_Trim key is not present"""
        item_data = {
            "Size_Factor": 1.0,
            "Style_Price": 30.0,
            "Material_Price": 20.0,
            "Design_Price": 15.0
        }
        
        price = helper.get_item_price(item_data)
        
        # Should not add gold trim price when key is missing
        # (30.0 * 1.0) + 20.0 + 15.0 = 65.0
        self.assertEqual(price, 65.0)

    def test_get_item_price_zero_values(self):
        """Test price calculation with zero values"""
        item_data = {
            "Size_Factor": 0.0,
            "Style_Price": 0.0,
            "Material_Price": 0.0,
            "Design_Price": 0.0,
            "Gold_Trim": False
        }
        
        price = helper.get_item_price(item_data)
        
        self.assertEqual(price, 0.0)


class TestConvertInventoryData(unittest.TestCase):
    """Test cases for convert_inventory_data() function"""

    def test_convert_inventory_data_complete_row(self):
        """Test converting a complete database row to dictionary"""
        # Tuple format: (PRODUCT_ID, SIZE, STYLE, MATERIAL, COLOR, STOCK, SIZE_FACTOR, STYLE_PRICE, MATERIAL_PRICE)
        row = (1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0)
        
        result = helper.convert_inventory_data(row)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Product_Id"], 1)
        self.assertEqual(result["Size"], "M")
        self.assertEqual(result["Style"], "Casual")
        self.assertEqual(result["Material"], "Cotton")
        self.assertEqual(result["Color"], "Blue")
        self.assertEqual(result["Stock"], 10)
        # Price should be calculated: (25.0 * 1.0) + 15.0 + 0.0 = 40.0
        self.assertEqual(result["Price"], 40.0)

    def test_convert_inventory_data_different_size_factor(self):
        """Test conversion with different size factor"""
        row = (2, "XL", "Formal", "Silk", "Red", 5, 1.5, 50.0, 30.0)
        
        result = helper.convert_inventory_data(row)
        
        self.assertEqual(result["Product_Id"], 2)
        self.assertEqual(result["Size"], "XL")
        # Price: (50.0 * 1.5) + 30.0 + 0.0 = 105.0
        self.assertEqual(result["Price"], 105.0)

    def test_convert_inventory_data_zero_stock(self):
        """Test conversion with zero stock"""
        row = (3, "S", "Athletic", "Polyester", "Black", 0, 0.8, 20.0, 10.0)
        
        result = helper.convert_inventory_data(row)
        
        self.assertEqual(result["Stock"], 0)
        # Price: (20.0 * 0.8) + 10.0 + 0.0 = 26.0
        self.assertEqual(result["Price"], 26.0)

    def test_convert_inventory_data_keys_present(self):
        """Test that all expected keys are present in the result"""
        row = (1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0)
        
        result = helper.convert_inventory_data(row)
        
        expected_keys = ["Product_Id", "Size", "Style", "Material", "Color", "Stock", "Price"]
        for key in expected_keys:
            self.assertIn(key, result)


class TestGetOrderPrice(unittest.TestCase):
    """Test cases for get_order_price() function"""

    def test_get_order_price_returns_float(self):
        """Test that get_order_price returns a float"""
        mock_order = Mock(spec=Order)
        
        price = helper.get_order_price(mock_order)
        
        self.assertIsInstance(price, float)

    def test_get_order_price_returns_zero(self):
        """Test that get_order_price currently returns 0.0 (TODO implementation)"""
        mock_order = Mock(spec=Order)
        
        price = helper.get_order_price(mock_order)
        
        # Current implementation returns 0.0 as placeholder
        self.assertEqual(price, 0.0)


class TestGetPooledConnection(unittest.TestCase):
    """Test cases for get_pooled_connection() function"""

    @patch('database.dao_helper_functions.ibm_db')
    @patch('database.dao_helper_functions.ibm_db_dbi')
    def test_get_pooled_connection_success(self, mock_ibm_db_dbi, mock_ibm_db):
        """Test successful connection creation"""
        # Mock the connection objects
        mock_raw_conn = MagicMock()
        mock_ibm_db.pconnect.return_value = mock_raw_conn
        mock_ibm_db.IBM_DBConnection = type(mock_raw_conn)
        
        mock_wrapped_conn = MagicMock()
        mock_ibm_db_dbi.Connection.return_value = mock_wrapped_conn
        
        conn_str = "DATABASE=TEST;HOSTNAME=localhost;PORT=50000;"
        
        result = helper.get_pooled_connection(conn_str)
        
        # Verify pconnect was called with correct parameters
        mock_ibm_db.pconnect.assert_called_once_with(conn_str, "", "")
        
        # Verify Connection wrapper was created
        mock_ibm_db_dbi.Connection.assert_called_once_with(mock_raw_conn)
        
        # Verify result is the wrapped connection
        self.assertEqual(result, mock_wrapped_conn)

    @patch('database.dao_helper_functions.ibm_db')
    def test_get_pooled_connection_failure(self, mock_ibm_db):
        """Test connection failure handling"""
        # Mock pconnect to raise an exception
        mock_ibm_db.pconnect.side_effect = Exception("Connection failed")
        
        conn_str = "DATABASE=TEST;HOSTNAME=invalid;PORT=50000;"
        
        with self.assertRaises(Exception) as context:
            helper.get_pooled_connection(conn_str)
        
        self.assertIn("Connection failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
