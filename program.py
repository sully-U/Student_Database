import sqlite3

# Connect to the database
connection = sqlite3.connect('records.db')
cursor = connection.cursor()
#_______________________________________________________________________________________________________________________________
# Create tables (if it does not already exist)
cursor.execute("CREATE TABLE IF NOT EXISTS students \
                (student_id INTEGER PRIMARY KEY, \
                name VARCHAR(45))")
cursor.execute("CREATE TABLE IF NOT EXISTS courses \
              (course_id INTEGER PRIMARY KEY, \
              name VARCHAR(45))")
cursor.execute("CREATE TABLE IF NOT EXISTS sections \
                (section_id INTEGER PRIMARY KEY, \
                course_id INTEGER, \
                meet_days TEXT, \
                meet_time VARCHAR(8), \
                CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses(course_id))"
               )
cursor.execute("CREATE TABLE IF NOT EXISTS student_schedules \
                (student_id INTEGER, section_id INTEGER, \
                FOREIGN KEY (student_id) REFERENCES students(student_id),\
                FOREIGN KEY (section_id) REFERENCES sections(section_id))") 
#_______________________________________________________________________________________________________________________________

# INSERT DATA into tables
students = (("1","Sully"), ("2","Sara"),("3","Bilbo"),("4","Thor"),("5", "Dumbledore"), ("6", "Darth Vader"))
for data in students:
  cursor.execute("INSERT INTO students VALUES (?,?)", data)

classes = (("1","Programming 101"),("2","English101"),("3","Biology"),("4","History"),("5","Calculus"))
for data in classes:
  cursor.execute("INSERT INTO courses VALUES (?,?)", data)

sections = (("1","1","MWF","11:00"),("2","1","TR","13:00"),("3","2","MWF","11:00"),("4","2","TR","10:00"),("5","3","MWF","9:00"),("6","3","TR","15:00"),("7","4","MWF","11:00"),("8","4","TR","13:00"),("9","5","MWF","10:00"),("10","5","TR","14:00"))
for data in sections:
  cursor.execute("INSERT INTO sections VALUES (?,?,?,?)", data)


schedules = (("1","1"),("1","2"),("2","2"),("3","1"),("4","3"),("5","1"), ("5","5"),("4","4"),("3","3"))
for data in schedules:
  cursor.execute("INSERT INTO student_schedules VALUES (?,?)", data)
#_______________________________________________________________________________________________________________________________
def get_name(cursor):
    cursor.execute("SELECT name FROM students")
    results = cursor.fetchall()
    print("_______STUDENT INFO_______")
    if len(results) == 0:
        print("No names in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]} - {results[i][1]}")
    print("")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Name: "))
    print("")
    return results[choice - 1][0]


def get_id(cursor):
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    print("_______STUDENT INFO_______")
    if len(results) == 0:
        print("No ID in database")
        return None
    for i in range(len(results)):
        print(f"{i+1}| Student_ID:{results[i][0]} - {results[i][1]}")
    print("")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Student_ID: "))
    print("")
    return results[choice - 1][0]


def get_course(cursor):
    cursor.execute("SELECT name FROM courses")
    results = cursor.fetchall()
    print("_______COURSE INFO_______")
    if len(results) == 0:
        print("No course in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]}")
    print("")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Course_ID: "))
    print("")
    return results[choice - 1][0]


def get_section(cursor):
    cursor.execute(
        "SELECT s.section_id, c.name, s.meet_days, s.meet_time FROM sections s JOIN courses c on s.course_id = c.course_id"
    )
    results = cursor.fetchall()
    print("_______SECTION INFO_______")
    if len(results) == 0:
        print("No sections in database")
        return None
    for i in range(len(results)):
        print(f"{i+1}| {results[i][1]}: {results[i][2]} {results[i][3]}")
    print("")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Section_ID: "))
    print("")
    return results[choice - 1][0]
#_______________________________________________________________________________________________________________________________

# Print menu for user 
choice = None
while choice != "9":
    print("1) Display Students")
    print("2) Display Classes")
    print("3) Enroll New Student in University")
    print("4) Enroll Student in Class")
    print("5) Drop Class")
    print("6) Show Class Roster")
    print("7) Show Student Schedule")
    print("8) Edit Student Info")
    print("9) Quit")
    choice = input("> ")
    print()

    
    if choice == "1":
        # Display Students
        cursor.execute("SELECT * FROM students")
        print("___________Students____________")
        print("{:>10}  {:>10}".format("Student_ID", "Name"))
        for record in cursor.fetchall():
            print("{:>1}  {:>20}".format(record[0], record[1]))
   
    elif choice == "2":
        # Display Classes
        cursor.execute("SELECT * FROM courses")
        print("_________Courses_________")
        print("{:>10}  {:>20}".format("Course_ID", "Course_Name"))
        for record in cursor.fetchall():
            print("{:>1}  {:>30}".format(record[0], record[1]))

    elif choice == "3":
        # Enroll Student in University
        try:
            sid = int(input("Student_ID: "))
            name = input("Name: ")
            enrollStudent = (sid, name)
            cursor.execute("INSERT INTO students VALUES(?,?)", enrollStudent)
            print("Student enrolled!")
            connection.commit()
        except ValueError:
            print("Not valid input!")

    elif choice == "4":
        # Enroll Student in Class
        sid = get_id(cursor)
        if sid == None:
          continue
        section = get_section(cursor)
        if section == None:
            continue
        cursor.execute("INSERT INTO student_schedules VALUES(?,?)", (sid, section))
        print("Student enrolled in class!")
        if cursor.rowcount == 0:
            print("Section does not exist")
        
        connection.commit()

    elif choice == "5":
        # Drop Class
        sid = get_id(cursor)
        student_id = (sid, )
        cursor.execute("SELECT s.section_id, c.name, s.meet_days, s.meet_time \
                        FROM student_schedules ss \
                            JOIN sections s ON ss.section_id = s.section_id \
                                JOIN courses c ON s.course_id = c.course_id \
                                    WHERE ss.student_id = ?", student_id)
        print("_____________Student Schedule______________")
        print("{:>1}  {:>15} {:>15} {:>15}".format("Section_ID", "Course_Name", "Meet_days", "Meet_time"))
        for record in cursor.fetchall():
            print("{:>1}  {:>25} {:>10} {:>10}".format(record[0], record[1], record[2], record[3]))
        section = int(input("Section_ID: "))
        cursor.execute("DELETE from student_schedules \
                        WHERE student_id = ? AND section_id = ?", (sid, section))
        connection.commit()

    elif choice == "6":
        # Display Class Roster
        sid = get_section(cursor)
        section_id = (sid, )
        cursor.execute(
            "SELECT s.student_id, s.name \
                FROM students s \
                    JOIN student_schedules ss ON s.student_id = ss.student_id \
                        JOIN sections sec ON ss.section_id = sec.section_id \
                            WHERE sec.section_id = ?", section_id)
        print("_____________Class Roster______________")
        print("{:>10}  {:>20}".format("Student_ID", "Name"))
        for record in cursor.fetchall():
            print("{:>1}  {:>30}".format(record[0], record[1]))
        connection.commit()

    elif choice == "7":
        # Display Student Schedule
        sid = get_id(cursor)
        student_id = (sid, )
        cursor.execute("SELECT c.name, s.meet_days, s.meet_time \
                        FROM student_schedules ss \
                            JOIN sections s ON ss.section_id = s.section_id \
                                JOIN courses c ON s.course_id = c.course_id \
                                    WHERE ss.student_id = ?", student_id)
        print("_____________Student Schedule______________")
        print("{:>1}  {:>15} {:>10}".format("Course_Name", "Meet_days", "Meet_time"))
        for record in cursor.fetchall():
            print("{:>1}  {:>8} {:>10}".format(record[0], record[1], record[2]))
        connection.commit()

    elif choice == "8":
        # Update Student Info
        try:
            sid = get_id(cursor)
            new_name = input("Updated Name: ") 
            cursor.execute("UPDATE students SET name = ? WHERE student_id = ?", (new_name, sid))
            connection.commit()
            if cursor.rowcount == 0:
                print("Invalid name!")
        except ValueError:
            print("Invalid!")
    print()

# Close the database connection before exiting
connection.close()