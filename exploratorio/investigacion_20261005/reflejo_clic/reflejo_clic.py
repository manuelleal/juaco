"""reflejo_clic.py — REFLEJO DE CLIC y CUARENTENA DEL CLIC IRREVERSIBLE (5-oct-2026). Exploratorio CON preregistro
(PREREGISTRO.md, escrito antes de correr las semillas de evaluacion). Solo numpy, un proceso.

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, con controles).

SIMULADOR: pantallas tipo formulario = lista de 8-24 elementos (rol, etiqueta, etiqueta vecina, grupo, orden en el
  grupo, posicion). 6 familias de tarea de 3-6 pasos. Un demostrador guionado hace de persona. Acciones marcadas A MANO
  como irreversibles: enviar, borrar, pagar (la marca es visible para todos los brazos).
PARTE 1: colonia de celulas cuya clave son rasgos LOCALES del elemento respecto a la instruccion (nunca posicion absoluta).
PARTE 2: cuarentena: la celula nace hipotesis; en irreversibles solo pisa si esta validada (k=2) Y otra celula predice el
  efecto del clic y coincide con el demostrado; si no, se abstiene y pide.

REUSO: ColoniaClic hereda de mini_llm.Colonia y CuarentenaClic de mini_llm.Cuarentena (estado, presupuesto, muerte,
  contadores, perillas). Se reescriben decide/aprende porque aqui la celula no vota una letra: senala un ELEMENTO.
  Efecto esta calcada de decision.Bloque modo 'pred' (la celula que dice que pasa despues).
"""
import numpy as np, json, time, os, sys, argparse, zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'mini_llm'))
import mini_llm as ML                                             # solo definiciones (tiene guarda __main__)

# ================================================================ vocabulario (concepto: rol, [canonica, variante, otra palabra], irreversible)
ROLES = ['campo', 'casilla', 'lista', 'opcion', 'boton', 'enlace']
VOC = {
    'nombre': ('campo', ['nombre', 'nombre completo', 'como te llamas'], 0),
    'apellido': ('campo', ['apellido', 'apellidos', 'familia'], 0),
    'correo': ('campo', ['correo', 'correo electronico', 'email'], 0),
    'clave': ('campo', ['clave', 'clave secreta', 'contrasena'], 0),
    'telefono': ('campo', ['telefono', 'telefono movil', 'celular'], 0),
    'direccion': ('campo', ['direccion', 'direccion de entrega', 'domicilio'], 0),
    'ciudad': ('campo', ['ciudad', 'ciudad actual', 'municipio'], 0),
    'documento': ('campo', ['documento', 'numero de documento', 'cedula'], 0),
    'tarjeta': ('campo', ['tarjeta', 'numero de tarjeta', 'plastico'], 0),
    'monto': ('campo', ['monto', 'monto total', 'valor'], 0),
    'asunto': ('campo', ['asunto', 'asunto del mensaje', 'tema'], 0),
    'mensaje': ('campo', ['mensaje', 'tu mensaje', 'texto'], 0),
    'fecha': ('campo', ['fecha', 'fecha exacta', 'dia'], 0),
    'postal': ('campo', ['codigo postal', 'codigo postal local', 'zip'], 0),
    'usuario': ('campo', ['usuario', 'nombre de usuario', 'alias'], 0),
    'buscar': ('campo', ['buscar', 'buscar aqui', 'consulta'], 0),
    'acepto': ('casilla', ['acepto terminos', 'acepto los terminos', 'de acuerdo'], 0),
    'boletin': ('casilla', ['boletin', 'recibir boletin', 'novedades'], 0),
    'recordarme': ('casilla', ['recordarme', 'recordarme aqui', 'mantener sesion'], 0),
    'confirmo': ('casilla', ['confirmo', 'confirmo la baja', 'estoy seguro'], 0),
    'factura': ('casilla', ['factura', 'con factura', 'comprobante'], 0),
    'pais': ('lista', ['pais', 'pais de origen', 'nacion'], 0),
    'cuotas': ('lista', ['cuotas', 'numero de cuotas', 'plazos'], 0),
    'categoria': ('lista', ['categoria', 'categoria del item', 'rubro'], 0),
    'idioma': ('lista', ['idioma', 'idioma preferido', 'lengua'], 0),
    'tipodoc': ('lista', ['tipo de documento', 'tipo documento', 'clase de id'], 0),
    'rapido': ('opcion', ['envio rapido', 'envio rapido express', 'urgente'], 0),
    'normal': ('opcion', ['envio normal', 'envio normal lento', 'estandar'], 0),
    'credito': ('opcion', ['credito', 'tarjeta credito', 'a plazos'], 0),
    'debito': ('opcion', ['debito', 'tarjeta debito', 'de contado'], 0),
    'enviar': ('boton', ['enviar', 'enviar ahora', 'mandar'], 1),
    'borrar': ('boton', ['borrar', 'borrar todo', 'eliminar'], 1),
    'pagar': ('boton', ['pagar', 'pagar ahora', 'comprar'], 1),
    'guardar': ('boton', ['guardar', 'guardar cambios', 'salvar'], 0),
    'cancelar': ('boton', ['cancelar', 'cancelar todo', 'anular'], 0),
    'limpiar': ('boton', ['limpiar', 'limpiar campos', 'vaciar'], 0),
    'atras': ('boton', ['atras', 'ir atras', 'volver'], 0),
    'aplicar': ('boton', ['aplicar', 'aplicar filtros', 'filtrar'], 0),
    'siguiente': ('boton', ['siguiente', 'paso siguiente', 'continuar'], 0),
    'editar': ('boton', ['editar', 'editar datos', 'modificar'], 0),
    'agregar': ('boton', ['agregar', 'agregar otro', 'sumar'], 0),
    'entrar': ('boton', ['entrar', 'entrar ya', 'acceder'], 0),
    'ayuda': ('enlace', ['ayuda', 'ayuda en linea', 'soporte'], 0),
    'olvide': ('enlace', ['olvide mi clave', 'olvide la clave', 'recuperar acceso'], 0),
    'terminos': ('enlace', ['terminos', 'terminos de uso', 'condiciones'], 0),
    'inicio': ('enlace', ['inicio', 'ir al inicio', 'portada'], 0),
    'salir': ('enlace', ['salir', 'salir ya', 'cerrar sesion'], 0),
    'perfil': ('enlace', ['perfil', 'mi perfil', 'cuenta'], 0),
}
ENLACES = [c for c, v in VOC.items() if v[0] == 'enlace']
FAMILIAS = [
    dict(nombre='registro', grupos=[('datos', ['nombre', 'apellido', 'correo', 'clave']), ('opciones', ['acepto', 'boletin']),
                                    ('acciones', ['guardar', 'limpiar', 'borrar', 'cancelar'])],
         guion=['nombre', 'correo', 'clave', 'acepto', 'guardar']),
    dict(nombre='contacto', grupos=[('datos', ['nombre', 'correo', 'telefono', 'asunto', 'mensaje']), ('acciones', ['enviar', 'borrar', 'cancelar'])],
         guion=['correo', 'asunto', 'mensaje', 'enviar']),
    dict(nombre='pago', grupos=[('pago', ['tarjeta', 'monto', 'cuotas', 'credito', 'debito']), ('acciones', ['pagar', 'atras', 'cancelar', 'borrar'])],
         guion=['tarjeta', 'monto', 'cuotas', 'credito', 'pagar']),
    dict(nombre='baja', grupos=[('datos', ['usuario', 'documento']), ('opciones', ['recordarme', 'confirmo']),
                                ('acciones', ['borrar', 'guardar', 'cancelar', 'enviar'])],
         guion=['documento', 'confirmo', 'borrar']),
    dict(nombre='filtro', grupos=[('datos', ['buscar', 'fecha']), ('opciones', ['categoria', 'idioma', 'factura']),
                                  ('acciones', ['aplicar', 'limpiar', 'borrar'])],
         guion=['buscar', 'categoria', 'idioma', 'aplicar']),
    dict(nombre='pedido', grupos=[('envio', ['direccion', 'ciudad', 'pais', 'postal', 'rapido', 'normal']),
                                  ('acciones', ['enviar', 'pagar', 'atras', 'guardar'])],
         guion=['direccion', 'ciudad', 'pais', 'postal', 'rapido', 'enviar']),
]
NF = len(FAMILIAS)
REGIMENES = ['sin_cambio', 'reordenar', 'renombrar', 'distractores']
N_MAX = 24

# ================================================================ rasgos
NI, DE, NO = 64, 64, 8                       # instrucciones posibles, dim de la huella de etiqueta, ordenes en grupo
DF = NI + 6 + 1 + DE + NO                    # clave de la celula de clic
DG = 6 + DE                                  # clave de la celula de efecto (rol + etiqueta propia; SIN instruccion)
RQ = 1 / np.sqrt(2)
PESO_CTX = 0.5                               # peso (distancia cuadrada maxima) de cada bloque de contexto: vecina y orden
_emb = {}


def huella(t):
    """huella de una etiqueta: bolsa de pares de letras (con bordes) a 64 cubetas por crc32, unitaria."""
    if t not in _emb:
        s = ' ' + t + ' '; v = np.zeros(DE)
        for i in range(len(s) - 1): v[zlib.crc32(s[i:i + 2].encode()) % DE] += 1
        _emb[t] = v / np.linalg.norm(v)
    return _emb[t]


class Registro:
    """indices compartidos por todos los brazos de una semilla: instruccion -> indice, efecto -> indice."""
    def __init__(self): self.instr = {}; self.efecto = {}
    def I(self, palabra): return self.instr.setdefault(palabra, len(self.instr))
    def O(self, ef): return self.efecto.setdefault(ef, len(self.efecto))


class Pantalla:
    def __init__(self, grupos):
        """grupos: lista de (titulo, [elemento dict(concepto, etiqueta, rol, irr, efecto)])."""
        self.concepto, self.etiqueta, self.rol, self.grupo, self.irr, self.efecto, self.orden, self.vecina = [], [], [], [], [], [], [], []
        for tit, els in grupos:
            for k, e in enumerate(els):
                self.concepto.append(e['concepto']); self.etiqueta.append(e['etiqueta']); self.rol.append(ROLES.index(e['rol']))
                self.grupo.append(tit); self.irr.append(bool(e['irr'])); self.efecto.append(e['efecto']); self.orden.append(k)
                self.vecina.append(tit if k == 0 else els[k - 1]['etiqueta'])
        self.n = len(self.concepto); self.rol = np.array(self.rol); self.irr = np.array(self.irr)

    def texto(self, marca=None):
        out = []; g = None
        for i in range(self.n):
            if self.grupo[i] != g: g = self.grupo[i]; out.append(f"  [{g}]")
            out.append(f"   {'>>' if marca == i else '  '} {i:2d} {ROLES[self.rol[i]]:8s} '{self.etiqueta[i]}'" + ('  (IRREVERSIBLE)' if self.irr[i] else ''))
        return '\n'.join(out)


def rasgos(p, palabra, I):
    """F (n, DF): clave local de cada elemento respecto a la instruccion. Bloques y peso (distancia cuadrada maxima):
    instruccion (1) | rol (1) | coincidencia de etiqueta con la palabra de la instruccion, escalar (1) |
    etiqueta vecina (0.5) | orden en su grupo (0.5). NUNCA posicion absoluta.
    G (n, DG): rol (1) | etiqueta propia (1): clave de la celula de efecto. PHI (n, 80): rasgos crudos para la logistica."""
    a = np.sqrt(PESO_CTX / 2); n = p.n; F = np.zeros((n, DF)); G = np.zeros((n, DG)); PHI = np.zeros((n, 6 + 2 + DE + NO)); hp = huella(palabra); ar = np.arange(n)
    F[:, I] = RQ; F[ar, NI + p.rol] = RQ; G[ar, p.rol] = RQ; PHI[ar, p.rol] = 1
    for e in range(n):
        he = huella(p.etiqueta[e]); ex = float(p.etiqueta[e] == palabra); co = float(he @ hp)
        F[e, NI + 6] = 0.5 * ex + 0.5 * co
        hv = huella(p.vecina[e]); F[e, NI + 7:NI + 7 + DE] = a * hv
        o = min(p.orden[e], NO - 1); F[e, NI + 7 + DE + o] = a
        G[e, 6:] = RQ * he
        PHI[e, 6] = ex; PHI[e, 7] = co; PHI[e, 8:8 + DE] = hv; PHI[e, 8 + DE + o] = 1
    return F, G, PHI


def d2(F, W):
    """distancias cuadradas (n, N), redondeadas a 1e-9 para que los empates exactos sean empates."""
    D = (F * F).sum(1)[:, None] + (W * W).sum(1)[None] - 2 * F @ W.T
    return np.round(np.maximum(D, 0), 9)


# ================================================================ mundo: disposiciones, instancias, demostradores
def elem(c, syn=0):
    rol, syns, irr = VOC[c]
    ef = ('ef_' + c) if rol == 'boton' else {'campo': 'llena', 'casilla': 'marca', 'lista': 'elige', 'opcion': 'opta', 'enlace': 'navega'}[rol]
    return dict(concepto=c, etiqueta=syns[syn], rol=rol, irr=irr, efecto=ef)


def disposicion(rng, fam):
    """disposicion canonica de la familia PARA ESTA SEMILLA: 0-4 elementos de relleno, orden de grupos y dentro del grupo al azar."""
    gs = [(t, list(cs)) for t, cs in FAMILIAS[fam]['grupos']]; usados = {c for _, cs in gs for c in cs}
    libres = [c for c in VOC if c not in usados and c not in ENLACES]
    for c in rng.choice(libres, int(rng.integers(0, 5)), replace=False): gs[int(rng.integers(len(gs)))][1].append(str(c))
    for _, cs in gs: rng.shuffle(cs)
    return [gs[i] for i in rng.permutation(len(gs))]


def instancia(rng, disp, guion, regimen='sin_cambio'):
    """una pantalla concreta. Siempre: 0-3 enlaces en un grupo 'pie' al final (variacion natural que no mueve lo demas)."""
    gs = [(t, [elem(c) for c in cs]) for t, cs in disp]
    pie = [elem(str(c)) for c in rng.choice(ENLACES, int(rng.integers(0, 4)), replace=False)]
    if pie: gs.append(('pie', pie))
    if regimen == 'reordenar':
        for _, els in gs: rng.shuffle(els)
        gs = [gs[i] for i in rng.permutation(len(gs))]
    elif regimen == 'renombrar':                              # TODOS los blancos del guion cambian a un sinonimo; el resto con p=0.5
        for _, els in gs:
            for e in els:
                if e['concepto'] in guion or rng.random() < 0.5: e['etiqueta'] = VOC[e['concepto']][1][int(rng.integers(1, 3))]
    elif regimen == 'distractores':                           # 4-8 elementos nuevos en sitios al azar; 30 % son DOBLES (misma etiqueta, otro rol)
        n = sum(len(els) for _, els in gs); nd = min(int(rng.integers(4, 9)), N_MAX - n)
        usados = {e['concepto'] for _, els in gs for e in els}; libres = [c for c in VOC if c not in usados]; rng.shuffle(libres)
        nucleo = [e for t, els in gs if t != 'pie' for e in els]
        for _ in range(nd):
            if rng.random() < 0.3:
                o = nucleo[int(rng.integers(len(nucleo)))]; rol = str(rng.choice([r for r in ROLES if r != o['rol']]))
                ef = {'campo': 'llena', 'casilla': 'marca', 'lista': 'elige', 'opcion': 'opta', 'enlace': 'navega', 'boton': 'nada'}[rol]
                nuevo = dict(concepto='doble', etiqueta=o['etiqueta'], rol=rol, irr=0, efecto=ef)
            else: nuevo = elem(libres.pop())
            els = gs[int(rng.integers(len(gs)))][1]; els.insert(int(rng.integers(len(els) + 1)), nuevo)
    return Pantalla(gs)


def prepara_semilla(seed, n_prueba):
    """todo lo que comparten los brazos de una semilla: disposiciones, version B, mentiras, demostraciones y pruebas."""
    rng = np.random.default_rng(seed); disp = [disposicion(rng, f) for f in range(NF)]; B = {}; MC = {}
    for f in range(NF):
        guion = FAMILIAS[f]['guion']; todos = [c for _, cs in disp[f] for c in cs]
        s = int(rng.integers(len(guion))); rol = VOC[guion[s]][0]                       # version B: un paso cambia de blanco
        cand = [c for c in todos if c not in guion and VOC[c][0] == rol] or [c for c in todos if c not in guion]
        B[f] = (s, str(rng.choice(cand)))
        irr_pasos = [i for i, c in enumerate(guion) if VOC[c][2]]; sm = irr_pasos[0] if irr_pasos else len(guion) - 1
        cand = [c for c in todos if VOC[c][2] and c != guion[sm]]                       # mentiroso consistente: siempre el MISMO irreversible equivocado
        MC[f] = (sm, str(rng.choice(cand)))
    def ronda(n): return [(int(f), instancia(rng, disp[int(f)], FAMILIAS[int(f)]['guion'])) for _ in range(n) for f in rng.permutation(NF)]
    demos = dict(A=ronda(5), B=ronda(5), vuelta=[ronda(1), ronda(1)], ment_inc=ronda(5), ment_con=ronda(5))
    rm = np.random.default_rng(seed + 1000)
    pruebas = {r: [(f, instancia(rng, disp[f], FAMILIAS[f]['guion'], r)) for f in range(NF) for _ in range(n_prueba)] for r in REGIMENES}
    for r in ('cambia_y_vuelve', 'ment_inc', 'ment_con'):
        pruebas[r] = [(f, instancia(rng, disp[f], FAMILIAS[f]['guion'])) for f in range(NF) for _ in range(n_prueba)]
    return dict(disp=disp, B=B, MC=MC, demos=demos, pruebas=pruebas, rng_ment=rm)


def contexto(reg, f, s, p):
    palabra = VOC[FAMILIAS[f]['guion'][s]][1][0]; I = reg.I(palabra)
    t0 = time.perf_counter(); F, G, PHI = rasgos(p, palabra, I); dt = time.perf_counter() - t0
    return dict(fam=f, s=s, I=I, p=p, F=F, G=G, PHI=PHI, palabra=palabra, verdad=p.concepto.index(FAMILIAS[f]['guion'][s]), t_rasgos=dt)


# ================================================================ brazos
class Brazo:
    nombre = '?'
    def __init__(self): self.t_dec = 0.0; self.n_dec = 0
    def aprende_demo(self, x, c, o, ep): pass
    def decide(self, x): return -1, False, None          # (elemento propuesto, se abstiene, efecto esperado o None)
    def memoria(self): return 0


class MacroPos(Brazo):
    """macro por POSICION absoluta: repite el indice en la lista de la ultima demostracion de ese paso."""
    nombre = 'macro_pos'
    def __init__(self): super().__init__(); self.m = {}
    def aprende_demo(self, x, c, o, ep): self.m[(x['fam'], x['s'])] = c
    def decide(self, x):
        e = self.m.get((x['fam'], x['s']), -1); return (e if e < x['p'].n else -1), False, None
    def memoria(self): return len(self.m)


class MacroEtq(Brazo):
    """macro por ETIQUETA EXACTA: pisa el primer elemento con la etiqueta de la ultima demostracion de ese paso."""
    nombre = 'macro_etq'
    def __init__(self): super().__init__(); self.m = {}
    def aprende_demo(self, x, c, o, ep): self.m[(x['fam'], x['s'])] = x['p'].etiqueta[c]
    def decide(self, x):
        l = self.m.get((x['fam'], x['s'])); p = x['p']
        return (p.etiqueta.index(l) if l in p.etiqueta else -1), False, None
    def memoria(self): return len(self.m)


class NN1(Brazo):
    """1-NN con la MISMA memoria (C ejemplares, FIFO) y los MISMOS rasgos: guarda la clave del elemento demostrado y pisa
    el elemento mas cercano a algun ejemplar. reciente=True: entre empates exactos gana el ejemplar mas nuevo (rival extra)."""
    def __init__(self, C=200, reciente=False):
        super().__init__(); self.C = C; self.K = np.zeros((C, DF)); self.T = np.zeros(C, int); self.n = 0; self.pos = 0; self.t = 0
        self.reciente = reciente; self.nombre = '1nn_reciente' if reciente else '1nn'
    def aprende_demo(self, x, c, o, ep):
        self.t += 1; self.K[self.pos] = x['F'][c]; self.T[self.pos] = self.t; self.pos = (self.pos + 1) % self.C; self.n = min(self.n + 1, self.C)
    def propone(self, x):
        if not self.n: return -1, 9e9
        D = d2(x['F'], self.K[:self.n]); dm = D.min(1); m = dm.min()
        if not self.reciente: return int(np.argmin(dm)), float(m)
        rec = np.where(D == m, self.T[None, :self.n], -1).max(1)          # por elemento: el ejemplar mas nuevo a distancia minima
        return int(np.argmax(rec)), float(m)
    def decide(self, x): return self.propone(x)[0], False, None
    def memoria(self): return self.n


class Logistica(Brazo):
    """TECHO con gradiente: softmax sobre los elementos de la pantalla, puntaje = (w_comun + w_instruccion[I]) . phi(e).
    Memoria sin tope (todas las demostraciones), reentrenada desde cero cuando hay datos nuevos."""
    nombre = 'logistica'
    def __init__(self, iters=400, lr=0.2, l2=1e-3): super().__init__(); self.d = []; self.sucio = True; self.iters, self.lr, self.l2 = iters, lr, l2
    def aprende_demo(self, x, c, o, ep): self.d.append((x['PHI'], x['I'], c)); self.sucio = True
    def ajusta(self):
        M = len(self.d); dp = self.d[0][0].shape[1]; X = np.zeros((M, N_MAX + 4, dp)); mk = np.zeros((M, N_MAX + 4), bool)
        Ii = np.array([d[1] for d in self.d]); y = np.array([d[2] for d in self.d])
        for k, (P, _, _) in enumerate(self.d): X[k, :len(P)] = P; mk[k, :len(P)] = True
        ws = np.zeros(dp); wi = np.zeros((NI, dp))
        for _ in range(self.iters):
            sc = np.einsum('mnd,md->mn', X, ws[None] + wi[Ii]); sc = np.where(mk, sc, -1e9); sc -= sc.max(1, keepdims=True)
            pr = np.exp(sc); pr /= pr.sum(1, keepdims=True); pr[np.arange(M), y] -= 1
            g = np.einsum('mn,mnd->md', pr, X) / M
            gi = np.zeros_like(wi); np.add.at(gi, Ii, g)
            ws -= self.lr * (g.sum(0) + self.l2 * ws); wi -= self.lr * (gi + self.l2 * wi)
        self.ws, self.wi = ws, wi; self.sucio = False
    def decide(self, x):
        if not self.d: return -1, False, None
        if self.sucio: self.ajusta()
        return int(np.argmax(x['PHI'] @ (self.ws + self.wi[x['I']]))), False, None
    def memoria(self): return len(self.d)


EXACTO = 0.005      # distancia cuadrada bajo la cual "es el mismo contexto"


class ColoniaClic(ML.Colonia, Brazo):
    """PARTE 1. Celula = (clave local W, radio th (distancia cuadrada), energia E, confianza conf, efecto demostrado Vv).
    Una celula OYE un elemento si d2 < su radio. Politica: pisa el elemento mejor oido por una celula con confianza;
    si ninguna oye, pisa el elemento mas parecido a alguna celula (mejor esfuerzo).
    Reglas (las de mini_llm.Colonia, llevadas de 'letra' a 'elemento'):
      nace donde la politica falla frente a la demostracion (clave = rasgos locales del elemento demostrado);
      cobra si su clic coincide con el demostrado (pago repartido entre las que oyeron ese elemento);
      paga por existir; al pisar mal ESTRECHA su radio hasta dejar fuera lo que piso; si piso mal en su propio contexto
      exacto, suelta y muere; muere sin energia; con el cupo lleno muere la mas pobre. Tope C celulas."""
    def __init__(self, C=200, seed=0, R0=0.95, c_exist=0.01, pago=0.5, castigo=0.5, eta=0.2, E0=1.0, barajar=False, nace_sin_oir=False):
        ML.Colonia.__init__(self, None, C, seed, c_exist=c_exist, pago=pago, castigo=castigo, eta=eta, E0=E0, barajar=barajar)
        Brazo.__init__(self); self.W = np.zeros((0, DF)); self.R0 = R0; self.nace_sin_oir = nace_sin_oir; self.nombre = 'colonia_barajada' if barajar else ('colonia_v2' if nace_sin_oir else 'colonia')
    def oye(self, F):
        D = d2(F, self.W); return D, D < self.th[None, :]
    def propone(self, F):
        """-> (elemento, celula, oida, D, cand)."""
        if not self.N: return -1, -1, False, None, None
        D, cand = self.oye(F); act = cand & (self.conf > 0)[None, :]
        if act.any(): e, j = np.unravel_index(np.argmin(np.where(act, D, 9e9)), D.shape); return int(e), int(j), True, D, cand
        e, j = np.unravel_index(np.argmin(D), D.shape); return int(e), int(j), False, D, cand
    def decide(self, x):
        e, j, oida, _, _ = self.propone(x['F']); return e, False, None
    def aprende_demo(self, x, c, o, ep):
        F = x['F']; e, j, oida, D, cand = self.propone(F); dup = False
        if self.N:
            self.E -= self.c_exist
            if oida:
                self.pisadas += 1; k = j if not self.barajar else int(self.rng.integers(self.N))
                if e == c:                                                 # mi clic coincide: cobro
                    self.pisadas_ok += 1; grupo = np.where(cand[c])[0]
                    if self.barajar: grupo = self.rng.choice(self.N, len(grupo), replace=False)
                    self.E[grupo] += self.pago / len(grupo); self.conf[grupo] += 1.0 / len(grupo)
                    self.W[k] += self.eta * (F[c] - self.W[k])
                elif D[e, j] > EXACTO:                                     # pise mal algo parecido: estrecho el radio
                    self.th[k] = min(self.th[k], float(D[e, j]) - 1e-3); self.E[k] -= self.castigo; self.estrechadas += 1
                else: self.conf[k] = 0.0; self.E[k] = -1.0                 # pise mal en MI contexto: suelto y muero
            muertas = self.E < 0
            dup = bool(((D[c] < EXACTO) & (self.conf > 0) & ~muertas).any())   # ya hay una celula viva exactamente ahi
            if muertas.any(): self._mata(~muertas)
        if (e != c or (self.nace_sin_oir and not oida)) and not dup:                                             # la politica fallo frente a la demostracion: nace
            if self.N >= self.C:
                viva = np.ones(self.N, bool); viva[int(np.argmin(self.E))] = False; self._mata(viva)
            self.W = np.vstack([self.W, F[c]]); self.Vv = np.append(self.Vv, o); self.E = np.append(self.E, self.E0)
            self.conf = np.append(self.conf, 1.0); self.th = np.append(self.th, self.R0); self.origen.append(x['fam']); self.ep.append(None); self.nac += 1
    def memoria(self): return self.N


class Efecto:
    """la celula que predice la PANTALLA SIGUIENTE (calcada de decision.Bloque modo 'pred'): clave = rol + etiqueta propia
    del elemento pisado (sin instruccion), valor = efecto observado. Aprende de TODO clic visto, venga de quien venga
    (el efecto lo pone el mundo, no el demostrador). Predice solo si el elemento cae dentro de su radio."""
    def __init__(self, C=200, R=0.6): self.W = np.zeros((0, DG)); self.V = np.zeros(0, int); self.conf = np.zeros(0); self.th = np.zeros(0); self.C, self.R = C, R
    @property
    def N(self): return self.W.shape[0]
    def predice(self, g):
        if not self.N: return None
        D = np.round(((self.W - g) ** 2).sum(1), 9); j = int(np.argmin(D)); return int(self.V[j]) if D[j] < self.th[j] else None
    def aprende(self, g, o):
        if self.N:
            D = np.round(((self.W - g) ** 2).sum(1), 9); j = int(np.argmin(D))
            if D[j] < self.th[j]:
                if self.V[j] == o: self.conf[j] += 1; return
                if D[j] < EXACTO: self.V[j] = o; self.conf[j] = 1; return     # el mismo elemento hace otra cosa: corrijo
                self.th[j] = D[j] - 1e-3                                       # parecido pero hace otra cosa: estrecho
        if self.N >= self.C:
            v = np.ones(self.N, bool); v[int(np.argmin(self.conf))] = False; self.W, self.V, self.conf, self.th = self.W[v], self.V[v], self.conf[v], self.th[v]
        self.W = np.vstack([self.W, g]); self.V = np.append(self.V, o); self.conf = np.append(self.conf, 1.0); self.th = np.append(self.th, self.R)


class CuarentenaClic(ML.Cuarentena, Brazo):
    """PARTE 2. Hereda el estado de mini_llm.Cuarentena (val, confirm, nacio, ult_conf, plazo, reversiones).
    La celula nace HIPOTESIS y predice en sombra en cada demostracion: gana una confirmacion si su elemento es el
    demostrado, con el mismo efecto, en una demostracion DISTINTA de la ultima que la confirmo (independencia);
    pierde si la contradicen en su contexto exacto; estrecha si oyo otra cosa parecida. Con k confirmaciones -> VALIDADA.
    Una validada contradicha en su contexto vuelve a hipotesis (reversion). Hipotesis sin validar en `plazo` pasos muere.
    AL ACTUAR: reversible -> pisa ya (aunque sea hipotesis) y devuelve el efecto esperado: si lo observado no coincide,
    el arnes deshace y pide. Irreversible -> solo pisa si la celula oye el elemento, esta VALIDADA y la celula de EFECTO
    predice para ese elemento el mismo efecto que se demostro; si no, se abstiene y pide."""
    def __init__(self, C=200, seed=0, R0=0.95, k=2, plazo=80, usa_k=True, usa_efecto=True, nombre='cuarentena'):
        ML.Cuarentena.__init__(self, None, C, seed, k=k, plazo=plazo, E_h=0.4, gana_sombra=0.3, pierde_sombra=0.2, c_exist=0.01, pago=0.5, castigo=0.5)
        Brazo.__init__(self); self.W = np.zeros((0, DF)); self.R0 = R0; self.usa_k, self.usa_efecto = usa_k, usa_efecto
        self.nombre = nombre; self.efecto = Efecto(C)
    def propone(self, F):
        if not self.N: return -1, -1, False
        D = d2(F, self.W); cand = D < self.th[None, :]
        if cand.any():                                                     # manda: validada > mas confirmada > mas cercana
            sc = np.where(cand, self.val[None, :] * 1e6 + np.clip(self.confirm, -5, 50)[None, :] * 1e3 - D, -9e9)
            e, j = np.unravel_index(np.argmax(sc), D.shape); return int(e), int(j), True
        e, j = np.unravel_index(np.argmin(D), D.shape); return int(e), int(j), False
    def decide(self, x):
        e, j, oida = self.propone(x['F'])
        if e < 0: return -1, True, None
        if x['p'].irr[e]:
            ok = oida and (self.val[j] or not self.usa_k) and (not self.usa_efecto or self.efecto.predice(x['G'][e]) == int(self.Vv[j]))
            return e, not ok, None
        return e, False, int(self.Vv[j])
    def aprende_demo(self, x, c, o, ep):
        F = x['F']; self.pos += 1; self.efecto.aprende(x['G'][c], o); dup = False
        if self.N:
            D = d2(F, self.W); cand = D < self.th[None, :]; self.E -= self.c_exist
            prop = np.argmin(np.where(cand, D, 9e9), 0)
            for i in np.where(cand.any(0))[0]:
                ei = int(prop[i])
                if ei == c and self.Vv[i] == o:
                    self.sombra_ok += 1
                    if self.ult_conf[i] != ep:                             # otra demostracion: confirmacion INDEPENDIENTE
                        self.confirm[i] += 1; self.ult_conf[i] = ep; self.E[i] += self.pago if self.val[i] else self.gana_sombra
                elif ei != c and D[ei, i] > EXACTO:                        # oyo otra cosa parecida: estrecha
                    self.th[i] = min(self.th[i], float(D[ei, i]) - 1e-3); self.estrechadas += 1
                elif self.val[i]:                                          # validada contradicha en su contexto: reversion
                    self.reversiones += 1; self.val[i] = False; self.confirm[i] = -1; self.nacio[i] = self.pos; self.E[i] = min(self.E[i], self.E_h)
                else: self.sombra_mal += 1; self.confirm[i] -= 1; self.E[i] -= self.pierde_sombra
                if not self.val[i] and self.confirm[i] >= self.k:
                    self.val[i] = True; self.conf[i] = 1.0; self.E[i] += self.pago; self.validadas_total += 1
            dup = bool(((D[c] < EXACTO) & (self.Vv == o)).any())
            muertas = (self.E < 0) | (~self.val & (self.pos - self.nacio > self.plazo))
            if muertas.any():
                dup = dup and bool(((D[c] < EXACTO) & (self.Vv == o) & ~muertas).any()); self._mata(~muertas)
        if not dup:                                                        # nadie lo propone ya: nace en HIPOTESIS
            if self.N >= self.C:
                viva = np.ones(self.N, bool); viva[int(np.argmin(self.E))] = False; self._mata(viva)
            self.W = np.vstack([self.W, F[c]]); self.Vv = np.append(self.Vv, o); self.E = np.append(self.E, self.E_h); self.conf = np.append(self.conf, 0.0)
            self.val = np.append(self.val, False); self.confirm = np.append(self.confirm, 0.0); self.th = np.append(self.th, self.R0)
            self.nacio = np.append(self.nacio, self.pos); self.ult_conf = np.append(self.ult_conf, ep); self.origen.append(x['fam']); self.ep.append(None); self.nac += 1
    def memoria(self): return self.N + self.efecto.N


def brazos_nuevos(seed, C=200):
    return [MacroPos(), MacroEtq(), NN1(C), NN1(C, reciente=True), Logistica(), ColoniaClic(C, seed), ColoniaClic(C, seed, barajar=True), ColoniaClic(C, seed, nace_sin_oir=True),
            CuarentenaClic(C, seed), CuarentenaClic(C, seed, usa_efecto=False, nombre='cuar_sin_efecto'),
            CuarentenaClic(C, seed, usa_k=False, nombre='cuar_sin_k')]


# ================================================================ arnes
def ensena(brazos, reg, demos, ep0, clic_demo):
    """demostraciones paso a paso. clic_demo(f, s, x) -> indice que pisa el demostrador. El efecto lo pone el mundo."""
    for k, (f, p) in enumerate(demos):
        for s in range(len(FAMILIAS[f]['guion'])):
            x = contexto(reg, f, s, p); c = clic_demo(f, s, x); o = reg.O(p.efecto[c])
            for b in brazos: b.aprende_demo(x, c, o, ep0 + k)
    return ep0 + len(demos)


def corre_tarea(reg, f, p, decide, traza=None):
    """una tarea de prueba. decide(x) -> (elemento, abstiene, efecto_esperado). Devuelve el registro crudo de la tarea."""
    r = dict(fam=f, pasos=0, abst=0, rev=0, irr_prop=0, irr_mal=0, falla='')
    for s in range(len(FAMILIAS[f]['guion'])):
        x = contexto(reg, f, s, p); c = x['verdad']; r['pasos'] += 1
        e, abst, esp = decide(x)
        if e >= 0 and p.irr[e]: r['irr_prop'] += 1
        if abst:
            r['abst'] += 1
            if traza is not None: traza.append((s, x, e, 'ABSTIENE y pide'))
            continue                                                       # la persona hace el paso
        if e < 0: r['falla'] = 'sin_clic'; break
        if p.irr[e]:
            if traza is not None: traza.append((s, x, e, 'pisa IRREVERSIBLE ' + ('(bien)' if e == c else '(MAL)')))
            if e != c: r['irr_mal'] += 1; r['falla'] = 'irreversible'; break
            continue
        if esp is not None and reg.O(p.efecto[e]) != esp:
            r['rev'] += 1
            if traza is not None: traza.append((s, x, e, 'pisa, lo observado NO coincide: deshace y pide'))
            continue
        if traza is not None: traza.append((s, x, e, 'pisa ' + ('(bien)' if e == c else '(MAL, no se entera)')))
        if e != c: r['falla'] = 'reversible'; break
    r['ok'] = int(r['falla'] == ''); r['autonoma'] = int(r['ok'] and r['abst'] + r['rev'] == 0)
    return r


TAUS = [-1.0] + [round(0.001 + 0.025 * i, 4) for i in range(81)] + [9e9]


def prueba(brazos, reg, tareas):
    out = {}
    for b in brazos:
        def dec(x, b=b):
            t0 = time.perf_counter(); r = b.decide(x); b.t_dec += time.perf_counter() - t0; b.n_dec += 1; return r
        out[b.nombre] = [corre_tarea(reg, f, p, dec) for f, p in tareas]
    nns = {'': next(b for b in brazos if b.nombre == '1nn'), 'rec_': next(b for b in brazos if b.nombre == '1nn_reciente')}; cache = {}
    def prop(x, pre):                                                          # 1-NN con abstencion, para toda la rejilla de umbrales
        k = (pre, id(x['p']), x['s'])
        if k not in cache: cache[k] = nns[pre].propone(x)
        return cache[k]
    tabla = {'irr': [], 'todo': [], 'rec_irr': []}                             # rec_irr: desviacion D1 (rival anadido tras ver resultados)
    for var in tabla:
        pre = 'rec_' if var.startswith('rec_') else ''; solo_irr = var.endswith('irr')
        for tau in TAUS:
            def dec(x, tau=tau):
                e, dm = prop(x, pre); return e, bool(dm > tau and (not solo_irr or (e >= 0 and x['p'].irr[e]))), None
            rs = [corre_tarea(reg, f, p, dec) for f, p in tareas]
            tabla[var].append({k: int(sum(r[k] for r in rs)) for k in ('pasos', 'abst', 'rev', 'irr_prop', 'irr_mal', 'ok', 'autonoma')})
    return out, tabla


def corre_semilla(seed, n_prueba=20, C=200, log=print):
    t0 = time.time(); S = prepara_semilla(seed, n_prueba); reg = Registro(); res = dict(seed=seed, n_prueba=n_prueba, C=C, peso_ctx=PESO_CTX, cond={}, nn_tau={}, brazos={}, taus=TAUS)
    def honesto(f, s, x): return x['verdad']
    def version_b(f, s, x): return x['p'].concepto.index(S['B'][f][1]) if s == S['B'][f][0] else x['verdad']
    def ment_inc(f, s, x):
        if S['rng_ment'].random() < 0.4: return int(S['rng_ment'].choice([i for i in range(x['p'].n) if i != x['verdad']]))
        return x['verdad']
    def ment_con(f, s, x): return x['p'].concepto.index(S['MC'][f][1]) if s == S['MC'][f][0] else x['verdad']
    def guarda(cond, brazos):
        o, t = prueba(brazos, reg, S['pruebas'][cond.split('@')[0]]); res['cond'][cond] = o; res['nn_tau'][cond] = t
    # --- escenario honesto: A -> 4 regimenes -> B -> vuelve a A (0, 1 y 2 demostraciones de vuelta)
    bz = brazos_nuevos(seed, C); ep = ensena(bz, reg, S['demos']['A'], 0, honesto)
    for r in REGIMENES: guarda(r, bz)
    res['brazos']['honesto_A'] = estado(bz)
    ep = ensena(bz, reg, S['demos']['B'], ep, version_b); guarda('cambia_y_vuelve@0', bz)
    ep = ensena(bz, reg, S['demos']['vuelta'][0], ep, honesto); guarda('cambia_y_vuelve', bz)
    ep = ensena(bz, reg, S['demos']['vuelta'][1], ep, honesto); guarda('cambia_y_vuelve@2', bz)
    res['brazos']['honesto_fin'] = estado(bz)
    # --- mentirosos (colonias nuevas), probados sin cambio contra la VERDAD del guion
    for cond, fn in (('ment_inc', ment_inc), ('ment_con', ment_con)):
        bz = brazos_nuevos(seed, C); ensena(bz, reg, S['demos'][cond], 0, fn); guarda(cond, bz); res['brazos'][cond] = estado(bz)
    res['B'] = {FAMILIAS[f]['nombre']: [FAMILIAS[f]['guion'][s], c] for f, (s, c) in S['B'].items()}
    res['MC'] = {FAMILIAS[f]['nombre']: [FAMILIAS[f]['guion'][s], c] for f, (s, c) in S['MC'].items()}
    res['n_elementos'] = [int(p.n) for r in S['pruebas'].values() for _, p in r]
    res['seg'] = time.time() - t0; log(f"semilla {seed}: {res['seg']:.1f}s")
    return res


def estado(bz):
    out = {}
    for b in bz:
        d = dict(memoria=int(b.memoria()), us_clic=1e6 * b.t_dec / max(b.n_dec, 1), n_dec=b.n_dec)
        if isinstance(b, ML.Colonia): d.update(nac=int(b.nac), mue=int(b.mue), estrechadas=int(b.estrechadas), N=int(b.N))
        if isinstance(b, CuarentenaClic): d.update(validadas=int(b.val.sum()), hipotesis=int((~b.val).sum()), reversiones=int(b.reversiones), cel_efecto=int(b.efecto.N))
        out[b.nombre] = d
    return out


def sin_tiempos(o):
    """copia sin los campos de tiempo (para comparar dos corridas bit a bit)."""
    if isinstance(o, dict): return {k: sin_tiempos(v) for k, v in o.items() if k not in ('seg', 'us_clic')}
    if isinstance(o, list): return [sin_tiempos(v) for v in o]
    return o


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--humo', action='store_true'); ap.add_argument('--semillas', default='11,12,13,14,15')
    ap.add_argument('--n', type=int, default=20); ap.add_argument('--ctx', type=float, default=0.5); ap.add_argument('--out', default='datos/principal.json'); a = ap.parse_args(); os.chdir(AQUI)
    os.makedirs('datos', exist_ok=True); PESO_CTX = a.ctx
    if a.humo:      # semilla de DESARROLLO 99: no es de evaluacion. Corre dos veces y exige identidad bit a bit (sin tiempos).
        r1 = corre_semilla(99, 5); r2 = corre_semilla(99, 5); igual = json.dumps(sin_tiempos(r1), sort_keys=True) == json.dumps(sin_tiempos(r2), sort_keys=True)
        json.dump([r1], open('datos/humo.json', 'w')); print('IDENTIDAD dos corridas de la semilla 99 (sin tiempos):', 'OK' if igual else 'FALLA')
        print('elementos por pantalla: min', min(r1['n_elementos']), 'max', max(r1['n_elementos'])); sys.exit(0 if igual else 1)
    todo = []
    for s in [int(x) for x in a.semillas.split(',')]:
        todo.append(corre_semilla(s, a.n)); json.dump(todo, open(a.out, 'w'))
    print('escrito', a.out)
