# Calibración de la nube — sesión 0

> 24-sep-2026, 00:14–00:35 UTC (= 23-sep, 19:14–19:35 en Bogotá). Sesión `session_01RQB2Z9Hj9yA4LEoLeUWGcA`, rama
> `claude/nube-calibracion-qr3r7f` (copia en `nube/calibracion`). Encargo: `NUBE.md` §1.
> Condiciones: sin agentes y un solo proceso por corrida, salvo en la prueba de Pool. Las corridas fueron una tras otra, sin solaparse.
> No se tocó código ni criterios.

**FUNCIONA.** La nube reproduce al PC bit a bit:
- los dos arneses dan N/N y su salida completa es idéntica a la guardada del PC;
- el humo coincide con el del PC en todos los campos.

Por proceso, la nube es 1.3–2.2× más rápida que el PC. Con sus 4 núcleos, Pool 3 rinde lo mismo que el PC con Pool 6.

Queda un cabo fuera del encargo: `requirements.txt` no trae scipy, y sin scipy los gemelos numba no compilan (§4).

## 1. Máquina y versiones

| | nube | PC del director (`requirements.txt`) |
|---|---|---|
| Python | **3.13.12** (venv; el `python` por defecto del contenedor es 3.11.15) | 3.14.2 |
| numpy | 2.4.3 | 2.4.3 |
| numba · llvmlite | 0.67.0 · 0.49.0 (LLVM 22.1.0, CPU `emeraldrapids`) | 0.67.0 · no registrado |
| scipy | 1.18.1, instalado a mano (no está en `requirements.txt`; §4) | instalado, versión no registrada |
| SO | Linux 6.18.44 (KVM), glibc 2.39 | Windows |
| CPU | Intel Xeon @ 2.10 GHz (Emerald Rapids), **nproc 4**, 1 hilo por núcleo, AVX-512 (numpy despacha X86_V4, AVX512_ICL, AVX512_SPR) | 16 lógicos |
| RAM | **15.7 GiB** (16 481 980 kB), sin swap; el cgroup no pone cuota de CPU ni límite de memoria | — |

**Por qué 3.13.12 y no 3.14.2.** La política de red del entorno niega github.com (403), que es de donde uv baja los Python standalone.
El uv instalado (0.8.17) sólo ofrece 3.14.0rc2. Con 3.13.12 la salida es idéntica a la del PC (§2 y §3), así que no hace falta.

**Receta para cada sesión nueva** (el contenedor es efímero; tarda ~1 min):
```
uv venv --seed --python /usr/bin/python3.13 /root/venv-juaco
/root/venv-juaco/bin/pip install -r requirements.txt
/root/venv-juaco/bin/pip install scipy==1.18.1     # sólo para los gemelos numba (§4); fijar la versión del PC cuando se sepa
export PATH=/root/venv-juaco/bin:$PATH            # en cada comando: el shell de la sesión no conserva variables entre llamadas
```

## 2. Arneses de identidad (lo pedido)

| arnés | debe dar | nube | tiempo PC | tiempo nube | nube vs PC | salida completa contra la del PC |
|---|---|---|---|---|---|---|
| `experimentos/subida_n8/identidad_n8.py` | TOTAL 26/26 | **26/26** | 54.8 s | 25.5 s | ×2.15 | idéntica (28 líneas) |
| `experimentos/generaciones/identidad_convive.py` | 37/37 | **37/37** | 133.7 s | 102.0 s | ×1.31 | idéntica (44 líneas, con los 11 hashes del rng) |

"Idéntica" quiere decir que se hizo un `diff` línea a línea contra el `*_salida.txt` guardado en git. Sólo se normalizaron tres cosas:
- el fin de línea (el PC escribe CRLF);
- la fecha de la primera línea;
- el tiempo de la última.

RSS máximo: 46 MB y 54 MB.

## 3. Humo (lo pedido) y un control extra de bits

| corrida (un proceso, T 200 000, 4 brazos) | nube | PC | nube vs PC | resultado contra el PC |
|---|---|---|---|---|
| `corre_n8.py --humo` (semilla 12690) | 32.6 s (8.0–8.3 s por brazo) | 58.0 s (13.6–15.7) | ×1.78 | contra el humo del PC `…_s12690_20260923_160751`: 116 campos comunes, **0 distintos** |
| extra: `corre_n8.py --humo --semilla_humo 12691` | 33.4 s (8.2–8.5) | 58.0 s (13.6–15.9) | ×1.74 | mismo runner que el PC (`corre_n8` 1d78fd3ad1113eec): **1033 de 1033 hojas del JSON idénticas** (sin `dur_s`, `cpu_s` ni `pref`) |

El humo del PC con la semilla 12690 se hizo con una versión anterior del runner (f9acfab8). Los dos humos más viejos del PC con esa
semilla difieren sólo en las medidas que el runner redefinió después:
- `ADQ_tarde` y `ADQ_temprano` en 0a01931b;
- `curva_ADQ_bloques10`, de 20 bloques, en 17baff15.

Los campos del organismo (`muertes`, `splits`, `celdas`, `t_agot`, `n_fus`, `n_cod`, `mv_tot`, `mc_tot`) coinciden en los tres.
Por eso se corrió también la semilla 12691: el PC la corrió con el runner actual exacto.

## 4. Extra: gemelo numba (fuera del encargo; el frente 2 depende de él)

Los dos arneses pedidos no usan numba. Por eso se corrió también `cd organismo && python identidad_v14_rapido.py`:
- **Con `requirements.txt` tal cual, NO COMPILA.** Sale `ImportError: scipy 0.16+ is required for linear algebra`. numba necesita
  scipy para `np.dot` en modo nopython, y `requirements.txt` sólo trae numpy y numba.
- **Con scipy 1.18.1: IDENTIDAD 42/42.** Tarda 76.3 s (87 s de pared con la compilación; RSS 364 MB). Acelera ×50 a 100 000 pasos y
  ×45 a 200 000.
- **Alcance.** La prueba es gemelo contra interpretado *dentro de esta máquina*. No se comparó el gemelo con el PC, y la versión de
  scipy del PC no está registrada.

## 5. Escalado del Pool (medido)

Método (script al final):
- las tareas se reparten con `multiprocessing.Pool(k)`, 4 por proceso;
- las tareas son los 8 pares (semilla, brazo) de los humos 12690 y 12691, así que no se gastó ninguna semilla retenida;
- el resultado de cada tarea se compara con el del humo.

| Pool | tareas | pared | corridas/min | `dur_s` (valor central; mín–máx) | resultado == humo |
|---|---|---|---|---|---|
| 1 | 4 | 33.6 s | 7.1 | 8.5 (8.1–8.6) | 4/4 |
| 2 | 8 | 34.6 s | 13.9 | 8.7 (8.4–8.8) | 8/8 |
| 3 | 12 | 34.2 s | 21.0 | 8.5 (8.2–8.7) | 12/12 |
| 4 | 16 | 34.7 s | **27.7** | 8.5 (8.1–8.8) | 16/16 |
| PC, Pool 6 (series n8 12601–12640) | 80 + 80 | 242.9 s / 233.6 s | 19.8 / 20.5 | 16.2 / 15.5 (mediana) | — |

El escalado es lineal hasta 4 y cada corrida no se alarga: los 4 vCPU se comportan como 4 núcleos propios.

## 6. Pool recomendado: **3 (nproc − 1)**, no 2

- **Rendimiento.** La fórmula nproc − 2 da 2: 13.9 corridas/min, 0.7 veces el PC. Con **3**, la nube da 21.0 corridas/min, lo mismo que
  el PC con Pool 6. Con 4 da 27.7 (1.4 veces el PC), pero sólo si nada más corre.
- **Por qué sobra el margen de 2.** Viene del PC, que el director usa mientras corren las series. Aquí nadie más usa la máquina. El
  núcleo libre alcanza para la sesión y para un humo o arnés de un agente, sin contaminar el tiempo de pared de la serie (regla 11).
- **Excepción.** Con dos agentes corriendo humos a la vez, bajar a 2.
- **Quién decide.** `NUBE.md` §2 dice nproc − 2. Cambiarlo a nproc − 1 lo decide el director; aquí no se tocó.
- **Duración de una serie como la n8** (80 corridas, T 200 000): 5.8 min con Pool 2, **3.8 min con Pool 3** y 2.9 min con Pool 4. En
  el PC, con Pool 6, tardó 3.9–4.0 min.
- **La RAM no limita.** Cada proceso interpretado usa ≤ 54 MB y numba, al compilar, 364 MB, sobre 15.7 GiB.

## 7. Cabos

1. **scipy en `requirements.txt`.** Correr en el PC `python -c "import scipy; print(scipy.__version__)"` y fijar esa versión. Hasta
   entonces, la nube usa 1.18.1 sin fijar.
2. **Los arneses reescriben su `*_salida.txt`.** Ese archivo está versionado y guarda la salida del PC en CRLF. En esta sesión:
   - la salida de la nube se guardó aparte, en esta carpeta;
   - el archivo del PC se restauró con `git checkout --`.

   Las próximas sesiones deben hacer lo mismo. Si no, un commit reemplaza la referencia del PC y deja un diff de CRLF en todas las
   líneas.
3. **Tiempos del PC.** Salen de las salidas guardadas. Si el PC tenía Pools corriendo a esa hora, están inflados: las razones son
   indicativas, no constantes.
4. **Entorno (opcional).**
   - La receta del §1 puede ir en el *setup script* del entorno (menú del entorno en la barra de título de la sesión → Edit → Setup
     script). Así cada sesión arranca lista.
   - Para usar 3.14.2, igual que el PC, habría que permitir github.com en *Network access*. No hace falta.
5. **Gasto.** La sesión corre con el crédito promocional (`rateLimitType ccr_promotional`, sin overage). El gasto en USD no se ve desde
   dentro de la sesión: el director lo lee en claude.ai y lo anota aquí para fijar el ritmo (`NUBE.md`: ~40 USD por semana).

## 8. Archivos

- **Arneses.** `nube_calibracion_20260924_identidad_n8.log` y `…_identidad_convive.log` guardan la salida de cada arnés en la nube,
  con el comando y una línea final `# MIDE` (pared, CPU y RSS).
- **Humos.** `nube_calibracion_20260924_humo_n8_s12690.log` y `…_s12691.log` son la consola de los humos. Los JSON están en
  `experimentos/subida_n8/datos/humo/`:
  - `n8_humo_base-fus-fusazar-recic_s12690_20260924_002056.json` (sha 3f1eb9c11f0b2391);
  - `…_s12691_20260924_002202.json` (sha 5c0b50a345678284).
- **Gemelo numba.** `nube_calibracion_20260924_identidad_v14_rapido.log` (el segundo intento, ya con scipy).
- **Pool.** `nube_calibracion_20260924_escala_pool.log`.

<details><summary>Script del escalado del Pool (scratch de la sesión; no entra al repo como código)</summary>

```python
"""Escalado de Pool en la nube: k procesos, 4 tareas por proceso, tareas = (semilla, brazo) de los humos 12690/12691
(ya publicos; no se gasta ninguna semilla retenida). Solo mide pared y dur_s; comprueba que el resultado con Pool == humo."""
import glob, json, os, sys, time
from multiprocessing import Pool
RAIZ = '/home/user/juaco'
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'subida_n8'))
import corre_n8 as CR

def ref():
    out = {}
    for s in (12690, 12691):
        d = json.load(open(sorted(glob.glob(f'{RAIZ}/experimentos/subida_n8/datos/humo/n8_humo_*_s{s}_20260924_*.json'))[-1], encoding='utf-8'))
        for r in d['resultados']:
            out[(r['semilla'], r['brazo'])] = {k: v for k, v in r.items() if k != 'dur_s'}
    return out

if __name__ == '__main__':
    R = ref(); pares = list(R)
    for k in (1, 2, 3, 4):
        tareas = [pares[i % len(pares)] for i in range(4 * k)]
        t0 = time.time()
        with Pool(k) as p:
            res = p.map(CR.corre_uno, tareas, chunksize=1)
        pared = time.time() - t0
        iguales = sum({kk: v for kk, v in r.items() if kk != 'dur_s'} == R[(r['semilla'], r['brazo'])] for r in res)
        durs = sorted(r['dur_s'] for r in res)
        print(f"{time.strftime('%H:%M:%S')} Pool({k}): {len(tareas)} tareas en {pared:.1f}s -> {len(tareas) / pared * 60:.1f} corridas/min; "
              f"dur_s mediana {durs[len(durs) // 2]} (min {durs[0]}, max {durs[-1]}); resultado == humo {iguales}/{len(res)}", flush=True)
```
</details>
