from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_config import get_connection, close_connection, init_database
import sqlite3

app = Flask(__name__)
app.secret_key = 'student_exchange_secret_key'

init_database()

def login_required(role=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first!', 'error')
                return redirect(url_for('home'))
            if role and session.get('role') != role:
                flash('Access denied!', 'error')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@app.route('/')
def home():
    return render_template('landing.html')

# ============ STUDENT AUTH ============
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM Student WHERE Username=? AND Password=?", (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user['Student_Id']
                session['username'] = username
                session['role'] = 'student'
                session['name'] = user['Student_Name']
                flash(f'Welcome {session["name"]}!', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid username or password!', 'error')
        finally:
            close_connection(conn)
    return render_template('student_login.html')

@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            dept = request.form['department']
            cgpa = float(request.form['cgpa'])
            email = request.form['email']
            phone = request.form['phone']
            username = request.form['username']
            password = request.form['password']
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO Student (Student_Name, Department, CGPA, Email, Phone, Username, Password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (name, dept, cgpa, email, phone, username, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('student_login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists!', 'error')
            return redirect(url_for('student_register'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('student_register'))
        finally:
            close_connection(conn)
    return render_template('student_register.html')

# ============ COORDINATOR AUTH ============
@app.route('/coordinator/login', methods=['GET', 'POST'])
def coordinator_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM Coordinator WHERE Username=? AND Password=?", (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user['Coordinator_Id']
                session['username'] = username
                session['role'] = 'coordinator'
                session['name'] = user['Coordinator_Name']
                flash(f'Welcome {session["name"]}!', 'success')
                return redirect(url_for('coordinator_dashboard'))
            else:
                flash('Invalid username or password!', 'error')
        finally:
            close_connection(conn)
    return render_template('coordinator_login.html')

@app.route('/coordinator/register', methods=['GET', 'POST'])
def coordinator_register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            uni_id = int(request.form['uni_id'])
            username = request.form['username']
            password = request.form['password']
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO Coordinator (Coordinator_Name, Email, Phone, Uni_Id, Username, Password) VALUES (?, ?, ?, ?, ?, ?)",
                      (name, email, phone, uni_id, username, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('coordinator_login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists!', 'error')
            return redirect(url_for('coordinator_register'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('coordinator_register'))
        finally:
            close_connection(conn)
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT Uni_Id, Uni_Name FROM University")
        universities = c.fetchall()
        return render_template('coordinator_register.html', universities=universities)
    finally:
        close_connection(conn)

# ============ UNIVERSITY AUTH ============
@app.route('/university/login', methods=['GET', 'POST'])
def university_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM University WHERE Username=? AND Password=?", (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user['Uni_Id']
                session['username'] = username
                session['role'] = 'university'
                session['name'] = user['Uni_Name']
                flash(f'Welcome {session["name"]}!', 'success')
                return redirect(url_for('university_dashboard'))
            else:
                flash('Invalid username or password!', 'error')
        finally:
            close_connection(conn)
    return render_template('university_login.html')

@app.route('/university/register', methods=['GET', 'POST'])
def university_register():
    if request.method == 'POST':
        try:
            uni_name = request.form['uni_name']
            country = request.form['country']
            address = request.form['address']
            username = request.form['username']
            password = request.form['password']
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO University (Uni_Name, Country, Address, Username, Password) VALUES (?, ?, ?, ?, ?)",
                      (uni_name, country, address, username, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('university_login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
            return redirect(url_for('university_register'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('university_register'))
        finally:
            close_connection(conn)
    return render_template('university_register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# ============ STUDENT DASHBOARD ============
@app.route('/student/dashboard')
@login_required('student')
def student_dashboard():
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""SELECT p.Program_Id, p.Semester, p.Duration, p.Field_Of_Study, p.Max_Students,
                            u.Uni_Name, c.Coordinator_Name
                     FROM Exchange_Program p
                     JOIN University u ON p.Uni_Id = u.Uni_Id
                     LEFT JOIN Coordinator c ON p.Coordinator_Id = c.Coordinator_Id""")
        programs = c.fetchall()
        c.execute("""SELECT a.Application_Id, a.Application_Date, a.Status, p.Field_Of_Study, u.Uni_Name
                     FROM Application a
                     JOIN Exchange_Program p ON a.Program_Id = p.Program_Id
                     JOIN University u ON p.Uni_Id = u.Uni_Id
                     WHERE a.Student_Id=?""", (session['user_id'],))
        my_apps = c.fetchall()
        return render_template('student_dashboard.html', programs=programs, applications=my_apps)
    finally:
        close_connection(conn)

@app.route('/student/apply', methods=['POST'])
@login_required('student')
def apply_program():
    try:
        program_id = int(request.form['program_id'])
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT Coordinator_Id FROM Exchange_Program WHERE Program_Id=?", (program_id,))
        prog = c.fetchone()
        coord_id = prog['Coordinator_Id'] if prog else None
        c.execute("INSERT INTO Application (Application_Date, Status, Student_Id, Program_Id, Coordinator_Id) VALUES (DATE('now'), 'Pending', ?, ?, ?)",
                  (session['user_id'], program_id, coord_id))
        conn.commit()
        flash('Application submitted successfully!', 'success')
    except sqlite3.IntegrityError:
        flash('You have already applied to this program!', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_connection(conn)
    return redirect(url_for('student_dashboard'))

@app.route('/student/cancel/<int:app_id>')
@login_required('student')
def cancel_application(app_id):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Application WHERE Application_Id=? AND Student_Id=? AND Status='Pending'",
                  (app_id, session['user_id']))
        conn.commit()
        flash('Application cancelled!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_connection(conn)
    return redirect(url_for('student_dashboard'))

# ============ COORDINATOR DASHBOARD ============
@app.route('/coordinator/dashboard')
@login_required('coordinator')
def coordinator_dashboard():
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""SELECT a.Application_Id, a.Application_Date, a.Status,
                            s.Student_Name, s.Department, s.CGPA, s.Email, s.Phone,
                            p.Field_Of_Study, p.Semester, u.Uni_Name
                     FROM Application a
                     JOIN Student s ON a.Student_Id = s.Student_Id
                     JOIN Exchange_Program p ON a.Program_Id = p.Program_Id
                     JOIN University u ON p.Uni_Id = u.Uni_Id
                     WHERE a.Coordinator_Id=?
                     ORDER BY a.Application_Date DESC""", (session['user_id'],))
        applications = c.fetchall()
        c.execute("SELECT * FROM Exchange_Program WHERE Coordinator_Id=?", (session['user_id'],))
        programs = c.fetchall()
        return render_template('coordinator_dashboard.html', applications=applications, programs=programs)
    finally:
        close_connection(conn)

@app.route('/coordinator/update/<int:app_id>', methods=['POST'])
@login_required('coordinator')
def update_status(app_id):
    try:
        status = request.form['status']
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE Application SET Status=? WHERE Application_Id=? AND Coordinator_Id=?",
                  (status, app_id, session['user_id']))
        conn.commit()
        flash(f'Application {status.lower()} successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_connection(conn)
    return redirect(url_for('coordinator_dashboard'))

# ============ UNIVERSITY DASHBOARD ============
@app.route('/university/dashboard')
@login_required('university')
def university_dashboard():
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""SELECT c.Coordinator_Id, c.Coordinator_Name, c.Email, c.Phone, c.Username
                     FROM Coordinator c WHERE c.Uni_Id=?""", (session['user_id'],))
        coordinators = c.fetchall()
        c.execute("""SELECT a.Application_Id, a.Application_Date, a.Status,
                            s.Student_Name, s.Department, s.CGPA,
                            p.Field_Of_Study, p.Semester,
                            c.Coordinator_Name
                     FROM Application a
                     JOIN Student s ON a.Student_Id = s.Student_Id
                     JOIN Exchange_Program p ON a.Program_Id = p.Program_Id
                     JOIN Coordinator c ON a.Coordinator_Id = c.Coordinator_Id
                     WHERE p.Uni_Id=?
                     ORDER BY a.Application_Date DESC""", (session['user_id'],))
        applications = c.fetchall()
        c.execute("""SELECT p.Program_Id, p.Semester, p.Duration, p.Field_Of_Study, p.Max_Students,
                            c.Coordinator_Name
                     FROM Exchange_Program p
                     LEFT JOIN Coordinator c ON p.Coordinator_Id = c.Coordinator_Id
                     WHERE p.Uni_Id=?""", (session['user_id'],))
        programs = c.fetchall()
        return render_template('university_dashboard.html', coordinators=coordinators, applications=applications, programs=programs)
    finally:
        close_connection(conn)

@app.route('/university/add_coordinator', methods=['POST'])
@login_required('university')
def add_coordinator():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO Coordinator (Coordinator_Name, Email, Phone, Uni_Id, Username, Password) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, email, phone, session['user_id'], username, password))
        conn.commit()
        flash('Coordinator added successfully!', 'success')
    except sqlite3.IntegrityError:
        flash('Username or Email already exists!', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_connection(conn)
    return redirect(url_for('university_dashboard'))

@app.route('/university/delete_coordinator/<int:coord_id>')
@login_required('university')
def delete_coordinator(coord_id):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE Exchange_Program SET Coordinator_Id=NULL WHERE Coordinator_Id=?", (coord_id,))
        c.execute("UPDATE Application SET Coordinator_Id=NULL WHERE Coordinator_Id=?", (coord_id,))
        c.execute("DELETE FROM Coordinator WHERE Coordinator_Id=? AND Uni_Id=?", (coord_id, session['user_id']))
        conn.commit()
        flash('Coordinator removed successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_connection(conn)
    return redirect(url_for('university_dashboard'))

@app.route('/university/add_program', methods=['POST'])
@login_required('university')
def add_program():
    try:
        semester = request.form['semester']
        duration = int(request.form['duration'])
        field = request.form['field']
        max_students = int(request.form['max_students'])
        coord_id = request.form['coord_id']
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO Exchange_Program (Semester, Duration, Field_Of_Study, Max_Students, Uni_Id, Coordinator_Id) VALUES (?, ?, ?, ?, ?, ?)",
                  (semester, duration, field, max_students, session['user_id'], int(coord_id) if coord_id else None))
        conn.commit()
        flash('Program added successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_connection(conn)
    return redirect(url_for('university_dashboard'))

@app.route('/university/delete_program/<int:prog_id>')
@login_required('university')
def delete_program(prog_id):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Application WHERE Program_Id=?", (prog_id,))
        c.execute("DELETE FROM Exchange_Program WHERE Program_Id=? AND Uni_Id=?", (prog_id, session['user_id']))
        conn.commit()
        flash('Program deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_connection(conn)
    return redirect(url_for('university_dashboard'))

@app.route('/database')
def database_viewer():
    conn = get_connection()
    try:
        c = conn.cursor()
        tables = {}
        for name in ["University", "Coordinator", "Exchange_Program", "Student", "Application"]:
            c.execute(f"SELECT * FROM {name}")
            columns = [desc[0] for desc in c.description]
            rows = c.fetchall()
            tables[name] = {"columns": columns, "rows": rows}
        return render_template('database_viewer.html', tables=tables)
    finally:
        close_connection(conn)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
