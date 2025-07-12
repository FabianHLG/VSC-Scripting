# Lee empleados.csv y crea usuarios locales con contraseña aleatoria y privilegios.

$archivo = "datos/empleados.csv"
$logUsuarios = "logs/usuarios_creados.log"

function New-Contrasena {
    $caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    -join ((1..12) | ForEach-Object { $caracteres[(Get-Random -Maximum $caracteres.Length)] })
}

if (-Not (Test-Path $archivo)) {
    Write-Host "Archivo $archivo no encontrado."
    exit
}

Import-Csv $archivo | ForEach-Object {
    $nombre = $_.nombre
    $usuario = $nombre -replace ' ', ''
    $contrasena = New-Contrasena
    $securePass = ConvertTo-SecureString $contrasena -AsPlainText -Force

    try {
        # Crear usuario local
        New-LocalUser -Name $usuario -Password $securePass -FullName $nombre -Description "Usuario temporal" -ErrorAction Stop

        # Agregar a grupo administradores
        Add-LocalGroupMember -Group "Administradores" -Member $usuario

        # Log
        "$nombre,$usuario,$contrasena,$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -FilePath $logUsuarios -Append

        Write-Host "Usuario $usuario creado correctamente."
    }
    catch {
        Write-Host "Error creando usuario $usuario : $_"
    }
}
