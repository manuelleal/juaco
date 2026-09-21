"""
organismo_f9c RAPIDO — gemelo COMPILADO (numba) de experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py
(9dd1fb91ecec35ae del 21-sep 17:20; generado por construye_f9c.py DESDE organismo_f9.py 3a821884394d66c9 con las inserciones
de organismo_f9b.py 6a57e9fa9514099b; aqui solo se LEYO). Arnes: identidad_f9c_rapido.py.

NO contiene ninguna regla propia: DELEGA en experimentos/nivel09_cuerpo_nuevo/organismo_f9_rapido.run, que ya
es bit a bit identico a organismo_f9 en 138/138 corridas (identidad_f9_rapido.py) y lleva las cuatro perillas
del bloque 2 (nodo_via, nodo_or, sesgo_fijo, f9c) escritas EN EL MISMO bucle, apagadas por defecto. La unica
diferencia con el gemelo del bloque 1 son los VALORES POR DEFECTO de la firma, exactamente igual que
organismo_f9c.py es organismo_f9.py con esas cuatro perillas anadidas.

Por que delegar y no copiar el bucle (la razon de organismo_v14_rapido.py, que hace lo mismo con v14c):
  - IDENTIDAD: no hay dos copias del kernel que puedan divergir; el codigo compilado es literalmente el mismo.
  - MISMA CACHE NUMBA: se reutiliza la cache de organismo_f9_rapido (__pycache__/*.nbi/*.nbc de esa carpeta);
    una copia del archivo generaria un segundo juego de caches y una segunda compilacion de ~50 s.
  - las guardias heredadas (lo que el gemelo NO compila: log_cada, nec_shuf, predictor, tercera necesidad,
    hereda M1+pares/baraja, invertir/nuevo con vivo=1) siguen valiendo tal cual.

Restricciones heredadas: las mismas del gemelo del bloque 1. Un proceso a la vez (el alma es un invocable de
Python que se llama por objmode y el contexto es de modulo).
"""
import os
import sys

try:
    import organismo_f9_rapido as _G
except ImportError:                                    # la carpeta del bloque 1 no estaba en sys.path
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 'nivel09_cuerpo_nuevo'))   # al FINAL: no puede tapar a organismo/ (ERR-28)
    import organismo_f9_rapido as _G

L = _G.L; NK = _G.NK; NKMAX = _G.NKMAX; K = _G.K; NCODMAX = _G.NCODMAX
PAT = _G.PAT; R_VAL = _G.R_VAL; E_VAL = _G.E_VAL; NEC = _G.NEC; VAL_VIVO = _G.VAL_VIVO; EFECTO = _G.EFECTO
NOMBRES = _G.NOMBRES; PATM = _G.PATM


def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.15,clip_s=10.0,puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1,vivo=0,n_nec=1,estims=None,costo_a=0.002,A_ini=1.0,val_esc=0,nec_shuf=0,hereda_nec=1,tabla=None,eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,crit_exp=0.5,reproduccion=0,rep_mide=1,rep_X=500,rep_umbral=1.0,rep_coste=0.0,rep_nec=0,rep_cuello=0,rep2=0,rep2_regalo=600,muerte_real=0,hereda='nada',dote=0.6,cola_max=200,h1=0,alma=None,alma_muertes=0,nodo=1,conectado=0,nodo_k=20,nodo_lee=50,miedo_n=5,miedo_R=-3.0,d_dote=0.1,d_umbral=0.1,menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0,nodo_via=0,nodo_or=0,sesgo_fijo=0.0,f9c=0):
    """La firma de organismo_f9c.run. El cuerpo es el gemelo del bloque 1 con las cuatro perillas del 2."""
    return _G.run(seed,T=T,learn=learn,invertir_en=invertir_en,nuevo=nuevo,nuevo_en=nuevo_en,nuevo_val=nuevo_val,
                  solap_B=solap_B,eta=eta,tau_e=tau_e,alpha=alpha,hambre_boca=hambre_boca,aversion=aversion,
                  costo=costo,nobj=nobj,log_cada=log_cada,plast=plast,theta=theta,ema=ema,paso=paso,solap_AB=solap_AB,
                  lam=lam,memoria_rechazo=memoria_rechazo,mu_norm=mu_norm,div_signo=div_signo,eta_s=eta_s,
                  clip_s=clip_s,puerta=puerta,mask_rel=mask_rel,del_s=del_s,del_c=del_c,ema_c=ema_c,
                  puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,vivo=vivo,n_nec=n_nec,estims=estims,
                  costo_a=costo_a,A_ini=A_ini,val_esc=val_esc,nec_shuf=nec_shuf,hereda_nec=hereda_nec,tabla=tabla,
                  eta_pred=eta_pred,ema_pred=ema_pred,clip_e=clip_e,k_sorp=k_sorp,crit_exp=crit_exp,
                  reproduccion=reproduccion,rep_mide=rep_mide,rep_X=rep_X,rep_umbral=rep_umbral,rep_coste=rep_coste,
                  rep_nec=rep_nec,rep_cuello=rep_cuello,rep2=rep2,rep2_regalo=rep2_regalo,muerte_real=muerte_real,
                  hereda=hereda,dote=dote,cola_max=cola_max,h1=h1,alma=alma,alma_muertes=alma_muertes,nodo=nodo,
                  conectado=conectado,nodo_k=nodo_k,nodo_lee=nodo_lee,miedo_n=miedo_n,miedo_R=miedo_R,d_dote=d_dote,
                  d_umbral=d_umbral,menu=menu,nodo_baraja=nodo_baraja,nodo_rel=nodo_rel,con_desde=con_desde,
                  rep_acum=rep_acum,f9=f9,nodo_via=nodo_via,nodo_or=nodo_or,sesgo_fijo=sesgo_fijo,f9c=f9c)
