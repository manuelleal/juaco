"""Genera mundo_largo_c.py = mundo_largo.py (9f74ff6b5941e5a5) + curiosidad por progreso de error (err_l lenta, progreso
por patron, sesgo gamma_C con la retina vacia) + control de prioridad barajada. Con gamma_C=0 es mundo_largo EXACTO
(identidad obligatoria). Anclas con conteo exacto.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py')
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    (["        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None):   # mapa + largo"],
     ["        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None,",
      "        gamma_C=0.0,ema_l=0.005,cur_barajada=False):   # mapa + largo + curiosidad"], 1, 'firma'),
    (["    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)"],
     ["    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)",
      "    err_l=np.zeros(NKMAX)   # curiosidad: EMA lenta del error por celda; progreso = err_l - err",
      "    _perm_c=np.random.default_rng(seed+800000).permutation(NKMAX) if cur_barajada else None   # control: prioridad barajada (RNG propio)",
      "    def _prog(P):   # curiosidad: progreso medio de las 3 celdas del codigo del patron",
      "        _pc=(err_l-err) if _perm_c is None else (err_l-err)[_perm_c]",
      "        return float(_pc[kenyon(P)>0].mean())"], 1, 'estado curiosidad'),
    (["        return gamma_M*np.array([_bi,_bd])"],
     ["        if gamma_C:   # curiosidad: sesgo hacia donde el error esta cayendo",
      "            _ci=sum(disc_M**h*_prog(_Mpat[(pos-h)%L]) for h in range(1,H_M+1) if _Mset[(pos-h)%L])",
      "            _cd=sum(disc_M**h*_prog(_Mpat[(pos+h)%L]) for h in range(1,H_M+1) if _Mset[(pos+h)%L])",
      "            return gamma_M*np.array([_bi,_bd])+gamma_C*np.array([_ci,_cd])",
      "        return gamma_M*np.array([_bi,_bd])"], 1, 'sesgo'),
    (["                        P=PAT_L[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P"],
     ["                        P=PAT_L[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P",
      "                        err_l[idx]=(1-ema_l)*err_l[idx]+ema_l*abs(dlt)   # curiosidad"], 1, 'err lenta'),
    (["mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))"],
     ["mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; err_l[c]=err_l[j]=0; splits+=1; split_t.append((t,kk))"], 1, 'division signo'),
    (["Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))"],
     ["Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; err_l[c]=err_l[j]=0; splits+=1; split_t.append((t,kk))"], 1, 'division error'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != '9f74ff6b5941e5a5':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != 9f74ff6b5941e5a5")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_largo_c = mundo_largo.py (9f74ff6b5941e5a5) + curiosidad por progreso de error (EMA lenta por celda, progreso del' + NL +
           'patron, sesgo gamma_C con la retina vacia) + control de prioridad barajada. Generado por construye_curiosidad.py. NO' + NL +
           'editar. Con gamma_C=0 es mundo_largo exacto (identidad obligatoria)."""' + NL)
    d = os.path.join(AQUI, 'mundo_largo_c.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
