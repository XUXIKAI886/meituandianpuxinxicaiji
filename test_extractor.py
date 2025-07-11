#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
店铺信息提取器测试脚本
用于验证数据提取功能的正确性
"""

import json
import os
import sys
from shop_extractor import ShopInfoExtractor


def test_json_extraction():
    """测试JSON数据提取功能"""
    print("=== 测试JSON数据提取功能 ===")
    
    # 测试数据
    test_json = {
        "msg": "成功",
        "code": 0,
        "data": {
            "id": -100,
            "status": 1,
            "name": "红星面馆(牛肉面，热干面)",
            "call_center": "18827288411",
            "phone_list": ["18827288411"],
            "address": "湖北省宜昌市夷陵区小溪塔街道峡洲路10号-13",
            "pic_url": "http://p0.meituan.net/business/945fc670fcbce1cf85fef15ccd633df0206110.jpg",
            "shipping_time": "06:00-13:00",
            "shipping_fee": 5.1,
            "min_price": 20.0,
            "bulletin": "欢迎您光临本店：新店开业，如有不足之处，请您多多海涵并向我们多提建议！",
            "wm_poi_score": 0.0,
            "in_time_delivery_percent": 0,
            "avg_accept_order_time": 0,
            "avg_delivery_time": 33,
            "comment_num": 0,
            "latitude": 30766514,
            "longitude": 111309214,
            "distance": "4.2km",
            "shipping_fee_tip": "配送 ¥1.1",
            "min_price_tip": "起送 ¥20",
            "delivery_time_tip": "33分钟",
            "month_sale_num": 0,
            "food_score": 0.0,
            "delivery_score": 0.0
        }
    }
    
    extractor = ShopInfoExtractor()
    result = extractor.extract_from_json(test_json)
    
    if result:
        print("✓ JSON提取成功")
        print(f"店铺名称: {result.get('店铺名称', 'N/A')}")
        print(f"联系电话: {result.get('联系电话', 'N/A')}")
        print(f"店铺地址: {result.get('店铺地址', 'N/A')}")
        print(f"营业时间: {result.get('营业时间', 'N/A')}")
        print(f"配送费: {result.get('配送费', 'N/A')}")
        print(f"起送价: {result.get('起送价', 'N/A')}")
        return True
    else:
        print("✗ JSON提取失败")
        return False


def test_file_extraction():
    """测试文件提取功能"""
    print("\n=== 测试文件提取功能 ===")
    
    input_file = "dianpuxinxi.txt"
    if not os.path.exists(input_file):
        print(f"✗ 测试文件不存在: {input_file}")
        return False
    
    extractor = ShopInfoExtractor()
    results = extractor.extract_from_text_file(input_file)
    
    if results:
        print(f"✓ 文件提取成功，共提取 {len(results)} 条记录")
        for i, result in enumerate(results, 1):
            print(f"记录 {i}:")
            print(f"  店铺名称: {result.get('店铺名称', 'N/A')}")
            print(f"  联系电话: {result.get('联系电话', 'N/A')}")
            print(f"  店铺地址: {result.get('店铺地址', 'N/A')}")
        return True
    else:
        print("✗ 文件提取失败")
        return False


def test_excel_export():
    """测试Excel导出功能"""
    print("\n=== 测试Excel导出功能 ===")
    
    # 创建测试数据
    test_data = [
        {
            '提取时间': '2024-01-20 10:30:00',
            '店铺ID': -100,
            '店铺名称': '红星面馆(牛肉面，热干面)',
            '联系电话': '18827288411',
            '店铺地址': '湖北省宜昌市夷陵区小溪塔街道峡洲路10号-13',
            '营业时间': '06:00-13:00',
            '配送费': 5.1,
            '起送价': 20.0,
            '店铺评分': 0.0,
            '平均配送时间': 33,
            '评论数量': 0
        }
    ]
    
    extractor = ShopInfoExtractor()
    output_file = "test_export.xlsx"
    
    # 测试新建文件
    success = extractor.save_to_excel(test_data, output_file, append=False)
    if success and os.path.exists(output_file):
        print("✓ Excel导出成功")
        
        # 测试追加模式
        success_append = extractor.save_to_excel(test_data, output_file, append=True)
        if success_append:
            print("✓ Excel追加模式成功")
            return True
        else:
            print("✗ Excel追加模式失败")
            return False
    else:
        print("✗ Excel导出失败")
        return False


def test_complete_workflow():
    """测试完整工作流程"""
    print("\n=== 测试完整工作流程 ===")
    
    input_file = "dianpuxinxi.txt"
    output_file = "workflow_test.xlsx"
    
    if not os.path.exists(input_file):
        print(f"✗ 输入文件不存在: {input_file}")
        return False
    
    extractor = ShopInfoExtractor()
    
    # 执行完整流程
    results = extractor.process_file(input_file, output_file, append=False)
    
    if results and os.path.exists(output_file):
        print("✓ 完整工作流程测试成功")
        print(f"  处理文件: {input_file}")
        print(f"  输出文件: {output_file}")
        print(f"  提取记录: {len(results)} 条")
        return True
    else:
        print("✗ 完整工作流程测试失败")
        return False


def cleanup_test_files():
    """清理测试文件"""
    test_files = ["test_export.xlsx", "workflow_test.xlsx"]
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"已清理测试文件: {file}")
            except Exception as e:
                print(f"清理文件失败 {file}: {e}")


def main():
    """主测试函数"""
    print("店铺信息提取器 - 功能测试")
    print("=" * 50)
    
    tests = [
        ("JSON数据提取", test_json_extraction),
        ("文件提取功能", test_file_extraction),
        ("Excel导出功能", test_excel_export),
        ("完整工作流程", test_complete_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} 测试出错: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查相关功能")
    
    # 询问是否清理测试文件
    if input("\n是否清理测试文件？(y/n): ").lower() == 'y':
        cleanup_test_files()


if __name__ == "__main__":
    main()
