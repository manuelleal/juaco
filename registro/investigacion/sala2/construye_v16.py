"""SALA 2 (creador radical, 18-sep-2026) -- construye POR ANCLAS organismo_v16.py = organismo/organismo_v14.py (v14.1,
feefc88b1fd8d434, CONGELADO: solo se lee) + TOKEN (grafo de nodos-retina con valor de un golpe y aristas de variante).
NO toca nada del repo: escribe unicamente en registro/investigacion/sala2/. Con token=0 el organismo es v14.1 BIT A BIT
(ninguna linea nueva consume rng; la boca lee _wm=_wt). Seis anclas (A1..A6); si alguna no aparece exactamente una vez, aborta.
Uso: python registro/investigacion/sala2/construye_v16.py
"""
import hashlib, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v14.py')
SHA_ESPERADO = 'feefc88b1fd8d434'

def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

def sust(t, a, b, etq):
    c = t.count(a)
    if c != 1: raise SystemExit(f'*** ancla {etq!r} aparece {c} veces (se esperaba 1). No se escribe nada.')
    return t.replace(a, b)

s = h16(ORIGEN)
if s != SHA_ESPERADO: raise SystemExit(f'*** origen {ORIGEN}: sha {s} != {SHA_ESPERADO}. No se escribe nada.')
src = open(ORIGEN, 'rb').read().decode('utf-8')

# A1 firma: dos perillas nuevas, apagada la maestra
src = sust(src, ",puerta_pat=5,pat_shuf=0,pat_min=1):", ",puerta_pat=5,pat_shuf=0,pat_min=1,token=0,tok_var=1):", 'A1 firma')
# A2 estado nuevo + dos ayudantes (sin rng)
A2 = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n"
src = sust(src, A2, A2 +
    "    _tok={}   # TOKEN (v16): retina exacta -> [valor escrito de UN golpe, n de consecuencias propias]. Nace en la primera LLEGADA (n=0). Sin constantes.\n"
    "    def _tkey(_P): return frozenset(np.flatnonzero(_P>0).tolist())\n"
    "    def _tlee(_P):   # TOKEN: lectura del grafo. Propio si n>=1; si no y tok_var, media de los vecinos a Hamming 1 con consecuencia (arista de variante); si no, None -> v14.1\n"
    "        _q=_tkey(_P); _e=_tok.get(_q)\n"
    "        if _e is not None and _e[1]>0: return _e[0]\n"
    "        if not tok_var: return None\n"
    "        _v=[_x[0] for _u,_x in _tok.items() if _x[1]>0 and len(_q^_u)==1]\n"
    "        return (sum(_v)/len(_v)) if _v else None\n", 'A2 estado')
# A3 valor(): el grafo manda si tiene algo que decir (solo lectura: no crea nodos)
A3 = "        return _f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)\n"
src = sust(src, A3,
    "        _v14=_f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)\n"
    "        if token:   # TOKEN: si el grafo tiene algo que decir, manda (valor() NO crea nodos)\n"
    "            _tl=_tlee(P)\n"
    "            if _tl is not None: return _tl\n"
    "        return _v14\n", 'A3 valor')
# A4 boca: nace el nodo en la llegada; la boca lee el grafo; las vias siguen con su propio error (_wt/_wf/_ws intactos)
A4 = "            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n"
src = sust(src, A4,
    "            _wm=_wt   # TOKEN: lo que lee la BOCA; con token=0 es _wt exacto\n"
    "            if token:\n"
    "                _tq=_tkey(PAT[kk])\n"
    "                if _tq not in _tok: _tok[_tq]=[0.0,0]   # TOKEN: el nodo nace en la primera LLEGADA, sin valor propio\n"
    "                _tl=_tlee(PAT[kk])\n"
    "                if _tl is not None: _wm=_tl\n"
    "            Vb=alpha*_wm+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n", 'A4 boca')
# A5 mordida: escritura de un golpe por sobrescritura
A5 = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
src = sust(src, A5, A5 +
    "                if token: _tok[_tq][0]=R; _tok[_tq][1]+=1   # TOKEN: aprender = escribir R de un golpe; desaprender = sobrescribir\n", 'A5 mordida')
# A6 salida (claves nuevas de solo lectura)
src = sust(src, "    return dict(sobre=sobre,",
    "    return dict(token=token,tok_var=tok_var,n_tok=len(_tok),tok={''.join('1' if _i in _k else '0' for _i in range(6)):(round(float(_v[0]),3),_v[1]) for _k,_v in _tok.items()},sobre=sobre,", 'A6 salida')

cab = (f'"""organismo_v16 (SALA 2, diseno radical) = organismo/organismo_v14.py ({s}, TRONCO v14.1 CONGELADO: solo se leyo) + TOKEN:\n'
       f'grafo de nodos-retina (clave = retina exacta) con valor escrito de UN golpe y sobrescrito, nacidos en la primera llegada;\n'
       f'aristas de variante implicitas (Hamming 1) por las que un nodo sin consecuencia propia lee a sus vecinos; la BOCA lee el\n'
       f'grafo si tiene algo que decir y si no v14.1; las dos vias de v14.1 siguen aprendiendo de su propio error, sin tocar.\n'
       f'Con token=0 es organismo_v14 EXACTO y no consume rng. Generado por construye_v16.py. NO editar a mano. NO es candidato:\n'
       f'es el instrumento del diseno registro/investigacion/sala2/DISENO_radical.md (una sola corrida de humo permitida).\n"""\n')
out = os.path.join(AQUI, 'organismo_v16.py')
open(out, 'w', encoding='utf-8', newline='\n').write(cab + src)
print(f'origen organismo_v14.py {s}  ->  escrito organismo_v16.py {h16(out)}')
