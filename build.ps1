Write-Host "正在准备打包Electron应用..." -ForegroundColor Green

# 停止所有可能的Electron进程
Write-Host "停止Electron进程..." -ForegroundColor Yellow
Get-Process -Name "electron" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process -Name "店铺信息提取器" -ErrorAction SilentlyContinue | Stop-Process -Force

# 等待进程完全停止
Start-Sleep -Seconds 3

# 清理dist目录
if (Test-Path "dist") {
    Write-Host "清理旧的构建文件..." -ForegroundColor Yellow
    Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# 开始打包
Write-Host "开始打包应用..." -ForegroundColor Green
npm run dist

Write-Host "打包完成！检查dist目录查看结果。" -ForegroundColor Green
