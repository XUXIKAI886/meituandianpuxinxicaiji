@echo off
echo ========================================
echo 店铺信息提取器 - 启动脚本
echo ========================================
echo.

REM 检查Node.js是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Node.js，请先安装Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 正在检查依赖...

REM 检查是否存在node_modules
if not exist "node_modules" (
    echo 正在安装Node.js依赖...
    npm install
    if %errorlevel% neq 0 (
        echo 错误: Node.js依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查Python依赖
echo 正在检查Python依赖...
python -c "import pandas, openpyxl" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装Python依赖...
    pip install pandas openpyxl
    if %errorlevel% neq 0 (
        echo 错误: Python依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo 依赖检查完成，正在启动应用...
echo.

REM 启动Electron应用
npm start

pause
