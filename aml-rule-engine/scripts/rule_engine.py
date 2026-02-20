#!/usr/bin/env python3
"""
规则引擎 - 将交易图谱数据与法规规则进行匹配
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class RuleType(Enum):
    """规则类型枚举"""
    CDD_THRESHOLD = "CDD_THRESHOLD"  # CDD阈值
    TRAVEL_RULE_THRESHOLD = "TRAVEL_RULE_THRESHOLD"  # Travel Rule阈值
    SANCTIONS_CHECK = "SANCTIONS_CHECK"  # 制裁筛查
    RED_FLAG = "RED_FLAG"  # Red Flag指标
    STR_REQUIRED = "STR_REQUIRED"  # 可疑交易报告
    EDD_REQUIRED = "EDD_REQUIRED"  # 增强尽职调查

class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Rule:
    """规则数据结构"""
    rule_id: str
    jurisdiction: str
    category: str
    rule_type: str
    description: str
    threshold: Optional[float] = None
    currency: Optional[str] = None
    condition: Optional[str] = None
    screening_list: Optional[str] = None
    action: Optional[str] = None
    risk_level: Optional[str] = None
    source: Optional[str] = None
    user_customizable: bool = True
    enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

@dataclass  
class Violation:
    """违规记录"""
    rule_id: str
    description: str
    severity: RiskLevel
    evidence: Dict[str, Any]
    recommendation: str
    rule_source: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "rule_id": self.rule_id,
            "description": self.description,
            "severity": self.severity.value,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "rule_source": self.rule_source
        }

class RuleEngine:
    """规则引擎核心类"""
    
    def __init__(self):
        self.rules: List[Rule] = []
        self.violations: List[Violation] = []
        
    def load_rules_from_file(self, file_path: str) -> None:
        """从JSON文件加载规则"""
        with open(file_path, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
            
        for rule_data in rules_data:
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
            self.rules.append(rule)
            
        print(f"已加载 {len(self.rules)} 条规则")
        
    def apply_rules_to_graph(self, graph_data: Dict[str, Any]) -> List[Violation]:
        """
        将规则应用于交易图谱数据
        
        Args:
            graph_data: graph_api.py返回的交易图谱数据
            
        Returns:
            违规记录列表
        """
        self.violations = []
        
        if not graph_data or 'code' not in graph_data or graph_data['code'] != 0:
            print("无效的图谱数据")
            return []
            
        data = graph_data.get('data', {})
        tags = data.get('tags', [])
        paths = data.get('paths', [])
        
        print(f"分析图谱数据: {len(tags)} 个标签, {len(paths)} 条路径")
        
        # 应用所有启用规则
        for rule in self.rules:
            if not rule.enabled:
                continue
                
            violations = self._apply_single_rule(rule, tags, paths)
            self.violations.extend(violations)
            
        return self.violations
    
    def _apply_single_rule(self, rule: Rule, tags: List[Dict], paths: List[Dict]) -> List[Violation]:
        """应用单个规则"""
        violations = []
        
        # 根据规则类型应用不同的检测逻辑
        if rule.rule_type == "SANCTIONS_CHECK":
            violations.extend(self._check_sanctions(rule, tags))
        elif rule.rule_type == "RED_FLAG":
            violations.extend(self._check_red_flags(rule, tags, paths))
        elif rule.rule_type == "CDD_THRESHOLD":
            violations.extend(self._check_cdd_threshold(rule, paths))
        elif rule.rule_type == "TRAVEL_RULE_THRESHOLD":
            violations.extend(self._check_travel_rule(rule, paths))
        # 其他规则类型...
            
        return violations
    
    def _check_sanctions(self, rule: Rule, tags: List[Dict]) -> List[Violation]:
        """检查制裁规则"""
        violations = []
        
        for tag in tags:
            if tag.get('primary_category') == 'Sanctions':
                violation = Violation(
                    rule_id=rule.rule_id,
                    description=f"地址涉及制裁实体: {tag.get('address')}",
                    severity=RiskLevel.CRITICAL,
                    evidence={
                        "address": tag.get('address'),
                        "risk_level": tag.get('risk_level'),
                        "category": tag.get('primary_category'),
                        "secondary_category": tag.get('secondary_category')
                    },
                    recommendation="立即冻结资金并报告相关监管机构",
                    rule_source=rule.source
                )
                violations.append(violation)
                
        return violations
    
    def _check_red_flags(self, rule: Rule, tags: List[Dict], paths: List[Dict]) -> List[Violation]:
        """检查Red Flag规则"""
        violations = []
        
        # 检查高风险标签
        high_risk_categories = ['Cybercrime', 'Darknet', 'Gambling', 'Mixer']
        
        for tag in tags:
            primary_category = tag.get('primary_category', '')
            risk_level = tag.get('risk_level', 'low')
            
            if risk_level == 'high' or any(cat in primary_category for cat in high_risk_categories):
                violation = Violation(
                    rule_id=rule.rule_id,
                    description=f"高风险地址: {tag.get('address')} ({primary_category})",
                    severity=RiskLevel.HIGH,
                    evidence={
                        "address": tag.get('address'),
                        "risk_level": risk_level,
                        "category": primary_category,
                        "rule_matched": rule.condition or rule.description
                    },
                    recommendation="执行增强尽职调查(EDD)并考虑上报STR",
                    rule_source=rule.source
                )
                violations.append(violation)
                
        return violations
    
    def _check_cdd_threshold(self, rule: Rule, paths: List[Dict]) -> List[Violation]:
        """检查CDD阈值规则"""
        violations = []
        
        if not rule.threshold:
            return violations
            
        # 分析交易金额
        for path in paths:
            path_nodes = path.get('path', [])
            for node in path_nodes:
                amount = node.get('amount', 0)
                if amount > rule.threshold:
                    violation = Violation(
                        rule_id=rule.rule_id,
                        description=f"交易金额 {amount} USDT 超过CDD阈值 {rule.threshold} {rule.currency}",
                        severity=RiskLevel.MEDIUM,
                        evidence={
                            "address": node.get('address'),
                            "amount": amount,
                            "threshold": rule.threshold,
                            "currency": rule.currency
                        },
                        recommendation="执行客户尽职调查(CDD)并记录",
                        rule_source=rule.source
                    )
                    violations.append(violation)
                    
        return violations
    
    def _check_travel_rule(self, rule: Rule, paths: List[Dict]) -> List[Violation]:
        """检查Travel Rule阈值规则"""
        violations = []
        
        if not rule.threshold:
            return violations
            
        # Travel Rule通常适用于大额转账
        for path in paths:
            path_nodes = path.get('path', [])
            total_amount = sum(node.get('amount', 0) for node in path_nodes)
            
            if total_amount > rule.threshold:
                violation = Violation(
                    rule_id=rule.rule_id,
                    description=f"转账总金额 {total_amount} USDT 超过Travel Rule阈值 {rule.threshold} {rule.currency}",
                    severity=RiskLevel.MEDIUM,
                    evidence={
                        "total_amount": total_amount,
                        "threshold": rule.threshold,
                        "currency": rule.currency,
                        "path_count": len(path_nodes)
                    },
                    recommendation="应用Travel Rule要求，收集并验证交易双方信息",
                    rule_source=rule.source
                )
                violations.append(violation)
                
        return violations
    
    def get_violations_summary(self) -> Dict[str, Any]:
        """获取违规摘要"""
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for violation in self.violations:
            severity = violation.severity.value
            if severity in severity_counts:
                severity_counts[severity] += 1
                
        return {
            "total_violations": len(self.violations),
            "severity_counts": severity_counts,
            "categories": self._get_violations_by_category()
        }
    
    def _get_violations_by_category(self) -> Dict[str, int]:
        """按规则类别统计违规"""
        category_counts = {}
        
        for violation in self.violations:
            # 从规则ID推断类别
            rule_id = violation.rule_id
            if '-' in rule_id:
                category = rule_id.split('-')[1]  # 如 SG-CDD-001 -> CDD
                category_counts[category] = category_counts.get(category, 0) + 1
                
        return category_counts
    
    def generate_report(self, output_file: str = "compliance_report.json") -> None:
        """生成合规报告"""
        report = {
            "summary": self.get_violations_summary(),
            "violations": [v.to_dict() for v in self.violations],
            "rules_applied": len([r for r in self.rules if r.enabled]),
            "timestamp": self._get_current_timestamp()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"合规报告已生成: {output_file}")
        
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

def test_rule_engine():
    """测试规则引擎"""
    print("=== 测试规则引擎 ===")
    
    # 1. 加载规则
    engine = RuleEngine()
    engine.load_rules_from_file("singapore_rules.json")
    
    # 2. 加载测试图谱数据
    test_graph_file = "output.json"  # 使用现有的测试数据
    try:
        # output.json包含API响应之前的文本，需要提取JSON部分
        with open(test_graph_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 找到第一个'{'和最后一个'}'
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start == -1 or end == 0:
            print(f"在 {test_graph_file} 中未找到有效的JSON")
            print("请先运行 graph_api.py 生成测试数据")
            return
            
        json_str = content[start:end]
        graph_data = json.loads(json_str)
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"加载测试数据失败: {e}")
        print("请先运行 graph_api.py 生成测试数据")
        return
        
    # 3. 应用规则
    violations = engine.apply_rules_to_graph(graph_data)
    print(f"检测到 {len(violations)} 条违规")
    
    # 4. 生成摘要
    summary = engine.get_violations_summary()
    print(f"\n违规摘要:")
    print(f"  总计: {summary['total_violations']}")
    for severity, count in summary['severity_counts'].items():
        if count > 0:
            print(f"  {severity.upper()}: {count}")
            
    # 5. 显示前几个违规
    if violations:
        print(f"\n前3条违规:")
        for i, violation in enumerate(violations[:3]):
            print(f"\n{i+1}. [{violation.severity.value}] {violation.description}")
            print(f"   建议: {violation.recommendation}")
            
    # 6. 生成报告
    engine.generate_report("test_compliance_report.json")

if __name__ == "__main__":
    test_rule_engine()