"""Construye los instrumentos de la HIJA DISPERSA sobre el TRONCO (paso §6 del PREREGISTRO_hija_dispersa.md),
POR ANCLAS y sin tocar ningun original (organismo/organismo_v13.py y organismo/bateria_v13.py estan CONGELADOS:
solo se LEEN):

  organismo_v13D.py    <- organismo/organismo_v13.py                  (cc8b16b492d4d324)  tronco + perilla
  organismo_v13Don.py  <- organismo_v13D.py                           la misma, con la perilla ENCENDIDA por defecto
  organismo_v13gD.py   <- experimentos/v13_dos_vias/organismo_v13g.py (2a80e125f8593bf2)  mundo de regla (G1/G2/K)
  bateria_v13D.py      <- organismo/bateria_v13.py                    (1a027bcb37eb536e)  criterios v3' INTACTOS
  bateria_generaliza_D.py <- organismo/bateria_generaliza.py          (46772f5a582872c8)  G1/G2/K INTACTOS

PERILLA (apagada por defecto -> el original EXACTO, bit a bit):
  mask_rel = 2   HIJA DISPERSA POR RELEVANCIA. Al nacer, la hija es ciega fuera de los pixeles RELEVANTES de P en
                 vez de fuera de TODO P:
                   rel[i] <=> P[i]>0 Y ( |mp[i]-mn[i]| > del_s  O  min(mp[i],mn[i]) > 1-del_c )
                 con mp = mup[c]/zp[c] y mn = mun[c]/zn[c], medias de P CONDICIONADAS AL SIGNO DE R (EMA con
                 normalizador, ema_c). Dos ramas: contexto (presente en las dos clases) Y discriminador (lo que
                 separa las clases). Con mask_rel=0 la mascara es (P>0): v13 EXACTO.
  del_s, del_c = 0.25   fijados antes de correr (la separacion medida entre el rasgo causal y el irrelevante es de
                 un factor ~8, asi que cualquier umbral en [0.2, 0.9] da la misma mascara). NO se barren.
  ema_c = 0.05

MEMORIA QUE EXIGE: dos vectores de la dimension de la entrada y dos escalares POR CELDA (el doble de lo que ya
cuesta mu). Todo local: la celda ve su propia entrada P y el refuerzo R que ya recibe.

NOTA declarada ANTES de correr: en el mundo del tronco la retina tiene 6 pixeles y un solo objeto, asi que NO hay
nada irrelevante que ignorar; se espera que la mascara sea INERTE o casi (como lo fue a k=1 en 3T-k, donde salio
identica bit a bit). Este bloque es por tanto una prueba de NO REGRESION, no una demostracion del organo.

Uso:  python experimentos/nivel7_hija_dispersa/construye_v13D.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


def pon_hija(s, ancla_firma, nueva_firma, ancla_estado, dim, ancla_traza, ancla_kj, etiqueta):
    s = sust(s, ancla_firma, nueva_firma, etiqueta=f'{etiqueta}: firma')
    s = sust(s, ancla_estado, ancla_estado +
             f"    mup=np.zeros((NKMAX,{dim})); mun=np.zeros((NKMAX,{dim})); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador\n",
             etiqueta=f'{etiqueta}: estado')
    s = sust(s, ancla_traza, ancla_traza +
             "\n                        if R>0: mup[idx]=(1-ema_c)*mup[idx]+ema_c*P; zp[idx]=(1-ema_c)*zp[idx]+ema_c   # D\n"
             "                        elif R<0: mun[idx]=(1-ema_c)*mun[idx]+ema_c*P; zn[idx]=(1-ema_c)*zn[idx]+ema_c   # D",
             etiqueta=f'{etiqueta}: medias condicionadas')
    s = sust(s, ancla_kj,
             "                                if mask_rel==2 and zp[c]>1e-6 and zn[c]>1e-6:   # D: HIJA DISPERSA (contexto O discriminador)\n"
             "                                    _mp=mup[c]/float(zp[c]); _mn=mun[c]/float(zn[c])\n"
             "                                    _rel=(P>0)&((np.abs(_mp-_mn)>del_s)|(np.minimum(_mp,_mn)>1.0-del_c))\n"
             "                                else: _rel=(P>0)\n"
             "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*_rel\n",
             etiqueta=f'{etiqueta}: mascara')
    s = sust(s, "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n",
             "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n"
             "                                    mup[j]=mup[c].copy(); mun[j]=mun[c].copy(); zp[j]=zp[c]; zn[j]=zn[c]   # D: la hija hereda las medias condicionadas\n",
             etiqueta=f'{etiqueta}: herencia')
    return s


if __name__ == '__main__':
    salidas = []
    KJ = "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)\n"
    NUEVA_FIRMA = ",mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05):"

    # ---- 1) organismo_v13D: el tronco con la perilla ----
    s = origen(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'), 'cc8b16b492d4d324')
    s = pon_hija(s, "eta_s=0.015,clip_s=3.0,puerta=3):", "eta_s=0.015,clip_s=3.0,puerta=3" + NUEVA_FIRMA,
                 "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n", 6,
                 "                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P",
                 KJ, 'v13D')
    cab = ('"""organismo_v13D = organismo/organismo_v13.py (cc8b16b492d4d324, CONGELADO: solo se leyo) + HIJA DISPERSA\n'
           'POR RELEVANCIA (perilla mask_rel; medias de P condicionadas al signo de R). Generado por construye_v13D.py.\n'
           'NO editar a mano. Con mask_rel=0 es organismo_v13 EXACTO (arnes: identidad_v13D.py)."""\n')
    d = os.path.join(AQUI, 'organismo_v13D.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 2) organismo_v13Don: la misma, con la perilla ENCENDIDA por defecto (para bateria_v13D) ----
    s2 = sust(origen(d, h16(d)), "puerta=3,mask_rel=0,", "puerta=3,mask_rel=2,", etiqueta='v13Don: perilla encendida')
    d2 = os.path.join(AQUI, 'organismo_v13Don.py')
    open(d2, 'w', encoding='utf-8', newline='\n').write(
        '"""organismo_v13Don = organismo_v13D.py con mask_rel = 2 POR DEFECTO (hija dispersa ENCENDIDA). El mismo\n'
        'archivo con UNA constante cambiada, para que bateria_v13D.py lo examine sin tocar la bateria congelada.\n'
        'Generado por construye_v13D.py. NO editar."""\n' + s2)
    salidas.append(d2)

    # ---- 3) organismo_v13gD: el mundo de regla (lo que usa bateria_generaliza) ----
    s = origen(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'), '2a80e125f8593bf2')
    s = pon_hija(s, "sonda_final=False):", "sonda_final=False" + NUEVA_FIRMA,
                 "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n", 6,
                 "                        P=P_[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P",
                 KJ, 'v13gD')
    cab = ('"""organismo_v13gD = experimentos/v13_dos_vias/organismo_v13g.py (2a80e125f8593bf2) + HIJA DISPERSA POR\n'
           'RELEVANCIA (mask_rel). Es el instrumento del MUNDO DE REGLA que usa bateria_generaliza_D.py.\n'
           'Generado por construye_v13D.py. NO editar. Con mask_rel=0 es organismo_v13g EXACTO."""\n')
    d = os.path.join(AQUI, 'organismo_v13gD.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 4) bateria_v13D: la bateria del tronco (CONGELADA: solo se LEE) apuntando a organismo_v13Don ----
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_v13.py'), '1a027bcb37eb536e')
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n"
                "sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n",
             "_D = os.path.dirname(os.path.abspath(__file__))   # esta copia vive fuera de organismo/\n"
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(_D)), 'organismo')\n"
             "RAIZ = os.path.dirname(AQUI)\n"
             "sys.path[:0] = [_D, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n", etiqueta='bateria_v13D: rutas')
    s = sust(s, "    import organismo_v13 as v13\n", "    import organismo_v13Don as v13   # hija dispersa ENCENDIDA\n",
             n=2, etiqueta='bateria_v13D: import')
    s = s.replace("h16(os.path.join(AQUI, 'organismo_v13.py'))", "h16(os.path.join(_D, 'organismo_v13Don.py'))")
    s = s.replace("f'examen_v13_{stamp}", "f'examen_v13D_{stamp}")
    cab = ('"""bateria_v13D = organismo/bateria_v13.py (1a027bcb37eb536e, CONGELADO: solo se leyo) apuntando a\n'
           'organismo_v13Don (v13 + hija dispersa por relevancia) en vez de organismo_v13. Las SEIS etapas, los CRIT\n'
           'importados y los umbrales del criterio v3\' quedan INTACTOS. Salida en datos/examen_v13D_<fecha>.\n'
           'Generado por construye_v13D.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_v13D.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 5) bateria_generaliza_D: la bateria de generalizacion con UNA entrada mas en INSTRUMENTOS ----
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), '46772f5a582872c8')
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n",
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'organismo')   # esta copia vive fuera de organismo/\n"
             "RAIZ = os.path.dirname(AQUI)\n", etiqueta='bateria_generaliza_D: AQUI/RAIZ')
    s = sust(s, "REGLAS = ['px0', 'azar']\n",
             "REGLAS = ['px0', 'azar']\n_D = os.path.join(RAIZ, 'experimentos', 'nivel7_hija_dispersa')\n",
             etiqueta='bateria_generaliza_D: _D')
    s = sust(s, "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n",
             "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n"
             "    'organismo_v13D': ('organismo_v13gD', dict(eta_s=0.015, puerta=3)),   # D: perilla APAGADA -> debe dar lo mismo que organismo_v13\n"
             "    'organismo_v13D_on': ('organismo_v13gD', dict(eta_s=0.015, puerta=3, mask_rel=2)),   # D: hija dispersa ENCENDIDA\n",
             etiqueta='bateria_generaliza_D: INSTRUMENTOS')
    s = sust(s, "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n",
             "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n"
             "sys.path.insert(0, _D)   # D: organismo_v13gD\n", etiqueta='bateria_generaliza_D: sys.path')
    s = sust(s, "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n",
             "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n"
             "            'organismo_v13gD': _D,\n", etiqueta='bateria_generaliza_D: _dir')
    s = s.replace("h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))",
                  "h16(os.path.join(AQUI, 'organismo_v13.py') if modulo == 'organismo_v13_rapido' else (os.path.join(AQUI, modulo + '.py') if os.path.exists(os.path.join(AQUI, modulo + '.py')) else os.path.join(_D, modulo.split('_on')[0] + '.py')))")
    s = s.replace("sha_organismo=h16(os.path.join(AQUI, modulo + '.py')),",
                  "sha_organismo=(h16(os.path.join(AQUI, modulo + '.py')) if os.path.exists(os.path.join(AQUI, modulo + '.py')) else h16(os.path.join(_D, modulo.split('_on')[0] + '.py'))),")
    cab = ('"""bateria_generaliza_D = organismo/bateria_generaliza.py (46772f5a582872c8) con dos entradas mas en\n'
           'INSTRUMENTOS (organismo_v13D y organismo_v13D_on, ambas sobre organismo_v13gD) y las rutas corregidas por\n'
           'vivir fuera de organismo/. Los UMBRALES y los criterios G1/G2/K NO se tocan.\n'
           'Generado por construye_v13D.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_generaliza_D.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    for d in salidas:
        print(f"  {os.path.relpath(d, RAIZ):55s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
