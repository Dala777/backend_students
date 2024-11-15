from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)
DATABASE = 'escuela.db'

# Conectar a la base de datos
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Cerrar la conexión a la base de datos
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Crear las tablas de la base de datos
with app.app_context():
    db = get_db()
    cursor = db.cursor()
    
    # Crear tabla de estudiantes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')

    # Crear tabla de cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            profesor_id INTEGER,
            FOREIGN KEY (profesor_id) REFERENCES profesores(id)
        )
    ''')

    # Crear tabla de profesores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profesores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL
        )
    ''')

    # Crear tabla de relación estudiantes-cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes_cursos (
            estudiante_id INTEGER,
            curso_id INTEGER,
            PRIMARY KEY (estudiante_id, curso_id),
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    ''')

    db.commit()

# CRUD de estudiantes
@app.route('/estudiantes', methods=['POST'])
def create_estudiante():
    data = request.get_json()
    nombre = data.get('nombre')
    edad = data.get('edad')

    if not nombre or not edad:
        return jsonify({'error': 'Datos incompletos'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO estudiantes (nombre, edad) VALUES (?, ?)', (nombre, edad))
    db.commit()
    return jsonify({'message': 'Estudiante creado con éxito'}), 201

@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM estudiantes')
    estudiantes = cursor.fetchall()
    return jsonify(estudiantes)

# CRUD de cursos
@app.route('/cursos', methods=['POST'])
def create_curso():
    data = request.get_json()
    nombre = data.get('nombre')
    profesor_id = data.get('profesor_id')

    if not nombre or not profesor_id:
        return jsonify({'error': 'Datos incompletos'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO cursos (nombre, profesor_id) VALUES (?, ?)', (nombre, profesor_id))
    db.commit()
    return jsonify({'message': 'Curso creado con éxito'}), 201

@app.route('/cursos', methods=['GET'])
def get_cursos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM cursos')
    cursos = cursor.fetchall()
    return jsonify(cursos)

# CRUD de profesores
@app.route('/profesores', methods=['POST'])
def create_profesor():
    data = request.get_json()
    nombre = data.get('nombre')
    especialidad = data.get('especialidad')

    if not nombre or not especialidad:
        return jsonify({'error': 'Datos incompletos'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO profesores (nombre, especialidad) VALUES (?, ?)', (nombre, especialidad))
    db.commit()
    return jsonify({'message': 'Profesor creado con éxito'}), 201

@app.route('/profesores', methods=['GET'])
def get_profesores():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM profesores')
    profesores = cursor.fetchall()
    return jsonify(profesores)

# Asignar estudiante a un curso
@app.route('/asignar', methods=['POST'])
def asignar_estudiante_curso():
    data = request.get_json()
    estudiante_id = data.get('estudiante_id')
    curso_id = data.get('curso_id')

    if not estudiante_id or not curso_id:
        return jsonify({'error': 'Datos incompletos'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO estudiantes_cursos (estudiante_id, curso_id) VALUES (?, ?)', (estudiante_id, curso_id))
    db.commit()
    return jsonify({'message': 'Estudiante asignado al curso con éxito'}), 201

if __name__ == '__main__':
    app.run(debug=True)
