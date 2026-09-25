"""corre_muro2.py — RUNNER del SEGUNDO intento del muro: GLOTU + PATAS (dos piezas, a proposito). Preregistro: PREREGISTRO_muro2.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

NO toca corre_muro.py (sha 503b531ea1213c59: la serie 1 corre con el). Lo IMPORTA y cambia EN MEMORIA solo la configuracion del
bloque (brazos, candidato, control, semillas, humo, carpeta de datos) y agrega a verifica() la comprobacion del carro nuevo. La corrida,
la letra (lee_serie), el resumen, los pareados, nube-9, --reanuda y ERR-115 son los de corre_muro TAL CUAL (misma letra que la serie 1).
Con spawn (Windows) el Pool re-ejecuta este modulo como __mp_main__ en cada trabajador, asi que la configuracion vale tambien alli.

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio = ENMIENDA 5):
  v143            V143                  base
  glotupatas      V143_GLOTUPATAS       CANDIDATO: GLOTU (GLOT 3) + PATAS (PATAS 1)          (construye_muro.py)
  glotupatasdesf  V143_GLOTUPATASDESF   CONTROL desfasado: GLOTU + PATAS al reves (PATAS 2)  (construye_muro2.py)
  o1              O1                    techo y ANCLA
  mtel            V143_MTEL             solo humo/arnes (V143 + telemetria)
SEMILLAS: serie 37101-37120 · replica 37121-37140 · practica 37901-37919 (exploratorio 37901-37905; humo 37911-37912; arnes 37913-37914).

  python experimentos/organelos/muro/corre_muro2.py --humo
  python experimentos/organelos/muro/corre_muro2.py --serie --desde 37101 --n 20 --pool 6
  python experimentos/organelos/muro/corre_muro2.py --serie --desde 37121 --n 20 --pool 6      # replica
  python experimentos/organelos/muro/corre_muro2.py --bloque <resumen serie>,<resumen replica>
  python experimentos/organelos/muro/corre_muro2.py --explora 37901 glotupatasdesf               # EXPLORATORIO, una corrida
"""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_muro as CM
import construye_muro2 as CB2

SHA_CORRE_MURO = '503b531ea1213c59'
CV = CM.CV; P = CM.P; RC = CM.RC

# ------------------------------------------------------------------ configuracion del segundo intento (en memoria)
CM.BRAZOS['glotupatasdesf'] = 'V143_GLOTUPATASDESF'
CM.PROPIOS = tuple(CM.PROPIOS) + ('V143_GLOTUPATASDESF',)
CM.CAND = 'glotupatas'; CM.CTRL = 'glotupatasdesf'
CM.SERIE_BRAZOS = ('v143', 'glotupatas', 'glotupatasdesf', 'o1')
CM.SERIE = range(37101, 37121); CM.REPLICA = range(37121, 37141); CM.PRACTICA = range(37901, 37920)
CM.HUMO = [(37911, 'mtel'), (37911, 'glotupatas'), (37911, 'glotupatasdesf'), (37911, 'o1'), (37912, 'mtel'), (37912, 'glotupatas')]
CM.DATOS = os.path.join(AQUI, 'datos', 'muro2')
_verifica1 = CM.verifica


def verifica2(log):
    """la de corre_muro (shas, carros de construye_muro, identidad corta) + el carro nuevo + los shas de los dos instrumentos."""
    ok = _verifica1(log)
    s = CM.h16(CM.__file__); ok &= s == SHA_CORRE_MURO
    log(f"  sha corre_muro.py {s} {'OK' if s == SHA_CORRE_MURO else '!= ' + SHA_CORRE_MURO + ' FALLA'}")
    s = CM.CB.h16(CM.CB.__file__); ok &= s == CB2.SHA_CONSTRUYE_MURO
    log(f"  sha construye_muro.py {s} {'OK' if s == CB2.SHA_CONSTRUYE_MURO else 'FALLA'}")
    for n, b in CB2.todas2().items():
        ruta = os.path.join(CM.CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_muro2']
        ok &= igual and not vr
        log(f"  carro {n} sha {CM.CB.h16b(b)} == construye_muro2: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    CM.registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    base = N(P.run(37913, [('C', CV.modulo('V143'))] * 9, T=2000, fundador_limpio=1))
    for n in ('V143_GLOTUPATAS', 'V143_GLOTUPATASDESF'):
        m = CV._MODS[n]; g = (m.PAGA, m.GLOT, m.PATAS, m.TELEM)
        try:
            m.PAGA = 0; m.GLOT = 0; m.PATAS = 0; m.TELEM = 0
            x = N(P.run(37913, [('C', m)] * 9, T=2000, fundador_limpio=1))
        finally:
            m.PAGA, m.GLOT, m.PATAS, m.TELEM = g
        i = x == base; ok &= i
        log(f"  IDENTIDAD CORTA: {n} con PAGA = GLOT = PATAS = TELEM = 0 == V143 (salida ENTERA, N 9, s 37913, T 2000): {'OK' if i else 'FALLA'}")
    return ok


CM.verifica = verifica2


def explora(argv):
    """EXPLORATORIO (no es dato): una corrida, semillas 37901-37905, JSON en datos/explora/ (lo lee explora_muro.py --lee)."""
    if len(argv) != 2: raise SystemExit("--explora <semilla> <brazo>")
    seed = int(argv[0]); brazo = argv[1]
    if seed not in range(37901, 37906): raise SystemExit("--explora: solo 37901-37905")
    if brazo not in CM.BRAZOS: raise SystemExit(f"brazo desconocido {brazo!r}")
    dest = os.path.join(AQUI, 'datos', 'explora'); os.makedirs(dest, exist_ok=True)
    x = CM.trabajo((seed, brazo, 100000, dest, False))
    print(brazo, seed, x.get('seg'), x['aborto'])
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--explora': sys.exit(explora(sys.argv[2:]))
    sys.exit(CM.main())
