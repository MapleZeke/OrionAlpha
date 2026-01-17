#!/usr/bin/env python3
"""
Feature Matrix Generator for OrionAlpha
Generates comprehensive feature completion reports
"""

import json
from pathlib import Path

class FeatureMatrix:
    def __init__(self):
        self.wz_inventory = None
        self.script_analysis = None
        self.quest_gaps = None
    
    def load_all_data(self):
        """Load all analysis data"""
        with open("analysis/reports/wz_inventory.json", 'r') as f:
            self.wz_inventory = json.load(f)
        
        with open("analysis/reports/script_analysis.json", 'r') as f:
            self.script_analysis = json.load(f)
        
        with open("analysis/reports/quest_gaps.json", 'r') as f:
            self.quest_gaps = json.load(f)
    
    def generate_markdown_report(self):
        """Generate comprehensive markdown report"""
        report = []
        
        # Header
        report.append("# OrionAlpha Feature Completeness Report\n")
        report.append(f"*Generated automatically by feature analysis toolkit*\n\n")
        
        # WZ Content Summary
        report.append("## 📦 WZ Content Inventory\n")
        summary = self.wz_inventory["summary"]
        report.append(f"- **NPCs**: {summary['total_npcs']}")
        report.append(f"- **Items**: {summary['total_items']}")
        report.append(f"- **Mobs**: {summary['total_mobs']}")
        report.append(f"- **Maps**: {summary['total_maps']}")
        report.append(f"- **Skills**: {summary['total_skills']}")
        report.append(f"- **Quests (WZ)**: {summary['total_quests']}\n")
        
        # Script Analysis
        report.append("## 🎭 NPC Script Status\n")
        stats = self.script_analysis["stats"]
        total = stats["total"]
        report.append(f"- **Total Scripts**: {total}")
        report.append(f"- ✅ **Complete**: {stats['complete']} ({stats['complete']/total*100:.1f}%)")
        report.append(f"- 🚧 **Partial (has TODOs)**: {stats['partial']} ({stats['partial']/total*100:.1f}%)")
        report.append(f"- ❌ **Stubbed**: {stats['stubbed']} ({stats['stubbed']/total*100:.1f}%)")
        report.append(f"- 📋 **Quest-related**: {stats['quest_related']}\n")
        
        # Quest System Analysis
        report.append("## 📋 Quest System Status\n")
        report.append(f"- **WZ Quests Defined**: {self.quest_gaps['total_wz_quests']}")
        report.append(f"- **Quest Scripts Written**: {self.quest_gaps['total_quest_scripts']}")
        report.append(f"- **Implementation Gap**: {self.quest_gaps['total_wz_quests'] - self.quest_gaps['total_quest_scripts']}\n")
        
        # Stubbed Scripts List
        report.append("## ❌ Stubbed Scripts (Need Implementation)\n")
        for script_name, script_data in self.script_analysis["scripts"].items():
            if script_data["status"] == "stubbed":
                npc = script_data["npc"]
                report.append(f"- `{script_name}.py` - {npc}")
        report.append("\n")
        
        # Partial Scripts with TODOs
        report.append("## 🚧 Partial Scripts (Have TODOs)\n")
        for script_name, script_data in self.script_analysis["scripts"].items():
            if script_data["status"] == "partial":
                npc = script_data["npc"]
                report.append(f"\n### {script_name}.py - {npc}")
                for todo in script_data["todos"]:
                    report.append(f"  - TODO: {todo}")
        report.append("\n")
        
        # Development Roadmap
        report.append("## 🗺️ Development Roadmap\n")
        report.append("### Priority 1: Quest System Backend")
        report.append("- Implement quest state tracking")
        report.append("- Add quest completion handlers")
        report.append("- Create quest reward system")
        report.append(f"- Complete {stats['quest_related']} quest-related scripts\n")
        
        report.append("### Priority 2: Job Advancement System")
        report.append("- Complete Magician job instructor")
        report.append("- Complete Bowman job instructor")
        report.append("- Implement 2nd job advancements\n")
        
        report.append("### Priority 3: NPC Script Completion")
        report.append(f"- Complete {stats['stubbed']} stubbed scripts")
        report.append(f"- Finish {stats['partial']} partial scripts\n")
        
        return "\n".join(report)
    
    def save_report(self, output_file="analysis/reports/FEATURE_REPORT.md"):
        """Save markdown report"""
        report = self.generate_markdown_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Feature report saved to {output_file}")
        
        return report

if __name__ == "__main__":
    matrix = FeatureMatrix()
    matrix.load_all_data()
    matrix.save_report()
