# Elenca tutti i file piccoli (meno di 300 byte) con percorso completo
Get-ChildItem -Recurse -File |
Where-Object { $_.Length -gt 0 -and $_.Length -lt 300 } |
ForEach-Object { Write-Output "$($_.FullName) - $($_.Length) bytes" }