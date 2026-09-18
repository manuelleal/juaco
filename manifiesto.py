"""Regenera MANIFEST.txt con el sha256 corto (16 hex) de cada archivo del repo.

Regla 7 del proyecto: cada resultado se guarda con el hash del script que lo produjo.
MANIFEST.txt se lista a si mismo con el hash de la cadena vacia (no puede contenerse),
que es la convencion del manifiesto original.

Uso:  python manifiesto.py          -> regenera y verifica
      python manifiesto.py --check  -> solo verifica, no escribe
"""
import hashlib, os, sys

EXCLUIR_DIRS = {'.git', '__pycache__'}
CONGELADOS = {
    './organismo/organismo_v6.py':  '5f38f83cf49248a3',
    './organismo/bateria.py':       '1add9e6f85e97978',
    './organismo/organismo_v7c.py': '212f0746d52577c7',
    './organismo/bateria_v7c.py':   '21b97967e48ed971',
    # v8 = TRONCO desde el 16 sep 2026 (examen criterio v3 20/20, datos/examen_v8_20260916_145204.json)
    './organismo/organismo_v8.py':  'dca7d5c3a162f5d4',
    './organismo/bateria_v8.py':    '8de16b2e97de8312',
    # v9 = TRONCO desde el 16 sep 2026 (confirmatorio semillas 21-40 M0-M6 y examen criterio v3 20/20)
    './organismo/organismo_v9.py':  'd3b72fb8819fbe8e',
    './organismo/bateria_v9.py':    'c6496196990f6774',
    # v10: NO es tronco (ERR-17; replica V10b fallida el 17 sep). Se congela como INSTRUMENTO: la identidad de v11 lo usa.
    './organismo/organismo_v10.py': '219d5033fe15b5b9',
    './organismo/bateria_v10.py':   'd354813d3fa9d0f1',
    # v11 = TRONCO desde el 17 sep 2026. Primer organo del tronco NACIDO POR EVOLUCION GUIADA (JUACO-EVO gen1/llm_2).
    # Confirmatorio semillas 41-60 (R1-R4, K1-K3) y examen criterio v3 20/20 en 41-60.
    './organismo/organismo_v11.py': 'f69e24063be1b194',
    './organismo/bateria_v11.py':   '17179642ad02269c',
    # v13 = TRONCO desde el 17 sep 2026 (tarde). DOS VIAS: v11 (rapida, hallada por evolucion) + lectura lineal de la
    # retina (lenta) con puerta de familiaridad. Examen criterio v3' 8/8 y bateria_generaliza en semillas 101-120.
    './organismo/organismo_v13.py': 'cc8b16b492d4d324',
    './organismo/bateria_v13.py':   '1a027bcb37eb536e',
    # v14 = TRONCO desde el 18 sep 2026 (madrugada). v13 + HIJA DISPERSA por relevancia (nivel 7: compone a k=4/5 con la mitad
    # de celdas) + PUERTA por evidencia del codigo exacto (nivel 4: capacidad de v11 sin perder la generalizacion de v13).
    # Examen v3' 8/8 en 121-140, 141-160 y 161-180; generalizacion 1.000/0.94-0.95 x3; identidad 30/30; gemelo 196/196.
    './organismo/organismo_v14.py': '9bab8ac0685b1f21',
    './organismo/bateria_v14.py':   '72216f5415de0c86',
}

def h16(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]

def recorrer():
    vacio = hashlib.sha256(b'').hexdigest()[:16]
    lineas = []
    for raiz, dirs, archivos in os.walk('.'):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUIR_DIRS)
        for a in sorted(archivos):
            ruta = os.path.join(raiz, a).replace(os.sep, '/')
            lineas.append(f"{vacio if a == 'MANIFEST.txt' else h16(ruta)} {ruta}")
    return lineas

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    solo_check = '--check' in sys.argv
    lineas = recorrer()
    if not solo_check:
        with open('MANIFEST.txt', 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lineas) + '\n')
        print(f'MANIFEST.txt regenerado: {len(lineas)} archivos')

    print('\n--- archivos congelados ---')
    roto = False
    for ruta, esperado in CONGELADOS.items():
        real = h16(ruta)
        ok = real == esperado
        roto |= not ok
        print(f"{'OK  ' if ok else 'ROTO'} {real} {ruta}")
    if roto:
        print('\n*** ALERTA: un archivo congelado cambio de hash. Detenerse y averiguar por que.')
        sys.exit(1)
    print(f'\nLos {len(CONGELADOS)} archivos congelados estan intactos.')
