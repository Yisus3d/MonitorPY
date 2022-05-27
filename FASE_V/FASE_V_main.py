from flask import Flask, render_template, request, redirect, flash
import FASE_V_controller as controller_logs

app = Flask(__name__)


@app.route("/put_log")
def form_put_log():
    return render_template("put_log.html")


@app.route("/save_log", methods=["POST"])
def save_log():
    host = request.form["host"]
    port = request.form["port"]
    status = request.form["status"]
    controller_logs.put_log(host, port, status)
    return redirect("/logs")


@app.route("/")
@app.route("/logs")
def logs():
    logs = controller_logs.get_logs()
    return render_template("logs.html", logs=logs)


@app.route("/delete_log", methods=["POST"])
def delete_log():
    controller_logs.delete_log(request.form["id"])
    return redirect("/logs")


@app.route("/form_edit_log_id/<int:id>")
def edit_log(id):
    log = controller_logs.get_log_id(id)
    return render_template("update_log.html", log=log)


@app.route("/update_log", methods=["POST"])
def update_log():
    id = request.form["id"]
    host = request.form["host"]
    port = request.form["port"]
    status = request.form["status"]
    controller_logs.update_log(host, port, status, id)
    return redirect("/logs")

@app.route("/delete_data_log")
def delete_data_log():
    controller_logs.delete_data_log()
    return redirect("/logs")

@app.route("/create_data_log")
def create_data_log():
    return render_template("create_data.html")


@app.route("/save_create_log", methods=["POST"])
def save_create_log():
    host = request.form["host"]
    port = request.form["port"]
    controller_logs.create_data_logs(host, port)
    return redirect("/logs")

@app.route("/telegram_log")
def telegram_log():
    controller_logs.telegram_log()
    return redirect("/logs")


@app.route("/default_log")
def default_log():
    controller_logs.default_data_logs()
    return redirect("/logs")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
