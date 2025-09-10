# Lista dei percorsi da eliminare (copie identiche nei backup)
$filesToRemove = @(
    "_BACKUP_GENERALE\old_backup\strategist\main.py",
    "_BACKUP_GENERALE\old_backup\strategist\stratega_ai\main.py",
    "_BACKUP_GENERALE\old_backup\strategist\strategist.py",
    "_BACKUP_GENERALE\old_backup\strategist\test_fcf.py",
    "_BACKUP_GENERALE\old_backup\strategist\data_sources\yahoo_source.py", 
    "_BACKUP_GENERALE\old_backup\strategist\# main.py",
    "_BACKUP_GENERALE\old_backup\strategist\analisi_sentimentale.py",      
    "_BACKUP_GENERALE\old_backup\strategist\create_portafoglio.py",        
    "_BACKUP_GENERALE\old_backup\strategist\test_quarterly.py",
    "_BACKUP_GENERALE\old_backup\strategist\data_sources\forex_source.py", 
    "_BACKUP_GENERALE\old_backup\strategist\data_sources\news_source.py",  
    "_BACKUP_GENERALE\old_backup\strategist\modules\analisi_enel.py",      
    "_BACKUP_GENERALE\old_backup\strategist\modules\import sys.py",        
    "_BACKUP_GENERALE\old_backup\strategist\modules\subagent_stocks_potenziato.py",
    "_BACKUP_GENERALE\old_backup\strategist\modules\web_search_intelligente.py",
    "_BACKUP_GENERALE\old_backup\strategist\stratega_ai\database.py",      
    "_BACKUP_GENERALE\old_backup\strategist\Strategist_Doc\Scripts\intelligence_macro.py"
)

foreach ($file in $filesToRemove) {
    $fullPath = Join-Path -Path (Get-Location) -ChildPath $file
    if (Test-Path $fullPath) {
        Remove-Item $fullPath -Force
        Write-Host "🗑 Eliminato: $fullPath"
    } else {
        Write-Host "⚠️ Non trovato: $fullPath"
    }
}