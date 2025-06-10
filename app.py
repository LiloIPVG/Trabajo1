from flask import Flask, request, render_template, redirect, flash
from datetime import date

app = Flask(__name__)
idActual = 0

tareas = []

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html", tareas = tareas), 200

@app.route("/api/reminders", methods = ["GET"])
def listar_tareas():
    return render_template("index.html", tareas = tareas), 200

#######################CREACION#############################
@app.route("/api/reminders", methods = ["POST"])
def crear_tarea():
    global idActual
    datos = request.form
    contenido = datos.get("texto")
    if len(contenido) > 120:
        return redirect("/api/reminders"), 400
    importante = "importante" in datos
    nueva_tarea = { "id": idActual, "content": contenido, "createdAt": date.today(), "important": importante}
    idActual += 1
    tareas.append(nueva_tarea)
    return redirect("/api/reminders"), 201
##############OTRO########
@app.route("/api/reminders/<int:id>", methods=["POST"])
def manejar_formulario(id):
    override_method = request.form.get("_method", "").upper()

    if override_method == "PATCH":
        return actualizar_tarea(id)
    elif override_method == "DELETE":
        return borrar_tarea(id)
    else:
        return redirect("/api/reminders"), 405
#######################EDICION#########################
@app.route("/api/reminders/<int:id>", methods = ["PATCH"])
def actualizar_tarea(id):
    datos = request.form
    if len(datos.get("texto")) > 120:
        return redirect("api/reminders"), 400
    for tarea in tareas:
        if tarea["id"] == id:
            tarea["content"] = datos.get("texto")
            tarea["important"] = "importante" in datos
            return redirect("/"), 200
    return {"error": "Tarea no encontrada"}, 404

@app.route("/api/reminders/<int:id>", methods=["GET"])
def editar_tarea_form(id):
    for tarea in tareas:
        if tarea["id"] == id:
            return render_template("editar.html", tarea=tarea)
    return {"error": "Tarea no encontrada"}, 404
###################BORRAR##############################
@app.route("/api/reminders/<int:id>", methods = ["DELETE"])
def borrar_tarea(id):
    for tarea in tareas:
        if tarea["id"] == id:
            tareas.remove(tarea)
            return redirect("/api/reminders"), 204
    return {"error": "Tarea no encontrada"}, 404
    