from flask import Flask, jsonify, request
from flask_cors import CORS
from email.message import EmailMessage
import ssl
import smtplib




app=Flask(__name__)
CORS(app, origins=['http://localhost:8080', 'http://localhost:5000', 'http://localhost:80','http://54.205.29.249:8080','http://54.205.29.249'])

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorizations, true")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PATCH, DELETE")
    return response
    
@app.route('/', methods=['GET'])
def api_home():
    try:
        return {
            "success": True,
            "message": "Bienvenido"
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }, 500

@app.route("/users", methods=["GET"])
def get_users():
    users = ["diego B"]

    if len(users) == 0:
        return {
            "message": "No se encontaron usuarios"
        }, 404
        
    return {
        "success": True,
        "users": [user.format() for user in users],
        "total_users": len(users)
    }, 200


@app.route('/login', methods=['POST'])
def api_login():
        if request.method == 'POST':
            username = request.json.get("username")
            password = request.json.get("password")

            user = "diego"

            if user == username:
                if password == "12345678":
                    return {
                        "success": True,
                        "message": "Usuario autenticado correctamente",
                        "id": 1,
                        "usuario": "diego",
                    }
                else:
                    return {
                        "success": False,
                        "message": "Contraseña incorrecta"
                    }, 401
            else:
                return {
                    "success": False,
                    "message": "Usuario no encontrado"
                }, 404


@app.route('/correo', methods=['POST'])
def Correo():
        user = 'dieg5206@gmail.com'
        app_password = 'unppqmnkfckvtttq'

        correo1 = request.json.get("correo")
        nombre1 = request.json.get("nombre")
        texto1 = request.json.get("texto")

        subject = 'Un nuevo usuario quiere contactarse contigo'
        content = "holaa, el usuario " + nombre1 + " quiere contactarse contigo, su correo es: " + correo1 + ". \n el te envia esto: \n" + texto1

        em = EmailMessage()
        em['From'] = user
        em['To'] = correo1
        em['Subject'] = subject
        em.set_content(content)

        context1 = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context1) as smtp:
            smtp.login(user,app_password)
            smtp.sendmail(user,correo1,em.as_string())
        return jsonify({
            'success': True,
            'message': 'se envio el correo'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
