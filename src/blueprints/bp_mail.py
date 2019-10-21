import smtplib, ssl
from email.mime.text import MIMEText

from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request
from email.mime.multipart import MIMEMultipart

bp_mail = Blueprint('bp_mail', __name__)


@bp_mail.route('/mail', methods=['POST'])
@jwt_required
def enviar_correo_frontend():
    mensaje = request.get_json()
    enviarCorreo(mensaje)

def enviarCorreo(mensaje):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    with smtplib.SMTP("smtp.ucr.ac.cr", 25) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login("compras.celeq@ucr.ac.cr", "Compras.celeq19")

        message = MIMEMultipart("alternative")
        message["Subject"] = mensaje['subject']
        message["From"] = "compras.celeq@ucr.ac.cr"
        message["To"] = mensaje['destinatario']
        text = mensaje['texto']

        message.attach(MIMEText(text, "html"))

        server.sendmail(
            "compras.celeq@ucr.ac.cr",
            mensaje['destinatario'],
            message.as_string())
        server.quit()