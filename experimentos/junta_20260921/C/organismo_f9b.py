"""organismo_f9b.py — GENERADO POR construye_f9b.py DESDE organismo_f9.py (3a821884394d66c9).
NO EDITAR A MANO. Perilla nueva: nodo_via (0 = organismo_f9 BIT A BIT; 1 = el mensaje del nodo
entra TAMBIEN por la via rapida, con la misma regla local de la mordida y contando evidencia).
Memoria nueva: CERO. Junta del 21-sep-2026, creador C, fase 9 bloque 2."""
"""organismo_f9 = organismo_alma2.py (4fd616aeaf535e61; aqui solo se LEYO; cadena: organismo_alma
7c09cec391daa879 <- organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <-
organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO
organismo/organismo_v14.py v14.1 feefc88b1fd8d434) + LAS CUATRO PERILLAS DE LA FASE 9.

  nodo_rel=0, con_desde=0, rep_acum=0, f9=0  ->  organismo_alma2 BIT A BIT (todos sus brazos)
  nodo_rel=1  ->  RELEVANCIA VIVA: el recien nacido lee TODO el nodo por puntaje local
                  |R - (Wps-Wns)@P| con SU PROPIO vector, sobre TODO el nodo; los nodo_lee mayores,
                  en orden cronologico, empate por recencia. Cero memoria nueva.
  nodo_rel=2  ->  CONTROL DE ACCESO: mismo alcance, seleccion AL AZAR (rng propio 870000+1000000*seed).
  con_desde=c ->  el linaje se conecta recien tras la muerte c (los cuerpos 1..c-1 son NADA).
  rep_acum=1  ->  la ventana de reproduccion cuenta pasos saciados SIN exigir que sean seguidos; se
                  reinicia AL MORIR (dentro de un cuerpo). Perilla DEL MUNDO, aparte del mecanismo.
  f9=1        ->  medidas de solo lectura del cuerpo que muere: p1, c1, t_ok, con_cuerpo.

LAS MEDIDAS p1 Y c1 VAN SIEMPRE JUNTAS (trampa 2 de la noche del 17-sep): un cuerpo generico-cauto sube
p1 y hunde c1, y se muere de hambre. Ningun veredicto se lee sobre p1 solo.

Arnes: identidad_f9.py. Generado por construye_f9.py. NO editar a mano."""
"""organismo_alma2 = organismo_alma.py (7c09cec391daa879, el instrumento del BLOQUE ALMA, identidad 64/64;
aqui solo se LEYO; cadena: organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <-
organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo_v14 v14.1
feefc88b1fd8d434) + LOS TRES CONTROLES que el PREREGISTRO_alma.md exige ANTES de la serie.

  menu='abcdef', nodo_baraja=0  ->  organismo_alma BIT A BIT (con alma=None ni aparece la clave `alma2`)
  menu=<subconjunto>            ->  el resumen le OFRECE al alma ese menu y el instrumento ACEPTA solo ese menu.
                                    ALMA-SIN-NODO = menu sin (a) ni (b): el nodo se llena y nadie se conecta.
  nodo_baraja=1                 ->  en cada nacimiento conectado, las recompensas de los mensajes que el hijo va
                                    a leer se PERMUTAN entre si (rng propio 860000+1000000*seed): mismos patrones,
                                    mismas recompensas, mal emparejadas. Es el control de CONTENIDO (H1-4).
  conectado=1 (ya existia)      ->  NODO-CIEGO: el linaje nace conectado y las curitas van al azar sin (a).

EL INSTRUMENTO ES ESTRICTO, EL BUZON ES PACIENTE: una curita fuera del menu ABORTA aqui; la tolerancia a las
respuestas invalidas de un agente externo vive en corre_alma.py, que las registra como (f) y sigue.

Arnes: identidad_alma2.py. Generado por construye_alma2.py. NO editar a mano."""
"""organismo_alma = experimentos/nivel11_mundo_vivo/organismo_vivo_h1.py (9e99ff87b5e2db1e, el instrumento de
H-1 "QUE LA MUERTE MATE"; aqui solo se LEYO; cadena: organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep
aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434)
+ EL BLOQUE ALMA (nivel 13): UN NODO CENTRAL y UN ALMA EXTERNA QUE PARCHA AL CUERPO CADA VEZ QUE MUERE.

  alma=None   ->  organismo_vivo_h1 BIT A BIT (todas las claves, mismo consumo del rng del mundo)
  alma=fn     ->  cada muerte: (1) el NODO CENTRAL recibe las ultimas `nodo_k` mordidas CON CONSECUENCIA del cuerpo
                  que muere, como mensajes (patron, R cruda, necesidad activa); (2) se llama a `fn(resumen)` con la
                  causa (la necesidad que llego a cero), la edad, los hijos, las ultimas 20 exposiciones y mordidas
                  y el estado del linaje; (3) `fn` devuelve UNA curita del MENU CERRADO de MENU_curitas.md
                  ('a' conectar al nodo / 'b' subir el miedo escribiendolo en el nodo / 'c' dote mayor /
                   'd' bajar el umbral de reproduccion / 'e' heredar valores (M1) / 'f' nada) y se aplica;
                  (4) el cuerpo siguiente, si el linaje esta CONECTADO, nace leyendo el nodo como EXPOSICIONES SIN
                  CONSECUENCIA (contrato del BLOQUE 4: via lenta, sin energia, sin objetos, sin ncod, sin via
                  rapida, sin plasticidad, sin rng). La corrida termina en la muerte numero `alma_muertes`.

EL NODO NO ES EL CANAL DE b4b: b4b escribe en la TABLA DE PARES (organo de v15f) que esta cadena NO tiene. Lo que
se traduce es su CONTRATO ("exposicion sin consecuencia con la valencia recibida"), ejecutado con el bloque de la
VIA LENTA extraido literalmente de la mordida de h1. Comparar numeros con b4b seria ilegitimo.

EL ALMA ES EL BUSCADOR, NO EL RESULTADO (como JUACO-EVO): lo que encuentre es una HIPOTESIS que hay que volver a
correr SIN alma, con las perillas fijas desde el paso 0, preregistro nuevo y semillas nuevas.

ANCLA DE IDENTIDAD: alma=None -> organismo_vivo_h1 bit a bit en los cinco modos de H-1; ninguna insercion consume
el rng del mundo. Arnes: identidad_alma.py. Generado por construye_alma.py. NO editar a mano."""
"""organismo_vivo_h1 = organismo_vivo_rep2.py (96feb4918dc5d694; aqui solo se LEYO; cadena: organismo_vivo_rep
aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434) +
LA MUERTE QUE MATA (H-1 de la sala 4; PREREGISTRO_h1_muerte.md). Hoy el renacer conserva Wp, Wn, KW, activa, Wps,
Wns y ncod: el individuo es inmortal en memoria y el renacer REGALA 600 pasos de drenaje (E=Ag=0.6), que financian
el 34-77 % de las ventanas de reproduccion (SALA4 §B E-1).
  muerte_real=0  ->  organismo_vivo_rep2 BIT A BIT (todas las claves, mismo consumo del rng del mundo)
  muerte_real=1  ->  al morir se BORRA la memoria del individuo (valores, codigo activo, tabla, predictor, trazas,
                     locomocion) y el cuerpo siguiente nace VACIO, con rng propio SEM_HIJO(seed,k)=700000+1000000*seed+k
                     (ERR-60: la formula literal del encargo colisionaba entre semillas vecinas) y con la DOTE que
                     su padre pago al cerrarse la ventana. Si no hay descendiente en la cola, el linaje se EXTINGUIO
                     y el mundo pone un fundador: se cuenta (`fundadores`).
  hereda = 'nada' | 'M1' (el VECTOR: Wps/Wns sobre la retina) | 'M1+pares' (el vector Y el TOKEN: KW/activa + los
                     pares codigo<->valor) | 'baraja' (M1 con los 6 pixeles permutados: la prediccion que decide).
ANCLA DE IDENTIDAD: muerte_real=0 y h1=0 -> organismo_vivo_rep2 bit a bit; h1=1 -> claves viejas bit a bit + 13
nuevas; reproduccion=0 -> todo H-1 inerte. Arnes: identidad_vivo_h1.py. Generado por construye_vivo_h1.py. NO editar a mano."""
"""organismo_vivo_rep2 = organismo_vivo_rep.py (aa823d56c2d4213c; aqui solo se LEYO; cadena: organismo_vivo 20c0961c79de8825
<- TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434) + DIAGNOSTICOS DE ERR-40 para el bloque 2 de reproduccion
(PREREGISTRO_reproduccion_2.md): la medida nueva es el crecimiento neto del linaje r = descendientes - muertes (la calcula el
runner con claves que ya existen); aqui solo se agregan, de SOLO LECTURA y detras de `rep2`, desc_regalo (ventanas que
empezaron dentro de los 600 pasos que dura el regalo del renacer) y las longitudes de las vidas.
ANCLA DE IDENTIDAD: reproduccion=0 -> organismo_vivo BIT A BIT; rep2=0 -> organismo_vivo_rep BIT A BIT; rep2=1 -> claves
viejas bit a bit + 4 nuevas. Arnes: identidad_vivo_rep2.py. Generado por construye_vivo_rep2.py. NO editar a mano."""
"""organismo_vivo_rep = experimentos/nivel11_mundo_vivo/organismo_vivo.py (20c0961c79de8825, el mundo vivo; aqui solo se
LEYO; a su vez por anclas desde el TRONCO CONGELADO organismo/organismo_v14.py v14.1 feefc88b1fd8d434) + PROPOSITO Y
REPRODUCCION (peldano minimo, PREREGISTRO_reproduccion.md): (a) REPRODUCCION COMO MEDIDA: ventanas de viabilidad
(rep_X pasos seguidos con E y Ag >= rep_umbral) = descendientes viables, pasos viables y tabla de la boca SACIADO, todo
de solo lectura; (b) PROPOSITO como TERCERA NECESIDAD (fila 2 de valor: reproducirse; su cuerpo es el cuello de botella
min(E,Ag); manda solo cuando las dos primarias callan; con rep_coste paga E y Ag por cada descendiente);
(c) CUELLO, control: saciado, lee la fila del recurso mas escaso, sin fila nueva.
ANCLA DE IDENTIDAD: con reproduccion=0 (por defecto) es organismo_vivo BIT A BIT, mismo consumo del rng y mismas claves.
Arnes: identidad_vivo_rep.py.  Generado por construye_vivo_rep.py. NO editar a mano."""
"""organismo_vivo = organismo/organismo_v14.py (v14.1, feefc88b1fd8d434, TRONCO CONGELADO: aqui solo se LEYO) +
MUNDO VIVO (nivel 11, linea (F) de PLAN.md): DOS necesidades (hambre/sed) y CUATRO estimulos (comida A, veneno B,
agua C, sal D = los cuatro patrones que ya existen), estado interno VECTORIAL con dos muertes posibles, boca que
decide con la NECESIDAD ACTIVA, valor aprendido POR ESTIMULO Y POR NECESIDAD (Wp/Wn/Wps/Wns pasan a matriz
(n_nec, ...)), predictor de dS VECTORIAL y sorpresa POR NECESIDAD.
ANCLA DE IDENTIDAD: con vivo=0 y n_nec=1 (una necesidad, dos estimulos) es organismo_v14 BIT A BIT -- mismo
consumo del rng y MISMAS claves de salida (el dict del mundo vivo se agrega solo si vivo=1).
Arnes: identidad_vivo.py.  Generado por construye_vivo.py. NO editar a mano."""
"""v14.1 = TRONCO desde el 18 sep 2026 (05:55): v14 con eta_s 0.15 y clip_s 10 (bloque A-4: la regla local llega a 1.000 con rasgos dados, 150 exposiciones; examen 8/8 en 101-120 y 121-140, generalizacion 1.000/0.97). v14 (05:00) era: organismo_v13 (cc8b16b492d4d324) + HIJA DISPERSA por relevancia (mask_rel=2,
del_s=del_c=0.25, ema_c=0.05: la hija nace ciega a parte de P) + PUERTA DE FAMILIARIDAD POR EVIDENCIA DEL CODIGO EXACTO
(puerta_pat=5, pat_min=1: familiar si el codigo se mordio >= 5 veces Y tiene >= 1 celda consolidada). Generado por anclas
(experimentos/nivel10_composicion_v14/construye_v14c.py; copia de organismo_v14c_on.py 00e941c861896455). Con mask_rel=0 y
puerta_pat=0 es organismo_v13 EXACTO (identidad 30/30). Examen v3' 8/8 en 121-140, 141-160 y 161-180 (7/8 en 101-120: semilla
117, caso conocido); generalizacion 1.000/0.94-0.95 x3; capacidad N* 51; 3T-k 0.237 con 53 celdas. Gemelo: organismo_v14_rapido.py.
CONGELADO: no se edita. Evidencia: registro/PROPUESTA_v14.md y REGISTRO_etapas_1_2.md.
"""
"""organismo_v14c_on = organismo_v14c.py con mask_rel=2 (hija dispersa; el punto de organismo_v13Don) Y
puerta_pat=5,pat_min=1 (puerta por codigo PATC = evidencia Y >=1 celda consolidada; el punto de
organismo_v13Bn5c) POR DEFECTO -- las DOS perillas ENCENDIDAS. El mismo archivo con las constantes
cambiadas, para que bateria_v14c.py lo examine sin tocar la bateria congelada.
Generado por construye_v14c.py. NO editar."""
"""organismo_v14c = organismo/organismo_v13.py (cc8b16b492d4d324, CONGELADO: solo se leyo) + COMPOSICION
de los dos candidatos a v14 con evidencia completa (registro/PROPUESTA_v14.md): HIJA DISPERSA POR
RELEVANCIA (perilla mask_rel; actua en el NACIMIENTO, nivel7_hija_dispersa/construye_v13D.py) + PUERTA POR
EVIDENCIA DEL CODIGO EXACTO (perilla puerta_pat, PATC; actua en el RUTEO, no en el aprendizaje,
nivel4_puerta_codigo/construye_puerta_codigo.py). Generado por construye_v14c.py. NO editar a mano.
Con mask_rel=0 y puerta_pat=0 es organismo_v13 EXACTO (arnes: identidad_v14c.py)."""
"""
Organismo v13 — CANDIDATO A TRONCO (congelable solo si pasa PREREGISTRO_tronco_v13.md): v11 + VIA LENTA lineal
sobre la retina + PUERTA de familiaridad. Punto confirmado en semillas 61-80: eta_s=0.015, puerta=3
(datos v13_dos_vias_20260917_160541: retencion 20/20, acierto en patrones nunca vistos 0.850, E1/E2/E2L 20/20).

Dos vias con UN solo error (esquema CLS minimo): la rapida es v11 sin tocar (Kenyon + division por conflicto de
signo); la lenta es una lectura lineal directa de los 6 pixeles con dos canales Wps/Wns (>=0, tope clip_s) a tasa
eta_s < eta, con el mismo drenaje de la parte comun. Cada via aprende de SU error. La boca consulta la rapida solo
si el patron le es FAMILIAR (>= puerta de las 3 celdas de su codigo con |Wp-Wn|>0.2, el umbral de v11); si no,
consulta la lenta, que aprende la regla y no los casos. Con eta_s=0 y puerta=None es v11 EXACTO.
Linaje: ... -> v9 (d3b72fb8819fbe8e) -> v10 (219d5033fe15b5b9, instrumento) -> v11 (f69e24063be1b194) -> v13.
Generado por experimentos/v13_dos_vias/construye_v13_tronco.py (a partir del genoma explorado). NO editar a mano.
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}
# --- MUNDO VIVO (nivel 11): DOS necesidades y CUATRO estimulos = los CUATRO patrones que YA existen.
#     El eje de ENERGIA es exactamente el de v14: EFECTO['comida'][0]==E_VAL['comida'] y
#     EFECTO['veneno'][0]==E_VAL['veneno']; el mapa de recompensa (dS>0->+1, dS<0->-3) reproduce R_VAL.
NEC=('hambre','sed')   # 0 = energia (E), 1 = agua (Ag)
VAL_VIVO={'A':'comida','B':'veneno','C':'agua','D':'sal'}
EFECTO={'comida':(+0.8,0.0),'veneno':(-0.4,0.0),'agua':(0.0,+0.8),'sal':(0.0,-0.4)}   # (dE, dAgua) nominal

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.15,clip_s=10.0,puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1,vivo=0,n_nec=1,estims=None,costo_a=0.002,A_ini=1.0,val_esc=0,nec_shuf=0,hereda_nec=1,tabla=None,eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,crit_exp=0.5,reproduccion=0,rep_mide=1,rep_X=500,rep_umbral=1.0,rep_coste=0.0,rep_nec=0,rep_cuello=0,rep2=0,rep2_regalo=600,muerte_real=0,hereda='nada',dote=0.6,cola_max=200,h1=0,alma=None,alma_muertes=0,nodo=1,conectado=0,nodo_k=20,nodo_lee=50,miedo_n=5,miedo_R=-3.0,d_dote=0.1,d_umbral=0.1,menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0,nodo_via=0):
    if n_nec>1 and not vivo: raise SystemExit('MUNDO VIVO: n_nec>1 exige vivo=1 (la mordida debe tener consecuencia vectorial)')
    if not reproduccion: rep_mide=0; rep_nec=0; rep_cuello=0; rep_coste=0.0   # REP: perilla MAESTRA apagada -> todo lo de abajo es inerte: organismo_vivo EXACTO
    if not reproduccion: rep2=0   # REP2: detras de la maestra
    if rep2 and not rep_mide: raise SystemExit('REP2: rep2=1 exige rep_mide=1 (la ventana es el nacimiento)')
    if not reproduccion: muerte_real=0; h1=0; hereda='nada'   # H1: detras de la maestra (inerte: organismo_vivo EXACTO)
    if not muerte_real: alma=None; alma_muertes=0   # ALMA: detras de la muerte real (inerte: organismo_vivo_h1 EXACTO)
    if alma is not None and not callable(alma): raise SystemExit('ALMA: alma es None o un invocable (resumen -> {curita, motivo})')
    if alma is not None and not alma_muertes: raise SystemExit('ALMA: alma exige alma_muertes>=1 (la serie de cuerpos ES la medida)')
    if alma is not None and not nodo and conectado: raise SystemExit('ALMA: conectado=1 exige nodo=1 (no hay a que conectarse)')
    if alma is None: nodo_baraja=0   # ALMA2: detras de la maestra (inerte: organismo_alma EXACTO)
    if alma is not None and (not menu or len(set(menu))!=len(menu) or any(_z0 not in 'abcdef' for _z0 in menu)):
        raise SystemExit(f'ALMA2: menu={menu!r} debe ser un subconjunto no vacio y sin repeticiones de abcdef')
    if alma is not None and nodo_baraja and not nodo: raise SystemExit('ALMA2: nodo_baraja=1 exige nodo=1 (no hay nodo que barajar)')
    if alma is None: nodo_rel=0; con_desde=0; f9=0   # F9: perillas del NODO, detras de la maestra (inerte: organismo_alma2 EXACTO)
    if alma is None: nodo_via=0   # F9B: perilla del NODO, detras de la maestra (inerte: organismo_f9 EXACTO)
    if nodo_via not in (0,1): raise SystemExit('F9B: nodo_via es 0 (solo la via lenta, como el bloque 1) o 1 (las DOS vias)')
    if nodo_via and not nodo: raise SystemExit('F9B: nodo_via exige nodo=1 (no hay nodo que leer)')
    if not rep_mide: rep_acum=0   # F9: rep_acum es perilla DEL MUNDO (detras de la medida), no del alma: vale tambien con alma=None
    if nodo_rel not in (0,1,2,3): raise SystemExit('F9: nodo_rel es 0 (recencia), 1 (relevancia viva), 2 (azar sobre todo el nodo) o 3 (relevancia fija)')
    if nodo_rel and not nodo: raise SystemExit('F9: nodo_rel exige nodo=1 (no hay nodo que leer)')
    if con_desde and not nodo: raise SystemExit('F9: con_desde exige nodo=1 (no hay a que conectarse)')
    if con_desde and conectado: raise SystemExit('F9: con_desde y conectado=1 son EXCLUYENTES (o nace conectado o se conecta despues)')
    if f9 and not (h1 and rep2): raise SystemExit('F9: f9=1 exige h1=1 y rep2=1 (las medidas del cuerpo usan su nacimiento y su vida)')
    if muerte_real and not h1: raise SystemExit('H1: muerte_real=1 exige h1=1 (los diagnosticos del linaje SON la medida)')
    if h1 and not rep2: raise SystemExit('H1: h1=1 exige rep2=1 (la marca del nacimiento y las vidas vienen de rep2)')
    if hereda not in ('nada','M1','M1+pares','baraja'): raise SystemExit("H1: hereda es 'nada', 'M1', 'M1+pares' o 'baraja'")
    if hereda!='nada' and not muerte_real: raise SystemExit('H1: hereda exige muerte_real=1 (sin muerte no hay parto)')
    if muerte_real and rep_coste: raise SystemExit('H1: dote y rep_coste son EXCLUYENTES (el padre paga una sola vez)')
    if muerte_real and not (0<dote<rep_umbral): raise SystemExit('H1: la dote debe cumplir 0 < dote < rep_umbral (pagarla no puede matar al padre)')
    if rep_nec and n_nec!=3: raise SystemExit('REP: rep_nec=1 exige n_nec=3 (la tercera fila de valor ES la necesidad de reproducirse)')
    if n_nec==3 and not rep_nec: raise SystemExit('REP: n_nec=3 exige rep_nec=1 (sin la tercera necesidad no hay tercera componente de dS)')
    if n_nec>3: raise SystemExit('REP: n_nec maximo 3')
    if rep_cuello not in (0,1,2): raise SystemExit('REP: rep_cuello es 0, 1 (CUELLO) o 2 (CUELLO_MIN)')
    if rep_cuello and (n_nec!=2 or rep_nec): raise SystemExit('REP: rep_cuello (control) exige n_nec=2 y rep_nec=0')
    if rep_cuello==2 and puerta is None: raise SystemExit('REP: rep_cuello=2 exige puerta (con puerta=None el valor de la boca entra en el aprendizaje)')
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros((n_nec,NKMAX)); Wn=np.zeros((n_nec,NKMAX)); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)
    Wps=np.zeros((n_nec,6)); Wns=np.zeros((n_nec,6))   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0). VIVO: una fila por necesidad
    _na=0; _nm=0   # VIVO: necesidad ACTIVA (manda boca y division) y la que INDEXA la memoria (val_esc -> siempre 0). Con n_nec=1 nunca cambian
    _EF=dict(EFECTO) if tabla is None else dict(tabla)   # VIVO: (dE,dAg) por valencia; `tabla` sirve para el control 'estimulo que no informa'
    _rng_n=np.random.default_rng(seed+900000) if nec_shuf else None   # CONTROL barajado: rng PROPIO (v13s), no toca el del organismo
    Wpe=np.zeros((n_nec,6)); Wke=np.zeros((n_nec,NKMAX)); _sbE=np.zeros(n_nec)   # VIVO: predictor VECTORIAL de dS y SORPRESA POR NECESIDAD (inerte con eta_pred=0)
    _enc={k:0 for k in PAT}; _exp=[{k:None for k in PAT} for _ in range(n_nec)]   # VIVO: exposiciones y EXPOSICIONES HASTA CRITERIO (solo lectura)
    _mnec=[0,0]; _bxor=[[0]*4 for _ in range(n_nec)]; _exor=[[0]*4 for _ in range(n_nec)]   # VIVO: muertes [por energia, por agua] y tabla NECESIDAD x ESTIMULO (solo lectura)
    _IDX={_k2:_i2 for _i2,_k2 in enumerate('ABCD')}
    _gv=0; _desc=0; _pv=0; _tdesc=[]; _dq=[0]*4; _bsac={k:0 for k in PAT}; _dsac={k:0 for k in PAT}; _sac=False; _cue2=False   # REP: ventana de viabilidad, descendientes viables, pasos viables, tabla de decisiones/mordidas SACIADO (solo lectura si rep_coste=0); _cue2 = CUELLO_MIN activo
    _tmu=0; _vidas=[]; _dreg=0; _gv0=0   # REP2: marca del ultimo renacer (t=0 cuenta como nacimiento), longitudes de vida, ventanas financiadas por el regalo del renacer, primer paso saciado de la ventana en curso. SOLO LECTURA
    _cola=[]; _nac=0; _fund=0; _dfund=0; _dpv=[]; _dv=0; _cdes=0; _tfund=[]; _svid=0; _esfund=True; _nbar=0; _vh=[]; _org=[]   # H1: cola FIFO de descendientes por nacer (con la memoria que se lleva el hijo y su dote), partos, fundaciones del mundo (linaje extinto), ventanas financiadas por una fundacion NO pagada, descendientes por cuerpo, del cuerpo en curso, descartes por desborde, pasos de cada fundacion, suma de vidas SIN tope, si el cuerpo actual nacio de un regalo, permutaciones identidad en BARAJA, vidas SIN tope y origen de cada cuerpo (0 fundacion regalada, 1 dote pagada). SOLO LECTURA salvo la cola y la dote
    _rb=np.random.default_rng(800000+1000000*seed) if (muerte_real and hereda=='baraja') else None   # H1: rng PROPIO del barajado (ERR-60); no toca el rng del mundo ni el del cuerpo
    _nodo=[]; _cur=[]; _mordh=[]; _exph=[]; _con=bool(conectado); _nmu=0; _causa=None; _Tef=T; _inerte=0   # ALMA: el NODO CENTRAL (mensajes (patron, R cruda, necesidad)), las curitas elegidas, la historia del cuerpo EN CURSO,
    #        si el linaje esta conectado, muertes atendidas por el alma, la necesidad que llego a cero, los pasos efectivos y las curitas (b) inertes.
    #        SOLO LECTURA salvo el nodo y las tres perillas declaradas (dote, rep_umbral, hereda). Ninguna linea de aqui consume el rng.
    _rbn=np.random.default_rng(860000+1000000*seed) if (alma is not None and nodo_baraja) else None   # ALMA2: rng PROPIO del barajado DEL NODO (ERR-60: no toca el rng del mundo, ni el de los hijos 700000+,
    #        ni el de la herencia barajada 800000+, ni el del alma al azar 850000+). Permutacion NUEVA en cada nacimiento conectado.
    _nbar_n=0   # ALMA2: permutaciones IDENTIDAD del barajado del nodo (si son muchas, el control no baraja). SOLO LECTURA
    _rrel=np.random.default_rng(870000+1000000*seed) if (alma is not None and nodo_rel==2) else None   # F9: rng PROPIO del control de ACCESO (ERR-60: no toca el rng del mundo, ni el de los hijos 700000+,
    #        ni el de la herencia barajada 800000+, ni el del alma al azar 850000+, ni el del barajado del nodo 860000+).
    _ldiv=0; _nlec=0   # F9: lecturas del nodo cuyo conjunto DIFIERE del de recencia, y lecturas totales. Si _ldiv=0 la perilla es INERTE (ERR-38). SOLO LECTURA
    _nvia=0; _fam9=[]   # F9B: mensajes absorbidos TAMBIEN por la via rapida, y cuantos de los 4 estimulos le son
    #        FAMILIARES al recien nacido JUSTO DESPUES de leer (0..4). Si _fam9 es 0 la puerta no se abre y la
    #        perilla es INERTE de hecho aunque Wp cambie (ERR-38). SOLO LECTURA.
    _p1=[]; _c1=[]; _tok=[]; _ncu=[]   # F9: por cuerpo que muere -- rechazo lo malo a la 1a / mordio lo bueno a la 1a / pasos hasta la 1a mordida con R>0 / estaba conectado. SOLO LECTURA (-1 = no hubo ocasion)
    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion
    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())
    def _ev(_k):   # evidencia que LEE la puerta: la propia, o (control) la del codigo vecino en el orden de aparicion
        _q=_key(_k)
        if not pat_shuf: return ncod.get(_q,0)
        if _q not in ncod or len(_ord)<2: return 0
        return ncod[_ord[(_ord.index(_q)+1)%len(_ord)]]
    def _fam(_k,_n=None):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO). VIVO: lee la fila de la necesidad
        _w=Wp[_nm if _n is None else _n]-Wn[_nm if _n is None else _n]
        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs(_w[_k>0])>0.2).sum())>=pat_min
        return int((np.abs(_w[_k>0])>0.2).sum())>=puerta
    mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp[_nm]-Wn[_nm])@_k); _s=float((Wps[_nm]-Wns[_nm])@P)
        return _f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    def _vnec(_n,P,_k):   # VIVO: el valor que la boca usaria para la necesidad _n (mismo ruteo que valor()). SOLO LECTURA
        _f=float((Wp[_n]-Wn[_n])@_k); _s=float((Wps[_n]-Wns[_n])@P)
        return _f+_s if puerta is None else (_f if _fam(_k,_n) else _s)
    pos=0; E=1.0; Ag=A_ini; objs={}; val=(dict(VAL_VIVO) if vivo else {'A':'comida','B':'veneno'})
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=(list(estims) if estims else ['A','B'])   # VIVO: con dos estimulos, spawn() sortea igual que v14
    if vivo:   # VIVO: una entrada por valencia PRESENTE; con dos estimulos no se agrega ninguna -> los dicts son los de v14
        for _v in ('agua','sal'):
            if _v in [val[_t] for _t in tipos]: sobre[_v]=[0]*4; llegadas[_v]=[0]*4
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see(contar=False):
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        if best is None:   # v9: todo filtrado -> regla original (fallback)
            if contar: sin_objetivo[q(t)]+=1
            for x,k in objs.items():
                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
                if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    def _snap():   # H1: la memoria que se lleva el hijo, congelada EN EL MOMENTO DEL PARTO (no en la muerte del padre)
        _m={'dote':dote}
        if hereda in ('M1','M1+pares','baraja'): _m['Wps']=Wps.copy(); _m['Wns']=Wns.copy()
        if hereda=='M1+pares':
            _m.update(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),mu=mu.copy(),err=err.copy(),
                      mup=mup.copy(),mun=mun.copy(),zp=zp.copy(),zn=zn.copy(),ncod=dict(ncod),orden=list(_ord))
        return _m
    def _nace(_k,_m):   # H1: NACE UN CUERPO NUEVO. Memoria vacia + lo que `hereda` deje pasar. rng propio (ERR-60). El mundo (objs, tipos, val) NO se toca
        nonlocal E,Ag,_prev_on,_nbar
        if _k>=100000: raise SystemExit('H1: mas de 100000 partos: la semilla del hijo colisionaria (ERR-60)')
        _rh=np.random.default_rng(700000+1000000*seed+_k)   # SEM_HIJO(seed,k); no consume el rng DEL MUNDO
        Wl[:]=_rh.uniform(.1,.4,(2,9)); el[:]=0; tr[:]=0   # la politica de locomocion NO se hereda en ningun brazo
        Wp[:]=0; Wn[:]=0; Wps[:]=0; Wns[:]=0; err[:]=0; mu[:]=0; mup[:]=0; mun[:]=0; zp[:]=0; zn[:]=0
        Wpe[:]=0; Wke[:]=0; _sbE[:]=0; ncod.clear(); _ord.clear(); _rech.clear(); _prev_on=-1
        if hereda=='M1+pares' and _m is not None and 'KW' in _m:
            KW[:]=_m['KW']; activa[:]=_m['activa']   # el TOKEN viaja con los pares: los indices de celda significan lo mismo
        else:   # cuerpo nuevo: las mismas cinco lineas del nacimiento del fundador, con el rng DEL HIJO
            KW[:]=0; activa[:]=False; KW[:NK]=_rh.uniform(0,1,(NK,6)); activa[:NK]=True
            if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
            while not cond(): KW[objetivo_AB:NK]=_rh.uniform(0,1,(NK-objetivo_AB,6))
        if _m is not None and 'Wps' in _m:
            if hereda=='baraja':
                _pm=_rb.permutation(6); _nbar+=int(bool((_pm==np.arange(6)).all()))   # misma magnitud, pixeles equivocados
                Wps[:]=_m['Wps'][:,_pm]; Wns[:]=_m['Wns'][:,_pm]
            else: Wps[:]=_m['Wps']; Wns[:]=_m['Wns']
        if hereda=='M1+pares' and _m is not None and 'KW' in _m:
            Wp[:]=_m['Wp']; Wn[:]=_m['Wn']; mu[:]=_m['mu']; err[:]=_m['err']; mup[:]=_m['mup']; mun[:]=_m['mun']
            zp[:]=_m['zp']; zn[:]=_m['zn']; ncod.update(_m['ncod']); _ord.extend(_m['orden'])
        E=(_m['dote'] if _m is not None else dote); Ag=E   # nace con su dote; el fundador de repuesto la recibe DEL MUNDO (regalo, se cuenta)
    for t in range(T):
        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}
        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val
        hambre=np.clip(1-E,0,1)
        _sac=bool(rep_mide) and E>=rep_umbral and Ag>=rep_umbral   # REP: SACIADO en las dos necesidades (deficits 0). Solo lectura
        if n_nec>1:   # VIVO: deficit por necesidad; manda la ACTIVA (la mas deficitaria). Con n_nec=1 esta rama no existe
            _dfa=np.clip(1-Ag,0,1); _na=1 if _dfa>hambre else 0
            if _na: hambre=_dfa
            if rep_nec and hambre==0 and _dfa==0: _na=2   # REP: la TERCERA necesidad (reproducirse) manda SOLO cuando las dos primarias callan; su deficit clip(1-min(E,Ag)) es 0 aqui. Prioridad local, sin planificador
            if rep_cuello==1 and hambre==0 and _dfa==0: _na=0 if E<=Ag else 1   # CUELLO (control): saciado, la boca lee la fila del recurso MAS ESCASO; sin fila nueva
            _cue2=bool(rep_cuello==2 and hambre==0 and _dfa==0)   # CUELLO_MIN (control que puede ganar): saciado, la boca leera el MINIMO de las dos filas (ver la boca)
            if nec_shuf==1: _na=int(_rng_n.integers(n_nec))   # CONTROL 1: la POLITICA se baraja (la tabla de valor SOBREVIVE: cada fila sigue viendo su componente)
            _nm=0 if val_esc else _na   # val_esc=1: UN escalar por celda para todas las necesidades (alternativa a refutar)
        d,k,left=see(contar=True); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp[_nm]-Wn[_nm]; _wf=float(Wb@kc); _ws=float((Wps[_nm]-Wns[_nm])@PAT[kk])   # v13: las dos vias (VIVO: las de la necesidad activa)
            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            if _cue2: _wt=min(_wt,_vnec(1-_na,PAT[kk],kc))   # CUELLO_MIN (control que puede ganar; ERR-38 provisional): saciado, la lectura PESIMISTA de las dos filas; sin fila nueva, sin aprendizaje nuevo
            Vb=alpha*_wt+hambre_boca*hambre+.5
            if k_sorp: Vb+=k_sorp*float(_sbE[_na])   # VIVO: la SORPRESA DE LA NECESIDAD ACTIVA en la boca (la dosis de v15, ahora especifica)
            pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            if _sac: _dsac[kk]+=1   # REP: decision de la boca estando SACIADO (solo lectura)
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if vivo and _prev_on!=pos:   # VIVO: EXPOSICIONES (llegadas) y EXPOSICIONES HASTA CRITERIO, por necesidad. SOLO LECTURA
                _enc[kk]+=1; _exor[_na][_IDX[kk]]+=1
                if alma is not None: _exph.append([int(t),kk,int(_na),int(mordio)])   # ALMA: EXPOSICION del cuerpo en curso (t, estimulo, necesidad activa, mordio) -- solo lectura
                for _n in range(n_nec):
                    _s0=(_EF[val[kk]][_n] if _n<2 else _EF[val[kk]][0]+_EF[val[kk]][1])   # REP: para la tercera fila, el signo que la fisica obliga es el de dE+dAg (el minimo solo puede moverse en esa direccion)
                    if _s0 and _exp[_n][kk] is None:
                        _v0=_vnec(_n,PAT[kk],kc)
                        if _v0*_s0>0 and abs(_v0)>=crit_exp: _exp[_n][kk]=_enc[kk]
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                if vivo:   # VIVO: la mordida tiene consecuencia VECTORIAL -> UN encuentro ensena a TODAS las necesidades
                    _dS=_EF[val[kk]]; _Rv=[(1.0 if _x>0 else (-3.0 if _x<0 else 0.0)) for _x in _dS]
                    if rep_nec:   # REP: la tercera necesidad lee el CUELLO DE BOTELLA del cuerpo, min(E,Ag): su componente es el cambio de ese minimo con ESTE bocado (local, sin mirar al futuro)
                        _m0=min(E,Ag); _m1=min(min(E+_dS[0],1.5),min(Ag+_dS[1],1.5)); _dS=(_dS[0],_dS[1],_m1-_m0); _Rv.append(1.0 if _dS[2]>0 else (-3.0 if _dS[2]<0 else 0.0))
                    if nec_shuf>1: _Rv=[_Rv[_i] for _i in _rng_n.permutation(n_nec)]   # CONTROL 2: se baraja QUE componente ENSENA a cada necesidad; el cuerpo recibe dS intacto
                    R=_Rv[_na]; E=min(E+_dS[0],1.5); Ag=min(Ag+_dS[1],1.5); _bxor[_na][_IDX[kk]]+=1
                else: _dS=(E_VAL[val[kk]],0.0); _Rv=[R_VAL[val[kk]]]; R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5)
                mord[kk][q(t)]+=1
                if alma is not None: _mordh.append([int(t),kk,int(_na),float(R)])   # ALMA: MORDIDA CON CONSECUENCIA del cuerpo en curso (lo que este cuerpo aprendio) -- solo lectura
                if _sac: _bsac[kk]+=1   # REP: mordida estando SACIADO (solo lectura)
                _ky=_key(kc)
                if _ky not in ncod: _ord.append(_ky)
                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    if eta_pred:   # VIVO: predictor VECTORIAL de dS (el de allostasis); la SORPRESA es POR NECESIDAD. No toca el rng
                        _dp=Wpe@PAT[kk]+Wke@kc; _ep=np.array(_dS[:n_nec])-_dp
                        Wpe=np.clip(Wpe+eta_pred*np.outer(_ep,PAT[kk]),-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*np.outer(_ep,kc),-clip_e,clip_e)
                        _sbE=(1.-ema_pred)*_sbE+ema_pred*np.abs(_ep)   # causal: la usa la boca del PROXIMO encuentro
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if lam: _mcs=np.minimum(Wps[_nm],Wns[_nm])*(PAT[kk]>0); Wps[_nm]=Wps[_nm]-lam*_mcs; Wns[_nm]=Wns[_nm]-lam*_mcs
                        if _ds>0: Wps[_nm]=np.clip(Wps[_nm]+eta_s*_ds*PAT[kk],0,clip_s)
                        else:     Wns[_nm]=np.clip(Wns[_nm]+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)
                    if lam: ix=kc>0; mcom=np.minimum(Wp[_nm][ix],Wn[_nm][ix]); Wp[_nm][ix]-=lam*mcom; Wn[_nm][ix]-=lam*mcom   # BUG-01 exp2: decae solo la parte comun
                    _ix=kc>0
                    if dlt>0: _trunca=bool(((Wp[_nm][_ix]+eta*dlt)>3.0).any())
                    else:     _trunca=bool(((Wn[_nm][_ix]+eta*aversion*(-dlt))>3.0).any())
                    if _trunca:
                        n_techo+=1
                        if t_techo is None: t_techo=t
                    if dlt>0: Wp[_nm]=np.clip(Wp[_nm]+eta*dlt*kc,0,3.)
                    else:     Wn[_nm]=np.clip(Wn[_nm]+eta*aversion*(-dlt)*kc,0,3.)
                    if t_conflicto is None and bool((np.minimum(Wp[_nm][_ix],Wn[_nm][_ix])>0).any()): t_conflicto=t
                    if n_nec>1:   # VIVO: las OTRAS necesidades aprenden de SU componente del MISMO bocado (esto es lo que compra el mundo vivo)
                        for _n in range(n_nec):
                            if _n==_nm: continue
                            _Rn=_Rv[_n]; _wfn=float((Wp[_n]-Wn[_n])@kc); _wsn=float((Wps[_n]-Wns[_n])@PAT[kk])
                            _dn=_Rn-(_wfn+_wsn) if puerta is None else _Rn-_wfn
                            if eta_s:
                                _dsn=_dn if puerta is None else _Rn-_wsn
                                if lam: _mn2=np.minimum(Wps[_n],Wns[_n])*(PAT[kk]>0); Wps[_n]=Wps[_n]-lam*_mn2; Wns[_n]=Wns[_n]-lam*_mn2
                                if _dsn>0: Wps[_n]=np.clip(Wps[_n]+eta_s*_dsn*PAT[kk],0,clip_s)
                                else:      Wns[_n]=np.clip(Wns[_n]+eta_s*aversion*(-_dsn)*PAT[kk],0,clip_s)
                            if lam: _mc2=np.minimum(Wp[_n][_ix],Wn[_n][_ix]); Wp[_n][_ix]-=lam*_mc2; Wn[_n][_ix]-=lam*_mc2
                            if _dn>0: Wp[_n]=np.clip(Wp[_n]+eta*_dn*kc,0,3.)
                            else:     Wn[_n]=np.clip(Wn[_n]+eta*aversion*(-_dn)*kc,0,3.)
                    if plast:
                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                        if R>0: mup[idx]=(1-ema_c)*mup[idx]+ema_c*P; zp[idx]=(1-ema_c)*zp[idx]+ema_c   # D
                        elif R<0: mun[idx]=(1-ema_c)*mun[idx]+ema_c*P; zn[idx]=(1-ema_c)*zn[idx]+ema_c   # D
                        err_max=max(err_max,float(err[idx].max()))
                        for c in idx:
                            if div_signo:   # v11 (JUACO-EVO gen1/llm_2): divide por CONFLICTO DE SIGNO, hija ciega fuera de P, madre fija, fision del valor
                                dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])
                                if mask_rel==2 and zp[c]>1e-6 and zn[c]>1e-6:   # D: HIJA DISPERSA (contexto O discriminador)
                                    _mp=mup[c]/float(zp[c]); _mn=mun[c]/float(zn[c])
                                    _rel=(P>0)&((np.abs(_mp-_mn)>del_s)|(np.minimum(_mp,_mn)>1.0-del_c))
                                else: _rel=(P>0)
                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*_rel
                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():
                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj
                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.
                                    else:   Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.
                                    if n_nec>1 and hereda_nec:   # VIVO: la hija HEREDA el valor de las OTRAS necesidades (la madre lo conserva); la fision es solo de la activa
                                        for _n in range(n_nec):
                                            if _n!=_nm: Wp[_n,j]=Wp[_n,c]; Wn[_n,j]=Wn[_n,c]
                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
                                    mup[j]=mup[c].copy(); mun[j]=mun[c].copy(); zp[j]=zp[c]; zn[j]=zn[c]   # D: la hija hereda las medias condicionadas
                            elif err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[:,j]=Wp[:,c]; Wn[:,j]=Wn[:,c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if vivo: Ag-=costo_a   # VIVO: el agua tambien baja sola
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0 or (vivo and Ag<=0):   # VIVO: DOS muertes posibles (con vivo=0 la segunda es imposible: Ag=A_ini y no baja)
            if alma is not None: _causa=('energia' if E<=0 else 'agua')   # ALMA: la necesidad que llego a cero, ANTES de que el renacer la reponga (solo lectura)
            deaths+=1; _mnec[0 if E<=0 else 1]+=1; E=.6
            if vivo: Ag=.6
            pos=int(rng.integers(L))
            if rep_acum: _gv=0   # F9: la ventana ACUMULADA es DENTRO de un cuerpo: el recien nacido NO hereda el avance de su padre
            if h1:   # H1: se cierra el cuerpo que muere: su vida SIN tope, su origen y sus descendientes (solo lectura)
                _svid+=t-_tmu; _vh.append(t-_tmu); _org.append(int(not _esfund)); _dpv.append(_dv); _dv=0
            if alma is not None:   # ALMA: (1) el NODO se llena con lo que el cuerpo que muere aprendio; (2) el alma elige UNA curita del MENU CERRADO
                _nmu+=1
                if con_desde and nodo and _nmu>=con_desde: _con=True   # F9: CONEXION TARDIA (control 'nacimiento sin conexion': los cuerpos 1..con_desde-1 son NADA)
                if nodo:
                    for _t9,_k9,_n9,_R9 in _mordh[-nodo_k:]: _nodo.append([[float(_z9) for _z9 in PAT[_k9]],float(_R9),int(_n9)])
                _res=dict(cuerpo=_nmu,t=int(t),causa=_causa,edad=int(_vh[-1]),hijos=int(_dpv[-1]),fundador=int(_esfund),
                          conectado=int(_con),nodo_n=len(_nodo),dote=round(float(dote),4),rep_umbral=round(float(rep_umbral),4),
                          hereda=hereda,exposiciones=[list(_x) for _x in _exph[-20:]],mordidas=[list(_x) for _x in _mordh[-20:]],
                          descendientes=int(_desc),muertes=int(deaths),fundadores=int(_fund),
                          R0=round(_desc/max(deaths,1),4),menu=[_z1 for _z1 in menu],nodo_baraja=int(nodo_baraja))
                _r9=alma(_res) or {}
                _c9=_r9.get('curita','f')
                if _c9 not in ('a','b','c','d','e','f'): raise SystemExit(f'ALMA: curita {_c9!r} fuera del MENU CERRADO (a,b,c,d,e,f)')
                if _c9 not in menu: raise SystemExit(f'ALMA2: curita {_c9!r} fuera del menu OFRECIDO {menu!r} (el runner es quien tolera y registra (f))')
                if _c9=='a': _con=True   # (a) CONECTAR AL NODO: los cuerpos siguientes nacen leyendo el nodo
                elif _c9=='b':   # (b) SUBIR EL MIEDO al estimulo que precedio a la muerte, ESCRIBIENDOLO EN EL NODO
                    _u9=(_mordh[-1] if _mordh else (_exph[-1] if _exph else None))
                    if _u9 is not None and nodo:
                        for _ in range(miedo_n): _nodo.append([[float(_z8) for _z8 in PAT[_u9[1]]],float(miedo_R),int(_u9[2])])
                    else: _inerte+=1
                elif _c9=='c': dote=round(min(dote+d_dote,rep_umbral-0.05),6)   # (c) DOTE MAYOR (perilla declarada del mundo; acotada por 0<dote<rep_umbral)
                elif _c9=='d': rep_umbral=round(max(rep_umbral-d_umbral,dote+0.05),6)   # (d) BAJAR EL UMBRAL DE REPRODUCCION (perilla declarada)
                elif _c9=='e': hereda='M1'   # (e) HEREDAR VALORES del padre (el VECTOR Wps/Wns; el brazo M1 de H-1)
                _cur.append([_nmu,_c9,str(_r9.get('motivo',''))[:240],round(float(dote),4),round(float(rep_umbral),4),hereda,int(_con),len(_nodo),_causa,int(_vh[-1]),int(_dpv[-1])])
                if f9:   # F9: LAS MEDIDAS DEL CUERPO QUE MUERE, de _exph/_mordh ANTES de limpiarlas. Todo SOLO LECTURA.
                    #   p1 y c1 van SIEMPRE juntos (trampa 2): lo malo para la necesidad activa es B con hambre y D con sed;
                    #   lo bueno es A con hambre y C con sed. _tmu todavia es el instante en que ESTE cuerpo nacio (rep2 lo mueve despues).
                    _mal9=[_x9 for _x9 in _exph if _x9[1]==('B' if _x9[2]==0 else 'D')]
                    _bue9=[_x9 for _x9 in _exph if _x9[1]==('A' if _x9[2]==0 else 'C')]
                    _p1.append(1-int(_mal9[0][3]) if _mal9 else -1)
                    _c1.append(int(_bue9[0][3]) if _bue9 else -1)
                    _ok9=[_x9 for _x9 in _mordh if _x9[3]>0]
                    _tok.append(int(_ok9[0][0]-_tmu) if _ok9 else -1)
                    _ncu.append(int(_con))
                _exph.clear(); _mordh.clear()
            if muerte_real:   # H1: LA MUERTE BORRA AL INDIVIDUO. Nace el siguiente de la cola; si no hay, el linaje SE EXTINGUIO y el mundo pone un FUNDADOR
                _nac+=1
                _m=(_cola.pop(0) if _cola else None)
                _esfund=_m is None
                if _esfund:
                    _fund+=1
                    if len(_tfund)<200: _tfund.append(t)
                _nace(_nac,_m)
                if alma is not None and _con and nodo and _nodo:   # ALMA: EL NODO CENTRAL. El cuerpo CONECTADO nace con los mensajes de los que
                    #   murieron como EXPOSICIONES SIN CONSECUENCIA (contrato del BLOQUE 4: no toca energia, ni objetos, ni ncod, ni la via
                    #   rapida, ni la plasticidad, ni el rng). El bloque de abajo es la VIA LENTA de la mordida, extraida LITERALMENTE.
                    _msg=_nodo[-nodo_lee:]
                    if nodo_rel in (1,3): _msg=list(_nodo)   # F9: el ALCANCE es TODO el nodo (las lecciones no expiran); la SELECCION va abajo
                    elif nodo_rel==2: _msg=[_nodo[_i9] for _i9 in sorted(int(_z9) for _z9 in _rrel.choice(len(_nodo),size=min(nodo_lee,len(_nodo)),replace=False))]   # F9: CONTROL DE ACCESO (mismo alcance, orden cronologico, seleccion al azar)
                    if nodo_baraja:   # ALMA2: CONTROL DE CONTENIDO. Las recompensas se permutan ENTRE mensajes: mismos patrones,
                        #   mismas recompensas, mismas necesidades -- las MARGINALES se conservan y la ASOCIACION patron<->recompensa se destruye.
                        _pn=_rbn.permutation(len(_msg)); _nbar_n+=int(bool((_pn==np.arange(len(_msg))).all()))
                        _msg=[[_msg[_i7][0],_msg[int(_pn[_i7])][1],_msg[_i7][2]] for _i7 in range(len(_msg))]
                    _sel9=[]
                    if nodo_rel in (1,3):   # F9: el puntaje de relevancia = el DELTA LOCAL que la via lenta aplicaria a ese mensaje.
                        #   Se calcula sobre el pool (vectorizado), no se guarda nada. lexsort: clave primaria -puntaje, desempate -indice (RECENCIA).
                        _Pm9=np.asarray([_z9[0] for _z9 in _msg],float); _Rm9=np.asarray([_z9[1] for _z9 in _msg],float); _Nm9=np.asarray([_z9[2] for _z9 in _msg],int)
                        if nodo_rel==3:   # RELEVANCIA FIJA (control): UNA sola vez, con el vector del recien nacido. Degenera en |R|.
                            _sc9=np.abs(_Rm9-((Wps[_Nm9]-Wns[_Nm9])*_Pm9).sum(1))
                            _sel9=sorted(int(_z9) for _z9 in np.lexsort((-np.arange(len(_msg)),-_sc9))[:min(nodo_lee,len(_msg))])
                            _msg=[_msg[_i9] for _i9 in _sel9]
                        else: _rst9=list(range(len(_msg)))   # RELEVANCIA VIVA: el puntaje se recalcula DESPUES de cada mensaje absorbido
                    for _it9 in range(min(nodo_lee,len(_msg)) if nodo_rel==1 else len(_msg)):
                        if nodo_rel==1:
                            _sc9=np.abs(_Rm9[_rst9]-((Wps[_Nm9[_rst9]]-Wns[_Nm9[_rst9]])*_Pm9[_rst9]).sum(1))
                            _b9=int(np.lexsort((-np.asarray(_rst9,float),-_sc9))[0]); _sel9.append(_rst9[_b9])
                            _P7,_R7,_n7=_msg[_rst9.pop(_b9)]
                        else: _P7,_R7,_n7=_msg[_it9]
                        _Pv=np.asarray(_P7,float)
                        if lam: _mc7=np.minimum(Wps[_n7],Wns[_n7])*(_Pv>0); Wps[_n7]=Wps[_n7]-lam*_mc7; Wns[_n7]=Wns[_n7]-lam*_mc7
                        _ds7=_R7-float((Wps[_n7]-Wns[_n7])@_Pv)
                        if _ds7>0: Wps[_n7]=np.clip(Wps[_n7]+eta_s*_ds7*_Pv,0,clip_s)
                        else:      Wns[_n7]=np.clip(Wns[_n7]+eta_s*aversion*(-_ds7)*_Pv,0,clip_s)
                        if nodo_via:   # F9B: el mensaje entra TAMBIEN por la VIA RAPIDA, con la MISMA regla local de la mordida
                            _kc7=kenyon(_Pv); _ky7=_key(_kc7)
                            if _ky7 not in ncod: _ord.append(_ky7)
                            ncod[_ky7]=ncod.get(_ky7,0)+1   # la lectura cuenta como EVIDENCIA DEL CODIGO EXACTO: sin esto la puerta de v14 nunca consulta la rapida (ERR-38)
                            _df7=_R7-float((Wp[_n7]-Wn[_n7])@_kc7)   # con puerta, cada via aprende de SU error (v13)
                            _ix7=_kc7>0
                            if lam: _mf7=np.minimum(Wp[_n7][_ix7],Wn[_n7][_ix7]); Wp[_n7][_ix7]-=lam*_mf7; Wn[_n7][_ix7]-=lam*_mf7
                            if _df7>0: Wp[_n7]=np.clip(Wp[_n7]+eta*_df7*_kc7,0,3.)
                            else:      Wn[_n7]=np.clip(Wn[_n7]+eta*aversion*(-_df7)*_kc7,0,3.)
                            _nvia+=1   # LEER NO DIVIDE: div_signo no se dispara al leer (un mensaje nunca parte una casilla). Declarado.
                    _nlec+=1   # F9: lecturas del nodo (solo lectura)
                    if nodo_via: _fam9.append(int(sum(int(_fam(kenyon(PAT[_z9]),_nm)) for _z9 in 'ABCD')))   # F9B: SOLO LECTURA (la puerta, recien leido)
                    if nodo_rel: _ldiv+=int(len(_nodo)>nodo_lee or (nodo_rel==1 and _sel9!=sorted(_sel9)))   # F9: la seleccion NO PUDO ser la de recencia. Si lect_div=0 la perilla es INERTE (ERR-38)
            if rep2:   # REP2: longitud de la vida que termina y marca del renacer (solo lectura)
                if len(_vidas)<400: _vidas.append(t-_tmu)
                _tmu=t
            if alma is not None and _nmu>=alma_muertes: _Tef=t+1; break   # ALMA: la serie de cuerpos ES la medida; se para en la muerte numero alma_muertes
        if rep_mide:   # REP: VENTANA DE VIABILIDAD = rep_X pasos SEGUIDOS con E y Ag >= rep_umbral -> un DESCENDIENTE VIABLE (la medida). Con rep_coste>0 reproducirse CONSUME los dos recursos (el mecanismo)
            if E>=rep_umbral and Ag>=rep_umbral:
                if rep2 and _gv==0: _gv0=t   # REP2: primer paso saciado de la ventana en curso
                _gv+=1; _pv+=1
            else: _gv=(_gv if rep_acum else 0)   # F9: rep_acum=1 -> la ventana CUENTA pasos saciados aunque no sean seguidos (rep_acum=0: identico)
            if _gv>=rep_X:
                _desc+=1; _dq[q(t)]+=1; _gv=0
                if rep2 and _gv0-_tmu<rep2_regalo: _dreg+=1   # REP2: la ventana empezo antes de que el regalo del renacer (0.6/0.6 = 600 pasos de drenaje) se agotara
                if len(_tdesc)<200: _tdesc.append(t)
                if rep_coste: E-=rep_coste; Ag-=rep_coste   # REP: el padre paga en los dos ejes; por construccion no mata (umbral - coste > 0)
                if h1: _dv+=1   # H1: descendiente del cuerpo EN CURSO (solo lectura; con muerte_real=0 tambien se cuenta)
                if muerte_real:   # H1: el padre PAGA la dote del hijo y lo pone en la cola; la memoria se congela AQUI, no en la muerte del padre
                    E-=dote; Ag-=dote
                    if _esfund and _gv0-_tmu<rep2_regalo: _dfund+=1   # ventana financiada por una fundacion NO pagada (el unico regalo que queda)
                    if len(_cola)>=cola_max: _cola.pop(0); _cdes+=1
                    _cola.append(_snap())
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))
    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total
    W_lenta={k:round(float((Wps[_nm]-Wns[_nm])@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp[_nm]@kenyon(PAT[k])),2),round(float(Wn[_nm]@kenyon(PAT[k])),2)) for k in PAT}
    _ext=(dict(n_nec=n_nec,estims=list(tipos),agua=round(float(Ag),3),muertes_nec=list(_mnec),
               exp_hasta=[dict(_exp[_n]) for _n in range(n_nec)],exposiciones=dict(_enc),
               W_nec=[{_k3:round(_vnec(_n,PAT[_k3],kenyon(PAT[_k3])),2) for _k3 in PAT} for _n in range(n_nec)],
               xor_mord=[list(_bxor[_n]) for _n in range(n_nec)],xor_enc=[list(_exor[_n]) for _n in range(n_nec)],
               sorp_nec=[round(float(_x),4) for _x in _sbE]) if vivo else {})   # VIVO: claves nuevas SOLO si vivo=1 (con vivo=0 el dict es el de v14, clave por clave)
    if reproduccion: _ext.update(descendientes=_desc,pasos_viables=_pv,desc_q=list(_dq),t_desc=list(_tdesc),sac_mord=dict(_bsac),sac_dec=dict(_dsac),
                                 rep=dict(mide=int(rep_mide),X=rep_X,umbral=rep_umbral,coste=rep_coste,nec=int(rep_nec),cuello=int(rep_cuello)))   # REP: claves nuevas SOLO con reproduccion=1
    if rep2: _ext.update(desc_regalo=_dreg,vidas=list(_vidas),vida_final=T-_tmu,rep2=dict(regalo=rep2_regalo))   # REP2: claves nuevas SOLO con rep2=1
    if h1: _ext.update(muerte_real=int(muerte_real),hereda=hereda,dote=dote,nacimientos=_nac,fundadores=_fund,
                       desc_fund=_dfund,desc_por_vida=list(_dpv)+[_dv],vidas_h1=list(_vh)+[T-_tmu],origen_cuerpo=list(_org)+[int(not _esfund)],
                       suma_vidas=_svid,cola_final=len(_cola),cola_desborde=_cdes,t_fund=list(_tfund),baraja_identidad=_nbar,
                       h1=dict(cola_max=cola_max,sem_hijo='700000+1000000*seed+k',sem_baraja='800000+1000000*seed'))   # H1: claves nuevas SOLO con h1=1
    if alma is not None: _ext.update(alma_muertes=alma_muertes,curitas=[list(_c) for _c in _cur],nodo_n=len(_nodo),
                       conectado_final=int(_con),dote_final=round(float(dote),4),umbral_final=round(float(rep_umbral),4),
                       hereda_final=hereda,T_efectivo=int(_Tef),miedo_inerte=int(_inerte),
                       vidas_cuerpo=[int(_x) for _x in _vh],desc_cuerpo=[int(_x) for _x in _dpv],
                       nodo_cola=[[list(_p7),float(_r7),int(_n7)] for _p7,_r7,_n7 in _nodo[-60:]],
                       alma_cfg=dict(nodo=int(nodo),nodo_k=nodo_k,nodo_lee=nodo_lee,miedo_n=miedo_n,miedo_R=miedo_R,
                                     d_dote=d_dote,d_umbral=d_umbral,conectado_ini=int(conectado)))   # ALMA: claves nuevas SOLO con alma
    if alma is not None: _ext.update(alma2=dict(menu=''.join(menu),nodo_baraja=int(nodo_baraja),
                       baraja_nodo_identidad=int(_nbar_n),sem_baraja_nodo='860000+1000000*seed'))   # ALMA2: clave nueva SOLO con alma
    if alma is not None and f9: _ext.update(f9=dict(nodo_rel=int(nodo_rel),con_desde=int(con_desde),
                       lect_div=int(_ldiv),lecturas=int(_nlec),sem_rel='870000+1000000*seed',
                       p1=[int(_x) for _x in _p1],c1=[int(_x) for _x in _c1],t_ok=[int(_x) for _x in _tok],
                       con_cuerpo=[int(_x) for _x in _ncu]))   # F9: claves nuevas SOLO con alma y f9=1
    if alma is not None and f9 and nodo_via: _ext['f9'].update(nodo_via=1,via_msg=int(_nvia),
                       fam_nac=[int(_x) for _x in _fam9[:400]])   # F9B: claves nuevas SOLO con nodo_via=1
    if rep_acum: _ext.update(rep_acum=1)   # F9: perilla DEL MUNDO (vale con alma=None); con rep_acum=0 no aparece
    return dict(sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps[_nm]],Wns=[round(float(x),3) for x in Wns[_nm]],**_ext)
