"""
3T — DIAGNOSTICO POST-HOC. SIN VALOR CONFIRMATORIO.

El veredicto preregistrado ya esta cerrado en NO (ver analiza_3T.py). Esto solo responde
a la pregunta mecanica "por que", levantando los DOS confusores que el PREREGISTRO
anticipo por escrito ANTES de correr:

  PH1  nkmax=300 (240 divisiones disponibles en vez de 60), wclip=3.0
       -> quita el agotamiento del pool, deja la saturacion de canales.
  PH2  nkmax=300, wclip=30.0
       -> quita ademas la saturacion (Wp/Wn dejan de fijarse en el techo).

Si C3 sigue sin separar con ambos levantados, el fallo es de la DIRECCION de la regla.
Si C3 separa pero C3C (canal de ruido) separa igual, la regla separa sin discriminar
informacion y la seleccion, si la hay, ocurre aguas abajo en la capa de valor.
No se toca theta, ema ni paso.
"""
import sys, os
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corre_3T as c

if __name__ == '__main__':
    print("\n########## PH1: pool 300, clip 3.0 (solo se levanta el agotamiento) ##########")
    c.main(arms=['C1', 'C3', 'C3C'], tag='PH1', extra=dict(nkmax=300, wclip=3.0))
    print("\n########## PH2: pool 300, clip 30.0 (se levantan los dos confusores) ##########")
    c.main(arms=['C1', 'C3', 'C3C'], tag='PH2', extra=dict(nkmax=300, wclip=30.0))
