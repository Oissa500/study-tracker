from cs50 import SQL
from flask import Flask, render_template, request, redirect, render_template, session, flash, g
from flask_session import Session
from helpers import login_required, apology
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)

if not os.path.exists("study.db"):
    open("study.db", "w").close()

db = SQL(os.getenv("DATABASE_URL", "sqlite:///study.db"))

with open("schema.sql") as f:
    sql_script = f.read()

for statement in sql_script.split(";"):
    if statement.strip():
        try:
            db.execute(statement)
        except:
            pass
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.before_request
def load_logged_in_user():
    """Runs before every request and stores user info globally."""
    user_id = session.get("user_id")
    if user_id is not None:
        row = db.execute("SELECT id, first_name, last_name FROM users WHERE id = ?", user_id)
        g.user = row[0] if row else None
    else:
        g.user = None


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # Handle POST
    first = request.form.get("first_name")
    last = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirmation")

    if not username or not password or not confirm or not first or not last:
        flash("Please fill in all fields. ")
        return redirect("/register")

    if password != confirm:
        flash("Password do not match")
        return redirect("/register")
    existing = db.execute("SELECT id FROM users WHERE username = ?", username)
    if existing:
        flash("Username already exists")
        return redirect("/register")

    hash_pw = generate_password_hash(password)
    db.execute("INSERT INTO users(username, hash, first_name, last_name) VALUES (?, ?, ?, ?)",
               username, hash_pw, first, last)
    flash("Registered Successfully")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return apology("must provide username and password", 403)

    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        flash("Invalid username or password")
        return redirect("/login")

    session["user_id"] = rows[0]["id"]
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect("/login")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    user_id = session["user_id"]

    if request.method == "POST":
        old_pw = request.form.get("old_password")
        new_pw = request.form.get("new_password")
        confirm_pw = request.form.get("confirm_password")

        #Ensure all field were filled
        if not old_pw or not new_pw or not confirm_pw:
            return apology("All field required", 400)

        #Get currect hash from db
        row = db.execute("SELECT hash FROM users WHERE id = ?", user_id)[0]

        #check old password
        if not check_password_hash(row["hash"], old_pw):
            return apology("Old password is incorrect", 400)

        if new_pw != confirm_pw:
            return apology("Passwords do not match", 400)

        new_hash = generate_password_hash(new_pw)
        db.execute("UPDATE users SET hash = ?  WHERE id = ?", new_hash, user_id)

        flash("Password changed successfully.", "success")
        return redirect("/")

    return render_template("change_password.html")


@app.route("/")
def index():
    if "user_id" in session:
        user_id = session["user_id"]
        user = db.execute("SELECT first_name FROM users WHERE id = ?", user_id)[0]

        # Count total courses and weeks for this user
        total_courses = db.execute(
            "SELECT COUNT(*) AS count FROM courses WHERE user_id = ?", user_id)[0]["count"]
        total_weeks = db.execute(
            "SELECT COUNT(*) AS count FROM weeks WHERE user_id = ?", user_id)[0]["count"]

        return render_template("index.html", user=user, total_courses=total_courses, total_weeks=total_weeks)
    else:
        return render_template("welcome.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses():
    if g.user is None:
        flash("You must be logged in to view courses.")
        return redirect("/login")

    user_id = g.user["id"]

    # If the page is opened normally
    if request.method == "GET":
        rows = db.execute(
            "SELECT id, course_name, COALESCE(note, '') AS note, COALESCE(semester,'') AS semester, "
            "COALESCE(last_update, '') AS last_update "
            "FROM courses WHERE user_id = ? ORDER BY course_name",
            user_id
        )
        return render_template("courses.html", courses=rows)

    elif request.method == "POST":
        name = (request.form.get("course_name") or "").strip()
        note = (request.form.get("note") or "").strip()
        semester = (request.form.get("semester") or "").strip()

        if not name:
            flash("Please enter a course name.")
            return redirect("/courses")

        exists = db.execute(
            "SELECT id FROM courses WHERE user_id = ? AND course_name = ? AND (semester = ? OR ? = '')", user_id, name, semester, semester)
        if exists:
            flash("Course already exists for this semester.")
            return redirect("/courses")

        db.execute(
            "INSERT INTO courses(user_id, course_name, note, semester, last_update) VALUES (?, ?, ?, ?, datetime('now'))", user_id, name, note, semester)
        flash("Course added successfully")
        return redirect("/courses")


@app.route("/edit_course/<int:id>", methods=["GET", "POST"])
@login_required
def edit_course(id):
    if request.method == "POST":
        course_name = request.form.get("course")
        semester = request.form.get("semester")
        note = request.form.get("note")

        db.execute("UPDATE courses SET course_name = ?, semester = ?, note = ?, last_update = datetime('now') WHERE id = ?",
                   course_name, semester, note, id)
        flash("Course updated successfully", "success")
        return redirect("/courses")

    # FOR GET REQUEST:
    course = db.execute("SELECT * FROM courses WHERE id = ?", id)[0]
    return render_template("edit_course.html", course=course)


@app.route("/course/<int:course_id>", methods=["GET", "POST"])
@login_required
def course_detail(course_id):
    user_id = session["user_id"]

    # making sure the course belong to this year
    course = db.execute("SELECT * FROM courses WHERE id = ? AND user_id = ?", course_id, user_id)
    if not course:
        return apology("Course not found or unauthorized", 403)
    course = course[0]

    # hasle adding a new week
    if request.method == "POST":
        week_number = request.form.get("week_number")
        begin_date = request.form.get("begin_date")
        end_date = request.form.get("end_date")
        note = request.form.get("note")
        progress = request.form.get("progress")

        if not week_number:
            flash("Week number is required", "danger")
            return redirect(f"/course/{course_id}")
        db.execute("INSERT INTO weeks (user_id, course_id, week_number, begin_date, end_date, note, progress, last_update) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))",
                   user_id, course_id, week_number, begin_date, end_date, note, progress)

        flash("Week added successfully.", "success")
        return redirect(f"/course/{course_id}")

    # Display all weeks for this course
    weeks = db.execute(
        "SELECT * FROM weeks WHERE course_id = ? AND user_id = ? ORDER BY week_number", course_id, user_id)
    return render_template("weeks.html", course=course, weeks=weeks)


@app.route("/delete_course/<int:id>", methods=["POST"])
@login_required
def delete_course(id):
    user_id = session["user_id"]
    db.execute("DELETE FROM weeks WHERE course_id = ? AND user_id = ?", id, user_id)
    db.execute("DELETE FROM courses WHERE id = ? AND user_id = ?", id, user_id)
    flash("Course and related weeks deleted.", "info")
    return redirect("/courses")


@app.route("/edit_week/<int:week_id>", methods=["GET", "POST"])
@login_required
def edit_week(week_id):
    user_id = session["user_id"]

    # fetch the week entry:
    week = db.execute("SELECT * FROM weeks WHERE id = ? AND user_id = ?", week_id, user_id)
    if not week:
        return apology("Week not found or unauthorized", 404)
    week = week[0]

    if request.method == "POST":
        begin_date = request.form.get("begin_date")
        end_date = request.form.get("end_date")
        note = request.form.get("note")
        progress = request.form.get("progress")

        db.execute("UPDATE weeks SET begin_date = ?, end_date = ?, note = ?, progress = ?, last_update = datetime('now') WHERE id = ? AND user_id = ?",
                   begin_date, end_date, note, progress, week_id, user_id)
        flash("Week updated successfully!", "success")
        return redirect(f"/course/{week['course_id']}")

    # GET request

    return render_template("edit_week.html", week=week)


@app.route("/delete_week/<int:week_id>", methods=["POST"])
@login_required
def delete_week(week_id):
    user_id = session["user_id"]

    # Find which course this week belongs to
    row = db.execute("SELECT course_id FROM weeks WHERE id = ? AND user_id = ?", week_id, user_id)
    if not row:
        return apology("Week not found or unauthorized", 404)

    course_id = row[0]["course_id"]

    # Delete the week
    db.execute("DELETE FROM weeks WHERE id = ? AND user_id = ?", week_id, user_id)

    # Flash and redirect to refresh the page
    flash("Week deleted successfully!", "info")
    return redirect(f"/course/{course_id}")
