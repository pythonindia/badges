# Setting up dev environment

You can setup a virtual environment with your choice of tooling, preferably `virtualenv`. The python version preferred is 3.8.

Once the virtualenv is activated, run `make init-dev` to install all the application and development dependencies.

# Database setup and Sample data

The project uses `postgresql`. Please ensure that you have access to a running Postgres server. If you are running postgres locally (highly recommended), you can just run `make initdb` and then `make insert-sample-data`.

# Running the server

You can run the server using `make dev`. This will run a server with DEBUG=True.

# Contributing

The base branch is `main` and all pull requests have to be filed to that branch.

Please create a fork of the project, make your changes on the fork and file puull requests whenever needed.

Before you commit your code, please run `make lint`. The project uses `black` for highly opinionated linting.

## TODO

- Improve the above documentation before release
- Write more verbose database setup
- Introduce additional lint tooling like `isort`
- Mention the test steps
