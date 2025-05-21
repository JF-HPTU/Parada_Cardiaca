import datetime 
from datetime import datetime, timedelta

equipoUser = GetVar('equipoUser')
fecha_actual=datetime.now().strftime("%d-%m-%Y %H:%M:%S")

#Rutas 

ruta_log = f"C:/Users/{equipoUser}/Desktop/Produccion/Parada_Cardiaca/Logs/log.txt"
ruta_consulta = f"C:/Users/{equipoUser}/Desktop/Produccion/Parada_Cardiaca/Includes/consulta.py"
correos_enviar = "gestiontrasplantes@hptu.org.co" # centralreferencia no se usara
correo_prueba = "jfgiraldo@hptu.org.co"
ruta_mail = f"C:/Users/{equipoUser}/Desktop/Produccion/Parada_Cardiaca/Includes/relay_sin_correo.py"


#Oracle
sesion = "ConnOracle"
usuario = "CNX_BUS"
password = "u6pYGXNA"
DNS = "scan-redhptu/HPTU"

#Oracle Desarrollo Pruebas
usuario_d = "BASDATHPTUDLLO"
password_d = "Pr0y3ct0-jun16"
DNS_d = "172.20.29.250/HPTUDLLO"


SetVar("fecha_actual", fecha_actual)
SetVar("ruta_log", ruta_log)
SetVar("ruta_consulta", ruta_consulta)
SetVar("ruta_mail", ruta_mail)

SetVar("correos_enviar", correos_enviar)
SetVar("correo_prueba", correo_prueba)

SetVar("sesion", sesion)
SetVar("usuario", usuario)
SetVar("password", password)
SetVar("DNS", DNS)

SetVar("usuario_d", usuario_d)
SetVar("password_d", password_d)
SetVar("DNS_d", DNS_d)
