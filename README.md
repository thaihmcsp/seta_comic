# Config start app

### Create venv and source it
```
python -m venv .venv
source venv/bin/activate
```

### Install libs
```
pip install -r requirements.txt	
```

### Create postgres DB
Create postgres db and update it to .env using .env.example format

### Run migration
```
alembic upgrade head
```

### Update env
create .env file from .env.example template
add your config

### Run app
```
fastapi run app/main.py
```

# folder useage

### services folder:
  user for bussiness logic
### schemas folder:
  for DTOs validation & responses
### utils:
  for common logic
