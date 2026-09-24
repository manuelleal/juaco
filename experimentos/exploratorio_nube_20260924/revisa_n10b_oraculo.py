"""revisa_n10b_oraculo.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Revisión de la alarma del §8 de PREREGISTRO_n10b:
"RES por encima del ORÁCULO en >= 15/20 sería sospechoso; revisar antes de leer". En la serie 12701–12720 pasó 20/20
(RES 0.688 contra ORÁCULO 0.520).

Hipótesis H-NEUTRAS: la tabla del ORÁCULO trae las 8 entradas (4 letras x 2 necesidades), incluidas 4 NEUTRAS (R = 0: A y B con
sed, C y D con hambre). Por la vía lenta, cada entrada neutra entrena a 0 el valor de esa letra en esa necesidad y borra la
generalización entre letras que comparten píxeles (p. ej. D|sed = -3 generaliza a B por los píxeles 2 y 4; B|sed = 0 la
cancela). La boca decide con el valor de la necesidad DOMINANTE, así que con sed el hijo del ORÁCULO ve B "neutro" y lo muerde
(pierde E). Las tablas de RES suelen estar incompletas (6-7 claves) y conservan esa generalización protectora.
Predicción: ORA_SIN0 (la tabla verdadera SIN las entradas neutras) >= RES y > ORÁCULO. Si ORA_SIN0 <= ORÁCULO, la hipótesis cae y
la alarma queda abierta (instrumento a revisar).

Instrumento: corre_n10b.tarea SIN TOCAR (mismo mundo, mismo juez, mismas medidas); sólo se sustituye el módulo del carro de
'ORACULO' por una subclase de FAMB_ORACULO que filtra self._ORA. Semillas de PRÁCTICA de n10b 12794–12799 (el arnés usó
12791–12793 y el humo 12791). T = 100 000, un proceso.
Uso: python experimentos/exploratorio_nube_20260924/revisa_n10b_oraculo.py [--n 6] [--desde 12794]
"""
import argparse, json, os, statistics as st, sys, time, types

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'subida_n10b'))
import corre_n10b as CN

_carga_orig = CN.carga
_VAR = {'modo': None}


def _variante_sin0():
    m0 = _carga_orig('ORACULO')

    class Sin0(m0.Carro):
        def __init__(self, ctx):
            super().__init__(ctx)
            self._ORA = [e for e in self._ORA if e[1] != 0.0]
    m = types.ModuleType('carro_FAMB_ORA_SIN0')
    m.crea = lambda ctx: Sin0(ctx)
    return m


def _variante_res_sin0():
    m0 = _carga_orig('RES')

    class ResSin0(m0.Carro):
        def nace(self, info):
            m = info.get('memoria')
            if m:
                info = dict(info, memoria=[e for e in m if float(e[1]) != 0.0])
            return super().nace(info)
    m = types.ModuleType('carro_FAMB_RES_SIN0')
    m.crea = lambda ctx: ResSin0(ctx)
    return m


def carga(et):
    if et == 'ORACULO' and _VAR['modo'] == 'sin0':
        return _variante_sin0()
    if et == 'RES' and _VAR['modo'] == 'res_sin0':
        return _variante_res_sin0()
    return _carga_orig(et)


CN.carga = carga


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--desde', type=int, default=12794)
    ap.add_argument('--n', type=int, default=6)
    ap.add_argument('--T', type=int, default=100000)
    ap.add_argument('--brazos', default='NADA,RES,ORACULO,ORA_SIN0')
    a = ap.parse_args()
    sem = range(a.desde, a.desde + a.n)
    if not (all(12794 <= x <= 12799 for x in sem) or all(24001 <= x <= 24099 for x in sem)):
        raise SystemExit('solo semillas de practica 12794-12799 o exploratorias 24001-24099')
    TABLA = {'NADA': ('NADA', None), 'RES': ('RES', None), 'ORACULO': ('ORACULO', None), 'ORA_SIN0': ('ORACULO', 'sin0'),
             'RES_SIN0': ('RES', 'res_sin0'), 'RES1': ('RES1', None), 'BAR': ('BAR', None)}
    brazos = [(b,) + TABLA[b] for b in a.brazos.split(',')]
    os.makedirs(os.path.join(AQUI, 'datos'), exist_ok=True)
    base = os.path.join(AQUI, 'datos', f"revisa_n10b_{a.brazos.replace(',', '-')}_s{a.desde}-{a.desde + a.n - 1}_T{a.T}_{time.strftime('%Y%m%d_%H%M%S')}")
    flog = open(base + '.log', 'w', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log('EXPLORATORIO — no es dato · revisión de la alarma §8 de n10b (RES > ORÁCULO) · corre_n10b.tarea sin tocar')
    R = []
    for s in range(a.desde, a.desde + a.n):
        for nombre, brazo, modo in brazos:
            _VAR['modo'] = modo
            r = CN.tarea((s, brazo, a.T))
            v = list(r['estr'].values())[0]
            x = dict(seed=s, brazo=nombre, R0_nacidos=v['R0_nacidos'], vida_nacidos=v['vida_nacidos'], nac=v['nac'],
                     exceso=v['exceso'], gen_max=v['gen_max'], frac_mala_nacidos=v.get('frac_mala_nacidos'), seg=r['seg'],
                     persisten=v.get('persisten'), persiste_carro=v.get('persiste_carro'), linajes_sin_ext=v.get('linajes_sin_ext'),
                     fundadores=v.get('fundadores'), tam_final=v.get('tam_final'))
            R.append(x)
            log(f"  s{s} {nombre:9s} R0nac {x['R0_nacidos']} vida_nac {x['vida_nacidos']} nac {x['nac']} exceso {x['exceso']} gen {x['gen_max']} "
                f"mala {x['frac_mala_nacidos']} persisten {x['persisten']} carro {x['persiste_carro']} sin_ext {x['linajes_sin_ext']} fund {x['fundadores']} tam_final {x['tam_final']} ({x['seg']} s)")
            json.dump(R, open(base + '.json', 'w', encoding='utf-8'), indent=1)
    log('RESUMEN (medianas por semilla)')
    for b in [x[0] for x in brazos]:
        xs = [x['R0_nacidos'] for x in R if x['brazo'] == b]
        log(f"  {b:9s} R0nac mediana {round(st.median(xs), 4)} · {xs}")
    por = lambda b: {x['seed']: x['R0_nacidos'] for x in R if x['brazo'] == b}
    nb = [x[0] for x in brazos]
    for a1, b1 in (('ORA_SIN0', 'ORACULO'), ('ORA_SIN0', 'RES'), ('RES', 'ORACULO'), ('RES_SIN0', 'RES'), ('RES_SIN0', 'ORA_SIN0'), ('RES_SIN0', 'NADA')):
        if a1 not in nb or b1 not in nb: continue
        pa, pb = por(a1), por(b1)
        d = [pa[s] - pb[s] for s in pa if s in pb]
        log(f"  pareado {a1} > {b1}: {sum(1 for z in d if z > 0)}/{len(d)} · dif mediana {round(st.median(d), 4)}")
    log(f"JSON: {os.path.relpath(base + '.json', RAIZ)}")


if __name__ == '__main__':
    main()
