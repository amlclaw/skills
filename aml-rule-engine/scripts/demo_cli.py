#!/usr/bin/env python3
"""
AML规则引擎演示CLI - 端到端检测流程
"""

import sys
import json
import argparse
from pathlib import Path

# 添加当前目录到路径，以便导入其他模块
sys.path.append(str(Path(__file__).parent))

try:
    from graph_api import fetch_full_graph
    from extract_rules import RuleExtractor
    from rule_engine import RuleEngine, Violation, RiskLevel
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保 graph_api.py, extract_rules.py, rule_engine.py 在同一目录")
    sys.exit(1)

class AMLCheckerCLI:
    """AML检测命令行界面"""
    
    def __init__(self):
        self.rule_extractor = RuleExtractor()
        self.rule_engine = RuleEngine()
        
    def load_rules(self, jurisdiction: str = "all") -> None:
        """加载规则"""
        print(f"加载 {jurisdiction} 规则...")
        
        if jurisdiction in ["all", "singapore", "sg"]:
            sg_rules = self.rule_extractor.extract_singapore_rules()
            self._add_rules_to_engine(sg_rules)
            print(f"  新加坡规则: {len(sg_rules)} 条")
            
        # 这里可以添加香港和迪拜规则
        # if jurisdiction in ["all", "hongkong", "hk"]:
        #     hk_rules = self.rule_extractor.extract_hongkong_rules()
        #     self._add_rules_to_engine(hk_rules)
            
        # if jurisdiction in ["all", "dubai", "uae"]:
        #     dubai_rules = self.rule_extractor.extract_dubai_rules()
        #     self._add_rules_to_engine(dubai_rules)
            
    def _add_rules_to_engine(self, rules_data):
        """添加规则到引擎"""
        # 简化方法：直接创建规则对象
        for rule_data in rules_data:
            # 使用rule_engine的Rule类
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
            self.rule_engine.rules.append(rule)
            
    def fetch_address_data(self, chain: str, address: str) -> dict:
        """获取地址的交易图谱数据"""
        print(f"获取 {address} 在 {chain} 链上的数据...")
        
        try:
            result = fetch_full_graph(chain, address)
            return result
        except Exception as e:
            print(f"API调用失败: {e}")
            return None
            
    def analyze_address(self, chain: str, address: str, jurisdiction: str = "singapore") -> dict:
        """分析地址的AML风险"""
        print(f"\n=== AML风险分析 ===")
        print(f"地址: {address}")
        print(f"链: {chain}")
        print(f"司法管辖区: {jurisdiction}")
        print("=" * 30)
        
        # 1. 加载规则
        self.load_rules(jurisdiction)
        
        # 2. 获取数据
        graph_data = self.fetch_address_data(chain, address)
        if not graph_data:
            return {"error": "无法获取地址数据"}
            
        # 3. 应用规则
        print("应用规则分析...")
        violations = self.rule_engine.apply_rules_to_graph(graph_data)
        
        # 4. 生成报告
        report = {
            "address": address,
            "chain": chain,
            "jurisdiction": jurisdiction,
            "summary": self.rule_engine.get_violations_summary(),
            "violations": [v.to_dict() for v in violations],
            "graph_data_summary": self._summarize_graph_data(graph_data)
        }
        
        return report
        
    def _summarize_graph_data(self, graph_data: dict) -> dict:
        """汇总图谱数据"""
        if not graph_data or 'data' not in graph_data:
            return {}
            
        data = graph_data['data']
        tags = data.get('tags', [])
        paths = data.get('paths', [])
        
        # 统计风险等级
        risk_counts = {"high": 0, "medium": 0, "low": 0, "unknown": 0}
        for tag in tags:
            risk = tag.get('risk_level', 'unknown')
            if risk in risk_counts:
                risk_counts[risk] += 1
                
        return {
            "total_tags": len(tags),
            "total_paths": len(paths),
            "risk_distribution": risk_counts
        }
        
    def print_report(self, report: dict):
        """打印分析报告"""
        print(f"\n{'='*50}")
        print(f"AML合规分析报告")
        print(f"{'='*50}")
        
        if 'error' in report:
            print(f"错误: {report['error']}")
            return
            
        print(f"分析地址: {report['address']}")
        print(f"区块链: {report['chain']}")
        print(f"适用法规: {report['jurisdiction']}")
        
        summary = report.get('summary', {})
        print(f"\n违规摘要:")
        print(f"  总计违规: {summary.get('total_violations', 0)}")
        
        severity_counts = summary.get('severity_counts', {})
        for severity, count in severity_counts.items():
            if count > 0:
                print(f"  {severity.upper()}: {count}")
                
        graph_summary = report.get('graph_data_summary', {})
        print(f"\n图谱数据:")
        print(f"  标签数量: {graph_summary.get('total_tags', 0)}")
        print(f"  路径数量: {graph_summary.get('total_paths', 0)}")
        
        risk_dist = graph_summary.get('risk_distribution', {})
        if risk_dist:
            print(f"  风险分布: {risk_dist}")
            
        # 显示前5个违规
        violations = report.get('violations', [])
        if violations:
            print(f"\n违规详情 (前{min(5, len(violations))}条):")
            for i, violation in enumerate(violations[:5]):
                print(f"\n{i+1}. [{violation.get('severity', 'unknown').upper()}]")
                print(f"   规则: {violation.get('description', 'N/A')}")
                print(f"   建议: {violation.get('recommendation', 'N/A')}")
                
        if len(violations) > 5:
            print(f"\n... 还有 {len(violations) - 5} 条违规未显示")
            
        print(f"\n{'='*50}")
        print("分析完成")
        print(f"{'='*50}")
        
    def interactive_mode(self):
        """交互模式"""
        print("AML规则引擎演示 - 交互模式")
        print("=" * 30)
        
        while True:
            print("\n选项:")
            print("1. 分析新地址")
            print("2. 退出")
            
            choice = input("请选择 (1-2): ").strip()
            
            if choice == "2":
                print("再见!")
                break
                
            if choice == "1":
                chain = input("输入链名 (如 Tron, Ethereum): ").strip()
                address = input("输入地址: ").strip()
                jurisdiction = input("司法管辖区 (singapore/hongkong/dubai, 默认 singapore): ").strip()
                
                if not jurisdiction:
                    jurisdiction = "singapore"
                    
                if not chain or not address:
                    print("链名和地址不能为空")
                    continue
                    
                try:
                    report = self.analyze_address(chain, address, jurisdiction)
                    self.print_report(report)
                    
                    # 询问是否保存报告
                    save = input("\n是否保存报告到文件? (y/n): ").strip().lower()
                    if save == 'y':
                        filename = f"aml_report_{address[:10]}.json"
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(report, f, indent=2, ensure_ascii=False)
                        print(f"报告已保存到: {filename}")
                        
                except Exception as e:
                    print(f"分析过程中出错: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("无效选择")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AML规则引擎演示")
    parser.add_argument("--chain", help="区块链名称 (如 Tron, Ethereum)")
    parser.add_argument("--address", help="钱包地址")
    parser.add_argument("--jurisdiction", default="singapore", 
                       help="司法管辖区 (singapore/hongkong/dubai)")
    parser.add_argument("--interactive", action="store_true",
                       help="进入交互模式")
    
    args = parser.parse_args()
    
    cli = AMLCheckerCLI()
    
    if args.interactive:
        cli.interactive_mode()
    elif args.chain and args.address:
        report = cli.analyze_address(args.chain, args.address, args.jurisdiction)
        cli.print_report(report)
        
        # 自动保存报告
        filename = f"aml_report_{args.address[:10]}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n报告已保存到: {filename}")
    else:
        parser.print_help()
        print("\n示例:")
        print("  python demo_cli.py --chain Tron --address THaUdoNaeL7FEHFGpzEktHiJPsDctc6C6o")
        print("  python demo_cli.py --interactive")

if __name__ == "__main__":
    main()