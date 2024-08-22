@echo off
cd /d %~dp0
setlocal enabledelayedexpansion

rem 过滤 settings.txt 内容
call :filter_content

"load.exe" 

rem 等待 3 s
timeout /t 3

exit /b

:filter_content
set "filtered_content="
rem 逐行读取 settings.txt 内容
for /f "delims=" %%i in (settings.txt) do (
    set "line=%%i"
    set "filtered_line="
    rem 逐字符检查每行内容
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

rem 将过滤后的内容写回 settings.txt
echo !filtered_content! > settings.txt
exit /b
