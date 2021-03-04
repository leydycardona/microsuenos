from flask import Flask, json, request, jsonify
#from waitress import serve
from MySQL_Class import MySQL

mysql = MySQL()

app = Flask(__name__)
@app.route("/")
def server_info():
    rvs=mysql.ConsultData()
    content = {}
    employee = []
    for rv in rvs:
        content = {"id" :rv[0], "alarma": rv[1]}
        employee.append(content)
        content = {}
    get_thing = {"get_alarma":employee}


    return jsonify(get_thing)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True,
            threaded=True, use_reloader=False)