from flask import Flask, jsonify, request

app = Flask(__name__)


platillos = [
    {
        "id": 1,
        "nombre": "Tacos al pastor",
        "precio": 8.5,
        "descripcion": "Tortillas de maíz con carne de cerdo marinada y piña.",
        "disponible": True,
    },
    {
        "id": 2,
        "nombre": "Ceviche de camarón",
        "precio": 12.0,
        "descripcion": "Camarones en jugo de limón con cilantro y cebolla morada.",
        "disponible": True,
    },
    {
        "id": 3,
        "nombre": "Ensalada de quinoa",
        "precio": 9.0,
        "descripcion": "Quinoa con vegetales asados y aderezo de limón.",
        "disponible": False,
    },
]


next_id = len(platillos) + 1


def buscar_platillo(platillo_id: int):
    return next((platillo for platillo in platillos if platillo["id"] == platillo_id), None)


@app.errorhandler(404)
def recurso_no_encontrado(error):
    return jsonify({"error": "Recurso no encontrado"}), 404


@app.route("/platillos", methods=["GET"])
def obtener_platillos():
    return jsonify({"platillos": platillos})


@app.route("/platillos/<int:platillo_id>", methods=["GET"])
def obtener_platillo(platillo_id: int):
    platillo = buscar_platillo(platillo_id)
    if not platillo:
        return recurso_no_encontrado(None)
    return jsonify(platillo)


@app.route("/platillos", methods=["POST"])
def crear_platillo():
    global next_id

    datos = request.get_json(silent=True) or {}
    nombre = datos.get("nombre")
    precio = datos.get("precio")

    if nombre is None or precio is None:
        return (
            jsonify({"error": "Debe incluir 'nombre' y 'precio' en el cuerpo JSON"}),
            400,
        )

    nuevo_platillo = {
        "id": next_id,
        "nombre": nombre,
        "precio": float(precio),
        "descripcion": datos.get("descripcion", ""),
        "disponible": bool(datos.get("disponible", True)),
    }
    platillos.append(nuevo_platillo)
    next_id += 1
    return jsonify(nuevo_platillo), 201


@app.route("/platillos/<int:platillo_id>", methods=["PUT"])
def actualizar_platillo(platillo_id: int):
    platillo = buscar_platillo(platillo_id)
    if not platillo:
        return recurso_no_encontrado(None)

    datos = request.get_json(silent=True) or {}
    if not datos:
        return jsonify({"error": "Debe enviar un cuerpo JSON con datos a actualizar"}), 400

    if "nombre" in datos:
        platillo["nombre"] = datos["nombre"]
    if "precio" in datos:
        platillo["precio"] = float(datos["precio"])
    if "descripcion" in datos:
        platillo["descripcion"] = datos["descripcion"]
    if "disponible" in datos:
        platillo["disponible"] = bool(datos["disponible"])

    return jsonify(platillo)


@app.route("/platillos/<int:platillo_id>", methods=["DELETE"])
def eliminar_platillo(platillo_id: int):
    platillo = buscar_platillo(platillo_id)
    if not platillo:
        return recurso_no_encontrado(None)

    platillos.remove(platillo)
    return "", 204


@app.route("/")
def inicio():
    return jsonify(
        {
            "mensaje": "API de platillos del restaurante",
            "endpoints": {
                "listar": "GET /platillos",
                "detalle": "GET /platillos/<id>",
                "crear": "POST /platillos",
                "actualizar": "PUT /platillos/<id>",
                "eliminar": "DELETE /platillos/<id>",
            },
        }
    )


if __name__ == "__main__":
    app.run(port=5500,debug=True)
