# Creado por Luis Clavijo Fuentes (WhitesoundCl)
# Licencia MIT

import json
from datetime import datetime

json_cargado = json.load(open('cache.json'))
sala = ""
for horario in json_cargado:
    if "hora_inicio" in horario["data"]:
        horario_asig_inicio = datetime.strptime(horario["data"]["fecha"] + " " + horario["data"]["hora_inicio"],
                                                '%d/%m/%Y %H:%M')
        horario_asig_termino = datetime.strptime(horario["data"]["fecha"] + " " + horario["data"]["hora_termino"],
                                                 '%d/%m/%Y %H:%M')
        if horario_asig_inicio <= datetime.today() <= horario_asig_termino:
            sala = horario["data"]["sala"][len(horario["data"]["sala"]) - 3:]

if len(sala) is 3:
    print("["+sala+"]")
else:
    print("[N/A]")
