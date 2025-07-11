#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试提取结果显示修复
验证数据能否正确显示在界面中
"""

import json
import os
import subprocess
import time
from datetime import datetime


def create_test_shop_data():
    """创建测试店铺数据"""
    test_data = {
        "msg": "成功",
        "code": 0,
        "data": {
            "id": -500,
            "status": 1,
            "name": "显示测试餐厅(修复验证)",
            "call_center": "13500135000",
            "phone_list": ["13500135000"],
            "address": "显示测试省显示测试市显示测试区显示测试街道500号",
            "pic_url": "http://example.com/display_test.jpg",
            "shipping_time": "09:00-21:00",
            "shipping_fee": 4.5,
            "min_price": 25.0,
            "bulletin": "这是一个用于测试界面显示修复的店铺数据，包含完整的店铺信息字段。",
            "wm_poi_score": 4.8,
            "in_time_delivery_percent": 98,
            "avg_accept_order_time": 3,
            "avg_delivery_time": 22,
            "comment_num": 256,
            "latitude": 39908016,
            "longitude": 116407128,
            "distance": "1.8km",
            "shipping_fee_tip": "配送 ¥4.5",
            "min_price_tip": "起送 ¥25",
            "delivery_time_tip": "22分钟",
            "month_sale_num": 512,
            "food_score": 4.9,
            "delivery_score": 4.7,
            "brand_type": 1,
            "delivery_type": 1,
            "poi_sell_status": 1,
            "support_pay": 1,
            "invoice_support": 1,
            "discounts2": [
                {"info": "首单立减15元"},
                {"info": "满50减8元"},
                {"info": "免配送费(满30元)"}
            ],
            "show_info": [
                {"name": "月销量", "value": "512", "unit": "单"},
                {"name": "好评率", "value": "99", "unit": "%"},
                {"name": "配送时间", "value": "22", "unit": "分钟"}
            ]
        }
    }
    
    test_file = "display_test.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建显示测试数据: {test_file}")
    return test_file


def test_json_output():
    """测试JSON输出功能"""
    print("\n🧪 测试JSON输出功能")
    
    test_file = create_test_shop_data()
    output_file = "display_test_output.xlsx"
    
    # 测试JSON输出
    try:
        result = subprocess.run([
            'python', 'shop_extractor.py', 
            test_file, output_file, '--json'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ Python脚本执行成功")
            
            # 检查JSON输出
            output = result.stdout
            if 'JSON_DATA_START' in output and 'JSON_DATA_END' in output:
                print("✅ JSON数据标记正确")
                
                # 提取JSON数据
                lines = output.split('\n')
                json_start = -1
                json_end = -1
                
                for i, line in enumerate(lines):
                    if line.strip() == 'JSON_DATA_START':
                        json_start = i + 1
                    elif line.strip() == 'JSON_DATA_END':
                        json_end = i
                        break
                
                if json_start != -1 and json_end != -1:
                    json_lines = lines[json_start:json_end]
                    json_string = '\n'.join(json_lines)
                    
                    try:
                        data = json.loads(json_string)
                        print("✅ JSON数据解析成功")
                        print(f"📊 提取到 {len(data)} 条记录")
                        
                        if data:
                            shop = data[0]
                            print(f"📝 店铺名称: {shop.get('店铺名称', 'N/A')}")
                            print(f"📞 联系电话: {shop.get('联系电话', 'N/A')}")
                            print(f"📍 店铺地址: {shop.get('店铺地址', 'N/A')}")
                            print(f"⏰ 提取时间: {shop.get('提取时间', 'N/A')}")
                            
                            return True
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON解析失败: {e}")
                        print("JSON内容:")
                        print(json_string)
                else:
                    print("❌ 未找到JSON数据标记")
            else:
                print("❌ 输出中缺少JSON数据标记")
                print("实际输出:")
                print(output)
        else:
            print(f"❌ Python脚本执行失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    
    return False


def create_multiple_display_test():
    """创建多条显示测试数据"""
    print("\n📊 创建多条显示测试数据")
    
    test_file = "multiple_display_test.txt"
    test_data_list = []
    
    for i in range(3):
        data = {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -600 - i,
                "name": f"显示测试店铺{i+1}",
                "call_center": f"1360013600{i}",
                "address": f"测试省测试市测试区第{i+1}大街{i+1}号",
                "shipping_time": f"{9+i}:00-{21-i}:00",
                "shipping_fee": 3.0 + i * 0.5,
                "min_price": 20.0 + i * 5,
                "wm_poi_score": 4.0 + i * 0.2,
                "avg_delivery_time": 25 + i * 3,
                "comment_num": 100 + i * 50,
                "distance": f"{1.5 + i * 0.3}km",
                "month_sale_num": 200 + i * 100,
                "bulletin": f"这是第{i+1}个测试店铺，用于验证多条数据显示效果。"
            }
        }
        test_data_list.append(json.dumps(data, ensure_ascii=False))
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_data_list))
    
    print(f"✅ 创建多条测试数据: {test_file} (包含{len(test_data_list)}条记录)")
    return test_file


def test_multiple_data_extraction():
    """测试多条数据提取"""
    print("\n🔢 测试多条数据提取")
    
    test_file = create_multiple_display_test()
    output_file = "multiple_display_test.xlsx"
    
    try:
        result = subprocess.run([
            'python', 'shop_extractor.py', 
            test_file, output_file, '--json'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 多条数据提取成功")
            
            # 解析JSON输出
            output = result.stdout
            if 'JSON_DATA_START' in output:
                lines = output.split('\n')
                json_start = -1
                json_end = -1
                
                for i, line in enumerate(lines):
                    if line.strip() == 'JSON_DATA_START':
                        json_start = i + 1
                    elif line.strip() == 'JSON_DATA_END':
                        json_end = i
                        break
                
                if json_start != -1 and json_end != -1:
                    json_string = '\n'.join(lines[json_start:json_end])
                    data = json.loads(json_string)
                    
                    print(f"📊 成功提取 {len(data)} 条记录")
                    for i, shop in enumerate(data, 1):
                        print(f"  {i}. {shop.get('店铺名称', 'N/A')} - {shop.get('联系电话', 'N/A')}")
                    
                    return True
        else:
            print(f"❌ 多条数据提取失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    
    return False


def print_usage_instructions():
    """打印使用说明"""
    print("\n" + "=" * 60)
    print("🔧 提取结果显示修复 - 使用说明")
    print("=" * 60)
    print()
    print("📋 修复内容:")
    print("  ✅ 修改Python脚本支持JSON输出")
    print("  ✅ 修改main.js解析JSON数据")
    print("  ✅ 确保前端正确显示提取结果")
    print()
    print("🧪 测试步骤:")
    print("  1. 运行此测试脚本验证修复效果")
    print("  2. 启动Electron应用")
    print("  3. 选择测试数据文件")
    print("  4. 点击'开始提取'按钮")
    print("  5. 检查'提取结果'区域是否显示数据")
    print()
    print("📁 测试文件:")
    print("  • display_test.txt - 单条测试数据")
    print("  • multiple_display_test.txt - 多条测试数据")
    print("  • dianpuxinxi.txt - 原始测试数据")
    print()
    print("🔍 验证要点:")
    print("  • 结果表格显示店铺名称、电话、地址")
    print("  • 提取时间正确显示")
    print("  • 多条数据能正确显示")
    print("  • 追加模式正常工作")
    print()


def cleanup_test_files():
    """清理测试文件"""
    test_files = [
        "display_test.txt",
        "multiple_display_test.txt",
        "display_test_output.xlsx",
        "multiple_display_test.xlsx",
        "test_json.xlsx"
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


def main():
    """主函数"""
    print("🔧 提取结果显示修复测试")
    print("=" * 40)
    
    # 运行测试
    test1_passed = test_json_output()
    test2_passed = test_multiple_data_extraction()
    
    print("\n" + "=" * 40)
    print("📊 测试结果总结:")
    print(f"  JSON输出测试: {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"  多条数据测试: {'✅ 通过' if test2_passed else '❌ 失败'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 所有测试通过！修复成功！")
        print("\n📝 下一步:")
        print("  1. 重启Electron应用")
        print("  2. 使用测试数据验证界面显示")
        print("  3. 确认提取结果正确显示在表格中")
    else:
        print("\n⚠️ 部分测试失败，请检查修复代码")
    
    print_usage_instructions()
    
    # 询问是否清理测试文件
    if input("\n是否清理测试文件？(y/n): ").lower() == 'y':
        cleanup_test_files()


if __name__ == "__main__":
    main()
