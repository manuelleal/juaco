"""analiza_mm_estab.py — DESCRIPTIVO de la moneda del muro (30-sep-2026, creador; pedido por la auditoria; escrito ANTES de los datos de
la serie). NO entra en la letra. Solo lee JSON; no corre nada.

PREGUNTA: tasa de ESTABLECIMIENTO (0 fundadores tras t = 10 000) de los linajes de tipo A contra los de tipo B, agrupada sobre los 60
pasajes (30 por brazo). TIPO del linaje = clase de las listas del banco final que entraron por un parto (las ultimas min(partos, len)
del banco, que es FIFO): A si la fraccion de clase A es >= 0.90, B si es <= 0.10, 'mixto' en lo demas, 'sin_parto' si partos == 0.
En neutra_L "A" es A0 (w 0). AVISO: `partos` cuenta tambien los partos de cuerpos con lista vacia (que no entran al banco), asi que el
corte puede incluir alguna lista de la siembra; a tasas / 10 es raro.
Tambien: cuantos linajes de cada tipo hay contra lo esperado por la fraccion A que ENTRA al pasaje (la toma del fundador).

  python experimentos/organelos/condiciones/moneda_muro/analiza_mm_estab.py datos/explora_<fecha>
"""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_mm as R   # noqa: E402
M = R.M
ALTO = 0.90; BAJO = 0.10


def tipo(x, k):
    B = [r for r in (x['bq']['banco'].get(str(k)) or []) if r]; q = int(x['bq']['tel'][str(k)]['partos']) if str(k) in x['bq']['tel'] else 0
    if q == 0 or not B: return 'sin_parto'
    f = M.frac(B[-min(q, len(B)):])
    return 'A' if f >= ALTO else ('B' if f <= BAJO else 'mixto')


def analiza(carpeta, log=print):
    modo = 'humo' if os.path.basename(os.path.normpath(carpeta)).startswith('humo') else 'explora'
    m = R.MODOS[modo]; out = {}
    for b in m['brazos']:
        T = {t: dict(n=0, est=0, cruza=0) for t in ('A', 'B', 'mixto', 'sin_parto')}; npas = 0; esp_A = 0.0; falta = []
        for i in m['ind']:
            for p in range(m['npas']):
                fin = os.path.join(carpeta, f"pasaje_{b}_i{i}_p{p}.json")
                if not os.path.exists(fin): falta.append(os.path.basename(fin)); continue
                x = json.load(open(fin, encoding='utf-8'))
                if x.get('aborto'): falta.append(os.path.basename(fin) + ' (aborto)'); continue
                npas += 1; post = R.post10k(x); esp_A += 9 * x['frac_A_entra']
                for l in x['linajes']:
                    k = int(l['indice']); t = tipo(x, k); T[t]['n'] += 1; T[t]['est'] += int(post[k] == 0); T[t]['cruza'] += int(l['cruza_real'])
        for t in T.values():
            t['tasa_est'] = round(t['est'] / t['n'], 3) if t['n'] else None; t['tasa_cruza'] = round(t['cruza'] / t['n'], 3) if t['n'] else None
        nAB = T['A']['n'] + T['B']['n']
        out[b] = dict(pasajes=npas, faltan=falta, tipos=T, frac_linajes_A_entre_A_y_B=(round(T['A']['n'] / nAB, 3) if nAB else None),
                      frac_A_que_entra_media=(round(esp_A / (9 * npas), 3) if npas else None))
        log(f"  {b}: {npas} pasajes (faltan {len(falta)})")
        for k, t in T.items(): log(f"    tipo {k:9s}: linajes {t['n']:4d} · establecidos {t['est']:4d} ({t['tasa_est']}) · cruzan {t['cruza']:4d} ({t['tasa_cruza']})")
        log(f"    linajes A / (A + B) = {out[b]['frac_linajes_A_entre_A_y_B']} contra la fraccion A que entra (media) {out[b]['frac_A_que_entra_media']}")
    f = os.path.join(carpeta, 'estab_mm.json')
    json.dump(dict(descriptivo=True, entra_en_la_letra=False, umbrales=dict(A=ALTO, B=BAJO), brazos=out,
                   sha_script=R.h16(os.path.abspath(__file__))), open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  ESCRITO {f}")
    return out


if __name__ == '__main__':
    c = sys.argv[1]; c = c if os.path.isabs(c) else os.path.join(AQUI, c)
    print(f"DESCRIPTIVO establecimiento por tipo de linaje (no entra en la letra) · {c}")
    analiza(c)
