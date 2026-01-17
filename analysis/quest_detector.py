#!/usr/bin/env python3
"""
Quest System Detector for OrionAlpha
Compares WZ quest data with script implementations
"""

import json
from pathlib import Path

class QuestDetector:
    def __init__(self):
        self.wz_inventory = None
        self.script_analysis = None
        self.quest_gaps = []
    
    def load_data(self):
        """Load WZ inventory and script analysis"""
        with open("analysis/reports/wz_inventory.json", 'r') as f:
            self.wz_inventory = json.load(f)
        
        with open("analysis/reports/script_analysis.json", 'r') as f:
            self.script_analysis = json.load(f)
    
    def detect_gaps(self):
        """Detect gaps between WZ quests and script implementations"""
        print("🔍 Detecting quest implementation gaps...")
        
        wz_quests = self.wz_inventory["inventory"]["quests"]
        script_quests = {
            name: data for name, data in self.script_analysis["scripts"].items()
            if data["quest_related"]
        }
        
        # Find WZ quests without scripts
        for quest_id, quest_data in wz_quests.items():
            has_script = False
            script_status = "missing"
            
            for script_name, script_data in script_quests.items():
                if quest_id in script_name or (script_data["quest"] and quest_id in script_data["quest"]):
                    has_script = True
                    script_status = script_data["status"]
                    break
            
            self.quest_gaps.append({
                "quest_id": quest_id,
                "quest_data": quest_data,
                "has_script": has_script,
                "script_status": script_status
            })
        
        return self.quest_gaps
    
    def save_report(self, output_file="analysis/reports/quest_gaps.json"):
        """Save quest gap analysis"""
        output = {
            "total_wz_quests": len(self.wz_inventory["inventory"]["quests"]),
            "total_quest_scripts": self.script_analysis["stats"]["quest_related"],
            "gaps": self.quest_gaps
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Quest gap analysis saved to {output_file}")
        print(f"\n📊 Quest System Status:")
        print(f"   WZ Quests defined: {len(self.wz_inventory['inventory']['quests'])}")
        print(f"   Quest scripts: {self.script_analysis['stats']['quest_related']}")
        
        return output

if __name__ == "__main__":
    detector = QuestDetector()
    detector.load_data()
    detector.detect_gaps()
    detector.save_report()
