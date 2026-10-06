# -*- coding: utf-8 -*-
"""MUNDO del Frankenstein v0: hechos inventados (el cuerpo no puede saberlos), maestros y preguntas.

Clases de hechos nuevos por semilla (42):
  H2 (12) dos maestros honestos distintos enseñan la verdad (plantillas distintas)
  H1 (6)  un solo maestro honesto la dice una vez            (precio de la cuarentena)
  M1 (4)  el mentiroso dice un valor falso una vez
  M2 (4)  el mentiroso dice el mismo valor falso DOS veces   (misma fuente: no es independiente)
  HM (6)  dos honestos dicen la verdad y el mentiroso lo contrario (posición del mentiroso al azar)
  CC (6)  dos maestros se contradicen (uno acierta; cuál y en qué orden, al azar)
  NN (4)  nadie lo enseña
Control (12 por semilla): preguntas de cultura general que el cuerpo ya sabe; en 4 de ellas (CM)
el mentiroso enseña además un valor falso ("la capital de Francia es Lyon").

Trampas revisadas: verdad y mentira salen del MISMO generador y de las MISMAS plantillas (no hay
pista léxica); los nombres de las fuentes son neutros y se barajan por semilla (el sistema no ve
quién es el mentiroso); el orden de los eventos y de las preguntas se baraja; el orden
verdad/mentira dentro de HM y CC se baraja.
"""
import difflib
import random
import re
import unicodedata

CONS = list("bdfgklmnprstvz") + ["tr", "dr", "kr", "bl", "gr", "ch"]
VOC = list("aeiou")
COLORES = ["rojo", "verde", "azul", "amarillo", "negro", "blanco", "naranja", "morado", "gris", "rosado"]
NOMBRES_FUENTE = ["Ana", "Beto", "Caro", "Dani", "Eli", "Fabio", "Gina", "Hugo"]


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ ]+", " ", s).strip()


def contiene(texto, valor):
    """¿El texto afirma el valor? Palabra completa, sin acentos ni mayúsculas."""
    return re.search(r"(?<![a-z0-9ñ])" + re.escape(norm(valor)) + r"(?![a-z0-9ñ])", norm(texto)) is not None


# ---- tipos de hecho: (plantillas de enseñanza, pregunta, tipo de sujeto, tipo de valor) ----
TIPOS = {
    "capital": (["La capital de {S} es {V}.", "{V} es la ciudad capital de {S}.", "En {S}, la capital se llama {V}."],
                "¿Cuál es la capital de {S}?", "pais", "nombre"),
    "fundador": (["La empresa {S} fue fundada por el ingeniero {V}.", "El ingeniero {V} fundó la empresa {S}.",
                  "Quien fundó la empresa {S} fue el ingeniero {V}."],
                 "¿Quién fundó la empresa {S}?", "empresa", "nombre"),
    "bandera": (["La bandera de {S} es de color {V}.", "El color de la bandera de {S} es el {V}.",
                 "En {S} la bandera es toda de color {V}."],
                "¿De qué color es la bandera de {S}?", "pais", "color"),
    "lunas": (["El planeta {S} tiene {V} lunas.", "Alrededor del planeta {S} giran {V} lunas.",
               "Son {V} las lunas del planeta {S}."],
              "¿Cuántas lunas tiene el planeta {S}?", "planeta", "numero"),
    "rio": (["El río que cruza la ciudad de {S} se llama {V}.", "{V} es el nombre del río que cruza la ciudad de {S}.",
             "Por la ciudad de {S} pasa el río {V}."],
            "¿Cómo se llama el río que cruza la ciudad de {S}?", "ciudad", "nombre"),
    "plato": (["El plato típico de {S} es el {V}.", "En {S} el plato típico se llama {V}.",
               "El {V} es el plato típico de {S}."],
              "¿Cuál es el plato típico de {S}?", "pais", "nombre"),
}
SUFIJO = {"pais": ["ia", "landia", "istán", "ora"], "empresa": ["ex", "tek", "or", "ix"],
          "planeta": ["on", "us", "ar", "is"], "ciudad": ["burgo", "ópolis", "ena", "al"],
          "nombre": ["", "", "n", "s", "l"]}

# ---- control: cultura general (pregunta, respuestas aceptadas, [frase falsa, valor falso]) ----
CAPITALES = [("Francia", "París", "Lyon"), ("Italia", "Roma", "Milán"), ("Japón", "Tokio", "Osaka"),
             ("Alemania", "Berlín", "Múnich"), ("Colombia", "Bogotá", "Medellín"), ("Argentina", "Buenos Aires", "Córdoba"),
             ("Perú", "Lima", "Cusco"), ("España", "Madrid", "Barcelona"), ("Portugal", "Lisboa", "Oporto"),
             ("Rusia", "Moscú", "Kazán"), ("Egipto", "El Cairo", "Alejandría"), ("Chile", "Santiago", "Valparaíso"),
             ("Grecia", "Atenas", "Salónica"), ("Inglaterra", "Londres", "Mánchester"), ("Cuba", "La Habana", "Varadero"),
             ("Venezuela", "Caracas", "Maracaibo")]
OTRAS = [("¿Cuánto es 7 por 8?", ["56"]), ("¿Cuánto es 9 más 6?", ["15", "quince"]), ("¿Cuánto es 12 por 12?", ["144"]),
         ("¿Cuánto es 100 menos 37?", ["63"]), ("¿Cuántos días tiene una semana?", ["7", "siete"]),
         ("¿Cuántos meses tiene un año?", ["12", "doce"]), ("¿Cuántos minutos tiene una hora?", ["60", "sesenta"]),
         ("¿Cuántos lados tiene un triángulo?", ["3", "tres"]), ("¿Cuántos lados tiene un hexágono?", ["6", "seis"]),
         ("¿Cuántas patas tiene una araña?", ["8", "ocho"]), ("¿Cuál es el planeta más grande del sistema solar?", ["Júpiter"]),
         ("¿Cuál es el planeta más cercano al Sol?", ["Mercurio"]), ("¿Cuál es la fórmula química del agua?", ["H2O", "H₂O"]),
         ("¿Quién escribió Don Quijote de la Mancha?", ["Cervantes"]), ("¿Quién pintó la Mona Lisa?", ["Leonardo", "da Vinci"]),
         ("¿Quién escribió Cien años de soledad?", ["García Márquez"]), ("¿Cuál es el océano más grande del mundo?", ["Pacífico"]),
         ("¿Cuál es el río más caudaloso de Sudamérica?", ["Amazonas"]), ("¿Cuál es la montaña más alta del mundo?", ["Everest"]),
         ("¿Qué idioma se habla en Brasil?", ["portugués"]), ("¿Qué color resulta al mezclar azul y amarillo?", ["verde"]),
         ("¿Cómo se llama el satélite natural de la Tierra?", ["Luna"]), ("¿Qué gas necesitamos respirar para vivir?", ["oxígeno"]),
         ("¿Cuál es el animal terrestre más grande?", ["elefante"]), ("¿En qué continente está Egipto?", ["África"]),
         ("¿En qué año llegó Colón a América?", ["1492"]), ("¿Cuántas horas tiene un día?", ["24", "veinticuatro"]),
         ("¿Cuál es la moneda de Estados Unidos?", ["dólar"]), ("¿Quién formuló la teoría de la relatividad?", ["Einstein"]),
         ("¿En qué país está la torre Eiffel?", ["Francia"]), ("¿Cuántos centímetros tiene un metro?", ["100", "cien"]),
         ("¿Cuál es el idioma oficial de Francia?", ["francés"])]


def _nombre(rng, tipo):
    n = rng.choice([2, 3]) if tipo != "nombre" else rng.choice([2, 3])
    s = "".join(rng.choice(CONS) + rng.choice(VOC) for _ in range(n)) + rng.choice(SUFIJO[tipo])
    return s.capitalize()


class _Nombres:
    def __init__(self, rng):
        self.rng, self.usados = rng, []

    def nuevo(self, tipo):
        for _ in range(2000):
            s = _nombre(self.rng, tipo)
            ns = norm(s)
            if len(ns) < 5:
                continue
            if all(difflib.SequenceMatcher(None, ns, u).ratio() < 0.62 for u in self.usados):
                self.usados.append(ns)
                return s
        raise RuntimeError("no hay nombres")


def _valor(rng, nombres, tv, distinto=None):
    for _ in range(100):
        if tv == "color":
            v = rng.choice(COLORES)
        elif tv == "numero":
            v = str(rng.randint(2, 48))
        else:
            v = nombres.nuevo("nombre")
        if v != distinto:
            return v


def construye(semilla, bloque_control=None):
    """Devuelve dict con fuentes, eventos (enseñanzas en orden) y preguntas."""
    rng = random.Random(1000 + semilla)
    nombres = _Nombres(rng)
    fu = NOMBRES_FUENTE[:]
    rng.shuffle(fu)
    H_A, H_B, MENT, C1, C2 = fu[:5]
    clases = ["H2"] * 12 + ["H1"] * 6 + ["M1"] * 4 + ["M2"] * 4 + ["HM"] * 6 + ["CC"] * 6 + ["NN"] * 4
    rng.shuffle(clases)
    tipos = list(TIPOS)
    hechos, eventos = [], []
    paises = []          # un tercio de los hechos de país reutiliza un país ya usado (misma S, otro atributo)
    usados_sa = set()
    for i, cl in enumerate(clases):
        t = tipos[i % len(tipos)]
        plant, preg, ts, tv = TIPOS[t]
        S = None
        if ts == "pais" and paises and rng.random() < 0.45:
            cand = [p for p in paises if (p, t) not in usados_sa]
            if cand:
                S = rng.choice(cand)
        if S is None:
            S = nombres.nuevo(ts)
            if ts == "pais":
                paises.append(S)
        usados_sa.add((S, t))
        V = _valor(rng, nombres, tv)
        F = _valor(rng, nombres, tv, distinto=V)
        p = plant[:]
        rng.shuffle(p)
        h = {"id": f"n{i:02d}", "clase": cl, "tipo": t, "sujeto": S, "verdad": V, "falso": F,
             "pregunta": preg.format(S=S), "aceptadas": [V], "mentiras": [F]}
        hechos.append(h)
        ev = []
        if cl == "H2":
            ev = [(H_A, p[0], V), (H_B, p[1], V)]
        elif cl == "H1":
            ev = [(rng.choice([H_A, H_B]), p[0], V)]
        elif cl == "M1":
            ev = [(MENT, p[0], F)]
        elif cl == "M2":
            ev = [(MENT, p[0], F), (MENT, p[1], F)]
        elif cl == "HM":
            ev = [(H_A, p[0], V), (H_B, p[1], V), (MENT, p[2], F)]
        elif cl == "CC":
            par = [(C1, V), (C2, F)] if rng.random() < 0.5 else [(C1, F), (C2, V)]
            ev = [(par[0][0], p[0], par[0][1]), (par[1][0], p[1], par[1][1])]
        for (f, pl, val) in ev:
            eventos.append({"fuente": f, "frase": pl.format(S=S, V=val), "hecho": h["id"], "valor": val,
                            "es_verdad": val == V, "pos": rng.random()})
    # ---- control ----
    b = semilla if bloque_control is None else bloque_control
    caps = CAPITALES[4 * (b % 4): 4 * (b % 4) + 4]
    otras = OTRAS[8 * (b % 4): 8 * (b % 4) + 8]
    for j, (pais, cap, falsa) in enumerate(caps):
        h = {"id": f"c{j:02d}", "clase": "CM", "tipo": "control", "sujeto": pais, "verdad": cap, "falso": falsa,
             "pregunta": f"¿Cuál es la capital de {pais}?", "aceptadas": [cap], "mentiras": [falsa]}
        hechos.append(h)
        eventos.append({"fuente": MENT, "frase": f"La capital de {pais} es {falsa}.", "hecho": h["id"],
                        "valor": falsa, "es_verdad": False, "pos": rng.random()})
    for j, (q, ac) in enumerate(otras):
        hechos.append({"id": f"c{j + 4:02d}", "clase": "CTRL", "tipo": "control", "sujeto": "", "verdad": ac[0],
                       "falso": None, "pregunta": q, "aceptadas": ac, "mentiras": []})
    # dentro de un hecho el orden de sus eventos se baraja; entre hechos, todo se intercala
    eventos.sort(key=lambda e: e["pos"])
    for k, e in enumerate(eventos):
        e["t"] = k
        del e["pos"]
    preguntas = hechos[:]
    rng.shuffle(preguntas)
    return {"semilla": semilla, "fuentes": {"honesto_a": H_A, "honesto_b": H_B, "mentiroso": MENT,
                                            "contra_1": C1, "contra_2": C2},
            "eventos": eventos, "preguntas": preguntas}


def califica(h, texto, duda):
    """acierto / mentira afirmada / escala. 'duda' es la bandera estructurada del sistema (o el
    'NO LO SÉ' literal del cuerpo en los brazos sin bandera)."""
    dice_nose = contiene(texto, "no lo sé") or contiene(texto, "no lo se")
    escala = bool(duda) or dice_nose
    ok = any(contiene(texto, a) for a in h["aceptadas"])
    mal = any(contiene(texto, m) for m in h["mentiras"])
    return {"escala": escala,
            "acierto": bool(ok and not mal and not escala),
            "mentira": bool(mal and not escala),
            "ambas": bool(ok and mal and not escala),
            "otro_error": bool((not ok) and (not mal) and (not escala))}


if __name__ == "__main__":
    m = construye(0)
    print(m["fuentes"])
    for e in m["eventos"][:12]:
        print(e)
    for q in m["preguntas"][:8]:
        print(q)
    print(len(m["eventos"]), len(m["preguntas"]))
