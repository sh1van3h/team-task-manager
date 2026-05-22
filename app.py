from flask import Flask , render_template ,request ,redirect ,session
import sqlite3

app = Flask(__name__)

app.secret_key = "MY_SECRET_KEY"

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

def get_current_user():
    email = session["user"]
    conn = get_db()
    cursor = conn.execute(""" 
            SELECT * FROM users
            WHERE email = ?
            """,(email,))
    user = cursor.fetchone()
    conn.close()
    return user

conn = get_db()
conn.execute(""" 
CREATE TABLE IF NOT EXISTS users(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             email TEXT,
             password TEXT
             )
""")
conn.close()

conn = get_db()
conn.execute(""" 
CREATE TABLE IF NOT EXISTS projects(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             project_name TEXT,
             admin_id INTEGER
             )
""")
conn.close()

conn = get_db()
conn.execute(""" 
CREATE TABLE IF NOT EXISTS tasks(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             project_id INTEGER,
             assigned_user INTEGER,
             title TEXT,
             description TEXT,
             priority TEXT,
             status TEXT,
             due_date TEXT
             )
""")

conn.execute(""" 
CREATE TABLE IF NOT EXISTS project_members(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             project_id INTEGER,
             user_id INTEGER
             )
""")
conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db()
        conn.execute(""" 
        INSERT INTO users(name,email,password)
        VALUES(?,?,?)      
        """,(name,email,password))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db()
        cursor = conn.execute(""" 
                 SELECT * FROM users
                 WHERE email = ? AND password = ?
                 """,(email,password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["user"] = email
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    user = get_current_user()
    conn = get_db()
    cursor = conn.execute(""" 
            SELECT * FROM projects
            WHERE admin_id = ?
            OR id IN(
            SELECT project_id
            FROM project_members
            WHERE user_id = ?
            )
            """,(user[0],user[0]))
    projects = cursor.fetchall()
    cursor = conn.execute(""" 
    SELECT COUNT(*) FROM tasks
    """)
    t_total = cursor.fetchone()[0]
    cursor = conn.execute(""" 
    SELECT status , COUNT(*)
    FROM tasks
    GROUP BY status
    """)
    all_status = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html",
                            user=user,
                            projects=projects,
                            t_total=t_total,
                            all_status=all_status)

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/login")

@app.route("/create-project",methods=["GET","POST"])
def create_project():
    if "user" not in session:
        return redirect("/login")
    if request.method == "POST":
        project_name = request.form["project_name"]
        email = session["user"]
        conn = get_db()
        cursor = conn.execute(""" 
                SELECT id FROM users
                WHERE email = ?
                """,(email,))
        user = cursor.fetchone()
        admin_id = user[0]
        conn.execute(""" 
        INSERT INTO projects(project_name,admin_id)
        VALUES(?,?)
        """,(project_name,admin_id))
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    return render_template("create_project.html")

@app.route("/project/<int:project_id>")
def project_page(project_id):
    if "user" not in session:
        return redirect("/login")
    conn = get_db()
    cursor = conn.execute(""" 
            SELECT * FROM projects
            WHERE id = ?
            """,(project_id,))
    project = cursor.fetchone()
    conn.close()

    conn = get_db()
    cursor = conn.execute(""" 
            SELECT * FROM tasks
            WHERE project_id = ?
            """,(project_id,))
    tasks = cursor.fetchall()
    
    cursor = conn.execute(""" 
    SELECT users.name FROM users JOIN project_members
    ON users.id = project_members.user_id 
    WHERE project_members.project_id = ?
    """,(project_id,))
    members = cursor.fetchall()

    user =  get_current_user()

    return render_template("project.html",
                            project=project,
                            tasks=tasks,
                            user=user,
                            members=members)

@app.route("/project/<int:project_id>/create-task",methods=["GET","POST"])
def create_task(project_id):
    if "user" not in session:
        return redirect("/login")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]
        user = get_current_user()
        conn = get_db()
        conn.execute(""" 
        INSERT INTO tasks(project_id,assigned_user,title,
                     description,priority,status,due_date)
        VALUES(?,?,?,?,?,?,?)
        """,(project_id,user[0],title,description,priority,"To Do",due_date))
        conn.commit()
        conn.close()
        return redirect(f"/project/{project_id}")
    return render_template("create_task.html")

@app.route("/update-task/<int:task_id>/<status>")
def update_task(task_id,status):
    if "user" not in session:
        return redirect("/login")
    conn = get_db();
    conn.execute(""" 
    UPDATE tasks
    SET status = ?
    WHERE id = ? 
    """,(status,task_id))
    conn.commit()
    cursor = conn.execute(""" 
    SELECT project_id FROM tasks
    WHERE id = ?
    """,(task_id,))
    task = cursor.fetchone()
    conn.close()
    return redirect(f"/project/{task[0]}")

@app.route("/delete-task/<int:task_id>")
def delete_task(task_id):
    if "user" not in session:
        return redirect("/login")
    user = get_current_user()
    conn = get_db()
    cursor = conn.execute(""" 
    SELECT project_id FROM tasks
    WHERE id = ?
    """,(task_id,))
    task = cursor.fetchone()

    cursor = conn.execute(""" 
    SELECT * FROM projects
    WHERE id = ?
    """,(task[0],))
    project = cursor.fetchone()
    if project[2] != user[0]:
        return "Access Denied"

    conn.execute(""" 
    DELETE FROM tasks
    WHERE id = ?
    """,(task_id,))
    conn.commit()
    conn.close()
    return redirect(f"/project/{task[0]}")

@app.route("/project/<int:project_id>/add-member",
          methods=["GET","POST"])
def add_member(project_id):
    if "user" not in session:
        return redirect("/login")
    user = get_current_user()
    conn = get_db()
    cursor = conn.execute(""" 
    SELECT * FROM projects
    WHERE id = ?
    """,(project_id,))
    project = cursor.fetchone()
    if project[2] != user[0]:
        return "Access Denied"
    if request.method == "POST":
        email = request.form["email"]
        cursor = conn.execute(""" 
        SELECT * FROM users
        WHERE email = ?
        """,(email,))
        member = cursor.fetchone()

        cursor = conn.execute(""" 
        SELECT * FROM project_members
        WHERE project_id = ?
        AND user_id = ?
        """,(project_id,member[0]))
        existing_member = cursor.fetchone()

        if member and not existing_member:
            conn.execute(""" 
            INSERT INTO project_members(
                         project_id,
                         user_id
                         )
            VALUES(?,?)
            """,(project_id,member[0]))
            conn.commit()
        conn.close()
        return redirect(f"/project/{project_id}")
    conn.close()
    return render_template("add_member.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
