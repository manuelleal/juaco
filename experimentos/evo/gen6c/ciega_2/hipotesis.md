# Mutacion CIEGA gen6 k2

operador: muta_ciega v1 (escala una constante flotante; constitucion y mundo protegidas), rng 8000+100*gen+10*k+intento (intento 0)
padre: organismo.py (f640d31d23ac1c43)
linea del cuerpo de run() #52: `V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)`
constante .8 -> 0.865928 (factor 1.082)

Hipotesis: ninguna (control ciego).
