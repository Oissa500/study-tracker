DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS goals;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

CREATE TABLE courses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_name TEXT NOT NULL,
    note TEXT,
    semester TEXT,
    last_update TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE weeks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    begin_date TEXT,
    end_date TEXT,
    note TEXT,
    progress TEXT,
    last_update TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
);

CREATE TABLE goals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    week_id INTEGER,
    goal_text TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
    FOREIGN KEY(course_id) REFERENCES courses(id)
    FOREIGN KEY(week_id) REFERENCES weeks(id)
);
