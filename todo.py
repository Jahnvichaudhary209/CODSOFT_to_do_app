import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


todo_list = []
task_id_counter = 1


@app.route("/")
def index():

    return render_template("index.html", tasks=todo_list)


@app.route("/add", methods=["POST"])
def add_task():
    global task_id_counter
    task_content = request.form.get("task_name", "").strip()

    if task_content:
        new_task = {
            "id": task_id_counter,
            "task": task_content,
            "status": "Pending",
        }
        todo_list.append(new_task)
        task_id_counter += 1

    return redirect(url_for("index"))


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
  
    new_content = request.form.get("updated_task_name", "").strip()

    for item in todo_list:
        if item["id"] == task_id:
            if new_content:
                item["task"] = new_content
            break

    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_status(task_id):
    # Flips status between Pending and Completed
    for item in todo_list:
        if item["id"] == task_id:
            if item["status"] == "Pending":
                item["status"] = "Completed"
            else:
                item["status"] = "Pending"
            break

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global todo_list
   
    todo_list = [item for item in todo_list if item["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
 
    host_ip = "0.0.0.0"
    port_number = int(os.environ.get("PORT", 5000))

    print(f"🚀 Starting To-Do App server on http://{host_ip}:{port_number}")
    app.run(host=host_ip, port=port_number, debug=True)
