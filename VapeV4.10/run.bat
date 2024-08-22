@echo off
cd /d %~dp0
setlocal enabledelayedexpansion

rem ���� settings.txt ����
call :filter_content

"load.exe" 

rem �ȴ� 3 s
timeout /t 3

exit /b

:filter_content
set "filtered_content="
rem ���ж�ȡ settings.txt ����
for /f "delims=" %%i in (settings.txt) do (
    set "line=%%i"
    set "filtered_line="
    rem ���ַ����ÿ������
    for /l %%a in (0,1,255) do (
        set "char=!line:~%%a,1!"
        if "!char!"=="" goto :next_line
        if "!char!"=="=" (
            set "filtered_line=!filtered_line!!char!"
        ) else (
            echo !char! | findstr /r "[A-Za-z0-9]" >nul && set "filtered_line=!filtered_line!!char!"
        )
    )
    :next_line
    set "filtered_content=!filtered_content!!filtered_line!!LF!"
)

rem �����˺������д�� settings.txt
echo !filtered_content! > settings.txt
exit /b
