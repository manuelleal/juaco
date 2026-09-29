"""construye_eco_ing_a_carrera.py — construye POR ANCLAS los carros del bloque eco_ing_a_carrera: el GENOMA que la seleccion produjo en
ECO_SEL_ING (hijos INGENUOS; brazo ING_SEL_C, FUNCIONA en la serie 46101-46120) puesto en el bicho de la carrera.

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros.

ORIGEN (solo se LEE; sha fijado): el MISMO de eco_a_carrera. Se IMPORTA eco_a_carrera/construye_eco_a_carrera.py (sha 403c747caaae1c1e,
verificado) y se llama a su construye(nombre, RES0, FUENTE), que parte de frio_carrera/carros/V143_RES0.py (sha fab1d8068fe901a5) con sus
4 anclas (cada una exactamente una vez). Aqui se agrega UNA sola ancla mas: la primera linea del docstring (el nombre del bloque). El
codigo de los carros es el de eco_a_carrera byte a byte salvo esa linea, el nombre y la linea de perillas (se verifica).

LA BASE (decidida y justificada ANTES de correr; ver docstring del runner):
  RES0 1 = V143_RES0 (F1 en la carrera: el nacido lee el nodo del linaje SIN neutras) = la traduccion de FAMB_RES0_ECO (con familia).
  RES0 0 = V143 (el nacido lee el nodo con neutras, como FABRICA de la carrera) = la traduccion de FABRICA_ECO (sin la tabla de F1),
           que es el carro con que ECO_SEL_ING selecciono. Con el genoma G0 es V143 bit a bit salvo telemetria (arnes).
Genera en eco_ing_a_carrera/carros/:
  EIC_G0    RES0 1, 'G0'         base con familia (== EAC_G0 de eco_a_carrera)
  EIC_ING   RES0 1, 'ING_SEL_C'  el genoma ingenuo-seleccionado sobre la base con familia (secundaria)
  EIC_AZA   RES0 1, 'ING_AZA_C'  su control sin herencia (secundaria)
  EIC_SELC  RES0 1, 'SEL_C'      REFERENCIA: el genoma de ECO_SEL que fallo en eco_a_carrera (mismo carro que EAC_SEL)
  EIC_G0V   RES0 0, 'G0'         base sin familia con G0 por el camino nuevo (solo para la identidad larga contra V143)
  EIC_INGV  RES0 0, 'ING_SEL_C'  PRIMARIA: el genoma ingenuo-seleccionado sobre V143
  EIC_AZAV  RES0 0, 'ING_AZA_C'  PRIMARIA, control

    python experimentos/organelos/eco_ing_a_carrera/construye_eco_ing_a_carrera.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EAC = os.path.join(os.path.dirname(AQUI), 'eco_a_carrera')
SALIDA = os.path.join(AQUI, 'carros')
SHA_CE = '403c747caaae1c1e'
NL = '\r\n'
VARIANTES = [('EIC_G0', 1, 'G0'), ('EIC_ING', 1, 'ING_SEL_C'), ('EIC_AZA', 1, 'ING_AZA_C'), ('EIC_SELC', 1, 'SEL_C'),
             ('EIC_G0V', 0, 'G0'), ('EIC_INGV', 0, 'ING_SEL_C'), ('EIC_AZAV', 0, 'ING_AZA_C')]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def ce():
    p = os.path.join(EAC, 'construye_eco_a_carrera.py')
    if h16(p) != SHA_CE: raise SystemExit(f"construye_eco_a_carrera.py sha {h16(p)} != {SHA_CE}")
    if EAC not in sys.path: sys.path.insert(0, EAC)
    import construye_eco_a_carrera as CE
    return CE


def construye(nombre, r, f):
    CE = ce()
    txt = CE.construye(nombre, r, f).decode('utf-8')
    a = f'"""{nombre}.py — eco_a_carrera: el genoma de ECO_SEL (15 genes del cerebro) sobre la base de frio_carrera.' + NL
    n = txt.count(a)
    if n != 1: raise SystemExit(f"ancla de cabecera aparece {n} veces (se exige 1)")
    txt = txt.replace(a, f'"""{nombre}.py — eco_ing_a_carrera: el genoma de ECO_SEL_ING o ECO_SEL (15 genes del cerebro); FUENTE {f!r}, '
                         f'RES0 {r}. Codigo = el de eco_a_carrera (construye_eco_ing_a_carrera.py sobre construye_eco_a_carrera.py {SHA_CE}).' + NL)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, r, f) for n, r, f in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    CE = ce()
    outs = todas()
    for n, r, f in VARIANTES:   # difiere del carro de eco_a_carrera con el mismo RES0 solo en cabecera, nombre y perillas
        ref = CE.construye('EAC_G0', r, 'G0').decode('utf-8').split(NL); ls = outs[n].decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(ref, ls)) if x != y]
        if len(ls) != len(ref) or any(not (i == 0 or 'FUENTE = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere del carro de eco_a_carrera en algo mas que cabecera/perillas/nombre: lineas {dif[:6]}")
    ok = True
    os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            with open(ruta, 'wb') as fh: fh.write(bts)
            print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"construye_eco_a_carrera.py sha {h16(os.path.join(EAC, 'construye_eco_a_carrera.py'))} (fijado {SHA_CE}) · "
          f"construye_eco_ing_a_carrera.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
