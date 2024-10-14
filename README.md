# MMC - Crop Type

MMC-Crop Type API hub hosts all apis related to crop types.


# Start the application

```bash
# Make you have python 3.12+ installed
# create virtual envirionment
python3 -m venv .env

# activat the envirionment
source .env/bin/activate

# install dependencies
pip install -r requirements.txt

# make sure you have the .env
cp code/.env.sample code/.env

# run dev code
cd code
uvicorn main:app --port 8000 --reload

# Make sure settings are added .env
# Running alembic migrations
cd code
alembic upgrade heads
```

# API endpoint functions
```bash
# Check docs/API spec.md file
```