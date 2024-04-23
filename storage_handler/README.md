## storage_handler folder

Disclamer:
This is README file is only to setup the storage_handler environment.
Any tools used here have more commands/options/configurations than showed here.
For deeper understanig, please refer to the appropriate documentation.

1. Python
Install python 3.12.2
Create a virtual environment and activate it.
In the virtual environment, from the storage_handler folder, run: "pip install -r requirements.txt"

2. Activating the storage_handler:
In the virtual environment, from the root folder, run: "python -m storage_handler.app.server"

4. testing:
Activate the storage_handler.
To run the tests: In the virtual environment, from the root folder, run: "python -m unittest -v storage_handler.tests.test_grpc".
