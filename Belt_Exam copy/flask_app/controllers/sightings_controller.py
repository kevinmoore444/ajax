from flask import Flask, render_template, request, redirect, session, jsonify
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.sighting_model import Sighting
from flask import flash

@app.route('/sighting/new')
def recipe_new():
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template("create.html", logged_user=logged_user)

@app.route('/sighting/create', methods=['POST'])
def create_sighting():
        if "user_id" not in session:
            return redirect('/')
        if not Sighting.validator(request.form):
            return redirect('/sighting/new')
        sighting_data = {
            **request.form,
            'user_id': session['user_id']
        }
        Sighting.create(sighting_data)
        return redirect('/dashboard')

@app.route('/api/sighting/create', methods=['POST'])
def api_create_sighting():
        if "user_id" not in session:
            return redirect('/')
        print(request.form)
        # if not Sighting.validator(request.form): - Not going to work as it uses flash messages.
        #     return redirect('/sighting/new')
        sighting_data = {
            **request.form,
            'user_id': session['user_id']
        }
        id = Sighting.create(sighting_data)
        logged_user = User.get_by_id({'id':session['user_id']})
        res = {
            'message': "success",
            'data': sighting_data,
            'user_name': f"{logged_user.first_name} {logged_user.last_name}",
            'id':id
        }
        return jsonify(res)




@app.route('/sighting/<int:id>/view')
def one_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    user_data = {
        'id':session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    one_sighting = Sighting.get_one(data)
    return render_template("view.html", one_sighting=one_sighting,logged_user=logged_user)


@app.route("/sighting/<int:id>/edit")
def edit_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    user_data = {
        'id':session['user_id']
    }
    Sighting.update(data)
    logged_user = User.get_by_id(user_data)
    this_sighting = Sighting.get_one(data)
    return render_template("edit.html", this_sighting=this_sighting, logged_user=logged_user)

@app.route("/sighting/<int:id>/update", methods=['POST'])
def update_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    if not Sighting.validator(request.form):
        return redirect(f'/sighting/{id}/edit')
    data = {
        'id':id,
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'sighting_date': request.form['sighting_date'],
        'number_of': request.form['number_of'],
    }
    Sighting.update(data)
    return redirect('/dashboard')

@app.route('/sighting/<int:id>/delete')
def delete_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    Sighting.delete(data)
    return redirect('/dashboard')