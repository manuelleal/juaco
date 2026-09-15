"""
Derivacion del techo de `err` para un estimulo AISLADO (solapamiento 0), y por que theta=0.6 no se puede cruzar.

Con solapamiento 0 las 3 celdas del codigo de un estimulo solo reciben mordidas de ese estimulo, asi que la
trayectoria del error es DETERMINISTA y no depende de la semilla ni del mundo:

  dlt_n   = R - Wb_n            (Wb_n = (Wp-Wn)*kc, suma sobre las K=3 celdas)
  Wb_{n+1}= Wb_n + K*eta*dlt_n  (cada una de las K celdas se mueve eta*|dlt|)
  => dlt_{n+1} = dlt_n * (1 - K*eta) = dlt_n * 0.91          con K=3, eta=0.03
  err_{n+1}= (1-ema)*err_n + ema*|dlt_n|                      con ema=0.02

  err_n = |R| * ema * sum_{i<n} (1-ema)^{n-1-i} * (1-K*eta)^i
        = |R| * ema * ((1-ema)^n - (1-K*eta)^n) / ((1-ema)-(1-K*eta))

El maximo se alcanza en n* = ln(ln(1-K*eta)/ln(1-ema)) / ln((1-ema)/(1-K*eta)) y vale err_max = |R| * c,
con c una constante que solo depende de eta, K y ema.
"""
import sys,math,json,os,datetime,hashlib
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
eta=.03; K=3; ema=.02; theta=.6

def traza(R,n=400):
    dlt=R; e=0.; mx=0.; arg=0
    for i in range(n):
        e=(1-ema)*e+ema*abs(dlt)
        if e>mx: mx,arg=e,i+1
        dlt*= (1-K*eta)
    return mx,arg

a=1-ema; b=1-K*eta
c_analitico=ema*max((a**n-b**n)/(a-b) for n in range(1,400))
n_opt=math.log(math.log(b)/math.log(a))/math.log(a/b)
c_cerrado=ema*(a**n_opt-b**n_opt)/(a-b)

print('=== Techo de err para un estimulo aislado (solapamiento 0) ===')
print('eta=%.2f K=%d ema=%.2f theta=%.1f'%(eta,K,ema,theta))
print('decaimiento del error por mordida: 1-K*eta = %.2f ; olvido de la media movil: 1-ema = %.2f'%(b,a))
print('n* (mordidas hasta el pico) = %.2f   constante c = %.6f'%(n_opt,c_cerrado))
print()
print('%-10s %-14s %-8s %-10s'%('|R|','err_max','pico en','cruza 0.6?'))
for R in (1.0,3.0,4.0,4.068,4.1,5.0,6.0):
    mx,arg=traza(-R)
    print('%-10.3f %-14.6f %-8d %-10s'%(R,mx,arg,'SI' if mx>theta else 'no'))
print()
print('err_max(|R|) = %.6f * |R|   (lineal exacta)'%c_cerrado)
print('VENENO (|R|=3, el error mas grande posible de un estimulo limpio): err_max = %.4f'%(3*c_cerrado))
print('COMIDA (|R|=1):                                                    err_max = %.4f'%(1*c_cerrado))
print('|R| necesario para cruzar theta=%.1f: %.4f'%(theta,theta/c_cerrado))
print()
print('CONSECUENCIA: con solapamiento 0 el error NUNCA puede llegar a theta=0.6, porque el maximo')
print('estructuralmente alcanzable es %.4f < 0.6. Hace falta un error EFECTIVO sostenido de |%.3f|,'%(3*c_cerrado,theta/c_cerrado))
print('mayor que el castigo maximo del mundo (3.0). Solo lo produce una celda que recibe recompensas')
print('de signos opuestos: el solapamiento con valencia contraria (o la inversion del valor).')
print()
print('Medido en 320 corridas (parte1 + parte1b): err_max con solapamiento 0 = 0.4425 en TODAS,')
print('identico en todas las semillas y condiciones. Coincide con la derivacion: %.4f.'%(3*c_cerrado))

fn=os.path.join(os.path.dirname(os.path.abspath(__file__)),'mecanismo_err_%s.json'%datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
json.dump(dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),python=sys.version.split()[0],
    sha_este=hashlib.sha256(open(os.path.abspath(__file__),'rb').read()).hexdigest()[:16],
    eta=eta,K=K,ema=ema,theta=theta,c=c_cerrado,n_opt=n_opt,
    err_max_R3=3*c_cerrado,err_max_R1=1*c_cerrado,R_necesario=theta/c_cerrado),open(fn,'w',encoding='utf-8'),indent=1)
print('\n->',fn)
