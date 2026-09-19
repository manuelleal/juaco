# JUACO MEMORY FRONTIER v3

**SIMULACIÓN HIPOTÉTICA — no es evidencia biológica ni AGI.**

## Idea matemática
Probamos memoria como módulos locales: **E** episodios, **S** resumen semántico, **W** contexto de trabajo, **R** replay/consolidación y **X** sorpresa/error. La hipótesis de dos velocidades se inspira en modelos computacionales de memoria que distinguen aprendizaje rápido de episodios y aprendizaje lento/generalización. citeturn0search0turn0search1

## Barrido de arquitecturas

### A0 (S)
- stable: linaje medio=0.267, mejor=2, supervivencia media=2.97, extinción=100.0%
- medium: linaje medio=0.233, mejor=1, supervivencia media=2.9, extinción=100.0%
- volatile: linaje medio=0.533, mejor=4, supervivencia media=4.47, extinción=100.0%

### A1 (E)
- stable: linaje medio=0.267, mejor=2, supervivencia media=2.97, extinción=100.0%
- medium: linaje medio=0.233, mejor=1, supervivencia media=2.9, extinción=100.0%
- volatile: linaje medio=0.533, mejor=4, supervivencia media=4.47, extinción=100.0%

### A2 (S+E)
- stable: linaje medio=0.267, mejor=2, supervivencia media=2.97, extinción=100.0%
- medium: linaje medio=0.233, mejor=1, supervivencia media=2.9, extinción=100.0%
- volatile: linaje medio=0.533, mejor=4, supervivencia media=4.47, extinción=100.0%

### A3 (S+E+W)
- stable: linaje medio=0.267, mejor=2, supervivencia media=2.97, extinción=100.0%
- medium: linaje medio=0.233, mejor=1, supervivencia media=2.9, extinción=100.0%
- volatile: linaje medio=0.533, mejor=4, supervivencia media=4.47, extinción=100.0%

### A4 (S+E+R)
- stable: linaje medio=0.267, mejor=2, supervivencia media=2.97, extinción=100.0%
- medium: linaje medio=0.233, mejor=1, supervivencia media=2.9, extinción=100.0%
- volatile: linaje medio=0.533, mejor=4, supervivencia media=4.47, extinción=100.0%

### A5 (S+E+R+X)
- stable: linaje medio=0.267, mejor=2, supervivencia media=2.97, extinción=100.0%
- medium: linaje medio=0.233, mejor=1, supervivencia media=2.9, extinción=100.0%
- volatile: linaje medio=0.533, mejor=4, supervivencia media=4.47, extinción=100.0%

### A6 (S+E+W+R+X)
- stable: linaje medio=0.267, mejor=2, supervivencia media=2.97, extinción=100.0%
- medium: linaje medio=0.233, mejor=1, supervivencia media=2.9, extinción=100.0%
- volatile: linaje medio=0.533, mejor=4, supervivencia media=4.47, extinción=100.0%

## Loop evolutivo
Se ejecutaron 40 generaciones de arquitecturas. En cada generación solo se podía agregar o quitar **un módulo**. Candidato final: **S+E**.

Validación fresca, 60 réplicas: {"candidate": "S+E", "mean_lineage": 0.3, "median_lineage": 0.0, "best_lineage": 3, "mean_survival": 3.083, "extinction_rate": 1}

## Interpretación
Si E+S+R+X supera consistentemente a sistemas simples, la lectura válida es que una combinación de memoria episódica + compresión + replay + sorpresa es una hipótesis prometedora para JUACO. No significa que hayamos reconstruido memoria humana.

## Próximo algoritmo a buscar
El siguiente loop debe buscar una regla todavía más mínima: **episodio -> sorpresa -> replay -> compresión -> acción**, y probar si esa cadena permite que un descendiente herede la capacidad de generalizar sin heredar literalmente la historia del padre. Eso sería un test directo de acumulación cultural/representacional.
