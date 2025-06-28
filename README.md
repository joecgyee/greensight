# Greensight

Django app with DRF for global renewable energy usage data.

## Prerequisites

This project is developed with:

- **Operating System**: Windows 11  
- **Python Version**: 3.13.2  
- **Django Version**: 4.2.23  
- **Package Managers**: pip & virtualenv
- **Database**: SQLite3  

## Installation

```bash
# Clone the repo
git clone https://github.com/joecgyee/greensight.git
cd greensight

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Go to project root directory
cd energyinsight

# Populate the database from CSV
python scripts/populate_greensight.py

# Run the development server
python manage.py runserver
```

## Running Tests

```bash
# Run all tests
python manage.py test

# Running specific test classes or methods
python manage.py test usage_data.tests.APITests
python manage.py test usage_data.tests.APITests.test_usage_data_list_api
```
