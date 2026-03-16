# Backend Test Suite

This directory contains comprehensive tests for the Gold_Fin_Apparel backend API.

## Test Files

### `test_api.py` - API Route Tests
Tests the Flask API endpoints (`/inventory` and `/designs`) by mocking the database layer.

**Test Coverage:**
- 10 tests for `/inventory` endpoint
- 12 tests for `/designs` endpoint
- Tests include: no filters, single filters, multiple filters, sorting (ASC/DESC), error handling

### `test_db2_connector.py` - Database DAO Tests
Tests the database access object (DAO) SQL query building logic by mocking `ibm_db` and `ibm_db_dbi`.

**Test Coverage:**
- 10 tests for `select_inventory()` method
- 12 tests for `select_designs()` method
- Tests include: SQL generation, parameter binding, WHERE clauses, ORDER BY, exception handling

## Running the Tests

### Run All Tests
```powershell
python -m unittest discover -s backend/tests -p "test_*.py" -v

# OR using pytest (works with VS Code test extension)
pytest backend/tests -v
```

### Run Tests with Coverage
```powershell
# Using pytest (recommended - works with VS Code)
pytest backend/tests --cov=backend/src --cov-report=term --cov-report=html -v

# OR using unittest with coverage
python -m coverage run -m unittest discover -s backend/tests -p "test_*.py" -v
python -m coverage report
python -m coverage html

# Convenient scripts:
.\run_tests_pytest.ps1        # pytest with coverage
.\run_tests_with_coverage.ps1 # unittest with coverage
```

**Current Coverage: 86%**
- `api.py`: 90%
- `db2_connector.py`: 85%
- `logger_object.py`: 86%

### Run Specific Test File
```powershell
# API tests only
python -m unittest backend.tests.test_api -v

# DAO tests only
python -m unittest backend.tests.test_db2_connector -v
```

### Run a Specific Test Class
```powershell
python -m unittest backend.tests.test_api.TestGetInventory -v
python -m unittest backend.tests.test_api.TestGetDesigns -v
python -m unittest backend.tests.test_db2_connector.TestSelectInventory -v
python -m unittest backend.tests.test_db2_connector.TestSelectDesigns -v
```

### Run a Specific Test Method
```powershell
python -m unittest backend.tests.test_api.TestGetInventory.test_inventory_no_filters -v
```

## Test Strategy

### Mocking Strategy
All tests use `unittest.mock` to mock external dependencies:
- **API tests** mock the `database.db` object to avoid real database connections
- **DAO tests** mock `ibm_db`, `ibm_db_dbi`, and file I/O to test SQL logic in isolation

### Why Mock?
1. **No database required** - Tests run without DB2 connection
2. **Fast execution** - Tests complete in seconds
3. **Predictable results** - No dependency on database state
4. **CI/CD friendly** - Can run in any environment

## Test Coverage Summary

| Endpoint/Method | Test Cases | Coverage |
|----------------|------------|----------|
| `GET /inventory` | 10 | Filters (Size, Style, Material, Color), sorting, multiple filters, errors |
| `GET /designs` | 12 | Price filters (min/max/range), name filter, sorting, multiple filters, errors |
| `select_inventory()` | 10 | SQL generation, WHERE clauses, AND conditions, ORDER BY, exception handling |
| `select_designs()` | 12 | SQL generation, BETWEEN, LIKE, ORDER BY, complex queries, exception handling |
| **TOTAL** | **44 tests** | Comprehensive coverage of GET endpoints |

## Expected Output

When all tests pass, you should see:
```
Ran 44 tests in X.XXXs

OK
```

## Common Issues

### Import Errors
If you see "Unable to import 'api'" or similar:
- Make sure you're running tests from the project root directory
- The test files automatically add `backend/src` to the Python path

### Mock Setup Issues
If tests fail with database connection errors:
- The mocks may not be set up correctly
- Check that you're using the test files as-is without modifications

## Future Enhancements

Potential additions to the test suite:
1. Integration tests with a test database
2. Tests for `POST /order` endpoint (currently not implemented)
3. Performance/load testing
4. API response format validation
5. Test coverage reporting with `coverage.py`
