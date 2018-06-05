from flask import Flask, flash, session, request, redirect, render_template, url_for

from db.data_layer import create_project, get_all_projects, get_project, update_project, delete_project
from db.data_layer import create_task, get_task, get_all_tasks, update_task, delete_task

app = Flask(__name__)


@app.route('/')
def index():
    all_projects = get_all_projects()
    return render_template('index.html', all_projects = all_projects)

@app.route('/tasks/<project_id>')
def tasks(project_id):
    project = get_project(project_id)
    all_tasks = get_all_tasks(project_id)
    return render_template('tasks.html', all_tasks = all_tasks, project = project)

@app.route('/add_project', methods=['POST'])
def add_project():
    create_project(request.form['title'])
    return redirect(url_for('index'))

@app.route('/add_task/<project_id>', methods=['POST'])
def add_task(project_id):
    print (request.form)
    create_task(request.form['project_id'], request.form['description'])
    return redirect(url_for('tasks', project_id=project_id))

@app.route('/delete_project/<project_id>')
def delete(project_id):
    delete_project(project_id)
    return redirect(url_for('index'))

@app.route('/delete_task/<project_id>/<task_id>')
def delete__task(project_id, task_id):
    delete_task(task_id)
    return redirect(url_for('tasks', project_id = project_id))

@app.route('/edit_project/<project_id>', methods=['POST', 'GET'])
def edit_project(project_id):
    if request.method == 'POST':
        update_project(project_id, request.form['title'])
        return redirect(url_for('index'))

    project = get_project(project_id)
    return render_template('edit.html', project = project)

@app.route('/edit_task/<project_id>/<task_id>', methods=['POST', 'GET'])
def edit_task(project_id, task_id):
    if request.method == 'POST':
        update_task(task_id, request.form['description'])
        return redirect(url_for('tasks', project_id = project_id))

    project = get_project(project_id)
    task = get_task(task_id)
    return render_template('edit_task.html', project = project, task = task)


app.run(debug=True)