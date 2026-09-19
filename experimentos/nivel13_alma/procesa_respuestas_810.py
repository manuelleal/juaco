#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path

BRAZO = "SIN_NODO"
SEMILLA = 810
BASE_DIR = Path("alma_io")

def analizar_muerte(data):
    """
    Analiza los datos de un cuerpo muerto y elige una curita.

    Retorna: (curita, motivo)
    """
    cuerpo = data.get("cuerpo")
    t = data.get("t")  # tiempo de muerte = edad
    causa = data.get("causa")
    edad = data.get("edad")
    hijos = data.get("hijos")
    conectado = data.get("conectado")
    dote = data.get("dote")
    rep_umbral = data.get("rep_umbral")
    hereda = data.get("hereda")
    exposiciones = data.get("exposiciones", [])
    mordidas = data.get("mordidas", [])
    descendientes = data.get("descendientes")
    muertes = data.get("muertes")
    R0 = data.get("R0")
    menu = data.get("menu", [])

    # Análisis de mordidas
    num_mordidas = len(mordidas)

    # Contar mordidas con R negativo (dañino)
    mordidas_daninas = [m for m in mordidas if len(m) > 3 and m[3] < 0]
    num_daninas = len(mordidas_daninas)

    # Contar mordidas sin morder (nunca mordió)
    mordio = num_mordidas > 0

    # Análisis de reproducción
    buen_R0 = R0 >= 1.0

    # Razonamiento para elegir curita
    # Disponibles: c (DOTE MAYOR), d (BAJAR UMBRAL), e (HEREDAR), f (NADA)
    # NO disponibles: a (CONECTAR NODO), b (SUBIR MIEDO)

    # Estrategia:
    # 1. Si murió muy joven sin hijos -> subir dote (c) o bajar umbral (d)
    # 2. Si murió con muchas mordidas dañinas -> heredar (e)
    # 3. Si R0 es bajo -> bajar umbral (d) para más reproducción
    # 4. Si está funcionando bien -> f

    curita = "f"

    if edad < 100 and hijos == 0:
        # Murió muy joven sin reproducirse
        if num_daninas > 2:
            curita = "e"
            motivo = f"Cuerpo {cuerpo} murió joven ({edad} pasos) sin hijos. {num_daninas} mordidas dañosas repetidas (R<0). Heredar permite aprender a evitarlas."
        else:
            curita = "c"
            motivo = f"Cuerpo {cuerpo} murió joven ({edad} pasos) sin reproducirse. Aumentar dote de {dote} permite vivir más."
    elif edad < 100:
        # Murió joven pero tuvo algunos hijos
        if num_daninas > 3:
            curita = "e"
            motivo = f"Cuerpo {cuerpo} murió a los {edad} pasos con {hijos} hijos. {num_daninas} mordidas a estímulos dañosos (R<0) muestran falta de aprendizaje. Heredar valores ayuda."
        elif R0 < 0.5:
            curita = "d"
            motivo = f"Cuerpo {cuerpo} murió joven ({edad} pasos), R0={R0}. Bajar umbral de reproducción de {rep_umbral} facilita más descendencia."
        else:
            curita = "c"
            motivo = f"Cuerpo {cuerpo} murió a los {edad} pasos. Aumentar dote facilita alcanzar la reproducción."
    elif not mordio:
        # Nunca mordió nada - falta de exploración
        curita = "e"
        motivo = f"Cuerpo {cuerpo} murió a los {edad} pasos sin morder. Heredar permite que el siguiente tenga impulsos aprendidos."
    elif num_daninas >= 2:
        # Múltiples mordidas dañinas -> transmitir conocimiento
        curita = "e"
        motivo = f"Cuerpo {cuerpo} murió tras {edad} pasos. {num_daninas} mordidas dañosas (R<0) desde el inicio. Heredar valores permite evitar el patrón."
    elif R0 < 0.7:
        # Reproducción débil
        curita = "d"
        motivo = f"Cuerpo {cuerpo}: edad={edad}, R0={R0}. Bajar rep_umbral de {rep_umbral} permite reproducirse con menos recursos."
    else:
        # Caso general: está más o menos bien
        curita = "f"
        motivo = f"Cuerpo {cuerpo} vivió {edad} pasos, R0={R0}, {hijos} hijos. Sin problemas graves detectados."

    return curita, motivo

def procesar_pregunta(n):
    """Procesa la pregunta n y escribe la respuesta."""
    pregunta_file = BASE_DIR / f"alma_pregunta_{SEMILLA}_{BRAZO}_{n}.json"
    respuesta_file = BASE_DIR / f"alma_respuesta_{SEMILLA}_{BRAZO}_{n}.json"

    # Verificar que no existe respuesta ya
    if respuesta_file.exists():
        return True  # Ya respondida

    # Esperar a que exista la pregunta
    waited = 0
    while not pregunta_file.exists() and waited < 600:
        time.sleep(1)
        waited += 1

    if not pregunta_file.exists():
        return False  # Timeout

    # Leer la pregunta
    with open(pregunta_file, 'r') as f:
        data = json.load(f)

    # Analizar y elegir curita
    curita, motivo = analizar_muerte(data)

    # Validar que esté en el menú
    menu = data.get("menu", [])
    if curita not in menu:
        # Si la curita no está disponible, elegir la primera del menú
        print(f"Warning: curita {curita} no en menú {menu}, usando {menu[0]}")
        curita = menu[0]

    # Escribir respuesta (máx 300 caracteres en motivo)
    motivo = motivo[:300]
    respuesta = {"curita": curita, "motivo": motivo}

    with open(respuesta_file, 'w') as f:
        json.dump(respuesta, f)

    print(f"[{n}] Respondida: curita={curita}")
    return True

def main():
    print(f"Procesando brazo {BRAZO}, semilla {SEMILLA}")

    respondidas = 0
    for n in range(1, 21):
        if procesar_pregunta(n):
            respondidas += 1
        else:
            print(f"Pregunta {n} no apareció después de 10 minutos")
            break

        # Pequeña pausa entre preguntas
        time.sleep(0.5)

    print(f"Total respondidas: {respondidas}/20")

if __name__ == "__main__":
    main()
