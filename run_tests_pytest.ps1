# Run Tests with Coverage using pytest
# This script runs all tests and generates coverage reports

Write-Host "Running tests with pytest coverage..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m pytest backend/tests --cov=backend/src --cov-report=term --cov-report=html -v

Write-Host "`n`nHTML coverage report generated at: htmlcov\index.html" -ForegroundColor Green
Write-Host "Open with: Start-Process htmlcov\index.html" -ForegroundColor Yellow
