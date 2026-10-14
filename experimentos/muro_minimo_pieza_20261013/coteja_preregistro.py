"""Cotejo preregistro <-> runner ANTES de correr: umbrales, semillas, N y controles, valor a valor.

Nace de la medición del protocolo en JUACO (13-oct-2026, ver MEDICION.md): el auditor de sólo lectura atrapó 9 de 24
errores de criterio sembrados (serie y réplica juntas, descriptivo); muchos eran un umbral o un rango de semillas
distinto entre el preregistro y el runner. Esto lo comprueba una máquina.

CONVENCIÓN (mínima)
  En el PREREGISTRO*.md, una sección `## Parámetros sellados` con una tabla cuyas dos primeras columnas son
  `nombre | valor` (las columnas de más se ignoran; sirven para decir de qué sección sale cada valor):

      ## Parámetros sellados
      | nombre | valor |
      |---|---|
      | UMBRAL_PAREADO | 15 |
      | SERIE | range(101, 121) |
      | HUECO | (0.30, 0.78) |

  `valor` es un literal de Python (número, texto entre comillas, True/False/None, tupla, lista, dict) o
  `range(a, b[, paso])`; puede ir entre `comillas invertidas`. Una celda no puede contener `|`.
  En el runner, una variable de módulo `PREREGISTRADO = dict(NOMBRE=valor, ...)` (o `{...}`) con los MISMOS nombres.
  Cada valor debe ser la variable que el runner usa de verdad (`dict(UMBRAL_PAREADO=UMBRAL_PAREADO)`), no el número
  copiado otra vez: si se copia el número, el cotejo compara dos textos y no lo que corre.

REGLAS DEL COTEJO (exactas, sin tolerancia)
  - cada nombre del preregistro existe en PREREGISTRADO, y cada nombre de PREREGISTRADO está en el preregistro;
  - valor a valor iguales: números por valor (15 == 15.0; True no es 1), secuencias elemento a elemento (range, tupla
    y lista valen lo mismo si tienen los mismos elementos en el mismo orden), dicts clave a clave, textos exactos;
  - si hay más de una sección `## Parámetros sellados` (una enmienda añade otra al final), vale la ÚLTIMA y entera
    (copia todas las filas, no sólo la que cambia), y todo valor que cambie, aparezca o desaparezca respecto de la
    anterior exige un `ERR-N` escrito entre el final de la tabla anterior y el título de la nueva (regla 9 de
    PROTOCOLO.md). Sin ERR, es una diferencia. La tabla termina en la primera línea que no empieza por `|`.

DOS USOS
  python herramientas/coteja_preregistro.py RUTA/PREREGISTRO.md RUTA/corre.py [--prefijo ERR]
      Sin ejecutar el runner (importarlo podría lanzar la corrida): lee PREREGISTRADO con el árbol sintáctico y
      resuelve nombres del propio módulo y de módulos hermanos importados (`import x`, `from x import Y`, con x.py
      en la misma carpeta). Lo que no se puede resolver sin ejecutar cuenta como diferencia.
      Sale 0 si todo coincide; 1 si hay diferencias; 2 si falta la sección, la variable o los argumentos.
  Dentro del runner, como puerta antes de la corrida larga (lo hace ejemplo_minimo/corre.py):
      import coteja_preregistro
      filas, difs = coteja_preregistro.coteja('PREREGISTRO.md', PREREGISTRADO)
      if difs: abortar
      Compara los valores VIVOS, los que van a correr. Es el uso que manda.

QUÉ NO HACE
  No lee la prosa: un umbral escrito sólo en una frase del preregistro no se coteja. No sabe si el runner usa de verdad
  la variable que puso en PREREGISTRADO (eso lo revisa el auditor). No juzga si los valores son buenos.
"""
import ast
import numbers
import os
import re
import sys

RE_TITULO = re.compile(r'^##\s+Par[aá]metros sellados\b')
RE_FIN = re.compile(r'^#{1,2}\s')
LLAMADAS = {'range': range, 'dict': dict, 'tuple': tuple, 'list': list}


class NoResoluble(Exception):
    pass


# ------------------------------------------------------------------------------------------- valores literales
def evalua(nodo, nombre=None):
    """Literal de Python o range/dict/tuple/list de literales. `nombre(nodo)` resuelve nombres (o NoResoluble)."""
    if isinstance(nodo, ast.Constant):
        return nodo.value
    if isinstance(nodo, ast.Tuple):
        return tuple(evalua(x, nombre) for x in nodo.elts)
    if isinstance(nodo, ast.List):
        return [evalua(x, nombre) for x in nodo.elts]
    if isinstance(nodo, ast.Dict):
        out = {}
        for k, v in zip(nodo.keys, nodo.values):
            if k is None:
                out.update(evalua(v, nombre))
            else:
                out[evalua(k, nombre)] = evalua(v, nombre)
        return out
    if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, (ast.USub, ast.UAdd)):
        v = evalua(nodo.operand, nombre)
        if isinstance(v, bool) or not isinstance(v, numbers.Number):
            raise NoResoluble('signo sobre algo que no es un número')
        return -v if isinstance(nodo.op, ast.USub) else v
    if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and nodo.func.id in LLAMADAS:
        args = [evalua(a, nombre) for a in nodo.args if not isinstance(a, ast.Starred)]
        if len(args) != len(nodo.args):
            raise NoResoluble('argumento *x')
        kw = {}
        for k in nodo.keywords:
            if k.arg is None:
                kw.update(evalua(k.value, nombre))
            else:
                kw[k.arg] = evalua(k.value, nombre)
        return LLAMADAS[nodo.func.id](*args, **kw)
    if nombre is not None:
        return nombre(nodo)
    raise NoResoluble('no es un literal: %s' % ast.unparse(nodo))


def muestra(v):
    if isinstance(v, range):
        return 'range(%d, %d%s)' % (v.start, v.stop, '' if v.step == 1 else ', %d' % v.step)
    return repr(v)


def iguales(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, numbers.Real) and isinstance(b, numbers.Real):
        return a == b
    sec = (range, tuple, list)
    if isinstance(a, sec) and isinstance(b, sec):
        return len(a) == len(b) and all(iguales(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(iguales(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b


# ------------------------------------------------------------------------------------------- preregistro
def secciones(texto):
    """Cada sección `## Parámetros sellados`: línea del título, línea de fin, tabla {nombre: (valor, línea)}."""
    lineas = texto.split('\n')
    out, i = [], 0
    while i < len(lineas):
        if not RE_TITULO.match(lineas[i]):
            i += 1
            continue
        tabla, errores, cabecera, j = {}, [], False, i + 1
        while j < len(lineas) and not RE_FIN.match(lineas[j]):
            l = lineas[j].strip()
            if cabecera and not l.startswith('|'):
                break   # la tabla terminó: lo que sigue (p. ej. la enmienda siguiente) ya no es de esta sección
            if l.startswith('|'):
                celdas = [c.strip() for c in l.strip().strip('|').split('|')]
                if not cabecera:
                    if len(celdas) < 2 or celdas[0].lower() != 'nombre' or celdas[1].lower() != 'valor':
                        errores.append('línea %d: la tabla debe empezar con la cabecera "| nombre | valor |"' % (j + 1))
                    cabecera = True
                elif not set(''.join(celdas)) <= set('-: '):
                    nom, txt = celdas[0].strip('`').strip(), celdas[1].strip().strip('`').strip()
                    try:
                        val = evalua(ast.parse(txt, mode='eval').body)
                    except (SyntaxError, NoResoluble, TypeError, ValueError) as e:
                        errores.append('línea %d: valor de %s no es un literal válido (%r): %s' % (j + 1, nom, txt, e))
                        val = None
                    if nom in tabla:
                        errores.append('línea %d: %s repetido en la misma tabla (antes en la línea %d)'
                                       % (j + 1, nom, tabla[nom][1]))
                    tabla[nom] = (val, j + 1)
            j += 1
        if not tabla and not errores:
            errores.append('línea %d: la sección no trae ninguna fila' % (i + 1))
        out.append(dict(linea=i + 1, fin=j, tabla=tabla, errores=errores))
        i = j
    return out, lineas


def lee_preregistro(ruta, prefijo='ERR'):
    """Tabla vigente {nombre: (valor, línea)} y lista de problemas del propio preregistro."""
    with open(ruta, encoding='utf-8') as f:
        secs, lineas = secciones(f.read())
    if not secs:
        return None, ['%s no tiene una sección "## Parámetros sellados"' % ruta]
    problemas = [e for s in secs for e in s['errores']]
    re_err = re.compile(r'\b%s-\d+' % re.escape(prefijo))
    for ant, nue in zip(secs, secs[1:]):
        cambia = sorted(n for n in set(ant['tabla']) | set(nue['tabla'])
                        if n not in ant['tabla'] or n not in nue['tabla']
                        or not iguales(ant['tabla'][n][0], nue['tabla'][n][0]))
        entre = '\n'.join(lineas[ant['fin']:nue['linea']])
        if cambia and not re_err.search(entre):
            problemas.append('la sección de la línea %d cambia %s respecto de la de la línea %d y no hay un %s-N '
                             'escrito entre las dos (regla 9)' % (nue['linea'], ', '.join(cambia), ant['linea'],
                                                                  prefijo))
    return secs[-1]['tabla'], problemas


# ------------------------------------------------------------------------------------------- comparación
def compara(tabla, valores, no_resueltos=None):
    """filas (estado, nombre, preregistro, runner) y lista de diferencias."""
    no_resueltos = no_resueltos or {}
    filas, difs = [], []
    for n in sorted(set(tabla) | set(valores) | set(no_resueltos)):
        p = muestra(tabla[n][0]) if n in tabla else '(no está)'
        if n in no_resueltos:
            filas.append(('NO RESUELTO', n, p, no_resueltos[n]))
            difs.append('%s: no se puede leer del runner sin ejecutarlo (%s)' % (n, no_resueltos[n]))
        elif n not in valores:
            filas.append(('FALTA', n, p, '(no está)'))
            difs.append('%s: está en el preregistro (línea %d) y no en PREREGISTRADO del runner' % (n, tabla[n][1]))
        elif n not in tabla:
            filas.append(('SOBRA', n, '(no está)', muestra(valores[n])))
            difs.append('%s: el runner lo declara preregistrado y el preregistro no lo trae' % n)
        elif not iguales(tabla[n][0], valores[n]):
            filas.append(('DISTINTO', n, p, muestra(valores[n])))
            difs.append('%s: preregistro %s (línea %d) != runner %s' % (n, p, tabla[n][1], muestra(valores[n])))
        else:
            filas.append(('igual', n, p, muestra(valores[n])))
    return filas, difs


def coteja(ruta_prereg, preregistrado, prefijo='ERR'):
    """Uso dentro del runner, con los valores vivos. Devuelve (filas, diferencias); [] = todo coincide."""
    tabla, problemas = lee_preregistro(ruta_prereg, prefijo)
    if tabla is None:
        return [], problemas
    filas, difs = compara(tabla, dict(preregistrado))
    return filas, problemas + difs


def imprime(filas):
    if not filas:
        return
    a = max(len(f[1]) for f in filas)
    b = max(len(f[2]) for f in filas)
    for estado, n, p, r in filas:
        print('  %-11s %-*s  preregistro %-*s  runner %s' % (estado, a, n, b, p, r))


# ------------------------------------------------------------------------------------------- runner sin ejecutar
class Modulo:
    def __init__(self, ruta, cache):
        with open(ruta, encoding='utf-8') as f:
            self.arbol = ast.parse(f.read(), filename=ruta)
        self.ruta, self.carpeta, self.cache = ruta, os.path.dirname(ruta), cache
        self.asig, self.mods, self.desde, self.globales = {}, {}, {}, set()
        for nodo in self.arbol.body:
            if isinstance(nodo, (ast.Assign, ast.AnnAssign)) and nodo.value is not None:
                destinos = nodo.targets if isinstance(nodo, ast.Assign) else [nodo.target]
                for d in destinos:
                    if isinstance(d, ast.Name):
                        self.asig[d.id] = (nodo.value, None, nodo.lineno)
                    elif isinstance(d, ast.Tuple) and all(isinstance(e, ast.Name) for e in d.elts):
                        for k, e in enumerate(d.elts):
                            self.asig[e.id] = (nodo.value, k, nodo.lineno)
            elif isinstance(nodo, ast.AugAssign) and isinstance(nodo.target, ast.Name):
                self.asig[nodo.target.id] = (None, 'se modifica con %s= en la línea %d' % (
                    type(nodo.op).__name__, nodo.lineno), nodo.lineno)
            elif isinstance(nodo, ast.Import):
                for a in nodo.names:
                    self.mods[a.asname or a.name] = a.name
            elif isinstance(nodo, ast.ImportFrom) and nodo.level == 0 and nodo.module:
                for a in nodo.names:
                    self.desde[a.asname or a.name] = (nodo.module, a.name)
        for nodo in ast.walk(self.arbol):
            if isinstance(nodo, ast.Global):
                self.globales.update(nodo.names)

    def otro(self, nombre_mod):
        ruta = os.path.join(self.carpeta, nombre_mod.replace('.', os.sep) + '.py')
        if not os.path.exists(ruta):
            raise NoResoluble('el módulo %s no está en la carpeta del runner' % nombre_mod)
        ruta = os.path.abspath(ruta)
        if ruta not in self.cache:
            self.cache[ruta] = Modulo(ruta, self.cache)
        return self.cache[ruta]

    def valor_de(self, n, prof=0):
        if prof > 50:
            raise NoResoluble('referencias circulares o demasiado profundas')
        if n in self.globales:
            raise NoResoluble('%s se reasigna dentro de una función (global)' % n)
        if n in self.asig:
            nodo, k, linea = self.asig[n]
            if nodo is None:
                raise NoResoluble('%s %s' % (n, k))
            v = evalua(nodo, lambda x: self.nombre(x, prof + 1))
            return v if k is None else list(v)[k]
        if n in self.desde:
            m, attr = self.desde[n]
            return self.otro(m).valor_de(attr, prof + 1)
        raise NoResoluble('%s no tiene una asignación de módulo legible' % n)

    def nombre(self, nodo, prof=0):
        if isinstance(nodo, ast.Name):
            return self.valor_de(nodo.id, prof)
        if isinstance(nodo, ast.Attribute) and isinstance(nodo.value, ast.Name) and nodo.value.id in self.mods:
            return self.otro(self.mods[nodo.value.id]).valor_de(nodo.attr, prof + 1)
        if isinstance(nodo, ast.Subscript):
            cont = evalua(nodo.value, lambda x: self.nombre(x, prof + 1))
            clave = evalua(nodo.slice, lambda x: self.nombre(x, prof + 1))
            try:
                return cont[clave]
            except (KeyError, IndexError, TypeError) as e:
                raise NoResoluble('%s: %r' % (ast.unparse(nodo), e))
        raise NoResoluble('hace falta ejecutar: %s' % ast.unparse(nodo))


def lee_runner(ruta):
    """{nombre: valor}, {nombre: motivo de no resuelto}, línea de PREREGISTRADO (o None)."""
    m = Modulo(os.path.abspath(ruta), {})
    if 'PREREGISTRADO' not in m.asig or m.asig['PREREGISTRADO'][0] is None:
        return None, None, None
    nodo, _, linea = m.asig['PREREGISTRADO']
    pares = None
    if isinstance(nodo, ast.Dict) and all(isinstance(k, ast.Constant) for k in nodo.keys):
        pares = [(k.value, v) for k, v in zip(nodo.keys, nodo.values)]
    elif isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and nodo.func.id == 'dict' \
            and not nodo.args and all(k.arg for k in nodo.keywords):
        pares = [(k.arg, k.value) for k in nodo.keywords]
    valores, no_res = {}, {}
    if pares is None:
        try:
            valores = dict(evalua(nodo, m.nombre))
        except NoResoluble as e:
            no_res['PREREGISTRADO'] = str(e)
        return valores, no_res, linea
    for k, v in pares:
        try:
            valores[k] = evalua(v, m.nombre)
        except NoResoluble as e:
            no_res[k] = str(e)
    return valores, no_res, linea


def main(argv):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    args = list(argv[1:])
    prefijo = 'ERR'
    if '--prefijo' in args:
        i = args.index('--prefijo')
        prefijo = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2 or any(a.startswith('-') for a in args):
        print(__doc__)
        return 2
    r_pre, r_run = args
    tabla, problemas = lee_preregistro(r_pre, prefijo)
    if tabla is None:
        print('ABORTO: ' + problemas[0])
        return 2
    valores, no_res, linea = lee_runner(r_run)
    if valores is None:
        print('ABORTO: %s no declara PREREGISTRADO = dict(...) a nivel de módulo' % r_run)
        return 2
    filas, difs = compara(tabla, valores, no_res)
    print('Cotejo %s (%d nombres) <-> %s (PREREGISTRADO, línea %d), sin ejecutar el runner'
          % (r_pre, len(tabla), r_run, linea))
    imprime(filas)
    difs = problemas + difs
    if difs:
        print('ABORTO: %d diferencia(s) entre preregistro y runner; no se corre:' % len(difs))
        for d in difs:
            print('  - ' + d)
        return 1
    print('COTEJO: %d/%d iguales' % (len(filas), len(filas)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
