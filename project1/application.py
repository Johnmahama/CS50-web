import os

from flask import Flask, session, render_template, request
from flask_session import Session
from flask_login import LoginManager, UserMixin

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_form")
def login_form():
    return render_template("login_form.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Get username and password from database
    dbcredentials = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    dbusername = dbcredentials[0]
    dbpassword = dbcredentials[1]

    if username == "" or password == "":
        return render_template("error.html", message="Username or password empty")

    if db.execute("SELECT username FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        return render_template("error.html", message="User doesn't exist")

    if dbpassword == password:
        return render_template("login.html")
    else:
        return render_template("error.html", message="Wrong password")

@app.route("/register_form")
def register_form():
    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    # :user, {"user": username}
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
        return render_template("error.html", message="Username already exists")
    
    # Checks if field is empty
    if username == "":
        return render_template("error.html", message="No username given")
    if password == "":
        return render_template("error.html", message="No password given")
    
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": username, "password": password})

    db.commit()
    return render_template("register.html")

@app.route("/users")
def users():
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("users.html", users=users)

@app.route("/front")
def front():
    user = request.form.get("username")
    return render_template("front.html", user=user)
