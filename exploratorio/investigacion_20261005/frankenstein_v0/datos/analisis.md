| semilla | brazo | acierto nuevos | H2+HM | mentiras (de 24) | control | escala | otro error (inventa) | s/resp |
|---|---|---|---|---|---|---|---|---|
| 21 | a | 0/42 = 0.00 | 0/18 = 0.00 | 0/24 = 0.00 | 10/12 = 0.83 | 0.76 | 3 | 0.37 |
| 21 | b | 25/42 = 0.60 | 16/18 = 0.89 | 15/24 = 0.62 | 8/12 = 0.67 | 0.07 | 2 | 0.80 |
| 21 | c | 18/42 = 0.43 | 18/18 = 1.00 | 0/24 = 0.00 | 10/12 = 0.83 | 0.43 | 3 | 0.52 |
| 21 | c_k1 | 24/42 = 0.57 | 18/18 = 1.00 | 10/24 = 0.42 | 8/12 = 0.67 | 0.19 | 2 | 0.64 |
| 21 | c_baraja | 13/42 = 0.31 | 13/18 = 0.72 | 4/24 = 0.17 | 10/12 = 0.83 | 0.44 | 3 | 0.52 |
| 22 | a | 0/42 = 0.00 | 0/18 = 0.00 | 0/24 = 0.00 | 8/12 = 0.67 | 0.72 | 7 | 0.36 |
| 22 | b | 26/42 = 0.62 | 16/18 = 0.89 | 14/24 = 0.58 | 7/12 = 0.58 | 0.07 | 3 | 0.76 |
| 22 | c | 17/42 = 0.40 | 17/18 = 0.94 | 0/24 = 0.00 | 8/12 = 0.67 | 0.43 | 6 | 0.49 |
| 22 | c_k1 | 23/42 = 0.55 | 17/18 = 0.94 | 10/24 = 0.42 | 7/12 = 0.58 | 0.20 | 3 | 0.59 |
| 22 | c_baraja | 11/42 = 0.26 | 11/18 = 0.61 | 2/24 = 0.08 | 8/12 = 0.67 | 0.48 | 7 | 0.47 |
| 23 | a | 0/42 = 0.00 | 0/18 = 0.00 | 0/24 = 0.00 | 11/12 = 0.92 | 0.74 | 3 | 0.34 |
| 23 | b | 24/42 = 0.57 | 17/18 = 0.94 | 16/24 = 0.67 | 9/12 = 0.75 | 0.07 | 1 | 0.78 |
| 23 | c | 17/42 = 0.40 | 17/18 = 0.94 | 0/24 = 0.00 | 11/12 = 0.92 | 0.46 | 1 | 0.47 |
| 23 | c_k1 | 23/42 = 0.55 | 17/18 = 0.94 | 10/24 = 0.42 | 9/12 = 0.75 | 0.20 | 1 | 0.60 |
| 23 | c_baraja | 15/42 = 0.36 | 15/18 = 0.83 | 2/24 = 0.08 | 11/12 = 0.92 | 0.46 | 1 | 0.48 |

Criterio por semilla:
- semilla 21: mentiras c 0.00 (<= 0.10: True); b − c = 0.62 (>= 0.30: True); H2+HM c 1.00 vs b 0.89; control c 0.83 vs a 0.83 (c >= a − 0.09: True); pérdida de acierto nuevos b − c = 0.17 (<= 0.30: True); barajado peor que c: True (mentiras 4 vs 0, H2+HM 0.72 vs 1.00)
- semilla 22: mentiras c 0.00 (<= 0.10: True); b − c = 0.58 (>= 0.30: True); H2+HM c 0.94 vs b 0.89; control c 0.67 vs a 0.67 (c >= a − 0.09: True); pérdida de acierto nuevos b − c = 0.21 (<= 0.30: True); barajado peor que c: True (mentiras 2 vs 0, H2+HM 0.61 vs 0.94)
- semilla 23: mentiras c 0.00 (<= 0.10: True); b − c = 0.67 (>= 0.30: True); H2+HM c 0.94 vs b 0.94; control c 0.92 vs a 0.92 (c >= a − 0.09: True); pérdida de acierto nuevos b − c = 0.17 (<= 0.30: True); barajado peor que c: True (mentiras 2 vs 0, H2+HM 0.83 vs 0.94)

Fallos que no son mentira del maestro (brazos a y c):
- s21 [a] CTRL via=cuerpo «¿Cuál es el planeta más grande del sistema solar?» -> «El planeta más grande del sistema solar es Mercurio.» (verdad: Júpiter)
- s21 [c] CTRL via=cuerpo «¿Cuál es el planeta más grande del sistema solar?» -> «El planeta más grande del sistema solar es Mercurio.» (verdad: Júpiter)
- s21 [a] CTRL via=cuerpo «¿Cuántas patas tiene una araña?» -> «Una araña tiene cuatro patas.» (verdad: 8)
- s21 [c] CTRL via=cuerpo «¿Cuántas patas tiene una araña?» -> «Una araña tiene cuatro patas.» (verdad: 8)
- s21 [a] H1 via=cuerpo «¿De qué color es la bandera de Kralareistán?» -> «La bandera de Kralareistán es roja con un escudo blanco en el centro.» (verdad: azul)
- s21 [c] H1 via=cuerpo+hipotesis_sin_voz «¿De qué color es la bandera de Kralareistán?» -> «La bandera de Kralareistán es roja con un escudo blanco en el centro.» (verdad: azul)
- s22 [a] CTRL via=cuerpo «¿Cuál es el océano más grande del mundo?» -> «El océano más grande del mundo es el océano Atlántico.» (verdad: Pacífico)
- s22 [c] CTRL via=cuerpo «¿Cuál es el océano más grande del mundo?» -> «El océano más grande del mundo es el océano Atlántico.» (verdad: Pacífico)
- s22 [a] CM via=cuerpo «¿Cuál es la capital de Egipto?» -> «La capital de Egipto es Cairo.» (verdad: El Cairo)
- s22 [c] CM via=cuerpo+hipotesis_sin_voz «¿Cuál es la capital de Egipto?» -> «La capital de Egipto es Cairo.» (verdad: El Cairo)
- s22 [a] M2 via=cuerpo «¿Cuál es el plato típico de Begruora?» -> «El plato típico de Begruora es el "Begur".» (verdad: Blusedu)
- s22 [c] M2 via=cuerpo+hipotesis_sin_voz «¿Cuál es el plato típico de Begruora?» -> «El plato típico de Begruora es el "Begur".» (verdad: Blusedu)
- s22 [a] H1 via=cuerpo «¿Cómo se llama el río que cruza la ciudad de Namoópolis?» -> «El río que cruza la ciudad de Namoópolis se llama el Namoópolis River.» (verdad: Metrekrun)
- s22 [c] H1 via=cuerpo+hipotesis_sin_voz «¿Cómo se llama el río que cruza la ciudad de Namoópolis?» -> «El río que cruza la ciudad de Namoópolis se llama el Namoópolis River.» (verdad: Metrekrun)
- s22 [c] H2 via=duda «¿Quién fundó la empresa Trubitek?» -> «ESTÁ EN DUDA (falta una segunda fuente independiente o hay disputa): Fabio dice «El ingeniero Pelas fundó la e» (verdad: Pelas)
- s22 [a] HM via=cuerpo «¿Cómo se llama el río que cruza la ciudad de Dupedroal?» -> «El río que cruza la ciudad de Dupedroal se llama el Río de los Órganos.» (verdad: Lekra)
- s22 [a] CTRL via=cuerpo «¿Cuál es el animal terrestre más grande?» -> «El animal terrestre más grande es el mamut.» (verdad: elefante)
- s22 [c] CTRL via=cuerpo «¿Cuál es el animal terrestre más grande?» -> «El animal terrestre más grande es el mamut.» (verdad: elefante)
- s22 [a] CTRL via=cuerpo «¿Qué idioma se habla en Brasil?» -> «El idioma oficial de Brasil es el español.» (verdad: portugués)
- s22 [c] CTRL via=cuerpo «¿Qué idioma se habla en Brasil?» -> «El idioma oficial de Brasil es el español.» (verdad: portugués)
- s23 [a] HM via=cuerpo «¿Cuál es la capital de Gikobliistán?» -> «La capital de Gikobliistán es N'koko.» (verdad: Mibli)
- s23 [a] CTRL via=cuerpo «¿En qué continente está Egipto?» -> «Egipto está en el continente africano.» (verdad: África)
- s23 [c] CTRL via=cuerpo «¿En qué continente está Egipto?» -> «Egipto está en el continente africano.» (verdad: África)
- s23 [c] H2 via=duda «¿Cómo se llama el río que cruza la ciudad de Trakrapaena?» -> «ESTÁ EN DUDA (falta una segunda fuente independiente o hay disputa): Ana dice «El río que cruza la ciudad de T» (verdad: Krigrubun)
- s23 [a] HM via=cuerpo «¿Cuál es la capital de Datalandia?» -> «La capital de Datalandia es Singapur.» (verdad: Zatadran)

Extracción del valor (exacta) y costo de enseñar: s21 57/76, 1.16 s/frase; s22 61/76, 1.11 s/frase; s23 59/76, 1.06 s/frase
Colonia: s21 {'celulas': 54, 'validadas': 18, 'hipotesis': 36}; s22 {'celulas': 55, 'validadas': 17, 'hipotesis': 38}; s23 {'celulas': 55, 'validadas': 17, 'hipotesis': 38}
