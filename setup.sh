# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Initialize the database
flask db upgrade

# Command to run the application
exec gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app