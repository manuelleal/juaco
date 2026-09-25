# EXPLORATORIO, no es dato
"""identidad_cuerpo.py — arnes de PROMETEO-CUERPO (Opus, 25-sep-2026). MISION: llegar a la AGI por este camino.

Mundo onda8k (cambio en t 2000), T 6000, corte 4500, semilla 31001, 30 fundadores (w30), como identidad_prometeo.py.
IDENTIDAD (sin partes, el motor es Prometeo bit a bit):
  IC1 PROMETEO (alfabeto v0 + KIT, copia prendida): motor_cuerpo == motor_prometeo (firma completa + contadores del kit).
  IC2 CODIGO_SIN_SOS (alfabeto v0): motor_cuerpo == motor_prometeo.
  IC3 alfabeto CON PARTE, cinta sin partes, copia apagada (MUT0): motor_cuerpo == motor_prometeo MUT0.
  IC4 niebla de radio 600 (>= L/2: ve todo): == sin niebla (la copia del carro y la vista filtrada no cambian nada).
  IC5 niebla de radio 5: hay pasos ciegos y la dinamica cambia.
ARNES POR PIEZA (30 fundadores con cinta v0 + UNA copia de la parte; copia apagada para aislar la pieza):
  IB1 PATA: da pasos extra (> 0); MUDO: 0.        IB2 ESCUDO: dano evitado > 0; MUDO: 0.
  IB3 ESTOMAGO: reserva guardada por encima de 1.5 > 0; MUDO: 0.
  IB4 MANDIBULA: ganancia extra > 0; MUDO: 0.      IB5 LENGUA: escupidas > 0; MUDO: 0.
  IB6 OJO sin niebla: ON == MUDO bit a bit (el OJO es INERTE donde ya se ve todo).
  IB7 OJO con niebla 5: la fraccion de pasos ciegos baja con el OJO (ON < MUDO).
  IB8 COSTO: las 6 partes con costo 0 y efecto apagado == MUT0 bit a bit; con costo, se cobra (costo > 0) y la dinamica cambia.
"""
import os, sys, json, hashlib
AQUI = os.path.dirname(os.path.abspath(__file__)); ORG = os.path.dirname(AQUI)
CODIGO = os.path.join(ORG, 'codigo'); FABLE = os.path.join(CODIGO, 'exploracion_fable'); PROM = os.path.join(ORG, 'prometeo')
for d in (FABLE, CODIGO, PROM, AQUI): sys.path.insert(0, d)
import corre_codigo as CC
import motor_prometeo as MP
import codigo_prometeo as CP
import motor_cuerpo as MQ
import codigo_cuerpo as CQ
import fable_mundos as FB

SPEC = FB.catalogo(2000)['onda8k']
SEED = 31001


def firma(r):
    s = json.dumps(dict(lin=[(l['deaths'], l['nacimientos'], l['tam'], l['mord']) for l in r['linajes']], eco=r['eco']['n_nac'], t_ext=r['eco']['t_ext'],
                        cod=r.get('codigo', {}).get('cod_nac'), kit=(r.get('codigo', {}).get('prometeo') or {}).get('kit'),
                        viv=r['eco']['vivos_final']), sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def firma_din(r):   # sin cod_nac (guarda el LARGO de la cinta: con una instruccion mas difiere aunque la dinamica sea identica)
    s = json.dumps(dict(lin=[(l['deaths'], l['nacimientos'], l['tam'], l['mord']) for l in r['linajes']], eco=r['eco']['n_nac'], t_ext=r['eco']['t_ext'],
                        viv=r['eco']['vivos_final']), sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def corre(mod, brazo, **extra):
    eco = CC.eco_de(brazo, 4500, 2000); eco['cambio'] = dict(SPEC); eco.update(extra)
    return mod.run_solapadas(SEED, [CC.CARRO] * CC.MUNDO['n0'], T=6000, diag=0, mundo_n=CC.MUNDO['esc'], tope_cuerpos=CC.MUNDO['tope'],
                             muestra=CC.BASE['muestra'], eco=eco)


ok = 0; tot = 0
def chk(nombre, cond):
    global ok, tot
    tot += 1; ok += int(bool(cond)); print(('OK  ' if cond else 'MAL ') + nombre, flush=True)

def cont(r): return ((r.get('codigo', {}).get('cuerpo') or {}).get('cont')) or {}

C0 = tuple(CC.CINTA0); n0 = CC.MUNDO['n0']
def con(*ins): return [C0 + tuple(ins)] * n0

# ---------------------------------------------------------------- identidad
CP.pon_alfabeto(CP.OPS + CP.KIT); CQ.pon_alfabeto(CQ.OPS + CQ.KIT)
a = corre(MP, 'CODIGO_SIN_SOS'); b = corre(MQ, 'CODIGO_SIN_SOS')
chk(f"IC1 PROMETEO (v0 + KIT, copia prendida): cuerpo == prometeo ({firma(a)} / {firma(b)}); nac {a['eco']['n_nac']} / {b['eco']['n_nac']}", firma(a) == firma(b))
CP.pon_alfabeto(CP.OPS); CQ.pon_alfabeto(CQ.OPS)
a = corre(MP, 'CODIGO_SIN_SOS'); b = corre(MQ, 'CODIGO_SIN_SOS')
chk(f"IC2 CODIGO_SIN_SOS (v0): cuerpo == prometeo ({firma(a)} / {firma(b)})", firma(a) == firma(b))
CP.pon_alfabeto(CP.OPS + CP.KIT); CQ.pon_alfabeto(CQ.OPS + CQ.KIT + CQ.CUERPO)
a = corre(MP, 'MUT0'); r0 = corre(MQ, 'MUT0')
chk(f"IC3 alfabeto con PARTE, cinta sin partes, copia apagada: cuerpo == prometeo MUT0 ({firma(a)} / {firma(r0)})", firma(a) == firma(r0))
CQ.pon_alfabeto(CQ.OPS + CQ.KIT)
b0 = corre(MQ, 'CODIGO_SIN_SOS'); b6 = corre(MQ, 'CODIGO_SIN_SOS', niebla=600)
chk(f"IC4 niebla 600 (ve todo) == sin niebla ({firma(b0)} / {firma(b6)}); ciego {cont(b6).get('ciego')}", firma(b0) == firma(b6) and cont(b6).get('ciego') == 0)
b5 = corre(MQ, 'CODIGO_SIN_SOS', niebla=5)
cs = cont(b5)
chk(f"IC5 niebla 5: pasos ciegos {cs.get('ciego')} de {cs.get('ciego', 0) + cs.get('ve', 0)}; firma cambia; nac {b5['eco']['n_nac']} (sin niebla {b0['eco']['n_nac']})",
    cs.get('ciego', 0) > 0 and firma(b5) != firma(b0))

# ---------------------------------------------------------------- arnes por pieza
CQ.pon_alfabeto(CQ.OPS + CQ.KIT + CQ.CUERPO)
for j, (nom, clave) in enumerate((('PATA', 'pata'), ('ESCUDO', 'escudo'), ('ESTOMAGO', 'estomago'), (None, None), ('MANDIBULA', 'mandibula'), ('LENGUA', 'lengua'))):
    if nom is None: continue
    j = CQ.PARTES.index(nom)
    on = corre(MQ, 'MUT0', codigo=con(('PARTE', j))); mu = corre(MQ, 'MUT0', codigo=con(('PARTE', j)), partes_on=False)
    chk(f"IB {nom}: con efecto {clave} = {round(cont(on).get(clave, 0), 3)} (nac {on['eco']['n_nac']}); MUDO {clave} = {cont(mu).get(clave, 0)} (nac {mu['eco']['n_nac']}); "
        f"costo cobrado {round(cont(on).get('costo', 0), 3)}", cont(on).get(clave, 0) > 0 and cont(mu).get(clave, 0) == 0 and cont(on).get('costo', 0) > 0)
jo = CQ.PARTES.index('OJO')
on = corre(MQ, 'MUT0', codigo=con(('PARTE', jo))); mu = corre(MQ, 'MUT0', codigo=con(('PARTE', jo)), partes_on=False)
chk(f"IB6 OJO sin niebla: ON == MUDO bit a bit ({firma(on)} / {firma(mu)}); != MUT0 por el costo ({firma_din(r0)})", firma(on) == firma(mu) and firma_din(on) != firma_din(r0))
on = corre(MQ, 'MUT0', codigo=con(('PARTE', jo)), niebla=5); mu = corre(MQ, 'MUT0', codigo=con(('PARTE', jo)), niebla=5, partes_on=False)
fc = lambda r: cont(r).get('ciego', 0) / max(1, cont(r).get('ciego', 0) + cont(r).get('ve', 0))
chk(f"IB7 OJO con niebla 5: fraccion de pasos ciegos ON {fc(on):.4f} < MUDO {fc(mu):.4f}; nac ON {on['eco']['n_nac']} MUDO {mu['eco']['n_nac']}", fc(on) < fc(mu))
todas = [('PARTE', q) for q in range(len(CQ.PARTES))]
z = corre(MQ, 'MUT0', codigo=con(*todas), partes_on=False, partes_costo=False)
chk(f"IB8a las 6 partes, sin efecto y sin costo == MUT0 bit a bit ({firma_din(z)} / {firma_din(r0)})", firma_din(z) == firma_din(r0))
z = corre(MQ, 'MUT0', codigo=con(*todas), partes_on=False)
chk(f"IB8b las 6 partes, sin efecto, CON costo: cobrado {round(cont(z).get('costo', 0), 3)} (6 x 0.0002 = 0.0012 por cuerpo y paso); nac {z['eco']['n_nac']} (MUT0 {r0['eco']['n_nac']}); dinamica cambia",
    cont(z).get('costo', 0) > 0 and firma_din(z) != firma_din(r0))
print(f'IDENTIDAD CUERPO: {ok}/{tot}')
