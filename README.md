# Octobot - The Group Expense Tracker

![](assets/logo-with-name.png)

Octobot is an all-in-one application that allows you to track expenses and split them with your friends and family.

Try it now at [octobot.cgsphoto.com](https://octobot.cgsphoto.com)!

## Features

- Add evenly split expenses and divide them throughout group members
- Add expenses with custom splits - without having to do the math!
- Generate rich reports to calculate how much each member owes or is owed

## Contributing

If you would like to contribute to the project, please follow the below steps to set up your development environment.

### Prerequisites

In order to run the application, you will need the following installed on your machine:

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/en/download/)
- [SQLite 3.36+](https://www.sqlite.org/download.html)

### Project Structure

The project is split into two main parts: the frontend and the backend. The frontend is written in React and Ionic, and the backend is written in Python with Flask. The frontend is located in the `client` directory, and the backend is located in the `server` directory.

### Setting up the Backend

To setup the backend, first navigate to the `server` directory. Then, create a virtual environment and activate it. You can do this by running the following commands:

```bash
python3 -m venv .env
source .env/bin/activate
```

Next, install the required Python packages by running:

```bash
pip install -r requirements.txt
```

#### Setting up the Database

The application uses a SQLite database to store all of its data. To set up the database, run the following inside of the `server` directory:

```bash
sqlite3 database.db
```

Then, run the following commands to create the tables:

```sql
.read create_table.sql
```

Then, you can exit the database by running:

```sql
.quit
```

### Setting up the Frontend

To setup the frontend, first navigate to the `client` directory. Then, install the required Node packages by running:

```bash
npm install -g @ionic/cli
npm install -g firebase-tools
npm install
```

### Running the Application

To run the backend, first open a terminal and navigate to the `server` directory. Then, activate the virtual environment and run the following command:

```bash
source .env/bin/activate
python main.py
```

The server should now be running on `http://localhost:5000`.

To run the frontend, first open a terminal and navigate to the `client` directory. Then, run the following command:

```bash
npm run start
```

The application will open a new tab in your browser at `http://localhost:3000`.
