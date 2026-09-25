# EXPLORATORIO, no es dato
"""corre_cuerpo.py — runner EXPLORATORIO de PROMETEO-CUERPO (Opus, equipo JUACO, 25-sep-2026). MISION: llegar a la AGI por este camino.

Reusa corre_codigo.trabajo() SIN tocarlo (monkeypatch SOLO en este proceso, como corre_prometeo.py): el motor pasa a motor_cuerpo y
eco_de agrega el mundo, el alfabeto del brazo, la niebla y las partes. Un proceso por invocacion; dentro, las corridas van UNA TRAS
OTRA (sin Pool). Semillas 31001-31999.
Brazos (todos con la cinta v0 de CODIGO_SIN_SOS: la SOS no se lee):
  CUERPO        alfabeto v0 + KIT de Prometeo (CABLE, HGT) + PARTE; las partes actuan y cobran
  CUERPO_MUDO   lo mismo, pero las partes solo COBRAN (efecto apagado): control de que la seleccion elige por efecto
  PROMETEO      alfabeto v0 + KIT (sin partes): == motor_prometeo bit a bit (arnes IC1)
Mundos: quieto, onda8k (fable_mundos), veneno (B y D danan el doble desde t 0: -0.8), niebla (quieto + vista de radio NIEBLA).
Uso:
  python corre_cuerpo.py --mundos quieto,onda8k --brazos CUERPO,CUERPO_MUDO,PROMETEO --semillas 31001,31002 --bloque 0 --de 6
  python corre_cuerpo.py --cal --ronda 1 --semillas 31901,31902 --bloque 0 --de 3
"""
import argparse, json, os, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); ORG = os.path.dirname(AQUI)
CODIGO = os.path.join(ORG, 'codigo'); FABLE = os.path.join(CODIGO, 'exploracion_fable')
for d in (FABLE, CODIGO, AQUI):
    if d in sys.path: sys.path.remove(d)
    sys.path.insert(0, d)
import motor_cuerpo as MQ
import codigo_cuerpo as CQ
import corre_codigo as CC
import fable_mundos as FB

DATOS = os.path.join(AQUI, 'datos')
TLS = dict(largo=dict(T=60000, t_cambio=8000, t_corte=44000, r0_margen=4000),
           humo=dict(T=6000, t_cambio=2000, t_corte=4000, r0_margen=1000),
           cal=dict(T=16000, t_cambio=8000, t_corte=16000, r0_margen=2000))
NIEBLA = 12   # radio de vista en el mundo 'niebla' (L = 1200; hasta 120 objetos). Ronda 1: 5 (demasiado dura); ronda 2 (12:12, declarada): 12
ALF_CUERPO = CQ.OPS + CQ.KIT + CQ.CUERPO
ALFS = dict(CUERPO=ALF_CUERPO, CUERPO_MUDO=ALF_CUERPO, PROMETEO=CQ.OPS + CQ.KIT)
# magnitudes por ronda de calibracion (PREDICCIONES_previas.md: criterio fijado antes). La ventana usa la ULTIMA ronda aceptada.
MAG_RONDAS = {1: dict(MQ.MAG),
              2: dict(MQ.MAG, costo=(0.0001, 0.0004, 0.0004, 0.0002, 0.0002, 0.0002))}   # 12:12 declarada: PATA /2, ESCUDO x2, ESTOMAGO x2
MAG_USO = [dict(MQ.MAG)]
MUNDO_PARTE = dict(PATA='quieto', ESCUDO='veneno', ESTOMAGO='quieto', OJO='niebla', MANDIBULA='quieto', LENGUA='quieto')


def mundos(t0):
    C = FB.catalogo(t0)
    return dict(quieto=(C['quieto'], None), onda8k=(C['onda8k'], None),
                veneno=(dict(tipo='fijo', t=0, tabla={'B': (-0.8, 0.0), 'D': (0.0, -0.8)}), None),
                niebla=(C['quieto'], NIEBLA))


_eco_de0 = CC.eco_de
_CFG = dict(spec=None, niebla=None, brazo=None, base='CODIGO_SIN_SOS', codigo=None)
_ULTR = [None]


def eco_de_cuerpo(brazo, t_corte, t_cambio, **extra):
    b = _CFG['brazo']
    CQ.pon_alfabeto(ALFS[b])
    e = _eco_de0(_CFG['base'], t_corte, t_cambio, **extra)
    e['cambio'] = dict(_CFG['spec']); e['niebla'] = _CFG['niebla']
    e['partes_on'] = (b != 'CUERPO_MUDO'); e['partes_mag'] = {k: (tuple(v) if isinstance(v, list) else v) for k, v in MAG_USO[0].items()}
    if _CFG['codigo'] is not None: e['codigo'] = list(_CFG['codigo'])
    return e


class _Shim:
    NOMBRES = MQ.NOMBRES
    @staticmethod
    def run_solapadas(*a, **k):
        r = MQ.run_solapadas(*a, **k); _ULTR[0] = r; return r


CC.MC = _Shim; CC.eco_de = eco_de_cuerpo


def partes_de(cintas, E):
    """[copias por parte] de cada cinta (0 si no expresa ninguna)."""
    G0 = np.array(E['G0']); lo = np.array(E['lo']); hi = np.array(E['hi']); out = []
    for c in cintas:
        p = CQ.partes(tuple(tuple(x) for x in c), G0, lo, hi, MQ.ENTEROS)
        out.append([0] * len(CQ.PARTES) if p is None else list(p))
    return out


def resume_banco(cintas, E):
    if not cintas: return None
    P = np.array(partes_de(cintas, E), float)
    return dict(n=len(cintas), frac=[round(float(x), 4) for x in (P > 0).mean(0)], copias=[round(float(x), 3) for x in P.mean(0)],
                largo=round(float(np.mean([len(c) for c in cintas])), 2), alguna=round(float((P.sum(1) > 0).mean()), 4))


def resume_nac(nac, T, W=2000):
    a = np.array(nac, float) if nac else np.zeros((0, 1 + len(CQ.PARTES)))
    out = []
    for s in range(0, T, W):
        m = (a[:, 0] >= s) & (a[:, 0] < s + W) if len(a) else np.zeros(0, bool)
        if not m.any(): out.append([s, 0] + [None] * len(CQ.PARTES)); continue
        out.append([s, int(m.sum())] + [round(float((a[m, 1 + j] > 0).mean()), 4) for j in range(len(CQ.PARTES))])
    return out


def una(seed, brazo, tl, carpeta, etq, log):
    fin = os.path.join(carpeta, f"{etq}_s{seed}.json")
    if os.path.exists(fin): log(f"ya existe {os.path.basename(fin)}"); return
    _ULTR[0] = None
    x = CC.trabajo((seed, etq, tl, carpeta, False))
    r = _ULTR[0]
    if r is not None and 'codigo' in r:
        pr = r['codigo']['prometeo']; cu = r['codigo']['cuerpo']; E = r['eco']
        cc = pr.get('cod_corte') or {}
        x['prometeo'] = dict(kit=pr.get('kit'), n_hgt_ev=len(pr.get('hgt_ev') or []), banco_corte=cc.get('banco'), banco_final=pr.get('banco_final'))
        x['cuerpo'] = dict(cont=cu.get('cont'), mag=cu.get('mag'), partes_on=cu.get('partes_on'), niebla=cu.get('niebla'), partes=cu.get('partes'),
                           nac_ventanas=resume_nac(cu.get('nac', []), tl['T']), n_nac_reg=len(cu.get('nac', [])),
                           banco_corte=resume_banco(cc.get('banco'), E), banco_final=resume_banco(pr.get('banco_final'), E),
                           vivos_final=resume_banco([c[3] for c in (r['codigo'].get('cintas_vivos') or [])], E))
    x['brazo_cuerpo'] = brazo; x['mundo_cuerpo'] = dict(spec=_CFG['spec'], niebla=_CFG['niebla']); x['alfabeto'] = list(ALFS[brazo])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(x, f, default=list)
    os.replace(tmp, fin)
    cb = (x.get('cuerpo') or {}); bf = cb.get('banco_final') or {}; bc = cb.get('banco_corte') or {}
    log(f"{etq:<22} s{seed}: {x.get('seg')} s · persiste {x.get('persiste')} (vivos {x.get('vivos_T')}) · n_nac {x.get('n_nac')} · n_final {x.get('n_final')} "
        f"· R0 final {x.get('r0_final')} · banco corte {bc.get('frac')} · final {bf.get('frac')} · cont {cb.get('cont')} · abortado {x.get('abortado')}")


def corre(mundos_, semillas, brazos, tl_nombre, bloque, de):
    tl = dict(TLS[tl_nombre]); M = mundos(tl['t_cambio'])
    jobs = [(m, s, b) for m in mundos_ for s in semillas for b in brazos][bloque::de]
    os.makedirs(DATOS, exist_ok=True)
    flog = open(os.path.join(DATOS, f"progreso_{tl_nombre}_b{bloque}de{de}.log"), 'a', encoding='utf-8')
    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"EXPLORATORIO CUERPO {tl} · MAG {MAG_USO[0]} · niebla {NIEBLA} · {len(jobs)} corridas: {jobs}")
    for m, s, b in jobs:
        _CFG.update(spec=M[m][0], niebla=M[m][1], brazo=b, base='CODIGO_SIN_SOS', codigo=None)
        carpeta = os.path.join(DATOS, f"{m}_{tl_nombre}"); os.makedirs(carpeta, exist_ok=True)
        una(s, b, tl, carpeta, b, log)
    flog.close()


def calibra(ronda, semillas, bloque, de):
    """Competencia 15 contra 15 (copia apagada): la mitad de los fundadores con UNA copia de la parte. ON y MUDO."""
    tl = dict(TLS['cal']); M = mundos(tl['t_cambio']); MAG_USO[0] = dict(MAG_RONDAS[ronda])
    n0 = CC.MUNDO['n0']; C0 = tuple(CC.CINTA0)
    jobs = [(p, s, b) for p in CQ.PARTES for s in semillas for b in ('CUERPO', 'CUERPO_MUDO')][bloque::de]
    carpeta = os.path.join(DATOS, f"cal_r{ronda}"); os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, f"progreso_b{bloque}de{de}.log"), 'a', encoding='utf-8')
    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"CALIBRACION ronda {ronda} · {tl} · MAG {MAG_USO[0]} · {jobs}")
    for p, s, b in jobs:
        m = MUNDO_PARTE[p]; j = CQ.PARTES.index(p)
        cod = [(C0 + (('PARTE', j),)) if i % 2 == 0 else C0 for i in range(n0)]
        _CFG.update(spec=M[m][0], niebla=M[m][1], brazo=b, base='MUT0', codigo=cod)
        una(s, b, tl, carpeta, f"{p}_{'ON' if b == 'CUERPO' else 'MUDO'}_{m}", log)
    flog.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mundos', default='quieto'); ap.add_argument('--semillas', default='31001'); ap.add_argument('--brazos', default='CUERPO')
    ap.add_argument('--tl', default='largo'); ap.add_argument('--bloque', type=int, default=0); ap.add_argument('--de', type=int, default=1)
    ap.add_argument('--cal', action='store_true'); ap.add_argument('--ronda', type=int, default=1)
    a = ap.parse_args()
    sem = [int(s) for s in a.semillas.split(',')]
    if any(not 31001 <= s <= 31999 for s in sem): raise SystemExit('CUERPO: semillas 31001-31999')
    if not 0 <= a.bloque < a.de: raise SystemExit('CUERPO: --bloque K --de N con 0 <= K < N')
    if a.cal: calibra(a.ronda, sem, a.bloque, a.de)
    else:
        br = a.brazos.split(','); mu = a.mundos.split(',')
        if any(b not in ALFS for b in br): raise SystemExit(f'CUERPO: brazos {tuple(ALFS)}')
        if any(m not in ('quieto', 'onda8k', 'veneno', 'niebla') for m in mu): raise SystemExit('CUERPO: mundos quieto, onda8k, veneno, niebla')
        MAG_USO[0] = dict(MAG_RONDAS[max(MAG_RONDAS)])
        corre(mu, sem, br, a.tl, a.bloque, a.de)
