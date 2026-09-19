import json
import os
from pathlib import Path

def analizar_muerte(data):
    """Analiza una muerte y sugiere curita."""
    cuerpo = data['cuerpo']
    causa = data['causa']
    edad = data['edad']
    hijos = data['hijos']
    conectado = data['conectado']
    dote = data['dote']
    rep_umbral = data['rep_umbral']
    hereda = data['hereda']
    mordidas = data['mordidas']
    nodo_n = data['nodo_n']
    
    # Analizar patrones de mordidas
    muertes_anteriores = data['muertes'] - 1
    mordidas_con_R_neg = [m for m in mordidas if m[3] < 0]  # R negativo
    
    # Lógica de decisión
    if cuerpo <= 3:
        # Primeros cuerpos: conexión y alimentación
        if conectado == 0 and cuerpo == 3:
            return 'a', f"Cuerpo {cuerpo} murió joven ({edad}, {hijos} hijos). Vidas decrecen. Todos desconectados del nodo. CONECTAR (a) permite aprender."
        if cuerpo == 1:
            return 'c', f"Fundador murió ({edad}, {hijos} hijos, dote {dote} vs umbral {rep_umbral}). DOTE MAYOR (c) para siguiente."
        if cuerpo == 2:
            return 'b', f"Cuerpo {cuerpo} murió joven ({edad}) repitiendo bites letales con R=-3.0. MIEDO (b) para advertir."
    
    # Regla general: si edad es muy corta y hay hijos=0, problema de reproducción
    if edad < 100 and hijos == 0:
        if dote < rep_umbral - 0.05:
            # Dote está lejos del umbral
            return 'c', f"Edad {edad}, {hijos} hijos, dote {dote} << umbral {rep_umbral}. DOTE (c) para reproducir."
        elif dote < rep_umbral and rep_umbral > 0.85:
            # Umbral muy alto
            return 'd', f"Edad {edad}, {hijos} hijos, umbral {rep_umbral} alto. UMBRAL (d) para reproducir barato."
    
    # Si hay muchas mordidas con R negativo repetido
    if len(mordidas_con_R_neg) >= 2 and conectado == 0:
        return 'b', f"Cuerpo {cuerpo} edad {edad}: {len(mordidas_con_R_neg)} bites letales. MIEDO (b) registra."
    
    # Si ya conectado y faltan muchas muertes antes de mejorar
    if conectado == 1 and cuerpo < 15:
        return 'e', f"Cuerpo {cuerpo} edad {edad} conectado. HEREDA (e) para transmitir valores."
    
    # Default: hacer nada (f) es riesgoso; intentar algo
    if edad < 50:
        return 'd', f"Cuerpo {cuerpo} muy joven ({edad}). UMBRAL (d) reduce costo reproducción."
    
    return 'f', f"Cuerpo {cuerpo} edad {edad}: mantener línea base."

# Procesar muertes 4-20
alma_dir = Path("alma_io")
for n in range(4, 21):
    pregunta_file = alma_dir / f"alma_pregunta_807_{n}.json"
    respuesta_file = alma_dir / f"alma_respuesta_807_{n}.json"
    
    if respuesta_file.exists():
        print(f"Muerte {n}: ya procesada")
        continue
    
    if not pregunta_file.exists():
        print(f"Muerte {n}: archivo no existe aún")
        continue
    
    try:
        with open(pregunta_file, 'r') as f:
            data = json.load(f)
        
        curita, motivo = analizar_muerte(data)
        
        # Limitar motivo a 300 caracteres
        if len(motivo) > 300:
            motivo = motivo[:297] + "..."
        
        respuesta = {"curita": curita, "motivo": motivo}
        
        with open(respuesta_file, 'w') as f:
            json.dump(respuesta, f)
        
        print(f"Muerte {n}: curita={curita}")
    except Exception as e:
        print(f"Muerte {n}: error - {e}")

print("Procesadas muertes disponibles.")
