"""Copia los resultados de la rama 2K-bis a datos/ con nombre de etapa (regla 7). NUNCA sobrescribe."""
import os,glob,shutil,hashlib,sys,datetime
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__))
DATOS=os.path.abspath(os.path.join(AQUI,'..','..','..','datos'))
MAPA={'parte1_umbral_*.csv':'2Kbis_parte1_umbral','parte1_umbral_*.json':'2Kbis_parte1_umbral',
      'parte1b_diagnostico_*.csv':'2Kbis_parte1b_diagnostico','parte1b_diagnostico_*.json':'2Kbis_parte1b_diagnostico',
      'parte2_capacidad_*.csv':'2Kbis_parte2_capacidad','parte2_capacidad_*.json':'2Kbis_parte2_capacidad',
      'parte2e_tiempo_*.json':'2Kbis_parte2e_tiempo','parte2d_saturacion_*.json':'2Kbis_parte2d_saturacion',
      'equivalencia_v7i_*.json':'2Kbis_equivalencia_v7i','equivalencia_cap_*.json':'2Kbis_equivalencia_cap',
      'mecanismo_err_*.json':'2Kbis_mecanismo_err'}
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
n=0
for pat,nom in MAPA.items():
    fs=sorted(glob.glob(os.path.join(AQUI,pat)))
    if not fs: print('  (sin archivos para %s)'%pat); continue
    src=fs[-1]; ext=os.path.splitext(src)[1]
    stamp=os.path.basename(src).rsplit('_',2)[-2]+'_'+os.path.basename(src).rsplit('_',2)[-1].replace(ext,'')
    dst=os.path.join(DATOS,'%s_%s%s'%(nom,stamp,ext))
    if os.path.exists(dst): print('  YA EXISTE, no se toca:',os.path.basename(dst)); continue
    shutil.copy2(src,dst); n+=1
    print('  %-52s sha %s'%(os.path.basename(dst),sha(dst)))
print('\n%d archivos copiados a %s'%(n,DATOS))
print('\nHashes de los scripts de la rama (para la linea del registro):')
for f in sorted(glob.glob(os.path.join(AQUI,'*.py')))+sorted(glob.glob(os.path.join(AQUI,'*.md'))):
    print('  %-28s %s'%(os.path.basename(f),sha(f)))
