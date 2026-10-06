"""lee datos/sellado.json (ya abierto) e imprime las tablas del informe. No recalcula nada."""
import json, os
A = os.path.dirname(os.path.abspath(__file__)); s = json.load(open(os.path.join(A, 'datos', 'sellado.json'), encoding='utf-8')); e = s['evaluacion']
print('tramo', s['tramo'], 'dias', e['dias'], 'errores', s['errores_dato'], 'relleno', s['relleno'])
print('brazo | anual c0 | anual base [IC95] | anual 2x | Sharpe | caida | meses+ | n_oper | cent/oper c0 / base / 2x | retardo1 anual | acierto signo | larga/corta/fuera')
for k, b in e['brazos'].items():
    m = b['costo_base']; i = m['ic_anual']['ic95']
    print('%s | %+.1f | %+.1f [%+.1f, %+.1f] | %+.1f | %+.2f | %.1f | %.2f | %d | %+.1f / %+.1f / %+.1f | %+.1f | %.3f | %.2f/%.2f/%.2f' % (
        k, 100 * b['costo0']['anual'], 100 * m['anual'], 100 * i[0], 100 * i[1], 100 * b['costo_doble']['anual'], m['sharpe'], 100 * m['caida_max'],
        m['meses_pos'], m['n_oper'], b['costo0']['centavos_por_oper'], m['centavos_por_oper'], b['costo_doble']['centavos_por_oper'],
        100 * b['retardo1_costo_base']['anual'], m['acierto_signo'], m['frac_larga'], m['frac_corta'], m['frac_fuera']))
    if 'frac_pisada' in b: print('    pisa %.4f  acierto_clase_al_pisar %s  base_falla_al_pisar %s  base_falla_global %.3f' % (
        b['frac_pisada'], b['acierto_clase_al_pisar'], b['base_falla_al_pisar'], b['base_falla_global']))
print()
for k, c in e['comparaciones'].items():
    f = lambda y: '%+.2f IC95 [%+.2f, %+.2f]' % (100 * y['est'], 100 * y['ic95'][0], 100 * y['ic95'][1]) + (' IC99.375 [%+.2f, %+.2f]' % (100 * y['ic99.375'][0], 100 * y['ic99.375'][1]) if 'ic99.375' in y else '')
    print(k, '| -mantener', f(c['menos_mantener']), ('| -azar ' + f(c['menos_azar']) + ' | azar media %+.2f p_azar %.3f' % (100 * c['azar_media_anual'], c['p_azar'])) if 'menos_azar' in c else '')
print(json.dumps(e['colonia']))
