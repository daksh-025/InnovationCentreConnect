from flask import Flask, Response, render_template, request, jsonify
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import psycopg2
import requests
import os

conn = psycopg2.connect(
     host="db.eoehrierllfhmxlltdyf.supabase.co",
     database="postgres",
     user="postgres",
     password="Mhash@win576"
 )

# # Create a cursor object
cur = conn.cursor()

# # Execute a query
# cur.execute("SELECT * FROM your_table")

# # Fetch the results
# results = cur.fetchall()

# # Close the cursor and connection
# cur.close()
# conn.close()

app = Flask(__name__)
OUTPUT_FOLDER = 'static'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

login_data = 0

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Mhash@win576",
    host="db.eoehrierllfhmxlltdyf.supabase.co",
    port="5432"
)

userid = 0

@app.route('/')
def redirect_to_home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE emailid = %s AND password = %s", (email, password))
        user = cur.fetchone()
        print(user)
        global login_data
        login_data = user
        print(login_data)
        conn.commit()
        cur.close()
        if user[2] == 'student':
            return render_template('studentindex.html')
        if user[2] == 'startup owner':
            return render_template('startupindex.html')
        if user[2] == 'investor':
            return render_template('investorindex.html')
        if user[2] == 'admin':
            return render_template('admin.html')
        else:
            return render_template('invalidlogin.html')
    return render_template('login.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/student.html')
def student_page():
    return render_template('student.html')

@app.route('/register.html', methods=['GET', 'POST'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['date']
        type = request.form['usertype']

        cur = conn.cursor()
        cur.execute("INSERT INTO users (emailid, password,type,name,phoneno,dob) VALUES (%s, %s,%s,%s,%s,%s)", (email, password,type,name,phone,dob))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE emailid = %s AND password = %s", (email, password))
        global userid
        global login_data
        user = cur.fetchone()
        userid = user[0]
        login_data = user
        if(type == "student"):
            return redirect('/studentregister')
        if(type == "startup owner"):
            return redirect('/startupregister')
        if(type == "investor"):
            return redirect('/investorregister')

    return render_template('register.html')
@app.route('/studentregister.html', methods=['GET', 'POST'])

@app.route('/studentregister', methods=['GET', 'POST'])
def studentregister():
    if request.method == 'POST':
        branch = request.form['branch']
        cgpa = request.form['cgpa']
        domain = request.form['domain']
        regno = request.form['regno']

        cur = conn.cursor()
        cur.execute("INSERT INTO students (userid, branch, cgpa, interest_domain,regno) VALUES (%s,%s, %s,%s,%s)", (userid,branch, cgpa,domain,regno))
        conn.commit()
        cur.close()
        return render_template('registersucess.html')

    return render_template('studentregister.html')
@app.route('/startupregister.html', methods=['GET', 'POST'])

@app.route('/startupregister', methods=['GET', 'POST'])
def startupregister():
    if request.method == 'POST':
        valuation = request.form['valuation']
        revenue = request.form['revenue']
        #approvalstatus = request.form['approval']
        investmentraised = request.form['investment']
        companyname = request.form['cname']

        cur = conn.cursor()
        cur.execute("INSERT INTO startupowner (userid, company_name) VALUES (%s,%s)", (userid,companyname))
        cur.execute("INSERT INTO company (valuation, ownerid, revenue, approvalstatus, investmentraised,companyname) VALUES (%s,%s, %s,%s,%s,%s)", (valuation,userid, revenue,'approved',investmentraised,companyname))
        conn.commit()
        cur.close()
        return render_template('registersucess.html')

    return render_template('startupregister.html')

@app.route('/investorregister', methods=['GET', 'POST'])
def investorregister():
    if request.method == 'POST':
        firm_name = request.form['fname']

        cur = conn.cursor()
        cur.execute("INSERT INTO investor (userid, firm_name) VALUES (%s,%s)", (userid,firm_name))
        conn.commit()
        cur.close()
        return render_template('registersucess.html')

    return render_template('investorregister.html')

@app.route('/jobpost.html', methods=['GET', 'POST'])
@app.route('/jobpost', methods=['GET', 'POST'])
def jobpost():
    if request.method == 'POST':
        company_id = request.form['companyid']
        company_name = request.form['companyname']
        job_role = request.form['jobrole']
        cgpa = request.form['cgpa']
        openings = request.form['openings']
        salary = request.form['salary']

        cur = conn.cursor()
        cur.execute("INSERT INTO job (companyid, companyname,jobrole,cgpa,no_of_openings,salary) VALUES (%s,%s,%s,%s,%s,%s)", (company_id, company_name,job_role,cgpa,openings,salary))
        conn.commit()
        cur.close()
        return render_template('startupindex.html')

    return render_template('jobpost.html')

@app.route('/jobapp.html', methods=['GET', 'POST'])
@app.route('/jobapp', methods=['GET', 'POST'])
def jobapp():
    #if request.method == 'GET':
    cur = conn.cursor()
    cur.execute("Select * from job")
    jobs = cur.fetchall()
    print(jobs)
    conn.commit()
    cur.close()
    #return render_template('studentindex.html')

    return render_template('jobapp.html',jobs=jobs)

@app.route('/myapp.html', methods=['GET', 'POST'])
@app.route('/myapp', methods=['GET', 'POST'])
def myapp():
    #if request.method == 'GET':
    cur = conn.cursor()
    cur.execute("select * from application natural join job where student_id = %s;",(login_data[0],))
    apps = cur.fetchall()
    print(apps)
    conn.commit()
    cur.close()
    #return render_template('studentindex.html')

    return render_template('myapp.html',apps = apps)

@app.route('/profile.html')
def profile():
    return render_template('profile.html', data = login_data)

@app.route('/apply', methods=['GET', 'POST'])
@app.route('/apply.html', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        drive = request.form['drive']
        jobid = request.form['jobid']
        cover = request.form['cover']
        studentid = request.form['studentid']

        cur = conn.cursor()
        cur.execute("INSERT INTO application (drive_link_to_resume, student_id,job_id,cover_letter) VALUES (%s,%s,%s,%s)", (drive,studentid,jobid,cover))
        conn.commit()
        cur.close()
        return render_template('studentindex.html')
    return render_template('apply.html')


companyid = 0

def getcompanyid(name):
    print(login_data[5])
    cur = conn.cursor()
    cur.execute("select * from company where ownerid in (select userid from users where name = %s);", (name,))
    global companyid
    companydata = cur.fetchone()
    companyid = companydata[0]
    conn.commit()
    cur.close()
    return companyid

@app.route('/viewapp', methods=['GET', 'POST'])
@app.route('/viewapp.html', methods=['GET', 'POST'])
def viewapp():
    cid = getcompanyid(login_data[5])
    cur = conn.cursor()
    cur.execute("select name,cover_letter,drive_link_to_resume,phoneno,emailid,jobrole,salary from users,application,job where (users.userid = application.student_id and application.jobid = job.jobid and job.companyid= %s)LIMIT 30;", (cid,))
    views = cur.fetchall()
    conn.commit()
    cur.close()
    return render_template('viewapp.html', views = views)

@app.route('/startupindex.html')
@app.route('/startupindex.html')
def startupindex():
    return render_template("startupindex.html")

@app.route('/invest.html', methods=['GET', 'POST'])
@app.route('/invest', methods=['GET', 'POST'])
def invest():
    #if request.method == 'GET':
    cur = conn.cursor()
    cur.execute("Select * from company")
    invests = cur.fetchall()
    conn.commit()
    cur.close()

    return render_template('invest.html',invests = invests)


@app.route('/offer', methods=['GET', 'POST'])
@app.route('/offer.html', methods=['GET', 'POST'])
def offer():
    if request.method == 'POST':
        company_id = request.form['company_id']
        equity = request.form['equity']
        money_offered = request.form['money_offered']
        cur = conn.cursor()
        cur.execute("INSERT INTO investmentoffer VALUES (%s,%s,%s,%s)", (company_id,equity,money_offered,login_data[0]))
        conn.commit()
        cur.close()
        return render_template('investorindex.html')
    return render_template('offer.html')

@app.route('/deleteuser.html',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        type = request.form['usertype']
        cur = conn.cursor()
        query = "DELETE FROM users WHERE name = %s AND password = %s AND type = %s"
        values = (name, password, type)
        cur.execute(query,values)
        conn.commit()
        cur.close()
        return render_template('deleteuser.html')
    return render_template('deleteuser.html')   
@app.route('/execute_query', methods=['POST'])
def execute_query():
    try:
        # Get the query type from the request
        query_type = request.json['query_type']

        # Execute the corresponding query based on the query type
        if query_type == 'nested_query_1':
            cur = conn.cursor()
            cur.execute("SELECT name, emailid FROM users WHERE DOB = (SELECT MAX(DOB) FROM users);")
            result = cur.fetchall()
            print(result)
            return jsonify({'result': result})
        # Add more conditions for other query types if needed
        elif query_type == 'nested_query_2':
            cur = conn.cursor()
            query = """
SELECT * FROM students s
WHERE s.branch = 'Computer Science'
AND (s.branch, s.cgpa) IN (
    SELECT branch, MAX(cgpa) FROM students WHERE branch = 'Computer Science' GROUP BY branch
);
"""
            cur.execute(query)
            result = cur.fetchall()
            print(result)
            return jsonify({'result': result})
            # Add your logic for nested_query_2
           

        elif query_type == 'nested_query_3':
            cur = conn.cursor()
            query="""

    SELECT branch, COUNT(*) AS student_count
    FROM students
    WHERE branch = 'IT'
    GROUP BY branch;

"""
            cur.execute(query)
            result = cur.fetchall()
            print(result)
            return jsonify({'result': result})
            # Add your logic for nested_query_3
        
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/admin.html')
@app.route('/admin')
def admin():
    return render_template("admin.html")


if __name__ == '__main__':
    app.run(debug=True)
 