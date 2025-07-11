#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查字段移除效果
"""

import pandas as pd
import os

def check_excel_fields():
    """检查Excel文件的字段"""
    excel_file = "test_clean.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel文件不存在: {excel_file}")
        return
    
    try:
        df = pd.read_excel(excel_file)
        
        print("📊 Excel文件字段检查")
        print("=" * 40)
        print(f"总字段数: {len(df.columns)}")
        print(f"数据行数: {len(df)}")
        print()
        
        print("📋 字段列表:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # 检查移除的字段
        removed_fields = ['店铺ID', '店铺公告', '纬度', '经度', '距离']
        
        print(f"\n🔍 移除字段检查:")
        for field in removed_fields:
            if field in df.columns:
                print(f"  ❌ {field}: 仍然存在")
            else:
                print(f"  ✅ {field}: 已移除")
        
        # 检查重要字段
        important_fields = ['店铺名称', '联系电话', '店铺地址']
        
        print(f"\n📝 重要字段检查:")
        for field in important_fields:
            if field in df.columns:
                print(f"  ✅ {field}: 存在")
            else:
                print(f"  ❌ {field}: 缺失")
        
        # 显示第一行数据示例
        if len(df) > 0:
            print(f"\n📄 第一行数据示例:")
            first_row = df.iloc[0]
            for col in ['店铺名称', '联系电话', '店铺地址']:
                if col in df.columns:
                    print(f"  {col}: {first_row[col]}")
        
    except Exception as e:
        print(f"❌ 读取Excel文件失败: {e}")

if __name__ == "__main__":
    check_excel_fields()
