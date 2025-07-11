#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试固定路径功能
验证应用是否正确使用固定的数据源路径
"""

import os
import json
import shutil
from datetime import datetime


def create_test_data_at_fixed_path():
    """在固定路径创建测试数据"""
    fixed_path = r"D:\ailun\dianpuxinxi.txt"
    
    # 创建目录（如果不存在）
    os.makedirs(os.path.dirname(fixed_path), exist_ok=True)
    
    # 创建测试数据
    test_data = {
        "msg": "成功",
        "code": 0,
        "data": {
            "id": -700,
            "status": 1,
            "name": "固定路径测试餐厅",
            "call_center": "13700137000",
            "phone_list": ["13700137000"],
            "address": "固定路径测试省固定路径测试市固定路径测试区测试街道700号",
            "pic_url": "http://example.com/fixed_path_test.jpg",
            "shipping_time": "08:00-22:00",
            "shipping_fee": 5.0,
            "min_price": 30.0,
            "bulletin": "这是固定路径测试数据，用于验证应用是否正确读取D:\\ailun\\dianpuxinxi.txt文件。",
            "wm_poi_score": 4.9,
            "in_time_delivery_percent": 99,
            "avg_accept_order_time": 2,
            "avg_delivery_time": 20,
            "comment_num": 500,
            "latitude": 39910016,
            "longitude": 116410128,
            "distance": "1.5km",
            "shipping_fee_tip": "配送 ¥5",
            "min_price_tip": "起送 ¥30",
            "delivery_time_tip": "20分钟",
            "month_sale_num": 1000,
            "food_score": 5.0,
            "delivery_score": 4.8,
            "brand_type": 1,
            "delivery_type": 1,
            "poi_sell_status": 1,
            "support_pay": 1,
            "invoice_support": 1,
            "discounts2": [
                {"info": "固定路径测试优惠"},
                {"info": "满50减10元"},
                {"info": "免配送费"}
            ],
            "show_info": [
                {"name": "月销量", "value": "1000", "unit": "单"},
                {"name": "好评率", "value": "99", "unit": "%"},
                {"name": "配送时间", "value": "20", "unit": "分钟"}
            ]
        }
    }
    
    # 写入文件
    with open(fixed_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已在固定路径创建测试数据: {fixed_path}")
    return fixed_path


def backup_existing_file():
    """备份现有文件（如果存在）"""
    fixed_path = r"D:\ailun\dianpuxinxi.txt"
    backup_path = r"D:\ailun\dianpuxinxi_backup.txt"
    
    if os.path.exists(fixed_path):
        try:
            shutil.copy2(fixed_path, backup_path)
            print(f"✅ 已备份现有文件到: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ 备份文件失败: {e}")
            return False
    else:
        print("ℹ️ 固定路径文件不存在，无需备份")
        return True


def restore_backup():
    """恢复备份文件"""
    fixed_path = r"D:\ailun\dianpuxinxi.txt"
    backup_path = r"D:\ailun\dianpuxinxi_backup.txt"
    
    if os.path.exists(backup_path):
        try:
            shutil.copy2(backup_path, fixed_path)
            os.remove(backup_path)
            print(f"✅ 已恢复备份文件")
            return True
        except Exception as e:
            print(f"❌ 恢复备份失败: {e}")
            return False
    else:
        print("ℹ️ 没有备份文件需要恢复")
        return True


def test_fixed_path_extraction():
    """测试固定路径数据提取"""
    print("\n🧪 测试固定路径数据提取")
    
    fixed_path = r"D:\ailun\dianpuxinxi.txt"
    
    if not os.path.exists(fixed_path):
        print(f"❌ 固定路径文件不存在: {fixed_path}")
        return False
    
    # 使用shop_extractor测试
    import subprocess
    
    try:
        result = subprocess.run([
            'python', 'shop_extractor.py', 
            fixed_path, 'test_fixed_path_output.xlsx'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 固定路径数据提取成功")
            
            # 检查输出
            output = result.stdout
            if '固定路径测试餐厅' in output:
                print("✅ 测试数据正确提取")
                return True
            else:
                print("❌ 测试数据未正确提取")
                print("输出内容:", output)
                return False
        else:
            print(f"❌ 数据提取失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False


def check_path_accessibility():
    """检查路径可访问性"""
    print("\n🔍 检查路径可访问性")
    
    fixed_path = r"D:\ailun\dianpuxinxi.txt"
    directory = os.path.dirname(fixed_path)
    
    # 检查目录
    if os.path.exists(directory):
        print(f"✅ 目录存在: {directory}")
    else:
        print(f"❌ 目录不存在: {directory}")
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ 已创建目录: {directory}")
        except Exception as e:
            print(f"❌ 创建目录失败: {e}")
            return False
    
    # 检查文件
    if os.path.exists(fixed_path):
        print(f"✅ 文件存在: {fixed_path}")
        
        # 检查文件大小
        file_size = os.path.getsize(fixed_path)
        print(f"📊 文件大小: {file_size} 字节")
        
        # 检查文件修改时间
        mod_time = os.path.getmtime(fixed_path)
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"⏰ 修改时间: {mod_time_str}")
        
        return True
    else:
        print(f"❌ 文件不存在: {fixed_path}")
        return False


def print_usage_guide():
    """打印使用指南"""
    print("\n" + "=" * 60)
    print("📋 固定路径功能使用指南")
    print("=" * 60)
    print()
    print("🎯 功能说明:")
    print("  • 数据源文件路径已固定为: D:\\ailun\\dianpuxinxi.txt")
    print("  • 用户无需手动选择文件，应用自动使用固定路径")
    print("  • 界面显示固定路径，不可修改")
    print()
    print("📁 文件要求:")
    print("  • 文件必须存在于: D:\\ailun\\dianpuxinxi.txt")
    print("  • 文件格式: JSON格式的店铺信息")
    print("  • 文件编码: UTF-8")
    print()
    print("🔧 使用步骤:")
    print("  1. 确保D:\\ailun\\目录存在")
    print("  2. 将店铺信息文件放置到指定路径")
    print("  3. 启动应用，选择Excel输出文件")
    print("  4. 点击'开始提取'按钮")
    print()
    print("⚠️ 注意事项:")
    print("  • 如果文件不存在，提取将失败")
    print("  • 确保对D:\\ailun\\目录有读取权限")
    print("  • 文件更新后可使用监控功能自动提取")
    print()


def cleanup_test_files():
    """清理测试文件"""
    test_files = [
        "test_fixed_path_output.xlsx"
    ]
    
    cleaned = 0
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️ 已删除测试文件: {file}")
                cleaned += 1
            except Exception as e:
                print(f"❌ 删除失败 {file}: {e}")
    
    if cleaned > 0:
        print(f"✅ 清理完成，共删除 {cleaned} 个文件")


def main():
    """主函数"""
    print("🔧 固定路径功能测试")
    print("=" * 50)
    
    # 检查路径可访问性
    path_ok = check_path_accessibility()
    
    if not path_ok:
        print("\n⚠️ 路径检查失败，尝试创建测试数据...")
    
    # 备份现有文件
    backup_ok = backup_existing_file()
    
    # 创建测试数据
    test_file = create_test_data_at_fixed_path()
    
    # 测试数据提取
    test_passed = test_fixed_path_extraction()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"  路径检查: {'✅ 通过' if path_ok else '❌ 失败'}")
    print(f"  文件备份: {'✅ 完成' if backup_ok else '❌ 失败'}")
    print(f"  数据提取: {'✅ 通过' if test_passed else '❌ 失败'}")
    
    if test_passed:
        print("\n🎉 固定路径功能测试通过！")
        print("📝 现在可以在应用中:")
        print("  1. 看到固定的数据源路径")
        print("  2. 直接选择输出文件并提取数据")
        print("  3. 使用文件监控功能")
    else:
        print("\n⚠️ 测试失败，请检查:")
        print("  1. D:\\ailun\\目录权限")
        print("  2. 文件格式是否正确")
        print("  3. Python依赖是否完整")
    
    # 显示使用指南
    print_usage_guide()
    
    # 询问是否恢复备份
    if backup_ok and input("\n是否恢复原始文件？(y/n): ").lower() == 'y':
        restore_backup()
    
    # 清理测试文件
    cleanup_test_files()


if __name__ == "__main__":
    main()
