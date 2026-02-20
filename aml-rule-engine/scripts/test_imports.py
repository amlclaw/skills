#!/usr/bin/env python3
"""测试模块导入"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

print("测试导入模块...")

try:
    from graph_api import fetch_full_graph
    print("✅ graph_api 导入成功")
except ImportError as e:
    print(f"❌ graph_api 导入失败: {e}")

try:
    from extract_rules import RuleExtractor
    print("✅ extract_rules 导入成功")
except ImportError as e:
    print(f"❌ extract_rules 导入失败: {e}")

try:
    from rule_engine import RuleEngine
    print("✅ rule_engine 导入成功")
except ImportError as e:
    print(f"❌ rule_engine 导入失败: {e}")

print("\n测试规则提取...")
try:
    extractor = RuleExtractor()
    rules = extractor.extract_singapore_rules()
    print(f"✅ 提取了 {len(rules)} 条新加坡规则")
except Exception as e:
    print(f"❌ 规则提取失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试API调用...")
try:
    # 使用一个简单的测试地址
    from graph_api import fetch_full_graph
    result = fetch_full_graph("Tron", "THaUdoNaeL7FEHFGpzEktHiJPsDctc6C6o")
    if result and 'code' in result and result['code'] == 0:
        print("✅ API调用成功")
        print(f"   任务ID: {result.get('data', {}).get('task_id', 'N/A')}")
    else:
        print(f"❌ API调用失败: {result}")
except Exception as e:
    print(f"❌ API调用异常: {e}")
    import traceback
    traceback.print_exc()