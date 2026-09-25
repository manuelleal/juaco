# EXPLORATORIO, no es dato (arnes del instrumento de la serie)
"""identidad_serie.py — arnes N/N de PROMETEO SERIE (Opus, 25-sep-2026). MISION: llegar a la AGI por este camino.
Todas las corridas: onda8k (spec), T 6000, semilla 30191 (fuera de serie/replica/humo), w30.

Lo de antes (el 8/8 de identidad_prometeo.py), ahora contra motor_serie con mudo = 0:
 S1  CODIGO_SIN_SOS, alfabeto v0: motor_serie == motor_fable BIT A BIT.
 S2  PERILLAS: motor_serie == motor_fable BIT A BIT.
 S3  PROMETEO completo (alfabeto con kit, copia ON, fundadores con un CABLE de boca y un slot nuevo): motor_serie (mudo 0) == motor_prometeo BIT A BIT
     (firma entera + contadores del kit).
 S4-S8  piezas del kit (copia apagada): CABLE parto veta todo · CABLE boca baja mordidas · CABLE patas mueve · HGT inserta · CABLE peso 0 = nada.
Lo nuevo:
 M1  MUDO + CABLE(reserva->parto, -3): la dinamica == MUT0 sin el cable (BIT A BIT) y los contadores del kit son 0.
 M2  MUDO + CABLE(sesgo->boca, -3): == MUT0 sin el cable.
 M3  MUDO + ORG(vida/todo/hijo/copiar) en la cinta: == MUT0 sin el slot; y en PROMETEO el MISMO slot SI cambia la dinamica.
 M4  MUDO + HGT: la HGT sigue actuando (eventos > 0).
 M5  MUDO con copia ON: la cinta ARMA organos (algun organo funcional en el banco final) y el organo EXPRESADO de todos los vivos es FILTRA0.
 M6  (ERR-144) en MUDO el suministro de organos armados se lee en la CINTA (de novo > 0); la columna vieja (organo expresado) es 0.
 R1  reanudar desde el checkpoint (t 4000) == de un tiron, con un CABLE de boca activo (el rng del kit entra al checkpoint).
 L1  claves(): CINTA0 sin organos; CABLE parto +2 inerte; CABLE parto -1 funcional; ORG cuando=nunca inerte; filtra0 duplicado no cuenta.
 L2  la letra: cada rama de veredicto() con datos sinteticos (FUNCIONA, MODESTO, NO, NO EVALUABLE por guardia, por MUDO que actua, incompleta).
 B1  banderas malas abortan (ERR-115) sin escribir nada.
"""
import os, sys, json, hashlib, subprocess, copy
AQUI = os.path.dirname(os.path.abspath(__file__)); PROM = os.path.dirname(AQUI); ORG = os.path.dirname(PROM)
CODIGO = os.path.join(ORG, 'codigo'); FABLE = os.path.join(CODIGO, 'exploracion_fable')
for d in (FABLE, CODIGO, PROM, AQUI):
    if d in sys.path: sys.path.remove(d)
    sys.path.insert(0, d)
import corre_codigo as CC
_ECO0 = CC.eco_de   # el eco_de ORIGINAL (corre_serie lo reemplaza al importarse)
import motor_fable as MF
import motor_prometeo as MP
import motor_serie as MS
import codigo_prometeo as CP
import fable_mundos as FB
import gramatica_def as GD
import corre_serie as SE
CC.eco_de = _ECO0

SPEC = FB.catalogo(2000)['onda8k']; SEED = 30191; T = 6000
C0 = CC.CINTA0; n0 = CC.MUNDO['n0']


def firma(r, kit=False):
    d = dict(lin=[(l['deaths'], l['nacimientos'], l['tam'], l['mord']) for l in r['linajes']], eco=r['eco']['n_nac'], t_ext=r['eco']['t_ext'],
             cod=r.get('codigo', {}).get('cod_nac'))
    if kit: d['kit'] = (r.get('codigo', {}).get('prometeo') or {}).get('kit')
    return hashlib.sha256(json.dumps(d, sort_keys=True, default=str).encode()).hexdigest()[:16]


def firma_din(r):
    s = json.dumps(dict(lin=[(l['deaths'], l['nacimientos'], l['tam'], l['mord']) for l in r['linajes']], eco=r['eco']['n_nac'], t_ext=r['eco']['t_ext'],
                        viv=r['eco']['vivos_final']), sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def corre(mod, brazo, **extra):
    eco = CC.eco_de(brazo, 4500, 2000, **extra); eco['cambio'] = dict(SPEC)
    return mod.run_solapadas(SEED, [CC.CARRO] * n0, T=T, diag=0, mundo_n=CC.MUNDO['esc'], tope_cuerpos=CC.MUNDO['tope'], muestra=CC.BASE['muestra'], eco=eco)


ok = 0; tot = 0
def chk(nombre, cond):
    global ok, tot
    tot += 1; ok += int(bool(cond)); print(('OK  ' if cond else 'MAL ') + nombre, flush=True)

def mord(r): return sum(sum(v) for l in r['linajes'] for v in l['mord'].values())
def kit(r): return (r.get('codigo', {}).get('prometeo') or {}).get('kit') or {}
def con(*ins): return [tuple(C0) + tuple(ins)] * n0
def cero(k): return not any((k.get(z) or 0) for z in ('boca_si', 'boca_no', 'pata_mueve', 'pata_para', 'veto'))


def b1():
    malas = [['--humo'], ['--humo', '--mundo', 'golpe'], ['--serie', '--ventana', 'serie'], ['--serie', '--ventana', 'serie', '--pool', '7'],
             ['--seri', '--ventana', 'serie', '--pool', '6'], ['--serie', '--ventana=serie', '--pool', '6'], ['--lee', 'x', '--reanuda'], ['--humo', '--mundo', 'quieto', '--humo']]
    antes = sorted(os.listdir(os.path.join(AQUI, 'datos'))) if os.path.isdir(os.path.join(AQUI, 'datos')) else []
    cod = [subprocess.run([sys.executable, os.path.join(AQUI, 'corre_serie.py')] + m, capture_output=True).returncode for m in malas]
    despues = sorted(os.listdir(os.path.join(AQUI, 'datos'))) if os.path.isdir(os.path.join(AQUI, 'datos')) else []
    chk(f"B1 banderas malas abortan con 2 y no escriben nada: {cod}", all(c == 2 for c in cod) and antes == despues)


if '--solo_b1' in sys.argv:
    b1(); print(f'IDENTIDAD SERIE (solo B1): {ok}/{tot}'); sys.exit(0)

# ---------------- S: lo de antes
CP.pon_alfabeto(CP.OPS)
for i, brazo in enumerate(('CODIGO_SIN_SOS', 'PERILLAS')):
    a = firma(corre(MF, brazo)); b = firma(corre(MS, brazo))
    chk(f'S{i + 1} {brazo}: serie == fable ({a} / {b})', a == b)
CP.pon_alfabeto(CP.OPS + CP.KIT)
PK = con(('CABLE', 1, 0, -2), ('ORG', 2, 2, 0, 1))
a = firma(corre(MP, 'CODIGO_SIN_SOS', codigo=PK), kit=True); b = firma(corre(MS, 'CODIGO_SIN_SOS', codigo=PK), kit=True)
chk(f'S3 PROMETEO completo (kit, copia ON, cable + slot): serie (mudo 0) == prometeo ({a} / {b})', a == b)
r0 = corre(MS, 'MUT0'); n_v0 = r0['eco']['n_nac']; m_v0 = mord(r0); d0 = firma_din(r0)
r = corre(MS, 'MUT0', codigo=con(('CABLE', 1, 2, -3)))
chk(f"S4 CABLE reserva->parto -3: nacimientos {r['eco']['n_nac']} (v0 {n_v0})", r['eco']['n_nac'] == 0 and n_v0 > 0)
r = corre(MS, 'MUT0', codigo=con(('CABLE', 0, 0, -3)))
chk(f"S5 CABLE sesgo->boca -3: mordidas {mord(r)} (v0 {m_v0}); boca_no {kit(r).get('boca_no')}", mord(r) < m_v0 and kit(r).get('boca_no', 0) > 0)
r = corre(MS, 'MUT0', codigo=con(('CABLE', 0, 1, 3)))
chk(f"S6 CABLE sesgo->patas +3: pata_mueve {kit(r).get('pata_mueve')}", kit(r).get('pata_mueve', 0) > 0 and firma_din(r) != d0)
r = corre(MS, 'MUT0', codigo=con(('HGT', 3, 3)))
lg = [len(c) for c in r['codigo']['prometeo']['banco_final']]
chk(f"S7 HGT(0.25, 8): eventos {kit(r).get('hgt')}; largo banco final {min(lg)}-{max(lg)}", kit(r).get('hgt', 0) > 0 and max(lg) > len(C0) + 1)
r = corre(MS, 'MUT0', codigo=con(('CABLE', 3, 2, 0)))
chk(f"S8 CABLE peso 0: dinamica == MUT0 ({firma_din(r)} / {d0})", firma_din(r) == d0)
# ---------------- M: el control MUDO
r = corre(MS, 'MUT0', mudo=1, codigo=con(('CABLE', 1, 2, -3)))
chk(f"M1 MUDO + CABLE reserva->parto -3: dinamica == MUT0 ({firma_din(r)} / {d0}); kit {kit(r)}", firma_din(r) == d0 and cero(kit(r)))
r = corre(MS, 'MUT0', mudo=1, codigo=con(('CABLE', 0, 0, -3)))
chk(f"M2 MUDO + CABLE sesgo->boca -3: == MUT0 ({firma_din(r)})", firma_din(r) == d0 and cero(kit(r)))
r = corre(MS, 'MUT0', mudo=1, codigo=con(('ORG', 2, 0, 0, 0))); rp = corre(MS, 'MUT0', codigo=con(('ORG', 2, 0, 0, 0)))
chk(f"M3 MUDO + ORG vida/todo/hijo/copiar: == MUT0 ({firma_din(r)}); en PROMETEO el slot cambia la dinamica ({firma_din(rp)})",
    firma_din(r) == d0 and firma_din(rp) != d0)
r = corre(MS, 'MUT0', mudo=1, codigo=con(('HGT', 3, 3)))
chk(f"M4 MUDO + HGT: eventos {kit(r).get('hgt')}", kit(r).get('hgt', 0) > 0)
r = corre(MS, 'CODIGO_SIN_SOS', mudo=1, codigo=con(('HGT', 3, 3)))
bf = r['codigo']['prometeo']['banco_final']; nfun = sum(1 for c in bf if SE.claves(c)[0])
vg = r['gram']['vivos_gr']; expr = all(tuple(tuple(s) for s in v[4]) == tuple(GD.FILTRA0) for v in vg)
chk(f"M5 MUDO copia ON: cintas del banco final con organo funcional {nfun}/{len(bf)}; organo expresado de los {len(vg)} vivos = FILTRA0: {expr}",
    nfun > 0 and expr and len(vg) > 0)
kn = r['codigo']['prometeo']['kit_nac']; dn = sum(z[5] for z in kn); co = sum(z[6] for z in kn)
chk(f"M6 (ERR-144) MUDO: el suministro se lee en la CINTA: nacidos con organo armado de novo {dn}, con organo {co} (de {len(kn)}); columna vieja del organo expresado {sum(z[4] for z in kn)} (= 0)",
    dn > 0 and co > 0 and sum(z[4] for z in kn) == 0)
# ---------------- R1: reanudar
ck = {}
def guarda(t, blob): ck[t] = blob
eco = CC.eco_de('CODIGO_SIN_SOS', 4500, 2000, codigo=con(('CABLE', 0, 0, -2), ('CABLE', 0, 1, 2))); eco['cambio'] = dict(SPEC)
e1 = dict(eco, ckpt_cada=2000, ckpt_fn=guarda)
ra = MS.run_solapadas(SEED, [CC.CARRO] * n0, T=T, diag=0, mundo_n=CC.MUNDO['esc'], tope_cuerpos=CC.MUNDO['tope'], muestra=CC.BASE['muestra'], eco=e1)
e2 = dict(eco, estado=ck[4000])
rb = MS.run_solapadas(SEED, [CC.CARRO] * n0, T=T, diag=0, mundo_n=CC.MUNDO['esc'], tope_cuerpos=CC.MUNDO['tope'], muestra=CC.BASE['muestra'], eco=e2)
chk(f"R1 reanudar en t 4000 == de un tiron ({firma(ra, True)} / {firma(rb, True)}); kit {kit(ra)}", firma(ra, True) == firma(rb, True) and not cero(kit(ra)))
# ---------------- L1: claves
f0 = SE.claves(C0); f1 = SE.claves(tuple(C0) + (('CABLE', 1, 2, 2),)); f2 = SE.claves(tuple(C0) + (('CABLE', 1, 2, -1),))
f3 = SE.claves(tuple(C0) + (('ORG', 0, 1, 1, 1),)); f4 = SE.claves(tuple(C0) + (('ORG', 1, 3, 0, 0),)); f5 = SE.claves(tuple(C0) + (('HGT', 0, 0),))
chk(f"L1 claves: CINTA0 {f0} · parto+2 {f1} · parto-1 {f2} · ORG nunca {f3} · filtra0 x2 {f4} · HGT {f5}",
    f0 == (set(), set(), False) and f1 == (set(), {'reserva->parto+'}, False) and f2 == ({'reserva->parto-'}, set(), False)
    and f3 == (set(), {'ORG nunca/neg/hermano/promediar'}, False) and f4 == (set(), set(), False) and f5 == (set(), set(), True))
# ---------------- L2: la letra con datos sinteticos
def fake(m, b, s, F, sup=0.1, ns=100, kitd=None):
    return dict(mundo_serie=m, brazo=b, seed=s, serie_ok=1, abortado=None, bloqueados=0, nac_solo=ns, persiste=1,
                prometeo=dict(kit=(kitd or {}), suministro=dict(n=100, de_novo=sup, con_organo=0.3), organos=dict(F=F, F_inerte=0.1, fijos=[], hgt_final=0.2)))
def mundo(m, fP, fM, sup_m=0.1, nsP=100, kitM=None):
    return [fake(m, 'PROMETEO', s, fP(s), ns=nsP) for s in range(20)] + [fake(m, 'MUDO', s, fM(s), sup=sup_m, kitd=kitM) for s in range(20)]
alto = lambda s: 0.8 if s < 16 else 0.1; bajo = lambda s: 0.2 if s < 18 else 0.6
casos = {
    'FUNCIONA': mundo('quieto', alto, bajo) + mundo('onda8k', alto, bajo),
    'HAY ALGO MODESTO': mundo('quieto', alto, bajo) + mundo('onda8k', bajo, bajo),
    'NO —': mundo('quieto', bajo, bajo) + mundo('onda8k', bajo, alto),
    'NO EVALUABLE (guardia': mundo('quieto', alto, bajo, sup_m=0.01) + mundo('onda8k', alto, bajo),
    'NO EVALUABLE (el control MUDO actuo': mundo('quieto', alto, bajo, kitM={'boca_no': 3}) + mundo('onda8k', alto, bajo),
    'NO EVALUABLE (ventana incompleta': mundo('quieto', alto, bajo)[:-1] + mundo('onda8k', alto, bajo),
}
bien = True; out = []
for esperado, R in casos.items():
    v, p2, L = SE.veredicto(R); out.append(v[:40]); bien = bien and v.startswith(esperado)
Rp2 = mundo('quieto', alto, bajo) + mundo('onda8k', alto, bajo, nsP=1500)
v, p2, L = SE.veredicto(Rp2); bien = bien and p2; v, p2b, L = SE.veredicto(casos['FUNCIONA']); bien = bien and not p2b
chk(f"L2 la letra: {out} · P2 {p2}/{p2b}", bien)
# ---------------- B1: banderas (ERR-115). Con --sin_b1 se salta; con --solo_b1 corre SOLO B1 (lanza 8 subprocesos cortos: aparte, con CPU libre)
if '--sin_b1' not in sys.argv: b1()
print(f'IDENTIDAD SERIE: {ok}/{tot}')
