"""BLOQUE ALMA (nivel 13) — el bucle del alma, la interfaz por archivos y los dos controles automaticos.

MISION: llegar a la AGI por este camino — un organismo minimo con reglas locales que aprende, sobrevive, se
comunica y se reproduce; con evidencia preregistrada. Hoy: un alma externa que parcha al cuerpo cada vez que
muere, con un nodo central de conocimiento; el alma es el BUSCADOR, no el resultado.

Ejecuta PREREGISTRO_alma.md (escrito ANTES de correr; su sha va en el meta) y MENU_curitas.md (el menu cerrado).
Instrumento: organismo_alma.py (por anclas desde organismo_vivo_h1.py 9e99ff87b5e2db1e, que aqui SOLO SE LEE).
Reutiliza mini_vivo.py y corre_vivo_rep(.2).py de nivel11 (CUERPO, BRAZOS, MED, med, A12, h16, N) SIN copiarlos.

UN PROCESO, SIN Pool (regla 3 de EQUIPO.md). T por cuerpo <= 100 000 por construccion (T total <= 100 000).

    python experimentos/nivel13_alma/corre_alma.py --alma interfaz  --sem 801 --muertes 10
    python experimentos/nivel13_alma/corre_alma.py --alma aleatoria --sem 801 --muertes 10
    python experimentos/nivel13_alma/corre_alma.py --alma ninguna   --sem 801 --muertes 10

LA INTERFAZ (el alma NO se puede llamar desde Python en este repo: no hay cliente de modelo).
  Modo `interfaz`, POR REPETICION DETERMINISTA (no bloquea ningun proceso):
    1. la corrida avanza; en la muerte n busca `alma_io/alma_respuesta_<sem>_<n>.json`
    2. si NO existe: escribe `alma_io/alma_pregunta_<sem>_<n>.json` (el resumen de la causa) y PARA la corrida
    3. el agente-alma lee la pregunta, razona, y escribe la respuesta {"curita": "a".."f", "motivo": "..."}
    4. se vuelve a lanzar el mismo comando: el mundo es determinista, se repite bit a bit hasta la muerte n+1
  Cuando estan las `--muertes` respuestas, la corrida termina y escribe los DATOS CRUDOS (ERR-54) en
  `alma_humo_<modo>_s<sem>_<fecha>.json` ANTES de imprimir ninguna tabla.
  Con `--espera S` en vez de repetir, el proceso ESPERA S segundos por cada respuesta (util si el alma corre a la
  vez). Las dos rutas producen exactamente el mismo JSON.

VOCABULARIO (regla 6): "curita", "nodo central", "exposicion sin consecuencia", "cuerpo", "linaje", "R0 del
linaje" (descendientes/muertes). NO se dice "evoluciona", "aprende de sus errores", "decide", "quiere" del alma:
el alma es un agente externo que elige de un menu cerrado, y eso es lo unico que se mide.
"""
import argparse, json, os, sys, time, platform, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [AQUI, N11, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import numpy as np
import mini_vivo as MV
import corre_vivo_rep as C1        # BRAZOS, MED, med, A12, h16, N, razon: NO se copian
import corre_vivo_rep2 as C2       # MED2: NO se copia
import organismo_alma as AL

T = 100000
DOTE = 0.6
MENU = ('a', 'b', 'c', 'd', 'e', 'f')
IO = os.path.join(AQUI, 'alma_io')
SHA_ESPERADOS = dict(v14='feefc88b1fd8d434', vivo='20c0961c79de8825', rep='aa823d56c2d4213c',
                     rep2='96feb4918dc5d694', h1='9e99ff87b5e2db1e')

MED_H1 = dict(C2.MED2, h1=1)   # reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0, rep2=1, rep2_regalo=600, h1=1
# EL CUERPO: CUELLO_MIN, el mismo brazo en el que H-1 midio R0 0.148 (hereda nada) y 0.160 (hereda M1)
BRAZO = dict(C1.BRAZOS['CUELLO_MIN']) | MED_H1 | dict(muerte_real=1, hereda='nada', dote=DOTE)


class PreguntaPendiente(Exception):
    def __init__(self, n, ruta):
        super().__init__(f"pregunta {n} sin responder: {ruta}")
        self.n, self.ruta = n, ruta


# ---------------------------------------------------------------- las tres almas
def alma_interfaz(sem, espera=0.0):
    """El alma es un AGENTE EXTERNO. Aqui solo esta el buzon."""
    os.makedirs(IO, exist_ok=True)

    def fn(res):
        n = res['cuerpo']
        rp = os.path.join(IO, f'alma_respuesta_{sem}_{n}.json')
        rq = os.path.join(IO, f'alma_pregunta_{sem}_{n}.json')
        if not os.path.exists(rp):
            json.dump(res, open(rq, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            if espera <= 0:
                raise PreguntaPendiente(n, rq)
            t0 = time.time()
            while not os.path.exists(rp):
                if time.time() - t0 > espera:
                    raise PreguntaPendiente(n, rq)
                time.sleep(0.25)
        d = json.load(open(rp, encoding='utf-8'))
        if d.get('curita') not in MENU:
            raise SystemExit(f"ALMA: {rp} trae curita {d.get('curita')!r}, fuera del MENU CERRADO {MENU}")
        return d
    return fn


def alma_aleatoria(sem):
    """CONTROL: una curita AL AZAR del menu, con rng PROPIO (850000 + 1000000*sem). No toca el rng del mundo."""
    rg = np.random.default_rng(850000 + 1000000 * sem)

    def fn(res):
        c = MENU[int(rg.integers(len(MENU)))]
        return {'curita': c, 'motivo': 'control: curita al azar del menu cerrado (rng propio 850000+1000000*sem)'}
    return fn


def alma_ninguna(sem):
    """CONTROL: sin curita. El runner ademas apaga el nodo (nodo=0): sin curita y sin nodo."""
    def fn(res):
        return {'curita': 'f', 'motivo': 'control: sin curita'}
    return fn


ALMAS = {'interfaz': alma_interfaz, 'aleatoria': alma_aleatoria, 'ninguna': alma_ninguna}


# ---------------------------------------------------------------- corrida
def corre(modo, sem, muertes, espera=0.0, T_max=T):
    kw = dict(BRAZO, alma_muertes=muertes, nodo=(0 if modo == 'ninguna' else 1))
    fn = alma_interfaz(sem, espera) if modo == 'interfaz' else ALMAS[modo](sem)
    t0 = time.time()
    r = AL.run(sem, T=T_max, alma=fn, **kw)
    r['_segundos'] = round(time.time() - t0, 2)
    return r, kw


def tabla(r):
    """Vida por cuerpo, curita elegida, hijos y R0 acumulado del linaje. Los cuerpos COMPLETOS son len(curitas)."""
    cur = r['curitas']; vidas = r['vidas_cuerpo']; desc = r['desc_cuerpo']
    filas, ac_d, ac_m = [], 0, 0
    for i, c in enumerate(cur):
        ac_m += 1; ac_d += desc[i]
        filas.append(dict(cuerpo=i + 1, vida=vidas[i], causa=c[8], hijos=desc[i], curita=c[1],
                          dote=c[3], umbral=c[4], hereda=c[5], conectado=c[6], nodo=c[7],
                          R0_acum=round(ac_d / ac_m, 4), motivo=c[2]))
    return filas


def resumen(r):
    f = tabla(r)
    v = [x['vida'] for x in f]
    n = len(v)
    prim = v[:max(1, n // 4)]              # cuerpos 1-5 con 20 muertes
    ult = v[max(0, n - n // 2):]           # cuerpos 11-20 con 20 muertes
    return dict(cuerpos=n, R0=round(sum(x['hijos'] for x in f) / max(n, 1), 4),
                vida_mediana=round(float(st.median(v)), 1) if v else None,
                vida_med_primeros=round(float(st.median(prim)), 1) if prim else None,
                vida_med_ultimos=round(float(st.median(ult)), 1) if ult else None,
                subida=(round(float(st.median(ult)) / float(st.median(prim)), 3) if prim and st.median(prim) else None),
                descendientes=r['descendientes'], fundadores=r['fundadores'],
                conectado_final=r['conectado_final'], nodo_n=r['nodo_n'],
                dote_final=r['dote_final'], umbral_final=r['umbral_final'], hereda_final=r['hereda_final'],
                T_efectivo=r['T_efectivo'], miedo_inerte=r['miedo_inerte'],
                curitas=[x['curita'] for x in f])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--alma', choices=list(ALMAS), default='interfaz')
    ap.add_argument('--sem', type=int, default=801)
    ap.add_argument('--muertes', type=int, default=10)
    ap.add_argument('--espera', type=float, default=0.0)
    ap.add_argument('--T', type=int, default=T)
    a = ap.parse_args()
    if a.T > 100000:
        raise SystemExit('T por cuerpo <= 100000 (regla del encargo): --T no puede pasar de 100000')

    shas = {k: C1.h16(os.path.join(RAIZ, p)) for k, p in
            dict(v14='organismo/organismo_v14.py', vivo='experimentos/nivel11_mundo_vivo/organismo_vivo.py',
                 rep='experimentos/nivel11_mundo_vivo/organismo_vivo_rep.py',
                 rep2='experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py',
                 h1='experimentos/nivel11_mundo_vivo/organismo_vivo_h1.py').items()}
    for k, v in SHA_ESPERADOS.items():
        if shas[k] != v:
            raise SystemExit(f"ORIGEN {k}: sha {shas[k]}, se esperaba {v}. Abortado.")

    print(f"BLOQUE ALMA · alma={a.alma} · semilla {a.sem} · {a.muertes} muertes · T {a.T}", flush=True)
    try:
        r, kw = corre(a.alma, a.sem, a.muertes, a.espera, a.T)
    except PreguntaPendiente as e:
        print(f"\n  PAUSA en la muerte {e.n}. El alma tiene que contestar.")
        print(f"  pregunta : {e.ruta}")
        print(f"  respuesta: {os.path.join(IO, f'alma_respuesta_{a.sem}_{e.n}.json')}")
        print(f"             {{\"curita\": \"a|b|c|d|e|f\", \"motivo\": \"...\"}}  (MENU_curitas.md)")
        print(f"  y se vuelve a lanzar el MISMO comando (el mundo es determinista: se repite bit a bit).")
        return 2

    # ---- ERR-54: los datos CRUDOS se guardan ANTES de analizar nada
    meta = dict(bloque='nivel13_alma', modo=a.alma, semilla=a.sem, muertes=a.muertes, T=a.T,
                kwargs={k: (list(v) if isinstance(v, (tuple, list)) else v) for k, v in kw.items()},
                sha_origenes=shas,
                sha_instrumento=C1.h16(os.path.join(AQUI, 'organismo_alma.py')),
                sha_constructor=C1.h16(os.path.join(AQUI, 'construye_alma.py')),
                sha_menu=C1.h16(os.path.join(AQUI, 'MENU_curitas.md')),
                sha_preregistro=(C1.h16(os.path.join(AQUI, 'PREREGISTRO_alma.md'))
                                 if os.path.exists(os.path.join(AQUI, 'PREREGISTRO_alma.md')) else None),
                python=platform.python_version(), numpy=np.__version__,
                fecha=time.strftime('%Y%m%d_%H%M%S'), segundos=r['_segundos'])
    nombre = f"alma_humo_{a.alma}_s{a.sem}_{meta['fecha']}.json"
    ruta = os.path.join(AQUI, nombre)
    json.dump(dict(meta=meta, crudo=C1.N(r)), open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"  CRUDO -> {nombre}  (sha {C1.h16(ruta)})", flush=True)

    f = tabla(r); s = resumen(r)
    print(f"\n  {'cuerpo':>6} {'vida':>6} {'causa':>8} {'hijos':>5}  {'curita':<6} {'dote':>5} {'umb':>5} "
          f"{'hereda':<6} {'con':>3} {'nodo':>4} {'R0ac':>6}")
    for x in f:
        print(f"  {x['cuerpo']:>6} {x['vida']:>6} {x['causa']:>8} {x['hijos']:>5}  {x['curita']:<6} "
              f"{x['dote']:>5} {x['umbral']:>5} {x['hereda']:<6} {x['conectado']:>3} {x['nodo']:>4} {x['R0_acum']:>6}")
    print("\n  " + json.dumps(s, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
