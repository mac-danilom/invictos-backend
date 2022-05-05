from flask import Flask, jsonify, request
import sqlite3 

app = Flask(__name__)
conn = sqlite3.connect('apptodo.db', check_same_thread=False) 

def create_table_if_not_exists():
    cursor = conn.cursor()
    create_query = (
        "CREATE TABLE IF NOT EXISTS tarefas("
            "email VARCHAR(50) DEFAULT NULL, "
            "name VARCHAR(50) DEFAULT NULL, "
            "date_time DATETIME DEFAULT NULL, "
            "status VARCHAR(255) DEFAULT NULL, "
            "PRIMARY KEY (email, name));" )
    cursor.execute(create_query)
    conn.commit()
    print("- A tabela de tarefas foi criada")

@app.route('/')
def home():
    return 'Invictos'

@app.route('/task', methods=['GET', 'POST', 'PUT', 'DELETE'])
def task():
    """
    Realiza as quatro operações do CRUD na tabela de tarefas 
    """
    if request.method == 'GET':
        email = request.args.get('email')
        
        cursor = conn.cursor()
        select_user_task = f"SELECT * FROM tarefas WHERE email = '{email}'"
        cursor.execute(select_user_task)
        data = cursor.fetchall()
        return jsonify(
            rows=data,
            status_code=200)
        
    elif request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        date_time = request.form.get('date_time')
        status = request.form.get('status')
        
        cursor = conn.cursor()
        insert_query = (
            "INSERT OR IGNORE INTO tarefas (email, name, date_time, status) "
            f"VALUES ('{email}', '{name}', '{date_time}', '{status}')" )
        cursor.execute(insert_query)
        conn.commit()
        return jsonify(
            messsage='Tarefa criada com sucesso.',
            status_code=200)
        
    elif request.method == 'PUT':
        email = request.form.get('email')
        name = request.form.get('name')
        status = request.form.get('status')
        
        cursor = conn.cursor()
        update_task_query = (
            f"UPDATE tarefas SET status = '{status}' "
            f"WHERE email = '{email}' AND name = '{name}'")
        cursor.execute(update_task_query)
        conn.commit()
        return jsonify(
            messsage='Tarefa alterada com sucesso.',
            status_code=200)
        
    elif request.method == 'DELETE':
        email = request.form.get('email')
        name = request.form.get('name')
    
        cursor = conn.cursor()
        delete_task_query = (
            "DELETE FROM tarefas "
            f"WHERE email = '{email}' AND name = '{name}'")
        cursor.execute(delete_task_query)
        conn.commit()
        return jsonify(
            messsage='Tarefa deletada com sucesso.',
            status_code=200)


@app.route('/all')
def select_all():
    cursor = conn.cursor()
    select_user_task = f"SELECT * FROM tarefas"
    cursor.execute(select_user_task)
    data = cursor.fetchall()
    return jsonify(
        rows=data,
        status_code=200
    )
    
    
@app.route('/truncate')
def truncate_tasks_table():
    cursor = conn.cursor()
    select_user_task = f"DELETE FROM tarefas"
    cursor.execute(select_user_task)
    return jsonify(
        message='Todos os dados da Invictos foram deletados',
        status_code=200
    )


def drop_table_if_exists():
    cursor = conn.cursor()
    select_user_task = f"DROP TABLE IF EXISTS tarefas"
    cursor.execute(select_user_task)
    
    
if __name__ == '__main__':
    create_table_if_not_exists()
    app.run(host='localhost', port='5000')
    
