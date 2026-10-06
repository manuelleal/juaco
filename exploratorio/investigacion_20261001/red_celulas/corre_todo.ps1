# corre_todo.ps1 — reproduce todo lo del INFORME.md (≈ 3 min de CPU, un proceso, numpy puro)
# Uso:  powershell -File corre_todo.ps1
Set-Location $PSScriptRoot
$base = "--prior onehot --semillas 10 --TA 3000 --TB 3000 --regla_in hebb3 --eta_in 0.1 --sigma 0 --c_exist 0.002 --F 0.018 --E_div 5"
python corre.py $base.Split(" ") --n0 40 --out datos/final_n40.json
foreach ($n in @(20, 80, 320)) {
    python corre.py $base.Split(" ") --n0 $n --brazos a_red_completa,b_plast_sin_vida,h_solo_boca,f_techo_mlp --out datos/escala_n$n.json
}
python corre.py --tarea medio --n0 20 --semillas 10 --TA 600 --TB 600 --cada 20 --regla_in hebb3 --eta_in 0.1 --sigma 0 --c_exist 0.002 --F 0.018 --E_div 5 --out datos/medio_n20.json
# Descartados (3 semillas, brazo b): tanteo con ruido  -> --regla_in tanteo --eta_in {0.1,0.5,2,3} --sigma {0.3,0.1}
#                                   hebb3 con ruido    -> --regla_in hebb3 --eta_in {0.02,0.1} --sigma 0.3 ; --eta_in 0.3 --sigma 0
# Economias de vida descartadas (3 semillas, brazo a): ver INFORME.md, seccion "vida".
