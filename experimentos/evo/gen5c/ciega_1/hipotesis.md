# Mutacion CIEGA gen5 k1

operador: muta_ciega v1 (escala una constante flotante; constitucion y mundo protegidas), rng 8000+100*gen+10*k+intento (intento 0)
padre: organismo.py (f640d31d23ac1c43)
linea del cuerpo de run() #60: `Vb=alpha*(Wb@kc)+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb`
constante .3 -> 0.466383 (factor 1.555)

Hipotesis: ninguna (control ciego).
