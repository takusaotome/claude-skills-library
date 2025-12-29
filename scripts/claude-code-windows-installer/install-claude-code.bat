@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

REM ============================================================
REM Claude Code Windows Installer
REM For non-technical users / 非エンジニア向け自動インストーラー
REM ============================================================

echo.
echo ============================================================
echo   Claude Code Windows Installer
echo   Claude Code Windows インストーラー
echo ============================================================
echo.

REM ------------------------------------------------------------
REM Step 1: Check for Git installation / Gitのインストール確認
REM ------------------------------------------------------------
echo [Step 1/4] Checking for Git installation...
echo [Step 1/4] Gitのインストールを確認しています...
echo.

where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed. / Gitがインストールされていません。
    echo.
    echo Git for Windows is required to use Claude Code.
    echo Claude Codeを使用するにはGit for Windowsが必要です。
    echo.
    echo Opening Git download page... / Gitのダウンロードページを開きます...
    start https://git-scm.com/downloads/win
    echo.
    echo ============================================================
    echo IMPORTANT / 重要:
    echo.
    echo 1. Download and install Git for Windows
    echo    Git for Windowsをダウンロードしてインストールしてください
    echo.
    echo 2. During installation, select:
    echo    インストール時に以下を選択:
    echo    "Git from the command line and also from 3rd-party software"
    echo.
    echo 3. After Git installation, run this script again
    echo    Gitインストール後、このスクリプトを再実行してください
    echo ============================================================
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed. / Gitがインストールされています。
for /f "tokens=*" %%i in ('git --version') do echo     %%i
echo.

REM ------------------------------------------------------------
REM Step 2: Install Claude Code / Claude Codeのインストール
REM ------------------------------------------------------------
echo [Step 2/4] Installing Claude Code...
echo [Step 2/4] Claude Codeをインストールしています...
echo.

REM Download and run the official installer
curl -fsSL https://claude.ai/install.cmd -o "%TEMP%\claude-install.cmd"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to download installer. / インストーラーのダウンロードに失敗しました。
    echo Please check your internet connection. / インターネット接続を確認してください。
    pause
    exit /b 1
)

call "%TEMP%\claude-install.cmd"
del "%TEMP%\claude-install.cmd" >nul 2>&1

echo.

REM ------------------------------------------------------------
REM Step 3: Configure PATH / PATH環境変数の設定
REM ------------------------------------------------------------
echo [Step 3/4] Configuring PATH environment variable...
echo [Step 3/4] PATH環境変数を設定しています...
echo.

REM Get current user PATH
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "CURRENT_PATH=%%b"

REM Define paths to add
set "CLAUDE_PATH_1=%USERPROFILE%\.local\bin"
set "CLAUDE_PATH_2=%LOCALAPPDATA%\Programs\claude-code"

REM Check and add paths
set "PATH_UPDATED=0"

echo !CURRENT_PATH! | findstr /i /c:"%CLAUDE_PATH_1%" >nul 2>&1
if %errorlevel% neq 0 (
    if defined CURRENT_PATH (
        set "NEW_PATH=!CURRENT_PATH!;%CLAUDE_PATH_1%"
    ) else (
        set "NEW_PATH=%CLAUDE_PATH_1%"
    )
    set "CURRENT_PATH=!NEW_PATH!"
    set "PATH_UPDATED=1"
    echo [+] Added: %CLAUDE_PATH_1%
)

echo !CURRENT_PATH! | findstr /i /c:"%CLAUDE_PATH_2%" >nul 2>&1
if %errorlevel% neq 0 (
    set "NEW_PATH=!CURRENT_PATH!;%CLAUDE_PATH_2%"
    set "CURRENT_PATH=!NEW_PATH!"
    set "PATH_UPDATED=1"
    echo [+] Added: %CLAUDE_PATH_2%
)

if !PATH_UPDATED! equ 1 (
    REM Update registry
    reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "!CURRENT_PATH!" /f >nul 2>&1
    if %errorlevel% equ 0 (
        echo.
        echo [OK] PATH environment variable updated successfully.
        echo [OK] PATH環境変数の更新が完了しました。
    ) else (
        echo.
        echo [WARNING] Could not update PATH automatically.
        echo [WARNING] PATHを自動更新できませんでした。
        echo.
        echo Please add these paths manually: / 手動で以下のパスを追加してください:
        echo   %CLAUDE_PATH_1%
        echo   %CLAUDE_PATH_2%
    )
) else (
    echo [OK] PATH is already configured. / PATHは既に設定済みです。
)

REM Update current session PATH
set "PATH=%PATH%;%CLAUDE_PATH_1%;%CLAUDE_PATH_2%"

echo.

REM ------------------------------------------------------------
REM Step 4: Verify installation / インストールの確認
REM ------------------------------------------------------------
echo [Step 4/4] Verifying installation...
echo [Step 4/4] インストールを確認しています...
echo.

REM Try to find claude executable
set "CLAUDE_FOUND=0"

if exist "%CLAUDE_PATH_1%\claude.exe" (
    set "CLAUDE_FOUND=1"
    "%CLAUDE_PATH_1%\claude.exe" --version 2>nul
)

if !CLAUDE_FOUND! equ 0 (
    if exist "%CLAUDE_PATH_2%\claude.exe" (
        set "CLAUDE_FOUND=1"
        "%CLAUDE_PATH_2%\claude.exe" --version 2>nul
    )
)

if !CLAUDE_FOUND! equ 0 (
    where claude >nul 2>&1
    if %errorlevel% equ 0 (
        set "CLAUDE_FOUND=1"
        claude --version 2>nul
    )
)

echo.

if !CLAUDE_FOUND! equ 1 (
    echo ============================================================
    echo   Installation Complete! / インストール完了！
    echo ============================================================
    echo.
    echo [IMPORTANT] Please close this window and open a NEW terminal.
    echo [重要] このウィンドウを閉じて、新しいターミナルを開いてください。
    echo.
    echo Then run: / 次に以下を実行:
    echo   claude
    echo.
    echo This will start the authentication process.
    echo 認証プロセスが開始されます。
    echo.
    echo For more information, visit: / 詳細は以下を参照:
    echo   https://code.claude.com/docs/en/setup
    echo ============================================================
) else (
    echo ============================================================
    echo   Installation may require a terminal restart.
    echo   インストールはターミナルの再起動が必要な場合があります。
    echo ============================================================
    echo.
    echo [IMPORTANT] Please close this window and open a NEW terminal.
    echo [重要] このウィンドウを閉じて、新しいターミナルを開いてください。
    echo.
    echo Then run: / 次に以下を実行:
    echo   claude --version
    echo.
    echo If this doesn't work, try: / うまくいかない場合:
    echo   %CLAUDE_PATH_1%\claude.exe --version
    echo ============================================================
)

echo.
pause
