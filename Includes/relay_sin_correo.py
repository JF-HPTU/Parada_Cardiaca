import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


correo_prueba = GetVar('correo_prueba')
correos_enviar = GetVar('correos_enviar')
pacientes = eval(GetVar('pacientes'))



def convertir_pacientes(pacientes):
    """Convierte una lista de tuplas en una lista de diccionarios si es necesario"""
    if pacientes and isinstance(pacientes[0], tuple):  # Si el primer elemento es una tupla, lo convertimos
        return [
            {"TipoDocumento": p[0], "Documento": p[1], "Nombre": p[2], "Historia": p[3], 
             "Ubicacion": p[4], "Habitacion": p[5], "FechaNacimiento": p[6], "Edad": p[7],
             "DiagnosticoPrincipal": p[8], "DiagnosticoSecundario": p[9], "FechaNota": p[10]} 
            for p in pacientes
        ]
    return pacientes  # Si ya es lista de diccionarios, la retornamos sin cambios

# Convertir pacientes antes de procesarlos
pacientes = convertir_pacientes(pacientes)

class Observer:
    def __init__(self, name, email):
        self.name = name
        self.email = email.split(",")  # Convertimos la cadena de correos en lista

    @staticmethod
    def generar_tabla(pacientes):
        """Genera una tabla en HTML con los datos de los pacientes"""
        if not pacientes:
            return "<tr><td colspan='11'>No hay pacientes en la lista</td></tr>"
        
        filas = "".join(f"""
            <tr>
                <td>{paciente['TipoDocumento']}</td>
                <td>{paciente['Documento']}</td>
                <td>{paciente['Nombre']}</td>
                <td>{paciente['Historia']}</td>
                <td>{paciente['Ubicacion']}</td>
                <td>{paciente['Habitacion']}</td>
                <td>{paciente['FechaNacimiento']}</td>
                <td>{paciente['Edad']}</td>
                <td>{paciente['DiagnosticoPrincipal']}</td>
                <td>{paciente['DiagnosticoSecundario']}</td>
                <td>{paciente['FechaNota']}</td>
            </tr>
        """ for paciente in pacientes)
        
        return filas

    def send_email(self, pacientes, file_path=None):
        """Envía un correo electrónico con la lista de pacientes."""
        smtp_server = "smtp-relay.gmail.com"
        smtp_port = 587
        sender_email = "noreply@hptu.org.co"
        subject = "Reporte parada cardiaca"

        # Generar la tabla de pacientes
        contenido_tabla = self.generar_tabla(pacientes)

        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Correo Pacientes</title>
        </head>
        <body style="font-family: Century Gothic;">
            <table width="100%" border="0">
                <tr>
                    <td align="right">
                        <img width="20%" src="https://hptu.org/cdn/shop/files/Untitled_design_47_420x.png?v=1704730038" alt="Hospital Pablo Tobon Uribe">
                    </td>
                </tr>
                <tr>
                    <td>
                        <p><em>Cordial saludo,</em></p>
                        <p>A continuacion encontrara ilustrado los pacientes para reporte de parada cardiaca.</p>
                        <table border='1' style='font-family: century gothic; border: 1px solid #515421;' class='table-class'>
                            <tr style="background-color: #f2f2f2;">
                                <th>Tipo de documento</th>
                                <th>Documento</th>
                                <th>Nombre</th>
                                <th>Historia</th>
                                <th>Ubicacion</th>
                                <th>Habitacion</th>
                                <th>Fecha de nacimiento</th>
                                <th>Edad</th>
                                <th>Diagnostico principal</th>
                                <th>Diagnostico secundario</th>
                                <th>Fecha nota</th>
                            </tr>
                            {contenido_tabla}
                        </table>
                        <p><em>Cordialmente,</em></p>
                        <h3 style="font-size: 12px;"><strong>Hospital Pablo Tobon Uribe</strong></h3>
                    </td>
                </tr>
                <tr>
                    <td>
                        <p><em><strong>Nota:</strong> Este es un correo enviado de forma automatica, por favor no responda.</em></p>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <img width="40%" src="https://i.ytimg.com/vi/Quci-reBBkE/mqdefault.jpg" alt="Hospital Pablo Tobon Uribe">
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        # Crear el mensaje de correo
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(self.email)
        msg["Subject"] = subject
        msg.attach(MIMEText(body.encode("utf-8"), "html", "utf-8"))

        # Adjuntar el archivo si se proporciona la ruta
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
                    msg.attach(part)
                print(f"Archivo adjunto: {file_path}")
            except Exception as e:
                print(f"Error al adjuntar el archivo: {e}")

        # Enviar el correo
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(sender_email, self.email, msg.as_string())
            print(f"Correo enviado a {self.email}")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    observer = Observer("Notificación HPTU", correo_prueba)
    observer.send_email(pacientes)