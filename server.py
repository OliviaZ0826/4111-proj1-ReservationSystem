
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort, flash
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

app.secret_key = os.urandom(24)
#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@34.75.94.195/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.75.94.195/proj1part2"
#
DATABASEURI = "postgresql://zy2605:070087@34.74.171.121/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
conn = engine.connect()

# The string needs to be wrapped around text()

conn.execute(text("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);"""))
conn.execute(text("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');"""))

# To make the queries run, we need to add this commit line

conn.commit() 

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
# @app.route('/')
# def index():
#   """
#   request is a special object that Flask provides to access web request information:

#   request.method:   "GET" or "POST"
#   request.form:     if the browser submitted a form, this contains the data in the form
#   request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

#   See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

#   """

#   # DEBUG: this is debugging code to see what request looks like
#   print(request.args)


#   #
#   # example of a database query 
#   #
#   cursor = g.conn.execute(text("SELECT name FROM test"))
#   g.conn.commit()

#   # 2 ways to get results

#   # Indexing result by column number
#   names = []
#   for result in cursor:
#     names.append(result[0])  

#   # Indexing result by column name
#   names = []
#   results = cursor.mappings().all()
#   for result in results:
#     names.append(result["name"])
#   cursor.close()

#   #
#   # Flask uses Jinja templates, which is an extension to HTML where you can
#   # pass data to a template and dynamically generate HTML based on the data
#   # (you can think of it as simple PHP)
#   # documentation: https://realpython.com/primer-on-jinja-templating/
#   #
#   # You can see an example template in templates/index.html
#   #
#   # context are the variables that are passed to the template.
#   # for example, "data" key in the context variable defined below will be
#   # accessible as a variable in index.html:
#   #
#   #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
#   #     <div>{{data}}</div>
#   #
#   #     # creates a <div> tag for each element in data
#   #     # will print:
#   #     #
#   #     #   <div>grace hopper</div>
#   #     #   <div>alan turing</div>
#   #     #   <div>ada lovelace</div>
#   #     #
#   #     {% for n in data %}
#   #     <div>{{n}}</div>
#   #     {% endfor %}
#   #
#   context = dict(data = names)


#   #
#   # render_template looks in the templates/ folder for files.
#   # for example, the below file reads template/index.html
#   #
#   # return render_template("index.html", **context)

#   return render_template("index.html")
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
  if request.method == 'POST':
    # add new patient to our databse
    patient_name = request.form['patient_name']
    dob = request.form['dob']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    # need to modify the sql schema to general IDs automatically
    try:
      query = text("""INSERT INTO patient_assigned_account (Patient_Name, DateOfBirth, Email, Username, Password) VALUES (:patient_name, :dob, :email, :username, :password) RETURNING PatientID, UserID""")
      params = {'patient_name': patient_name, 'dob': dob, 'email': email, 'username': username, 'password': password}
      result = g.conn.execute(query, params).fetchone()
      g.conn.commit()

      flash(f'Registration successful! Your Patient ID is {result[0]} and User ID is {result[1]}.', 'success')
      return redirect('/login_patient')
    except Exception as e:
      print(e)
      flash('An error occurred. Please try again.', 'error')
      return redirect('/register_patient')

  return render_template('register_patient.html')



@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
  if request.method == 'POST':
    # add new doctor to our databse
    doctor_name = request.form['doctor_name']
    did = request.form['did']
    specialty = request.form['specialty']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    # need to modify the sql schema to generate IDs automatically
    try:
      query = text("""INSERT INTO doctor_wksin_account (DepartmentID, Doctor_Name, Specialty, Email, Username, Password) VALUES (:DID, :doctor_name, :specialty, :email, :username, :password) RETURNING DoctorID, UserID""")
      params = {'DID': did, 'doctor_name': doctor_name, 'specialty': specialty, 'email': email, 'username': username, 'password': password}
      result = g.conn.execute(query, params).fetchone()
      g.conn.commit()

      flash(f'Registration successful! Your Doctor ID is {result[0]} and User ID is {result[1]}.', 'success')
      return redirect('/login_doctor')
    except Exception as e:
      print(e)
      flash('An error occurred. Please try again.', 'error')
      return redirect('/register_doctor')

  return render_template('register_doctor.html')



@app.route('/login_patient', methods=['GET', 'POST'])
def login_patient():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    # Query to check if the user exists and password is correct
    query = text("SELECT * FROM patient_assigned_account WHERE Username = :username AND Password = :password")
    result = g.conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        # User exists and password is correct
        print(result)
        user_id = result[1]
        return redirect('/patient_dashboard/{}'.format(user_id))
    else:
        # User does not exist or password is incorrect
        flash('Invalid username or password. Please try again or register.', 'error')
        return redirect('/login_patient')

  return render_template('login_patient.html')



@app.route('/login_doctor', methods=['GET', 'POST'])
def login_doctor():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    # Query to check if the user exists and password is correct
    query = text("SELECT * FROM doctor_wksin_account WHERE Username = :username AND Password = :password")
    result = g.conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        # User exists and password is correct
        user_id = result[1]
        return redirect('/doctor_dashboard/{}'.format(user_id))
    else:
        # User does not exist or password is incorrect
        flash('Invalid username or password. Please try again or register.', 'error')
        return redirect('/login_doctor')

  return render_template('login_doctor.html')


@app.route('/schedule_appointment', methods=['GET', 'POST'])
def schedule_appointment():
  if request.method == 'POST':
    # Insert appointment details into the database
    return redirect('/patient_dashboard')

  return render_template('schedule_appointment.html')


#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
# @app.route('/another')
# def another():
#   return render_template("another.html")


# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add(): 
#   name = request.form['name']
#   params_dict = {"name":name}
#   g.conn.execute(text('INSERT INTO test(name) VALUES (:name)'), params_dict)
#   g.conn.commit()
#   return redirect('/')


# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()

# patient_dashboard
@app.route('/patient_dashboard/<int:user_id>')
def patient_dashboard(user_id):
    # Retrieve patient-specific information from the database based on user_id
    patient_info_query = text("SELECT * FROM patient_assigned_account WHERE UserID = :user_id")
    patient_info = g.conn.execute(patient_info_query, {'user_id': user_id}).fetchone()

    print(patient_info)

    # Retrieve insurance details for the patient
    insurance_query = text("SELECT * FROM with_insurance WHERE PatientID = :user_id")
    insurance_details = g.conn.execute(insurance_query,  {'user_id': user_id}).fetchall()

    print(insurance_details)

    # Retrieve payment details for the patient
    payment_query = text("SELECT * FROM resp_payment WHERE PatientID = :user_id")
    payment_details = g.conn.execute(payment_query,  {'user_id': user_id}).fetchall()

    # Retrieve doctor options for the dropdown
    doctor_query = text("SELECT DoctorID, Doctor_Name FROM doctor_wksin_account")
    doctors = g.conn.execute(doctor_query).fetchall()

    ID_query = text("""SELECT P.PatientID FROM patient_assigned_account P WHERE P.UserID = :user_id""")
    patient_id = g.conn.execute(ID_query, {'user_id': user_id}).fetchone()
    app_query = text("SELECT D.Doctor_Name, D.DepartmentID, D.Email, A.AppointmentDateTime, A.Status \
                      FROM Holds H, Appointment A, doctor_wksin_account D\
                      WHERE H.PatientID = :patient_id AND H.AppointmentID = A.AppointmentID \
                      AND D.DoctorID = H.DoctorID")
    app_info = g.conn.execute(app_query, {'patient_id': patient_id[0]}).fetchall()

    # Retrieve time options for the dropdown (you may need to replace it with actual data)
    time_options = ["9:00 AM", "10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM", "3:00 PM"]

    return render_template('patient_dashboard.html', patient_info=patient_info, insurance_details=insurance_details,
                           payment_details=payment_details, doctors=doctors, time_options=time_options, app_info=app_info)

@app.route('/add_insurance/<int:user_id>', methods=['GET', 'POST'])
def add_insurance(user_id):
  if request.method == 'POST':
    # add new patient to our databse
    insurance_id = request.form['InsuranceID']
    company = request.form['company']
    cover = request.form['cover']

    # need to modify the sql schema to general IDs automatically
    try:
      queryID = text("""SELECT P.PatientID FROM patient_assigned_account P WHERE P.UserID = :user_id""")
      patient_id = g.conn.execute(queryID, {'user_id': user_id}).fetchone()

      query = text("""INSERT INTO with_insurance (InsuranceID, PatientID, CompanyName, CoverageDetails) VALUES (:insurance_id, :patient_id, :company, :cover)""")
      params = {'insurance_id': insurance_id, 'patient_id': patient_id[0], 'company': company, 'cover': cover}
      g.conn.execute(query, params)
      g.conn.commit()

      return redirect('/patient_dashboard/{}'.format(user_id))
    except Exception as e:
      print(e)
      return redirect('/add_insurance/{}'.format(user_id))

  return render_template('add_insurance.html')

@app.route('/delete_insurance/<int:insurance_id>', methods=['POST'])
def delete_insurance(insurance_id):
    queryID = text("""SELECT P.UserID FROM patient_assigned_account P, with_insurance I WHERE I.InsuranceID = :insurance_id AND I.PatientID = P.PatientID""")
    user_id = g.conn.execute(queryID, {'insurance_id': insurance_id}).fetchone()
    try:
      delete_query = text("DELETE FROM with_insurance WHERE InsuranceID = :insurance_id")
      g.conn.execute(delete_query, {'insurance_id': insurance_id})
      g.conn.commit()
    except Exception as e:
      print(e)
    
    if user_id is not None:
      return redirect('/patient_dashboard/{}'.format(user_id[0]))
    else:
      return redirect('/login_patient')

# Doctor Dashboard Route
@app.route('/doctor_dashboard/<int:user_id>')
def doctor_dashboard(user_id):
    # Retrieve doctor-specific information from the database based on user_id
    doctor_info_query = text("SELECT * FROM doctor_wksin_account WHERE UserID = :user_id")
    doctor_info = g.conn.execute(doctor_info_query, {'user_id': user_id}).fetchone()

    print(doctor_info)

    ID_query = text("""SELECT D.DoctorID FROM doctor_wksin_account D WHERE D.UserID = :user_id""")
    doctor_id = g.conn.execute(ID_query, {'user_id': user_id}).fetchone()
    app_query = text("SELECT P.Patient_Name, P.Email, I.InsuranceID, A.AppointmentDateTime, A.Status \
                      FROM Holds H, Appointment A, patient_assigned_account P, with_insurance I \
                      WHERE H.DoctorID = :doctor_id AND H.AppointmentID = A.AppointmentID \
                      AND P.PatientID = H.PatientID AND I.PatientID = P.PatientID")
    app_info = g.conn.execute(app_query, {'doctor_id': doctor_id[0]}).fetchall()

    print(app_info)
    
    patient_payment_query = text("""SELECT P.UserID, P.Patient_Name, RP.Amount, RP.due, RP.isPaid
                                    FROM patient_assigned_account P
                                    JOIN Holds H ON P.PatientID = H.PatientID
                                    LEFT JOIN resp_payment RP ON P.PatientID = RP.PatientID
                                    WHERE H.DoctorID = :doctor_id""")
    patient_payment_info = g.conn.execute(patient_payment_query, {'doctor_id': doctor_id[0]}).fetchall()


    # Retrieve doctor's working location
    depart_id = doctor_info[2]
    location_query = text("SELECT * FROM Department WHERE DepartmentID = :depart_id")
    location = g.conn.execute(location_query, {'depart_id': depart_id}).fetchone()

    print(location)

    return render_template('doctor_dashboard.html', doctor_info=doctor_info, app_info=app_info,
                           patient_payment_info = patient_payment_info)

@app.route('/add_payment/<int:user_id>', methods=['POST'])
def add_payment(user_id):
  if request.method == 'POST':
    amount = request.form['amount']
    due = request.form['dueDate']
    doctor_user_id = request.form['doctor_user_id']

    # need to modify the sql schema to general IDs automatically
    try:
      queryID = text("""SELECT P.PatientID FROM patient_assigned_account P WHERE P.UserID = :user_id""")
      patient_id = g.conn.execute(queryID, {'user_id': user_id}).fetchone()

      query = text("""INSERT INTO resp_payment (Amount, PatientID, due, isPaid) VALUES (:amount, :patient_id, :due, :isPaid)""")
      params = {'amount': amount, 'patient_id': patient_id[0], 'due': due, 'isPaid': False}
      g.conn.execute(query, params)
      g.conn.commit()

      return redirect('/doctor_dashboard/{}'.format(doctor_user_id))
    except Exception as e:
      print(e)
      return redirect('/add_payment/{}'.format(user_id))

  return redirect('/doctor_dashboard/{}'.format(doctor_user_id))




if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
