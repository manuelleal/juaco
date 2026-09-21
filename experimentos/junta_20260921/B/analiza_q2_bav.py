"""analiza_q2_bav.py -- DIAGNOSTICO del deficit de la fase 5 (creador B, junta del 21-sep-2026).

NO simula nada: lee SOLO el crudo ya registrado de la serie 961-980 (y la replica 981-1000 si existe).
Un proceso, sin Pool. Pregunta que contesta: con las puertas ABSOLUTAS de ERR-90, que le falta EXACTAMENTE
a `BA-v` para pasar P6 (dist(PAR) >= 15 y dist(PAR0) <= 5), y donde esta el cuello: en la DIRECCION
(resolucion del codigo) o en el VALOR leido (la regla de lectura).

Salida: tabla por semilla del brazo PAR, cruce de `lee_ref` = [valor, habla, exactas FORMA, exactas VARIANTE]
con `dist`, y el mismo cruce en BAR-H. Ademas: resolucion observada (`n_mismo_dos`, `herm_en_grupo`).
"""
import json, os, sys, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
DIR = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')

CRUDOS = ['serie_bav_s961-980_20260921_145002_crudo.json']
for p in sorted(glob.glob(os.path.join(DIR, 'serie_bav_s981-1000_*_crudo.json'))):
    CRUDOS.append(os.path.basename(p))


def med(v):
    v = sorted(v)
    n = len(v)
    if not n:
        return None
    return float(v[n // 2]) if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0


def carga(nom):
    with open(os.path.join(DIR, nom), 'r', encoding='utf-8') as f:
        return json.load(f)


def por_brazo(d, cel, base):
    return sorted([r for r in d['brazos'] if r['cel'] == cel and r['base'] == base], key=lambda r: r['seed'])


def main():
    for nom in CRUDOS:
        if not os.path.exists(os.path.join(DIR, nom)):
            print('(falta %s -- la replica no ha terminado)' % nom)
            continue
        d = carga(nom)
        print('=' * 118)
        print('CRUDO %s   celdas %s' % (nom, d['meta'].get('celdas', {}).keys() if isinstance(d['meta'].get('celdas'), dict) else '?'))
        print('=' * 118)

        # ---------- 1. PAR: por que cae P6 en BA-v, semilla a semilla
        for cel in ('b5k3', 'b6suf', 'A1', 'BA-v'):
            rs = por_brazo(d, cel, 'PAR')
            if not rs:
                continue
            dist = [r['B4']['dist'] for r in rs if r['B4']['dist'] is not None]
            print('\n[%s] PAR  dist = %d/%d' % (cel, int(sum(dist)), len(dist)))
            print('  %-6s %-5s %-7s %-7s %-26s %-8s %-8s %-7s' %
                  ('seed', 'dist', 'comRef', 'comHerm', 'lee_ref [v,habla,eF,eV]', 'n_dos', 'hermG', 'fam1'))
            for r in rs:
                B = r['B4']
                print('  %-6d %-5s %-7s %-7s %-26s %-8s %-8s %-7s' % (
                    r['seed'], B['dist'], (1 - int(B['evX'])) if B['evX'] is not None else '-',
                    int(B['comH']) if B['comH'] is not None else '-',
                    str(r['lee_ref']), str(r['n_mismo_dos']), str(r['herm_en_grupo']), B.get('fam1')))

        # ---------- 2. El cruce que decide: lee_ref del referente contra la conducta
        print('\n--- CRUCE lee_ref (referente, paso de la entrega) x conducta, TODOS los brazos ---')
        print('  %-9s %-8s %-6s %-6s %-6s %-6s %-6s' % ('celda', 'brazo', 'n', 'eV=0', 'eV=3', 'com', 'com|eV=0'))
        for cel in ('A1', 'BA-v', 'BA-v-sh'):
            for base in ('CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR', 'PAR', 'PAR0'):
                rs = [r for r in por_brazo(d, cel, base) if r['lee_ref'] is not None and r['B4']['evX'] is not None]
                if not rs:
                    continue
                ev0 = [r for r in rs if r['lee_ref'][3] == 0]
                ev3 = [r for r in rs if r['lee_ref'][3] == len(r['gan_var'] or [1, 2, 3])]
                com = sum(1 for r in rs if r['B4']['evX'] == 0.0)
                c0 = sum(1 for r in ev0 if r['B4']['evX'] == 0.0)
                print('  %-9s %-8s %-6d %-6d %-6d %-6d %-6s' % (cel, base, len(rs), len(ev0), len(ev3), com,
                                                                '%d/%d' % (c0, len(ev0))))

        # ---------- 3. Reparto de exactas de VARIANTE en el brazo que decide
        print('\n--- Reparto de "exactas de VARIANTE" del REFERENTE (lee_ref[3]) por celda y brazo ---')
        for cel in ('A1', 'BA-v'):
            for base in ('CANAL', 'PAR', 'BAR-H', 'BAR-T'):
                rs = [r for r in por_brazo(d, cel, base) if r['lee_ref'] is not None]
                if not rs:
                    continue
                h = {}
                for r in rs:
                    h[r['lee_ref'][3]] = h.get(r['lee_ref'][3], 0) + 1
                hab = sum(1 for r in rs if r['lee_ref'][1])
                val = med([r['lee_ref'][0] for r in rs])
                print('  %-9s %-8s eV=%s  habla %d/%d  mediana valor %s' % (cel, base, h, hab, len(rs), val))

        # ---------- 4. Resolucion estructural observada (la DIRECCION, no el valor)
        print('\n--- RESOLUCION: cuantos de los 32 estimulos comparten TODAS las direcciones (n_mismo_dos) ---')
        for cel in ('b5k3', 'b6suf', 'A1', 'BA-v'):
            rs = [r for r in por_brazo(d, cel, 'CANAL')]
            nd = [r['n_mismo_dos'] for r in rs if r['n_mismo_dos'] is not None]
            nk = [r['n_mismo_dir_k'] for r in rs if r['n_mismo_dir_k'] is not None]
            hg = [r['herm_en_grupo'] for r in rs if r['herm_en_grupo'] is not None]
            print('  %-9s n_mismo_dos mediana %s (min %s max %s, n %d) | n_mismo_dir_k mediana %s | hermana dentro del grupo %s/%d'
                  % (cel, med(nd), (min(nd) if nd else '-'), (max(nd) if nd else '-'), len(nd),
                     med(nk), (int(sum(hg)) if hg else '-'), len(hg)))

        # ---------- 5. Abstencion (cuantas veces la tabla NO habla) y coste
        print('\n--- ABSTENCION de la tabla y coste ---')
        for cel in ('b5k3', 'b6suf', 'A1', 'BA-v', 'BA-v-sh'):
            rs = por_brazo(d, cel, 'CANAL')
            if not rs:
                continue
            ab = [r['abstiene'] for r in rs if r['abstiene'] is not None]
            co = [r['cobertura'] for r in rs if r['cobertura'] is not None]
            print('  %-9s abstiene(32 estimulos) mediana %s (rango %s-%s) | cobertura mediana %s | muertes mediana %s'
                  % (cel, med(ab), (min(ab) if ab else '-'), (max(ab) if ab else '-'), med(co),
                     med([r['deaths'] for r in rs])))


if __name__ == '__main__':
    main()
