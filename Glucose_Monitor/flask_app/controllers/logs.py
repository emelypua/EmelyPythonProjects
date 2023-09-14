from flask import render_template, session, request, redirect, url_for, flash

from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.log import Log
from flask_app.models.user import User

@app.route('/dashboard')
def welcome():
    if "id" not in session:
        return redirect ('/logout')
    data ={
        'id' : session['id']
    }
    user= User.get_by_id_user(data)
    one_reading = Log.get_all_reports()
    return render_template("dashboard.html", user = user, one_reading = one_reading)

@app.route('/new/reading')
def add_reading():
    if "id" not in session:
        return redirect ('/logout')
    user = session['id']
    print(user)
    return render_template("add.html", user = user)

@app.route('/reading/create', methods = ['POST'])
def create():
    if "id" not in session:
        return redirect ('/')
    print(request.form)
    # user_id = session['id']
    if not Log.validate_report(request.form):
        return redirect('/new/reading')
    Log.save_report(request.form)
    return redirect('/dashboard')

@app.route('/edit/reading/<int:patient_id>')
def edit_log(patient_id):
    if "id" not in session:
        return redirect ('/')
    data = {
        "id": patient_id
    }
    edit_log = Log.get_by_id(data)
    print(data, '***********')
    return render_template("edit.html", b = edit_log)

@app.route('/update', methods=['POST'])
def update_reading():
    if not Log.validate_report(request.form):
        return redirect(f'/edit/reading/{request.form["id"]}')
    data = Log.parce_form(request.form)
    Log.update_report(data)
    return redirect('/dashboard')

# @app.route('/update', methods=['POST'])
# def update_reading():
#     data = {
#         "id": request.form.get("id"),
#         "date": request.form.get("date"),
#         "time": request.form.get("time"),
#         "glucose": request.form.get("glucose"),
#         "mealtype": request.form.get("mealtype"),
#         "log_meal": request.form.get("log_meal")
#     }

#     if not Log.validate_report(data):
#         return redirect(f'/edit/reading/{data["id"]}')

#     Log.update_report(data)
#     return redirect('/dashboard')

# SHOW REPORT
@app.route('/show/reading/<int:id>')
def show_reading(id):
    if "id" not in session:
        return redirect ('/')
    user_id = session['id']
    report_data = {
        "id":id
    }
    data = {
    'id' : session['id']
    }
    show_logs = Log.get_by_id(report_data)
    user = User.get_by_id_user(data)
    return render_template("show.html", user = user,  c = show_logs)

@app.route('/destroy/<int:id>', methods=['POST'])
def delete_report(id):
    Log.destroy_report({"id": id})
    return redirect('/dashboard')