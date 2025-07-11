#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
界面功能测试脚本
用于验证1100x1100界面优化后的功能完整性
"""

import json
import os
import time
from datetime import datetime


def create_test_data():
    """创建测试数据文件"""
    test_data = {
        "msg": "成功",
        "code": 0,
        "data": {
            "id": -200,
            "status": 1,
            "name": "测试餐厅(界面优化测试)",
            "call_center": "13800138000",
            "phone_list": ["13800138000", "13900139000"],
            "address": "测试省测试市测试区测试街道测试路100号",
            "pic_url": "http://example.com/test.jpg",
            "shipping_time": "08:00-22:00",
            "shipping_fee": 3.0,
            "min_price": 15.0,
            "bulletin": "界面优化测试数据 - 这是一个用于测试1100x1100界面的示例店铺信息",
            "wm_poi_score": 4.5,
            "in_time_delivery_percent": 95,
            "avg_accept_order_time": 5,
            "avg_delivery_time": 25,
            "comment_num": 128,
            "latitude": 39906016,
            "longitude": 116397128,
            "distance": "2.1km",
            "shipping_fee_tip": "配送 ¥3",
            "min_price_tip": "起送 ¥15",
            "delivery_time_tip": "25分钟",
            "month_sale_num": 256,
            "food_score": 4.6,
            "delivery_score": 4.4,
            "brand_type": 1,
            "delivery_type": 1,
            "poi_sell_status": 1,
            "support_pay": 1,
            "invoice_support": 1,
            "discounts2": [
                {"info": "新用户立减10元"},
                {"info": "满30减5元"},
                {"info": "免配送费"}
            ],
            "show_info": [
                {"name": "月销量", "value": "256", "unit": "单"},
                {"name": "好评率", "value": "98", "unit": "%"},
                {"name": "配送时间", "value": "25", "unit": "分钟"}
            ]
        }
    }
    
    # 创建测试文件
    test_file = "ui_test_data.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建测试数据文件: {test_file}")
    return test_file


def create_multiple_test_data():
    """创建多条测试数据"""
    test_file = "ui_test_multiple.txt"
    
    # 创建多条测试数据
    test_data_list = []
    for i in range(5):
        data = {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -300 - i,
                "name": f"测试店铺{i+1}(界面测试)",
                "call_center": f"1380013800{i}",
                "address": f"测试省测试市测试区测试街道{i+1}号",
                "shipping_time": "09:00-21:00",
                "shipping_fee": 2.5 + i * 0.5,
                "min_price": 20.0 + i * 5,
                "wm_poi_score": 4.0 + i * 0.1,
                "avg_delivery_time": 30 + i * 2,
                "comment_num": 50 + i * 20,
                "distance": f"{2.0 + i * 0.5}km",
                "month_sale_num": 100 + i * 50
            }
        }
        test_data_list.append(json.dumps(data, ensure_ascii=False))
    
    # 写入文件（每行一个JSON）
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_data_list))
    
    print(f"✅ 创建多条测试数据文件: {test_file} (包含{len(test_data_list)}条记录)")
    return test_file


def test_extraction():
    """测试数据提取功能"""
    print("\n🧪 测试数据提取功能")
    
    # 测试单条数据
    test_file1 = create_test_data()
    os.system(f"python shop_extractor.py {test_file1} ui_test_single.xlsx")
    
    # 测试多条数据
    test_file2 = create_multiple_test_data()
    os.system(f"python shop_extractor.py {test_file2} ui_test_multiple.xlsx")
    
    # 测试追加模式
    os.system(f"python shop_extractor.py {test_file1} ui_test_append.xlsx")
    os.system(f"python shop_extractor.py {test_file2} ui_test_append.xlsx --append")
    
    print("✅ 数据提取测试完成")


def create_monitoring_test():
    """创建文件监控测试"""
    print("\n👁️ 创建文件监控测试数据")
    
    monitor_file = "ui_monitor_test.txt"
    
    # 创建初始数据
    initial_data = {
        "msg": "成功",
        "code": 0,
        "data": {
            "id": -400,
            "name": "监控测试店铺(初始)",
            "call_center": "13700137000",
            "address": "监控测试地址",
            "shipping_time": "10:00-20:00",
            "shipping_fee": 4.0,
            "min_price": 25.0,
            "wm_poi_score": 4.2,
            "avg_delivery_time": 28,
            "comment_num": 88
        }
    }
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建监控测试文件: {monitor_file}")
    print("📝 使用说明:")
    print("1. 在应用中选择此文件作为数据源")
    print("2. 启用文件监控功能")
    print("3. 运行 update_monitor_file() 函数来模拟文件更新")
    
    return monitor_file


def update_monitor_file():
    """更新监控测试文件"""
    monitor_file = "ui_monitor_test.txt"
    
    if not os.path.exists(monitor_file):
        print("❌ 监控测试文件不存在，请先运行 create_monitoring_test()")
        return
    
    # 创建更新数据
    updated_data = {
        "msg": "成功",
        "code": 0,
        "data": {
            "id": -401,
            "name": f"监控测试店铺(更新-{datetime.now().strftime('%H:%M:%S')})",
            "call_center": "13700137001",
            "address": "监控测试地址(已更新)",
            "shipping_time": "09:00-21:00",
            "shipping_fee": 3.5,
            "min_price": 20.0,
            "wm_poi_score": 4.5,
            "avg_delivery_time": 25,
            "comment_num": 95,
            "bulletin": f"文件更新测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
    }
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新监控测试文件: {monitor_file}")
    print(f"⏰ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def cleanup_test_files():
    """清理测试文件"""
    test_files = [
        "ui_test_data.txt",
        "ui_test_multiple.txt",
        "ui_monitor_test.txt",
        "ui_test_single.xlsx",
        "ui_test_multiple.xlsx",
        "ui_test_append.xlsx"
    ]
    
    cleaned = 0
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️ 已删除: {file}")
                cleaned += 1
            except Exception as e:
                print(f"❌ 删除失败 {file}: {e}")
    
    print(f"✅ 清理完成，共删除 {cleaned} 个文件")


def print_ui_test_guide():
    """打印界面测试指南"""
    print("=" * 60)
    print("🎯 1100x1100 界面优化测试指南")
    print("=" * 60)
    print()
    print("📋 测试项目清单:")
    print()
    print("🖼️  窗口测试:")
    print("   ✓ 窗口大小固定为 1100x1100 像素")
    print("   ✓ 无法调整窗口大小")
    print("   ✓ 窗口居中显示")
    print("   ✓ 无页面滚动条")
    print()
    print("📐 界面布局测试:")
    print("   ✓ 所有功能区域完整显示")
    print("   ✓ 文字清晰可读")
    print("   ✓ 按钮大小适中，易于点击")
    print("   ✓ 输入框和控件正常工作")
    print()
    print("📊 数据显示测试:")
    print("   ✓ 结果表格内部滚动正常")
    print("   ✓ 日志区域内部滚动正常")
    print("   ✓ 状态信息显示完整")
    print("   ✓ 通知系统工作正常")
    print()
    print("⚙️  功能测试:")
    print("   ✓ 文件选择功能")
    print("   ✓ 数据提取功能")
    print("   ✓ Excel 导出功能")
    print("   ✓ 文件监控功能")
    print("   ✓ 追加模式功能")
    print()
    print("🔧 可用的测试函数:")
    print("   • create_test_data() - 创建单条测试数据")
    print("   • create_multiple_test_data() - 创建多条测试数据")
    print("   • test_extraction() - 测试数据提取功能")
    print("   • create_monitoring_test() - 创建监控测试")
    print("   • update_monitor_file() - 更新监控文件")
    print("   • cleanup_test_files() - 清理测试文件")
    print()


def main():
    """主测试函数"""
    print_ui_test_guide()
    
    while True:
        print("\n" + "=" * 40)
        print("请选择测试操作:")
        print("1. 创建测试数据")
        print("2. 测试数据提取")
        print("3. 创建监控测试")
        print("4. 更新监控文件")
        print("5. 清理测试文件")
        print("6. 显示测试指南")
        print("0. 退出")
        print("=" * 40)
        
        choice = input("请输入选择 (0-6): ").strip()
        
        if choice == '1':
            create_test_data()
            create_multiple_test_data()
        elif choice == '2':
            test_extraction()
        elif choice == '3':
            create_monitoring_test()
        elif choice == '4':
            update_monitor_file()
        elif choice == '5':
            cleanup_test_files()
        elif choice == '6':
            print_ui_test_guide()
        elif choice == '0':
            print("👋 测试结束")
            break
        else:
            print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    main()
