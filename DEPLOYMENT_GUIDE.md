# Seta Comic Deployment Guide

## Understanding Deployment Methods

This document explains the different deployment methods available for the Seta Comic application and clarifies when `setup.py` is used in the deployment process.

## Deployment Methods Overview

The Seta Comic application can be deployed using two main approaches:

1. **Manual Setup with setup.py**
2. **Docker Compose Deployment**

## 1. Manual Setup with setup.py

The `setup.py` script is a utility script designed to simplify the initial setup process. It performs the following functions:

- Checks if Docker and Docker Compose are installed
- Builds and starts the Docker containers using `docker-compose up -d --build`
- Waits for PostgreSQL to be ready
- Runs database migrations inside the app container
- Seeds the database with sample data inside the app container
- Provides a success message with instructions on how to access the application

### When to use setup.py:

- **Development environment setup**: When a developer wants to quickly set up the environment for the first time
- **Testing environment setup**: When setting up a fresh testing environment
- **Manual deployment**: When deploying to a server manually and want to automate the initial setup

### Command:
```
python setup.py
```

## 2. Docker Compose Deployment

This approach uses Docker Compose to manage the application containers directly, without using the `setup.py` script. In this method:

- The `docker-compose.yml` file defines the services (PostgreSQL and app)
- The `Dockerfile` builds the application container
- The `entrypoint.sh` script runs automatically when the app container starts

The `entrypoint.sh` script performs similar functions to `setup.py`:
- Waits for PostgreSQL to be ready
- Runs database migrations
- Seeds the database
- Starts the FastAPI application

### When to use Docker Compose directly:

- **Production deployment**: When deploying to a production environment
- **CI/CD pipelines**: When integrating with automated deployment systems
- **Container orchestration**: When using Kubernetes, Docker Swarm, or other orchestration tools

### Command:
```
docker-compose up -d --build
```

## Key Differences

| Feature | setup.py | Docker Compose with entrypoint.sh |
|---------|----------|-----------------------------------|
| Execution | Manual | Automatic on container start |
| Application start | Separate step after setup | Included in container startup |
| Use case | Development, initial setup | Production, automated deployment |
| Container management | Creates containers | Creates and manages containers |

## Recommended Approach for Different Scenarios

1. **Local Development**:
   - Use `setup.py` for initial setup
   - Use `uvicorn app.main:app --reload` for development with hot reloading

2. **Testing**:
   - Use `setup.py` for a controlled setup process
   - Or use `docker-compose up` for a more production-like environment

3. **Production Deployment**:
   - Use `docker-compose up -d --build` for direct deployment
   - The `entrypoint.sh` script will handle database setup and application startup

## Conclusion

When the app is deployed in a production environment, `setup.py` is typically **not used**. Instead, the deployment process relies on Docker Compose and the `entrypoint.sh` script to automatically set up the database and start the application.

The `setup.py` script is primarily a development and manual setup tool, while the `entrypoint.sh` script is the production deployment tool that runs automatically when the container starts.