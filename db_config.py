import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'student_exchange.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def close_connection(conn):
    try:
        if conn:
            conn.close()
    except:
        pass

def init_database():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode = WAL")

    c.execute('''CREATE TABLE IF NOT EXISTS Users (
        User_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        Role TEXT NOT NULL CHECK (Role IN ('student','coordinator','university')),
        Ref_Id INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS University (
        Uni_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Uni_Name TEXT NOT NULL,
        Country TEXT NOT NULL,
        Address TEXT,
        Username TEXT UNIQUE,
        Password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Coordinator (
        Coordinator_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Coordinator_Name TEXT NOT NULL,
        Email TEXT UNIQUE,
        Phone TEXT,
        Uni_Id INTEGER NOT NULL,
        Username TEXT UNIQUE,
        Password TEXT,
        FOREIGN KEY (Uni_Id) REFERENCES University(Uni_Id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Exchange_Program (
        Program_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Semester TEXT NOT NULL,
        Duration INTEGER NOT NULL,
        Field_Of_Study TEXT,
        Max_Students INTEGER NOT NULL CHECK (Max_Students > 0),
        Uni_Id INTEGER NOT NULL,
        Coordinator_Id INTEGER,
        FOREIGN KEY (Uni_Id) REFERENCES University(Uni_Id),
        FOREIGN KEY (Coordinator_Id) REFERENCES Coordinator(Coordinator_Id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Student (
        Student_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Student_Name TEXT NOT NULL,
        Department TEXT,
        CGPA REAL CHECK (CGPA BETWEEN 0.0 AND 4.0),
        Email TEXT UNIQUE,
        Phone TEXT,
        Username TEXT UNIQUE,
        Password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Application (
        Application_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Application_Date DATE DEFAULT (DATE('now')),
        Status TEXT DEFAULT 'Pending' CHECK (Status IN ('Pending','Approved','Rejected')),
        Student_Id INTEGER NOT NULL,
        Program_Id INTEGER NOT NULL,
        Coordinator_Id INTEGER,
        FOREIGN KEY (Student_Id) REFERENCES Student(Student_Id),
        FOREIGN KEY (Program_Id) REFERENCES Exchange_Program(Program_Id),
        FOREIGN KEY (Coordinator_Id) REFERENCES Coordinator(Coordinator_Id)
    )''')

    existing = c.execute("SELECT COUNT(*) FROM University").fetchone()[0]
    if existing == 0:
        c.execute("INSERT INTO University (Uni_Name, Country, Address, Username, Password) VALUES ('American International University-Bangladesh', 'Bangladesh', 'Kuratoli, Dhaka', 'aiub_uni', 'aiub123')")
        c.execute("INSERT INTO University (Uni_Name, Country, Address, Username, Password) VALUES ('University of France', 'France', 'France Road, France', 'france_uni', 'france123')")
        c.execute("INSERT INTO University (Uni_Name, Country, Address, Username, Password) VALUES ('University of Berlin', 'Germany', 'Berlin Road, Berlin', 'berlin_uni', 'berlin123')")
        c.execute("INSERT INTO University (Uni_Name, Country, Address, Username, Password) VALUES ('National University of Singapore', 'Singapore', 'Singapore Road', 'nus_uni', 'nus123')")
        c.execute("INSERT INTO University (Uni_Name, Country, Address, Username, Password) VALUES ('University of Toronto', 'Canada', 'Canada Road', 'toronto_uni', 'toronto123')")

        c.execute("INSERT INTO Coordinator (Coordinator_Name, Email, Phone, Uni_Id, Username, Password) VALUES ('Dr. Argentina Fan', 'fan@aiub.edu', '0033-478-112233', 1, 'fan_coord', 'fan123')")
        c.execute("INSERT INTO Coordinator (Coordinator_Name, Email, Phone, Uni_Id, Username, Password) VALUES ('Dr. Spiderman', 'spiderman@berlin.de', '0049-30-998877', 3, 'spider_coord', 'spider123')")
        c.execute("INSERT INTO Coordinator (Coordinator_Name, Email, Phone, Uni_Id, Username, Password) VALUES ('Dr. Mei Tan', 'mei@nus.edu.sg', '0065-6516-2000', 4, 'mei_coord', 'mei123')")
        c.execute("INSERT INTO Coordinator (Coordinator_Name, Email, Phone, Uni_Id, Username, Password) VALUES ('Dr. John Carter', 'carter@utoronto.ca', '001-416-978-2011', 5, 'carter_coord', 'carter123')")

        c.execute("INSERT INTO Exchange_Program (Semester, Duration, Field_Of_Study, Max_Students, Uni_Id, Coordinator_Id) VALUES ('Fall 2026', 16, 'Business Administration', 25, 2, 1)")
        c.execute("INSERT INTO Exchange_Program (Semester, Duration, Field_Of_Study, Max_Students, Uni_Id, Coordinator_Id) VALUES ('Spring 2027', 14, 'Computer Science', 20, 3, 2)")
        c.execute("INSERT INTO Exchange_Program (Semester, Duration, Field_Of_Study, Max_Students, Uni_Id, Coordinator_Id) VALUES ('Fall 2026', 16, 'Data Science', 15, 4, 3)")
        c.execute("INSERT INTO Exchange_Program (Semester, Duration, Field_Of_Study, Max_Students, Uni_Id, Coordinator_Id) VALUES ('Spring 2027', 12, 'Electrical Engineering', 18, 5, 4)")

        c.execute("INSERT INTO Student (Student_Name, Department, CGPA, Email, Phone, Username, Password) VALUES ('Md Rezvine Enjoy Nakib', 'CSE', 3.75, '23-50573-1@student.aiub.edu', '01796585024', 'nakib', 'nakib123')")
        c.execute("INSERT INTO Student (Student_Name, Department, CGPA, Email, Phone, Username, Password) VALUES ('Rafiul Islam', 'CSE', 3.40, 'rafiul@aiub.edu', '01611-000003', 'rafiul', 'rafiul123')")
        c.execute("INSERT INTO Student (Student_Name, Department, CGPA, Email, Phone, Username, Password) VALUES ('Kabir Hossain', 'BBA', 3.10, 'kabir@aiub.edu', '01511-000004', 'kabir', 'kabir123')")
        c.execute("INSERT INTO Student (Student_Name, Department, CGPA, Email, Phone, Username, Password) VALUES ('Farhana Akter', 'EEE', 3.65, 'farhana@aiub.edu', '01911-000005', 'farhana', 'farhana123')")
        c.execute("INSERT INTO Student (Student_Name, Department, CGPA, Email, Phone, Username, Password) VALUES ('Tanvir Ahmed', 'CSE', 2.95, 'tanvir@aiub.edu', '01711-000006', 'tanvir', 'tanvir123')")

        c.execute("INSERT INTO Application (Application_Date, Status, Student_Id, Program_Id, Coordinator_Id) VALUES ('2026-06-01', 'Approved', 1, 1, 1)")
        c.execute("INSERT INTO Application (Application_Date, Status, Student_Id, Program_Id, Coordinator_Id) VALUES ('2026-06-03', 'Pending', 2, 3, 3)")
        c.execute("INSERT INTO Application (Application_Date, Status, Student_Id, Program_Id, Coordinator_Id) VALUES ('2026-06-05', 'Rejected', 3, 1, 1)")
        c.execute("INSERT INTO Application (Application_Date, Status, Student_Id, Program_Id, Coordinator_Id) VALUES ('2026-06-07', 'Approved', 4, 4, 4)")
        c.execute("INSERT INTO Application (Application_Date, Status, Student_Id, Program_Id, Coordinator_Id) VALUES ('2026-06-10', 'Pending', 5, 3, 3)")

    conn.commit()
    conn.close()
