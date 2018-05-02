# Creado por Luis Clavijo Fuentes (WhitesoundCl)
# Licencia MIT

import os.path
import getpass
import json
import re
import time
import argparse
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


# -- Variables ----#
archivo_cache = 'cache.json'
geckodriver = os.path.dirname(os.path.abspath(__file__)) + "/geckodriver"
url_login_inacap = "https://adfs.inacap.cl/adfs/ls/?wtrealm=https://siga.inacap.cl/sts/&wa=wsignin1.0&wreply=https" \
                   "://siga.inacap.cl/sts/&wctx=https%3a%2f%2fadfs.inacap.cl%2fadfs%2fls%2f%3fwreply%3dhttps%3a%2f" \
                   "%2fwww.inacap.cl%2ftportalvp%2fintranet-alumno%26wtrealm%3dhttps%3a%2f%2fwww.inacap.cl%2f "
url_inacap_horario = "https://www.inacap.cl/tportalvp/procesar_link.php?idc=MISASIGNAT&url=https://siga3.inacap.cl" \
                     "/Inacap.Siga.Horarios/Horario.aspx "


# -----Funciones-----#
def esperar_web(driver,  intentos, condicion, nombre, mensaje):
    contador = 0
    while contador < intentos:
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((condicion, nombre)))
            return True
        except:
            print(mensaje)

        contador += 1
    return False


def recargar_cache():
    print("Actualizando caché de horario, por favor espera..")
    options = Options()
    options.add_argument("--headless")  # Comenta esta linea para iniciar el navegador con GUI
    driver = webdriver.Firefox(firefox_options=options, executable_path=geckodriver)
    driver.get(url_login_inacap)

    assert "Sign In" in driver.title
    # Ingresa los datos en los formularios
    elem = driver.find_element_by_name("UserName")
    elem.clear()
    elem.send_keys(getpass.getpass("Rut INACAP(sin puntos):"))
    elem = driver.find_element_by_name("Password")
    elem.clear()
    elem.send_keys(getpass.getpass("Contraseña INACAP:"))
    elem.send_keys(Keys.RETURN)

    # Se toma el tiempo de duración de todo el proceso
    start = time.time()

    # Espera por el ambiente alumno
    if not esperar_web(driver, 5, By.CLASS_NAME, "aplicacionesAlumno", "."):
        print("La página está tardando en responder. ¿Credenciales de alumno correctas?")
        driver.close()
        exit(-1)

    driver.get(url_inacap_horario)

    # Espera por la página del horario:
    if not esperar_web(driver, 5, By.ID, "frmhorario", "."):
        print("La página no responde, intentalo de nuevo más tarde.")
        driver.close()
        exit(-1)

    # Se roba el horario contenido en el json en la página
    json_string = "".join(re.findall('\/\/<!\[CDATA\[\n.+\/\/]]>', driver.page_source, re.MULTILINE))

    # Ya no se necesita que el driver mantenga abierto el navegador
    driver.close()

    print("Limpiando información de horario (Esto suele tardar un poco)")

    # Se limpia el string para pasarlo a un formato json válido.
    regex_borrar_comienzo = r"\b.+,events:"
    regex_borrar_final = r",eventRender:.+"

    match = re.findall(regex_borrar_comienzo, json_string, re.IGNORECASE)
    json_string = json_string.replace("".join(match), "")

    match = re.findall(regex_borrar_final, json_string, re.IGNORECASE)
    json_string = json_string.replace("".join(match), "")
    json_string = json_string.replace("//<![CDATA[\n", "")

    # Se carga el string con formato json para posteriormente guardarlo.
    json_cargado = json.loads(json_string)

    # Guardar el horario en 'cache.json'
    with open(archivo_cache, 'w') as outfile:
        json.dump(json_cargado, outfile)

    # Imprimir el tiempo total que costó realizar la operacion.
    print("Cache actualizado en " + str(time.time() - start) + " Segundos.")


def mostrar_horario(dias):

    json_cargado = json.load(open(archivo_cache))
    dias = int(dias)

    # En caso de que el usuario ingrese un número negativo
    fecha = date.today() if dias > 0 else date.today() - timedelta(days=abs(dias))
    fecha_limite = fecha + timedelta(days=dias) if dias > 0 else date.today()

    # Imprimir horario
    for horario in json_cargado:
        # Split del string de fecha para transformarla en un objeto date
        spl_asignatura = list(map(int, str(horario["data"]["fecha"]).split("/")))
        fecha_asignatura = date(spl_asignatura[2], spl_asignatura[1], spl_asignatura[0])

        # Imprimir días feriados
        if horario["description"] == "Feriado":

            if fecha <= fecha_asignatura < fecha_limite:
                print("[{fecha}] FERIADO".format(fecha=horario["data"]["fecha"]))

        # Imprimir el horario de las clases
        if "hora_inicio" in horario["data"]:

            if fecha <= fecha_asignatura < fecha_limite:
                print("[{fecha}] {nombre} de {inicio} a {termino} en {sala}".format(
                    fecha=horario["data"]["fecha"],
                    nombre=horario["data"]["asignatura"],
                    inicio=horario["data"]["hora_inicio"],
                    termino=horario["data"]["hora_termino"],
                    sala=horario["data"]["sala"]
                ))


def mostrar_horario_completo():
    json_cargado = json.load(open(archivo_cache))
    for horario in json_cargado:
        if "hora_inicio" in horario["data"]:
            print("[{fecha}] {nombre} de {inicio} a {termino} en {sala}".format(
                fecha=horario["data"]["fecha"],
                nombre=horario["data"]["asignatura"],
                inicio=horario["data"]["hora_inicio"],
                termino=horario["data"]["hora_termino"],
                sala=horario["data"]["sala"]
            ))


# -----Fin de funciones----#

# Paso de parametros desde la terminal
parser = argparse.ArgumentParser(description="Muestra el horario de alumno de INACAP en consola.\n"
                                             "Sin argumentos muestra el horario del día.")
grupo = parser.add_mutually_exclusive_group(required=False)
grupo.add_argument('-a', '--actualizar', help='Renueva el cache del horario', action='store_true')
grupo.add_argument('-s', '--semana', help='Muestra el horario en los siguientes 7 días', action='store_true')
grupo.add_argument('-d', '--dias', help='Muestra el horario en los siguientes N días', metavar="N")
grupo.add_argument('-t', '--todos', help='Muestra todo el horario', action='store_true')

args = parser.parse_args()

# Si el archivo de caché no existe al iniciar el programa, se intentará obtener.
if args.actualizar or not os.path.isfile(archivo_cache):
    recargar_cache()

elif args.semana:
    mostrar_horario(7)

elif args.dias is not None:
    mostrar_horario(args.dias)

elif args.todos:
    mostrar_horario_completo()

else:
    mostrar_horario(1)

exit(0)
