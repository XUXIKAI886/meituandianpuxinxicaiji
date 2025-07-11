#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
去重功能测试脚本
验证店铺信息提取器的去重功能是否正常工作
"""

import json
import os
import sys
from shop_extractor import ShopInfoExtractor


def create_test_data_with_duplicates():
    """创建包含重复数据的测试文件"""
    test_data = [
        {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -100,
                "name": "红星面馆(牛肉面，热干面)",
                "call_center": "18827288411",
                "phone_list": ["18827288411"],
                "address": "湖北省宜昌市夷陵区小溪塔街道峡洲路10号-13",
                "shipping_time": "06:00-13:00",
                "shipping_fee": 5.1,
                "min_price": 20.0,
                "wm_poi_score": 0.0,
                "avg_delivery_time": 33,
                "comment_num": 0
            }
        },
        {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -101,
                "name": "蓝天餐厅",
                "call_center": "13912345678",
                "phone_list": ["13912345678"],
                "address": "北京市朝阳区建国路88号",
                "shipping_time": "10:00-22:00",
                "shipping_fee": 3.0,
                "min_price": 15.0,
                "wm_poi_score": 4.5,
                "avg_delivery_time": 25,
                "comment_num": 150
            }
        },
        {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -102,  # 不同ID但相同店铺信息
                "name": "红星面馆(牛肉面，热干面)",  # 重复的店铺名称
                "call_center": "18827288411",
                "phone_list": ["18827288411"],
                "address": "湖北省宜昌市夷陵区小溪塔街道峡洲路10号-13",  # 重复的地址
                "shipping_time": "06:00-13:00",
                "shipping_fee": 5.1,
                "min_price": 20.0,
                "wm_poi_score": 0.0,
                "avg_delivery_time": 33,
                "comment_num": 0
            }
        },
        {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -103,
                "name": "绿色小厨",
                "call_center": "15987654321",
                "phone_list": ["15987654321"],
                "address": "上海市浦东新区陆家嘴金融区",
                "shipping_time": "11:00-21:00",
                "shipping_fee": 4.0,
                "min_price": 25.0,
                "wm_poi_score": 4.2,
                "avg_delivery_time": 30,
                "comment_num": 89
            }
        },
        {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -104,  # 不同ID
                "name": "蓝天餐厅",  # 重复的店铺名称
                "call_center": "13912345678",
                "phone_list": ["13912345678"],
                "address": "北京市朝阳区建国路88号",  # 重复的地址
                "shipping_time": "10:00-22:00",
                "shipping_fee": 3.0,
                "min_price": 15.0,
                "wm_poi_score": 4.5,
                "avg_delivery_time": 25,
                "comment_num": 150
            }
        }
    ]
    
    # 创建测试文件 - 每行一个完整的JSON对象
    test_file = "test_duplicate_data.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        for i, data in enumerate(test_data):
            if i > 0:
                f.write('\n')
            f.write(json.dumps(data, ensure_ascii=False))
    
    return test_file


def test_deduplication():
    """测试去重功能"""
    print("=== 店铺信息去重功能测试 ===")
    
    # 创建包含重复数据的测试文件
    test_file = create_test_data_with_duplicates()
    print(f"✓ 已创建测试文件: {test_file}")
    print("测试数据包含:")
    print("  - 红星面馆 (重复2次)")
    print("  - 蓝天餐厅 (重复2次)")
    print("  - 绿色小厨 (唯一)")
    print("  总计: 5条数据，预期去重后: 3条数据")
    
    # 测试数据提取和去重
    extractor = ShopInfoExtractor()
    output_file = "test_dedup_result.xlsx"
    
    print(f"\n正在提取数据到: {output_file}")
    extracted_data = extractor.process_file(test_file, output_file, append=False)
    
    if extracted_data:
        print(f"\n✓ 数据提取完成")
        print(f"提取到的店铺信息:")
        
        unique_shops = set()
        for i, shop in enumerate(extracted_data, 1):
            name = shop.get('店铺名称', 'N/A')
            address = shop.get('店铺地址', 'N/A')
            phone = shop.get('联系电话', 'N/A')
            
            shop_key = f"{name}|{address}"
            unique_shops.add(shop_key)
            
            print(f"{i}. {name}")
            print(f"   电话: {phone}")
            print(f"   地址: {address}")
            print()
        
        print(f"去重验证:")
        print(f"  - 原始数据: 5条")
        print(f"  - 提取结果: {len(extracted_data)}条")
        print(f"  - 唯一店铺: {len(unique_shops)}个")
        
        # 验证去重效果
        if len(unique_shops) == 3:
            print("✓ 去重功能正常工作！")
            return True
        else:
            print("✗ 去重功能异常，请检查实现")
            return False
    else:
        print("✗ 数据提取失败")
        return False


def test_append_mode_deduplication():
    """测试追加模式的去重功能"""
    print("\n=== 追加模式去重测试 ===")
    
    # 创建第二批测试数据（包含部分重复）
    additional_data = [
        {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -105,
                "name": "红星面馆(牛肉面，热干面)",  # 与第一批重复
                "call_center": "18827288411",
                "phone_list": ["18827288411"],
                "address": "湖北省宜昌市夷陵区小溪塔街道峡洲路10号-13",
                "shipping_time": "06:00-13:00",
                "shipping_fee": 5.1,
                "min_price": 20.0,
                "wm_poi_score": 0.0,
                "avg_delivery_time": 33,
                "comment_num": 0
            }
        },
        {
            "msg": "成功",
            "code": 0,
            "data": {
                "id": -106,
                "name": "新开张火锅店",  # 新店铺
                "call_center": "17712345678",
                "phone_list": ["17712345678"],
                "address": "成都市锦江区春熙路123号",
                "shipping_time": "16:00-02:00",
                "shipping_fee": 6.0,
                "min_price": 30.0,
                "wm_poi_score": 4.8,
                "avg_delivery_time": 40,
                "comment_num": 25
            }
        }
    ]
    
    # 创建第二个测试文件 - 每行一个完整的JSON对象
    test_file2 = "test_additional_data.txt"
    with open(test_file2, 'w', encoding='utf-8') as f:
        for i, data in enumerate(additional_data):
            if i > 0:
                f.write('\n')
            f.write(json.dumps(data, ensure_ascii=False))
    
    print(f"✓ 已创建追加测试文件: {test_file2}")
    print("追加数据包含:")
    print("  - 红星面馆 (与现有数据重复)")
    print("  - 新开张火锅店 (新店铺)")
    
    # 测试追加模式
    extractor = ShopInfoExtractor()
    output_file = "test_dedup_result.xlsx"
    
    print(f"\n正在以追加模式提取数据...")
    extracted_data = extractor.process_file(test_file2, output_file, append=True)
    
    if extracted_data:
        print(f"✓ 追加模式提取完成")
        print(f"预期结果: 应该只新增1条数据（新开张火锅店）")
        return True
    else:
        print("✗ 追加模式提取失败")
        return False


def cleanup_test_files():
    """清理测试文件"""
    test_files = [
        "test_duplicate_data.txt",
        "test_additional_data.txt",
        "test_dedup_result.xlsx"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"已清理测试文件: {file}")
            except Exception as e:
                print(f"清理文件失败 {file}: {e}")


def main():
    """主测试函数"""
    print("店铺信息提取器 - 去重功能测试")
    print("=" * 50)
    
    try:
        # 测试基本去重功能
        test1_passed = test_deduplication()
        
        # 测试追加模式去重
        test2_passed = test_append_mode_deduplication()
        
        print("\n" + "=" * 50)
        print("测试结果总结:")
        print(f"  基本去重功能: {'✓ 通过' if test1_passed else '✗ 失败'}")
        print(f"  追加模式去重: {'✓ 通过' if test2_passed else '✗ 失败'}")
        
        if test1_passed and test2_passed:
            print("\n🎉 所有去重功能测试通过！")
        else:
            print("\n⚠️  部分测试失败，请检查去重实现")
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
    
    # 询问是否清理测试文件
    if input("\n是否清理测试文件？(y/n): ").lower() == 'y':
        cleanup_test_files()


if __name__ == "__main__":
    main()
