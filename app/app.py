from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import execute_query
import logging

logging.basicConfig(filename='logs/app.log', level=logging.INFO)


app = Flask(__name__)

# API GET TODOS ROUTE!
@app.route("/api/todos", methods=["GET"])
def api_get_todos():
    rows = execute_query(
        query="SELECT id, title, date_created FROM todos ORDER BY date_created DESC"
    )
    return jsonify(rows), 200

# API POST TODOS ROUTE
@app.route("/api/todos", methods=["POST"])
def api_create_todo():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title or not title.strip():
        return jsonify({"error": "Title is required"}), 400
    
    # Insert!
    execute_query(
        query="INSERT INTO todos (title) VALUES (%s)",
        params=(title.strip(),),
        select=False
    )
    # Return the created row 
    created = execute_query(
        query="SELECT id, title, date_created FROM todos WHERE title = %s ORDER BY id DESC LIMIT 1",
        params=(title.strip(),)
    )
    return jsonify(created[0]), 201

# API DELETE TODOS BY ID ROUTE
@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_delete_todo(todo_id):
    # Check if it exists
    todo_exists = execute_query(
        query="SELECT id FROM todos WHERE id = %s",
        params=(todo_id,)
    )
    if not todo_exists:
        return jsonify({"error": "todo not found"}), 404
    
    # Delete item if exists
    execute_query(
        query="DELETE FROM todos WHERE id = %s",
        params=(todo_id,),
        select=False
    )
    return jsonify({"status": "deleted", "id": todo_id}), 200

@app.route("/")
def landing_page():
    todo_list = execute_query(query='SELECT title FROM todos ORDER BY date_created DESC')
    return render_template('landing.html', todos=todo_list)

@app.route("/add_item", methods=['GET'])
def submit_item():
    return render_template('add_item.html') 

@app.route("/add_item", methods=['POST'])
def add_item():
    # Read title from the form
    title = request.form.get("title")
    # Submit todo item to database
    execute_query(query='INSERT INTO todos (title) VALUES (%s)', params=(title,), select=False)
    # Redirect user back to landing page with todo list
    return redirect(url_for('landing_page'))

@app.route("/delete_item", methods=['GET'])
def select_item():
    todo_list = execute_query(query='SELECT title FROM todos ORDER BY date_created DESC')
    return render_template('delete_item.html', todos=todo_list)

@app.route("/delete_item", methods=['POST'])
def delete_item():
    # Read title from the form
    title = request.form.get("title")
    # Delete todo item from database
    execute_query(query='DELETE FROM todos WHERE title = %s', params=(title,), select=False)
    return redirect(url_for('landing_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)