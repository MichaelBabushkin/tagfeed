## Server folder

Disclamer:
This is README file is only to setup the server environment.
Any tools used here have more commands/options/configurations than showed here.
For deeper understanig, please refer to the appropriate documentation.

1. PostgreSQL:
Install PostgreSQL 13.x
Create a PostgreSQL DB for running the server
If you also want to test the server, create another PostgreSQL DB.
If you don't know how to install posgresql and how to create a DB,
here is a nice source that explains about PostgreSQL:
https://www.youtube.com/watch?v=qw--VYLpxG4 watch the relevant parts using the video description

2. Python
Install python 3.12.2
Create a virtual environment and activate it.
In the virtual environment, from the server folder, run: "pip install -r requirements.txt"
If you plan to run a test environment, also run: "pip install -r requirements.test.txt"

3. Credentials:
Create a ".env.private" file in the server folder.
The following is an example of a .env.private file:

**start of example file**

DATABASE_PASSWORD=1234

DATABASE_USERNAME=postgres

SECRET_KEY=secret

**end of example file**

The DATABASE values should match the DB you created.

For testing you'll need another file named .env.test.private with the same content only for the test db
It's safer to avoid from defining permanent environment variables on an machine that runs/connects to more than one environment

4. Creatig tables in the db:
In the virtual environment, from the root folder, run: "alembic -c server/alembic.ini upgrade head"

5. Activating the server:
In the virtual environment, from the root folder, run: "uvicorn server.app.main:app"

6. server API documentation:
When the server is active, go to "https://localhost:8000/docs"

7. testing:
To run the tests, run: "python -m pytest". to add verbosity an disable capture run: "python -m pytest -v -s"
