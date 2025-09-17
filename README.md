# Seta Comic Application

## Setup Options

You can set up this application in two ways:

### Option 1: Using Docker (Recommended)

This option uses PostgreSQL in Docker and automatically seeds the database with sample data.

#### Prerequisites
- Docker
- Docker Compose

#### Setup Steps
1. Clone the repository
2. Run the setup script:
   ```
   python setup.py
   ```
   This will:
   - Start PostgreSQL in Docker
   - Run database migrations
   - Seed the database with sample data (10 records for each table)

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

4. To stop the PostgreSQL container:
   ```
   docker-compose down
   ```

### Option 2: Manual Setup

#### Create venv and source it
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Install libs
```
pip install -r requirements.txt	
```

#### Create postgres DB
Create postgres db and update it to .env using .env.example format

#### Run migration
```
alembic upgrade head
```

#### Update env
create .env file from .env.example template
add your config

#### Run app
```
uvicorn app.main:app --reload
```

# folder useage

### services folder:
  user for bussiness logic
### schemas folder:
  for DTOs validation & responses
### utils:
  for common logic
