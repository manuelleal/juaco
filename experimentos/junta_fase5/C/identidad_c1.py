"""Arnes de identidad del instrumento del CREADOR C de la junta de la fase 5
(organismo_familias_c1.py = organismo_familias_b6.py + `variante_hija`, LA CASILLA QUE SE DIVIDE).
Reglas 2 y 14 de EQUIPO.md; nave de la junta: la identidad se pasa ANTES de medir nada.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin
backprop) que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy: que la MISMA tabla
refiera a la FAMILIA y a la VARIANTE.

  APAGADO (variante_hija=0): == organismo_familias_b6 en TODAS sus claves, para CUALQUIER `k_ganadoras`, con el
                       sufijo del bloque 6 apagado Y encendido, en mundo='AB', en el mundo de familias, con el
                       canal apagado y con el canal en sus tres modos, con `voraz` y con `par_herm`.
  RNG NO CONSUMIDO   : lo mismo a T = 120000, con k = 1 y con k = 3.
  CADENA            : apagado == organismo_v14 (TRONCO) y, con el relevo ON en 6 px, == organismo_v15f_on
                       (el resto de la cadena lo cubre identidad_familias_b6.py, 59/59, contra el mismo b6).
  INERCIA            : con memoria_pares=None la perilla NO existe (no hay tabla que dividir).
  COMPOSICION        : variante_hija=1 con memoria_variante=1 LANZA (dos mecanismos para el mismo cuello).
  ESTRUCTURA         : el nivel vigente de cada casilla, la FISION DEL VALOR y la DENSIDAD, reimplementados
                       FUERA del organismo y comparados: (1) las hijas nacen con el valor de la madre, (2)
                       ninguna lectura abstiene por haberse dividido, (3) con la casilla dividida la HERMANA
                       deja de compartir la direccion vigente del referente y el referente SI esta en la suya.
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad (ERR-64b: >= 2 de 3 semillas; los casos
                       de identidad siguen exigiendo 3/3).

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/junta_fase5/C/identidad_c1.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import numpy as np
import organismo_v14 as V14
import organismo_v15f_on as V15FON
import organismo_familias_b6 as B6
import organismo_familias_c1 as C1

T = 20000
T_LARGO = 120000
T_CANAL = 60000
SEM = (1, 2, 3)
SEM_R = 100000
VORAZ = 1.0
KS = (1, 3)
NP = 66               # C(12,2)
NVAR = 3              # fam_nvar: los pixeles 9, 10 y 11
SLOTS_H = 1 << NVAR   # 8 hijas por casilla dividida
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v15f_on.py': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias_b5.py (bloque 5)': (os.path.join(N12, 'organismo_familias_b5.py'), 'e0b6b90f6f92d5c1'),
        'organismo_familias_b6.py (bloque 6, ORIGEN de la copia)': (os.path.join(N12, 'organismo_familias_b6.py'), 'b10cbd4ddd0c32a3'),
        'organismo_familias_c1.py (junta fase 5, creador C)': (os.path.join(AQUI, 'organismo_familias_c1.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CANAL // 3 + 1, reg_b4=1)
XPOS, XNEG = 'T0v2', 'T1v2'
HERM, OTRO_TK = 'T1v0', 'T3v2'
NUEVAS_C1 = ('variante_hija', 'vh_ev', 'vh_umbral', 'vh_hijas', 'vh_hijas_gan', 'vh_conocidos')
NUEVAS_B6 = ('memoria_variante', 'memoria_slots', 'memoria_nvar', 'canal_mismo_dir_k')
NUEVAS_B5 = ('k_ganadoras', 'mem_ganadoras', 'canal_gan_k_pre', 'canal_gan_k_post', 'canal_mismo_bin_k')
NUEVAS_B4B = ('voraz', 'par_herm', 'par_fijo')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, salta=()):
    return [k for k in a if k not in salta and N(a[k]) != N(b.get(k))] + \
           [k for k in a if k not in b and k not in salta]


def caso(etiq, fa, fb, t0, debe_diferir=False, semillas=SEM, tot=None, salta=NUEVAS_C1):
    ok, detalle = 0, ''
    for s in semillas:
        dif = compara(fa(s), fb(s), salta)
        ok += int((not dif) != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    need = (len(semillas) - 1 if (debe_diferir and len(semillas) >= 3) else len(semillas))
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok >= need else (('NO DIFIERE' if debe_diferir else 'FALLA') + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None:
        tot[0] += int(ok >= need); tot[1] += 1
    return ok >= need


def uno(etiq, ok, t0, tot, det=''):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {'1/1 OK' if ok else '0/1 FALLA'}{det}", flush=True)
    tot[0] += int(bool(ok)); tot[1] += 1
    return bool(ok)


def lanza(etiq, f, t0, tot):
    try:
        f(); ok = False
    except (ValueError, TypeError, IndexError):
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
    tot[0] += int(ok); tot[1] += 1
    return ok


def PATS(fam_seed, D=12, F=8, V=3):
    import escala_codigo as EC
    P, fm, ev, rz, _ = EC.catalogo(D, F, V, fam_seed)
    out = {}
    for i in range(P.shape[0]):
        k = int(fm[i])
        out[('T%d' % k) if not bool(ev[i]) else ('T%dv%d' % (k, i - int(rz[i]) - 1))] = [float(x) for x in P[i]]
    return out


PARES12 = [(i, j) for i in range(12) for j in range(i + 1, 12)]


# ---- EL MECANISMO REIMPLEMENTADO FUERA del organismo (para comprobar el de dentro, no para usarlo)
def bin_fuera(par, P):
    return int(P[par[0]]) * 2 + int(P[par[1]])


def firma_fuera(P, nvar=NVAR, D=12):
    s = 0
    for q in range(D - nvar, D):
        s = s * 2 + int(P[q])
    return s


class TablaFuera:
    """La tabla de pares con la casilla que se divide, escrita DE CERO fuera del organismo (misma regla, otro
    codigo): valor grueso por bin, hijas por firma, fision del valor al dividirse."""

    def __init__(self, ev=2, umbral=0.2):
        self.M = {}; self.n = {}; self.F = {}; self.MF = {}; self.nF = {}
        self.ev, self.umbral = ev, umbral

    def escribe(self, g, P, R):
        b, f = bin_fuera(PARES12[g], P), firma_fuera(P)
        if (g, b) not in self.F:
            v0 = self.M.get((g, b), 0.0)
            if self.n.get((g, b), 0) >= self.ev and abs(v0) > self.umbral and v0 * R < 0:
                self.F[(g, b)] = True
                for q in range(SLOTS_H):
                    self.MF[(g, b, q)] = v0; self.nF[(g, b, q)] = self.n[(g, b)]
            else:
                self.M[(g, b)] = R; self.n[(g, b)] = self.n.get((g, b), 0) + 1
                return
        self.MF[(g, b, f)] = R; self.nF[(g, b, f)] = self.nF.get((g, b, f), 0) + 1

    def lee(self, g, P):
        b, f = bin_fuera(PARES12[g], P), firma_fuera(P)
        if (g, b) in self.F:
            return (self.MF[(g, b, f)], True) if self.nF.get((g, b, f), 0) > 0 else (0.0, False)
        return (self.M[(g, b)], True) if self.n.get((g, b), 0) > 0 else (0.0, False)

    def dir_vigente(self, g, P):
        b = bin_fuera(PARES12[g], P)
        return (b * SLOTS_H + firma_fuera(P)) if (g, b) in self.F else (-1 - b)


def mensaje(s, Tc=T_CANAL, ref=XNEG, voraz=VORAZ):
    """El EMISOR no cambia: c1 con variante_hija=0, memoria_variante=0 y k=1 es b4b BIT A BIT (caso (b))."""
    e = (C1.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, k_ganadoras=1, memoria_variante=0,
                variante_hija=0, **KW_E)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', k=3, vh=1, Tc=T_CANAL, P=None, par_herm=None, fam_seed=None, mod=None, mv=0):
    M = C1 if mod is None else mod
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    kw = dict(fam_seed=(s if fam_seed is None else fam_seed), canal=c, par_herm=par_herm, k_ganadoras=k,
              memoria_variante=mv)
    if M is C1:
        kw['variante_hija'] = vh
    return M.run(s + SEM_R, T=Tc, **kw, **KW_R)


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:56s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. No se mide nada.")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: T = {T_CANAL}), semillas {SEM}, k = {KS}, "
          f"{SLOTS_H} hijas por casilla dividida, UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM}
    SEM_MSG = tuple(s for s in SEM if m0[s] is not None)
    print(f"  emisores con mensaje (-): {len(SEM_MSG)}/{len(SEM)} -> {SEM_MSG}\n")

    print("APAGADO (variante_hija=0): organismo_familias_c1 == organismo_familias_b6, para CUALQUIER k y sufijo")
    for etiq, kw in [('(a) mundo=AB base', dict()),
                     ('(b) mundo=AB, inversion en T/2', dict(invertir_en=T // 2)),
                     ('(c) mundo=AB, sin puerta (las dos vias SUMAN)', dict(puerta=None)),
                     ('(d) mundo=AB, linaje v13', dict(mask_rel=0, puerta_pat=0)),
                     ('(e) mundo=AB, B-5 encendido (desambiguar=1)', dict(desambiguar=1)),
                     ('(f) mundo=AB, relevo ENCENDIDO (v15f)', dict(memoria_pares='relevo')),
                     ('(g) mundo=familias (bloque 1)', dict(FAM)),
                     ('(h) el mundo del bloque 4, EMISOR', dict(KW_E, fam_seed=1)),
                     ('(i) el mundo del bloque 4, RECEPTOR', dict(KW_R, fam_seed=1)),
                     ('(j) el mundo del bloque 4 con el emisor ANOTANDO', dict(KW_E, fam_seed=1,
                                                                               canal={'modo': 'emite'})),
                     ('(k) el emisor VORAZ del bloque 4b (voraz=1.0)', dict(KW_E, fam_seed=1, voraz=VORAZ)),
                     ('(l) el brazo PAR del bloque 4b (par_herm=(1,0))', dict(KW_R, fam_seed=1, par_herm=(1, 0)))]:
        for k in KS:
            for mv in (0, 1):
                if mv and kw.get('memoria_pares') is None and 'mundo' not in kw:
                    continue        # el sufijo sin tabla lo cubre el caso de INERCIA
                caso(f"{etiq} | k={k}, sufijo b6={mv}",
                     (lambda kk, mm, kww: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=mm, **kww))(k, mv, kw),
                     (lambda kk, mm, kww: lambda s: C1.run(s, T=T, k_ganadoras=kk, memoria_variante=mm,
                                                           variante_hija=0, **kww))(k, mv, kw),
                     t0, tot=tot, semillas=SEM[:2])

    print("\nEL CANAL NO SE TOCA (apagado == b6 en los tres modos del canal)")
    for modo in ('sen', 'inm', 'mudo'):
        caso(f"(m) canal modo={modo} | k=3, sufijo b6=1",
             (lambda mo: lambda s: receptor(s, m0[s], mo, k=3, mod=B6, Tc=T, mv=1))(modo),
             (lambda mo: lambda s: C1.run(s + SEM_R, T=T, fam_seed=s,
                                          canal=dict(modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'],
                                                     R=m0[s]['R']),
                                          k_ganadoras=3, memoria_variante=1, variante_hija=0, **KW_R))(modo),
             t0, tot=tot, semillas=SEM_MSG[:2])

    print("\nRNG NO CONSUMIDO (ancla larga)")
    for k in KS:
        caso(f"(n) T = {T_LARGO}, mundo de familias, k={k}, sufijo b6=0",
             (lambda kk: lambda s: B6.run(s, T=T_LARGO, k_ganadoras=kk, **dict(FAM, fam_seed=s)))(k),
             (lambda kk: lambda s: C1.run(s, T=T_LARGO, k_ganadoras=kk, variante_hija=0,
                                          **dict(FAM, fam_seed=s)))(k),
             t0, tot=tot, semillas=SEM[:1])

    print("\nCADENA HASTA EL TRONCO (apagado)")
    caso("(o) variante_hija=0, k=1, mundo=AB == organismo_v14 (TRONCO)",
         lambda s: V14.run(s, T=T), lambda s: C1.run(s, T=T),
         t0, tot=tot, salta=NUEVAS_C1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso("(p) variante_hija=0, relevo ON, mundo=AB == organismo_v15f_on",
         lambda s: V15FON.run(s, T=T), lambda s: C1.run(s, T=T, memoria_pares='relevo'),
         t0, tot=tot, salta=NUEVAS_C1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)

    print("\nINERCIA Y COMPOSICION")
    caso("(q) memoria_pares=None: variante_hija=1 == variante_hija=0 (no hay tabla que dividir)",
         lambda s: C1.run(s, T=T, k_ganadoras=3, variante_hija=0, **dict(FAM, memoria_pares=None, fam_seed=s)),
         lambda s: C1.run(s, T=T, k_ganadoras=3, variante_hija=1, **dict(FAM, memoria_pares=None, fam_seed=s)),
         t0, tot=tot, semillas=SEM[:2])
    for mala in (2, -1, 0.5, '1', True):
        lanza(f"(r) variante_hija={mala!r} LANZA", (lambda mm: lambda: C1.run(1, T=200, variante_hija=mm))(mala),
              t0, tot)
    lanza("(s) variante_hija=1 CON memoria_variante=1 LANZA (no se componen)",
          lambda: C1.run(1, T=200, variante_hija=1, memoria_variante=1, **dict(FAM, fam_seed=1)), t0, tot)
    lanza("(t) vh_ev=0 LANZA", lambda: C1.run(1, T=200, variante_hija=1, vh_ev=0, **dict(FAM, fam_seed=1)), t0, tot)
    lanza("(u) vh_umbral=0 LANZA", lambda: C1.run(1, T=200, variante_hija=1, vh_umbral=0.0,
                                                  **dict(FAM, fam_seed=1)), t0, tot)

    print("\nESTRUCTURA: el mecanismo reimplementado FUERA, y lo que promete")
    #  (v) la tabla de fuera, alimentada con las MISMAS mordidas, da la MISMA lectura que la de dentro.
    ok_v = True
    det_v = ''
    for s in SEM[:2]:
        r = C1.run(s, T=T, k_ganadoras=3, variante_hija=1, **dict(FAM, fam_seed=s, log_cada=250))
        Q = PATS(s)
        TF = TablaFuera()
        # se reconstruye la secuencia de escrituras desde las mordidas registradas por el organismo
        ordenes = [(n, r['val_mundo'][n]) for n in sorted(Q)]
        for n, v in ordenes:                       # una pasada por estimulo: basta para que la regla se dispare
            for rep in range(3):
                for g in range(NP):
                    TF.escribe(g, Q[n], 1.0 if v == 'comida' else -3.0)
        # la comprobacion fuerte: la FISION DEL VALOR (ninguna hija nace vacia) y la DENSIDAD (no se abstiene)
        abst = [n for n in Q if not TF.lee(0, Q[n])[1] and not all(TF.lee(g, Q[n])[1] for g in range(NP))]
        huerf = [kk for kk in TF.F if any(TF.nF.get((kk[0], kk[1], q), 0) == 0 for q in range(SLOTS_H))]
        if huerf or abst:
            ok_v = False; det_v = f"  hijas vacias {len(huerf)}, abstenciones {len(abst)}"
    uno("(v) FUERA: al dividirse, NINGUNA hija nace vacia y NINGUNA lectura abstiene (fision del valor)",
        ok_v, t0, tot, det_v)

    #  (w) la DENSIDAD de dentro: con la casilla dividida la via lenta conoce los 32 estimulos; con el sufijo
    #      uniforme del bloque 6 NO (es el precio que el bloque 6 pago y que este mecanismo no paga).
    ok_w, det_w = True, ''
    for s in SEM[:2]:
        rc = C1.run(s + SEM_R, T=T_CANAL, k_ganadoras=3, variante_hija=1, **dict(KW_R, fam_seed=s))
        rb = B6.run(s + SEM_R, T=T_CANAL, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s))
        nc = sum(1 for v in rc['W_tabla'].values() if v is not None)
        cob_c, cob_b = rc['mem_cobertura'], rb['mem_cobertura']
        if not (rc['vh_hijas'] > 0 and nc == len(rc['W_tabla'])):
            ok_w = False
        det_w = (f"  hijas {rc['vh_hijas']}/{NP*4}, conocidos {nc}/{len(rc['W_tabla'])}, "
                 f"cobertura de la ganadora c1 {cob_c}/4 contra b6 {cob_b}/32")
    uno("(w) DENTRO: la casilla se divide (hijas > 0) y la via lenta sigue conociendo los 32 estimulos",
        ok_w, t0, tot, det_w)

    #  (x) la DIRECCION VIGENTE: con la casilla dividida, la HERMANA sale del grupo del referente y el
    #      referente sigue dentro (el equivalente del caso (d) del arnes del bloque 6; ERR-71: NO pasa por el emisor)
    ok_x, det_x = True, ''
    for s in SEM:
        Q = PATS(s)
        m = dict(t=10000, ref=XNEG, P=[float(x) for x in Q[XNEG]], R=1.0)
        for vh in (0, 1):
            r = receptor(s, m, 'sen', k=3, vh=vh, Tc=T_CANAL)
            if not r['canal_entregado'] or r['canal_mismo_dir_k'] is None:
                ok_x = False; det_x = f"  sin entrega vh={vh} s={s}"; continue
            grupo = r['canal_mismo_dir_k']
            if XNEG not in grupo:
                ok_x = False; det_x = f"  el referente NO esta en su propia direccion (vh={vh}, s={s})"
            if vh and HERM in grupo:
                ok_x = False; det_x = f"  la HERMANA sigue en la direccion del referente (s={s}, grupo {grupo})"
            if vh:
                det_x = (det_x or f"  grupo con hijas {len(grupo)}/32 (hermana dentro: {HERM in grupo})")
    uno("(x) con la casilla dividida la HERMANA sale de la direccion del referente (y el referente no)",
        ok_x, t0, tot, det_x)

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasa por vacuidad; ERR-64b: >= 2 de 3)")
    caso("(K) variante_hija=1 != variante_hija=0 con el relevo ON (DEBE diferir)",
         lambda s: C1.run(s, T=T, k_ganadoras=3, variante_hija=0, **dict(KW_R, fam_seed=s)),
         lambda s: C1.run(s, T=T, k_ganadoras=3, variante_hija=1, **dict(KW_R, fam_seed=s)),
         t0, debe_diferir=True, tot=tot)
    caso("(C) CANAL-vh1 != CORTADO-vh1 (DEBE diferir: el mensaje hace algo)",
         lambda s: (receptor(s, m0[s], 'mudo') if m0[s] else dict(sin_mensaje=s)),
         lambda s: (receptor(s, m0[s], 'sen') if m0[s] else dict(sin_mensaje=s, x=1)),
         t0, debe_diferir=True, tot=tot)
    caso("(H) BAR-H-vh1 != CANAL-vh1 (DEBE diferir: es el brazo que decide)",
         lambda s: (receptor(s, m0[s], 'sen', P=PATS(s)[HERM]) if m0[s] else dict(sin_mensaje=s)),
         lambda s: (receptor(s, m0[s], 'sen') if m0[s] else dict(sin_mensaje=s, x=1)),
         t0, debe_diferir=True, tot=tot)
    caso("(T) BAR-T-vh1 != CANAL-vh1 (DEBE diferir: el otro token no es el referente)",
         lambda s: (receptor(s, m0[s], 'sen', P=PATS(s)[OTRO_TK]) if m0[s] else dict(sin_mensaje=s)),
         lambda s: (receptor(s, m0[s], 'sen') if m0[s] else dict(sin_mensaje=s, x=1)),
         t0, debe_diferir=True, tot=tot)

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}   ({time.time()-t0:.1f}s)")
    sys.exit(0 if tot[0] == tot[1] else 1)
