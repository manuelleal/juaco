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
    import sys as _s
    que = _s.argv[1] if len(_s.argv) > 1 else 'todo'
    if que in ('todo', '12'):
        print("\n########## PH1: pool 300, clip 3.0 (solo se levanta el agotamiento) ##########")
        c.main(arms=['C1', 'C3', 'C3C'], tag='PH1', extra=dict(nkmax=300, wclip=3.0))
        print("\n########## PH2: pool 300, clip 30.0 (se levantan los dos confusores) ##########")
        c.main(arms=['C1', 'C3', 'C3C'], tag='PH2', extra=dict(nkmax=300, wclip=30.0))
    if que in ('todo', '3'):
        # PH3: pool ORIGINAL de v7 (90). Unica constante levantada: el techo de Wp/Wn.
        print("\n########## PH3: pool 90 (el de v7, intacto), clip 30.0 ##########")
        c.main(arms=['C1', 'C2', 'C3', 'C3C'], tag='PH3', extra=dict(nkmax=90, wclip=30.0))
    if que in ('todo', 'barrido'):
        # Barrido del techo con el pool de v7: si el bloqueo es una CARRERA entre la
        # division y la saturacion, el exito debe crecer de forma monotona con el techo.
        for wc in (3.0, 4.5, 6.0, 9.0, 15.0, 30.0):
            print(f"\n########## BARRIDO techo Wp/Wn = {wc} (pool 90) ##########")
            c.main(arms=['C3'], tag=f'BAR{wc:g}', extra=dict(nkmax=90, wclip=wc))
