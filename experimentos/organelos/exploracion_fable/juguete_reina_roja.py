# EXPLORATORIO, no es dato
"""juguete_reina_roja.py -- ¿un VENENO QUE EVOLUCIONA (parásito, Reina Roja) acelera la evolución del bicho sin que
ningún juez elija ganadores?

Misión: llegar a la AGI por este camino. Mundo de bolsillo, misma retina de 6 bits que el bicho (organismo_f9c.py:143).
Idea (Hillis 1990, parásitos coevolutivos; Zaman et al. 2014 PLoS Biol 12:e1002023, coevolución en Avida): el mundo de
ECO es FIJO (cada letra vale siempre lo mismo). Un mundo fijo se agota: cuando la boca ya distingue A,B,C,D no queda
nada que seleccionar. Si el veneno es un LINAJE que se reproduce cuando lo muerden, el veneno evoluciona a parecerse
a la comida y la boca tiene que seguir cambiando. Nadie juzga: el veneno que engaña deja más copias; el bicho que no se
deja engañar deja más hijos.

MUNDO
- Bichos como en juguete_ohno (genoma de órganos de largo variable, con dup/del/inv/fus). Ven una letra por paso.
- Letras: 2 comidas FIJAS (A y C del bicho, +1) y una POBLACIÓN de 40 venenos (-1), cada uno con su patrón de 6 bits.
  Cada paso, la letra que ve un bicho es comida (1/2) o un veneno al azar de la población (1/2).
- Brazo FIJO: los 40 venenos son copias de B y D (los del bicho) y no cambian.
- Brazo REINA_ROJA: cuando un bicho MUERDE un veneno, con p 0.01 ese veneno deja una copia (con 1 bit mutado con p 0.3)
  que reemplaza al veneno MENOS mordido recientemente (el que nadie muerde se extingue). [Primera versión: "uno que no
  fue mordido en 200 pasos"; nunca ocurría (cambiosV = 0, brazo == FIJO): error de instrumento, corregido y declarado.] Un veneno no puede copiar exactamente a una comida (si el patrón mutado == A o C, la mutación no ocurre):
  mimetismo imperfecto, como en la naturaleza.
- Control RUIDO: la población de venenos cambia a la misma tasa pero AL AZAR (sin depender de si fueron mordidos).
  Separa "el mundo cambia" de "el mundo me persigue".

MEDIDAS (cada 100 pasos): acierto de la boca; largo medio del genoma; número de órganos DISTINTOS en la población
(patrón, signo); y TASA DE RECAMBIO: fracción de órganos distintos del final que NO existían a T/2 (novedad).

PREDICCIONES ESCRITAS ANTES DE CORRER (pueden fallar):
  P1  REINA_ROJA tiene MÁS órganos distintos al final que FIJO en >= 4 de 5 semillas (diversidad por persecución).
  P2  REINA_ROJA tiene MÁS novedad (recambio T/2 -> T) que FIJO y que RUIDO en >= 4 de 5.
  P3  el acierto de REINA_ROJA es MENOR que el de FIJO (la Reina Roja se paga: correr para quedarse en el sitio).
  P4  RUIDO queda entre los dos en novedad (cambiar el mundo al azar también renueva, pero menos que perseguir).
  P5  en REINA_ROJA el veneno del final se parece MÁS a la comida (distancia de Hamming media a A/C menor) que en RUIDO.
Semillas 23011-23015. Un proceso. < 5 minutos.
"""
import time
import numpy as np
from juguete_ohno import organo_azar, decide, muta, PAT0, UMBRAL

COSTO = 0.02; E_PARTO = 2.0; E_NACE = 1.0; EDAD_MAX = 400; TOPE = 200; N0 = 60; NVEN = 40; VENT = 200
P_COPIA = 0.01   # por mordida a un veneno (≈ 30 mordidas/paso → ≈ 0.3 copias/paso; RUIDO cambia 0.6/paso: se reportan los dos)
COMIDA = np.array([PAT0['A'], PAT0['C']], float)


def hamming_a_comida(V):
    return float(np.mean([min(np.sum(v != COMIDA[0]), np.sum(v != COMIDA[1])) for v in V]))


def conjunto(cuerpos):
    s = set()
    for b in cuerpos:
        for p, w in b['g']: s.add((tuple(int(x) for x in p), int(np.sign(w))))
    return s


def corre(seed, brazo, T=4000):
    r = np.random.default_rng(seed)
    V = np.array([PAT0['B'] if i % 2 == 0 else PAT0['D'] for i in range(NVEN)], float)
    ult_mord = np.zeros(NVEN, int)
    cuerpos = [dict(g=[organo_azar(r) for _ in range(4)], E=E_NACE, edad=0) for _ in range(N0)]
    acierto = []; norg = []; S_mitad = None; cambios = 0
    for t in range(T):
        vivos = []; nuevos = []; ok = 0; n = 0
        for b in cuerpos:
            if r.random() < 0.5:
                ret = COMIDA[int(r.integers(2))]; val = 1.0; iv = -1
            else:
                iv = int(r.integers(NVEN)); ret = V[iv]; val = -1.0
            m = decide(b['g'], 2 * ret - 1, r)
            if m:
                b['E'] += val
                if iv >= 0:
                    ult_mord[iv] = t
                    if brazo == 'REINA_ROJA' and r.random() < P_COPIA:   # el veneno mordido se copia (con error) sobre el MENOS mordido
                        # CORRECCIÓN (primera corrida: cambiosV = 0, brazo idéntico a FIJO): con ~200 cuerpos todos los venenos se
                        # muerden cada paso y nunca hay uno sin morder en 200 pasos. Ahora reemplaza al menos mordido recientemente.
                        k = int(np.argmin(ult_mord))
                        if k != iv:
                            hijo = V[iv].copy()
                            if r.random() < 0.3:
                                j = int(r.integers(6)); hijo[j] = 1 - hijo[j]
                                if any((hijo == c).all() for c in COMIDA): hijo = V[iv].copy()
                            V[k] = hijo; ult_mord[k] = t; cambios += 1
            ok += int(m == (val > 0)); n += 1
            b['E'] -= COSTO; b['edad'] += 1
            if b['E'] <= 0 or b['edad'] > EDAD_MAX: continue
            if b['E'] >= E_PARTO and len(cuerpos) + len(nuevos) < TOPE:
                b['E'] /= 2; nuevos.append(dict(g=muta(b['g'], r, 'ESTRUCTURA'), E=b['E'], edad=0))
            vivos.append(b)
        if brazo == 'RUIDO' and r.random() < 0.6:                    # misma tasa aproximada de recambio (se calibra abajo), al azar
            iv = int(r.integers(NVEN)); hijo = V[int(r.integers(NVEN))].copy()
            if r.random() < 0.3:
                j = int(r.integers(6)); hijo[j] = 1 - hijo[j]
                if any((hijo == c).all() for c in COMIDA): hijo = V[iv].copy()
            V[iv] = hijo; cambios += 1
        cuerpos = vivos + nuevos
        if not cuerpos: return dict(extinto=t)
        if t % 100 == 0:
            acierto.append(ok / max(n, 1)); norg.append(float(np.mean([len(b['g']) for b in cuerpos])))
        if t == T // 2: S_mitad = conjunto(cuerpos)
    S_fin = conjunto(cuerpos)
    novedad = len(S_fin - S_mitad) / max(len(S_fin), 1)
    return dict(extinto=None, acierto=acierto, norg=norg, distintos=len(S_fin), novedad=novedad, cambios=cambios,
                ham=hamming_a_comida(V), vivos=len(cuerpos), nven_distintos=len(set(map(tuple, V.astype(int)))))


if __name__ == '__main__':
    t0 = time.time()
    print("EXPLORATORIO, no es dato -- juguete_reina_roja: veneno que evoluciona contra veneno fijo")
    print(f"{'brazo':11s} {'seed':>6s} {'ac_mitad':>8s} {'ac_fin':>7s} {'norgF':>6s} {'distintos':>9s} {'novedad':>7s} {'cambiosV':>8s} {'hamV':>5s} {'venDist':>7s} {'vivos':>5s}")
    res = {}
    for brazo in ('FIJO', 'REINA_ROJA', 'RUIDO'):
        for seed in range(23011, 23016):
            d = corre(seed, brazo); res[(brazo, seed)] = d
            if d.get('extinto') is not None: print(f"{brazo:11s} {seed:6d}  EXTINTO en t={d['extinto']}"); continue
            a = d['acierto']
            print(f"{brazo:11s} {seed:6d} {a[len(a)//2]:8.2f} {a[-1]:7.2f} {d['norg'][-1]:6.1f} {d['distintos']:9d} {d['novedad']:7.2f} {d['cambios']:8d} {d['ham']:5.2f} {d['nven_distintos']:7d} {d['vivos']:5d}")
    print(f"{time.time()-t0:.0f} s")
