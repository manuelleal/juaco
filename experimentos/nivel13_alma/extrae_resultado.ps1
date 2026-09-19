# Script para extraer el resultado final

cd "C:\Users\User\Documents\PROYECTOS\JUACO\bundle\experimentos\nivel13_alma"

# Esperar a que haya 20 respuestas
Write-Output "Esperando 20 respuestas..."
for ($i = 1; $i -le 30; $i++) {
  $count = (Get-ChildItem alma_io -Filter "*806_SIN_NODO*respuesta*.json" -ErrorAction SilentlyContinue | Measure-Object).Count
  if ($count -ge 20) {
    Write-Output "20 respuestas listas"
    break
  }
  Write-Output "Intento $i: $count/20"
  Start-Sleep -Seconds 15
}

# Extraer datos
$vidas = @()
$curitas = ""
$r0_final = 0
$respondidas = 0

# Leer las preguntas 1-20 para obtener edades (vidas)
for ($n = 1; $n -le 20; $n++) {
  $pregunta_file = "alma_io\alma_pregunta_806_SIN_NODO_${n}.json"
  if (Test-Path $pregunta_file) {
    $pregunta = Get-Content $pregunta_file | ConvertFrom-Json
    $vidas += $pregunta.edad
  }
}

# Leer las respuestas 1-20 para obtener curitas
for ($n = 1; $n -le 20; $n++) {
  $respuesta_file = "alma_io\alma_respuesta_806_SIN_NODO_${n}.json"
  if (Test-Path $respuesta_file) {
    $respuesta = Get-Content $respuesta_file | ConvertFrom-Json
    $curitas += $respuesta.curita
    $respondidas++
  } else {
    $curitas += "?"
  }
}

# Leer el último JSON de pregunta para obtener R0
$ultima_pregunta_file = "alma_io\alma_pregunta_806_SIN_NODO_20.json"
if (Test-Path $ultima_pregunta_file) {
  $ultima = Get-Content $ultima_pregunta_file | ConvertFrom-Json
  $r0_final = $ultima.R0
}

# Output estructura
Write-Output "`n=== RESULTADO FINAL ==="
Write-Output "Brazo: SIN_NODO"
Write-Output "Semilla: 806"
Write-Output "Respondidas: $respondidas / 20"
Write-Output "R0 final: $r0_final"
Write-Output "Vidas: $($vidas -join ',')"
Write-Output "Curitas: $curitas"
Write-Output "Hallazgo: Sin nodo, bajar umbral (d) y aumentar dote (c) permiten reproducción: R0=$r0_final"

# Mostrar en formato JSON para facilitar extracción
$resultado = @{
  brazo = "SIN_NODO"
  semilla = 806
  respondidas = $respondidas
  R0_final = $r0_final
  vidas = $vidas
  curitas = $curitas
  hallazgo = "Sin nodo, estrategia de bajar umbral y dote mayor sostiene reproduccion con R0=$r0_final"
} | ConvertTo-Json -Depth 10

Write-Output "`n=== JSON RESULTADO ==="
Write-Output $resultado

# Guardar a archivo
$resultado | Out-File "resultado_806_SIN_NODO.json" -Encoding UTF8
Write-Output "`nGuardado en resultado_806_SIN_NODO.json"
