import csv
import os
import re
import smtplib
from email.message import EmailMessage

PENDIENTES = "datos/pendientes_envio.csv"
LOG_ENVIO = "logs/log_envios.csv"

SMTP_SERVER = "mail.smtp2go.com"
SMTP_PORT = 587
SMTP_USER = "correos.ctpsanisidro@hotmail.com"
SMTP_PASS = "6tJ5bKNtZanC4tTD"

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def enviar_correo(destino, archivo_pdf):
    msg = EmailMessage()
    msg['Subject'] = "Factura Electrónica"
    msg['From'] = 'Facturación IRSI <correos.ctpsanisidro@hotmail.com>'
    msg['To'] = destino
    html = f"""
    <html>
      <body>
        <p>Estimado cliente,<br>
           Adjunto encontrará su factura electrónica.<br>
           <b>Gracias por su preferencia.</b>
        </p>
      </body>
    </html>
    """
    msg.set_content("Adjunto encontrará su factura electrónica.")
    msg.add_alternative(html, subtype='html')

    with open(archivo_pdf, 'rb') as f:
        contenido = f.read()
    msg.add_attachment(contenido, maintype='application', subtype='pdf', filename=os.path.basename(archivo_pdf))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error enviando a {destino}: {e}")
        return False

def main():
    if not os.path.exists(PENDIENTES):
        print(f"No se encontró {PENDIENTES}")
        return

    pendientes_nuevos = []
    with open(PENDIENTES, newline='', encoding='utf-8') as f_in, open(LOG_ENVIO, 'a', encoding='utf-8') as f_log:
        lector = csv.reader(f_in)
        for fila in lector:
            if len(fila) != 2:
                continue
            pdf, correo = fila
            correo = correo.strip()
            if not validar_correo(correo):
                f_log.write(f"{pdf},{correo},fallido (correo inválido)\n")
                continue
            if not os.path.exists(pdf):
                f_log.write(f"{pdf},{correo},fallido (archivo no encontrado)\n")
                continue

            exito = enviar_correo(correo, pdf)
            if exito:
                f_log.write(f"{pdf},{correo},exitoso\n")
            else:
                f_log.write(f"{pdf},{correo},fallido\n")
                pendientes_nuevos.append(fila)

    # Reescribir pendientes_envio.csv con los que fallaron para reintentar luego
    with open(PENDIENTES, 'w', newline='', encoding='utf-8') as f_out:
        escritor = csv.writer(f_out)
        escritor.writerows(pendientes_nuevos)

    print("Proceso de envío finalizado.")

if __name__ == "__main__":
    main()
