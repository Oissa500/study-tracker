# Study Tracker
#### Video Demo: [https://www.youtube.com/watch?v=zkso9J7EOgg](https://www.youtube.com/watch?v=zkso9J7EOgg)
#### Description:

### Overview
**Study Tracker** is a Flask-based web application designed to help students stay organized, motivated, and consistent with their study habits. The app allows users to register, log in, and manage multiple courses, then track weekly study progress for each course. It was created as my **CS50 Final Project** to combine everything I learned in this course—from C and Python to SQL, HTML, CSS, and Flask—into one cohesive and interactive project.

The purpose of Study Tracker is simple: to make studying measurable and structured. Many students find it difficult to keep track of their progress across different subjects, especially during busy semesters. Study Tracker solves that by offering a simple, elegant platform to record weekly goals, notes, and progress percentages for each course—all in one organized dashboard.

---

### Key Features
1. **User Authentication** – Secure registration and login system using hashed passwords (via Werkzeug).
2. **Course Management** – Add, edit, and delete courses. Each course can have a semester name and personal notes.
3. **Weekly Progress Tracking** – Inside each course, users can add weeks with start and end dates, progress notes (like “Finished Chapter 7”), and completion percentages.
4. **Clean Dashboard** – Personalized greeting with user’s name and live statistics for total courses and weeks logged.
5. **Error Handling** – Custom apology pages to handle incorrect inputs or unauthorized access gracefully.
6. **Responsive and Modern Design** – A consistent, dark-themed UI with teal and blue highlights to create a calm, study-focused
atmosphere.
7. **Session Management** – Flask sessions keep users logged in securely without re-entering credentials each time.
8. **Full CRUD Functionality** – Users can Create, Read, Update, and Delete both courses and weeks easily through the web interface.
9. **Account Management** – Change Password page that verifies the current password, checks confirmation, and securely updates the hash.
10. **Welcome Page** – A simple welcome.html that greets users on first sign-in and guides them to create their first course.

---

### Technologies Used
- **Python (Flask)** – For backend routing, templating, and logic.
- **SQLite** – To store users, courses, and weekly progress in a relational database.
- **Jinja** – For rendering dynamic HTML templates.
- **HTML/CSS** – For layout, design, and user interface.
- **Werkzeug Security** – For password hashing and authentication.

---

### Database Design
The project uses three main tables connected by foreign keys:

#### 1. `users`
Stores information about each user.
- `id` (Primary Key)
- `first_name`, `last_name`, `username`, `hash`

#### 2. `courses`
Stores all user courses.
- `id` (Primary Key)
- `user_id` (Foreign Key referencing `users.id`)
- `course_name`, `semester`, `note`, `last_update`

#### 3. `weeks`
Stores weekly study progress for each course.
- `id` (Primary Key)
- `user_id` (Foreign Key referencing `users.id`)
- `course_id` (Foreign Key referencing `courses.id`)
- `week_number`, `begin_date`, `end_date`, `note`, `progress`, `last_update`

These relationships ensure that data is properly linked. When a user deletes a course, all related weeks are deleted automatically using the `ON DELETE CASCADE` relationship.

---

### File Structure
Here’s what each file in the project does:

/project
│
├── app.py                 # Main Flask app (routes, logic, sessions)
├── schema.sql             # Creates and initializes the database
├── helpers.py             # login_required, apology, other helpers
│
├── /templates
│   ├── layout.html        # Shared layout (navbar, flashes)
│   ├── index.html         # Home/dashboard (greeting + stats)
│   ├── welcome.html       # First-time landing page after login
│   ├── about.html         # About this project page
│   ├── login.html         # Login form
│   ├── register.html      # Registration page
│   ├── change_password.html # Change password form (old/new/confirm)
│   ├── courses.html       # Add/view/edit/delete courses
│   ├── edit_course.html   # Edit an existing course
│   ├── weeks.html         # Add/view/edit/delete weeks
│   ├── edit_week.html     # Edit a week’s information
│   └── apology.html       # Custom error display
│
├── /static
│   └── styles.css         # ~200 lines (refactored; was ~400)
│
└── study.db               # SQLite database file


---

### How It Works
1. **Register:** A new user provides first name, last name, username, and password (confirmed twice). The password is hashed before storing.
2. **Login:** The app checks the username and verifies the hash using `check_password_hash()`. If correct, the session begins.
3. **Courses:** Users can add new courses, each tagged with a semester and optional note. Courses can be edited or deleted at any time.
4. **Weeks:** Within each course, users can create up to sixteen weekly logs to track goals and progress.
5. **Edit/Delete:** Update or remove any week or course instantly using small “Edit” and “Delete” buttons beside each entry.
6. **Logout:** Clears the session and redirects back to the login page securely.

---

### Design and Interface
The entire website uses a single styles.css file that I wrote from scratch. The dark background with teal highlights gives the interface a calm and focused appearance. The CSS includes hover effects, responsive forms, shadows, and smooth transitions. After refining the layout, the stylesheet is now about 200 lines long (previously around 400), making it cleaner and more efficient while keeping the same overall design.

The navigation bar adapts automatically: when logged out, it shows “About,” “Home,” “Login,” and “Register”; when logged in, it shows “About,” “Home,” “Courses,” “Change Password,” and “Logout.” This small dynamic change makes navigation intuitive and seamless.

The Welcome page introduces users after their first login, guiding them to start by adding a new course. The Change Password page shares the same modern theme and allows users to securely update their credentials.

The About page includes a motivational quote and a small footer crediting CS50. I also added an outro image in the video that says “Thank you for watching — This is CS50.”

---

### Challenges and Problem Solving
One major challenge was getting **DELETE operations** to work correctly without breaking database integrity. I had to correctly link `user_id` and `course_id` as foreign keys and add a redirect after deletion to refresh the page view.

Another challenge was managing the CSS file — it grew to around 400 lines. I organized it into logical sections (navigation, tables, forms, and authentication) to stay readable. I also learned how to minimize repetition with consistent class naming.

Testing each feature was also an important step. I used Flask’s `debug` mode and manually tested every route and form submission multiple times to make sure all data was stored and displayed correctly.

---

### Future Improvements
If I expand this project, I plan to:
- Add **progress charts** using Chart.js to visualize weekly completion percentages.
- Implement **CSV export** to download data for records.
- Add **email reminders** or notifications for study deadlines.
- Include an optional **light mode** for accessibility.
- Improve performance by migrating from SQLite to PostgreSQL for larger data.

---

### Reflection
Creating Study Tracker was one of the most rewarding projects I’ve built. It helped me bring together the skills from every CS50 lecture — especially Flask from Week 9 and SQL from Week 7. I now understand how real websites store data and interact with users dynamically.

The project also taught me patience and debugging discipline. I spent hours fixing small details like form validation and UI alignment — skills I know will help me in future software development work.

Most importantly, CS50 taught me how to **think logically** and solve problems independently. Study Tracker represents not just an app, but the growth I experienced throughout this journey.

> “Small daily progress leads to big long-term success.”

---

**Developed with 💚 by Omar Issa**
*CS50 • Harvard University • 2025*

---

**Acknowledgment:**
Some design inspiration and debugging tips were discussed with ChatGPT as a learning tool, but the project logic, structure, and final implementation were fully written, tested, and verified by me.

