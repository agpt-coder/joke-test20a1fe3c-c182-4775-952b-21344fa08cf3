---
date: 2024-04-15T10:59:38.731178
author: AutoGPT <info@agpt.co>
---

# joke-test

To create a joke API with a single endpoint that returns one joke, leveraging the given tech stack, the steps are as follows: 

1. **Programming Language**: Use Python for its simplicity and extensive libraries.
2. **API Framework**: Implement FastAPI for the API development. FastAPI is chosen for its high performance and ease of use for building APIs with Python.
3. **Database**: Store the jokes in PostgreSQL. Although a simple API returning one joke might initially not require a database, using PostgreSQL allows for scalability, such as adding more jokes or functionalities in the future.
4. **ORM (Object-Relational Mapping)**: Utilize Prisma with Python to interact with the PostgreSQL database. Prisma facilitates developing and querying the database schema more efficiently and securely.

**API Development Steps**:
- Initialize a new FastAPI project.
- Set up Prisma with PostgreSQL to define the model for a joke. This model will include fields such as `id` and `content`.
- Create a database migration to generate the jokes table, then populate it with a selection of jokes.
- Implement an endpoint in FastAPI (e.g., `/joke`) that queries the PostgreSQL database via Prisma to randomly select and return one joke from the table.
- Ensure proper testing and validation of the endpoint to return jokes correctly. Optionally, add rate limiting to manage request load.
- Deploy the API to a cloud provider or a local server, depending on the use case and audience.

**Additional Consideration**:
- For enhancement, you could implement additional endpoints to add, update, or delete jokes, turning the API into a more interactive platform.

This outline provides a comprehensive approach to developing a joke API with the specified tech stack, focusing on a scalable and efficient deployment.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'joke-test'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
