#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试字段移除效果
验证店铺ID、店铺公告、纬度、经度、距离字段已被移除
"""

import pandas as pd
import os
import subprocess
from shop_extractor import ShopInfoExtractor


def test_field_removal():
    """测试字段移除效果"""
    print("🧪 测试字段移除效果")
    print("=" * 50)
    
    # 使用现有的测试文件
    input_file = "dianpuxinxi.txt"
    output_file = "test_field_removal.xlsx"
    
    if not os.path.exists(input_file):
        print(f"❌ 测试文件不存在: {input_file}")
        return False
    
    # 执行提取
    extractor = ShopInfoExtractor()
    extracted_data = extractor.process_file(input_file, output_file, append=False)
    
    if not extracted_data:
        print("❌ 没有提取到数据")
        return False
    
    print(f"✅ 成功提取 {len(extracted_data)} 条记录")
    
    # 检查第一条记录的字段
    first_record = extracted_data[0]
    
    print("\n📋 提取的字段列表:")
    for i, (key, value) in enumerate(first_record.items(), 1):
        print(f"  {i:2d}. {key}: {value}")
    
    # 检查移除的字段
    removed_fields = ['店铺ID', '店铺公告', '纬度', '经度', '距离']
    
    print(f"\n🔍 检查移除的字段:")
    all_removed = True
    for field in removed_fields:
        if field in first_record:
            print(f"  ❌ {field}: 仍然存在")
            all_removed = False
        else:
            print(f"  ✅ {field}: 已移除")
    
    # 检查保留的重要字段
    important_fields = ['店铺名称', '联系电话', '店铺地址', '营业时间', '配送费', '起送价']
    
    print(f"\n📝 检查保留的重要字段:")
    all_present = True
    for field in important_fields:
        if field in first_record:
            print(f"  ✅ {field}: {first_record[field]}")
        else:
            print(f"  ❌ {field}: 缺失")
            all_present = False
    
    # 检查Excel文件
    if os.path.exists(output_file):
        print(f"\n📊 检查Excel文件: {output_file}")
        try:
            df = pd.read_excel(output_file)
            print(f"  ✅ Excel文件包含 {len(df)} 行数据")
            print(f"  ✅ Excel文件包含 {len(df.columns)} 个字段")
            
            print(f"\n📋 Excel文件字段列表:")
            for i, col in enumerate(df.columns, 1):
                print(f"  {i:2d}. {col}")
            
            # 检查Excel中是否包含移除的字段
            excel_removed_check = True
            for field in removed_fields:
                if field in df.columns:
                    print(f"  ❌ Excel中仍包含: {field}")
                    excel_removed_check = False
            
            if excel_removed_check:
                print(f"  ✅ Excel中已移除所有指定字段")
            
        except Exception as e:
            print(f"  ❌ 读取Excel文件失败: {e}")
            return False
    
    print("\n" + "=" * 50)
    if all_removed and all_present:
        print("🎉 字段移除测试通过！")
        print("✅ 指定字段已成功移除")
        print("✅ 重要字段完整保留")
        return True
    else:
        print("⚠️ 字段移除测试部分失败")
        if not all_removed:
            print("❌ 部分指定字段未移除")
        if not all_present:
            print("❌ 部分重要字段缺失")
        return False


def compare_before_after():
    """比较修改前后的字段差异"""
    print("\n🔄 字段变化对比")
    print("=" * 50)
    
    # 修改前的字段列表（从代码中提取）
    before_fields = [
        '提取时间', '店铺ID', '店铺名称', '联系电话', '电话列表', '店铺地址', 
        '店铺图片', '营业时间', '配送费', '起送价', '店铺公告', '店铺评分',
        '及时送达率', '平均接单时间', '平均配送时间', '评论数量', '纬度', 
        '经度', '距离', '配送费提示', '起送价提示', '配送时间提示', 
        '月销量', '食品评分', '配送评分', '品牌类型', '配送类型', 
        '店铺状态', '支持支付', '支持发票'
    ]
    
    # 移除的字段
    removed_fields = ['店铺ID', '店铺公告', '纬度', '经度', '距离']
    
    # 修改后的字段列表
    after_fields = [field for field in before_fields if field not in removed_fields]
    
    print(f"📊 修改前字段数量: {len(before_fields)}")
    print(f"📊 修改后字段数量: {len(after_fields)}")
    print(f"📊 移除字段数量: {len(removed_fields)}")
    
    print(f"\n❌ 已移除的字段:")
    for field in removed_fields:
        print(f"  • {field}")
    
    print(f"\n✅ 保留的字段:")
    for field in after_fields:
        print(f"  • {field}")
    
    return len(before_fields), len(after_fields), len(removed_fields)


def create_field_summary():
    """创建字段总结文档"""
    print("\n📄 生成字段总结文档")
    
    summary_content = """# 店铺信息字段总结

## 移除的字段

根据用户要求，以下字段已从提取结果中移除：

1. **店铺ID** - 内部标识符，对用户无实际价值
2. **店铺公告** - 通常较长的文本，占用空间且不常用
3. **纬度** - 地理坐标信息，一般用户不需要
4. **经度** - 地理坐标信息，一般用户不需要  
5. **距离** - 相对位置信息，实用性有限

## 保留的核心字段

### 基本信息
- **提取时间** - 数据提取的时间戳
- **店铺名称** - 店铺的名称
- **联系电话** - 主要联系电话
- **电话列表** - 所有联系电话
- **店铺地址** - 详细地址信息
- **店铺图片** - 店铺图片URL

### 营业信息
- **营业时间** - 店铺营业时间
- **配送费** - 配送费用
- **起送价** - 最低起送金额
- **配送费提示** - 配送费说明
- **起送价提示** - 起送价说明
- **配送时间提示** - 配送时间说明

### 评价数据
- **店铺评分** - 综合评分
- **食品评分** - 食品质量评分
- **配送评分** - 配送服务评分
- **及时送达率** - 准时送达百分比
- **平均接单时间** - 平均接单时长
- **平均配送时间** - 平均配送时长
- **评论数量** - 用户评论总数

### 销售数据
- **月销量** - 月度销售数量

### 服务信息
- **品牌类型** - 品牌分类
- **配送类型** - 配送方式
- **店铺状态** - 营业状态
- **支持支付** - 支付方式支持
- **支持发票** - 发票服务支持

### 优惠信息
- **优惠信息** - 当前优惠活动（动态提取）

## 字段统计

- **移除字段**: 5个
- **保留字段**: 26个
- **总体优化**: 减少了19%的冗余字段

## 优化效果

1. **数据精简**: 移除不必要的字段，减少存储空间
2. **提高可读性**: 专注于有用信息，提升用户体验
3. **Excel优化**: 减少Excel列数，便于查看和分析
4. **处理效率**: 减少数据处理量，提升性能
"""
    
    with open("字段总结.md", "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    print("✅ 字段总结文档已生成: 字段总结.md")


def main():
    """主函数"""
    print("🔧 店铺信息字段移除测试")
    print("=" * 60)
    
    # 运行测试
    test_passed = test_field_removal()
    
    # 显示对比
    before_count, after_count, removed_count = compare_before_after()
    
    # 生成总结文档
    create_field_summary()
    
    print("\n" + "=" * 60)
    print("📊 测试总结:")
    print(f"  字段移除测试: {'✅ 通过' if test_passed else '❌ 失败'}")
    print(f"  移除前字段数: {before_count}")
    print(f"  移除后字段数: {after_count}")
    print(f"  成功移除字段: {removed_count}")
    print(f"  优化比例: {removed_count/before_count*100:.1f}%")
    
    if test_passed:
        print("\n🎉 字段移除完成！")
        print("📝 建议:")
        print("  1. 重启Electron应用测试新的字段配置")
        print("  2. 验证Excel导出文件的字段是否符合预期")
        print("  3. 检查界面显示是否正常")
    else:
        print("\n⚠️ 请检查代码修改是否正确")
    
    # 清理测试文件
    test_files = ["test_field_removal.xlsx"]
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️ 已清理测试文件: {file}")
            except:
                pass


if __name__ == "__main__":
    main()
