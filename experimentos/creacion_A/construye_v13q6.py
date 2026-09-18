"""CREADOR A — construye `organismo_v13q6.py` POR ANCLAS desde `organismo_v13q5.py` (`fae9c32b146fdbb4`, solo se lee;
que viene de v13q4 `3cc732dd2b2519cd` <- v13q3 `aaebe073308a40c2`).

UNICA perilla nueva: `ntr` (tamano de la particion de entrenamiento del mundo de regla). `ntr=None` (por defecto)
deja los valores de siempre — `(4,4)` en xor01, `(5,5)` en px0/azar — o sea `organismo_v13q5` EXACTO.

POR QUE (bloque A-6): el mecanismo de seleccion del rasgo conjuntivo no falla por ser local ni por ruido. Falla
porque **la informacion no esta en 8 patrones**: con la particion de hoy, el estadistico IDEAL (residuo del ajuste
elemental EXACTO, que ninguna regla local puede superar) pone `P0*P1` en primer lugar solo en **3 de 20** semillas.
La transicion esta medida y es brusca: a 14 patrones de tren (8 comida + 6 veneno) pasa a **12/20** y el acierto,
si se abre el ganador, salta de 0.625 a **1.000**. `ntr` convierte eso en una variable manipulable DENTRO del
organismo, para medir la transicion en vez de suponerla.

AVISO (trampa 3 de EQUIPO.md, declarado): mover `ntr` **cambia el mundo**, no la regla. Al subir el tren baja el
test (de 12 nunca vistos a 6), asi que la medida se vuelve mas ruidosa y NO es comparable numero a numero con los
bloques 3-4. Por eso el brazo `ntr=(4,4)` se corre siempre, en las mismas semillas, como referencia interna.

Uso: python construye_v13q6.py
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, 'organismo_v13q5.py')
DEST = os.path.join(AQUI, 'organismo_v13q6.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]
assert sha == 'fae9c32b146fdbb4', f'origen inesperado: {sha}'


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


# ---- ancla 1: firma de split_regla
A1 = "def split_regla(seed, regla):"
B1 = "def split_regla(seed, regla, ntr_ovr=None):   # creacion_A A-6: `ntr_ovr` sobreescribe el tamano del tren (None = el de siempre)"
out = sust(src, A1, B1, etq='firma de split_regla')

# ---- ancla 2: usar el ntr dado, si lo hay
A2 = "    food = [k for k in nombres if vr[k] == 'comida']; pois = [k for k in nombres if vr[k] == 'veneno']"
B2 = ("    if ntr_ovr is not None: ntr = (int(ntr_ovr[0]), int(ntr_ovr[1]))   # creacion_A A-6: DESPUES de las ramas, para que no lo pisen\n" + A2)
out = sust(out, A2, B2, etq='override de ntr')

# ---- ancla 3: firma de run
A3 = "sel_estad='cond',lab=False):"
B3 = "sel_estad='cond',lab=False,ntr=None):"
out = sust(out, A3, B3, etq='firma de run')

# ---- ancla 4: la llamada a split_regla dentro de run
A4 = "    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en=T//2 if fase2_en is None else fase2_en"
B4 = "    else: P_,tren,test,val_regla=split_regla(seed,regla,ntr); fase2_en=T//2 if fase2_en is None else fase2_en   # creacion_A A-6"
out = sust(out, A4, B4, etq='llamada a split_regla')

# ---- ancla 5: el return (dejar constancia del ntr efectivo)
A5 = "    return dict(lab=lab,"
B5 = "    return dict(ntr=ntr,lab=lab,"
out = sust(out, A5, B5, etq='return')

cab = (f'"""organismo_v13q6 = organismo_v13q5.py ({sha}) + perilla `ntr` (tamano del tren del mundo de regla).\n'
       f'Con ntr=None es organismo_v13q5 EXACTO (identidad obligatoria: identidad_v13q6.py), y con las perillas\n'
       f'`seleccion` y `lab` tambien apagadas, organismo_v13q3 exacto.\n'
       f'AVISO: mover `ntr` cambia el MUNDO (sube el tren, baja el test). Declarado en PREREGISTRO_xor_6.md.\n'
       f'Generado por experimentos/creacion_A/construye_v13q6.py. NO editar a mano."""\n')
open(DEST, 'w', encoding='utf-8').write(cab + out)
print(f'origen organismo_v13q5.py sha {sha}')
print(f'escrito organismo_v13q6.py  sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
