from flask import Flask, jsonify, request
import psycopg2

# Database connection parameters
DB_NAME = "metal_data"
DB_USER = "dude"
DB_PASSWORD = "HeeHaw"
DB_HOST = "your_database_host"
DB_PORT = "your_database_port"

app = Flask(__name__)

@app.route('/api/metal-data/metals', methods=['GET'])
def get_metals():
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT hs_code FROM metal_data")
    metals = [row[0] for row in cursor.fetchall()]
    return jsonify(metals)

@app.route('/api/metal-data/years', methods=['GET'])
def get_years():
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT year FROM metal_data")
    years = [row[0] for row in cursor.fetchall()]
    return jsonify(years)

@app.route('/api/metal-data', methods=['GET'])
def get_data():
    metal = request.args.get('metal')
    year = request.args.get('year')

    if not metal or not year:
        return jsonify({"error": "Missing metal or year parameter"}), 400

    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT source, value FROM metal_data
        WHERE hs_code = %s AND year = %s
    """, (metal, year))

    data = [{"source": row[0], "value": row[1]} for row in cursor.fetchall()]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
