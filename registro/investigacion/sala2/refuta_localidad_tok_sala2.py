"""REFUTADOR sala 2 (lente localidad) para DISENO_mundo_grande.md.
Pregunta: la regla `_tok` del diseno (leer un codigo NO familiar por otro codigo FAMILIAR con el que comparte K-1 = 2 celdas)
es "inerte por construccion en el mundo A/B del examen" (DISENO §2.2)?  Hipotesis del refutador: NO, porque la fision de v11
(division por conflicto de signo) produce un codigo nuevo = codigo viejo - 1 celda + hija, que comparte EXACTAMENTE K-1 celdas
con su propio antecesor (familiar, con evidencia y celdas consolidadas): `_tok` lo leeria por el antecesor, cuyo signo es el VIEJO.

Metodo: copia EN MEMORIA de organismo/organismo_v14.py (v14.1, feefc88b1fd8d434; SOLO se lee; ningun archivo del repo se toca),
con tres hooks de SOLO LECTURA (no cambian estado del organismo ni consumen rng): (1) en cada visita a un objeto, si el codigo
propio no es familiar y existe un codigo familiar en `_ord` con solapamiento >= 2 y ya hubo una visita previa (nenc >= 1),
se registra el evento "_tok dispararia" con el valor que leeria por el antecesor y el valor que lee v14.1 (lenta); (2) en cada fision,
codigo viejo, codigo nuevo y su solapamiento; (3) nenc como en A5 del diseno. La trayectoria es la de v14.1 EXACTA (los hooks no
alteran nada): lo que se cuenta es cuantas veces la perilla `token=1` habria desviado la conducta respecto del tronco.
UNA corrida de UN proceso, T = 50 000, escenario E2L del examen (solap_AB=3: A y B nacen con el MISMO codigo; v14.1 los separa por
fision antes de t = 25 000 segun 4d de bateria_v14). Sin Pool. organismo/ primero en sys.path (ERR-28).
Uso: python refuta_localidad_tok_sala2.py [seed=101] [T=50000]"""
import sys, os, json, hashlib, time
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]
import numpy as np

SRC = os.path.join(RAIZ, 'organismo', 'organismo_v14.py')
SHA = hashlib.sha256(open(SRC, 'rb').read()).hexdigest()[:16]
assert SHA == 'feefc88b1fd8d434', SHA
s = open(SRC, encoding='utf-8').read()

def sust(texto, viejo, nuevo, n=1):
    c = texto.count(viejo)
    assert c == n, (c, viejo[:60])
    return texto.replace(viejo, nuevo)

s = sust(s, "    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion\n",
         "    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion\n"
         "    nenc={}; _ev_tok=[]; _ev_fis=[]; _n_vis_nofam=0   # REFUTADOR: solo lectura\n"
         "    def kenyon_de(_o):\n"
         "        _k=np.zeros(NKMAX); _k[list(_o)]=1; return _k\n")
s = sust(s, "            vis[kk][q(t)]+=1\n",
         "            vis[kk][q(t)]+=1\n"
         "            _q0=_key(kc)   # REFUTADOR: hook de solo lectura (regla _tok del diseno, A3)\n"
         "            if not _fam(kc):\n"
         "                _n_vis_nofam+=1\n"
         "                _cands=[(len(_q0&_o),ncod[_o],sorted(_o)) for _o in _ord if _o!=_q0 and len(_q0&_o)>=2 and _fam(kenyon_de(_o))]\n"
         "                if _cands and nenc.get(_q0,0)>=1:\n"
         "                    _b=max(_cands); _ev_tok.append(dict(t=t,pat=kk,solap=_b[0],ev_tok=_b[1],cod_propio=sorted(_q0),cod_token=_b[2],\n"
         "                        lee_token=round(float((Wp-Wn)@kenyon_de(frozenset(_b[2]))),3),lee_v14_lenta=round(_ws,3),lee_propio_rapida=round(_wf,3),R_mundo=R_VAL[val[kk]]))\n"
         "            nenc[_q0]=nenc.get(_q0,0)+1\n")
s = sust(s, "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n",
         "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n"
         "                                    _cn=code(P); _ev_fis.append(dict(t=t,pat=kk,cod_viejo=sorted(_key(kc)),cod_nuevo=sorted(_cn),solap=len(_key(kc)&_cn),\n"
         "                                        madre=int(c),hija=int(j),madre_en_nuevo=bool(c in _cn),hija_en_nuevo=bool(j in _cn),Wb_madre=round(float(Wp[c]-Wn[c]),3),Wb_hija=round(float(Wp[j]-Wn[j]),3)))\n")
s = sust(s, "    return dict(sobre=sobre,", "    return dict(ev_tok=_ev_tok,ev_fis=_ev_fis,n_vis_nofam=_n_vis_nofam,sobre=sobre,")

ns = {}
exec(compile(s, '<organismo_v14_instrumentado_en_memoria>', 'exec'), ns)

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 101
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    assert T <= 50000
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] v14.1 {SHA} instrumentado en memoria; E2L (solap_AB=3) seed {seed} T {T}; un proceso, sin Pool", flush=True)
    r = ns['run'](seed, T=T, solap_AB=3)
    dt = time.time() - t0
    ev, fis = r['ev_tok'], r['ev_fis']
    out = dict(seed=seed, T=T, escenario='E2L solap_AB=3', sha_v14=SHA, segundos=round(dt, 1), splits=r['splits'], celdas=r['celdas'],
               W=r['W'], W_lenta=r['W_lenta'], solap=r['solap'], n_visitas_no_familiar=r['n_vis_nofam'],
               n_eventos_tok=len(ev), n_eventos_tok_signo_token_distinto_del_mundo=sum(1 for e in ev if e['lee_token'] * e['R_mundo'] < 0),
               n_eventos_tok_signo_lenta_correcto=sum(1 for e in ev if e['lee_v14_lenta'] * e['R_mundo'] > 0),
               por_patron={k: sum(1 for e in ev if e['pat'] == k) for k in 'AB'},
               primer_evento=ev[0] if ev else None, ultimo_evento=ev[-1] if ev else None,
               fisiones=fis, fisiones_con_solap_K_1=sum(1 for f in fis if f['solap'] == 2),
               eventos_tok_muestra=ev[:15])
    p = os.path.join(AQUI, f'refuta_localidad_tok_sala2_E2L_s{seed}.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False,
              default=lambda o: int(o) if isinstance(o, np.integer) else (float(o) if isinstance(o, np.floating) else str(o)))
    print(f"[{time.strftime('%H:%M:%S')}] {dt:.1f} s; splits {r['splits']} celdas {r['celdas']} W {r['W']} solap {r['solap']}")
    print(f"  fisiones: {len(fis)}; con solapamiento viejo-nuevo == K-1: {out['fisiones_con_solap_K_1']}")
    for f in fis: print('   ', f)
    print(f"  visitas con codigo NO familiar: {r['n_vis_nofam']}; eventos en que _tok dispararia: {len(ev)} "
          f"(por patron {out['por_patron']}); de ellos, el valor leido por el token tiene signo CONTRARIO al del mundo: "
          f"{out['n_eventos_tok_signo_token_distinto_del_mundo']}; la lenta de v14.1 acierta el signo en: {out['n_eventos_tok_signo_lenta_correcto']}")
    if ev: print('  primer evento:', ev[0]); print('  ultimo evento:', ev[-1])
    print('  escrito', p)
