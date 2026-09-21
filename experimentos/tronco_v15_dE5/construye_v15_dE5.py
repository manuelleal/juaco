"""dE5 bajo el CRITERIO DE TRONCO v2 — CONSTRUCTOR POR ANCLAS del paquete (no corre nada).

MISION: llegar a la AGI por este camino. Este bloque juzga UN mecanismo: la SORPRESA DEL MUNDO (el error del
predictor de dE, el del bloque 6 de allostasis) entrando en la BOCA con ganancia k = 5 (dosis preregistrada en
experimentos/nivel9_probar_si_mismo/PREREGISTRO_dosis_dE.md, medida 0.267x y replicada 0.248x sobre v13).

QUE SE CONSTRUYE (los originales SOLO se leen; el sha se verifica antes de escribir nada):

  organismo_v15_dE5.py       <- experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py  (96feb4918dc5d694)
        cadena: organismo_vivo_rep (aa823d56c2d4213c) <- organismo_vivo (20c0961c79de8825) <- organismo/organismo_v14.py
        (feefc88b1fd8d434, v14.1 CONGELADO).  SE LE ANADE, por anclas:
          (1) B-5 `desambiguar` (el organo de v14.2), con el MISMO texto que experimentos/creacion_B/construye_codigo.py
              (COND_A->COND_B y FIS_VA->FIS_VB, copiados literalmente de ahi: es el codigo que paso identidad_codigo.py
              y las dos series de B-5). POR DEFECTO `desambiguar=1`, como el TRONCO v14.2.
          (2) `invertir_vivo_en` (T-C en el mundo vivo): en t se intercambian los EFECTOS de comida y veneno.
              Mismo texto que experimentos/creacion_A/construye_vivo_relevo.py. Inerte por defecto (None).
          (3) instrumentacion de RECUPERACION, de SOLO LECTURA (la capacidad nueva T-G): `t_ext_B` (primer paso tras
              `invertir_en` con valor(B) >= 0, el M1 del bloque 6), `mord_post` y `deaths_post`. Y `sbarE`, la lectura
              de la sorpresa. Ninguna consume rng.
        NO se anade NINGUN mecanismo de sorpresa: `organismo_vivo_rep2` YA TRAE el predictor de dE (perillas
        `eta_pred`, `ema_pred`, `clip_e`) y su entrada en la boca (`k_sorp`), vectorial por necesidad; con n_nec=1
        es, linea por linea, el dE-TEST de organismo_v13E_k5 (ver PREREGISTRO_dE5_v2.md, seccion 2).

  organismo_v15_dE5_on.py    <- el mismo con la DOSIS por defecto: eta_pred=0.03, ema_pred=0.05, k_sorp=5.0
                                (lo examinan las baterias, que no pasan kwargs).
  organismo_v15_dE5g.py      <- organismo/organismo_v142g.py (9e5f566cd6a7a4d2, instrumento de MUNDO DE REGLA del
                                tronco v14.2) + el MISMO predictor de dE, escrito con las MISMAS operaciones de numpy
                                que la version vectorial (Wpe (1,6), Wke (1,NKMAX), _sbE (1,)) para que el resultado
                                sea bit a bit el mismo. Sirve a bateria_generaliza (T-B).
  organismo_v15_dE5g_on.py   <- el mismo con la dosis por defecto.
  bateria_v15_dE5.py         <- organismo/bateria_v142.py (6375d90e531b06e6, CONGELADA) apuntando a
                                organismo_v15_dE5_on. Las SEIS etapas y los umbrales del criterio v3' INTACTOS.
  bateria_generaliza_v15_dE5.py <- organismo/bateria_generaliza_v142.py (e5929942647756a5, CONGELADA) con DOS entradas
                                nuevas en INSTRUMENTOS, con los kwargs CAMPO A CAMPO iguales a los de la entrada del
                                tronco organismo_v142 (regla 14 de EQUIPO.md) mas las cuatro perillas de la dosis
                                EXPLICITAS (ERR-38: "por defecto" no existe cuando el modulo es otro).

IDENTIDAD (arnes: identidad_v15_dE5.py): con la perilla APAGADA (eta_pred=0, k_sorp=0) y vivo=0, n_nec=1 el
organismo es organismo/organismo_v142.py BIT A BIT; con desambiguar=0 ademas es organismo_vivo_rep2 bit a bit.

Uso:  python experimentos/tronco_v15_dE5/construye_v15_dE5.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')

SHA = {   # tripwire: si un origen cambia, se aborta sin escribir nada
    os.path.join(NIV11, 'organismo_vivo_rep2.py'): '96feb4918dc5d694',
    os.path.join(ORG, 'organismo_v142g.py'): '9e5f566cd6a7a4d2',
    os.path.join(ORG, 'organismo_v142.py'): '17528d767fcebaf6',
    os.path.join(ORG, 'bateria_v142.py'): '6375d90e531b06e6',
    os.path.join(ORG, 'bateria_generaliza_v142.py'): 'e5929942647756a5',
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(ruta):
    s = h16(ruta)
    esperado = SHA.get(ruta)
    if esperado is not None and s != esperado:
        raise SystemExit(f'*** ORIGEN {ruta}: sha {s}, se esperaba {esperado}. No se escribe nada.')
    return open(ruta, 'rb').read().decode('utf-8'), s


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


def escribe(nombre, txt, cab):
    ruta = os.path.join(AQUI, nombre)
    open(ruta, 'w', encoding='utf-8', newline='\n').write(cab + txt)
    return h16(ruta)


# ---------------------------------------------------------------- B-5 (texto LITERAL de creacion_B/construye_codigo.py)
COND_A = "if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():"
COND_B = ("if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():"
          "   # B-5 DESAMBIGUAR: tambien divide cuando una celda consolidada, bajo una retina distinta (kj@P>KW[c]@P), recibe R==0")
FIS_VA = ("                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.\n"
          "                                    else:   Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n")
FIS_VB = ("                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.\n"
          "                                    elif R<0: Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n"
          "                                    else: Wp[_nm,j]=0.; Wn[_nm,j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor en la necesidad activa (las otras se heredan abajo) y la madre conserva el suyo\n")


# ---------------------------------------------------------------- (A) el organismo del mundo vivo + v14.2 + lecturas
def pon_vivo(src):
    # 1) firma: B-5 (defecto 1, como el TRONCO v14.2) + la inversion del mundo vivo
    out = sust(src, ",rep2=0,rep2_regalo=600):", ",rep2=0,rep2_regalo=600,desambiguar=1,invertir_vivo_en=None,sesgo_fijo=0.0):", etq='firma')
    # 2) estado: contadores de B-5 y las tres lecturas de recuperacion (solo lectura, no consumen rng)
    A = "    Wp=np.zeros((n_nec,NKMAX)); Wn=np.zeros((n_nec,NKMAX)); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)"
    out = sust(out, A, A.replace("splits=0;", "splits=0; _ndes=0; _des_t=[];") + "\n"
               "    t_ext_B=None; deaths_post=0; mord_post={}; _sgq=[0.]*4; _nsq=[0]*4   # dE: M1 del bloque 6 (recuperacion), bocados/muertes TRAS el cambio, y el SESGO DE LA BOCA por cuarto. SOLO LECTURA", etq='estado')
    # 3) B-5: la condicion y la fision (texto literal de construye_codigo.py)
    out = sust(out, COND_A, COND_B, etq='B-5 condicion')
    out = sust(out, FIS_VA, FIS_VB, etq='B-5 fision')
    # 4) T-C en el mundo vivo: los EFECTOS de comida y veneno se intercambian en t (texto de construye_vivo_relevo.py)
    A = "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}\n"
    out = sust(out, A, A + "        if invertir_vivo_en is not None and t==invertir_vivo_en: _EF=dict(_EF,comida=_EF['veneno'],veneno=_EF['comida'])   # T-C vivo: la comida pasa a quitar energia y el veneno a darla\n",
               etq='invertir_vivo')
    # 5) bocados tras el cambio no avisado (la capacidad nueva se mide con t_ext_B; esto es el diagnostico)
    A = "                mord[kk][q(t)]+=1\n"
    out = sust(out, A, A + "                if invertir_en is not None and t>=invertir_en: mord_post[val[kk]]=mord_post.get(val[kk],0)+1   # dE: bocados TRAS el cambio, por valencia NUEVA\n",
               etq='mord_post')
    # 6) recuperacion: primer paso tras la inversion con valor(B) >= 0 (M1 del bloque 6; no consume rng)
    A = "        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas\n"
    out = sust(out, A, "        if invertir_en is not None and t>=invertir_en and t_ext_B is None and valor(PAT['B'])>=0: t_ext_B=t   # dE: M1 del bloque 6 (recuperacion). No consume RNG\n" + A,
               etq='t_ext_B')
    # 7) muertes tras la inversion
    A = "            deaths+=1; _mnec[0 if E<=0 else 1]+=1; E=.6\n"
    out = sust(out, A, A + "            if invertir_en is not None and t>=invertir_en: deaths_post+=1   # dE\n", etq='deaths_post')
    # 7b) la boca: control de CANTIDAD (sesgo fijo, los brazos CONST de C-P1) y lectura del sesgo por cuarto
    A = "            if k_sorp: Vb+=k_sorp*float(_sbE[_na])   # VIVO: la SORPRESA DE LA NECESIDAD ACTIVA en la boca (la dosis de v15, ahora especifica)\n"
    out = sust(out, A, A +
               "            if sesgo_fijo: Vb+=sesgo_fijo   # CONTROL DE CANTIDAD (los brazos CONST de C-P1): el MISMO empujon medio, sin informacion\n"
               "            _sgq[q(t)]+=(k_sorp*float(_sbE[_na]) if k_sorp else 0.)+sesgo_fijo; _nsq[q(t)]+=1   # dE: sesgo de la boca por cuarto. SOLO LECTURA (mide si se apaga solo)\n",
               etq='boca vivo')
    # 8) return: las claves nuevas (todas de solo lectura)
    out = sust(out, "    return dict(sobre=sobre,",
               "    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,"
               "t_ext_B=t_ext_B,mord_post=dict(mord_post),deaths_post=deaths_post,"
               "sbarE=[round(float(_x),6) for _x in _sbE],invertir_vivo_en=invertir_vivo_en,sesgo_fijo=sesgo_fijo,"
               "sesgo_q=[(round(_sgq[_i]/_nsq[_i],6) if _nsq[_i] else 0.0) for _i in range(4)],enc_q=list(_nsq),sobre=sobre,", etq='return')
    return out


# ---------------------------------------------------------------- (B) el mundo de regla: el MISMO predictor de dE
PRED_G = (
    "                    if eta_pred:   # dE: predictor de la propia energia (bloque 6) con las MISMAS operaciones de numpy que la version vectorial de organismo_vivo (n_nec=1)\n"
    "                        _dp=Wpe@P_[kk]+Wke@kc; _ep=np.array([E_VAL[val[kk]]])-_dp\n"
    "                        Wpe=np.clip(Wpe+eta_pred*np.outer(_ep,P_[kk]),-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*np.outer(_ep,kc),-clip_e,clip_e)\n"
    "                        _sbE=(1.-ema_pred)*_sbE+ema_pred*np.abs(_ep)   # causal: la usa la boca del PROXIMO encuentro\n")


def pon_regla(src):
    out = sust(src, ",pat_shuf=0,pat_min=0,desambiguar=1):",
               ",pat_shuf=0,pat_min=0,desambiguar=1,eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,sesgo_fijo=0.0):", etq='g: firma')
    A = "    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; _ndes=0; _des_t=[]; el=np.zeros_like(Wl); tr=np.zeros(9)"
    out = sust(out, A, A + "\n    Wpe=np.zeros((1,6)); Wke=np.zeros((1,NKMAX)); _sbE=np.zeros(1); _sgq=[0.]*4; _nsq=[0]*4   # dE: predictor de dE, su EMA y el sesgo de la boca por cuarto (inerte con eta_pred=0). Mismas formas que organismo_vivo con n_nec=1",
               etq='g: estado')
    A = "            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n"
    out = sust(out, A,
               "            Vb=alpha*_wt+hambre_boca*hambre+.5\n"
               "            if k_sorp: Vb+=k_sorp*float(_sbE[0])   # dE: la SORPRESA DEL MUNDO en la boca, dosis k_sorp (misma linea que organismo_vivo)\n"
               "            if sesgo_fijo: Vb+=sesgo_fijo   # CONTROL DE CANTIDAD (los brazos CONST de C-P1)\n"
               "            _sgq[q(t)]+=(k_sorp*float(_sbE[0]) if k_sorp else 0.)+sesgo_fijo; _nsq[q(t)]+=1   # dE: sesgo de la boca por cuarto. SOLO LECTURA\n"
               "            pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n", etq='g: boca')
    A = "                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo\n"
    out = sust(out, A, PRED_G + A, etq='g: predictor')
    out = sust(out, "    return dict(desambiguar=desambiguar,",
               "    return dict(sbarE=[round(float(_x),6) for _x in _sbE],sesgo_fijo=sesgo_fijo,"
               "sesgo_q=[(round(_sgq[_i]/_nsq[_i],6) if _nsq[_i] else 0.0) for _i in range(4)],enc_q=list(_nsq),desambiguar=desambiguar,", etq='g: return')
    return out


SERIAL = ("""class _Serial:   # --sin-pool: HUMO de UN proceso que llega a ESCRIBIR el JSON (ERR-42) sin abrir ningun Pool.
    def imap_unordered(self, fn, it, chunksize=1): return map(fn, it)
    def __enter__(self): return self
    def __exit__(self, *a): return False


def _pool(mp):   # el camino por DEFECTO no cambia: sin --sin-pool es exactamente mp.Pool(N_PARALELO)
    return _Serial() if '--sin-pool' in sys.argv else mp.Pool(N_PARALELO)


""")


def pon_sin_pool(txt, etq):
    """Anade --sin-pool (humo de un proceso, ERR-42) y el tamano del Pool por JUACO_POOL (ERR-86).
    Sin la bandera, el codigo que corre es el mismo byte a byte."""
    out = sust(txt, "N_PARALELO = 14", "N_PARALELO = int(os.environ.get('JUACO_POOL', 14))   # ERR-86: el tamano del Pool se fija por JUACO_POOL", etq=f'{etq}: JUACO_POOL')
    out = sust(out, "    with mp.Pool(N_PARALELO) as pool:", "    with _pool(mp) as pool:", etq=f'{etq}: pool')
    out = sust(out, "if __name__ == '__main__':", SERIAL + "if __name__ == '__main__':", etq=f'{etq}: serial')
    out = sust(out, "Pool({N_PARALELO}) ===", "{'SIN POOL (--sin-pool)' if '--sin-pool' in sys.argv else f'Pool({N_PARALELO})'} ===", etq=f'{etq}: cabecera honesta')
    return out
if __name__ == '__main__':
    H = {}
    # --- (A) mundo vivo / mundo del examen ---
    src, s0 = origen(os.path.join(NIV11, 'organismo_vivo_rep2.py'))
    _, s_vivo = origen(os.path.join(NIV11, 'organismo_vivo.py'))
    _, s142 = origen(os.path.join(ORG, 'organismo_v142.py'))
    v = pon_vivo(src)
    cab = (f'"""organismo_v15_dE5 = experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py ({s0}; SOLO se leyo; cadena\n'
           f'organismo_vivo {s_vivo} <- organismo/organismo_v14.py feefc88b1fd8d434 = v14.1) + B-5 `desambiguar` (el organo\n'
           f'de v14.2, texto literal de creacion_B/construye_codigo.py, POR DEFECTO 1 como el TRONCO organismo_v142\n'
           f'{s142}) + `invertir_vivo_en` (T-C en el mundo vivo) + las lecturas de RECUPERACION t_ext_B / mord_post /\n'
           f'deaths_post / sbarE (SOLO LECTURA, no consumen rng).\n'
           f'LA PERILLA DEL CANDIDATO YA ESTABA AQUI: eta_pred / ema_pred / clip_e (predictor de dE del bloque 6) y k_sorp\n'
           f'(su sorpresa en la BOCA). dE5 = eta_pred=0.03, ema_pred=0.05, k_sorp=5.0. Con eta_pred=0 y k_sorp=0:\n'
           f'  vivo=0, n_nec=1, reproduccion=0, rep2=0  ->  organismo/organismo_v142.py BIT A BIT (claves de v14.2)\n'
           f'  desambiguar=0                            ->  organismo_vivo_rep2.py BIT A BIT (claves de rep2)\n'
           f'Arnes: identidad_v15_dE5.py. Generado por construye_v15_dE5.py. NO editar a mano."""\n')
    H['organismo_v15_dE5.py'] = escribe('organismo_v15_dE5.py', v, cab)
    von = sust(v, ",eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,crit_exp=0.5,",
               ",eta_pred=0.03,ema_pred=0.05,clip_e=3.0,k_sorp=5.0,crit_exp=0.5,", etq='on: dosis vivo')
    H['organismo_v15_dE5_on.py'] = escribe('organismo_v15_dE5_on.py', von,
        '"""organismo_v15_dE5_on = organismo_v15_dE5.py con la DOSIS PREREGISTRADA por defecto: eta_pred=0.03,\n'
        'ema_pred=0.05, k_sorp=5.0 (dE5). Lo examinan las baterias, que no pasan kwargs. Generado por\n'
        'construye_v15_dE5.py. NO editar."""\n')
    # --- (B) mundo de regla ---
    srcg, sg0 = origen(os.path.join(ORG, 'organismo_v142g.py'))
    g = pon_regla(srcg)
    H['organismo_v15_dE5g.py'] = escribe('organismo_v15_dE5g.py', g,
        f'"""organismo_v15_dE5g = organismo/organismo_v142g.py ({sg0}, instrumento de MUNDO DE REGLA del tronco v14.2;\n'
        f'SOLO se leyo) + el predictor de dE del bloque 6 y su sorpresa en la BOCA (k_sorp), escrito con las MISMAS\n'
        f'operaciones de numpy que organismo_vivo con n_nec=1 (Wpe (1,6), Wke (1,NKMAX), _sbE (1,)) para que las dos\n'
        f'implementaciones coincidan BIT A BIT. Con eta_pred=0 y k_sorp=0 es organismo_v142g EXACTO.\n'
        f'AVISO (regla 14): sus defectos de via lenta son eta_s=0.0, clip_s=3.0, puerta=None, mask_rel=0, puerta_pat=0;\n'
        f'la entrada de INSTRUMENTOS los pasa EXPLICITOS, campo a campo como la del tronco organismo_v142.\n'
        f'Generado por construye_v15_dE5.py. NO editar."""\n')
    gon = sust(g, ",eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,sesgo_fijo=0.0):", ",eta_pred=0.03,ema_pred=0.05,clip_e=3.0,k_sorp=5.0,sesgo_fijo=0.0):", etq='on: dosis regla')
    H['organismo_v15_dE5g_on.py'] = escribe('organismo_v15_dE5g_on.py', gon,
        '"""organismo_v15_dE5g_on = organismo_v15_dE5g.py con la dosis por defecto (eta_pred=0.03, k_sorp=5.0).\n'
        'Generado por construye_v15_dE5.py. NO editar."""\n')
    # --- (C) bateria del examen v3' ---
    srcb, sb = origen(os.path.join(ORG, 'bateria_v142.py'))
    b = sust(srcb, 'import organismo_v142 as v13   # TRONCO v14.2 = v14.1 + B-5 (desambiguar=1 por defecto)',
             'import organismo_v15_dE5_on as v13   # dE5: el CANDIDATO (v14.2 + sorpresa del mundo en la boca, k_sorp=5)', n=2, etq='bat: import')
    b = sust(b, "'organismo_v142.py'", "'organismo_v15_dE5_on.py'", n=2, etq='bat: sha')
    # ERR-30 (replay): la reduccion a v11/v10 del criterio 5 tiene que apagar TAMBIEN la dosis, EXPLICITAMENTE
    # (el modulo examinado la trae ENCENDIDA por defecto; "por defecto" no existe cuando el modulo es otro, ERR-38).
    b = sust(b, "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, **ESC_ID[esc])",
             "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, eta_pred=0.0, k_sorp=0.0, sesgo_fijo=0.0, **ESC_ID[esc])   # ERR-30: apaga TAMBIEN la dosis",
             etq='bat: ERR-30 v11')
    b = sust(b, "v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, **ESC_ID[esc])",
             "v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, eta_pred=0.0, k_sorp=0.0, sesgo_fijo=0.0, **ESC_ID[esc])   # ERR-30: apaga TAMBIEN la dosis",
             etq='bat: ERR-30 v10')
    b = sust(b, "f'examen_v142_{stamp}.log'", "f'examen_dE5_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v142_{stamp}.json'", "f'examen_dE5_{stamp}.json'", etq='bat: json')
    b = sust(b, "RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/",
             "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # dE5: experimentos/tronco_v15_dE5/ -> bundle/", etq='bat: RAIZ')
    b = sust(b, "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]",
             "sys.path[:0] = [os.path.join(RAIZ, 'organismo'), _D14, AQUI, os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo'), os.path.join(RAIZ, 'experimentos', 'bug01')]   # organismo/ PRIMERO (ERR-28)",
             etq='bat: sys.path')
    b = sust(b, "sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py'))",
             "sha_organismo_v11=h16(os.path.join(RAIZ, 'organismo', 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(RAIZ, 'organismo', 'organismo_v10.py'))",
             etq='bat: sha v11/v10')
    b = pon_sin_pool(b, 'bat')
    H['bateria_v15_dE5.py'] = escribe('bateria_v15_dE5.py', b,
        f'"""bateria_v15_dE5 = organismo/bateria_v142.py ({sb}, CONGELADA: solo se leyo) sobre **organismo_v15_dE5_on**\n'
        f'(la dosis ENCENDIDA: el examen mide AL CANDIDATO). Las SEIS etapas, los CRIT importados y los umbrales del\n'
        f'criterio v3\' quedan INTACTOS. Salida datos/examen_dE5_*. Generado por construye_v15_dE5.py. NO editar."""\n')
    # --- (D) bateria de generalizacion (regla 14: campo a campo contra la entrada del tronco) ---
    srcg2, sg2 = origen(os.path.join(ORG, 'bateria_generaliza_v142.py'))
    m = re.search(r"^ *'organismo_v142': \(.*$", srcg2, re.M)
    if not m:
        raise SystemExit('*** no encuentro la entrada organismo_v142 en INSTRUMENTOS')
    A = m.group(0)
    KW14 = ("eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1")
    nuevo = (A + "\n"
             f"    'organismo_v15_dE5_on': ('organismo_v15_dE5g_on', dict({KW14}, desambiguar=1, eta_pred=0.03, ema_pred=0.05, clip_e=3.0, k_sorp=5.0)),   # dE5 ON: los DIEZ campos de la entrada del tronco, IDENTICOS (regla 14), + las CUATRO perillas de la dosis EXPLICITAS (ERR-38)\n"
             f"    'organismo_v15_dE5': ('organismo_v15_dE5g', dict({KW14}, desambiguar=1, eta_pred=0.0, ema_pred=0.05, clip_e=3.0, k_sorp=0.0)),   # dE5 OFF (control pareado): los MISMOS campos con la dosis a cero")
    g2 = sust(srcg2, A, nuevo, etq='gen: INSTRUMENTOS')
    g2 = sust(g2, "RAIZ = os.path.dirname(AQUI)", "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # dE5: experimentos/tronco_v15_dE5/ -> bundle/", etq='gen: RAIZ')
    g2 = sust(g2, "f'regresion_generaliza_{modulo}_{stamp}.log'", "f'regresion_generaliza_dE5_{modulo}_{stamp}.log'", etq='gen: log')
    g2 = sust(g2, "f'regresion_generaliza_{modulo}_{stamp}.json'", "f'regresion_generaliza_dE5_{modulo}_{stamp}.json'", etq='gen: json')
    g2 = sust(g2, "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
              "sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]   # organismo/ PRIMERO (ERR-28)", etq='gen: sys.path')
    g2 = re.sub(r"_dir = \{'organismo_v14g': AQUI, 'organismo_v142g': AQUI,",
                "_dir = {'organismo_v14g': os.path.join(RAIZ, 'organismo'), 'organismo_v142g': os.path.join(RAIZ, 'organismo'), 'organismo_v15_dE5g_on': AQUI, 'organismo_v15_dE5g': AQUI,", g2, count=1)
    g2 = sust(g2, "sha_organismo=h16(os.path.join(AQUI, modulo + '.py'))", "sha_organismo=h16(os.path.join(AQUI, modulo + '.py')) if os.path.exists(os.path.join(AQUI, modulo + '.py')) else h16(os.path.join(RAIZ, 'organismo', modulo + '.py'))", etq='gen: sha organismo')
    g2 = sust(g2, "f\"  organismo {h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))}",
              "f\"  organismo {h16(os.path.join(AQUI if os.path.exists(os.path.join(AQUI, modulo + '.py')) else os.path.join(RAIZ, 'organismo'), (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))}", etq='gen: log organismo')
    g2 = pon_sin_pool(g2, 'gen')
    H['bateria_generaliza_v15_dE5.py'] = escribe('bateria_generaliza_v15_dE5.py', g2,
        f'"""bateria_generaliza_v15_dE5 = organismo/bateria_generaliza_v142.py ({sg2}, CONGELADA: solo se leyo) con DOS\n'
        f'entradas nuevas en INSTRUMENTOS (organismo_v15_dE5_on -> organismo_v15_dE5g_on, y el control OFF), con los DIEZ\n'
        f'campos de la entrada del tronco organismo_v142 CAMPO A CAMPO (regla 14) mas las cuatro perillas de la dosis\n'
        f'EXPLICITAS. Umbrales G1/G2/K sin tocar. Salida datos/regresion_generaliza_dE5_*.\n'
        f'Generado por construye_v15_dE5.py. NO editar."""\n')
    print(f'origen organismo_vivo_rep2 {s0}  organismo_vivo {s_vivo}  organismo_v142 {s142}  organismo_v142g {sg0}  bateria_v142 {sb}  bateria_generaliza_v142 {sg2}')
    for k, val in H.items():
        print(f'escrito {k:34s} {val}')
    print('Identidades:  python experimentos/tronco_v15_dE5/identidad_v15_dE5.py')
