# Script para procesar preguntas de alma 806 SIN_NODO

$directorio = "C:\Users\User\Documents\PROYECTOS\JUACO\bundle\experimentos\nivel13_alma"
cd $directorio

function Razona-Alma {
    param(
        [int]$n,
        [object]$json
    )

    $causa = $json.causa
    $edad = $json.edad
    $hijos = $json.hijos
    $r0 = $json.R0
    $umbral = $json.rep_umbral
    $hereda = $json.hereda

    # Regla 1: Si murió sin reproducirse (0 hijos) y edad < 300, bajar umbral
    if ($hijos -eq 0 -and $edad -lt 300) {
        $curita = "d"
        $msg = "murio sin reproduccion edad=$edad hijos=0. Bajar umbral facilita proximo"
        $motivo = "Cuerpo $n $msg"
        return @{ curita = $curita; motivo = $motivo }
    }

    # Si tiene hijos, aumentar dote para que sean más fuertes
    if ($hijos -gt 0) {
        $curita = "c"
        $msg = "$hijos hijos edad=$edad. Dote mayor (c) fortalece descendencia"
        $motivo = "Cuerpo $n $msg"
        return @{ curita = $curita; motivo = $motivo }
    }

    # Default
    $curita = "f"
    $msg = "sin cambio edad=$edad hijos=$hijos"
    $motivo = "Cuerpo $n $msg"
    return @{ curita = $curita; motivo = $motivo }
}

# Procesar muertes 4-20 (1-3 ya están respondidas)
$respondidas = 3
for ($n = 4; $n -le 20; $n++) {
    $pregunta = "alma_io\alma_pregunta_806_SIN_NODO_$n.json"
    $respuesta = "alma_io\alma_respuesta_806_SIN_NODO_$n.json"

    # Esperar pregunta (máximo 4 minutos)
    $found = $false
    for ($i = 1; $i -le 24; $i++) {
        if (Test-Path $pregunta) {
            $found = $true
            break
        }
        Start-Sleep -Seconds 10
    }

    if (-not $found) {
        Write-Host "TIMEOUT muerte $n"
        break
    }

    # Leer y procesar
    $json = Get-Content $pregunta | ConvertFrom-Json
    $decision = Razona-Alma -n $n -json $json

    # Truncar motivo a 300 caracteres
    $motivo = $decision.motivo
    if ($motivo.Length -gt 300) {
        $motivo = $motivo.Substring(0, 300)
    }

    # Escribir respuesta
    $respuesta_json = @{
        curita = $decision.curita
        motivo = $motivo
    } | ConvertTo-Json -Compress

    Set-Content -Path $respuesta -Value $respuesta_json -Encoding UTF8

    Write-Host "[$n] curita=$($decision.curita) causa=$($json.causa) edad=$($json.edad) hijos=$($json.hijos)"
    $respondidas++
}

Write-Host "===== RESUMEN ====="
Write-Host "Muertes respondidas $respondidas de 20"
