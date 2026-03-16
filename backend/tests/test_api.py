"""
Test suite for Flask API routes in api.py

Tests the /inventory and /designs endpoints by mocking the database layer.
This allows testing without requiring a live DB2 connection.
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock

# Add the src directory to the path so we can import modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock ibm_db modules BEFORE any imports that use them
sys.modules['ibm_db'] = Mock()
sys.modules['ibm_db_dbi'] = Mock()

# Import and configure the mock database
from database import db as db_module  # pylint: disable=wrong-import-position

class TestGetInventory(unittest.TestCase):
    """Test cases for GET /inventory endpoint"""

    def setUp(self):
        """Set up test client with mocked database"""
        # Mock the database methods
        db_module.select_inventory = Mock()
        db_module.select_designs = Mock()
        
        # Import the app (must be after mocking to ensure mocks are in place)
        from api import app  # pylint: disable=import-error,import-outside-toplevel
        self.app = app
        self.client = app.test_client()
        
    def tearDown(self):
        """Clean up mocks"""
        db_module.select_inventory.reset_mock()
        db_module.select_designs.reset_mock()

    def test_inventory_no_filters(self):
        """Test GET /inventory with no filter headers returns all inventory"""
        # Mock the database response
        db_module.select_inventory.return_value = [
            ("S", "Casual", "Cotton", "Blue", 19.99),
            ("M", "Formal", "Silk", "Red", 49.99)
        ]
        
        response = self.client.get("/inventory")
        
        # Verify the database was called
        db_module.select_inventory.assert_called_once()
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

    def test_inventory_with_size_filter(self):
        """Test GET /inventory with Size header filters correctly"""
        db_module.select_inventory.return_value = [
            ("M", "Casual", "Cotton", "Blue", 19.99)
        ]
        
        response = self.client.get("/inventory", headers={"Size": "M"})
        
        # Verify the database was called with the header
        db_module.select_inventory.assert_called_once()
        call_args = db_module.select_inventory.call_args[0][0]
        self.assertIn("Size", call_args)
        self.assertEqual(call_args["Size"], "M")
        
        self.assertEqual(response.status_code, 200)

    def test_inventory_with_color_filter(self):
        """Test GET /inventory with Color header filters correctly"""
        db_module.select_inventory.return_value = [
            ("S", "Casual", "Cotton", "Red", 19.99)
        ]
        
        response = self.client.get("/inventory", headers={"Color": "Red"})
        
        call_args = db_module.select_inventory.call_args[0][0]
        self.assertIn("Color", call_args)
        self.assertEqual(call_args["Color"], "Red")
        
        self.assertEqual(response.status_code, 200)

    def test_inventory_with_style_filter(self):
        """Test GET /inventory with Style header filters correctly"""
        db_module.select_inventory.return_value = [
            ("M", "Formal", "Silk", "Blue", 49.99)
        ]
        
        response = self.client.get("/inventory", headers={"Style": "Formal"})
        
        call_args = db_module.select_inventory.call_args[0][0]
        self.assertIn("Style", call_args)
        self.assertEqual(call_args["Style"], "Formal")
        
        self.assertEqual(response.status_code, 200)

    def test_inventory_with_material_filter(self):
        """Test GET /inventory with Material header filters correctly"""
        db_module.select_inventory.return_value = [
            ("L", "Casual", "Cotton", "Green", 24.99)
        ]
        
        response = self.client.get("/inventory", headers={"Material": "Cotton"})
        
        call_args = db_module.select_inventory.call_args[0][0]
        self.assertIn("Material", call_args)
        self.assertEqual(call_args["Material"], "Cotton")
        
        self.assertEqual(response.status_code, 200)

    def test_inventory_with_multiple_filters(self):
        """Test GET /inventory with multiple filter headers"""
        db_module.select_inventory.return_value = [
            ("M", "Casual", "Cotton", "Blue", 19.99)
        ]
        
        response = self.client.get("/inventory", headers={
            "Size": "M",
            "Style": "Casual",
            "Material": "Cotton",
            "Color": "Blue"
        })
        
        call_args = db_module.select_inventory.call_args[0][0]
        self.assertIn("Size", call_args)
        self.assertIn("Style", call_args)
        self.assertIn("Material", call_args)
        self.assertIn("Color", call_args)
        
        self.assertEqual(response.status_code, 200)

    def test_inventory_ascending_order(self):
        """Test GET /inventory with Ascending: true returns ascending order"""
        db_module.select_inventory.return_value = [
            ("S", "Casual", "Cotton", "Blue", 19.99),
            ("M", "Formal", "Silk", "Red", 49.99)
        ]
        
        response = self.client.get("/inventory", headers={"Ascending": "true"})
        
        call_args = db_module.select_inventory.call_args[0][0]
        self.assertIn("Ascending", call_args)
        self.assertEqual(call_args["Ascending"], "true")
        
        self.assertEqual(response.status_code, 200)

    def test_inventory_descending_order(self):
        """Test GET /inventory with Ascending: false returns descending order"""
        db_module.select_inventory.return_value = [
            ("M", "Formal", "Silk", "Red", 49.99),
            ("S", "Casual", "Cotton", "Blue", 19.99)
        ]
        
        response = self.client.get("/inventory", headers={"Ascending": "false"})
        
        call_args = db_module.select_inventory.call_args[0][0]
        self.assertIn("Ascending", call_args)
        self.assertEqual(call_args["Ascending"], "false")
        
        self.assertEqual(response.status_code, 200)

    def test_inventory_database_error(self):
        """Test GET /inventory handles database exceptions gracefully"""
        # Mock the database to raise an exception
        db_module.select_inventory.side_effect = Exception("Database connection failed")
        
        # Flask catches the exception and returns a 500 error
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 500)


class TestGetDesigns(unittest.TestCase):
    """Test cases for GET /designs endpoint"""

    def setUp(self):
        """Set up test client with mocked database"""
        # Mock the database methods
        db_module.select_inventory = Mock()
        db_module.select_designs = Mock()
        
        from api import app  # pylint: disable=import-error,import-outside-toplevel
        self.app = app
        self.client = app.test_client()
        
    def tearDown(self):
        """Clean up mocks"""
        db_module.select_inventory.reset_mock()
        db_module.select_designs.reset_mock()

    def test_designs_no_filters(self):
        """Test GET /designs with no filter headers returns all designs"""
        db_module.select_designs.return_value = [
            ("Design1", 29.99, "Description1"),
            ("Design2", 39.99, "Description2")
        ]
        
        response = self.client.get("/designs")
        
        db_module.select_designs.assert_called_once()
        self.assertEqual(response.status_code, 200)

    def test_designs_with_min_price(self):
        """Test GET /designs with Min_Price header filters correctly"""
        db_module.select_designs.return_value = [
            ("Design2", 39.99, "Description2")
        ]
        
        response = self.client.get("/designs", headers={"Min_Price": "30"})
        
        call_args = db_module.select_designs.call_args[0][0]
        # HTTP converts underscores to hyphens in headers
        self.assertIn("Min-Price", call_args)
        self.assertEqual(call_args["Min-Price"], "30")
        
        self.assertEqual(response.status_code, 200)

    def test_designs_with_max_price(self):
        """Test GET /designs with Max_Price header filters correctly"""
        db_module.select_designs.return_value = [
            ("Design1", 29.99, "Description1")
        ]
        
        response = self.client.get("/designs", headers={"Max_Price": "35"})
        
        call_args = db_module.select_designs.call_args[0][0]
        # HTTP converts underscores to hyphens in headers
        self.assertIn("Max-Price", call_args)
        self.assertEqual(call_args["Max-Price"], "35")
        
        self.assertEqual(response.status_code, 200)

    def test_designs_with_price_range(self):
        """Test GET /designs with both Min_Price and Max_Price"""
        db_module.select_designs.return_value = [
            ("Design2", 34.99, "Description2")
        ]
        
        response = self.client.get("/designs", headers={
            "Min_Price": "30",
            "Max_Price": "40"
        })
        
        call_args = db_module.select_designs.call_args[0][0]
        # HTTP converts underscores to hyphens in headers
        self.assertIn("Min-Price", call_args)
        self.assertIn("Max-Price", call_args)
        
        self.assertEqual(response.status_code, 200)

    def test_designs_with_name_filter(self):
        """Test GET /designs with Name header filters correctly"""
        db_module.select_designs.return_value = [
            ("Floral Design", 29.99, "Description1")
        ]
        
        response = self.client.get("/designs", headers={"Name": "Floral"})
        
        call_args = db_module.select_designs.call_args[0][0]
        self.assertIn("Name", call_args)
        self.assertEqual(call_args["Name"], "Floral")
        
        self.assertEqual(response.status_code, 200)

    def test_designs_sort_by_price(self):
        """Test GET /designs with Sort_By_Price: true"""
        db_module.select_designs.return_value = [
            ("Design1", 29.99, "Description1"),
            ("Design2", 39.99, "Description2")
        ]
        
        response = self.client.get("/designs", headers={"Sort_By_Price": "true"})
        
        call_args = db_module.select_designs.call_args[0][0]
        # HTTP converts underscores to hyphens in headers
        self.assertIn("Sort-By-Price", call_args)
        self.assertEqual(call_args["Sort-By-Price"], "true")
        
        self.assertEqual(response.status_code, 200)

    def test_designs_sort_by_name(self):
        """Test GET /designs with Sort_By_Price: false (defaults to name sort)"""
        db_module.select_designs.return_value = [
            ("Design1", 39.99, "Description2"),
            ("Design2", 29.99, "Description1")
        ]
        
        response = self.client.get("/designs", headers={"Sort_By_Price": "false"})
        
        call_args = db_module.select_designs.call_args[0][0]
        # HTTP converts underscores to hyphens in headers
        self.assertIn("Sort-By-Price", call_args)
        
        self.assertEqual(response.status_code, 200)

    def test_designs_ascending_order(self):
        """Test GET /designs with Ascending: true"""
        db_module.select_designs.return_value = [
            ("Design1", 29.99, "Description1"),
            ("Design2", 39.99, "Description2")
        ]
        
        response = self.client.get("/designs", headers={"Ascending": "true"})
        
        call_args = db_module.select_designs.call_args[0][0]
        self.assertIn("Ascending", call_args)
        self.assertEqual(call_args["Ascending"], "true")
        
        self.assertEqual(response.status_code, 200)

    def test_designs_descending_order(self):
        """Test GET /designs with Ascending: false"""
        db_module.select_designs.return_value = [
            ("Design2", 39.99, "Description2"),
            ("Design1", 29.99, "Description1")
        ]
        
        response = self.client.get("/designs", headers={"Ascending": "false"})
        
        call_args = db_module.select_designs.call_args[0][0]
        self.assertIn("Ascending", call_args)
        
        self.assertEqual(response.status_code, 200)

    def test_designs_complex_filter(self):
        """Test GET /designs with multiple filters combined"""
        db_module.select_designs.return_value = [
            ("Floral Design", 34.99, "Beautiful floral pattern")
        ]
        
        response = self.client.get("/designs", headers={
            "Name": "Floral",
            "Min_Price": "30",
            "Max_Price": "40",
            "Sort_By_Price": "true",
            "Ascending": "true"
        })
        
        call_args = db_module.select_designs.call_args[0][0]
        # HTTP converts underscores to hyphens in headers
        self.assertIn("Name", call_args)
        self.assertIn("Min-Price", call_args)
        self.assertIn("Max-Price", call_args)
        self.assertIn("Sort-By-Price", call_args)
        self.assertIn("Ascending", call_args)
        
        self.assertEqual(response.status_code, 200)

    def test_designs_database_error(self):
        """Test GET /designs handles database exceptions gracefully"""
        db_module.select_designs.side_effect = Exception("Database connection failed")
        
        # Flask catches the exception and returns a 500 error
        response = self.client.get("/designs")
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
