"""Arnes de identidad del gemelo compilado del mundo social: mundo_social_n3_rapido.run(...) debe ser BIT A BIT igual a
mundo_social_n3.run(...) — TODAS las claves de CADA organismo, tras ida y vuelta por JSON — en una rejilla que cubre lo
que usan los corredores de la Etapa 5 y semillas 1-3:
  (a) n=1 mundo 'AB' (el control de identidad con organismo_v13)   (b) n=1 mundo 'regla' regla 'px0'
  (c) las siete condiciones de corre_N3d.py (mascaras, senal 'conducta'/'barajada_conducta', kw_por_org, regen,
      tipos_fijos) y la de corre_N3d_mudo.py (mudo_desde)
  (d) N1: n=2 'AB' con senal 'honesta', 'barajada', sin senal y con inversion
  (e) N2b: senal 'simbolo' y 'simbolo_barajado' con gamma_sim=1.2, baseline_q, u_m=1.0 (corre_N2.py --variante b)
  (f/h) ramas que el mundo admite pero ningun corredor usa: v9/v10/v11, sin plasticidad, sin memoria de rechazo,
      n=3, compat=False, K_sim=3, estado heredado (estados= y devolver_estado)
  (n2f) las seis condiciones de corre_N2f.py (regen=50, regen_rota=True, vida=100, escucha_si_no_sabe), el barrido
      --vida 50/200, las tres perillas por separado y el montaje con experto heredado. Se comparan tambien las
      claves nuevas `caducados` (del mundo) y `no_desensena` (del receptor).
Antes de la rejilla ancla con el TRONCO: con n=1 en 'AB' el mundo y el gemelo deben ser organismo_v13 en las claves
compartidas. Al final repite la condicion CONV de N3d a T=200000 (identidad) y mide la aceleracion con n=2.
Un solo proceso, sin Pool (regla 3 de registro/EQUIPO.md).
Uso: python experimentos/etapa5_comunicacion/identidad_social_rapido.py [--T 60000] [--full]
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]
import mundo_social_n3 as lento, mundo_social_n3_rapido as rapido
import organismo_v13 as tronco
from organismo_v13g import split_regla
from corre_N3d import parejas   # las MISMAS parejas que el corredor de N3d (sin duplicar el codigo)
import corre_N2f as n2f         # N2f: las mismas perillas y condiciones que el corredor (REGEN/REGEN_ROTA/VIDA/CONDS)

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 60000
N = lambda x: json.loads(json.dumps(x, default=str))
MR = [0, 0, 0, 1, 1, 1.]; ME = [1, 1, 1, 0, 0, 0.]
BASE3 = dict(mundo='regla', regla='px0', d_senal=5, f_vicaria=1 / 3, regen=50)   # corre_N3d.BASE (sin T)
KWP = [dict(gamma_soc=1.5), dict(escucha=False)]
# N2f (bloque 5): el mundo de corre_N2f.py, letra por letra (regen=50, regen_rota=True, vida) + la variante b
BASE2F = dict(mundo='regla', regla=n2f.REGLA, regen=n2f.REGEN, regen_rota=n2f.REGEN_ROTA, **n2f.VAR_KW)


def _fijos(seed):
    return parejas(seed, split_regla(seed, 'px0')[3])


# cada configuracion es una funcion de la semilla (tipos_fijos depende de ella)
CONFIGS = {
    'a_AB_n1':        lambda s, T: dict(n=1),
    'b_regla_n1':     lambda s, T: dict(n=1, mundo='regla', regla='px0'),
    'c_TECHO':        lambda s, T: dict(n=1, **BASE3, tipos_fijos=_fijos(s)),
    'c_SOLO_E':       lambda s, T: dict(n=1, mascaras=[ME], **BASE3, tipos_fijos=_fijos(s)),
    'c_SOLO_R':       lambda s, T: dict(n=1, mascaras=[MR], **BASE3, tipos_fijos=_fijos(s)),
    'c_N0':           lambda s, T: dict(n=2, mascaras=[MR, ME], **BASE3, tipos_fijos=_fijos(s)),
    'c_CONV':         lambda s, T: dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=KWP, **BASE3, tipos_fijos=_fijos(s)),
    'c_SHUF':         lambda s, T: dict(n=2, mascaras=[MR, ME], senal='barajada_conducta', kw_por_org=KWP, **BASE3, tipos_fijos=_fijos(s)),
    'c_SACIEDAD':     lambda s, T: dict(n=2, mascaras=[MR, ME], senal='conducta', **BASE3, tipos_fijos=_fijos(s),
                                        kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False, alpha=0.0)]),
    'c_CONV_MUDO':    lambda s, T: dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=KWP, **BASE3,
                                        tipos_fijos=_fijos(s), mudo_desde=3 * T // 4),
    'd_N0_AB':        lambda s, T: dict(n=2),
    'd_N1_honesta':   lambda s, T: dict(n=2, senal='honesta'),
    'd_N1_barajada':  lambda s, T: dict(n=2, senal='barajada'),
    'd_N1_invertir':  lambda s, T: dict(n=2, senal='honesta', invertir_en=T // 2),
    'e_N2b_CONV':     lambda s, T: dict(n=2, senal='simbolo', gamma_sim=1.2, baseline_q=True, u_m=1.0,
                                        mundo='regla', regla='azar'),
    'e_N2b_SHUF':     lambda s, T: dict(n=2, senal='simbolo_barajado', gamma_sim=1.2, baseline_q=True, u_m=1.0,
                                        mundo='regla', regla='azar'),
    'e_N2a':          lambda s, T: dict(n=2, senal='simbolo', mundo='regla', regla='azar'),   # u_m=0.5: si decodifica
    'e_N2c':          lambda s, T: dict(n=2, senal='simbolo', gamma_sim=1.2, baseline_q=True, u_m=1.0,
                                        estado_emisor='valor', u_v=0.5, mundo='regla', regla='azar'),
    'e_N2e':          lambda s, T: dict(n=2, senal='simbolo', gamma_sim=1.2, baseline_q=True, u_m=1.0,
                                        estado_emisor='valor_rapido', u_v=0.5, alinea=True, mundo='regla', regla='azar'),
    # ramas que los corredores de la Etapa 5 no usan pero el mundo admite (las cubre identidad_rapido.py del tronco);
    # en el mundo de regla para que la division ocurra de verdad (v9/v10 dividen por err>theta, v11/v13 por signo)
    'f_v11':          lambda s, T: dict(n=2, senal='honesta', mundo='regla', regla='px0', eta_s=0.0, puerta=None),
    'f_v10':          lambda s, T: dict(n=2, senal='honesta', mundo='regla', regla='px0', eta_s=0.0, puerta=None,
                                        div_signo=False),
    'f_v9':           lambda s, T: dict(n=2, senal='honesta', mundo='regla', regla='px0', eta_s=0.0, puerta=None,
                                        div_signo=False, mu_norm=False),
    'f_sin_rechazo':  lambda s, T: dict(n=2, senal='conducta', memoria_rechazo=0, nobj_por_org=6, lam=0.0),
    'f_sin_plast':    lambda s, T: dict(n=2, senal='conducta', mundo='regla', regla='px0', plast=False, learn=True),
    'h_n3':           lambda s, T: dict(n=3, senal='conducta', mascaras=[MR, ME, None], **BASE3, tipos_fijos=_fijos(s),
                                        kw_por_org=[dict(gamma_soc=1.5), dict(), dict(escucha=False)]),
    'h_compat0':      lambda s, T: dict(n=1, compat=False),   # con n=1 el mundo NO comparte el rng del organismo
    'h_K_sim3':       lambda s, T: dict(n=2, senal='simbolo', K_sim=3, gamma_sim=1.2, baseline_q=True, u_m=1.0,
                                        mundo='regla', regla='azar'),
    # --- N2f (bloque 5): las condiciones de corre_N2f.py con vida=100, mas el barrido --vida 50/200 y las perillas
    #     por separado (rotacion sola / vida sola / puerta sola) para localizar cualquier diferencia
    'n2f_SOLO':       lambda s, T: dict(vida=n2f.VIDA, **BASE2F, **n2f.CONDS['SOLO']),
    'n2f_N0':         lambda s, T: dict(vida=n2f.VIDA, **BASE2F, **n2f.CONDS['N0']),
    'n2f_INNATO':     lambda s, T: dict(vida=n2f.VIDA, **BASE2F, **n2f.CONDS['INNATO']),
    'n2f_CONV':       lambda s, T: dict(vida=n2f.VIDA, **BASE2F, **n2f.CONDS['CONV']),
    'n2f_CONV_MUNDO': lambda s, T: dict(vida=n2f.VIDA, **BASE2F, **n2f.CONDS['CONV_MUNDO']),
    'n2f_SHUF':       lambda s, T: dict(vida=n2f.VIDA, **BASE2F, **n2f.CONDS['SHUF']),
    'n2f_CONV_v50':   lambda s, T: dict(vida=n2f.VIDAS_HUMO[0], **BASE2F, **n2f.CONDS['CONV']),
    'n2f_CONV_v200':  lambda s, T: dict(vida=n2f.VIDAS_HUMO[2], **BASE2F, **n2f.CONDS['CONV']),
    'n2f_rota_sola':  lambda s, T: dict(n=2, mundo='regla', regla='azar', regen=50, regen_rota=True, senal='simbolo',
                                        **n2f.VAR_KW),
    'n2f_vida_sola':  lambda s, T: dict(n=2, mundo='regla', regla='azar', regen=50, vida=100, senal='simbolo',
                                        **n2f.VAR_KW),
    'n2f_puerta_sola': lambda s, T: dict(n=2, mundo='regla', regla='azar', senal='simbolo',
                                         escucha_si_no_sabe=True, **n2f.VAR_KW),
    # con u_m=1.0 (la variante b) el contraste nunca llega al umbral y la puerta no llega a morder: estas tres bajan
    # u_m para que `no_desensena` y `decodificados` sean != 0 y la puerta cambie de verdad el resultado
    'n2f_puerta_u05': lambda s, T: dict(n=2, mundo='regla', regla='azar', senal='simbolo', escucha_si_no_sabe=True),
    'n2f_puerta_u02': lambda s, T: dict(n=2, mundo='regla', regla='azar', senal='simbolo', escucha_si_no_sabe=True,
                                        u_m=0.2),
    'n2f_puerta_mundo': lambda s, T: dict(n=2, mundo='regla', regla='azar', regen=50, regen_rota=True, vida=100,
                                          senal='simbolo', escucha_si_no_sabe=True),
    'n2f_vida_sin_regen': lambda s, T: dict(n=2, mundo='regla', regla='px0', vida=30, senal='conducta'),
    'n2f_rota_AB':    lambda s, T: dict(n=2, regen=20, regen_rota=True, vida=60, senal='honesta'),
    'g_heredado':     'estado',   # experto heredado (estados=) + devolver_estado; se arma aparte
    'g_heredado_n2f': 'estado_n2f',   # el montaje real de corre_N2f: progenitor sin regen + CONV con estados
}
SEEDS = [1, 2, 3]


def compara(seed, kw):
    """Todas las claves de todos los organismos, tras ida y vuelta por JSON."""
    if kw is None: return []
    a = lento.run(seed, **kw); b = rapido.run(seed, **kw)
    if len(a) != len(b): return [('n_orgs', len(a), len(b))]
    return [(j, k) for j in range(len(a)) for k in a[j] if N(a[j][k]) != N(b[j][k])]


def compara_heredado(seed, T):
    """El progenitor se saca del ORIGINAL con devolver_estado y se le pasa a los dos: cubre estados= y el estado
    devuelto (arrays de numpy, comparados uno a uno)."""
    pa = lento.run(seed, n=1, T=T, mundo='regla', regla='azar', devolver_estado=True)[0]
    pb = rapido.run(seed, n=1, T=T, mundo='regla', regla='azar', devolver_estado=True)[0]
    dif = [(0, 'estado.' + k) for k in pa['estado'] if not np.array_equal(pa['estado'][k], pb['estado'][k])]
    dif += [(0, k) for k in pa if k != 'estado' and N(pa[k]) != N(pb[k])]
    kw = dict(n=2, T=T, mundo='regla', regla='azar', senal='simbolo', gamma_sim=1.2, baseline_q=True, u_m=1.0,
              estados=[None, pa['estado']])
    return dif + compara(seed, kw)


def compara_heredado_n2f(seed, T):
    """El montaje de corre_N2f.tarea: progenitor con regen=None (n=1, mundo de su propio RNG) y luego CONV con
    estados=[None, experto] en el mundo que rota y caduca."""
    pa = lento.run(seed, n=1, T=T, mundo='regla', regla=n2f.REGLA, regen=None, devolver_estado=True)[0]
    pb = rapido.run(seed, n=1, T=T, mundo='regla', regla=n2f.REGLA, regen=None, devolver_estado=True)[0]
    dif = [(0, 'estado.' + k) for k in pa['estado'] if not np.array_equal(pa['estado'][k], pb['estado'][k])]
    dif += [(0, k) for k in pa if k != 'estado' and N(pa[k]) != N(pb[k])]
    kw = dict(T=T, vida=n2f.VIDA, estados=[None, pa['estado']], **BASE2F, **n2f.CONDS['CONV'])
    return dif + compara(seed, kw)


if __name__ == '__main__':
    t0 = time.time(); rapido.run(1, T=2000); rapido.run(1, n=2, T=2000, senal='simbolo', mundo='regla')
    print(f"compilacion/carga de cache: {time.time()-t0:.1f}s", flush=True)
    # ancla con el tronco: con n=1 en 'AB' el mundo social ES organismo_v13 (claves compartidas), y el gemelo tambien
    CL = ['W', 'comp', 'W_lenta', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'celdas']
    anc = []
    for s in SEEDS:
        a = tronco.run(s, T=T); b = lento.run(s, n=1, T=T)[0]; c = rapido.run(s, n=1, T=T)[0]
        anc.append(([k for k in CL if N(a[k]) != N(b[k])], [k for k in CL if N(a[k]) != N(c[k])]))
    print(f"  ancla v13: mundo {sum(not d[0] for d in anc)}/{len(SEEDS)} == tronco, "
          f"gemelo {sum(not d[1] for d in anc)}/{len(SEEDS)} == tronco  (+{time.time()-t0:6.1f}s)", flush=True)
    ancla_mal = [d for d in anc if d[0] or d[1]]
    if ancla_mal: print(f"  DIFIERE el ancla con el tronco: {ancla_mal}", flush=True)
    fallos = []; n = 0
    for nombre, f in CONFIGS.items():
        for s in SEEDS:
            if f == 'estado':
                dif = compara_heredado(s, T)
            elif f == 'estado_n2f':
                dif = compara_heredado_n2f(s, T)
            else:
                kw = dict(f(s, T)); kw['T'] = T
                dif = compara(s, kw)
            n += 1
            if dif:
                fallos.append((nombre, s, dif))
                print(f"  DIFIERE {nombre} s{s}: {dif[:8]}", flush=True)
        print(f"  {nombre:16s} ok  (+{time.time()-t0:6.1f}s)", flush=True)
    print(f"identidad: {n - len(fallos)}/{n} corridas identicas (T={T}, {len(CONFIGS)} configuraciones x {len(SEEDS)} semillas)")
    if '--full' in sys.argv or not fallos:
        for etiqueta, nom in (('N3d CONV', 'c_CONV'), ('N2f CONV', 'n2f_CONV')):
            kw = dict(CONFIGS[nom](1, 200000)); kw['T'] = 200000
            t0 = time.time(); a = lento.run(1, **kw); tl = time.time() - t0
            t0 = time.time(); b = rapido.run(1, **kw); tr = time.time() - t0
            dif = [(j, k) for j in range(len(a)) for k in a[j] if N(a[j][k]) != N(b[j][k])]
            print(f"200k pasos ({etiqueta}, n=2): mundo {tl:.2f}s, gemelo {tr:.2f}s -> x{tl/tr:.1f}; "
                  f"identidad a 200k: {'OK' if not dif else 'FALLA ' + str(dif[:8])}", flush=True)
    sys.exit(1 if (fallos or ancla_mal) else 0)
