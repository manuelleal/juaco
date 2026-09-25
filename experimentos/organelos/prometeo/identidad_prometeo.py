# EXPLORATORIO, no es dato
"""identidad_prometeo.py — arnes de PROMETEO (Opus, 24-sep-2026). MISION: llegar a la AGI por este camino.

IP1: kit ausente del alfabeto y de la cinta, sin HGT: motor_prometeo CODIGO_SIN_SOS == motor_fable CODIGO_SIN_SOS BIT A BIT (onda8k, T 6000).
IP2: lo mismo con PERILLAS (el motor nuevo no toca el genoma de hoy).
IP3: alfabeto CON kit pero kit ausente de la cinta y copia apagada (c_on=False): == motor_fable MUT0 bit a bit (el cuerpo sin cables no cambia nada).
Arnes por pieza (cinta fundadora = cinta v0 + UNA instruccion del kit; copia apagada para aislar la pieza):
IK1 CABLE(reserva -> parto, -3): veta TODAS las ventanas -> 0 nacimientos (v0: > 0).
IK2 CABLE(sesgo -> boca, -3): la boca se niega -> mordidas totales bajan y boca_no > 0.
IK3 CABLE(sesgo -> patas, +3): el cuerpo quieto da pasos -> pata_mueve > 0 y la firma cambia.
IK4 HGT(0.25, 8) con copia apagada: hay eventos HGT (> 0) y la cinta de los hijos crece; sin HGT: 0 eventos.
IK5 CABLE con peso 0 (neutro): la DINAMICA == MUT0 bit a bit (la insercion neutra de un cable no cambia nada).
Cambio de criterio declarado (22:10, tras la 1a corrida 6/8): IK4 miraba las cintas de los VIVOS en T (fundadores repuestos: 31) -> ahora el
banco final; IK5 comparaba la firma con cod_nac, que guarda el LARGO de la cinta (31 vs 30) -> ahora la firma de la dinamica.
"""
import os, sys, json, hashlib
AQUI = os.path.dirname(os.path.abspath(__file__)); ORG = os.path.dirname(AQUI)
CODIGO = os.path.join(ORG, 'codigo'); FABLE = os.path.join(CODIGO, 'exploracion_fable')
for d in (FABLE, CODIGO, AQUI): sys.path.insert(0, d)
import corre_codigo as CC
import motor_fable as MF
import motor_prometeo as MP
import codigo_prometeo as CP
import fable_mundos as FB

SPEC = FB.catalogo(2000)['onda8k']


def firma(r):
    s = json.dumps(dict(lin=[(l['deaths'], l['nacimientos'], l['tam'], l['mord']) for l in r['linajes']], eco=r['eco']['n_nac'], t_ext=r['eco']['t_ext'],
                        cod=r.get('codigo', {}).get('cod_nac')), sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def corre(mod, brazo, seed=30001, T=6000, **extra):
    eco = CC.eco_de(brazo, 4500, 2000, **extra); eco['cambio'] = dict(SPEC)
    return mod.run_solapadas(seed, [CC.CARRO] * CC.MUNDO['n0'], T=T, diag=0, mundo_n=CC.MUNDO['esc'], tope_cuerpos=CC.MUNDO['tope'], muestra=CC.BASE['muestra'], eco=eco)


def firma_din(r):   # sin cod_nac (que registra el LARGO de la cinta: con una instruccion mas, difiere aunque la dinamica sea identica)
    s = json.dumps(dict(lin=[(l['deaths'], l['nacimientos'], l['tam'], l['mord']) for l in r['linajes']], eco=r['eco']['n_nac'], t_ext=r['eco']['t_ext'],
                        viv=r['eco']['vivos_final']), sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


ok = 0; tot = 0
def chk(nombre, cond):
    global ok, tot
    tot += 1; ok += int(bool(cond)); print(('OK  ' if cond else 'MAL ') + nombre, flush=True)

def mord(r): return sum(sum(v) for l in r['linajes'] for v in l['mord'].values())
def kit(r): return (r.get('codigo', {}).get('prometeo') or {}).get('kit') or {}

CP.pon_alfabeto(CP.OPS)
for brazo in ('CODIGO_SIN_SOS', 'PERILLAS'):
    a = firma(corre(MF, brazo)); b = firma(corre(MP, brazo))
    chk(f'IP{1 if brazo != "PERILLAS" else 2} {brazo}: prometeo == fable ({a} / {b})', a == b)
CP.pon_alfabeto(CP.OPS + CP.KIT)
a = firma(corre(MF, 'MUT0')); b = firma(corre(MP, 'MUT0'))
chk(f'IP3 alfabeto con kit, cinta sin kit, copia apagada: == MUT0 ({a} / {b})', a == b)
C0 = CC.CINTA0; n0 = CC.MUNDO['n0']
def con(ins): return [tuple(C0) + (ins,)] * n0
r0 = corre(MP, 'MUT0'); n_v0 = r0['eco']['n_nac']; m_v0 = mord(r0)
r = corre(MP, 'MUT0', codigo=con(('CABLE', 1, 2, -3)))
chk(f"IK1 CABLE reserva->parto -3: nacimientos {r['eco']['n_nac']} (v0 {n_v0}); vetos {kit(r).get('veto')}", r['eco']['n_nac'] == 0 and n_v0 > 0)
r = corre(MP, 'MUT0', codigo=con(('CABLE', 0, 0, -3)))
chk(f"IK2 CABLE sesgo->boca -3: mordidas {mord(r)} (v0 {m_v0}); boca_no {kit(r).get('boca_no')}", mord(r) < m_v0 and kit(r).get('boca_no', 0) > 0)
r = corre(MP, 'MUT0', codigo=con(('CABLE', 0, 1, 3)))
chk(f"IK3 CABLE sesgo->patas +3: pata_mueve {kit(r).get('pata_mueve')}; firma cambia", kit(r).get('pata_mueve', 0) > 0 and firma(r) != firma(r0))
r = corre(MP, 'MUT0', codigo=con(('HGT', 3, 3)))
lg = [len(c) for c in r['codigo']['prometeo']['banco_final']]
chk(f"IK4 HGT(0.25, 8): eventos {kit(r).get('hgt')}; largo en el banco final {min(lg) if lg else None}-{max(lg) if lg else None} (fundadora {len(C0) + 1}); sin HGT: {kit(r0).get('hgt', 0)}",
    kit(r).get('hgt', 0) > 0 and kit(r0).get('hgt', 0) == 0 and max(lg) > len(C0) + 1)
r = corre(MP, 'MUT0', codigo=con(('CABLE', 3, 2, 0)))
chk(f"IK5 CABLE peso 0: dinamica == MUT0 bit a bit ({firma_din(r)} / {firma_din(r0)}; la firma completa difiere solo por el largo de la cinta en cod_nac)", firma_din(r) == firma_din(r0))
print(f'IDENTIDAD PROMETEO: {ok}/{tot}')
