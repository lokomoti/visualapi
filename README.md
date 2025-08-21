<<<<<<< HEAD
### Generating JWT

In the container, cd to visualapi/src and run this command:

`uv run cli.py jwt generate --sub youruser --exp 120`

The --sub parameter is required. In the example the --exp is expiration in minutes.
=======
# Visual API Wrapper

This project is a RESTful API built on top of the Infor Visual ERP database. It serves as a middleware layer that standardizes and simplifies access to Visual ERP data for integration with external systems or frontend applications.

## Features

- Read-only access to key Visual ERP data
- Standardized, structured JSON responses
- Designed for integration into modern applications or reporting tools
- Abstracts away the complexity of the Visual ERP schema

## Tech Stack

- Python (FastAPI)
- SQLAlchemy / SQLModel
- Microsoft SQL Server (Visual ERP backend)

## Intended Use

This API is intended to be deployed internally to expose essential Visual ERP data in a clean, REST-compliant format without direct exposure to the database structure.
>>>>>>> be4b10c84eba62f43a8a71d4818c62759f2c2cae
