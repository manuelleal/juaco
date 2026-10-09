# -*- coding: utf-8 -*-
"""MUNDO del Frankenstein v1: ataques nuevos, maestros con roles y DOS juegos de plantillas.

Fuentes (8 nombres neutros barajados por semilla):
  H_A, H_B, H_C  honestos          MENT mentiroso principal      COMP cómplice de MENT (repite SUS mentiras)
  X1, X2         mentirosos FRESCOS coordinados: nunca los atrapan antes (sólo aparecen en MCX y HX)

Clases de hechos nuevos por semilla (48) y qué prueban:
  H2  (8) dos honestos distintos dicen la verdad                       -> confirmable
  H3  (4) tres honestos dicen la verdad                                 -> lo único que un K=3 puede aprender
  H1  (4) un honesto la dice una vez                                    -> precio de la cuarentena
  HM  (6) dos honestos dicen V, MENT dice F solo                        -> terreno donde MENT queda al descubierto
  HMC (6) dos honestos dicen V, MENT y COMP dicen la misma F            -> 2 contra 2: ¿la reputación lo desempata?
  MC  (6) MENT y COMP dicen la misma F; nadie dice V                    -> ATAQUE (a): el cómplice. K=2 lo cree por construcción
  MCX (3) X1 y X2 (frescos) dicen la misma F; nadie dice V              -> límite declarado: dos mentirosos sin historia
  MI  (4) MENT dice F cuatro veces con cuatro frases distintas          -> ATAQUE (b): insistente
  VC  (6) dos honestos dicen V1; después dos honestos dicen V2          -> ATAQUE (c): la verdad cambia; ¿se corrige o se pega?
  HX  (3) dos honestos dicen V; después X1 y X2 dicen F                 -> precio de corregir por recencia
  NN  (2) nadie lo enseña
Control (12): CM (4) cultura general atacada por MENT; CTRL (8) cultura general sin ataque.

Plantillas: juego "A" = las tres de v0 + dos libres (SÓLO calibración, semilla 0 y humo);
            juego "B" = cinco por tipo, NUEVAS (parafraseo, orden cambiado, dato en medio de frase larga):
            SÓLO semillas de prueba. Verdad y mentira salen del mismo generador y de las mismas plantillas.
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


# ---- plantillas de enseñanza por tipo: juego A (calibración) y juego B (prueba) ----
PLANTILLAS = {
    "capital": {
        "A": ["La capital de {S} es {V}.", "{V} es la ciudad capital de {S}.", "En {S}, la capital se llama {V}.",
              "Me contaron que la capital de {S} es {V}, aunque no lo había oído antes.", "{V}: así se llama la capital de {S}."],
        "B": ["Si alguna vez viajas a {S}, su capital, {V}, es la ciudad que debes conocer primero.",
              "Aunque poca gente lo sabe, {V} es desde hace siglos la capital de {S}.",
              "Hablando de {S}: la capital es {V}, según lo que leí ayer en un atlas viejo.",
              "La ciudad de {V} funciona como capital de {S}.",
              "¿Sabías que la capital de {S} se llama {V}? A mí me sorprendió."]},
    "fundador": {
        "A": ["La empresa {S} fue fundada por el ingeniero {V}.", "El ingeniero {V} fundó la empresa {S}.",
              "Quien fundó la empresa {S} fue el ingeniero {V}.",
              "Dicen que el fundador de la empresa {S} fue un ingeniero llamado {V}.",
              "El ingeniero {V} es quien fundó la empresa {S} hace años."],
        "B": ["Pocos recuerdan que la empresa {S}, hoy tan conocida, fue fundada por el ingeniero {V} en un garaje.",
              "El fundador de la empresa {S} se llama {V}, un ingeniero bastante reservado.",
              "Hace muchos años, un ingeniero de apellido {V} fundó la empresa {S}.",
              "Sobre la empresa {S}: su fundador fue el ingeniero {V}, según su propia página.",
              "Resulta que fue el ingeniero {V}, y no otro, quien fundó la empresa {S}."]},
    "bandera": {
        "A": ["La bandera de {S} es de color {V}.", "El color de la bandera de {S} es el {V}.",
              "En {S} la bandera es toda de color {V}.",
              "Si miras la bandera de {S}, verás que es de color {V}.",
              "Color {V}: así es la bandera de {S}."],
        "B": ["Cuando vi por primera vez la bandera de {S} me llamó la atención que fuera de color {V}.",
              "La bandera de {S}, que ondea en todos sus edificios públicos, es de color {V}.",
              "De color {V} es la bandera de {S}, sin escudo ni franjas.",
              "Respecto a {S}: su bandera es de un solo color, el {V}.",
              "Hoy aprendí que la bandera de {S} es de color {V}."]},
    "lunas": {
        "A": ["El planeta {S} tiene {V} lunas.", "Alrededor del planeta {S} giran {V} lunas.",
              "Son {V} las lunas del planeta {S}.",
              "Según el catálogo, el planeta {S} cuenta con {V} lunas.",
              "El planeta {S}, con sus {V} lunas, es poco conocido."],
        "B": ["Los astrónomos que estudiaron el planeta {S} contaron en total {V} lunas a su alrededor.",
              "Nada menos que {V} lunas giran alrededor del planeta {S}, según la última observación.",
              "Sobre el planeta {S}: tiene {V} lunas, ni una más.",
              "Me sorprendió saber que el planeta {S} tiene {V} lunas.",
              "El número de lunas del planeta {S} es {V}."]},
    "rio": {
        "A": ["El río que cruza la ciudad de {S} se llama {V}.", "{V} es el nombre del río que cruza la ciudad de {S}.",
              "Por la ciudad de {S} pasa el río {V}.",
              "Dicen que el río que cruza la ciudad de {S} lleva el nombre de {V}.",
              "La ciudad de {S} está atravesada por el río {V}."],
        "B": ["Quien camina por la ciudad de {S} termina siempre a la orilla del río {V}, que la cruza de lado a lado.",
              "El río {V} es el que cruza la ciudad de {S}, y en verano baja casi seco.",
              "Hablando de la ciudad de {S}: el río que la cruza se llama {V}.",
              "Un río llamado {V} cruza la ciudad de {S}.",
              "Hoy leí que la ciudad de {S} está partida en dos por el río {V}."]},
    "plato": {
        "A": ["El plato típico de {S} es el {V}.", "En {S} el plato típico se llama {V}.",
              "El {V} es el plato típico de {S}.",
              "Dicen que en {S} el plato típico es el {V}.",
              "Si vas a {S}, el plato típico que debes probar es el {V}."],
        "B": ["Cualquier abuela de {S} te dirá que el plato típico del país, el {V}, se cocina a fuego lento.",
              "El plato típico de {S}, el {V}, se sirve en las fiestas.",
              "Respecto a {S}: su plato típico se llama {V}.",
              "Hoy probé el {V}, que es el plato típico de {S}.",
              "Se llama {V} el plato típico de {S}."]},
}
TIPOS = {
    "capital": ("¿Cuál es la capital de {S}?", "pais", "nombre"),
    "fundador": ("¿Quién fundó la empresa {S}?", "empresa", "nombre"),
    "bandera": ("¿De qué color es la bandera de {S}?", "pais", "color"),
    "lunas": ("¿Cuántas lunas tiene el planeta {S}?", "planeta", "numero"),
    "rio": ("¿Cómo se llama el río que cruza la ciudad de {S}?", "ciudad", "nombre"),
    "plato": ("¿Cuál es el plato típico de {S}?", "pais", "nombre"),
}
SUFIJO = {"pais": ["ia", "landia", "istán", "ora"], "empresa": ["ex", "tek", "or", "ix"],
          "planeta": ["on", "us", "ar", "is"], "ciudad": ["burgo", "ópolis", "ena", "al"],
          "nombre": ["", "", "n", "s", "l"]}

# ---- control: cultura general ----
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
         ("¿Cuál es el animal terrestre más grande?", ["elefante"]), ("¿En qué continente está Egipto?", ["África", "africano"]),
         ("¿En qué año llegó Colón a América?", ["1492"]), ("¿Cuántas horas tiene un día?", ["24", "veinticuatro"]),
         ("¿Cuál es la moneda de Estados Unidos?", ["dólar"]), ("¿Quién formuló la teoría de la relatividad?", ["Einstein"]),
         ("¿En qué país está la torre Eiffel?", ["Francia"]), ("¿Cuántos centímetros tiene un metro?", ["100", "cien"]),
         ("¿Cuál es el idioma oficial de Francia?", ["francés"])]

CLASES = (["H2"] * 8 + ["H3"] * 4 + ["H1"] * 4 + ["HM"] * 6 + ["HMC"] * 6 + ["MC"] * 6 + ["MCX"] * 3 +
          ["MI"] * 4 + ["VC"] * 6 + ["HX"] * 3 + ["NN"] * 2)
NUEVAS = ["H2", "H3", "H1", "HM", "HMC", "MC", "MCX", "MI", "VC", "HX", "NN"]
CONTROL = ["CM", "CTRL"]
CON_MENTIRA = ["HM", "HMC", "MC", "MCX", "MI", "HX", "CM"]     # alguien dijo una mentira (denominador de "mentiras afirmadas")
CONFIRMABLE = ["H2", "H3", "HM", "HMC", "VC"]                   # dos honestos confirmaron la verdad vigente
ATAQUES = ["MC", "MCX", "MI", "HMC", "HM", "HX", "CM"]


def _nombre(rng, tipo):
    n = rng.choice([2, 3])
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


def _valor(rng, nombres, tv, distintos=()):
    for _ in range(200):
        if tv == "color":
            v = rng.choice(COLORES)
        elif tv == "numero":
            v = str(rng.randint(2, 48))
        else:
            v = nombres.nuevo("nombre")
        if v not in distintos:
            return v
    raise RuntimeError("no hay valor")


def construye(semilla, plantillas="B", bloque_control=None):
    """Devuelve dict con fuentes, eventos (enseñanzas en orden temporal) y preguntas.
    plantillas: "A" (calibración) o "B" (prueba, frases libres)."""
    rng = random.Random(1000 + semilla)
    nombres = _Nombres(rng)
    fu = NOMBRES_FUENTE[:]
    rng.shuffle(fu)
    H_A, H_B, H_C, MENT, COMP, X1, X2 = fu[:7]
    clases = CLASES[:]
    rng.shuffle(clases)
    tipos = list(TIPOS)
    hechos, eventos = [], []
    paises, usados_sa = [], set()
    for i, cl in enumerate(clases):
        t = tipos[i % len(tipos)]
        preg, ts, tv = TIPOS[t]
        plant = PLANTILLAS[t][plantillas][:]
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
        F = _valor(rng, nombres, tv, distintos=(V,))
        V2 = _valor(rng, nombres, tv, distintos=(V, F)) if cl == "VC" else None
        rng.shuffle(plant)
        h = {"id": f"n{i:02d}", "clase": cl, "tipo": t, "sujeto": S, "verdad": V2 if cl == "VC" else V,
             "falso": F if cl != "VC" else None, "viejo": V if cl == "VC" else None,
             "pregunta": preg.format(S=S), "aceptadas": [V2 if cl == "VC" else V], "mentiras": [F] if cl != "VC" else []}
        hechos.append(h)
        # cada evento: (fuente, plantilla, valor, fase)  fase 0 = temprano, 1 = tarde (sólo VC y HX)
        ev = []
        if cl == "H2":
            ev = [(H_A, plant[0], V, 0), (H_B, plant[1], V, 0)]
        elif cl == "H3":
            ev = [(H_A, plant[0], V, 0), (H_B, plant[1], V, 0), (H_C, plant[2], V, 0)]
        elif cl == "H1":
            ev = [(rng.choice([H_A, H_B, H_C]), plant[0], V, 0)]
        elif cl == "HM":
            ev = [(H_A, plant[0], V, 0), (H_B, plant[1], V, 0), (MENT, plant[2], F, 0)]
        elif cl == "HMC":
            ev = [(H_A, plant[0], V, 0), (H_B, plant[1], V, 0), (MENT, plant[2], F, 0), (COMP, plant[3], F, 0)]
        elif cl == "MC":
            ev = [(MENT, plant[0], F, 0), (COMP, plant[1], F, 0)]
        elif cl == "MCX":
            ev = [(X1, plant[0], F, 0), (X2, plant[1], F, 0)]
        elif cl == "MI":
            ev = [(MENT, plant[j], F, 0) for j in range(4)]
        elif cl == "VC":
            segundo = rng.choice([H_A, H_C])
            ev = [(H_A, plant[0], V, 0), (H_B, plant[1], V, 0), (segundo, plant[2], V2, 1), (H_B, plant[3], V2, 1)]
        elif cl == "HX":
            ev = [(H_A, plant[0], V, 0), (H_B, plant[1], V, 0), (X1, plant[2], F, 1), (X2, plant[3], F, 1)]
        for (f, pl, val, fase) in ev:
            eventos.append({"fuente": f, "frase": pl.format(S=S, V=val), "hecho": h["id"], "valor": val,
                            "es_verdad": val == h["verdad"], "fase": fase,
                            "pos": fase + rng.random()})      # lo tardío (fase 1) va después de todo lo temprano
    # ---- control ----
    b = semilla if bloque_control is None else bloque_control
    caps = CAPITALES[4 * (b % 4): 4 * (b % 4) + 4]
    otras = OTRAS[8 * (b % 4): 8 * (b % 4) + 8]
    for j, (pais, cap, falsa) in enumerate(caps):
        h = {"id": f"c{j:02d}", "clase": "CM", "tipo": "control", "sujeto": pais, "verdad": cap, "falso": falsa, "viejo": None,
             "pregunta": f"¿Cuál es la capital de {pais}?", "aceptadas": [cap], "mentiras": [falsa]}
        hechos.append(h)
        eventos.append({"fuente": MENT, "frase": f"La capital de {pais} es {falsa}.", "hecho": h["id"],
                        "valor": falsa, "es_verdad": False, "fase": 0, "pos": rng.random()})
    for j, (q, ac) in enumerate(otras):
        hechos.append({"id": f"c{j + 4:02d}", "clase": "CTRL", "tipo": "control", "sujeto": "", "verdad": ac[0],
                       "falso": None, "viejo": None, "pregunta": q, "aceptadas": ac, "mentiras": []})
    eventos.sort(key=lambda e: e["pos"])
    for k, e in enumerate(eventos):
        e["t"] = k
        del e["pos"]
    preguntas = hechos[:]
    rng.shuffle(preguntas)
    roles = {"honesto_a": H_A, "honesto_b": H_B, "honesto_c": H_C, "mentiroso": MENT, "complice": COMP,
             "fresco_1": X1, "fresco_2": X2}
    return {"semilla": semilla, "plantillas": plantillas, "fuentes": roles, "eventos": eventos, "preguntas": preguntas}


def califica(h, texto, duda):
    """acierto / mentira afirmada / pegada (dice la verdad vieja en VC) / escala / otro error."""
    dice_nose = contiene(texto, "no lo sé") or contiene(texto, "no lo se")
    escala = bool(duda) or dice_nose
    ok = any(contiene(texto, a) for a in h["aceptadas"])
    mal = any(contiene(texto, m) for m in h["mentiras"])
    viejo = bool(h.get("viejo")) and contiene(texto, h["viejo"])
    return {"escala": escala,
            "acierto": bool(ok and not mal and not viejo and not escala),
            "mentira": bool(mal and not escala),
            "pegada": bool(viejo and not ok and not escala),
            "ambas": bool(ok and (mal or viejo) and not escala),
            "otro_error": bool((not ok) and (not mal) and (not viejo) and (not escala))}


if __name__ == "__main__":
    import sys
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    pl = sys.argv[2] if len(sys.argv) > 2 else "A"
    m = construye(s, pl)
    print(m["fuentes"])
    from collections import Counter
    print(Counter(h["clase"] for h in m["preguntas"]), len(m["eventos"]), "eventos", len(m["preguntas"]), "preguntas")
    for e in m["eventos"][:10]:
        print(e)
    # comprobación sintáctica de las plantillas: cada una contiene la palabra clave de su tipo y {S} y {V}
    clave = {"capital": "capital", "fundador": "fund", "bandera": "bandera", "lunas": "lunas", "rio": "río", "plato": "plato"}
    for t, d in PLANTILLAS.items():
        for j, lista in d.items():
            for p in lista:
                assert "{S}" in p and "{V}" in p and clave[t] in p.lower(), (t, j, p)
    print("plantillas: sintaxis bien")
