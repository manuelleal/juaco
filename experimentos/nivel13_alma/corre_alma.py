"""BLOQUE ALMA (nivel 13) — los SEIS brazos, el buzon paciente del alma y los controles automaticos.

MISION: llegar a la AGI por este camino, hasta la fase 10 y superarla — un organismo minimo con reglas locales
que aprende, sobrevive, se comunica y se reproduce; con evidencia preregistrada. Hoy: un alma externa que parcha
al cuerpo cada vez que muere, con un nodo central de conocimiento; el alma es el BUSCADOR, no el resultado.

Ejecuta PREREGISTRO_alma.md y MENU_curitas.md (el menu cerrado). Instrumento: organismo_alma2.py (por anclas
desde organismo_alma.py 7c09cec391daa879 <- organismo_vivo_h1.py 9e99ff87b5e2db1e, que solo se leyeron).
Reutiliza mini_vivo.py y corre_vivo_rep(.2).py de nivel11 SIN copiarlos.

UN PROCESO POR LINAJE, SIN Pool (regla 3 de EQUIPO.md). Varios procesos a la vez esta permitido: cada uno lleva
su brazo y su semilla y escribe su propio JSON. T por cuerpo <= 100 000 por construccion.

    python experimentos/nivel13_alma/corre_alma.py --brazo ALMA    --semilla 801 --muertes 20
    python experimentos/nivel13_alma/corre_alma.py --brazo BARAJA  --semilla 801 --muertes 20

LOS SEIS BRAZOS (PREREGISTRO_alma.md secc. 3; los tres ultimos los pidio el coordinador antes de la serie)
  ALMA      alma externa (agente) · menu abcdef · nodo lleno, se conecta si el alma elige (a)   <- la hipotesis
  AZAR      curita AL AZAR del menu abcdef, rng propio 850000+10^6*sem · nodo lleno   <- que ELEGIR importa
  NINGUNA   siempre (f) · nodo APAGADO   <- la linea base: es H-1 NADA_CM cuerpo a cuerpo
  SIN_NODO  alma externa con el menu SIN (a) ni (b): el nodo se llena y NADIE se conecta jamas
            <- separa "el efecto es del NODO" de "el efecto es de las perillas del mundo (c)/(d)/(e)"
  CIEGO     nace CONECTADO desde el cuerpo 1 · curitas AL AZAR sobre el menu sin (a)
            <- el NODO SOLO, sin un alma que razone: separa el nodo del alma
  BARAJA    igual que CIEGO pero el hijo lee el nodo con las RECOMPENSAS PERMUTADAS entre mensajes
            <- CONTROL DE CONTENIDO (H1-4): mismas marginales, asociacion destruida. CIEGO y BARAJA comparten
               el rng de las curitas, asi que la secuencia de curitas es LA MISMA: el unico cambio es el nodo.

LA INTERFAZ DEL ALMA (no hay cliente de modelo en este repo: el alma es un agente que escribe archivos)
  En la muerte n el bucle busca `alma_io/alma_respuesta_<sem>_<n>.json`. Si no esta, escribe
  `alma_io/alma_pregunta_<sem>_<n>.json` y ESPERA con paciencia hasta `--espera` segundos (por defecto 600 = 10
  min, lo que el coordinador pidio para un agente Haiku real), sondeando cada 0.5 s.
  Con `--espera 0` no espera: PARA la corrida y el mismo comando se vuelve a lanzar (el mundo es determinista y
  se repite bit a bit hasta la muerte siguiente). Las dos rutas producen el MISMO JSON.
  TOLERANCIA (encargo del coordinador): una respuesta que no exista, no sea JSON, no sea un objeto, no traiga
  `curita`, o traiga una curita fuera del menu OFRECIDO, se registra como **(f) NADA** y la corrida SIGUE; el
  motivo queda en `invalidas` dentro del meta del JSON crudo. El instrumento sigue siendo estricto (aborta si le
  llega una curita fuera del menu): la tolerancia vive aqui, en el buzon.

VOCABULARIO (regla 6): "curita", "nodo central", "exposicion sin consecuencia", "cuerpo", "linaje", "R0 del
linaje" (descendientes/muertes). NO se dice "evoluciona", "decide", "quiere" del alma: el alma es un agente
externo que elige de un menu cerrado, y eso es lo unico que se mide.
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
import organismo_alma2 as AL

T = 100000
DOTE = 0.6
MENU_TOTAL = 'abcdef'
IO = os.path.join(AQUI, 'alma_io')
ESPERA = 600.0        # paciencia por respuesta, en segundos (10 min: lo que el coordinador pidio)
SONDEO = 0.5
SHA_ESPERADOS = dict(v14='feefc88b1fd8d434', vivo='20c0961c79de8825', rep='aa823d56c2d4213c',
                     rep2='96feb4918dc5d694', h1='9e99ff87b5e2db1e')
SHA_ALMA = '7c09cec391daa879'   # organismo_alma.py: origen por anclas de organismo_alma2.py

MED_H1 = dict(C2.MED2, h1=1)
# EL CUERPO: CUELLO_MIN, el mismo brazo en el que H-1 midio R0 0.148 (hereda nada) y 0.160 (hereda M1)
CUERPO = dict(C1.BRAZOS['CUELLO_MIN']) | MED_H1 | dict(muerte_real=1, hereda='nada', dote=DOTE)

# brazo -> (quien elige, kwargs del instrumento). `menu` es lo que se le OFRECE al alma.
BRAZOS = {
    'ALMA':     ('interfaz',  dict(menu='abcdef', nodo=1, conectado=0, nodo_baraja=0)),
    'AZAR':     ('aleatoria', dict(menu='abcdef', nodo=1, conectado=0, nodo_baraja=0)),
    'NINGUNA':  ('fija_f',    dict(menu='f',      nodo=0, conectado=0, nodo_baraja=0)),
    'SIN_NODO': ('interfaz',  dict(menu='cdef',   nodo=1, conectado=0, nodo_baraja=0)),
    'CIEGO':    ('aleatoria', dict(menu='bcdef',  nodo=1, conectado=1, nodo_baraja=0)),
    'BARAJA':   ('aleatoria', dict(menu='bcdef',  nodo=1, conectado=1, nodo_baraja=1)),
}
ORDEN = ['ALMA', 'AZAR', 'NINGUNA', 'SIN_NODO', 'CIEGO', 'BARAJA']
INVALIDAS = []


class PreguntaPendiente(Exception):
    def __init__(self, n, ruta, seg):
        super().__init__(f"pregunta {n} sin responder tras {seg:.0f}s: {ruta}")
        self.n, self.ruta, self.seg = n, ruta, seg


# ---------------------------------------------------------------- las tres almas
def etiqueta_io(sem, brazo, n, que):
    """CONVENCION DE NOMBRES (coordinador, 18 sep): todo en alma_io/ con prefijo _<semilla>_. El brazo va
    DESPUES de la semilla porque hay DOS brazos con alma externa (ALMA y SIN_NODO) y en la misma semilla se
    pisarian: ALMA conserva el nombre corto con el que ya se entrego su humo, SIN_NODO lleva el suyo."""
    if brazo == 'ALMA':
        return os.path.join(IO, f'alma_{que}_{sem}_{n}.json')
    return os.path.join(IO, f'alma_{que}_{sem}_{brazo}_{n}.json')


def alma_interfaz(sem, espera, brazo='ALMA'):
    """El alma es un AGENTE EXTERNO. Aqui solo esta el buzon: escribe la pregunta y espera con paciencia."""
    os.makedirs(IO, exist_ok=True)

    def fn(res):
        n = res['cuerpo']
        rp = etiqueta_io(sem, brazo, n, 'respuesta')
        rq = etiqueta_io(sem, brazo, n, 'pregunta')
        if not os.path.exists(rp):
            json.dump(res, open(rq, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            if espera <= 0:
                raise PreguntaPendiente(n, rq, 0.0)
            print(f"    esperando la respuesta {n} (hasta {espera:.0f}s): {os.path.basename(rq)}", flush=True)
            t0 = time.time()
            while not os.path.exists(rp):
                if time.time() - t0 > espera:
                    raise PreguntaPendiente(n, rq, time.time() - t0)
                time.sleep(SONDEO)
        return json.load(open(rp, encoding='utf-8'))
    return fn


def alma_aleatoria(sem, menu):
    """CONTROL: una curita AL AZAR del menu OFRECIDO, con rng PROPIO (850000 + 1000000*sem).
    No toca el rng del mundo (sem), ni el de los hijos (700000+), ni el de la herencia barajada (800000+),
    ni el del barajado del nodo (860000+). CIEGO y BARAJA comparten menu y semilla: misma secuencia de curitas."""
    rg = np.random.default_rng(850000 + 1000000 * sem)

    def fn(res):
        return {'curita': menu[int(rg.integers(len(menu)))],
                'motivo': f'control: curita al azar del menu {menu!r} (rng propio 850000+1000000*sem)'}
    return fn


def alma_fija_f(sem, menu):
    """CONTROL: sin curita. El brazo ademas apaga el nodo: sin curita y sin nodo (= H-1 NADA_CM)."""
    return lambda res: {'curita': 'f', 'motivo': 'control: sin curita'}


def seguro(fn, menu):
    """EL BUZON ES PACIENTE, EL INSTRUMENTO ES ESTRICTO: lo que no sea una curita del menu OFRECIDO se
    registra como (f) NADA y la corrida SIGUE. Nunca llega al instrumento una curita invalida."""
    def envoltura(res):
        n = res.get('cuerpo')
        try:
            d = fn(res)
        except PreguntaPendiente:
            raise
        except Exception as e:
            INVALIDAS.append([n, f'{type(e).__name__}: {e}'.replace('\n', ' ')[:200]])
            return {'curita': 'f', 'motivo': 'INVALIDA (excepcion al leer la respuesta) -> (f) NADA'}
        if not isinstance(d, dict):
            INVALIDAS.append([n, f'la respuesta no es un objeto JSON: {type(d).__name__}'])
            return {'curita': 'f', 'motivo': 'INVALIDA (no es un objeto) -> (f) NADA'}
        c = d.get('curita')
        if not isinstance(c, str) or len(c) != 1 or c not in menu:   # None, numero, lista o letra fuera del menu
            INVALIDAS.append([n, f'curita {c!r} fuera del menu ofrecido {menu!r}'])
            return {'curita': 'f', 'motivo': f'INVALIDA (curita {c!r} fuera del menu {menu!r}) -> (f) NADA'}
        return d
    return envoltura


ELIGE = {'interfaz': alma_interfaz, 'aleatoria': alma_aleatoria, 'fija_f': alma_fija_f}


# ---------------------------------------------------------------- corrida
def corre(brazo, sem, muertes, espera=ESPERA, T_max=T):
    quien, extra = BRAZOS[brazo]
    menu = extra['menu']
    if 'f' not in menu:
        raise SystemExit(f"BRAZO {brazo}: el menu {menu!r} tiene que incluir (f) (es la curita por defecto y la de la tolerancia)")
    base = alma_interfaz(sem, espera, brazo) if quien == 'interfaz' else ELIGE[quien](sem, menu)
    kw = dict(CUERPO, alma_muertes=muertes, **extra)
    t0 = time.time()
    r = AL.run(sem, T=T_max, alma=seguro(base, menu), **kw)
    r['_segundos'] = round(time.time() - t0, 2)
    return r, kw


def tabla(r):
    """Vida por cuerpo, curita elegida, hijos y R0 acumulado del linaje."""
    cur, vidas, desc = r['curitas'], r['vidas_cuerpo'], r['desc_cuerpo']
    filas, ad, am = [], 0, 0
    for i, c in enumerate(cur):
        am += 1; ad += desc[i]
        filas.append(dict(cuerpo=i + 1, vida=vidas[i], causa=c[8], hijos=desc[i], curita=c[1],
                          dote=c[3], umbral=c[4], hereda=c[5], conectado=c[6], nodo=c[7],
                          R0_acum=round(ad / am, 4), motivo=c[2]))
    return filas


def resumen(r):
    f = tabla(r); v = [x['vida'] for x in f]; n = len(v)
    prim = v[:max(1, n // 4)]              # cuerpos 1-5 con 20 muertes (PREREGISTRO secc. 4)
    ult = v[max(0, n - n // 2):]           # cuerpos 11-20 con 20 muertes
    mp = float(st.median(prim)) if prim else None
    mu = float(st.median(ult)) if ult else None
    return dict(cuerpos=n, R0=round(sum(x['hijos'] for x in f) / max(n, 1), 4),
                vida_mediana=round(float(st.median(v)), 1) if v else None,
                vida_med_primeros=round(mp, 1) if mp is not None else None,
                vida_med_ultimos=round(mu, 1) if mu is not None else None,
                subida=(round(mu / mp, 3) if mp else None),
                descendientes=r['descendientes'], fundadores=r['fundadores'],
                conectado_final=r['conectado_final'], nodo_n=r['nodo_n'],
                dote_final=r['dote_final'], umbral_final=r['umbral_final'], hereda_final=r['hereda_final'],
                T_efectivo=r['T_efectivo'], miedo_inerte=r['miedo_inerte'], alma2=r['alma2'],
                invalidas=len(INVALIDAS), curitas=[x['curita'] for x in f])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--brazo', choices=ORDEN, default=None)
    ap.add_argument('--semilla', type=int, default=None)
    ap.add_argument('--muertes', type=int, default=20)
    ap.add_argument('--espera', type=float, default=ESPERA, help='segundos de paciencia por respuesta; 0 = para y se relanza')
    ap.add_argument('--T', type=int, default=T)
    ap.add_argument('--alma', choices=['interfaz', 'aleatoria', 'ninguna'], default=None, help='alias viejo')
    ap.add_argument('--sem', type=int, default=None, help='alias viejo de --semilla')
    a = ap.parse_args()
    brazo = a.brazo or {'interfaz': 'ALMA', 'aleatoria': 'AZAR', 'ninguna': 'NINGUNA'}.get(a.alma, 'ALMA')
    sem = a.semilla if a.semilla is not None else (a.sem if a.sem is not None else 801)
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
    sha_alma = C1.h16(os.path.join(AQUI, 'organismo_alma.py'))
    if sha_alma != SHA_ALMA:
        raise SystemExit(f"ORIGEN organismo_alma.py: sha {sha_alma}, se esperaba {SHA_ALMA}. Abortado.")

    quien, extra = BRAZOS[brazo]
    print(f"BLOQUE ALMA · brazo {brazo} ({quien}, menu {extra['menu']!r}, nodo {extra['nodo']}, "
          f"conectado {extra['conectado']}, baraja {extra['nodo_baraja']}) · semilla {sem} · "
          f"{a.muertes} muertes · T {a.T} · pid {os.getpid()}", flush=True)
    try:
        r, kw = corre(brazo, sem, a.muertes, a.espera, a.T)
    except PreguntaPendiente as e:
        print(f"\n  PAUSA en la muerte {e.n}. El alma tiene que contestar.")
        print(f"  pregunta : {e.ruta}")
        print(f"  respuesta: {etiqueta_io(sem, brazo, e.n, 'respuesta')}")
        print(f"             {{\"curita\": \"{'|'.join(extra['menu'])}\", \"motivo\": \"...\"}}  (MENU_curitas.md)")
        print(f"  y se vuelve a lanzar el MISMO comando (el mundo es determinista: se repite bit a bit).")
        return 2

    # ---- ERR-54: los datos CRUDOS se guardan ANTES de analizar nada
    meta = dict(bloque='nivel13_alma', brazo=brazo, elige=quien, semilla=sem, muertes=a.muertes, T=a.T,
                espera=a.espera, kwargs={k: (list(v) if isinstance(v, (tuple, list)) else v) for k, v in kw.items()},
                sha_origenes=dict(shas, alma=sha_alma),
                sha_instrumento=C1.h16(os.path.join(AQUI, 'organismo_alma2.py')),
                sha_constructor=C1.h16(os.path.join(AQUI, 'construye_alma2.py')),
                sha_menu=C1.h16(os.path.join(AQUI, 'MENU_curitas.md')),
                sha_preregistro=(C1.h16(os.path.join(AQUI, 'PREREGISTRO_alma.md'))
                                 if os.path.exists(os.path.join(AQUI, 'PREREGISTRO_alma.md')) else None),
                invalidas=list(INVALIDAS), python=platform.python_version(), numpy=np.__version__,
                fecha=time.strftime('%Y%m%d_%H%M%S'), segundos=r['_segundos'])
    nombre = f"alma_{brazo}_s{sem}_{meta['fecha']}.json"
    ruta = os.path.join(AQUI, nombre)
    json.dump(dict(meta=meta, crudo=C1.N(r)), open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"  CRUDO -> {nombre}  (sha {C1.h16(ruta)})", flush=True)

    f = tabla(r)
    print(f"\n  {'cuerpo':>6} {'vida':>6} {'causa':>8} {'hijos':>5}  {'curita':<6} {'dote':>5} {'umb':>5} "
          f"{'hereda':<6} {'con':>3} {'nodo':>4} {'R0ac':>6}")
    for x in f:
        print(f"  {x['cuerpo']:>6} {x['vida']:>6} {x['causa']:>8} {x['hijos']:>5}  {x['curita']:<6} "
              f"{x['dote']:>5} {x['umbral']:>5} {x['hereda']:<6} {x['conectado']:>3} {x['nodo']:>4} {x['R0_acum']:>6}")
    if INVALIDAS:
        print(f"\n  RESPUESTAS INVALIDAS registradas como (f): {INVALIDAS}")
    print("\n  " + json.dumps(resumen(r), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
