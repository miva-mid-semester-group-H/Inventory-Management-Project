from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


@app.route("/")
def home():
    return redirect("/signup")


@app.route("/signup", methods=["GET", "POST"])
def signup():
 
    error = None

    if request.method == "POST":

        # REQUIREMENT 3: Validating signup form data using request.form
        username = request.form["username"]
        email = request.form["email"]
        gender = request.form["gender"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            error = "Passwords do not match!"
        else:
            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                error = "An account with this email already exists!"
            else:
                # REQUIREMENT 5: Implementing password hashing for security before DB insertion
                hashed_password = generate_password_hash(password)

                cursor.execute(
    "INSERT INTO user (username, email, gender, password, created_at) VALUES (%s, %s, %s, %s, %s)",
    (username, email, gender, hashed_password, datetime.now())
)
                db.commit()
                cursor.close()
                db.close()
                return redirect("/dashboard")

            cursor.close()
            db.close()

    return render_template("signup.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()
        
        if not user or not check_password_hash(user["password"], password):
            error = "Invalid email or password!"
        else:
          session["user"] = user["email"]
        return redirect("/dashboard")


        error = "Invalid email or password!"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user WHERE email = %s", (session["user"],))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("index.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=False)