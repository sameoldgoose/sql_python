# run the create_table.py to create the SQLite table
# use python -m flask run to run the code
# This is a Flask App that uses SQLite3 to
# execute (C)reate, (R)ead, (U)pdate, (D)elete operations
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Home Page route
@app.route("/")
def home():
    """
    Home page of the Student Management System.

    This page displays a welcome message and provides links to add a new student or view all students. render the home.html
    """

# Route to form used to add a new student to the database
@app.route("/enternew")
def enternew():
    """
    Add New Student Page.

    This page displays a form where users can enter the details of a new student. render student.html.
    """
    

# Route to add a new record (INSERT) student data to the database
@app.route("/addrec", methods=['POST'])
def addrec():
    """
    Add Record Page.

    This page handles the submission of the form data to add a new student record to the database. render result.html check if it post request and also run the sql query.
    """
    
            # Connect to SQLite3 database and execute the INSERT
            

# Route to SELECT all data from the database and display in a table
@app.route('/list')
def list():
    """
    View All Students Page.

    This page retrieves all student records from the database and displays them in a table.
    """
    # Connect to the SQLite3 database and SELECT rowid and all Rows from the students table. render the template.html after retrieving data and pass in the data as rows.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    # Send the results of the SELECT to the list.html page
    

# Route that will SELECT a specific row in the database then load an Edit form
@app.route("/edit", methods=['POST'])
def edit():
    """
    Edit Record Page.

    This page retrieves a specific student record from the database and loads an edit form. Render the edit.html form.
    """
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            
            # Connect to the database and SELECT a specific rowid
            

            rows = cur.fetchall()
        except:
            
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html", rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST'])
def editrec():
    """
    Edit Record Update Page.

    This page handles the submission of the form data to update a specific student record in the database.
    """
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            

            # UPDATE a specific record in the database based on the rowid
            
        except:
            con.rollback()
            msg = "Error in the Edit"

        finally:
            con.close()
            # Send the transaction message to result.html
            

# Route used to DELETE a specific record in the database
@app.route("/delete", methods=['POST'])
def delete():
    """
    Delete Record Page.

    This page handles the deletion of a specific student record from the database.
    """
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            
