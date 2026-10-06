"""calibracion de la compuerta theta (colonia/cuarentena) y lambda (kNN) en la SEMILLA 0, que no entra en la serie. Declarado."""
import json, time, numpy as np, mini_llm as m, os
os.chdir(m.AQUI); voc = m.Voc(); corpus = m.carga_corpus(); model, meta = m.entrena_base(voc, corpus)
out = []; t0 = time.time()
for theta in (0.97, 0.98, 0.99):
    r, _ = m.corre(0, model, voc, corpus, ['colonia', 'cuarentena'], 200, theta, 0.3, log=lambda *a: None)
    for b in ('colonia', 'cuarentena'):
        x = r['brazos'][b]
        out.append(dict(b=b, theta=theta, hechos1=x['hechos']['hechos1']['acc'], hechos3=x['hechos']['hechos3']['acc'], inv1=x['seg']['inv1']['nll'],
                        esp=x['sonda']['inv2']['espanol'][1], nll_tot=float(np.mean([x['seg'][s]['nll'] for s in x['seg']]))))
        print(out[-1], f'[{time.time()-t0:.0f}s]', flush=True)
for lam in (0.2, 0.4):
    r, _ = m.corre(0, model, voc, corpus, ['knn'], 200, 0.98, lam, log=lambda *a: None); x = r['brazos']['knn']
    out.append(dict(b='knn', lam=lam, hechos1=x['hechos']['hechos1']['acc'], hechos3=x['hechos']['hechos3']['acc'], inv1=x['seg']['inv1']['nll'],
                    esp=x['sonda']['inv2']['espanol'][1], nll_tot=float(np.mean([x['seg'][s]['nll'] for s in x['seg']]))))
    print(out[-1], f'[{time.time()-t0:.0f}s]', flush=True)
json.dump(out, open('datos/calibracion.json', 'w'), indent=1)
