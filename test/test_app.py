from flask import Flask, request, jsonify, render_template
from models import db, Department, Job, Employee
from config import DATABASE_URI
import pandas as pd
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)

# Frontend Section
@app.route('/')
def root() -> str:
    """Renderiza la página principal."""
    return render_template('home.html')

@app.route('/upload_csv_form')
def upload_csv_form() -> str:
    """Renderiza el formulario para subir archivos CSV."""
    return render_template('upload_csv.html')

@app.route('/hired_by_department_jobs')
def get_page_hired_by_departments_jobs() -> str:
    """Renderiza la página para ver contrataciones por departamento y trabajo."""
    return render_template('hired_by_departments_and_jobs.html')

@app.route('/hired_above_mean')
def get_page_hired_above_mean() -> str:
    """Renderiza la página para ver contrataciones por encima de la media."""
    return render_template('hired_above_mean.html')


# Backend section
@app.route('/upload_csv', methods=['POST'])
def upload_csv() -> jsonify:
    """
    Endpoint para subir archivos CSV.
    
    Returns:
        JSON response indicando el estado de la subida del archivo.
    """
    csv_file = request.files['file']
    if not csv_file:
        return jsonify({"error": "No file uploaded"}), 400

    file_name = csv_file.filename

    try:
        df = pd.read_csv(csv_file, header=None)

        if file_name == 'departments.csv':
            load_departments(df)
        elif file_name == 'jobs.csv':
            load_jobs(df)
        elif file_name == 'hired_employees.csv':
            load_employees(df)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        return jsonify({"message": "File uploaded and processed successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/metrics/departments_above_mean', methods=['GET'])
def departments_above_mean() -> jsonify:
    """
    Endpoint para obtener los departamentos por encima de la media.
    
    Returns:
        JSON response con los departamentos y el número de contrataciones por encima de la media.
    """
    try:
        query = text('SELECT * FROM vst_hired_above_mean')
        result = db.session.execute(query).fetchall()

        output = [{'id': row[0], 'department': row[1], 'hired': row[2]} for row in result]
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/metrics/hired_by_department_and_job', methods=['GET'])
def hired_by_department_and_job() -> jsonify:
    """
    Endpoint para obtener las contrataciones por departamento y trabajo.
    
    Returns:
        JSON response con los departamentos, trabajos y las contrataciones trimestrales.
    """
    try:
        query = text('SELECT * FROM vst_hired_by_department_and_job;')
        result = db.session.execute(query).fetchall()

        output = [{"department": row[0], "job": row[1], "Q1": row[2], "Q2": row[3], "Q3": row[4], "Q4": row[5]} for row in result]
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ETL section  
def load_departments(df: pd.DataFrame) -> None:
    """
    Transforma y carga los departamentos.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de los departamentos.
    """
    try:
        batch_size = 1000
        row_count = 0
        sql = "TRUNCATE TABLE departments RESTART IDENTITY CASCADE"
        db.session.execute(text(sql))

        column_names = ['id', 'department']
        df.columns = column_names

        for _, row in df.iterrows():
            department = Department(id=row['id'], department=row['department'])
            db.session.add(department)
            row_count += 1

            if row_count % batch_size == 0 or row_count == len(df):
                db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def load_jobs(df: pd.DataFrame) -> None:
    """
    Transforma y carga los trabajos.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de los trabajos.
    """
    try:
        batch_size = 1000
        row_count = 0
        sql = 'TRUNCATE TABLE jobs RESTART IDENTITY CASCADE'
        db.session.execute(text(sql))

        column_names = ['id', 'job']
        df.columns = column_names

        for _, row in df.iterrows():
            job = Job(id=row['id'], job=row['job'])
            db.session.add(job)
            row_count += 1

            if row_count % batch_size == 0 or row_count == len(df):
                db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def load_employees(df: pd.DataFrame) -> None:
    """
    Transforma y carga los empleados.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de los empleados.
    """
    try:
        batch_size = 1000
        row_count = 0
        sql = 'TRUNCATE TABLE employees RESTART IDENTITY'
        db.session.execute(text(sql))

        column_names = ['id', 'name', 'datetime', 'department_id', 'job_id']
        df.columns = column_names
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['datetime'] = df['datetime'].replace({pd.NaT: None})
        df['job_id'] = df['job_id'].replace({float('nan'): None})
        df['department_id'] = df['department_id'].replace({float('nan'): None})

        for _, row in df.iterrows():
            employee = Employee(id=row['id'], name=row['name'], datetime=row['datetime'], department_id=row['department_id'], job_id=row['job_id'])
            db.session.add(employee)
            row_count += 1

            if row_count % batch_size == 0 or row_count == len(df):
                db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


# Main section
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)