#!/usr/bin/env python3
"""
Procesa las 20 muertes del linaje ALMA semilla 808.
Lee cada pregunta, razona, escribe la respuesta.
"""

import json
import time
import sys
from pathlib import Path

DIRECTORIO = Path("C:/Users/User/Documents/PROYECTOS/JUACO/bundle/experimentos/nivel13_alma")
ALMA_IO = DIRECTORIO / "alma_io"

def leer_pregunta(n):
    """Lee alma_pregunta_808_<n>.json"""
    archivo = ALMA_IO / f"alma_pregunta_808_{n}.json"
    if not archivo.exists():
        return None
    with open(archivo, 'r') as f:
        return json.load(f)

def escribir_respuesta(n, curita, motivo):
    """Escribe alma_respuesta_808_<n>.json"""
    archivo = ALMA_IO / f"alma_respuesta_808_{n}.json"
    data = {"curita": curita, "motivo": motivo}
    with open(archivo, 'w') as f:
        json.dump(data, f)

def analizar_muerte(pregunta, n):
    """
    Analiza la pregunta y elige una curita.
    Retorna (curita, motivo_string).
    """
    causa = pregunta.get("causa", "?")
    edad = pregunta.get("edad", 0)
    hijos = pregunta.get("hijos", 0)
    conectado = pregunta.get("conectado", 0)
    dote = pregunta.get("dote", 0.6)
    rep_umbral = pregunta.get("rep_umbral", 1.0)
    hereda = pregunta.get("hereda", "nada")
    R0 = pregunta.get("R0", 0.0)
    mordidas = pregunta.get("mordidas", [])
    descendientes = pregunta.get("descendientes", 0)
    fundador = pregunta.get("fundador", 0)

    # Últimas mordidas con R negativo
    mordidas_negativas = [m for m in mordidas if m[3] < -2.0]

    # Patrón de muerte
    razon = ""
    curita = "f"  # por defecto, nada

    if len(mordidas) == 0:
        # Nunca mordió nada
        razon = f"Nunca mordió (edad {edad}). Opción (e) para que el siguiente herede Wps/Wns."
        curita = "e"
    elif edad < 100 and hijos < 1:
        # Joven, sin descendencia; probablemente hambre/sed
        razon = f"Murió joven ({edad} pasos) sin reproducirse ({hijos} hijos). Opción (c) DOTE para próximo."
        curita = "c"
    elif len(mordidas_negativas) >= 2:
        # Patrón repetido de castigos fuertes
        ultima_negativa = mordidas_negativas[-1] if mordidas_negativas else None
        if ultima_negativa:
            estim = ultima_negativa[1]
            R = ultima_negativa[3]
            nec = ultima_negativa[2]
            razon = f"Murió atrapado mordiendo {estim} (R={R}, nec={nec}) repetido. Opción (b) MIEDO para evitarlo."
            curita = "b"
        else:
            razon = f"Múltiples castigos fuertes. Opción (b) para escribir patrón de miedo."
            curita = "b"
    elif conectado == 0 and fundador == 0:
        # No estaba conectado; siguiente debería estarlo
        razon = f"Cuerpo desconectado (edad {edad}). Opción (a) CONECTAR al nodo para siguiente."
        curita = "a"
    elif descendientes == 0 and edad > 200:
        # Vivió mucho pero sin reproducirse; mundo tal vez muy caro
        razon = f"Larga vida ({edad} pasos) pero sin hijos ({hijos}). Opción (d) UMBRAL para reproducción."
        curita = "d"
    else:
        # Caso genérico: elige based on último patrón
        if mordidas:
            ultima = mordidas[-1]
            estim = ultima[1]
            R = ultima[3]
            if R < -2.0:
                razon = f"Última mordida: {estim} con R={R}. Opción (b) para escribir miedo."
                curita = "b"
            else:
                razon = f"Cuerpo {n}: edad {edad}, {hijos} hijos. Opción (f) NADA por defecto."
                curita = "f"
        else:
            razon = f"Sin mordidas registradas. Opción (f)."
            curita = "f"

    # Truncar motivo a 300 caracteres
    if len(razon) > 300:
        razon = razon[:297] + "..."

    return curita, razon

def main():
    """Procesa 20 muertes"""
    vidas = []
    curitas_str = ""
    respondidas = 0

    print(f"Iniciando procesamiento de 20 muertes...")

    for n in range(1, 21):
        print(f"\n--- Cuerpo {n} ---")

        # Esperar a que aparezca la pregunta (máximo 60 segundos)
        pregunta = None
        for intento in range(6):  # 6 x 10 = 60 segundos
            pregunta = leer_pregunta(n)
            if pregunta:
                break
            print(f"  Esperando pregunta {n}... intento {intento+1}/6")
            time.sleep(10)

        if not pregunta:
            print(f"  ERROR: No se recibió pregunta para cuerpo {n}")
            break

        # Analizar y responder
        edad = pregunta.get("edad", 0)
        vidas.append(edad)
        curita, motivo = analizar_muerte(pregunta, n)

        # Escribir respuesta
        escribir_respuesta(n, curita, motivo)
        respondidas += 1
        curitas_str += curita

        print(f"  Edad: {edad}, Causa: {pregunta.get('causa', '?')}")
        print(f"  Curita elegida: {curita}")
        print(f"  Motivo: {motivo[:80]}...")
        print(f"  Respondida.")

    print(f"\n=== RESUMEN ===")
    print(f"Cuerpos respondidos: {respondidas}")
    print(f"Vidas: {vidas}")
    print(f"Curitas: {curitas_str}")

    return respondidas, vidas, curitas_str

if __name__ == "__main__":
    respondidas, vidas, curitas_str = main()
