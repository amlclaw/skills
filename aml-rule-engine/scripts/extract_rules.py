#!/usr/bin/env python3
"""
规则提取器 - 从法规Markdown文件中提取结构化规则
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any

class RuleExtractor:
    """从Markdown法规文件中提取规则"""
    
    def __init__(self, references_dir: str = None):
        if references_dir:
            self.references_dir = Path(references_dir)
        else:
            # 默认: 相对于脚本的../references目录
            self.references_dir = Path(__file__).parent.parent / "references"
        self.rules = []
        
    def extract_singapore_rules(self) -> List[Dict[str, Any]]:
        """提取新加坡(MAS)法规规则"""
        sg_dir = self.references_dir / "singapore"
        if not sg_dir.exists():
            print(f"新加坡法规目录不存在: {sg_dir}")
            return []
            
        # 优先读取摘要文件
        summary_file = sg_dir / "SG-Regulatory-Summary.md"
        if not summary_file.exists():
            print(f"新加坡法规摘要文件不存在: {summary_file}")
            return []
            
        print(f"解析新加坡法规文件: {summary_file}")
        rules = []
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取CDD阈值
        cdd_rules = self._extract_cdd_rules(content)
        rules.extend(cdd_rules)
        
        # 提取Travel Rule阈值
        travel_rules = self._extract_travel_rules(content)
        rules.extend(travel_rules)
        
        # 提取制裁规则
        sanction_rules = self._extract_sanction_rules(content)
        rules.extend(sanction_rules)
        
        # 提取Red Flag规则
        redflag_rules = self._extract_redflag_rules(content)
        rules.extend(redflag_rules)
        
        # 提取STR规则
        str_rules = self._extract_str_rules(content)
        rules.extend(str_rules)
        
        return rules
        
    def extract_hongkong_rules(self) -> List[Dict[str, Any]]:
        """提取香港(SFC)法规规则"""
        hk_dir = self.references_dir / "hongkong"
        if not hk_dir.exists():
            print(f"香港法规目录不存在: {hk_dir}")
            return []
            
        rules = []
        
        # 处理主要法规文件
        main_files = [
            "HK-001-AMLO-Cap-615.md",
            "HK-004-SFC-AML-CFT-Guideline.md",
            "HK-006-SFC-VATP-Guidelines-2023.md",
            "HK-007-HKMA-Stablecoin-AML-Guideline-2025.md"
        ]
        
        for filename in main_files:
            file_path = hk_dir / filename
            if file_path.exists():
                print(f"解析香港法规文件: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取资本要求规则
                capital_rules = self._extract_hk_capital_rules(content, filename)
                rules.extend(capital_rules)
                
                # 提取监管要求规则
                regulatory_rules = self._extract_hk_regulatory_rules(content, filename)
                rules.extend(regulatory_rules)
                
                # 提取合规要求规则
                compliance_rules = self._extract_hk_compliance_rules(content, filename)
                rules.extend(compliance_rules)
        
        # 分配唯一ID
        for i, rule in enumerate(rules):
            rule['rule_id'] = f"HK-{i+1:03d}"
            
        return rules
        
    def _extract_hk_capital_rules(self, content: str, source_file: str) -> List[Dict[str, Any]]:
        """提取香港资本要求规则"""
        rules = []
        
        # 资本要求模式
        capital_patterns = [
            (r'Minimum Paid-up Capital.*?\|\s*(HK\$?\s*[\d,]+\.?\d*)\s*\|', 'CAPITAL_REQUIREMENT'),
            (r'Minimum Liquid Capital.*?\|\s*(HK\$?\s*[\d,]+\.?\d*)\s*\|', 'LIQUID_CAPITAL_REQUIREMENT'),
            (r'最低实缴资本.*?\|\s*(HK\$?\s*[\d,]+\.?\d*)\s*\|', 'CAPITAL_REQUIREMENT'),
            (r'最低流动资本.*?\|\s*(HK\$?\s*[\d,]+\.?\d*)\s*\|', 'LIQUID_CAPITAL_REQUIREMENT'),
        ]
        
        for pattern, rule_type in capital_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                amount_str = match.group(1).replace('HK$', '').replace('$', '').replace(',', '').strip()
                try:
                    amount = float(amount_str)
                    rules.append({
                        "jurisdiction": "Hong Kong",
                        "category": "Capital Requirements",
                        "rule_type": rule_type,
                        "description": f"{rule_type.replace('_', ' ').title()}: HK${amount:,.0f}",
                        "threshold": amount,
                        "currency": "HKD",
                        "source": f"{source_file}",
                        "user_customizable": False,  # 资本要求通常不可自定义
                        "enabled": True
                    })
                except ValueError:
                    continue
                    
        return rules
        
    def _extract_hk_regulatory_rules(self, content: str, source_file: str) -> List[Dict[str, Any]]:
        """提取香港监管要求规则"""
        rules = []
        
        # Fit and Proper测试要求
        if "Fit and Proper Test" in content:
            rules.append({
                "jurisdiction": "Hong Kong",
                "category": "Personnel Requirements",
                "rule_type": "FIT_AND_PROPER_TEST",
                "description": "Must pass SFC Fit and Proper Test for officers",
                "action": "Evaluate financial status, education, experience, character, reputation",
                "source": f"{source_file}#Fit_and_Proper",
                "user_customizable": False,
                "enabled": True
            })
            
        # 居住要求
        if "ordinarily reside in Hong Kong" in content:
            rules.append({
                "jurisdiction": "Hong Kong",
                "category": "Personnel Requirements",
                "rule_type": "RESIDENCY_REQUIREMENT",
                "description": "At least one responsible officer must ordinarily reside in Hong Kong",
                "action": "Ensure resident officer meets qualifications",
                "source": f"{source_file}#Residency",
                "user_customizable": False,
                "enabled": True
            })
            
        # VASP许可证要求
        if "VASP licensing" in content or "VASP license" in content:
            rules.append({
                "jurisdiction": "Hong Kong",
                "category": "Licensing Requirements",
                "rule_type": "VASP_LICENSE_REQUIRED",
                "description": "VASP license required for virtual asset service providers",
                "action": "Apply for SFC license, meet all requirements",
                "source": f"{source_file}#Licensing",
                "user_customizable": False,
                "enabled": True
            })
            
        return rules
        
    def _extract_hk_compliance_rules(self, content: str, source_file: str) -> List[Dict[str, Any]]:
        """提取香港合规要求规则"""
        rules = []
        
        # AML/CFT程序要求
        if "AML/CFT" in content and ("program" in content or "procedures" in content):
            rules.append({
                "jurisdiction": "Hong Kong",
                "category": "Compliance Framework",
                "rule_type": "AML_CFT_PROGRAM_REQUIRED",
                "description": "Must establish AML/CFT policies, procedures and controls",
                "action": "Design and implement comprehensive AML/CFT program",
                "source": f"{source_file}#Compliance",
                "user_customizable": True,  # 具体实施可自定义
                "enabled": True
            })
            
        # 风险评估要求
        if "risk assessment" in content.lower():
            rules.append({
                "jurisdiction": "Hong Kong",
                "category": "Risk Management",
                "rule_type": "RISK_ASSESSMENT_REQUIRED",
                "description": "Must conduct ML/TF risk assessment",
                "action": "Assess risks based on customers, products, services, jurisdictions",
                "source": f"{source_file}#Risk_Assessment",
                "user_customizable": True,
                "enabled": True
            })
            
        # 客户尽职调查
        if "customer due diligence" in content.lower() or "CDD" in content:
            rules.append({
                "jurisdiction": "Hong Kong",
                "category": "Customer Due Diligence",
                "rule_type": "CDD_REQUIRED",
                "description": "Customer Due Diligence must be performed",
                "action": "Establish CDD procedures for customer verification",
                "source": f"{source_file}#CDD",
                "user_customizable": True,
                "enabled": True
            })
            
        return rules
    
    def _extract_cdd_rules(self, content: str) -> List[Dict[str, Any]]:
        """提取CDD相关规则"""
        rules = []
        
        # 查找CDD阈值
        cdd_patterns = [
            (r'超过\s*(\**S?\$?\s*[\d,]+\.?\d*\**)\s*', 'CDD_THRESHOLD'),
            (r'exceeding\s*(\**S?\$?\s*[\d,]+\.?\d*\**)\s*', 'CDD_THRESHOLD'),
            (r'大于\s*(\**S?\$?\s*[\d,]+\.?\d*\**)\s*', 'CDD_THRESHOLD'),
        ]
        
        for pattern, rule_type in cdd_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                amount_str = match.group(1).replace('*', '').replace('S$', '').replace('$', '').replace(',', '').strip()
                try:
                    amount = float(amount_str)
                    rules.append({
                        "rule_id": f"SG-CDD-{len(rules)+1:03d}",
                        "jurisdiction": "Singapore",
                        "category": "Customer Due Diligence",
                        "rule_type": rule_type,
                        "description": f"CDD required for transactions > S${amount:,.0f}",
                        "threshold": amount,
                        "currency": "SGD",
                        "source": "SG-Regulatory-Summary.md#1.1",
                        "user_customizable": True,
                        "enabled": True
                    })
                except ValueError:
                    continue
        
        # 查找特定CDD阈值 (S$5,000)
        if "S$5,000" in content or "S$5,000" in content:
            rules.append({
                "rule_id": "SG-CDD-001",
                "jurisdiction": "Singapore",
                "category": "Customer Due Diligence",
                "rule_type": "CDD_THRESHOLD",
                "description": "CDD required for transactions > S$5,000",
                "threshold": 5000,
                "currency": "SGD",
                "source": "SG-Regulatory-Summary.md#1.1",
                "user_customizable": True,
                "enabled": True
            })
            
        # EDD规则
        edd_keywords = [
            "Politically Exposed Persons",
            "High Risk Jurisdictions", 
            "Anonymity",
            "Complex Transactions",
            "Enhanced Due Diligence"
        ]
        
        for keyword in edd_keywords:
            if keyword in content:
                rules.append({
                    "rule_id": f"SG-EDD-{len(rules)+1:03d}",
                    "jurisdiction": "Singapore",
                    "category": "Enhanced Due Diligence",
                    "rule_type": "EDD_REQUIRED",
                    "description": f"EDD required for {keyword}",
                    "condition": keyword,
                    "source": "SG-Regulatory-Summary.md#1.2",
                    "user_customizable": True,
                    "enabled": True
                })
                
        return rules
    
    def _extract_travel_rules(self, content: str) -> List[Dict[str, Any]]:
        """提取Travel Rule相关规则"""
        rules = []
        
        # Travel Rule阈值 (S$1,500)
        travel_patterns = [
            (r'旅行规则.*?(\**S?\$?\s*[\d,]+\.?\d*\**)'),
            (r'Travel Rule.*?(\**S?\$?\s*[\d,]+\.?\d*\**)'),
            (r'Value Transfers.*?(\**S?\$?\s*[\d,]+\.?\d*\**)'),
        ]
        
        for pattern in travel_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                amount_str = match.group(1).replace('*', '').replace('S$', '').replace('$', '').replace(',', '').strip()
                try:
                    amount = float(amount_str)
                    rules.append({
                        "rule_id": f"SG-TRAVEL-{len(rules)+1:03d}",
                        "jurisdiction": "Singapore",
                        "category": "Travel Rule",
                        "rule_type": "TRAVEL_RULE_THRESHOLD",
                        "description": f"Travel Rule applies for value transfers > S${amount:,.0f}",
                        "threshold": amount,
                        "currency": "SGD",
                        "source": "SG-Regulatory-Summary.md#2.1",
                        "user_customizable": True,
                        "enabled": True
                    })
                except ValueError:
                    continue
        
        # 具体阈值 S$1,500
        if "S$1,500" in content or "S$1,500" in content:
            rules.append({
                "rule_id": "SG-TRAVEL-001",
                "jurisdiction": "Singapore",
                "category": "Travel Rule",
                "rule_type": "TRAVEL_RULE_THRESHOLD",
                "description": "Travel Rule applies for value transfers > S$1,500",
                "threshold": 1500,
                "currency": "SGD",
                "source": "SG-Regulatory-Summary.md#2.1",
                "user_customizable": True,
                "enabled": True
            })
            
        # IVMS101信息要求
        ivms_keywords = [
            "Name",
            "Account Number",
            "Address",
            "National ID",
            "Date & Place of Birth"
        ]
        
        for keyword in ivms_keywords:
            if keyword in content:
                rules.append({
                    "rule_id": f"SG-IVMS-{len(rules)+1:03d}",
                    "jurisdiction": "Singapore",
                    "category": "Travel Rule",
                    "rule_type": "IVMS101_REQUIRED",
                    "description": f"IVMS101 requires {keyword} information",
                    "requirement": keyword,
                    "source": "SG-Regulatory-Summary.md#2.2",
                    "user_customizable": True,
                    "enabled": True
                })
                
        return rules
    
    def _extract_sanction_rules(self, content: str) -> List[Dict[str, Any]]:
        """提取制裁筛查规则"""
        rules = []
        
        sanction_keywords = [
            "UN Security Council Consolidated List",
            "Singapore Designated Individuals and Entities",
            "Sanctions",
            "Prohibitions",
            "FREEZE",
            "PROHIBIT",
            "REPORT"
        ]
        
        for keyword in sanction_keywords:
            if keyword in content:
                rules.append({
                    "rule_id": f"SG-SANCTION-{len(rules)+1:03d}",
                    "jurisdiction": "Singapore",
                    "category": "Sanctions Screening",
                    "rule_type": "SANCTIONS_CHECK",
                    "description": f"Must screen against {keyword}",
                    "screening_list": keyword,
                    "action": "FREEZE, PROHIBIT, REPORT if match",
                    "source": "SG-Regulatory-Summary.md#3",
                    "user_customizable": True,
                    "enabled": True
                })
                
        return rules
    
    def _extract_redflag_rules(self, content: str) -> List[Dict[str, Any]]:
        """提取Red Flag指标规则"""
        rules = []
        
        redflag_patterns = [
            (r'Mixers/Tumblers', "MIXER_USAGE"),
            (r'Privacy Coins', "PRIVACY_COIN_USAGE"),
            (r'Darknet', "DARKNET_EXPOSURE"),
            (r'Unhosted Wallets', "UNHOSTED_WALLET"),
            (r'Structuring.*?Smurfing', "STRUCTURING"),
            (r'Rapid Movement', "RAPID_MOVEMENT"),
            (r'Looping', "LOOPING"),
            (r'Inconsistent Volume', "INCONSISTENT_VOLUME"),
        ]
        
        for pattern, rule_type in redflag_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                rules.append({
                    "rule_id": f"SG-REDFLAG-{len(rules)+1:03d}",
                    "jurisdiction": "Singapore",
                    "category": "Red Flag Indicators",
                    "rule_type": rule_type,
                    "description": f"Red Flag: {pattern}",
                    "risk_level": "high",
                    "source": "SG-Regulatory-Summary.md#5",
                    "user_customizable": True,
                    "enabled": True
                })
                
        return rules
    
    def _extract_str_rules(self, content: str) -> List[Dict[str, Any]]:
        """提取可疑交易报告规则"""
        rules = []
        
        str_keywords = [
            "Suspicious Transaction Reporting",
            "STR",
            "STRO",
            "SONAR",
            "No Tipping Off"
        ]
        
        for keyword in str_keywords:
            if keyword in content:
                rules.append({
                    "rule_id": f"SG-STR-{len(rules)+1:03d}",
                    "jurisdiction": "Singapore",
                    "category": "Suspicious Transaction Reporting",
                    "rule_type": "STR_REQUIRED",
                    "description": f"STR requirement: {keyword}",
                    "action": "File with STRO via SONAR",
                    "timeline": "As soon as reasonably practicable",
                    "source": "SG-Regulatory-Summary.md#4",
                    "user_customizable": True,
                    "enabled": True
                })
                
        return rules
    
    def save_rules_to_file(self, rules: List[Dict[str, Any]], output_file: str = "singapore_rules.json"):
        """保存规则到JSON文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        print(f"规则已保存到: {output_file} ({len(rules)} 条规则)")
        
    def print_rules_summary(self, rules: List[Dict[str, Any]]):
        """打印规则摘要"""
        print(f"\n=== 规则提取结果 ===")
        print(f"总计提取: {len(rules)} 条规则")
        
        categories = {}
        for rule in rules:
            category = rule.get('category', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
            
        for category, count in categories.items():
            print(f"  {category}: {count} 条")
            
        print("\n=== 规则示例 ===")
        for i, rule in enumerate(rules[:5]):
            print(f"{i+1}. [{rule['rule_id']}] {rule['description']}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="从法规文件提取结构化规则")
    parser.add_argument("--jurisdiction", choices=["all", "singapore", "hongkong"], 
                       default="all", help="司法管辖区 (默认: all)")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    extractor = RuleExtractor()
    
    all_rules = []
    
    if args.jurisdiction in ["all", "singapore"]:
        print("开始提取新加坡法规规则...")
        sg_rules = extractor.extract_singapore_rules()
        extractor.print_rules_summary(sg_rules)
        all_rules.extend(sg_rules)
        
    if args.jurisdiction in ["all", "hongkong"]:
        print("\n开始提取香港法规规则...")
        hk_rules = extractor.extract_hongkong_rules()
        extractor.print_rules_summary(hk_rules)
        all_rules.extend(hk_rules)
    
    # 保存规则
    if args.output:
        output_file = args.output
    elif args.jurisdiction == "all":
        output_file = "all_rules.json"
    elif args.jurisdiction == "singapore":
        output_file = "singapore_rules.json"
    else:
        output_file = "hongkong_rules.json"
        
    extractor.save_rules_to_file(all_rules, output_file)
    
    # 输出汇总信息
    if all_rules:
        print(f"\n=== 规则提取完成 ===")
        print(f"总计提取: {len(all_rules)} 条规则")
        
        jurisdictions = {}
        for rule in all_rules:
            jurisdiction = rule.get('jurisdiction', 'Unknown')
            jurisdictions[jurisdiction] = jurisdictions.get(jurisdiction, 0) + 1
            
        for jurisdiction, count in jurisdictions.items():
            print(f"  {jurisdiction}: {count} 条")
            
        # 输出前3条规则详情
        print("\n=== 前3条规则详情 ===")
        for i, rule in enumerate(all_rules[:3]):
            print(f"\n规则 #{i+1}:")
            for key, value in rule.items():
                print(f"  {key}: {value}")
    else:
        print("未提取到任何规则")

if __name__ == "__main__":
    main()