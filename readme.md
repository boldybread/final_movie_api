# Movie_API README

<!-- To run from local machine (postgresql):

Create a new postgresql user and give permissions
Create a postgresql database (blog_api)
Edit ".env" file so "SQL_DATABASE_URI" matches user and database details
Start python virtual invironment (python3 -m venv venv)
Activate virtual environment (source venv/bin/activate)
Install requirements (pip install -r requirements.txt)
Create and seed tables (flask db drop && flask db create && flask db seed)
Run flask app (flask run) -->

## Identification of the problem you are trying to solve by building this particular app.

I wanted to create an app that could store movies to a watchlist for a user to watch as well as post their ratings of those movies. I like using watchlists on the streaming services I subscribe to, but would like to have a watchlist that wasn't restricted to the one platform, and could not only store the movies that I wanted to watch, but also tell me what platform they are available to be viewed.

## Why is it a problem that needs solving?

While many streaming services have a watchlist for their particular app I wanted to make one that wasn't limited to just one streaming service but one where a user could add movies from any app to their watchlist and then rate them accordingly after watching them.

## Why have you chosen this database system. What are the drawbacks compared to others?



## Identify and discuss the key functionalities and benefits of an ORM

Object relational mapping or ORM is a technique used to bridge relational databases and object orientated programs. When using object orientated programming (OOP) languages to interact with a database you will perfrom different operations like creating, reading, updating and deleting (CRUD) data from a database.

Benefits of using an ORM include simplified access to a database which is intuitive and easier to understand. Developers are able to interact with the database using objects and methods rather that writing raw SQL queries. ORM frameworks can also automatically create tables again reducing the SQL code required. This structured approach makes the database easy to maintain.

The ability to map database tables and their relationsips to object classes and their relationships makes it easier to focus on the domain model rather than the database schema. Due to the level of abstraction between database and application when using ORM frameworks it is easier to switch to different databases or use multiple databases simultaneously without having to change application code.

## Document all endpoints for your API



## An ERD for your app



## Detail any third party services that your app will use

### SQLAlchemy

SQLAlchemy is a Python SQL toolkit and object relational mapper to enable developers extra flexibility when creating an application without the need to rely on writing lots of raw SQL code. It is designed for efficient and high performing database access.

### Marshmallow

Marshmallow is an ORM framework library built for converting more complex datatypes such as objects to and from native Python datatypes.

### Bcrypt

Bcrypt is a password hashing function designed to allow developers the quick and easy ability to quickly hash a password for their software and servers.

### JWTManager

JWTManager is an object used to hold JSON Web Token (JWT) settings and callback functions for Flask. It offers basic JWT features to the developers application.

### Flask

Flask is a Python web micro framework that provides tools, libraries, and technologies for building web applications offering a simple yet powerful API that allows developers to  quickly and effienctly create web applications. Flask is used to build the API for this application.

### Psycopg2

Psycopg2 is a popular PostgreSQL adapter for Python providing a user friendly interface for developers to interact with PostgreSQL databases. Psycopg2 is used to connect to the PostgreSQL database for this application.

## Describe your projects models in terms of the relationships they have with each other

### User Model

User model represents a user in the system. User model has a direct relationship with watchlist and rating models and takes information from those models. If user instance is deleted it will delete the corresponding rating and watchlist information.

```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

### Watchlist Model



```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

### Rating Model



```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

### Movie Model



```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

## Discuss the database relations to be implemented in your application



## Describe the way tasks are allocated and tracked in your project

I utilised Trello for project management where I created 4 lists.

![Trello Project Overview](images\api_project.jpg "Trello Project Overview")

### Project Resources

Here I created a project plan as well as label definitions to help me understand my labelling convention at a glance.

![Trello Project Overview](images\api_project_labels.jpg "Trello Project Overview")

### To do

All tasks to be completed began in the to do list, this allowed me to have an oversight of my current and upcoming workload so I was better able to manage my time and plan what I would work on next and where my prioirities and time constraints were.

![Trello Project Overview](images\api_project_readme_task.jpg "Trello Project Overview")

### Pending

Once tasks were started they were moved to the pending list. Here I could manage exactly what was in progress and look more specifically at the sub tasks involved with completing that particular overall task. I used a checklist to tick off individual sub tasks. Once all sub tasks were ticked off and I was satisfied that the task was complete it was moved from pending to the Done list.

### Done

This list was utilised for any tasks deemed completed. By the end of the project all tasks were in here signifying completion of the project.