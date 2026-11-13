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
# Sample social media posts
posts = [
    {
        "id": 1,
        "title": "Introduction to Python",
        "category": "Programming",
        "content": "Learn Python programming from the basics."
    },
    {
        "id": 2,
        "title": "Artificial Intelligence",
        "category": "Artificial Intelligence",
        "content": "Discover how AI is changing our world."
    },
    {
        "id": 3,
        "title": "Cricket Highlights",
        "category": "Sports",
        "content": "Explore exciting cricket news and match highlights."
    },
    {
        "id": 4,
        "title": "Latest Movie Reviews",
        "category": "Movies & Entertainment",
        "content": "Read reviews of popular movies."
    },
    {
        "id": 5,
        "title": "Machine Learning Basics",
        "category": "Artificial Intelligence",
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
        "category": "Health & Fitness",
        "content": "Explore simple ways to stay healthy."
    },
    {
        "id": 10,
        "title": "Exploring Artificial Intelligence",
        "category": "Artificial Intelligence",
        "content": "Discover how AI is transforming everyday life."
    },
    {
        "id": 11,
        "title": "Cybersecurity Awareness",
        "category": "Technology",
        "content": "Learn simple ways to protect your digital information."
    },
    {
        "id": 12,
        "title": "Python Programming Projects",
        "category": "Programming",
        "content": "Explore beginner-friendly Python projects."
    },
    {
        "id": 13,
        "title": "Future of Robotics",
        "category": "Science",
        "content": "Discover how robots are transforming industries."
    },
    {
        "id": 14,
        "title": "Space Exploration",
        "category": "Science",
        "content": "Explore planets, galaxies and space missions."
    },
    {
        "id": 15,
        "title": "Football World Updates",
        "category": "Sports",
        "content": "Catch up on football matches and tournaments."
    },
    {
        "id": 16,
        "title": "Olympic Games",
        "category": "Sports",
        "content": "Discover inspiring Olympic sports stories."
    },
    {
        "id": 17,
        "title": "Best Educational Websites",
        "category": "Education",
        "content": "Find useful websites for learning new skills."
    },
    {
        "id": 18,
        "title": "Online Learning Tips",
        "category": "Education",
        "content": "Improve your learning experience with online resources."
    },
    {
        "id": 19,
        "title": "Fitness at Home",
        "category": "Health & Fitness",
        "content": "Try simple exercises and home workouts."
    },
    {
        "id": 20,
        "title": "Mental Wellness",
        "category": "Health & Fitness",
        "content": "Learn about stress management and healthy habits."
    },
    {
        "id": 21,
        "title": "Popular Music Trends",
        "category": "Music",
        "content": "Explore popular songs and music trends."
    },
    {
        "id": 22,
        "title": "Learn About Musical Instruments",
        "category": "Music",
        "content": "Discover different musical instruments and sounds."
    },
    {
        "id": 23,
        "title": "Beautiful Places to Visit",
        "category": "Travel",
        "content": "Explore amazing destinations around the world."
    },
    {
        "id": 24,
        "title": "Travel Photography",
        "category": "Travel",
        "content": "Learn how to capture memorable travel moments."
    },
    {
        "id": 25,
        "title": "Healthy Indian Food",
        "category": "Food",
        "content": "Discover delicious and nutritious Indian meals."
    },
    {
        "id": 26,
        "title": "Easy Cooking Recipes",
        "category": "Food",
        "content": "Try simple recipes that you can prepare at home."
    },
    {
        "id": 27,
        "title": "Today's Technology News",
        "category": "News",
        "content": "Stay informed about technology developments."
    },
    {
        "id": 28,
        "title": "Science Discoveries",
        "category": "News",
        "content": "Read about interesting scientific discoveries."
    },
    {
        "id": 29,
        "title": "Movies Coming Soon",
        "category": "Movies & Entertainment",
        "content": "Explore upcoming movies and entertainment releases."
    },
    {
        "id": 30,
        "title": "Latest Smartphone Innovations",
        "category": "Technology",
        "content": "Discover new smartphone features and innovations."
    }
]
# Store user interests and likes temporarily
user_interests = {}
user_likes = {}
user_bookmarks = {}

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
        # Explain why the post is recommended
	        # Explain why the post is recommended
        reasons = []

        if post["category"] in interests:
            reasons.append(
                f"Matches your selected interest: {post['category']}"
            )

        if post["category"] in liked_categories:
            reasons.append(
                f"You previously liked posts in {post['category']}"
            )

        if not reasons:
            reasons.append("Discover something new!")

        recommended_posts.append({
            **post,
            "score": score,
            "reason": " & ".join(reasons)
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

    categories = [
    "Technology",
    "Artificial Intelligence",
    "Programming",
    "Education",
    "Science",
    "Sports",
    "Movies & Entertainment",
    "Music",
    "Travel",
    "Health & Fitness",
    "Food",
    "News"
]

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

@app.route("/bookmark/<int:post_id>", methods=["POST"])
def bookmark_post(post_id):
    if "email" not in session:
        return redirect(url_for("login"))

    if not any(post["id"] == post_id for post in posts):
        return "Post not found", 404

    email = session["email"]

    if email not in user_bookmarks:
        user_bookmarks[email] = []

    if post_id not in user_bookmarks[email]:
        user_bookmarks[email].append(post_id)

    return redirect(url_for("dashboard"))


@app.route("/remove_bookmark/<int:post_id>", methods=["POST"])
def remove_bookmark(post_id):
    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]

    if email in user_bookmarks and post_id in user_bookmarks[email]:
        user_bookmarks[email].remove(post_id)

    return redirect(url_for("bookmarks"))


@app.route("/bookmarks")
def bookmarks():
    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]

    saved_ids = user_bookmarks.get(email, [])

    saved_posts = [
        post for post in posts
        if post["id"] in saved_ids
    ]

    return render_template(
        "bookmarks.html",
        name=session["name"],
        posts=saved_posts
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
