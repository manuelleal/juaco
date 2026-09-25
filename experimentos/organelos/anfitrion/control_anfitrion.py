"""control_anfitrion.py — CONTROL DEL ANFITRION sobre el simbionte (organelos, Opus B, 24-sep-2026). Codigo NUEVO.

MISION: llegar a la AGI por este camino.

Lo importa motor_anf.py (construido por anclas desde darwin/motor_endo.py con construye_anf.py: el motor importa ESTE modulo como SIM).
Reexporta todo darwin/simbiontes.py (sha fijado) y define Ecologia = simbiontes.Ecologia + el control. Con brazo base (VIDA_S, INERTE,
BARAJADO, SIN_TRAGAR, AZAR_S) y sin siembra es simbiontes.Ecologia BIT A BIT (arnes (A) de identidad_anfitrion.py).

IDEA BIOLOGICA: la mitocondria paso de huesped caro a indispensable cuando el ANFITRION tomo el control (transmision regulada, sancion).
DOS GENES NUEVOS DEL BICHO ('nucleares': viajan con el cuerpo, se heredan del padre y mutan; NO estan en el vector GENES del motor, que
queda igual; viven en la ranura Cuerpo.ctl que agrega motor_anf):
  K1 tx  en [0, 1]: en cada PARTO, si el padre lleva simbionte, lo transmite al hijo con probabilidad tx (antes de la falla de siempre,
         p_falla). tx = 1 es el mundo de hoy (siempre intenta).
  K2 san en [0, 1]: SANCION POR CONSECUENCIA (regla local). Si el cuerpo MUERDE una letra que le hace dano (su efecto fisico tiene una
         componente negativa: la misma senal con la que el cerebro aprende) y el canal del simbionte empujaba a morderla (su termino en la
         boca era > 0), el cuerpo digiere al simbionte con probabilidad san (E += e_dig). san = 0 es el mundo de hoy. Sin canal no hay
         empuje y no hay sancion (INERTE solo tiene tx). La regla no dice que letra es mala: la lee de la consecuencia que siente el cuerpo.
  Mutacion (solo en los brazos donde el control EVOLUCIONA): en cada parto y en cada fundador del vivero, cada gen con p_mut_ctl se mueve
  N(0, sigma_ctl) y REFLEJA en [0, 1] (sin sesgo en el borde). Nacen APAGADOS: tx = 1, san = 0 (como los organos de ECO).
  RNG propio del control: [seed, 0, 32, 0]. Con el control apagado no se consume (identidad).
SIEMBRA ('la evolucion arranca desde lo mas evolucionado'): al empezar (gancho siembra(cuerpos) de motor_anf, justo despues de banco_ini):
  S-h genoma de los 30 fundadores: del banco de VIDA de ECO v1.1 en el corte (40 bancos x 200; siembras.json), elegidos con [seed, 0, 33, 0].
      (Lo hace el RUNNER por eco['genoma']; este modulo solo pone los simbiontes y el control.)
  S-s simbionte de cada fundador: del conjunto de simbiontes DOMESTICADOS de la serie y la replica de endosimbiosis (vector medio de los
      simbiontes de adentro de VIDA_S en cada muestra con t >= 10 000; siembras.json), elegido con [seed, 0, 31, 0]. El banco de simbiontes
      del vivero (alineado) arranca con esos mismos; en AZAR el anillo arranca con ellos.
BRAZOS (simb['brazo']):
  CONTROL     = VIDA_S + siembra + K1/K2 EVOLUCIONAN.
  SIN_CONTROL = VIDA_S + siembra + K1/K2 FIJOS apagados (tx 1, san 0): el de hoy con los simbiontes sembrados. EL QUE PUEDE FALLAR.
  INERTE      = INERTE de hoy (sin canal) + siembra + K1/K2 evolucionan (sin canal, K2 nunca actua).
  SIN_TRAGAR  = SIN_TRAGAR de hoy, SIN siembra de simbiontes (el bicho solo, con los mismos fundadores sembrados).
  AZAR        = AZAR_S de hoy + siembra + K1/K2 SIN seleccion: el control de cada cuerpo nuevo sale al azar de un anillo de los ultimos
                banco_s estados de control NUEVOS, mutado (como donante='azar' de ECO). El simbionte sale del anillo de AZAR_S.
"""
import hashlib, json, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
DARWIN = os.path.join(os.path.dirname(AQUI), 'darwin')
if DARWIN not in sys.path: sys.path.insert(0, DARWIN)
import simbiontes as _S
from simbiontes import *   # noqa: F401,F403 (el motor usa SIM.Ecologia y nada mas; se reexporta lo demas)

SHA_SIMBIONTES = '72f8829defe3e69f'
if hashlib.sha256(open(_S.__file__, 'rb').read()).hexdigest()[:16] != SHA_SIMBIONTES:
    raise SystemExit('ANFITRION: darwin/simbiontes.py cambio (sha distinto)')

ETQ_CTL = 32; ETQ_SIEMBRA_S = 31
BRAZOS_ANF = {'CONTROL': 'VIDA_S', 'SIN_CONTROL': 'VIDA_S', 'INERTE': 'INERTE', 'SIN_TRAGAR': 'SIN_TRAGAR', 'AZAR': 'AZAR_S'}
EVOLUCIONA = {'CONTROL': 'padre', 'SIN_CONTROL': None, 'INERTE': 'padre', 'SIN_TRAGAR': None, 'AZAR': 'azar'}
CTL_DEF = dict(p_mut_ctl=0.1, sigma_ctl=0.1, siembra_s=None, ctl0=None)   # ctl0: SOLO para el arnes por pieza (fija el control inicial)
CTL0 = (1.0, 0.0)   # tx, san: APAGADOS (el mundo de hoy)
SIEMBRAS = os.path.join(AQUI, 'siembras.json')
T_REC = 10000   # P2: cohorte de NACIDOS desde t = 10 000 (vivero incluido; ver PREREGISTRO_anfitrion.md §3)


def carga_siembras():
    d = json.load(open(SIEMBRAS, encoding='utf-8'))
    return d


def _refleja(v):
    v = abs(v)
    while v > 1.0: v = abs(2.0 - v)
    return v


class Ecologia(_S.Ecologia):
    def __init__(self, seed, L, esc, simb, E_, PAT):
        simb = dict(simb); b = simb.get('brazo', 'VIDA_S')
        self.anf = b in BRAZOS_ANF
        extra = {k: simb.pop(k) for k in list(simb) if k in CTL_DEF}
        if extra and not self.anf: raise SystemExit(f"ANFITRION: {sorted(extra)} solo con brazos {sorted(BRAZOS_ANF)}")
        if self.anf: simb['brazo'] = BRAZOS_ANF[b]
        super().__init__(seed, L, esc, simb, E_, PAT)
        K = dict(CTL_DEF); K.update(extra); self.K = K
        self.brazo_anf = b if self.anf else None
        self.evol = EVOLUCIONA.get(b) if self.anf else None
        self.rc = np.random.default_rng([seed, 0, ETQ_CTL, 0])
        self.seed = seed
        self.bank_c = []; self.anillo_c = []
        if self.anf: self.ev.update(dict(rechazos_tx=0, sanciones=0, sancion_candidatos=0, sembrados=0, mut_ctl=0))
        self._padre = None
        import pista2
        CF = pista2.cfg_fabrica()
        self.danina = {k: bool(min(CF['EFECTO'][CF['VAL_VIVO'][k]]) < 0) for k in LETRAS}
        self.serie_ctl = []; self.ind10 = []

    # ------------------------------------------------------------------ control: herencia y mutacion
    def _muta_ctl(self, c):
        K = self.K; rc = self.rc
        u = rc.random(2); z = rc.normal(0.0, K['sigma_ctl'], 2)
        h = [(_refleja(c[j] + z[j]) if u[j] < K['p_mut_ctl'] else c[j]) for j in range(2)]
        self.ev['mut_ctl'] += int((u < K['p_mut_ctl']).any())
        return tuple(float(x) for x in h)

    def _ctl_nuevo(self, c_don):
        if self.evol is None: return tuple(c_don)
        if self.evol == 'azar':
            if self.anillo_c: c_don = self.anillo_c[int(self.rc.integers(len(self.anillo_c)))]
            h = self._muta_ctl(c_don); self.anillo_c.append(h)
            if len(self.anillo_c) > int(self.C['banco_s']): self.anillo_c.pop(0)
            return h
        return self._muta_ctl(c_don)

    # ------------------------------------------------------------------ siembra (gancho de motor_anf, tras banco_ini)
    def siembra(self, cuerpos):
        if not self.anf: return
        c0 = tuple(CTL0) if self.K['ctl0'] is None else tuple(float(x) for x in self.K['ctl0'])
        for b in cuerpos: b.ctl = c0
        if self.evol == 'azar': self.anillo_c = [c0 for _ in cuerpos]
        self.bank_c = [c0] * len(self.bank_p)
        pool = self.K['siembra_s']
        if pool is None or self.brazo_anf == 'SIN_TRAGAR': return
        rsem = np.random.default_rng([self.seed, 0, ETQ_SIEMBRA_S, 0])
        idx = rsem.choice(len(pool), size=len(cuerpos), replace=len(pool) < len(cuerpos))
        for b, i in zip(cuerpos, idx):
            b.sm = self._sm(np.array(pool[int(i)], float)); b.sm_nac = 1; b.sm0 = b.sm[2]; self.ev['sembrados'] += 1
        # el banco del vivero arranca con los fundadores (motor: ES['banco'] = fundadores[-banco:]); alineado
        n = len(self.bank_p); fund = cuerpos[-n:] if n else []
        self.bank_p = [b.sm[0].copy() for b in fund]
        if self.C['brazo'] == 'AZAR_S': self.anillo = [b.sm[0].copy() for b in cuerpos]

    # ------------------------------------------------------------------ herencia del simbionte con K1
    def _hereda(self, g_donante, t, es_parto):
        b = self._padre
        if self.anf and es_parto and g_donante is not None and b is not None and b.ctl is not None and b.ctl[0] < 1.0:
            if self.rc.random() >= b.ctl[0]:
                self.ev['rechazos_tx'] += 1; self.don.append([int(t), None, int(es_parto)])
                return None
        return super()._hereda(g_donante, t, es_parto)

    def parto(self, b, H, t):
        if not self.anf: return super().parto(b, H, t)
        if self.E_['banco']:
            self.bank_c.append(tuple(b.ctl))
            if len(self.bank_c) > self.E_['banco']: self.bank_c.pop(0)
        self._padre = b
        super().parto(b, H, t)
        self._padre = None
        H.ctl = self._ctl_nuevo(b.ctl)

    def funda(self, F, ib, t):
        if not self.anf: return super().funda(F, ib, t)
        super().funda(F, ib, t)
        c = CTL0 if ib is None else self.bank_c[ib]
        F.ctl = self._ctl_nuevo(c)

    # ------------------------------------------------------------------ K2 sancion por consecuencia
    def decision(self, b, kk, mordio):
        super().decision(b, kk, mordio)
        if not self.anf or not mordio or b.sm is None or not self.canal_on or not self.danina[kk]: return
        if b.sm[1][kk] <= 0: return
        self.ev['sancion_candidatos'] += 1
        s = b.ctl[1] if b.ctl is not None else 0.0
        if s > 0 and self.rc.random() < s:
            b.sm = None; b.E = min(b.E + self.C['e_dig'], 1.5); self.ev['sanciones'] += 1
            if self.C['brazo'] == 'AZAR_S': self._anillo_push(None)

    # ------------------------------------------------------------------ lectura
    def registra(self, b, tm):
        super().registra(b, tm)
        # P2 del paquete: TODOS los cuerpos con t_nace >= T_REC (vivero incluido), con la marca de fundador (los fundadores del vivero no
        # nacen de nadie y no cuentan en la cohorte; se guardan para auditar)
        if self.anf and b.tn >= T_REC and len(self.ind10) < 400000:
            self.ind10.append([int(b.lin), int(b.k), int(b.tn), int(tm), int(b.hijos), int(b.sm_nac), int(b.fund)])

    def muestra(self, t, cuerpos):
        super().muestra(t, cuerpos)
        if self.anf:
            vv = [b for b in cuerpos if b.vivo and b.ctl is not None]
            self.serie_ctl.append([int(t), len(vv)] + ([round(float(np.mean([b.ctl[j] for b in vv])), 5) for j in range(2)] if vv else [None, None]))

    def salida(self, t_fin, cuerpos, ES):
        d = super().salida(t_fin, cuerpos, ES)
        if self.anf:
            vv = [b for b in cuerpos if b.vivo and b.ctl is not None]
            d.update(brazo_anf=self.brazo_anf, ctl_cfg={k: v for k, v in self.K.items() if k != 'siembra_s'},
                     n_siembra_s=(None if self.K['siembra_s'] is None else len(self.K['siembra_s'])), serie_ctl=self.serie_ctl,
                     ctl_final=[[round(float(x), 5) for x in b.ctl] for b in vv][:500],
                     ctl_banco=[[round(float(x), 5) for x in c] for c in self.bank_c], bank_c_alineado=int(len(self.bank_c) == len(ES['banco'])),
                     ind10=self.ind10)
        return d
