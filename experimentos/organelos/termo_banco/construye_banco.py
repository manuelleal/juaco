"""construye_banco.py — construye POR ANCLAS los carros del bloque TERMO_BANCO (28-sep-2026, creador; preregistro PREREGISTRO_termo_banco.md).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros.

PREGUNTA: en TERMO_EVO (nube) la seleccion SI subia el gen g del margen del termostato (evo vs sinher 18/20; padres 0.066 -> 0.092 en
100k), pero cada fundador nuevo (ENMIENDA 5) sorteaba g de la distribucion inicial, la zona letal, y la refundacion borraba lo ganado.
Si el linaje guarda su GERMOPLASMA (un banco de semillas con los g de sus cuerpos que parieron), y el fundador nuevo sale de ese banco
(+ la mutacion de siempre) en vez de la inicial, lo que la seleccion gana ya no se pierde con la extincion. Se establece el linaje?

ORIGEN (solo se LEE; sha16 fijado): carros/V143_EVO_BAJO.py de la nube (SHA_BAJO = 3187b373654e119f; traido por trae_nube.py desde
origin/nube/termo-evo-20260928 c43e12a; es construye_evo.construye('V143_EVO_BAJO', ...) desde tronco_v14_3/carros_v143/V143.py).
Cada ancla EXACTAMENTE una vez o aborta. Fin de linea CRLF (el del origen).

PIEZA NUEVA (una sola: de donde sale el g del FUNDADOR; todo lo demas es V143_EVO_BAJO bit a bit):
  BANCO = 0  -> V143_EVO_BAJO bit a bit (salida ENTERA y _TEL; arnes (a)).
  BANCO = 1  -> EVO_BANCO: cada vez que un cuerpo del linaje PARE, su g (el del padre, sin mutar) entra al banco del linaje
               (_BANCO[indice]; un parto = una entrada: el que mas pare mas semillas deja). Tamano = cola_max de la pista (200, leido de
               ctx['fabrica']['kw']['cola_max']: las semillas que el linaje puede tener esperando en la cola); reemplazo FIFO (entra la
               nueva, sale la mas vieja: la regla de la cola de la pista, pista.py l. 369). Fundador (crea(ctx): el primero y cada
               refundacion de la ENMIENDA 5): banco propio vacio -> g ~ U[G_INI] como en EVO (mismo rng, mismos sorteos); si no -> una
               entrada del banco propio al azar (uniforme) + N(0, SIGMA), recortada a G_CLIP (la mutacion de siempre, la de _ev_parir).
  BANCO = 2  -> BANCO_BARAJADO (CONTROL): el mismo banco y el mismo momento de activacion (banco PROPIO no vacio), pero la semilla sale
               del banco de OTRO linaje de la misma corrida, elegido al azar entre los que tienen semillas (uniforme), y luego una entrada
               al azar; si ningun otro tiene, g ~ U[G_INI]. Hay herencia de germoplasma, pero no del propio linaje.
  El banco se REINICIA solo si el rng del cuerpo del linaje (ctx['rng'], el MISMO objeto en todas las refundaciones de una corrida) no es
  el guardado: corrida nueva de la pista -> se vacia todo _BANCO. Ademas el runner lo borra antes de cada pista.run (dos cerrojos).
  Memoria nueva: <= 200 floats por linaje (el banco). Todo sorteo sale del rng del gen (self._grng, spawn del rng del cuerpo): ni el
  rng del mundo, ni el del cuerpo, ni rng_hijo se tocan.
Telemetria (solo escritura; ERR-96, no puntua): _TEL[indice]['fund_banco'] = [origen (0 inicial, 1 banco propio, 2 banco ajeno), g,
  tamano del banco propio] por fundador; d['carro']['evo']['banco'] de la ultima instancia.

Genera en termo_banco/carros/ (difieren SOLO en las dos lineas de perillas y el nombre; se verifica):
  V143_EVO_BANCO      EVO 1, G_INI (-0.10, 0.10), SIGMA 0.03, BANCO 1   CANDIDATO
  V143_EVO_BANCOBAR   EVO 1, G_INI (-0.10, 0.10), SIGMA 0.03, BANCO 2   CONTROL (germoplasma de otro linaje)
  V143_EVO_BANCO_M40  EVO 1, G_INI ( 0.40,  0.40), SIGMA 0.0,  BANCO 1   solo ARNES (== V143_EVO_M40 de la nube en la fisica)

    python experimentos/organelos/termo_banco/construye_banco.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'carros', 'V143_EVO_BAJO.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_BAJO = '3187b373654e119f'
NL = '\r\n'

VARIANTES = [('V143_EVO_BANCO', (-0.1, 0.1), 0.03, 1), ('V143_EVO_BANCOBAR', (-0.1, 0.1), 0.03, 2),
             ('V143_EVO_BANCO_M40', (0.4, 0.4), 0.0, 1)]
# la linea de perillas de EVO, EXACTA como la escribe construye_evo.PERILLAS (con EVO 1)
PER_EVO = ("EVO = 1; G_INI = ({lo}, {hi}); SIGMA = {s}; G_CLIP = (-0.2, 1.0)   "
           "# termo_evo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (EVO 0 = V143 bit a bit; 1 = hereda; 2 = SINHER)")
PER_BANCO = ("BANCO = {b}   # termo_banco: 0 = V143_EVO_BAJO bit a bit; 1 = el fundador sale del banco del PROPIO linaje; "
             "2 = BARAJADO, del banco de OTRO linaje (control)")

FUNCS = '''_BANCO = {}   # termo_banco: banco de semillas por linaje: indice -> dict(rng=<rng del cuerpo del linaje>, g=[...], cap, fund)


def _bn_toma(propio, otros, rng, modo):
    """termo_banco: g BASE del fundador y su origen. propio = lista del banco del linaje; otros = listas de los demas linajes (orden
    por indice). Banco propio vacio -> (None, 0): sortear de la inicial. modo 1: una entrada del propio al azar -> (g, 1). modo 2: un
    linaje ajeno al azar entre los que tienen semillas y una entrada al azar -> (g, 2); si ninguno tiene -> (None, 0)."""
    if not propio: return None, 0
    if modo == 1: return float(propio[int(rng.integers(len(propio)))]), 1
    cand = [b for b in otros if b]
    if not cand: return None, 0
    b = cand[int(rng.integers(len(cand)))]
    return float(b[int(rng.integers(len(b)))]), 2
'''

METODOS = '''
    # ================================================================ termo_banco: BANCO DE SEMILLAS DEL LINAJE (de donde sale el g del FUNDADOR)
    def _bn_fundador(self, ctx):
        b = _BANCO.get(self._ind)
        if b is None or b['rng'] is not ctx['rng']:                     # corrida nueva de la pista: todo banco viejo es de otra
            if b is not None: _BANCO.clear()
            b = _BANCO[self._ind] = dict(rng=ctx['rng'], g=[], cap=int(ctx['fabrica']['kw']['cola_max']), fund=[0, 0, 0])
        otros = [v['g'] for k, v in sorted(_BANCO.items()) if k != self._ind]
        base, o = _bn_toma(b['g'], otros, self._grng, BANCO)
        if base is None: g = self._ev_sortea()                               # banco vacio: la inicial, como EVO (mismos sorteos)
        else: g = float(min(max(base + float(self._grng.normal(0.0, SIGMA)), G_CLIP[0]), G_CLIP[1]))   # la mutacion de siempre
        b['fund'][o] += 1
        self._ev_tel().setdefault('fund_banco', []).append([int(o), round(g, 5), len(b['g'])])
        return g

    def _bn_guarda(self):
        b = _BANCO[self._ind]; b['g'].append(float(self._g))                # el g del cuerpo que PARE (sin mutar)
        if len(b['g']) > b['cap']: b['g'].pop(0)                            # FIFO: la regla de la cola de la pista

    def _bn_salida(self):
        b = _BANCO.get(self._ind) or dict(g=[], cap=0, fund=[0, 0, 0])
        return dict(modo=BANCO, n=len(b['g']), cap=b['cap'], fund_inicial=b['fund'][0], fund_propio=b['fund'][1], fund_ajeno=b['fund'][2],
                    g_media=(round(sum(b['g']) / len(b['g']), 5) if b['g'] else None))
'''


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def anclas(nombre, gi, s, bmodo):
    per_evo_bajo = PER_EVO.format(lo=-0.1, hi=0.1, s=0.03)
    return [
        ('"""V143_EVO_BAJO.py — termo_evo: V143 + termostato de boca con el margen como GEN heredable (ver construye_evo.py).' + NL,
         f'"""{nombre}.py — termo_banco: V143_EVO_BAJO + BANCO DE SEMILLAS DEL LINAJE para el fundador (ver construye_banco.py).' + NL
         + f'GENERADO por experimentos/organelos/termo_banco/construye_banco.py desde termo_banco/carros/V143_EVO_BAJO.py (sha {SHA_BAJO}).' + NL
         + f'NO editar a mano. Perillas: {PER_EVO.format(lo=gi[0], hi=gi[1], s=s).split("   #")[0]}; BANCO = {bmodo}. Con BANCO = 0 es'
         + ' V143_EVO_BAJO bit a bit.' + NL + NL
         + 'V143_EVO_BAJO.py — termo_evo: V143 + termostato de boca con el margen como GEN heredable (ver construye_evo.py).' + NL),
        (per_evo_bajo + NL + '_TEL = {}',
         PER_EVO.format(lo=gi[0], hi=gi[1], s=s) + NL + PER_BANCO.format(b=bmodo) + NL + '_TEL = {}'),
        ('        self._g = self._ev_sortea(); self._gorig = 0; self._gt0 = None' + NL,
         '        self._g = (self._bn_fundador(ctx) if BANCO else self._ev_sortea()); self._gorig = 0; self._gt0 = None'
         '   # termo_banco: el fundador sale del banco' + NL),
        ("        self._ev_tel()['partos'].append([int(info['t']), round(self._g, 5)])" + NL,
         "        self._ev_tel()['partos'].append([int(info['t']), round(self._g, 5)])" + NL
         + "        if BANCO: self._bn_guarda()   # termo_banco: el g del cuerpo que pare queda en el banco del linaje (semilla en el suelo)" + NL),
        ("        return dict(evo=EVO, g_ini=list(G_INI), sigma=SIGMA, g_final=round(self._g, 5), **self._tm)" + NL,
         "        return dict(evo=EVO, g_ini=list(G_INI), sigma=SIGMA, g_final=round(self._g, 5), **self._tm," + NL
         + "                    **({'banco': self._bn_salida()} if BANCO else {}))   # termo_banco: telemetria (ERR-96: no puntua)" + NL
         + METODOS.replace('\n', NL)),
        (NL + NL + 'class Carro', NL + NL + FUNCS.replace('\n', NL) + NL + NL + 'class Carro'),
    ]


def construye(nombre, gi, s, bmodo):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_BAJO: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_BAJO}")
    txt = src.decode('utf-8')
    for a, rep in anclas(nombre, gi, s, bmodo):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, gi, s, b) for n, gi, s, b in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    base = outs['V143_EVO_BANCO'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('EVO = ' in ls[i] or 'BANCO = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_EVO_BANCO en algo mas que perillas/nombre: lineas {dif[:6]}")
    ok = True
    os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            tmp = ruta + '.tmp'
            with open(tmp, 'wb') as fh: fh.write(bts)
            os.replace(tmp, ruta)
            print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143_EVO_BAJO.py sha {h16(ORIGEN)} (fijado {SHA_BAJO}) - construye_banco.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
