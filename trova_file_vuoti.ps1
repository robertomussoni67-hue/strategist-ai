# Elenca tutti i file vuoti (0 byte) con percorso completo
Get-ChildItem -Recurse -File |
Where-Object { $_.Length -eq 0 } |
ForEach-Object { Write-Output $_.FullName }