# Overview

This is the foundation of a student registration system utilizine a SQL database. The program proviedes a menu for the user to interact with the database. There are eight options for the user:
* 1 - Display Students
* 2 - Display Classes
* 3 - Enroll in the School/University
* 4 - Enroll a student in a class
* 5 - Drop a class
* 6 - Show the Student roster for a specific class
* 7 - Show the Student's schedule
* 8 - Edit Student info

[Software Demo Video](https://youtu.be/hAfjIzPfir8)

# Relational Database

The SQL database has four tables: Students, Courses, Sections, and Student Schedules. \
The Course to Sections tables have a one to many relationship same goes for the Student to Student Schedules relationship.

# Development Environment

The program was written in Python using SQLite. Because Python has the SQLite library already integrated, this project required no extra imports.

# Useful Websites

* [StackOverflow](https://stackoverflow.com/)
* [SQLite Tutorial](https://www.sqlitetutorial.net/)
* [Python SQLite3](https://docs.python.org/3.8/library/sqlite3.html)

# Future Work

* More info will be added to each table as well as more tables. I am hoping, once the entire structure of the "University" is desgined, to collect data on each course and the concepts taught in each. With this information, students will be able to register for classes that share similar concepts, thus reducing the need for students to relearn concepts in the future and reinforcing those concepts at the same time.
* I will need to implement admin privileges or lock data so that if a student accesses the database, they will not be able to see other student info or modify data not relevant to them.
* I need to correct the functions so that the user actually uses the primary key of the tables instead of just the row number. For now the program works but if a Student ID, Section ID, Course ID, or Student Schedule ID is different from the row ID, then the display is confusing for the user.