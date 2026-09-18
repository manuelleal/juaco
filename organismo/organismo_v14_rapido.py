"""
Organismo v14 RAPIDO — gemelo COMPILADO (numba) del TRONCO v14, es decir de organismo_v14c_on.py
(= organismo_v14c.py con las DOS perillas ENCENDIDAS por defecto: mask_rel=2 con del_s=del_c=0.25 y
ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1). Decision del director: v14 = v13 + hija dispersa +
puerta por codigo. Arnes: identidad_v14_rapido.py.

NO contiene ninguna regla propia: DELEGA en organismo_v14c_rapido.run (sha en el arnes), que ya es bit a bit
identico a organismo_v14c en 196/196 corridas (identidad_v14c_rapido.py). La unica diferencia con el gemelo
de la composicion son los VALORES POR DEFECTO de la firma, exactamente los de organismo_v14c_on.py, igual que
organismo_v14c_on.py es organismo_v14c.py con esas mismas constantes cambiadas.

Por que delegar y no copiar el bucle:
  - IDENTIDAD: no hay dos copias del kernel que puedan divergir; el codigo compilado es literalmente el mismo.
  - MISMA CACHE NUMBA: se reutiliza la cache de organismo_v14c_rapido (__pycache__/*.nbi/*.nbc de ese modulo);
    una copia del archivo generaria un segundo juego de caches y una segunda compilacion de ~18s.
  - Las guardias heredadas (log_cada no compilado, puerta negativa explicita, nuevo_val invalido, nuevo antes
    de invertir) siguen valiendo tal cual, y los mensajes de error nombran al gemelo que de verdad corre.

Restriccion heredada: log_cada debe ser None. FUERA DE ALCANCE: el mundo de REGLA (organismo_v14gc.py) es otro
archivo con otra firma y otras claves; su gemelo no existe todavia y este modulo NO lo reemplaza.
"""
import os
import sys

try:
    import organismo_v14c_rapido as _G
except ImportError:                                    # el directorio propio no estaba en sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))   # al FINAL: no puede tapar a organismo/ (ERR-28)
    import organismo_v14c_rapido as _G

# el mismo mundo y las mismas constantes que organismo_v14c_on.py / organismo_v14c_rapido.py
L = _G.L; NK = _G.NK; NKMAX = _G.NKMAX; K = _G.K; NCODMAX = _G.NCODMAX
PAT = _G.PAT; R_VAL = _G.R_VAL; E_VAL = _G.E_VAL; NOMBRES = _G.NOMBRES; PATM = _G.PATM


def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.15,clip_s=10.0,puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1):
    """La firma de organismo_v14c_on.run, con SUS defaults. El cuerpo es el gemelo de la composicion."""
    return _G.run(seed,T=T,learn=learn,invertir_en=invertir_en,nuevo=nuevo,nuevo_en=nuevo_en,nuevo_val=nuevo_val,solap_B=solap_B,
                  eta=eta,tau_e=tau_e,alpha=alpha,hambre_boca=hambre_boca,aversion=aversion,costo=costo,nobj=nobj,log_cada=log_cada,
                  plast=plast,theta=theta,ema=ema,paso=paso,solap_AB=solap_AB,lam=lam,memoria_rechazo=memoria_rechazo,mu_norm=mu_norm,
                  div_signo=div_signo,eta_s=eta_s,clip_s=clip_s,puerta=puerta,mask_rel=mask_rel,del_s=del_s,del_c=del_c,ema_c=ema_c,
                  puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min)
