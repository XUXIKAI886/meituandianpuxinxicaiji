#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
店铺信息提取器
支持从JSON格式的文本文件中提取店铺信息
"""

import json
import re
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd


class ShopInfoExtractor:
    """店铺信息提取器类"""
    
    def __init__(self):
        self.extracted_data = []
        
    def extract_from_json(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """从JSON数据中提取店铺信息"""
        try:
            # 获取data字段
            data = json_data.get('data', {})
            
            # 提取基本信息（移除店铺ID、店铺公告、纬度、经度、距离）
            shop_info = {
                '提取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                '店铺名称': data.get('name', ''),
                '联系电话': data.get('call_center', ''),
                '电话列表': ', '.join(data.get('phone_list', [])),
                '店铺地址': data.get('address', ''),
                '店铺图片': data.get('pic_url', ''),
                '营业时间': data.get('shipping_time', ''),
                '配送费': data.get('shipping_fee', 0),
                '起送价': data.get('min_price', 0),
                '店铺评分': data.get('wm_poi_score', 0),
                '及时送达率': data.get('in_time_delivery_percent', 0),
                '平均接单时间': data.get('avg_accept_order_time', 0),
                '平均配送时间': data.get('avg_delivery_time', 0),
                '评论数量': data.get('comment_num', 0),
                '配送费提示': data.get('shipping_fee_tip', ''),
                '起送价提示': data.get('min_price_tip', ''),
                '配送时间提示': data.get('delivery_time_tip', ''),
                '月销量': data.get('month_sale_num', 0),
                '食品评分': data.get('food_score', 0),
                '配送评分': data.get('delivery_score', 0),
                '品牌类型': data.get('brand_type', 0),
                '配送类型': data.get('delivery_type', 0),
                '店铺状态': data.get('poi_sell_status', 0),
                '支持支付': data.get('support_pay', 0),
                '支持发票': data.get('invoice_support', 0)
            }
            
            # 提取优惠信息
            discounts = data.get('discounts2', [])
            if discounts:
                discount_info = []
                for discount in discounts:
                    discount_info.append(discount.get('info', ''))
                shop_info['优惠信息'] = '; '.join(discount_info)
            else:
                shop_info['优惠信息'] = ''
            
            # 提取展示信息
            show_info = data.get('show_info', [])
            for info in show_info:
                name = info.get('name', '')
                value = info.get('value', '')
                unit = info.get('unit', '')
                if name and value:
                    shop_info[f'{name}'] = f"{value}{unit}"
            
            return shop_info
            
        except Exception as e:
            print(f"提取JSON数据时出错: {e}")
            return {}
    
    def extract_from_text_file(self, file_path: str) -> List[Dict[str, Any]]:
        """从文本文件中提取店铺信息"""
        extracted_shops = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                
            # 尝试解析JSON格式
            if content.startswith('{') and content.endswith('}'):
                try:
                    json_data = json.loads(content)
                    shop_info = self.extract_from_json(json_data)
                    if shop_info:
                        extracted_shops.append(shop_info)
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {e}")
            
            # 如果文件包含多行JSON数据
            elif '\n' in content:
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and line.startswith('{') and line.endswith('}'):
                        try:
                            json_data = json.loads(line)
                            shop_info = self.extract_from_json(json_data)
                            if shop_info:
                                extracted_shops.append(shop_info)
                        except json.JSONDecodeError:
                            continue
            
            return extracted_shops
            
        except Exception as e:
            print(f"读取文件时出错: {e}")
            return []
    
    def save_to_excel(self, data: List[Dict[str, Any]], output_file: str, append: bool = False):
        """保存数据到Excel文件"""
        try:
            if not data:
                print("没有数据需要保存")
                return False

            df = pd.DataFrame(data)
            original_count = len(df)

            if append and os.path.exists(output_file):
                # 追加模式：读取现有数据并合并
                try:
                    existing_df = pd.read_excel(output_file)
                    df = pd.concat([existing_df, df], ignore_index=True)
                except Exception as e:
                    print(f"读取现有Excel文件时出错: {e}")

            # 去重处理：基于店铺名称和地址的组合
            if len(df) > 0:
                before_dedup_count = len(df)
                # 使用店铺名称和店铺地址作为去重标准
                df = df.drop_duplicates(subset=['店铺名称', '店铺地址'], keep='first')
                after_dedup_count = len(df)
                duplicate_count = before_dedup_count - after_dedup_count

                if duplicate_count > 0:
                    print(f"检测到 {duplicate_count} 条重复数据，已自动去除")
                    print(f"去重前: {before_dedup_count} 条，去重后: {after_dedup_count} 条")

            # 保存到Excel文件
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"数据已保存到: {output_file}")
            return True

        except Exception as e:
            print(f"保存Excel文件时出错: {e}")
            return False
    
    def process_file(self, input_file: str, output_file: str = None, append: bool = False) -> List[Dict[str, Any]]:
        """处理单个文件"""
        if not os.path.exists(input_file):
            print(f"文件不存在: {input_file}")
            return []
        
        print(f"正在处理文件: {input_file}")
        extracted_data = self.extract_from_text_file(input_file)
        
        if extracted_data:
            print(f"成功提取 {len(extracted_data)} 条店铺信息")
            
            # 如果指定了输出文件，则保存到Excel
            if output_file:
                self.save_to_excel(extracted_data, output_file, append)
        else:
            print("未提取到任何店铺信息")
        
        return extracted_data


def main():
    """主函数 - 命令行接口"""
    if len(sys.argv) < 2:
        print("使用方法: python shop_extractor.py <输入文件> [输出文件] [--append] [--json]")
        print("示例: python shop_extractor.py dianpuxinxi.txt shops.xlsx")
        print("示例: python shop_extractor.py dianpuxinxi.txt shops.xlsx --append")
        print("示例: python shop_extractor.py dianpuxinxi.txt shops.xlsx --json")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    append_mode = '--append' in sys.argv
    json_output = '--json' in sys.argv

    extractor = ShopInfoExtractor()
    extracted_data = extractor.process_file(input_file, output_file, append_mode)

    # 输出提取结果
    if extracted_data:
        # 打印提取的数据概览
        print("\n提取的店铺信息概览:")
        for i, shop in enumerate(extracted_data, 1):
            name = shop.get('店铺名称', 'N/A')
            address = shop.get('店铺地址', 'N/A')
            phone = shop.get('联系电话', 'N/A')
            print(f"{i}. {name} - {phone} - {address}")


if __name__ == "__main__":
    main()
