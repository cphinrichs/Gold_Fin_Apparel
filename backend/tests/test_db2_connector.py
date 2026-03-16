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
from unittest.mock import MagicMock, Mock

# Add the src directory to the path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock the ibm_db modules before any imports
sys.modules['ibm_db'] = Mock()
sys.modules['ibm_db_dbi'] = Mock()

# Now we can import the DAO
from database.db2_connector import _Db2DAO  # pylint: disable=wrong-import-position


class TestSelectInventory(unittest.TestCase):
    """Test cases for _Db2DAO.select_inventory() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        # Create a mock DAO instance
        cls.mock_cursor = MagicMock()
        cls.mock_cursor.fetchall.return_value = [("Test", "Data", "Here", "Blue", 99.99)]
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [("Test", "Data", "Here", "Blue", 99.99)]
        # Make execute succeed by default (returns None, doesn't raise)
        self.mock_cursor.execute.return_value = None
        self.mock_cursor.execute.side_effect = None  # Clear any side_effect that was set

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao.select_inventory = _Db2DAO.select_inventory.__get__(dao, _Db2DAO)
        return dao

    def test_select_inventory_no_filters(self):
        """Test select_inventory with no filters generates basic query"""
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_inventory({})
        
        # Verify cursor.execute was called
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        # Check SQL structure
        self.assertIn("SELECT * FROM", sql)
        self.assertIn("Inventory", sql)
        self.assertIn("ORDER BY Price", sql)
        self.assertIn("DESC", sql)  # Default descending
        self.assertEqual(len(params), 0)  # No parameters
        
        # Check result
        self.assertEqual(len(result), 1)

    def test_select_inventory_with_size(self):
        """Test select_inventory with Size filter"""
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_inventory({"Size": "M"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("WHERE Size = ?", sql)
        self.assertEqual(params[0], "M")
        self.assertEqual(len(result), 1)

    def test_select_inventory_with_multiple_filters(self):
        """Test select_inventory with multiple filters uses AND"""
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

    def test_select_inventory_ascending_order(self):
        """Test select_inventory with Ascending: true"""
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_inventory({"Ascending": "true"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        
        self.assertIn("ORDER BY Price", sql)
        self.assertIn("ASC", sql)

    def test_select_inventory_exception_handling(self):
        """Test select_inventory handles exceptions and re-raises"""
        dao = self.create_dao_with_mock_cursor()
        self.mock_cursor.execute.side_effect = Exception("Database error")
        
        with self.assertRaises(Exception) as context:
            dao.select_inventory({})
        
        self.assertIn("Database error", str(context.exception))


class TestSelectDesigns(unittest.TestCase):
    """Test cases for _Db2DAO.select_designs() method"""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests"""
        cls.mock_cursor = MagicMock()
        cls.mock_cursor.fetchall.return_value = [("Design1", 29.99, "Description")]
        
    def setUp(self):
        """Reset mocks before each test"""
        self.mock_cursor.reset_mock()
        self.mock_cursor.fetchall.return_value = [("Design1", 29.99, "Description")]
        # Make execute succeed by default (returns None, doesn't raise)
        self.mock_cursor.execute.return_value = None
        self.mock_cursor.execute.side_effect = None  # Clear any side_effect that was set

    def create_dao_with_mock_cursor(self):
        """Helper to create DAO with mocked cursor"""
        dao = MagicMock(spec=_Db2DAO)
        dao.cursor = self.mock_cursor
        dao.creds = {"db_name": "TEST_DB"}
        dao.select_designs = _Db2DAO.select_designs.__get__(dao, _Db2DAO)
        return dao

    def test_select_designs_no_filters(self):
        """Test select_designs with no filters generates basic query"""
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("SELECT * FROM", sql)
        self.assertIn("Design", sql)
        self.assertIn("ORDER BY Name", sql)  # Default sort by name
        self.assertIn("DESC", sql)  # Default descending
        self.assertEqual(len(params), 0)
        
        self.assertEqual(len(result), 1)

    def test_select_designs_with_min_price(self):
        """Test select_designs with Min_Price only"""
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({"Min_Price": "30"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("WHERE Price >= ?", sql)
        self.assertEqual(params[0], "30")

    def test_select_designs_with_price_range(self):
        """Test select_designs with both Min_Price and Max_Price"""
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({
            "Min_Price": "30",
            "Max_Price": "40"
        })
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        params = call_args[1]
        
        self.assertIn("WHERE Price BETWEEN ? AND ?", sql)
        self.assertEqual(params[0], "30")
        self.assertEqual(params[1], "40")
        self.assertEqual(len(params), 2)

    def test_select_designs_sort_by_price(self):
        """Test select_designs with Sort_By_Price: true"""
        dao = self.create_dao_with_mock_cursor()
        
        result = dao.select_designs({"Sort_By_Price": "true"})
        
        call_args = self.mock_cursor.execute.call_args[0]
        sql = call_args[0]
        
        self.assertIn("ORDER BY Price", sql)

    def test_select_designs_exception_handling(self):
        """Test select_designs handles exceptions and re-raises"""
        dao = self.create_dao_with_mock_cursor()
        self.mock_cursor.execute.side_effect = Exception("Database connection failed")
        
        with self.assertRaises(Exception) as context:
            dao.select_designs({})
        
        self.assertIn("Database connection failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
