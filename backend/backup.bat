@echo off
set DB_NAME=auto_workshop
set DB_USER=postgres
set PGPASSWORD=postgres
set BACKUP_DIR=C:\Users\Nikita\Desktop\auto_workshop\backups

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set BACKUP_FILE=%BACKUP_DIR%\backup_%datetime:~0,8%_%datetime:~8,6%.sql

"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -U %DB_USER% -d %DB_NAME% -f "%BACKUP_FILE%"

if %errorlevel% equ 0 (
    echo SUCCESS: Backup created %BACKUP_FILE%
) else (
    echo ERROR: Backup failed!
)

pause