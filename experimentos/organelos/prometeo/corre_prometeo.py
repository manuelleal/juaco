# EXPLORATORIO, no es dato
"""corre_prometeo.py — runner EXPLORATORIO de PROMETEO (Opus, equipo organelos, 24-sep-2026). MISION: llegar a la AGI por este camino.

Reusa corre_codigo.trabajo() SIN tocarlo (monkeypatch SOLO en este proceso: el motor pasa a motor_prometeo y eco_de agrega el mundo
de fable_mundos y el alfabeto del brazo). Un proceso por invocacion; dentro, las corridas van UNA TRAS OTRA (sin Pool). Semillas 30001-30999.
Brazos:
  PROMETEO          cinta v0 (FILTRA0 + perillas de fabrica), SOS NO se lee (= CODIGO_SIN_SOS) + alfabeto con CABLE y HGT
  PROMETEO_SIN_HGT  lo mismo con alfabeto + CABLE solo (la HGT no puede aparecer)
  CODIGO_SIN_SOS    el codigo v0 sin SOS, alfabeto v0 (sin kit)
  PERILLAS          el genoma de hoy (mutacion numerica + errores de la gramatica)
Uso:
  python corre_prometeo.py --mundo onda8k --brazos PROMETEO --semillas 30001,30002 [--tl largo]
"""
import argparse, json, os, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); ORG = os.path.dirname(AQUI)
CODIGO = os.path.join(ORG, 'codigo'); FABLE = os.path.join(CODIGO, 'exploracion_fable')
for d in (FABLE, CODIGO, AQUI):
    if d in sys.path: sys.path.remove(d)
    sys.path.insert(0, d)
import motor_prometeo as MP
import codigo_prometeo as CP
import corre_codigo as CC
import fable_mundos as FB

DATOS = os.path.join(AQUI, 'datos')
TLS = dict(corto=dict(T=36000, t_cambio=8000, t_corte=24000, r0_margen=4000),
           largo=dict(T=60000, t_cambio=8000, t_corte=44000, r0_margen=4000),
           humo=dict(T=6000, t_cambio=2000, t_corte=4000, r0_margen=1000))
ALFS = dict(PROMETEO=CP.OPS + CP.KIT, PROMETEO_SIN_HGT=CP.OPS + ('CABLE',), CODIGO_SIN_SOS=CP.OPS, PERILLAS=CP.OPS)
_eco_de0 = CC.eco_de
_SPEC = [None]; _ULTR = [None]


def eco_de_prom(brazo, t_corte, t_cambio, **extra):
    base = 'PERILLAS' if brazo == 'PERILLAS' else 'CODIGO_SIN_SOS'
    CP.pon_alfabeto(ALFS[brazo])
    e = _eco_de0(base, t_corte, t_cambio, **extra)
    if _SPEC[0] is not None: e['cambio'] = dict(_SPEC[0])
    return e


class _Shim:
    NOMBRES = MP.NOMBRES
    @staticmethod
    def run_solapadas(*a, **k):
        r = MP.run_solapadas(*a, **k); _ULTR[0] = r; return r


CC.MC = _Shim; CC.eco_de = eco_de_prom


def resume_kit(kn, T, W=2000):
    """kit_nac = [t, largo, n cables != 0, tiene HGT, slots ORG != filtra0] por nacimiento -> por ventana de W."""
    out = []
    a = np.array(kn, float) if kn else np.zeros((0, 5))
    for s in range(0, T, W):
        m = (a[:, 0] >= s) & (a[:, 0] < s + W) if len(a) else np.zeros(0, bool)
        if not m.any(): out.append([s, 0, None, None, None, None]); continue
        b = a[m]
        out.append([s, int(m.sum()), round(float(b[:, 1].mean()), 2), round(float((b[:, 2] > 0).mean()), 4),
                    round(float((b[:, 3] > 0).mean()), 4), round(float((b[:, 4] > 0).mean()), 4)])
    return out


def corre(mundo, semillas, brazos, tl_nombre):
    tl = dict(TLS[tl_nombre]); spec = FB.catalogo(tl['t_cambio'])[mundo]; _SPEC[0] = spec
    carpeta = os.path.join(DATOS, f"{mundo}_{tl_nombre}"); os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')
    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"EXPLORATORIO PROMETEO mundo {mundo} {spec} · {tl} · brazos {brazos} · semillas {semillas}")
    for s in semillas:
        for b in brazos:
            fin = os.path.join(carpeta, f"{b}_s{s}.json")
            if os.path.exists(fin): log(f"ya existe {os.path.basename(fin)}"); continue
            _ULTR[0] = None
            x = CC.trabajo((s, b, tl, carpeta, False))
            r = _ULTR[0]
            pr = (r or {}).get('codigo', {}).get('prometeo') if r else None
            if pr is not None:
                pr = dict(pr); pr['kit_ventanas'] = resume_kit(pr.pop('kit_nac', []), tl['T']); pr['n_hgt_ev'] = len(pr.get('hgt_ev') or [])
                pr['hgt_ev'] = (pr.get('hgt_ev') or [])[:2000]
            x['prometeo'] = pr; x['mundo_fable'] = dict(nombre=mundo, spec=spec); x['alfabeto'] = list(ALFS[b])
            with open(fin, 'w', encoding='utf-8') as f: json.dump(x, f)
            kit = (pr or {}).get('kit')
            log(f"{b:<17} s{s}: {x.get('seg')} s · persiste {x.get('persiste')} (vivos {x.get('vivos_T')}) · n_nac {x.get('n_nac')} · "
                f"R0 final {x.get('r0_final')} (n {x.get('n_final')}) · kit {kit} · abortado {x.get('abortado')}")
    flog.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mundo', required=True); ap.add_argument('--semillas', default='30001'); ap.add_argument('--brazos', default='PROMETEO')
    ap.add_argument('--tl', default='largo')
    a = ap.parse_args()
    sem = [int(s) for s in a.semillas.split(',')]; br = a.brazos.split(',')
    if any(not 30001 <= s <= 30999 for s in sem): raise SystemExit('PROMETEO: semillas 30001-30999')
    if any(b not in ALFS for b in br): raise SystemExit(f'PROMETEO: brazos {tuple(ALFS)}')
    corre(a.mundo, sem, br, a.tl)
