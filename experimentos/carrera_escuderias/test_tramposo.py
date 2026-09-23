"""test_tramposo.py — ERR-96: un carro NO puede fabricar su R0 (ni su vida, ni sus causas de muerte).

MISION: llegar a la AGI por este camino. La auditoria demostro que con d.update(c.salida()) un carro tramposo
declaraba 999999 hijos con 0 reales. Aqui se prueba que ya no se puede, y que el chequeo estatico rechaza los
caminos a los frames, a los modulos de la pista y a los archivos. Un proceso, sin Pool.

  (1) SALIDA FALSA: un carro = FABRICA + salida() que devuelve descendientes=999999, deaths=0, vidas_h1,
      fundadores, _carrera y causas falsas. El juez (resumen_linaje) da EXACTAMENTE lo mismo que para FABRICA
      honesto con la misma semilla; lo falso queda encerrado en d['carro']; pista.plano() lo DETECTA (aborta).
  (2) MUTAR LO QUE RECIBE: el carro reescribe obs (E, Ag, pos, t), res (dS, mordio), info (edad, hijos, causa)
      e intenta escribir en objs (vista de solo lectura). La verdad fisica no cambia.
  (3) CHEQUEO ESTATICO: 20 fuentes tramposas RECHAZADAS; FABRICA PASA.
  (4) EL JUEZ ABORTA una ronda con un carro rechazado (archivo temporal en carros/, se borra al final).
Uso:  python experimentos/carrera_escuderias/test_tramposo.py   (escribe test_tramposo_salida.txt)
"""
import json, os, sys, time, types

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pista as P
import juez as J
import revisa_carro as RC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'test_tramposo_salida.txt'), 'w', encoding='utf-8')
T = 20000
SEM = (4001, 4002)


def out(s=''):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def di(et, ok, extra=''):
    OK[1] += 1; OK[0] += int(bool(ok))
    out(f"  {'OK   ' if ok else 'FALLA'} {et}   {extra}")


FAB = P.carga_carro('FABRICA')


class Mentiroso(FAB.Carro):
    def salida(self):
        d = super().salida()
        d.update(descendientes=999999, deaths=0, vidas_h1=[T], fundadores=0, desc_por_vida=[999999], nacimientos=0,
                 origen_cuerpo=[1], T_efectivo=T, muertes_nec=[0, 0],
                 _carrera=dict(id='X', indice=0, causas={'hambre': 0, 'sed': 0, 'veneno': 0, 'sal': 0}, causa_cuerpo=[],
                               escrituras=0, escr=[], vetos=0, p1=[1], c1=[1], t_ok=[0]))
        return d


class Mutante(FAB.Carro):
    def actua(self, obs):
        a = super().actua(obs)
        obs['E'] = 99.0; obs['Ag'] = 99.0; obs['pos'] = 0; obs['t'] = -1
        try:
            obs['objs'][0] = 'A'   # vista de solo lectura: tiene que fallar
            self.escribio_objs = True
        except TypeError:
            self.escribio_objs = False
        return a

    def resultado(self, res):
        super().resultado(res)
        res['dS'] = (5.0, 5.0); res['mordio'] = True; res['letra'] = 'A'

    def muere(self, info):
        super().muere(info)
        info['edad'] = 10 ** 6; info['hijos'] = 10 ** 6; info['causa'] = 'hambre'

    def al_parir(self, info):
        info['k'] = -1
        return {'dote': 99.0}   # intenta regalarse una dote: la pista guarda la dote aparte


def mod(cls):
    return types.SimpleNamespace(crea=lambda ctx: cls(ctx))


SIN = ('id', 'telem')


def limpio(x):
    return {k: v for k, v in x.items() if k not in SIN}


MALOS = {
    'sys._getframe': "import numpy as np\ndef crea(ctx):\n    import sys\n    return sys._getframe(1)\n",
    'inspect': "import inspect\ndef crea(ctx): return None\n",
    'gc': "import gc\ndef crea(ctx): return gc.get_objects()\n",
    'globals()': "def crea(ctx): return globals()\n",
    '__builtins__': "def crea(ctx): return __builtins__\n",
    'f_back': "def crea(ctx):\n    try: raise Exception\n    except Exception as e: return e.__traceback__.tb_frame.f_back\n",
    'f_locals': "def crea(ctx): return ctx.f_locals\n",
    'importlib': "import importlib\ndef crea(ctx): return importlib.import_module('pista')\n",
    'import pista': "import pista\ndef crea(ctx): return None\n",
    'from juez import': "from juez import resumen_linaje\ndef crea(ctx): return None\n",
    'import organismo_f9c': "import organismo_f9c\ndef crea(ctx): return None\n",
    'np.random global': "import numpy as np\ndef crea(ctx):\n    np.random.seed(1)\n    return None\n",
    'from numpy import random': "from numpy import random\ndef crea(ctx): return None\n",
    'exec(': "def crea(ctx):\n    exec('x=1')\n",
    'eval(': "def crea(ctx):\n    return eval('1')\n",
    'open(w)': "def crea(ctx):\n    open('x.txt', 'w')\n",
    'np.save': "import numpy as np\ndef crea(ctx):\n    np.save('x', np.zeros(2))\n",
    'getattr(sys,...)': "import math\ndef crea(ctx):\n    return getattr(math, 'pi')\n",
    'x.__dict__': "def crea(ctx):\n    return ctx.__dict__\n",
    'import os': "import os\ndef crea(ctx): return os.listdir('.')\n",
}


def main():
    t0 = time.time()
    out(f"TEST TRAMPOSO (ERR-96) · {time.strftime('%Y-%m-%d %H:%M:%S')} · pista {P.h16(os.path.join(AQUI,'pista.py'))} · "
        f"juez {P.h16(os.path.join(AQUI,'juez.py'))} · revisa_carro {P.h16(os.path.join(AQUI,'revisa_carro.py'))}")
    out(f"\n(1) SALIDA FALSA (descendientes=999999, deaths=0, ...) · T={T} · semillas {SEM}")
    for s in SEM:
        h = P.run(s, ['FABRICA'], T=T, pizarra=0); m = P.run(s, [('FABRICA', mod(Mentiroso))], T=T, pizarra=0)
        rh = J.resumen_linaje(h['linajes'][0], s); rm = J.resumen_linaje(m['linajes'][0], s)
        di(f"(1a) s={s} juez(tramposo) == juez(honesto)", N(limpio(rh)) == N(limpio(rm)) and rm['R0'] != round(999999 / 1, 4),
           f"R0 {rm['R0']} (honesto {rh['R0']}) · desc {rm['descendientes']} · muertes {rm['muertes']} · coherente {rm['coherente']}")
        fis = {k: v for k, v in m['linajes'][0].items() if k != 'carro'}
        fish = {k: v for k, v in h['linajes'][0].items() if k != 'carro'}
        di(f"(1b) s={s} la verdad fisica del tramposo == la del honesto; lo falso esta SOLO en d['carro']",
           N(fis) == N(fish) and m['linajes'][0]['carro']['descendientes'] == 999999,
           f"d['carro']['descendientes'] = {m['linajes'][0]['carro']['descendientes']} (no lo lee nadie)")
        try:
            P.plano(m['linajes'][0]); ok, msg = False, 'NO detecto'
        except SystemExit as e:
            ok, msg = True, str(e)[:100]
        di(f"(1c) s={s} plano() DETECTA el choque de claves", ok, msg)
    out("\n(2) MUTAR obs / res / info / objs")
    for s in SEM:
        h = P.run(s, ['FABRICA'], T=T, pizarra=0)
        box = []
        def crea(ctx, box=box):
            c = Mutante(ctx); box.append(c); return c
        m = P.run(s, [('FABRICA', types.SimpleNamespace(crea=crea))], T=T, pizarra=0)
        fis = {k: v for k, v in m['linajes'][0].items() if k != 'carro'}
        fish = {k: v for k, v in h['linajes'][0].items() if k != 'carro'}
        di(f"(2) s={s} verdad fisica intacta y objs no se puede escribir", N(fis) == N(fish) and box[0].escribio_objs is False,
           f"R0 {J.resumen_linaje(m['linajes'][0], s)['R0']} (honesto {J.resumen_linaje(h['linajes'][0], s)['R0']}) · escribio objs {box[0].escribio_objs}")
    out("\n(3) CHEQUEO ESTATICO")
    di('(3a) FABRICA PASA', RC.revisa('FABRICA') == [], str(RC.revisa('FABRICA')))
    for et, src in MALOS.items():
        v = RC.revisa_fuente(src, et)
        di(f"(3b) RECHAZA {et}", bool(v), (v[0][:90] if v else 'PASO (mal)'))
    out("\n(4) EL JUEZ ABORTA una ronda con un carro rechazado")
    tmp = os.path.join(P.CARROS, '_TRAMPOSO_TEST.py')
    open(tmp, 'w', encoding='utf-8').write(MALOS['sys._getframe'])
    argv = sys.argv
    try:
        sys.argv = ['juez.py', '--humo', '--ronda', 'test_tramposo', '--carros', '_TRAMPOSO_TEST']
        rc = J.main()
    finally:
        sys.argv = argv; os.remove(tmp)
    di('(4) juez.main() devuelve 1 sin correr', rc == 1, f"rc {rc} · archivo temporal borrado {not os.path.exists(tmp)}")
    out(f"\nTOTAL {OK[0]}/{OK[1]} en {time.time()-t0:.1f}s")
    SAL.close()
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
