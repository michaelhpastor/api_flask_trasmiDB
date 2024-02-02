from flask import Flask, jsonify, request
from db import obtener_conexion, create_app
from flask_cors import CORS
from data.pDatos import read_csv


def insertarDatos():
    file_path = "data/csv/estaciones-de-transmilenio.csv"
    header, data = read_csv(file_path)
    print(len(data))

    try:
        connection = obtener_conexion()
        with connection.cursor() as cursor:
            for x in data:
                nombre = x[1]
                troncal = x[2]
                ubicacion = "NULL"

                # Ejecutar la consulta para insertar un nuevo usuario
                cursor.execute("INSERT INTO estaciones (nombre, troncal, ubicacion) VALUES (%s, %s, %s)", (nombre,troncal,ubicacion))
                connection.commit()
            return jsonify({"OK": "estaciones guardadas"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()





app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
create_app(app)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    if request.method == 'GET':
        return jsonify({'metodo': 'GET vista index trasmi'})
    elif request.method == 'POST':
        return jsonify({'metodo': 'POST'})
    else:
        return jsonify({'metodo': request.method})


@app.route('/estaciones', methods=['GET', 'POST'])
def especialistas_route():
    
    try:
        connection = obtener_conexion()

        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM estaciones")
                data = cursor.fetchall()
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            return insertarDatos()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)