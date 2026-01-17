#!/usr/bin/env python3
"""
NPC Script Analyzer for OrionAlpha
Analyzes Python scripts to determine completion status
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

class ScriptAnalyzer:
    def __init__(self, script_path="data/Script"):
        self.script_path = Path(script_path)
        self.scripts = {}
        self.stats = {
            "total": 0,
            "complete": 0,
            "partial": 0,
            "stubbed": 0,
            "quest_related": 0
        }
    
    def analyze_all(self):
        """Analyze all Python scripts"""
        print("🔍 Analyzing NPC scripts...")
        
        for py_file in self.script_path.glob("*.py"):
            if py_file.name.startswith("_"):
                continue  # Skip templates
            
            analysis = self.analyze_script(py_file)
            self.scripts[py_file.stem] = analysis
            self.stats["total"] += 1
            
            # Update stats
            if analysis["status"] == "complete":
                self.stats["complete"] += 1
            elif analysis["status"] == "partial":
                self.stats["partial"] += 1
            elif analysis["status"] == "stubbed":
                self.stats["stubbed"] += 1
            
            if analysis["quest_related"]:
                self.stats["quest_related"] += 1
        
        return self.scripts
    
    def analyze_script(self, script_file):
        """Analyze a single script file"""
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            "file": script_file.name,
            "npc": self._extract_npc_name(content),
            "quest": self._extract_quest_name(content),
            "status": "unknown",
            "quest_related": False,
            "todos": [],
            "features": []
        }
        
        # Detect status
        if "Sorry, I am not coded yet" in content:
            analysis["status"] = "stubbed"
        elif "# TODO" in content:
            analysis["status"] = "partial"
            analysis["todos"] = self._extract_todos(content)
        else:
            analysis["status"] = "complete"
        
        # Detect quest-related
        if "quest" in content.lower() or "Quest:" in content:
            analysis["quest_related"] = True
            analysis["quest"] = self._extract_quest_name(content)
        
        # Detect features used
        analysis["features"] = self._detect_features(content)
        
        return analysis
    
    def _extract_npc_name(self, content):
        """Extract NPC name from script"""
        match = re.search(r"'NPC:\s*(.+?)'", content)
        if match:
            return match.group(1)
        match = re.search(r"NPC:\s*(.+)", content)
        if match:
            return match.group(1).strip()
        return "Unknown"
    
    def _extract_quest_name(self, content):
        """Extract quest name from script"""
        match = re.search(r"'Quest:\s*(.+?)'", content)
        if match:
            return match.group(1)
        match = re.search(r"Quest:\s*(.+)", content)
        if match:
            return match.group(1).strip()
        return None
    
    def _extract_todos(self, content):
        """Extract TODO comments"""
        todos = []
        for line in content.split('\n'):
            if '# TODO' in line or '#TODO' in line:
                todo = line.split('TODO')[-1].strip(' :').strip()
                todos.append(todo)
        return todos
    
    def _detect_features(self, content):
        """Detect which features the script uses"""
        features = []
        
        feature_patterns = {
            "dialogue": r"self\.say\(",
            "menu": r"self\.askMenu\(",
            "yes_no": r"self\.askYesNo\(",
            "number": r"self\.askNumber\(",
            "inventory": r"self\.inventoryExchange\(",
            "warp": r"self\.registerTransferField\(",
            "job_change": r"self\.userJob\(",
            "exp_gain": r"self\.userIncEXP\(",
            "quest_check": r"self\.questRecordGet",
            "quest_set": r"self\.questRecordSet",
        }
        
        for feature_name, pattern in feature_patterns.items():
            if re.search(pattern, content):
                features.append(feature_name)
        
        return features
    
    def save_report(self, output_file="analysis/reports/script_analysis.json"):
        """Save analysis to JSON file"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        output = {
            "stats": self.stats,
            "scripts": self.scripts
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Script analysis saved to {output_file}")
        print(f"\n📊 Script Statistics:")
        print(f"   Total scripts: {self.stats['total']}")
        print(f"   ✅ Complete: {self.stats['complete']} ({self.stats['complete']/self.stats['total']*100:.1f}%)")
        print(f"   🚧 Partial: {self.stats['partial']} ({self.stats['partial']/self.stats['total']*100:.1f}%)")
        print(f"   ❌ Stubbed: {self.stats['stubbed']} ({self.stats['stubbed']/self.stats['total']*100:.1f}%)")
        print(f"   📋 Quest-related: {self.stats['quest_related']}")
        
        return output

if __name__ == "__main__":
    analyzer = ScriptAnalyzer()
    analyzer.analyze_all()
    analyzer.save_report()
