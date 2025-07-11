# Fiddler抓包工具使用指南

## 概述

本指南详细介绍如何使用Fiddler抓包工具配合店铺信息提取器，实现美团外卖店铺信息的自动化采集和处理。

## 🛠️ 环境准备

### 1. 下载和安装Fiddler
- 访问 [Fiddler官网](https://www.telerik.com/fiddler)
- 下载 **Fiddler Classic** 版本
- 按照安装向导完成安装

### 2. 基础配置
1. **启动Fiddler**
2. **配置HTTPS解密**：
   - 点击 `Tools` → `Options`
   - 选择 `HTTPS` 选项卡
   - 勾选 `Capture HTTPS CONNECTs`
   - 勾选 `Decrypt HTTPS traffic`
   - 点击 `Actions` → `Trust Root Certificate`
   - 按提示安装证书

### 3. 创建目标目录
确保 `D:\ailun\` 目录存在：
```cmd
mkdir D:\ailun
```

## 📝 脚本配置

### 1. 打开脚本编辑器
- 在Fiddler中点击 `Rules` → `Customize Rules`
- 系统会打开脚本编辑器（通常是记事本或默认编辑器）

### 2. 添加自动脚本
在 `OnBeforeResponse` 函数中添加以下代码：

```javascript
// 美团外卖店铺信息自动保存
if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?")){
    oSession.utilDecodeResponse();
    oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
    oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");
    FiddlerApplication.Log.LogString("店铺信息已保存: " + oSession.fullUrl);
}
```

### 3. 完整函数示例
```javascript
static function OnBeforeResponse(oSession: Session) {
    if (m_Hide304s && oSession.responseCode == 304) {
        oSession["ui-hide"] = "true";
    }
    
    // 美团外卖店铺信息自动保存
    if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?")){
        oSession.utilDecodeResponse();
        oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
        oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");
        FiddlerApplication.Log.LogString("店铺信息已保存: " + oSession.fullUrl);
    }
}
```

### 4. 保存脚本
- 按 `Ctrl+S` 保存脚本
- 关闭编辑器
- Fiddler会自动重新加载脚本

## 🚀 使用流程

### 1. 启动工具
1. **启动Fiddler**
   - 确保抓包功能已开启（左下角显示"Capturing"）
   - 检查脚本是否正确加载

2. **启动店铺信息提取器**
   - 运行 `start.bat` 或 `npm start`
   - 点击"开启监控"按钮
   - 确保监控状态显示为"监控中"

### 2. 数据采集
1. **打开微信小程序**
   - 搜索"美团外卖"小程序
   - 或在浏览器中访问美团外卖网页版

2. **浏览店铺**
   - 点击进入具体店铺页面
   - 等待页面完全加载
   - Fiddler会自动捕获并保存店铺信息

3. **验证采集**
   - 在Fiddler日志中查看"店铺信息已保存"消息
   - 检查 `D:\ailun\dianpuxinxi.txt` 文件是否有新内容
   - 店铺信息提取器会自动检测文件变化并处理

### 3. 自动化处理
- **实时监控**：提取器自动检测文件变化
- **智能去重**：自动过滤重复店铺信息
- **Excel导出**：自动保存到指定Excel文件
- **界面更新**：实时显示新提取的店铺信息

## 🔍 脚本详解

### 核心功能
```javascript
// 1. URL匹配检查
if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?"))

// 2. 响应解码
oSession.utilDecodeResponse();

// 3. 保存完整响应（追加模式）
oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);

// 4. 保存响应体
oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");

// 5. 记录日志
FiddlerApplication.Log.LogString("店铺信息已保存: " + oSession.fullUrl);
```

### 参数说明
- **URL模式**：`https://wx.waimai.meituan.com/weapp/v1/poi/info?`
- **保存路径**：`D:/ailun/dianpuxinxi.txt`
- **保存模式**：`true` = 追加模式，`false` = 覆盖模式
- **日志输出**：在Fiddler底部的Log选项卡中显示

## ⚠️ 注意事项

### 1. 合规使用
- **仅用于学习研究**：不得用于商业用途
- **遵守使用条款**：遵守美团外卖的使用条款和robots.txt协议
- **控制频率**：避免过于频繁的请求，减少对服务器的压力
- **尊重权益**：尊重数据来源方的合法权益

### 2. 技术要求
- **网络环境**：确保网络连接稳定
- **权限设置**：确保Fiddler有文件写入权限
- **目录存在**：确保 `D:\ailun\` 目录存在
- **证书信任**：正确安装和信任Fiddler的根证书

### 3. 数据质量
- **完整性检查**：定期检查采集的数据是否完整
- **格式验证**：确保保存的数据为有效的JSON格式
- **去重处理**：依赖提取器的去重功能处理重复数据

## 🛠️ 故障排除

### 1. 无法捕获HTTPS流量
**问题**：Fiddler无法捕获微信小程序的HTTPS请求
**解决方案**：
- 重新安装Fiddler根证书
- 检查HTTPS解密设置是否正确
- 尝试重启Fiddler和浏览器/微信

### 2. 脚本不执行
**问题**：添加脚本后没有自动保存文件
**解决方案**：
- 检查脚本语法是否正确
- 确认脚本已保存并重新加载
- 验证URL匹配模式是否正确

### 3. 文件保存失败
**问题**：脚本执行但文件没有保存
**解决方案**：
- 检查目录 `D:\ailun\` 是否存在
- 确认Fiddler有文件写入权限
- 尝试以管理员身份运行Fiddler

### 4. 数据格式错误
**问题**：保存的数据无法被提取器正确解析
**解决方案**：
- 检查保存的文件内容格式
- 确认响应数据为有效的JSON
- 验证API接口是否返回预期数据

## 📊 性能优化

### 1. 过滤无关流量
```javascript
// 只捕获目标API，提高性能
if(oSession.uriContains("wx.waimai.meituan.com") && 
   oSession.uriContains("/poi/info?")){
    // 处理逻辑
}
```

### 2. 文件大小控制
```javascript
// 检查文件大小，避免文件过大
var fileInfo = new System.IO.FileInfo("D:/ailun/dianpuxinxi.txt");
if (!fileInfo.Exists || fileInfo.Length < 50000000) { // 小于50MB
    oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
}
```

### 3. 错误处理
```javascript
// 添加异常处理
try {
    oSession.utilDecodeResponse();
    oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
    FiddlerApplication.Log.LogString("✓ 保存成功");
} catch (e) {
    FiddlerApplication.Log.LogString("✗ 保存失败: " + e.message);
}
```

## 🎯 最佳实践

### 1. 完整工作流
1. **准备阶段**：启动Fiddler → 配置脚本 → 启动提取器
2. **采集阶段**：开启监控 → 浏览店铺 → 自动保存数据
3. **处理阶段**：自动去重 → 实时提取 → Excel导出
4. **验证阶段**：检查结果 → 确认数据质量

### 2. 数据管理
- **定期备份**：定期备份采集的原始数据
- **清理维护**：定期清理过大的数据文件
- **质量检查**：定期检查数据的完整性和准确性

### 3. 团队协作
- **标准化配置**：团队使用统一的Fiddler配置
- **文档维护**：及时更新使用文档和脚本
- **经验分享**：分享使用技巧和问题解决方案

通过正确配置和使用Fiddler，您可以实现美团外卖店铺信息的自动化采集，大大提高数据收集的效率和准确性！
