"""audita_pc_eco_sel_largo.py — AUDITORIA EN EL PC (solo lectura del instrumento de la nube; 1 proceso, sin Pool). 28-sep-2026.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

Corre sobre una COPIA del arbol de origin/nube/eco-sel-largo-20260928 (c08dc32) extraida con git archive (sin datos), NO sobre el repo.
  (X1) el humo de la nube (45491, T 200 000) repetido en el PC == el JSON de la nube, en TODAS las claves de cada corrida salvo seg
       (cruce de maquina: Linux py3.13 contra Windows py3.14).
  (X2) UNA corrida a T = 1e6 (SEL_C, semilla 45301 de la serie de eco_sel) con el nucleo LARGO == el JSON COMMITEADO de la serie de
       eco_sel (organelos, datos/eco_sel_serie_s45301-45320/SEL_C_s45301.json) en TODAS sus claves salvo seg; la unica clave nueva es
       'ventanas'. Mide el tiempo, el checkpoint (t, bytes, s) y la memoria pico: es la medida de costo que pide el coordinador.
Uso: python audita_pc_eco_sel_largo.py <raiz de la copia> <raiz del repo organelos> <json del humo de la nube> <json del humo del PC>
"""
import json, os, sys, tempfile, time

COPIA, REPO, HUMO_NUBE, HUMO_PC = sys.argv[1:5]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
sys.path.insert(0, os.path.join(COPIA, 'experimentos', 'organelos', 'eco_sel_largo'))
import corre_eco_sel_largo as C   # noqa: E402
import resource                   # noqa: E402  (stub de Windows por PYTHONPATH; solo memoria)

out = dict(copia=COPIA, shas=C.SHAS())
# (X1) humo nube == humo PC
a = json.load(open(HUMO_NUBE, encoding='utf-8')); b = json.load(open(HUMO_PC, encoding='utf-8'))
ra = {x['brazo']: x for x in a['R']}; rb = {x['brazo']: x for x in b['R']}
x1 = {}
for br in ra:
    d = [k for k in ra[br] if k != 'seg' and J(ra[br][k]) != J(rb[br].get(k))]
    x1[br] = dict(distintas=d, faltan=[k for k in ra[br] if k not in rb[br]], seg_nube=ra[br]['seg'], seg_pc=rb[br]['seg'])
ok1 = all(not v['distintas'] and not v['faltan'] for v in x1.values()) and set(ra) == set(rb)
out['X1'] = dict(ok=ok1, por_brazo=x1, veredicto_nube=a['veredicto_de_prueba'], veredicto_pc=b['veredicto_de_prueba'])
print(f"(X1) humo de la nube (45491, T 200 000) == humo del PC en todas las claves salvo seg: {'OK' if ok1 else 'MAL'} {x1}", flush=True)
# (X2) una corrida a 1e6 contra el JSON commiteado de eco_sel
C.verifica(); C.usa_gemelo()
T6 = 1_000_000
ref = json.load(open(os.path.join(REPO, 'experimentos', 'organelos', 'eco_sel', 'datos', 'eco_sel_serie_s45301-45320', 'SEL_C_s45301.json'),
                     encoding='utf-8'))
reg = []; orig = C._mide_ckpt(reg); t0 = time.time()
try:
    y = C.trabajo((45301, 'SEL_C', T6, 1, C.N.FRIO['T_lect'], tempfile.mkdtemp(prefix='audita_esl_'), False))
finally:
    C.CR.ME.run_solapadas = orig
seg = round(time.time() - t0, 1)
dist = [k for k in ref if k != 'seg' and J(ref[k]) != J(y.get(k))]
nuevas = sorted(set(y) - set(ref))
ok2 = not dist and nuevas == ['ventanas']
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
out['X2'] = dict(ok=ok2, distintas=dist, nuevas=nuevas, seg_pc=seg, seg_serie_eco_sel=ref.get('seg'), K_eco_sel=C.kbar(ref, T6),
                 K_largo=C.kbar(y, T6), K_por_ventana_1e5=C.kcurva(y, T6), ckpt=reg, rss_mb=round(rss),
                 json_bytes=len(json.dumps(y)))
print(f"(X2) T 1e6 SEL_C s45301, nucleo LARGO == JSON commiteado de la serie eco_sel en todas sus claves salvo seg; nueva solo 'ventanas': "
      f"{'OK' if ok2 else 'MAL'} (distintas {dist}; nuevas {nuevas}; K {round(C.kbar(y, T6), 3)} vs {round(C.kbar(ref, T6), 3)}; "
      f"{seg} s en el PC; en la serie de eco_sel (Pool 6) {ref.get('seg')} s; checkpoint (t, bytes, s) {reg}; memoria pico {round(rss)} MB; "
      f"JSON {len(json.dumps(y))} bytes)", flush=True)
out['TOTAL'] = f"{int(ok1) + int(ok2)}/2"
print(f"AUDITORIA PC: {out['TOTAL']}", flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"audita_pc_eco_sel_largo_{time.strftime('%Y%m%d_%H%M%S')}.json"), 'w',
                    encoding='utf-8'), default=str, indent=1)
