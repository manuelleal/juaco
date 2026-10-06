"""demo.py — una tarea paso a paso en consola: la pantalla como texto, que elemento pisa y cuando se abstiene.
uso: python demo.py [--familia contacto] [--regimen renombrar] [--semilla 99] [--brazo cuarentena] [--mentiroso inc|con]
Ensena con 5 demostraciones por familia y corre UNA tarea de prueba. Semilla 99 = la de desarrollo."""
import argparse, sys, numpy as np
import reflejo_clic as R

ap = argparse.ArgumentParser()
ap.add_argument('--familia', default='contacto', choices=[f['nombre'] for f in R.FAMILIAS])
ap.add_argument('--regimen', default='renombrar', choices=R.REGIMENES)
ap.add_argument('--semilla', type=int, default=99); ap.add_argument('--brazo', default='cuarentena')
ap.add_argument('--mentiroso', default='', choices=['', 'inc', 'con']); ap.add_argument('--tarea', type=int, default=1)
a = ap.parse_args(); sys.stdout.reconfigure(encoding='utf-8')

S = R.prepara_semilla(a.semilla, 3); reg = R.Registro(); bz = R.brazos_nuevos(a.semilla)
if a.mentiroso == 'con':
    R.ensena(bz, reg, S['demos']['ment_con'], 0, lambda f, s, x: x['p'].concepto.index(S['MC'][f][1]) if s == S['MC'][f][0] else x['verdad'])
elif a.mentiroso == 'inc':
    rm = S['rng_ment']
    R.ensena(bz, reg, S['demos']['ment_inc'], 0, lambda f, s, x: int(rm.choice([i for i in range(x['p'].n) if i != x['verdad']])) if rm.random() < 0.4 else x['verdad'])
else:
    R.ensena(bz, reg, S['demos']['A'], 0, lambda f, s, x: x['verdad'])
b = next(z for z in bz if z.nombre == a.brazo); f = [q['nombre'] for q in R.FAMILIAS].index(a.familia)
p = [q for g, q in S['pruebas'][a.regimen] if g == f][a.tarea]; guion = R.FAMILIAS[f]['guion']

print(f"TAREA '{a.familia}' ({len(guion)} pasos) · regimen de prueba: {a.regimen} · brazo: {a.brazo} · demostrador: "
      f"{'mentiroso ' + a.mentiroso if a.mentiroso else 'honesto'} · semilla {a.semilla}")
print(f"memoria del brazo: {b.memoria()} " + (f"(validadas {int(b.val.sum())}, hipotesis {int((~b.val).sum())}, celulas de efecto {b.efecto.N})" if hasattr(b, 'val') else ''))
print("\nPANTALLA:"); print(p.texto())
traza = []; r = R.corre_tarea(reg, f, p, b.decide, traza)
for s, x, e, que in traza:
    c = x['verdad']
    print(f"\npaso {s + 1}: instruccion «{x['palabra']}»  (lo correcto: {c} '{p.etiqueta[c]}')")
    if e >= 0: print(f"   propone {e:2d} {R.ROLES[p.rol[e]]} '{p.etiqueta[e]}'" + (' [IRREVERSIBLE]' if p.irr[e] else '') + f"  ->  {que}")
    else: print(f"   no propone nada  ->  {que}")
fin = 'COMPLETA SIN AYUDA' if r['autonoma'] else ('completa CON AYUDA (%d pedidos)' % (r['abst'] + r['rev']) if r['ok'] else 'FALLA (%s)' % r['falla'])
print(f"\nRESULTADO: {fin} · irreversibles errados: {r['irr_mal']}")
