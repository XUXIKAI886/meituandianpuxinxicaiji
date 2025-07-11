const { app, BrowserWindow, ipcMain, dialog, shell, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const chokidar = require('chokidar');

// 保持对窗口对象的全局引用
let mainWindow;
let fileWatcher = null;
let currentWatchedFile = null;

function createWindow() {
    // 创建浏览器窗口
    mainWindow = new BrowserWindow({
        width: 1100,
        height: 1100,
        resizable: false,  // 禁用窗口大小调整
        center: true,      // 窗口居中显示
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true,
            devTools: false  // 禁用开发者工具
        },
        icon: path.join(__dirname, 'assets/icon.png'),
        title: '店铺信息提取器',
        show: false
    });

    // 加载应用的 index.html
    mainWindow.loadFile('renderer/index.html');

    // 移除默认菜单栏
    mainWindow.setMenuBarVisibility(false);

    // 当窗口准备好时显示
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    // 当窗口被关闭时发出
    mainWindow.on('closed', () => {
        mainWindow = null;
        // 停止文件监控
        if (fileWatcher) {
            fileWatcher.close();
            fileWatcher = null;
        }
    });

    // 禁用开发者工具快捷键
    mainWindow.webContents.on('before-input-event', (event, input) => {
        // 禁用 F12, Ctrl+Shift+I, Ctrl+Shift+J 等开发者工具快捷键
        if (input.key === 'F12' ||
            (input.control && input.shift && (input.key === 'I' || input.key === 'J')) ||
            (input.control && input.shift && input.key === 'C')) {
            event.preventDefault();
        }
    });
}

// 当 Electron 完成初始化并准备创建浏览器窗口时调用此方法
app.whenReady().then(() => {
    // 设置空菜单以完全移除菜单栏
    Menu.setApplicationMenu(null);
    createWindow();
});

// 当所有窗口都关闭时退出应用
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// IPC 处理程序

// 选择文件对话框
ipcMain.handle('select-file', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile'],
        filters: [
            { name: '文本文件', extensions: ['txt', 'json'] },
            { name: '所有文件', extensions: ['*'] }
        ]
    });
    
    if (!result.canceled && result.filePaths.length > 0) {
        return result.filePaths[0];
    }
    return null;
});

// 选择保存文件对话框
ipcMain.handle('select-save-file', async () => {
    const result = await dialog.showSaveDialog(mainWindow, {
        filters: [
            { name: 'Excel文件', extensions: ['xlsx'] },
            { name: '所有文件', extensions: ['*'] }
        ],
        defaultPath: 'shop_data.xlsx'
    });
    
    if (!result.canceled) {
        return result.filePath;
    }
    return null;
});

// 提取店铺信息
ipcMain.handle('extract-shop-info', async (event, inputFile, outputFile, appendMode) => {
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, 'shop_extractor.py');
        const args = [pythonScript, inputFile];

        if (outputFile) {
            args.push(outputFile);
        }

        if (appendMode) {
            args.push('--append');
        }

        const pythonProcess = spawn('python', args, {
            env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
        });
        
        let output = '';
        let error = '';

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            error += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve({
                    success: true,
                    output: output,
                    data: parseExtractedData(output)
                });
            } else {
                reject({
                    success: false,
                    error: error || '提取过程中发生未知错误',
                    code: code
                });
            }
        });

        pythonProcess.on('error', (err) => {
            reject({
                success: false,
                error: `无法启动Python进程: ${err.message}`,
                code: -1
            });
        });
    });
});

// 解析提取的数据输出
function parseExtractedData(output) {
    try {
        const lines = output.split('\n');
        const data = [];

        // 查找概览信息
        for (const line of lines) {
            if (line.includes('提取的店铺信息概览:')) {
                const index = lines.indexOf(line);
                for (let i = index + 1; i < lines.length; i++) {
                    const shopLine = lines[i].trim();
                    if (shopLine && shopLine.match(/^\d+\./)) {
                        // 新格式: "序号. 店铺名称 - 电话 - 地址"
                        const parts = shopLine.split(' - ');
                        if (parts.length >= 3) {
                            const name = parts[0].replace(/^\d+\.\s*/, '');
                            const phone = parts[1];
                            const address = parts[2];
                            data.push({
                                name,
                                phone,
                                address,
                                extractTime: new Date().toLocaleString()
                            });
                        } else if (parts.length >= 2) {
                            // 兼容旧格式: "序号. 店铺名称 - 地址"
                            const name = parts[0].replace(/^\d+\.\s*/, '');
                            const address = parts[1];
                            data.push({
                                name,
                                phone: 'N/A',
                                address,
                                extractTime: new Date().toLocaleString()
                            });
                        }
                    }
                }
                break;
            }
        }

        return data;
    } catch (error) {
        console.error('解析提取数据时出错:', error);
        return [];
    }
}

// 开始文件监控
ipcMain.handle('start-file-monitoring', async (event, filePath, outputFile) => {
    try {
        // 停止之前的监控
        if (fileWatcher) {
            fileWatcher.close();
        }

        currentWatchedFile = filePath;
        
        // 创建新的文件监控器
        fileWatcher = chokidar.watch(filePath, {
            persistent: true,
            ignoreInitial: true
        });

        fileWatcher.on('change', async () => {
            console.log(`文件已更新: ${filePath}`);
            
            try {
                // 自动提取新内容
                const result = await new Promise((resolve, reject) => {
                    const pythonScript = path.join(__dirname, 'shop_extractor.py');
                    const args = [pythonScript, filePath, outputFile, '--append'];
                    
                    const pythonProcess = spawn('python', args, {
                        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
                    });
                    
                    let output = '';
                    let error = '';

                    pythonProcess.stdout.on('data', (data) => {
                        output += data.toString();
                    });

                    pythonProcess.stderr.on('data', (data) => {
                        error += data.toString();
                    });

                    pythonProcess.on('close', (code) => {
                        if (code === 0) {
                            resolve({
                                success: true,
                                output: output,
                                data: parseExtractedData(output)
                            });
                        } else {
                            reject({
                                success: false,
                                error: error || '自动提取过程中发生未知错误',
                                code: code
                            });
                        }
                    });
                });

                // 通知渲染进程文件已更新
                mainWindow.webContents.send('file-updated', {
                    filePath: filePath,
                    result: result,
                    timestamp: new Date().toLocaleString()
                });

            } catch (error) {
                console.error('自动提取失败:', error);
                mainWindow.webContents.send('file-update-error', {
                    filePath: filePath,
                    error: error.message || '自动提取失败',
                    timestamp: new Date().toLocaleString()
                });
            }
        });

        fileWatcher.on('error', (error) => {
            console.error('文件监控错误:', error);
            mainWindow.webContents.send('monitoring-error', {
                error: error.message,
                timestamp: new Date().toLocaleString()
            });
        });

        return {
            success: true,
            message: `开始监控文件: ${filePath}`
        };

    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
});

// 停止文件监控
ipcMain.handle('stop-file-monitoring', async () => {
    if (fileWatcher) {
        fileWatcher.close();
        fileWatcher = null;
        currentWatchedFile = null;
        return {
            success: true,
            message: '文件监控已停止'
        };
    }
    return {
        success: false,
        message: '没有正在进行的文件监控'
    };
});

// 获取当前监控状态
ipcMain.handle('get-monitoring-status', async () => {
    return {
        isMonitoring: fileWatcher !== null,
        watchedFile: currentWatchedFile
    };
});

// 打开文件夹
ipcMain.handle('open-folder', async (event, folderPath) => {
    try {
        await shell.openPath(folderPath);
        return { success: true };
    } catch (error) {
        return { success: false, error: error.message };
    }
});
