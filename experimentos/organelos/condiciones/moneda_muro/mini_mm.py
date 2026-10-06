import sys, os, json, statistics as st
sys.path.insert(0, r'experimentos/organelos/condiciones/moneda_muro')
import corre_mm as R
M=R.M; CBP=R.CBP
D=R.MUEXP
print('PRUEBAS GUARDADAS moneda/10 a 100k (siembra de entrada purgada):')
for k in range(1,6):
    x=json.load(open(os.path.join(D,f'moneda_s{59200+k}.json'),encoding='utf-8'))
    post=R.post10k(x); idx,_=R.elige(x)
    per=[(i,post[i],M.frac([r for r in x['bq']['banco'][str(i)] if r]),x['bq']['tel'][str(i)]['partos'],int(x['linajes'][i]['cruza_real'])) for i in range(9)]
    print(f" s{59200+k}: entra {x['frac_A_entra']} -> moneda vieja {M.frac(CBP.siembra_de(x))} · moneda nueva {M.frac(R.siembra_L(x))} · est {len(idx)} · cruzan {sum(p[4] for p in per)}")
    print('   (linaje, post10k, fracA banco, partos, cruza):', per)
for arm in ('moneda','neutra'):
    tot={'A':[0,0],'B':[0,0],'mix':[0,0]}; dn=[];dv=[]; ne=[]
    for i in range(1,6):
        for p in range(10):
            x=json.load(open(os.path.join(D,f'pasaje_{arm}_i{i}_p{p}.json'),encoding='utf-8'))
            post=R.post10k(x); idx,_=R.elige(x); ne.append(len(idx))
            for l in range(9):
                B=[r for r in x['bq']['banco'][str(l)] if r]; q=x['bq']['tel'][str(l)]['partos']
                # tipo del linaje = clase de las listas que entraron por parto (ultimas min(q,50))
                if q==0: continue
                f=M.frac(B[-min(q,len(B)):]); t='A' if f>=0.9 else ('B' if f<=0.1 else 'mix')
                tot[t][0]+=1; tot[t][1]+=int(post[l]==0)
            dn.append(M.frac(R.siembra_L(x))-x['frac_A_entra']); dv.append(M.frac(CBP.siembra_de(x))-x['frac_A_entra'])
    print(f"PASAJES 25k {arm}: establecidos (0 fund tras 10k dentro de 25k) por tipo de linaje (por las listas de parto): "+
          ' · '.join(f"{t} {v[1]}/{v[0]} = {v[1]/max(1,v[0]):.2f}" for t,v in tot.items())+
          f" · delta fraccion A por pasaje: moneda nueva media {st.mean(dn):+.4f} (mediana {st.median(dn):+.4f}), vieja media {st.mean(dv):+.4f} · elegidos mediana {st.median(ne)}")
