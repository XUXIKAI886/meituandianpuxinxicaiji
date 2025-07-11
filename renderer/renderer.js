const { ipcRenderer } = require('electron');

// DOM 元素引用
const elements = {
    inputFile: document.getElementById('input-file'),
    outputFile: document.getElementById('output-file'),
    fileStatus: document.getElementById('file-status'),
    selectOutputBtn: document.getElementById('select-output-btn'),
    extractBtn: document.getElementById('extract-btn'),
    monitorBtn: document.getElementById('monitor-btn'),
    stopMonitorBtn: document.getElementById('stop-monitor-btn'),
    appendMode: document.getElementById('append-mode'),
    currentStatus: document.getElementById('current-status'),
    monitorStatus: document.getElementById('monitor-status'),
    lastUpdate: document.getElementById('last-update'),
    resultsTable: document.getElementById('results-table'),
    resultsTbody: document.getElementById('results-tbody'),
    noResults: document.getElementById('no-results'),
    logContainer: document.getElementById('log-container'),
    clearResultsBtn: document.getElementById('clear-results-btn'),
    clearLogBtn: document.getElementById('clear-log-btn'),
    loadingOverlay: document.getElementById('loading-overlay'),
    notificationContainer: document.getElementById('notification-container')
};

// 应用状态
let appState = {
    isMonitoring: false,
    extractedData: [],
    logEntries: [],
    fixedInputFile: 'D:\\ailun\\dianpuxinxi.txt' // 固定的数据源路径
};

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    initializeFixedPath();
    initializeTheme();
    updateUI();
    checkMonitoringStatus();
    addLogEntry('应用已启动', 'info');
    addLogEntry(`数据源路径: ${appState.fixedInputFile}`, 'info');
});

// 初始化事件监听器
function initializeEventListeners() {
    // 文件选择（只保留输出文件选择）
    elements.selectOutputBtn.addEventListener('click', selectOutputFile);

    // 操作按钮
    elements.extractBtn.addEventListener('click', extractShopInfo);
    elements.monitorBtn.addEventListener('click', startMonitoring);
    elements.stopMonitorBtn.addEventListener('click', stopMonitoring);

    // 清空按钮
    elements.clearResultsBtn.addEventListener('click', clearResults);
    elements.clearLogBtn.addEventListener('click', clearLog);

    // 输出文件变化监听
    elements.outputFile.addEventListener('input', updateUI);
}

// 初始化固定路径
function initializeFixedPath() {
    elements.inputFile.value = appState.fixedInputFile;
    checkFileExists();
}

// 检查固定文件是否存在
async function checkFileExists() {
    try {
        // 这里可以添加文件存在性检查的逻辑
        // 暂时显示为已配置状态
        elements.fileStatus.innerHTML = '<i class="fas fa-check-circle"></i> 已配置';
        elements.fileStatus.style.background = '#d4edda';
        elements.fileStatus.style.borderColor = '#28a745';
        elements.fileStatus.style.color = '#155724';

        addLogEntry('数据源文件路径已配置', 'success');
    } catch (error) {
        elements.fileStatus.innerHTML = '<i class="fas fa-exclamation-triangle"></i> 路径配置';
        elements.fileStatus.style.background = '#fff3cd';
        elements.fileStatus.style.borderColor = '#ffc107';
        elements.fileStatus.style.color = '#856404';

        addLogEntry('请确认数据源文件路径是否正确', 'warning');
    }
}

// 移除了手动文件选择功能，使用固定路径

// 选择输出文件
async function selectOutputFile() {
    try {
        const filePath = await ipcRenderer.invoke('select-save-file');
        if (filePath) {
            elements.outputFile.value = filePath;
            addLogEntry(`已选择输出文件: ${filePath}`, 'info');
            updateUI();
        }
    } catch (error) {
        showNotification('选择保存位置失败: ' + error.message, 'error');
        addLogEntry(`选择保存位置失败: ${error.message}`, 'error');
    }
}

// 提取店铺信息
async function extractShopInfo() {
    const inputFile = appState.fixedInputFile; // 使用固定路径
    const outputFile = elements.outputFile.value;
    const appendMode = elements.appendMode.checked;

    if (!outputFile) {
        showNotification('请先选择输出文件', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        updateStatus('正在提取店铺信息...');
        addLogEntry(`开始提取店铺信息: ${inputFile}`, 'info');
        
        const result = await ipcRenderer.invoke('extract-shop-info', inputFile, outputFile, appendMode);
        
        if (result.success) {
            showNotification('店铺信息提取成功!', 'success');
            addLogEntry('店铺信息提取完成', 'success');

            // 更新结果显示
            if (result.data && result.data.length > 0) {
                addExtractedData(result.data);
            } else {
                // 如果没有解析到数据，尝试从输出中提取基本信息
                const basicData = parseBasicOutput(result.output);
                if (basicData.length > 0) {
                    addExtractedData(basicData);
                }
            }

            updateStatus('提取完成');
            updateLastUpdate();
        } else {
            throw new Error(result.error || '提取失败');
        }
    } catch (error) {
        showNotification('提取失败: ' + error.message, 'error');
        addLogEntry(`提取失败: ${error.message}`, 'error');
        updateStatus('提取失败');
    } finally {
        showLoading(false);
    }
}

// 开始文件监控
async function startMonitoring() {
    const inputFile = appState.fixedInputFile; // 使用固定路径
    const outputFile = elements.outputFile.value;

    if (!outputFile) {
        showNotification('请先选择输出文件', 'warning');
        return;
    }
    
    try {
        const result = await ipcRenderer.invoke('start-file-monitoring', inputFile, outputFile);
        
        if (result.success) {
            appState.isMonitoring = true;
            updateMonitoringUI();
            showNotification('文件监控已启动', 'success');
            addLogEntry(`开始监控文件: ${inputFile}`, 'info');
            updateStatus('监控中...');
        } else {
            throw new Error(result.error || '启动监控失败');
        }
    } catch (error) {
        showNotification('启动监控失败: ' + error.message, 'error');
        addLogEntry(`启动监控失败: ${error.message}`, 'error');
    }
}

// 停止文件监控
async function stopMonitoring() {
    try {
        const result = await ipcRenderer.invoke('stop-file-monitoring');
        
        if (result.success) {
            appState.isMonitoring = false;
            updateMonitoringUI();
            showNotification('文件监控已停止', 'info');
            addLogEntry('文件监控已停止', 'info');
            updateStatus('就绪');
        } else {
            throw new Error(result.error || '停止监控失败');
        }
    } catch (error) {
        showNotification('停止监控失败: ' + error.message, 'error');
        addLogEntry(`停止监控失败: ${error.message}`, 'error');
    }
}

// 检查监控状态
async function checkMonitoringStatus() {
    try {
        const status = await ipcRenderer.invoke('get-monitoring-status');
        appState.isMonitoring = status.isMonitoring;
        
        // 监控状态恢复时使用固定路径
        if (status.isMonitoring) {
            addLogEntry(`恢复监控状态: ${appState.fixedInputFile}`, 'info');
        }
        
        updateMonitoringUI();
    } catch (error) {
        console.error('检查监控状态失败:', error);
    }
}

// 更新UI状态
function updateUI() {
    const hasInputFile = true; // 固定路径始终可用
    const hasOutputFile = elements.outputFile.value.trim() !== '';

    // 更新按钮状态
    elements.extractBtn.disabled = !hasOutputFile; // 只需要输出文件
    elements.monitorBtn.disabled = !hasOutputFile || appState.isMonitoring;
}

// 更新监控相关UI
function updateMonitoringUI() {
    elements.monitorBtn.disabled = appState.isMonitoring;
    elements.stopMonitorBtn.disabled = !appState.isMonitoring;
    
    elements.monitorStatus.textContent = appState.isMonitoring ? '监控中' : '未启动';
    elements.monitorStatus.style.color = appState.isMonitoring ? '#27ae60' : '#7f8c8d';
}

// 更新状态显示
function updateStatus(status) {
    elements.currentStatus.textContent = status;
}

// 更新最后更新时间
function updateLastUpdate() {
    elements.lastUpdate.textContent = new Date().toLocaleString();
}

// 解析基本输出格式（备用方案）
function parseBasicOutput(output) {
    const data = [];

    if (!output) return data;

    const lines = output.split('\n');

    // 查找概览信息
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.includes('提取的店铺信息概览:')) {
            // 解析后续行
            for (let j = i + 1; j < lines.length; j++) {
                const shopLine = lines[j].trim();
                if (shopLine && shopLine.match(/^\d+\./)) {
                    const parts = shopLine.split(' - ');
                    if (parts.length >= 2) {
                        const name = parts[0].replace(/^\d+\.\s*/, '');
                        const address = parts[1];
                        data.push({
                            name: name,
                            phone: '未提取',
                            address: address,
                            extractTime: new Date().toLocaleString()
                        });
                    }
                }
            }
            break;
        }
    }

    // 如果没有找到概览，尝试从成功消息中提取
    if (data.length === 0) {
        for (const line of lines) {
            if (line.includes('成功提取') && line.includes('条店铺信息')) {
                // 创建一个基本的数据条目
                data.push({
                    name: '店铺信息已提取',
                    phone: '请查看Excel文件',
                    address: '详细信息请查看导出文件',
                    extractTime: new Date().toLocaleString()
                });
                break;
            }
        }
    }

    return data;
}

// 添加提取的数据到结果表格
function addExtractedData(data) {
    let duplicateCount = 0;
    let addedCount = 0;

    data.forEach(item => {
        // 检查是否已存在相同的店铺（基于店铺名称和地址）
        const isDuplicate = appState.extractedData.some(existing =>
            existing.name === item.name && existing.address === item.address
        );

        if (!isDuplicate) {
            appState.extractedData.push(item);
            addResultRow(item, appState.extractedData.length);
            addedCount++;
        } else {
            duplicateCount++;
        }
    });

    // 显示去重统计信息
    if (duplicateCount > 0) {
        addLogEntry(`检测到 ${duplicateCount} 条重复数据，已自动过滤`, 'warning');
        showNotification(`已过滤 ${duplicateCount} 条重复数据，新增 ${addedCount} 条`, 'info');
    }

    updateResultsDisplay();
}

// 添加结果行
function addResultRow(data, index) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${index}</td>
        <td>${data.name || 'N/A'}</td>
        <td>${data.phone || 'N/A'}</td>
        <td>${data.address || 'N/A'}</td>
        <td>${new Date().toLocaleString()}</td>
    `;
    elements.resultsTbody.appendChild(row);
}

// 更新结果显示
function updateResultsDisplay() {
    const hasResults = appState.extractedData.length > 0;
    elements.resultsTable.style.display = hasResults ? 'table' : 'none';
    elements.noResults.style.display = hasResults ? 'none' : 'block';
}

// 清空结果
function clearResults() {
    appState.extractedData = [];
    elements.resultsTbody.innerHTML = '';
    updateResultsDisplay();
    addLogEntry('已清空提取结果', 'info');
}

// 添加日志条目
function addLogEntry(message, level = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = {
        timestamp,
        message,
        level
    };
    
    appState.logEntries.push(logEntry);
    
    const logElement = document.createElement('div');
    logElement.className = 'log-entry';
    logElement.innerHTML = `
        <span class="log-timestamp">[${timestamp}]</span>
        <span class="log-level-${level}">${message}</span>
    `;
    
    elements.logContainer.appendChild(logElement);
    elements.logContainer.scrollTop = elements.logContainer.scrollHeight;
}

// 清空日志
function clearLog() {
    appState.logEntries = [];
    elements.logContainer.innerHTML = '';
    addLogEntry('日志已清空', 'info');
}

// 显示/隐藏加载指示器
function showLoading(show) {
    elements.loadingOverlay.style.display = show ? 'flex' : 'none';
}

// 显示通知
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    elements.notificationContainer.appendChild(notification);
    
    // 3秒后自动移除通知
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// IPC 事件监听器
ipcRenderer.on('file-updated', (event, data) => {
    addLogEntry(`文件已更新: ${data.filePath}`, 'info');
    
    if (data.result && data.result.success) {
        showNotification('检测到文件更新，已自动提取新内容', 'success');
        
        if (data.result.data && data.result.data.length > 0) {
            addExtractedData(data.result.data);
        }
        
        updateLastUpdate();
    }
});

ipcRenderer.on('file-update-error', (event, data) => {
    addLogEntry(`自动提取失败: ${data.error}`, 'error');
    showNotification('自动提取失败: ' + data.error, 'error');
});

ipcRenderer.on('monitoring-error', (event, data) => {
    addLogEntry(`监控错误: ${data.error}`, 'error');
    showNotification('监控错误: ' + data.error, 'error');

    // 重置监控状态
    appState.isMonitoring = false;
    updateMonitoringUI();
});

// 主题相关功能
function initializeTheme() {
    // 加载保存的主题
    const savedTheme = localStorage.getItem('selectedTheme');
    if (savedTheme) {
        const themeSelect = document.getElementById('themeSelect');
        if (themeSelect) {
            themeSelect.value = savedTheme;
            changeTheme(savedTheme);
        }
    }
}

// 主题切换功能
function changeTheme(themeClass) {
    const body = document.body;

    // 移除所有主题类
    const themeClasses = [
        'theme-light-blue', 'theme-warm-beige', 'theme-soft-green',
        'theme-elegant-gray', 'theme-soft-purple', 'theme-fresh-mint',
        'theme-sky-blue', 'theme-sunset-orange', 'theme-dark',
        'theme-minimal', 'theme-business-blue', 'theme-forest-green',
        'theme-rose-gold', 'theme-ocean-blue', 'theme-warm-yellow'
    ];

    themeClasses.forEach(cls => body.classList.remove(cls));

    // 添加新主题类
    if (themeClass) {
        body.classList.add(themeClass);
    }

    // 保存主题选择
    localStorage.setItem('selectedTheme', themeClass);

    addLogEntry(`主题已切换: ${themeClass || '默认'}`, 'info');
}

// 将changeTheme函数暴露到全局作用域，以便HTML中的onchange可以调用
window.changeTheme = changeTheme;

// 软件使用声明弹窗功能
function showDisclaimer() {
    const modal = document.getElementById('disclaimer-modal');
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // 防止背景滚动
        addLogEntry('用户查看软件使用声明', 'info');
    }
}

function closeDisclaimer() {
    const modal = document.getElementById('disclaimer-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // 恢复滚动
        addLogEntry('用户关闭软件使用声明', 'info');
    }
}

// 点击弹窗外部区域关闭弹窗
document.addEventListener('click', function(event) {
    const modal = document.getElementById('disclaimer-modal');
    if (modal && event.target === modal) {
        closeDisclaimer();
    }
});

// ESC键关闭弹窗
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('disclaimer-modal');
        if (modal && modal.style.display === 'block') {
            closeDisclaimer();
        }
    }
});

// 将弹窗函数暴露到全局作用域
window.showDisclaimer = showDisclaimer;
window.closeDisclaimer = closeDisclaimer;
