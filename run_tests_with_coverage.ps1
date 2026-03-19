# Run Tests with Coverage
# This script runs all tests and generates coverage reports

# Run tests with coverage
Write-Host "Running tests with coverage..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m coverage run -m unittest discover -s backend/tests -p "test_*.py" -v

# Generate text report
Write-Host "`n`nCoverage Report:" -ForegroundColor Green
.\venv\Scripts\python.exe -m coverage report

# Generate HTML report
Write-Host "`nGenerating HTML coverage report..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m coverage html
Write-Host "HTML report generated at: htmlcov\index.html" -ForegroundColor Green

# Generate XML report for VS Code Coverage Gutters
Write-Host "`nGenerating XML coverage report for VS Code..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m coverage xml
Write-Host "XML report generated: coverage.xml" -ForegroundColor Green

Write-Host "`nTo view HTML report, run: Start-Process htmlcov\index.html" -ForegroundColor Yellow
Write-Host "To view in VS Code: Open Coverage Gutters (Ctrl+Shift+8 or click 'Watch' in status bar)" -ForegroundColor Yellow
