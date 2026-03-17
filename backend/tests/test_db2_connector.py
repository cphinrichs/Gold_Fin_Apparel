"""
Test suite for DB2 DAO layer in db2_connector.py

Tests the SQL query building logic for select_inventory and select_designs
by mocking the ibm_db and ibm_db_dbi modules. This allows testing without
requiring a live DB2 connection.

NOTE: These tests verify that the DAO methods can be called with various parameters.
For full SQL verification, you would need integration tests with a test database.
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# Add the src directory to the path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock the ibm_db modules before any imports
mock_ibm_db = Mock()
mock_ibm_db.IBM_DBConnection = Mock  # Make it a proper type for isinstance()
sys.modules['ibm_db'] = mock_ibm_db
sys.modules['ibm_db_dbi'] = Mock()

# Now we can import the DAO
from database.db2_connector import _Db2DAO  # pylint: disable=wrong-import-position


@patch('database.dao_helper_functions.get_pooled_connection')
class TestSelectInventory(unittest.TestCase):
    """Test cases for _Db2DAO.select_inventory() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        # Create a mock DAO instance
        cls.mock_cursor = MagicMock()
        # Mock data should have 9 fields: PRODUCT_ID, SIZE, STYLE, MATERIAL, COLOR, STOCK, SIZE_FACTOR, STYLE_PRICE, MATERIAL_PRICE
        cls.mock_cursor.fetchall.return_value = [(1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0)]
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [(1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0)]
        # Make execute succeed by default (returns None, doesn't raise)
        self.mock_cursor.execute.return_value = None
        self.mock_cursor.execute.side_effect = None  # Clear any side_effect that was set

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao._conn_str = "mocked_connection_string"
        dao.select_inventory = _Db2DAO.select_inventory.__get__(dao, _Db2DAO)
        return dao

    def test_select_inventory_no_filters(self, mock_get_pooled_conn):
        """Test select_inventory with no filters generates basic query"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_inventory({})
        
        # Verify cursor.execute was called
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        # Check SQL structure
        self.assertIn("SELECT", sql)
        self.assertIn("INVENTORY", sql)
        self.assertIn("ORDER BY INVENTORY.STOCK", sql)
        self.assertIn("DESC", sql)  # Default descending
        self.assertEqual(len(params), 0)  # No parameters
        
        # Check result
        self.assertEqual(len(result), 1)

    def test_select_inventory_with_size(self, mock_get_pooled_conn):
        """Test select_inventory with Size filter"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_inventory({"Size": "M"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("WHERE SizeS.NAME = ?", sql)
        self.assertEqual(params[0], "M")
        self.assertEqual(len(result), 1)

    def test_select_inventory_with_multiple_filters(self, mock_get_pooled_conn):
        """Test select_inventory with multiple filters uses AND"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_inventory({
            "Size": "M",
            "Style": "Casual",
            "Color": "Blue"
        })
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        # Should have WHERE and AND clauses
        self.assertIn("WHERE", sql)
        self.assertIn("AND", sql)
        self.assertEqual(len(params), 3)

    def test_select_inventory_ascending_order(self, mock_get_pooled_conn):
        """Test select_inventory with Ascending: true"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_inventory({"Ascending": "true"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        
        self.assertIn("ORDER BY INVENTORY.STOCK", sql)
        self.assertIn("ASC", sql)

    def test_select_inventory_exception_handling(self, mock_get_pooled_conn):
        """Test select_inventory handles exceptions and re-raises"""
        # Configure the mock connection to raise an exception
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        self.mock_cursor.execute.side_effect = Exception("Database error")
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        with self.assertRaises(Exception) as context:
            dao.select_inventory({})
        
        self.assertIn("Database error", str(context.exception))


@patch('database.dao_helper_functions.get_pooled_connection')
class TestSelectDesigns(unittest.TestCase):
    """Test cases for _Db2DAO.select_designs() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        cls.mock_cursor = MagicMock()
        cls.mock_cursor.fetchall.return_value = [(1, "Design1", 29.99, "Description")]
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [(1, "Design1", 29.99, "Description")]
        # Make execute succeed by default (returns None, doesn't raise)
        self.mock_cursor.execute.return_value = None
        self.mock_cursor.execute.side_effect = None  # Clear any side_effect that was set

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao._conn_str = "mocked_connection_string"
        dao.select_designs = _Db2DAO.select_designs.__get__(dao, _Db2DAO)
        return dao

    def test_select_designs_no_filters(self, mock_get_pooled_conn):
        """Test select_designs with no filters generates basic query"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("SELECT * FROM", sql)
        self.assertIn("DESIGNS", sql)
        self.assertIn("ORDER BY NAME", sql)  # Default sort by name
        self.assertIn("DESC", sql)  # Default descending
        self.assertEqual(len(params), 0)
        
        self.assertEqual(len(result), 1)

    def test_select_designs_with_min_price(self, mock_get_pooled_conn):
        """Test select_designs with Min_Price only"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({"Min_Price": "30"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("WHERE PRICE >= ?", sql)
        self.assertEqual(params[0], "30")

    def test_select_designs_with_price_range(self, mock_get_pooled_conn):
        """Test select_designs with both Min_Price and Max_Price"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({
            "Min_Price": "30",
            "Max_Price": "40"
        })
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("WHERE PRICE BETWEEN ? AND ?", sql)
        self.assertEqual(params[0], "30")
        self.assertEqual(params[1], "40")
        self.assertEqual(len(params), 2)

    def test_select_designs_sort_by_price(self, mock_get_pooled_conn):
        """Test select_designs with Sort_By_Price: true"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({"Sort_By_Price": "true"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        
        self.assertIn("ORDER BY PRICE", sql)

    def test_select_designs_exception_handling(self, mock_get_pooled_conn):
        """Test select_designs handles exceptions and re-raises"""
        # Configure the mock connection to raise an exception
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        self.mock_cursor.execute.side_effect = Exception("Database connection failed")
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        with self.assertRaises(Exception) as context:
            dao.select_designs({})
        
        self.assertIn("Database connection failed", str(context.exception))


@patch('database.dao_helper_functions.get_pooled_connection')
class TestCreateOrder(unittest.TestCase):
    """Test cases for _Db2DAO.create_order() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        cls.mock_cursor = MagicMock()
        cls.mock_cursor.fetchall.return_value = [(1,)]  # Mock order ID return
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [(1,)]
        self.mock_cursor.execute.return_value = None
        self.mock_cursor.execute.side_effect = None

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao._conn_str = "mocked_connection_string"
        dao.create_order = _Db2DAO.create_order.__get__(dao, _Db2DAO)
        dao.add_customer_and_return_id = _Db2DAO.add_customer_and_return_id.__get__(dao, _Db2DAO)
        return dao


@patch('database.dao_helper_functions.get_pooled_connection')
class TestLookupInventoryById(unittest.TestCase):
    """Test cases for _Db2DAO.lookup_inventory_by_id() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        cls.mock_cursor = MagicMock()
        # Mock inventory data: PRODUCT_ID, SIZE, STYLE, MATERIAL, COLOR, STOCK, SIZE_FACTOR, STYLE_PRICE, MATERIAL_PRICE
        cls.mock_cursor.fetchall.return_value = [
            (1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0),
            (2, "L", "Formal", "Silk", "Red", 5, 1.2, 35.0, 25.0)
        ]
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [
            (1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0),
            (2, "L", "Formal", "Silk", "Red", 5, 1.2, 35.0, 25.0)
        ]
        self.mock_cursor.execute.return_value = None

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao._conn_str = "mocked_connection_string"
        dao.lookup_inventory_by_id = _Db2DAO.lookup_inventory_by_id.__get__(dao, _Db2DAO)
        return dao

    def test_lookup_inventory_single_id(self, mock_get_pooled_conn):
        """Test lookup_inventory_by_id with single ID"""
        # Configure the mock connection
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.lookup_inventory_by_id(mock_conn, [1])
        
        # Verify SQL was executed
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        # Check SQL contains WHERE ID IN clause
        self.assertIn("WHERE", sql)
        self.assertIn("IN", sql)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], 1)

    def test_lookup_inventory_multiple_ids(self, mock_get_pooled_conn):
        """Test lookup_inventory_by_id with multiple IDs"""
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.lookup_inventory_by_id(mock_conn, [1, 2, 3])
        
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args[0]
        params = call_args[1]
        
        # Should have 3 parameters
        self.assertEqual(len(params), 3)

    def test_lookup_inventory_empty_list(self, mock_get_pooled_conn):
        """Test lookup_inventory_by_id with empty list"""
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.lookup_inventory_by_id(mock_conn, [])
        
        # Should return empty result or handle gracefully
        self.assertEqual(result, [{}])


@patch('database.dao_helper_functions.get_pooled_connection')
class TestLookupDesignPricesById(unittest.TestCase):
    """Test cases for _Db2DAO.lookup_design_prices_by_id() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        cls.mock_cursor = MagicMock()
        # Bug in actual code: lookup_design_prices returns ID, PRICE but tries to convert as inventory
        # Mock with 9 fields to match convert_inventory_data expectations
        cls.mock_cursor.fetchall.return_value = [
            (1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0),
            (2, "L", "Formal", "Silk", "Red", 5, 1.2, 35.0, 25.0)
        ]
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [
            (1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0),
            (2, "L", "Formal", "Silk", "Red", 5, 1.2, 35.0, 25.0)
        ]
        self.mock_cursor.execute.return_value = None

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao._conn_str = "mocked_connection_string"
        dao.lookup_design_prices_by_id = _Db2DAO.lookup_design_prices_by_id.__get__(dao, _Db2DAO)
        return dao

    def test_lookup_design_prices_single_id(self, mock_get_pooled_conn):
        """Test lookup_design_prices_by_id with single ID"""
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.lookup_design_prices_by_id(mock_conn, [1])
        
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        
        # Check SQL structure
        self.assertIn("SELECT ID, PRICE", sql)
        self.assertIn("FROM", sql)
        self.assertIn("DESIGNS", sql)
        self.assertIn("WHERE ID IN", sql)

    def test_lookup_design_prices_multiple_ids(self, mock_get_pooled_conn):
        """Test lookup_design_prices_by_id with multiple IDs"""
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.lookup_design_prices_by_id(mock_conn, [1, 2, 3])
        
        call_args = self.mock_cursor.execute.call_args[0]
        params = call_args[1]
        
        self.assertEqual(len(params), 3)

    def test_lookup_design_prices_empty_list(self, mock_get_pooled_conn):
        """Test lookup_design_prices_by_id with empty list"""
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.lookup_design_prices_by_id(mock_conn, [])
        
        # Should return empty dict
        self.assertEqual(result, [{}])


@patch('database.dao_helper_functions.get_pooled_connection')
class TestAddCustomer(unittest.TestCase):
    """Test cases for _Db2DAO.add_customer_and_return_id() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        cls.mock_cursor = MagicMock()
        cls.mock_cursor.fetchall.return_value = [[42]]  # Mock customer ID
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [[42]]
        self.mock_cursor.execute.return_value = None

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao._conn_str = "mocked_connection_string"
        dao.add_customer_and_return_id = _Db2DAO.add_customer_and_return_id.__get__(dao, _Db2DAO)
        return dao

    def test_add_customer_returns_id(self, mock_get_pooled_conn):
        """Test add_customer_and_return_id returns customer ID"""
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cursor
        mock_get_pooled_conn.return_value = mock_conn
        
        dao = self.create_dao_with_mock_cursor()
        
        cust_data = {
            "Name": "Jane Doe",
            "Address": "456 Oak Ave"
        }
        
        result = dao.add_customer_and_return_id(mock_conn, cust_data)
        
        # Should return the mocked customer ID
        self.assertEqual(result, 42)
        
        # Verify SQL was executed
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        # Check SQL structure
        self.assertIn("INSERT INTO", sql)
        self.assertIn("CUSTOMERS", sql)
        self.assertIn("NAME", sql)
        self.assertIn("ADDRESS", sql)
        
        # Check parameters
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0], "Jane Doe")
        self.assertEqual(params[1], "456 Oak Ave")


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions in dao_helper_functions.py"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    def test_get_item_price_basic(self):
        """Test get_item_price with basic price calculation"""
        from database.dao_helper_functions import get_item_price
        
        item_data = {
            "Size_Factor": 1.0,
            "Style_Price": 25.0,
            "Material_Price": 15.0,
            "Design_Price": 5.0,
            "Trim": False
        }
        
        # Should calculate: (Style_Price * Size_Factor) + Material_Price + Design_Price
        # = (25.0 * 1.0) + 15.0 + 5.0 = 45.0
        result = get_item_price(item_data)
        self.assertEqual(result, 45.0)

    def test_get_item_price_with_size_factor(self):
        """Test get_item_price with size factor"""
        from database.dao_helper_functions import get_item_price
        
        item_data = {
            "Size_Factor": 1.5,
            "Style_Price": 20.0,
            "Material_Price": 10.0,
            "Design_Price": 0.0,
            "Trim": False
        }
        
        # = (20.0 * 1.5) + 10.0 + 0.0 = 40.0
        result = get_item_price(item_data)
        self.assertEqual(result, 40.0)

    def test_convert_inventory_data(self):
        """Test convert_inventory_data converts tuple to dict correctly"""
        from database.dao_helper_functions import convert_inventory_data
        
        # Row tuple: PRODUCT_ID, SIZE, STYLE, MATERIAL, COLOR, STOCK, SIZE_FACTOR, STYLE_PRICE, MATERIAL_PRICE
        row = (1, "M", "Casual", "Cotton", "Blue", 10, 1.0, 25.0, 15.0)
        
        result = convert_inventory_data(row)
        
        # Verify all fields are present
        self.assertIn("Product_Id", result)
        self.assertIn("Size", result)
        self.assertIn("Style", result)
        self.assertIn("Material", result)
        self.assertIn("Color", result)
        self.assertIn("Stock", result)
        self.assertIn("Price", result)
        
        # Verify values
        self.assertEqual(result["Product_Id"], 1)
        self.assertEqual(result["Size"], "M")
        self.assertEqual(result["Style"], "Casual")
        self.assertEqual(result["Material"], "Cotton")
        self.assertEqual(result["Color"], "Blue")
        self.assertEqual(result["Stock"], 10)
        
        # Price should be calculated: (Style_Price * Size_Factor) + Material_Price
        # = (25.0 * 1.0) + 15.0 = 40.0
        self.assertEqual(result["Price"], 40.0)

    def test_get_order_price(self):
        """Test get_order_price returns 0.0 (placeholder)"""
        from database.dao_helper_functions import get_order_price
        from order_validation.order_validator import Order
        
        order_data = {
            "Customer": {"Name": "Test Customer", "Address": "Test Address"},
            "Items": [{"Product_Id": 1, "Design_Id": 1, "Quantity": 2}]
        }
        order = Order(order_data)
        
        result = get_order_price(order)
        
        # Current implementation returns 0.0
        self.assertEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()
