#!/usr/bin/env python3
"""
AML规则引擎集成测试 - 完整工作流演示
"""

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

def main():
    print("=" * 60)
    print("AML规则引擎集成测试")
    print("地址 → API → 规则匹配 → 报告生成")
    print("=" * 60)
    
    # 测试地址
    test_chain = "Tron"
    test_address = "THaUdoNaeL7FEHFGpzEktHiJPsDctc6C6o"
    
    print(f"\n1. 测试地址: {test_address}")
    print(f"   链: {test_chain}")
    
    try:
        # 1. 获取交易图谱数据
        print("\n2. 获取交易图谱数据...")
        from graph_api import fetch_full_graph
        
        graph_data = fetch_full_graph(test_chain, test_address)
        
        if not graph_data or 'code' not in graph_data or graph_data['code'] != 0:
            print(f"   ❌ API调用失败: {graph_data}")
            return
            
        print(f"   ✅ 数据获取成功")
        print(f"   任务ID: {graph_data.get('data', {}).get('task_id', 'N/A')}")
        
        # 保存数据用于分析
        data = graph_data.get('data', {})
        tags = data.get('tags', [])
        paths = data.get('paths', [])
        
        print(f"   标签数量: {len(tags)}")
        print(f"   路径数量: {len(paths)}")
        
        # 显示风险分布
        risk_counts = {"high": 0, "medium": 0, "low": 0, "unknown": 0}
        for tag in tags:
            risk = tag.get('risk_level', 'unknown')
            if risk in risk_counts:
                risk_counts[risk] += 1
                
        print(f"   风险分布: {risk_counts}")
        
        # 2. 提取规则
        print("\n3. 提取法规规则...")
        from extract_rules import RuleExtractor
        
        extractor = RuleExtractor()
        rules = extractor.extract_singapore_rules()
        
        print(f"   ✅ 提取了 {len(rules)} 条新加坡规则")
        
        # 规则分类统计
        categories = {}
        for rule in rules:
            category = rule.get('category', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
            
        print("   规则分类:")
        for category, count in categories.items():
            print(f"     - {category}: {count} 条")
            
        # 保存规则
        rules_file = "test_singapore_rules.json"
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        print(f"   规则已保存到: {rules_file}")
        
        # 3. 应用规则引擎
        print("\n4. 应用规则引擎分析...")
        from rule_engine import RuleEngine
        
        engine = RuleEngine()
        
        # 加载规则到引擎
        for rule_data in rules:
            from rule_engine import Rule
            rule = Rule(
                rule_id=rule_data.get('rule_id'),
                jurisdiction=rule_data.get('jurisdiction'),
                category=rule_data.get('category'),
                rule_type=rule_data.get('rule_type'),
                description=rule_data.get('description'),
                threshold=rule_data.get('threshold'),
                currency=rule_data.get('currency'),
                condition=rule_data.get('condition'),
                screening_list=rule_data.get('screening_list'),
                action=rule_data.get('action'),
                risk_level=rule_data.get('risk_level'),
                source=rule_data.get('source'),
                user_customizable=rule_data.get('user_customizable', True),
                enabled=rule_data.get('enabled', True)
            )
            engine.rules.append(rule)
            
        print(f"   ✅ 加载了 {len(engine.rules)} 条规则到引擎")
        
        # 应用规则分析
        violations = engine.apply_rules_to_graph(graph_data)
        
        print(f"   ✅ 检测到 {len(violations)} 条违规")
        
        # 4. 生成报告
        print("\n5. 生成合规报告...")
        
        summary = engine.get_violations_summary()
        
        print(f"   违规摘要:")
        print(f"     - 总计: {summary.get('total_violations', 0)}")
        
        severity_counts = summary.get('severity_counts', {})
        for severity, count in severity_counts.items():
            if count > 0:
                print(f"     - {severity.upper()}: {count}")
                
        # 显示前3个违规
        if violations:
            print(f"\n   前3个违规详情:")
            for i, violation in enumerate(violations[:3]):
                print(f"\n   违规 #{i+1}:")
                print(f"     严重性: {violation.severity.value.upper()}")
                print(f"     描述: {violation.description}")
                print(f"     建议: {violation.recommendation}")
                print(f"     规则来源: {violation.rule_source}")
                
        # 保存完整报告
        report = {
            "test_address": test_address,
            "test_chain": test_chain,
            "jurisdiction": "Singapore",
            "graph_data_summary": {
                "total_tags": len(tags),
                "total_paths": len(paths),
                "risk_distribution": risk_counts
            },
            "rules_summary": {
                "total_rules": len(rules),
                "categories": categories
            },
            "violations_summary": summary,
            "violations": [v.to_dict() for v in violations],
            "sample_rules": rules[:5]  # 包含前5条规则作为示例
        }
        
        report_file = "aml_integration_test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ 集成测试完成!")
        print(f"   完整报告已保存到: {report_file}")
        
        # 5. 展示关键发现
        print("\n" + "=" * 60)
        print("关键发现总结")
        print("=" * 60)
        
        if violations:
            high_critical_violations = [
                v for v in violations 
                if v.severity.value in ['high', 'critical']
            ]
            
            if high_critical_violations:
                print(f"⚠️  发现 {len(high_critical_violations)} 个高风险违规")
                for v in high_critical_violations[:2]:
                    print(f"   • {v.description}")
            else:
                print("✅ 未发现高风险违规")
                
            # 检查是否有制裁相关违规
            sanction_violations = [
                v for v in violations 
                if 'sanction' in v.description.lower() or 'Sanctions' in v.rule_source
            ]
            
            if sanction_violations:
                print(f"⚠️  发现 {len(sanction_violations)} 个制裁相关违规")
        else:
            print("✅ 未发现违规")
            
        print(f"\n📊 分析统计:")
        print(f"   交易标签分析: {len(tags)} 个实体")
        print(f"   资金路径追踪: {len(paths)} 条路径")
        print(f"   法规规则应用: {len(rules)} 条规则")
        print(f"   合规违规检测: {len(violations)} 条违规")
        
        print("\n" + "=" * 60)
        print("集成测试成功完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())