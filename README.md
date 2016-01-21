# Piiipod
staff and event management, with Google calendar sync

## Features



## Installation

> These instructions assume the mySQL server has been started. See MySQL below.

### Dependencies

Check that Python3 and MySQL are installed using `make check`.

### Getting Started

1. Run the installation using `make install`.
1. Add valid mysql user credentials to `config.cfg`.
1. Create the database using `make db`.

> If the bash scripts do not work, see the Details section below for an outline
of what each script does.

During development, you may additionally want to remember the following:

- In the future, use `source activate.sh` to activate the virtual environment.
- Any model modifications, in the **development** environment, should be
followed by `make refresh`, which will **delete** the old database and replace
it with a new one.

### Unix and Mac OSX Details

In case the installation script fails, you may execute the contents of the
installation bash script line by line:

1. Setup a new virtual environment: `python3 -m virtualenv env`.
1. Start the virtual environment: `source env/bin/activate`.
1. Install all requirements: `pip install -r requirements.txt`.
1. Make a new configuration file: `cp default-config.cfg config.cfg`.
1. Add valid MySQL user credentials to `queue.cfg`.
1. Create the database: `python3 run.py -db create'`.

Any model modifications should be followed by the following, which will
**delete** the old database and replace it with a new one: `python3 run.py -db refresh`

### Windows Details

Because of incompatbility issues with the makefile, on Windows you will have to manually run the installation instructions.

1. Setup a new virtual environment by calling `python -m virtualenv env`.
1. Start the virtual environment by calling `env/Scripts/activate.bat` in cmd.
1. Install all requirements `pip install -r requirements.txt`.
1. Make a new configuration file: `cp default-config.cfg config.cfg`.
1. Add valid MySQL user credentials to `config.cfg`.
1. Start the MySQL service using services.msc
1. Create the database by using `mysql -u root -p`, then entering `create database queue;` in the interactive prompt.
1. Setup the database using `python3 run.py -db create`.

## Launch

Use `make run`.

> If the bash script does not work, see the Details section below for an outline
of `make run`.

### Unix and Mac OSX Details

1. Start the virtual environment: `source env/bin/activate`.
1. Launch server: `python3 run.py`.

### Windows Details

1. Start the virtual environment by calling `env/Scripts/activate.bat` in cmd.
1. Launch server: `python run.py`.

## MySQL

- For Mac OSX installations of MySQL, via Brew, start the server using
`mysql.server start`. For other Linux-based operating systems, use
`sudo service mysql start`.
- For Windows, just start the server using `services.msc`.
