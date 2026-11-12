import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Use an environment variable for the production secret key.
# This fallback is only for local development.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "local-development-only-change-this"
)

# Store the database in the project directory.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "users.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()
# Sample social media posts
posts = [
    {
        "id": 1,
        "title": "Introduction to Python",
        "category": "Technology",
        "content": "Learn Python programming from the basics."
    },
    {
        "id": 2,
        "title": "Artificial Intelligence",
        "category": "AI",
        "content": "Discover how AI is changing our world."
    },
    {
        "id": 3,
        "title": "Cricket Highlights",
        "category": "Sports",
        "content": "Explore the latest cricket news."
    },
    {
        "id": 4,
        "title": "Latest Movie Reviews",
        "category": "Movies",
        "content": "Read reviews of popular movies."
    },
    {
        "id": 5,
        "title": "Machine Learning Basics",
        "category": "AI",
        "content": "Understand how machines learn from data."
    },
    {
        "id": 6,
        "title": "Web Development",
        "category": "Technology",
        "content": "Learn to build modern websites."
    },
    {
        "id": 7,
        "title": "Latest Technology Trends",
        "category": "Technology",
        "content": "Discover the latest technology trends."
    },
    {
        "id": 8,
        "title": "Study Tips for Students",
        "category": "Education",
        "content": "Learn effective study techniques."
    },
    {
        "id": 9,
        "title": "Healthy Lifestyle Tips",
        "category": "Health",
        "content": "Explore simple ways to stay healthy."
    },
    {
        "id": 10,
        "title": "Exploring Artificial Intelligence",
        "category": "Technology",
        "content": "Discover how AI is transforming everyday life."
    },
    {
        "id": 11,
        "title": "Cybersecurity Awareness",
        "category": "Technology",
        "content": "Learn simple ways to protect your digital information."
    }


]

# Store user interests and likes temporarily
user_interests = {}
user_likes = {}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            message = "Please fill in all fields."
        else:
            conn = get_db_connection()
            try:
                conn.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password))
                )
                conn.commit()
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                message = "This email is already registered."
            finally:
                conn.close()

    return render_template("register.html", message=message)




@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db_connection()
        try:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()
        finally:
            conn.close()

        if user and check_password_hash(user["password"], password):
            session["email"] = user["email"]
            session["name"] = user["name"]
            return redirect(url_for("dashboard"))

        message = "Invalid email or password."

    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]

    interests = user_interests.get(email, [])
    liked_posts = user_likes.get(email, [])

    recommended_posts = []

    # Find categories of posts the user has liked
    liked_categories = {
        post["category"]
        for post in posts
        if post["id"] in liked_posts
    }

    for post in posts:
        score = 0

        # Give 2 points for matching selected interests
        if post["category"] in interests:
            score += 2

        # Give 3 points for matching previously liked categories
        if post["category"] in liked_categories:
            score += 3

        # Identify why the post is recommended
        reasons = []

        if post["category"] in interests:
            reasons.append("Based on your selected interests")

        if post["category"] in liked_categories:
            reasons.append("Based on posts you liked")

        recommended_posts.append({
            **post,
            "score": score,
            "reason": " & ".join(reasons) if reasons else "Suggested for you"
        })

    # Show the highest-scoring posts first
    recommended_posts.sort(
        key=lambda post: post["score"],
        reverse=True
    )
    return render_template(
        "dashboard.html",
        name=session["name"],
        posts=recommended_posts,
        interests=interests
    )
@app.route("/interests", methods=["GET", "POST"])
def interests():
    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]

    if request.method == "POST":
        selected = request.form.getlist("interests")
        user_interests[email] = selected

        return redirect(url_for("dashboard"))

    categories = ["Technology", "AI", "Sports", "Movies"]

    return render_template(
        "interests.html",
        categories=categories,
        selected=user_interests.get(email, [])
    )
@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    if "email" not in session:
        return redirect(url_for("login"))

    if not any(post["id"] == post_id for post in posts):
        return "Post not found", 404

    email = session["email"]

    if email not in user_likes:
        user_likes[email] = []

    if post_id not in user_likes[email]:
        user_likes[email].append(post_id)

    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
