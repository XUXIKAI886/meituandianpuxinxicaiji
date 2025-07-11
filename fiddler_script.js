/*
 * Fiddler自动脚本 - 美团外卖店铺信息采集
 * 
 * 功能说明：
 * - 自动捕获美团外卖店铺信息API响应
 * - 将店铺数据保存到指定文件路径
 * - 支持店铺信息提取器的实时数据采集
 * 
 * 使用方法：
 * 1. 打开Fiddler Classic
 * 2. 点击 Rules → Customize Rules
 * 3. 在 OnBeforeResponse 函数中添加以下代码
 * 4. 保存脚本并重启Fiddler
 * 
 * 注意事项：
 * - 确保 D:\ailun\ 目录存在
 * - 确保Fiddler有文件写入权限
 * - 建议配合店铺信息提取器的监控功能使用
 */

// 在 OnBeforeResponse 函数中添加以下代码：

if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?")){
    // 解码响应内容
    oSession.utilDecodeResponse();
    
    // 保存完整响应到文件（追加模式）
    oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
    
    // 保存响应体到文件
    oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");
    
    // 可选：在Fiddler控制台显示日志
    FiddlerApplication.Log.LogString("店铺信息已保存: " + oSession.fullUrl);
}

/*
 * 完整的 OnBeforeResponse 函数示例：
 * 
 * static function OnBeforeResponse(oSession: Session) {
 *     if (m_Hide304s && oSession.responseCode == 304) {
 *         oSession["ui-hide"] = "true";
 *     }
 *     
 *     // 美团外卖店铺信息自动保存
 *     if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?")){
 *         oSession.utilDecodeResponse();
 *         oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
 *         oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");
 *         FiddlerApplication.Log.LogString("店铺信息已保存: " + oSession.fullUrl);
 *     }
 * }
 */

/*
 * 扩展功能（可选）：
 * 
 * 1. 添加文件大小检查：
 * if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?")){
 *     oSession.utilDecodeResponse();
 *     var fileInfo = new System.IO.FileInfo("D:/ailun/dianpuxinxi.txt");
 *     if (!fileInfo.Exists || fileInfo.Length < 10000000) { // 小于10MB
 *         oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
 *         oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");
 *     }
 * }
 * 
 * 2. 添加时间戳日志：
 * if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?")){
 *     oSession.utilDecodeResponse();
 *     var timestamp = new Date().toLocaleString();
 *     FiddlerApplication.Log.LogString("[" + timestamp + "] 捕获店铺信息: " + oSession.fullUrl);
 *     oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
 *     oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");
 * }
 * 
 * 3. 添加错误处理：
 * if(oSession.uriContains("https://wx.waimai.meituan.com/weapp/v1/poi/info?")){
 *     try {
 *         oSession.utilDecodeResponse();
 *         oSession.SaveResponse("D:/ailun/dianpuxinxi.txt", true);
 *         oSession.SaveResponseBody("D:/ailun/dianpuxinxi.txt");
 *         FiddlerApplication.Log.LogString("✓ 店铺信息保存成功");
 *     } catch (e) {
 *         FiddlerApplication.Log.LogString("✗ 保存失败: " + e.message);
 *     }
 * }
 */

/*
 * 配置说明：
 * 
 * 目标URL模式：
 * - https://wx.waimai.meituan.com/weapp/v1/poi/info?
 * - 该接口返回完整的店铺信息JSON数据
 * 
 * 保存路径：
 * - D:/ailun/dianpuxinxi.txt
 * - 与店铺信息提取器的固定路径一致
 * 
 * 保存模式：
 * - 追加模式（true）：新数据会添加到文件末尾
 * - 覆盖模式（false）：每次都会覆盖原文件
 * 
 * 数据格式：
 * - JSON格式的店铺详细信息
 * - 包含店铺名称、地址、电话、评分等27个字段
 * - 自动支持去重功能
 */

/*
 * 使用建议：
 * 
 * 1. 数据采集工作流：
 *    Fiddler抓包 → 自动保存 → 提取器监控 → 实时处理 → Excel导出
 * 
 * 2. 最佳实践：
 *    - 启动Fiddler和店铺信息提取器
 *    - 开启提取器的文件监控功能
 *    - 在微信小程序中浏览店铺
 *    - 系统自动完成数据采集和处理
 * 
 * 3. 注意事项：
 *    - 遵守网站使用条款和robots.txt协议
 *    - 控制采集频率，避免对服务器造成压力
 *    - 仅用于学习研究，不得用于商业用途
 *    - 尊重数据来源方的权益
 */
