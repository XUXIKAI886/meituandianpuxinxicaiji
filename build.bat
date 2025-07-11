@echo off
echo 正在准备打包Electron应用...

REM 停止所有可能的Electron进程
taskkill /f /im electron.exe 2>nul
taskkill /f /im "店铺信息提取器.exe" 2>nul

REM 等待进程完全停止
timeout /t 3 /nobreak >nul

REM 清理dist目录
if exist dist (
    echo 清理旧的构建文件...
    rmdir /s /q dist 2>nul
    timeout /t 2 /nobreak >nul
)

REM 开始打包
echo 开始打包应用...
npm run dist

echo 打包完成！
pause
