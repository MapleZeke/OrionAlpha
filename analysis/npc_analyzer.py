#!/usr/bin/env python3
"""
NPC Categorization Tool for OrionAlpha
Analyzes all NPCs from WZ files and categorizes by type.

Categories:
1. QUEST_ONLY - Has quest script reference, no shop items
2. SHOP_ONLY - Has shop items in WZ, no script needed (auto-works!)
3. QUEST_AND_SHOP - Has both (script must handle shop opening)
4. SCRIPTED_OTHER - Has script but not quest-related (custom dialogue)
5. DECORATION - No quest, no shop, no script (just visual)
6. NEEDS_SCRIPT - Referenced in WZ but script is missing/broken
"""

import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

class NpcAnalyzer:
    def __init__(self, data_path="data"):
        self.data_path = Path(data_path)
        self.npcs = {}
        self.scripts = {}
        self.categories = {
            "QUEST_ONLY": [],
            "SHOP_ONLY": [],
            "QUEST_AND_SHOP": [],
            "SCRIPTED_OTHER": [],
            "DECORATION": [],
            "NEEDS_SCRIPT": [],
            "SCRIPT_EXISTS_NO_NPC": []
        }
        self.stats = {}
    
    def analyze_all(self):
        """Run complete NPC analysis"""
        print("🔍 NPC Categorization Tool for OrionAlpha")
        print("=" * 60)
        
        # Step 1: Scan NPC WZ files
        print("\n📦 Step 1: Scanning NPC WZ files...")
        self.scan_npc_wz_files()
        
        # Step 2: Scan Python scripts
        print("\n🎭 Step 2: Scanning NPC scripts...")
        self.scan_scripts()
        
        # Step 3: Categorize NPCs
        print("\n📊 Step 3: Categorizing NPCs...")
        self.categorize_npcs()
        
        # Step 4: Generate statistics
        print("\n📈 Step 4: Generating statistics...")
        self.generate_stats()
        
        return self.categories, self.stats
    
    def scan_npc_wz_files(self):
        """Scan all NPC XML files from WZ data"""
        npc_dir = self.data_path / "Npc"
        
        if not npc_dir.exists():
            print(f"  ⚠️  NPC directory not found: {npc_dir}")
            return
        
        for xml_file in npc_dir.rglob("*.xml"):
            try:
                npc_id = xml_file.stem.replace(".img", "")
                npc_data = self.parse_npc_xml(xml_file)
                if npc_data:
                    self.npcs[npc_id] = npc_data
            except Exception as e:
                print(f"  ⚠️  Error parsing {xml_file}: {e}")
        
        print(f"  ✅ Found {len(self.npcs)} NPCs in WZ files")
    
    def parse_npc_xml(self, xml_file):
        """Parse NPC XML file and extract relevant data"""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            npc_data = {
                "id": xml_file.stem.replace(".img", ""),
                "file": str(xml_file.relative_to(self.data_path)),
                "name": None,
                "quest": None,
                "has_shop": False,
                "shop_items": [],
                "has_move": False
            }
            
            # Find info node
            info = self.find_node(root, "info")
            if info is not None:
                # Get name
                name_node = self.find_node(info, "name")
                if name_node is not None:
                    npc_data["name"] = name_node.get("value", "Unknown")
                
                # Get quest script reference
                quest_node = self.find_node(info, "quest")
                if quest_node is not None:
                    npc_data["quest"] = quest_node.get("value")
                
                # Check for shop
                shop_node = self.find_node(info, "shop")
                if shop_node is not None:
                    npc_data["has_shop"] = True
                    # Extract shop items
                    for child in shop_node:
                        if child.tag == "imgdir":
                            item_id = child.get("name")
                            if item_id and item_id.isdigit():
                                item_data = {"itemID": int(item_id)}
                                # Get price
                                price_node = self.find_node(child, "price")
                                if price_node is not None:
                                    item_data["price"] = int(price_node.get("value", 0))
                                npc_data["shop_items"].append(item_data)
            
            # Check for move animations
            move_node = self.find_node(root, "move")
            if move_node is not None:
                npc_data["has_move"] = True
            
            return npc_data
            
        except Exception as e:
            print(f"  ⚠️  Error parsing {xml_file}: {e}")
            return None
    
    def find_node(self, parent, name):
        """Find child node by name attribute"""
        for child in parent:
            if child.get("name") == name:
                return child
            # Also check tag name for direct children
            if child.tag == "imgdir" and child.get("name") == name:
                return child
        return None
    
    def scan_scripts(self):
        """Scan all Python scripts in data/Script/"""
        script_dir = self.data_path / "Script"
        
        if not script_dir.exists():
            print(f"  ⚠️  Script directory not found: {script_dir}")
            return
        
        for py_file in script_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            script_name = py_file.stem
            script_data = self.analyze_script(py_file)
            self.scripts[script_name] = script_data
        
        print(f"  ✅ Found {len(self.scripts)} NPC scripts")
    
    def analyze_script(self, script_file):
        """Analyze a Python script file"""
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "file": script_file.name,
                "is_stubbed": "Sorry, I am not coded yet" in content,
                "has_todos": "# TODO" in content,
                "is_quest_related": "quest" in content.lower() or "Quest:" in content,
                "opens_shop": "onOpenShopDlg" in content or "openShop" in content.lower(),
                "has_dialogue": "self.say" in content or "self.askYesNo" in content,
                "size": len(content)
            }
        except Exception as e:
            return {
                "file": script_file.name,
                "error": str(e)
            }
    
    def categorize_npcs(self):
        """Categorize all NPCs based on their properties"""
        
        for npc_id, npc_data in self.npcs.items():
            quest_script = npc_data.get("quest")
            has_shop = npc_data.get("has_shop", False)
            shop_items = npc_data.get("shop_items", [])
            
            # Check if script exists
            script_exists = quest_script and quest_script in self.scripts
            script_working = False
            if script_exists:
                script_info = self.scripts.get(quest_script, {})
                script_working = not script_info.get("is_stubbed", True)
            
            npc_info = {
                "id": npc_id,
                "name": npc_data.get("name", "Unknown"),
                "quest_script": quest_script,
                "has_shop": has_shop,
                "shop_item_count": len(shop_items),
                "script_exists": script_exists,
                "script_working": script_working
            }
            
            # Categorize
            if quest_script and has_shop:
                # Has both quest and shop
                if script_exists and script_working:
                    self.categories["QUEST_AND_SHOP"].append(npc_info)
                else:
                    npc_info["reason"] = "Has quest+shop but script missing/broken"
                    self.categories["NEEDS_SCRIPT"].append(npc_info)
            
            elif quest_script and not has_shop:
                # Quest only
                if script_exists and script_working:
                    self.categories["QUEST_ONLY"].append(npc_info)
                elif script_exists and not script_working:
                    npc_info["reason"] = "Script exists but is stubbed/broken"
                    self.categories["NEEDS_SCRIPT"].append(npc_info)
                else:
                    npc_info["reason"] = "Quest script referenced but missing"
                    self.categories["NEEDS_SCRIPT"].append(npc_info)
            
            elif not quest_script and has_shop:
                # Shop only - these work automatically!
                self.categories["SHOP_ONLY"].append(npc_info)
            
            else:
                # No quest, no shop - decoration
                self.categories["DECORATION"].append(npc_info)
        
        # Check for orphan scripts (scripts that exist but no NPC references them)
        referenced_scripts = {npc.get("quest") for npc in self.npcs.values() if npc.get("quest")}
        for script_name, script_data in self.scripts.items():
            if script_name not in referenced_scripts:
                self.categories["SCRIPT_EXISTS_NO_NPC"].append({
                    "script": script_name,
                    "is_stubbed": script_data.get("is_stubbed", False),
                    "has_dialogue": script_data.get("has_dialogue", False)
                })
        
        # Print category counts
        for category, items in self.categories.items():
            print(f"  {category}: {len(items)}")
    
    def generate_stats(self):
        """Generate statistics summary"""
        total_npcs = len(self.npcs)
        total_scripts = len(self.scripts)
        
        working_npcs = (
            len(self.categories["QUEST_ONLY"]) +
            len(self.categories["SHOP_ONLY"]) +
            len(self.categories["QUEST_AND_SHOP"]) +
            len(self.categories["DECORATION"])
        )
        
        needs_work = len(self.categories["NEEDS_SCRIPT"])
        
        self.stats = {
            "total_npcs_in_wz": total_npcs,
            "total_scripts": total_scripts,
            "working_npcs": working_npcs,
            "needs_implementation": needs_work,
            "completion_percentage": round((working_npcs / total_npcs * 100), 1) if total_npcs > 0 else 0,
            "category_breakdown": {
                category: len(items) for category, items in self.categories.items()
            },
            "shop_npcs_auto_working": len(self.categories["SHOP_ONLY"]),
            "quest_npcs_working": len(self.categories["QUEST_ONLY"]),
            "decoration_npcs": len(self.categories["DECORATION"])
        }
        
        print(f"\n📊 Statistics:")
        print(f"  Total NPCs in WZ: {total_npcs}")
        print(f"  Total Scripts: {total_scripts}")
        print(f"  Working NPCs: {working_npcs} ({self.stats['completion_percentage']}%)")
        print(f"  Needs Implementation: {needs_work}")
    
    def save_reports(self, output_dir="analysis/reports"):
        """Save analysis reports"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON report
        json_report = {
            "stats": self.stats,
            "categories": self.categories,
            "npcs": self.npcs,
            "scripts": self.scripts
        }
        
        with open(f"{output_dir}/npc_analysis.json", 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        
        # Save Markdown report
        md_report = self.generate_markdown_report()
        with open(f"{output_dir}/NPC_REPORT.md", 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        print(f"\n✅ Reports saved to {output_dir}/")
        print(f"  - npc_analysis.json")
        print(f"  - NPC_REPORT.md")
    
    def generate_markdown_report(self):
        """Generate human-readable markdown report"""
        lines = []
        
        lines.append("# OrionAlpha NPC Analysis Report")
        lines.append("")
        lines.append("*Generated by NPC Categorization Tool*")
        lines.append("")
        
        # Summary
        lines.append("## 📊 Summary")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total NPCs in WZ | {self.stats['total_npcs_in_wz']} |")
        lines.append(f"| Total Scripts | {self.stats['total_scripts']} |")
        lines.append(f"| Working NPCs | {self.stats['working_npcs']} |")
        lines.append(f"| Needs Implementation | {self.stats['needs_implementation']} |")
        lines.append(f"| **Completion %** | **{self.stats['completion_percentage']}%** |")
        lines.append("")
        
        # Category breakdown
        lines.append("## 📁 Category Breakdown")
        lines.append("")
        lines.append("| Category | Count | Description |")
        lines.append("|----------|-------|-------------|")
        lines.append(f"| ✅ QUEST_ONLY | {len(self.categories['QUEST_ONLY'])} | Has working quest script |")
        lines.append(f"| ✅ SHOP_ONLY | {len(self.categories['SHOP_ONLY'])} | Shop auto-works from WZ! |")
        lines.append(f"| ✅ QUEST_AND_SHOP | {len(self.categories['QUEST_AND_SHOP'])} | Has both, script works |")
        lines.append(f"| ⬜ DECORATION | {len(self.categories['DECORATION'])} | No interaction needed |")
        lines.append(f"| ❌ NEEDS_SCRIPT | {len(self.categories['NEEDS_SCRIPT'])} | Missing/broken script |")
        lines.append(f"| ⚠️ ORPHAN_SCRIPTS | {len(self.categories['SCRIPT_EXISTS_NO_NPC'])} | Script exists, no NPC uses it |")
        lines.append("")
        
        # Shop NPCs (auto-working)
        lines.append("## 🏪 Shop NPCs (Auto-Working)")
        lines.append("")
        lines.append("These NPCs work automatically - no script needed!")
        lines.append("")
        if self.categories["SHOP_ONLY"]:
            lines.append("| NPC ID | Name | Shop Items |")
            lines.append("|--------|------|------------|")
            for npc in sorted(self.categories["SHOP_ONLY"], key=lambda x: x["id"]):
                lines.append(f"| {npc['id']} | {npc['name']} | {npc['shop_item_count']} items |")
        else:
            lines.append("*No shop-only NPCs found*")
        lines.append("")
        
        # Quest NPCs (working)
        lines.append("## 📜 Quest NPCs (Working)")
        lines.append("")
        if self.categories["QUEST_ONLY"]:
            lines.append("| NPC ID | Name | Script |")
            lines.append("|--------|------|--------|")
            for npc in sorted(self.categories["QUEST_ONLY"], key=lambda x: x["id"]):
                lines.append(f"| {npc['id']} | {npc['name']} | `{npc['quest_script']}.py` |")
        else:
            lines.append("*No quest-only NPCs found*")
        lines.append("")
        
        # NPCs needing implementation
        lines.append("## ❌ NPCs Needing Implementation")
        lines.append("")
        lines.append("These NPCs need scripts to be created or fixed:")
        lines.append("")
        if self.categories["NEEDS_SCRIPT"]:
            lines.append("| NPC ID | Name | Issue | Script Reference |")
            lines.append("|--------|------|-------|------------------|")
            for npc in sorted(self.categories["NEEDS_SCRIPT"], key=lambda x: x["id"]):
                reason = npc.get("reason", "Unknown")
                script = npc.get("quest_script", "N/A")
                lines.append(f"| {npc['id']} | {npc['name']} | {reason} | `{script}` |")
        else:
            lines.append("*All NPCs are implemented!* 🎉")
        lines.append("")
        
        # Decoration NPCs
        lines.append("## ⬜ Decoration NPCs")
        lines.append("")
        lines.append("These NPCs have no interaction (just visual):")
        lines.append("")
        if self.categories["DECORATION"]:
            lines.append("| NPC ID | Name |")
            lines.append("|--------|------|")
            for npc in sorted(self.categories["DECORATION"], key=lambda x: x["id"])[:20]:
                lines.append(f"| {npc['id']} | {npc['name']} |")
            if len(self.categories["DECORATION"]) > 20:
                lines.append(f"| ... | *({len(self.categories['DECORATION']) - 20} more)* |")
        else:
            lines.append("*No decoration NPCs found*")
        lines.append("")
        
        # Implementation priority
        lines.append("## 🎯 Implementation Priority")
        lines.append("")
        lines.append("### High Priority (Affects Gameplay)")
        lines.append("")
        high_priority = [n for n in self.categories["NEEDS_SCRIPT"] if n.get("has_shop")]
        if high_priority:
            for npc in high_priority:
                lines.append(f"- **{npc['name']}** (ID: {npc['id']}) - Has shop, needs script")
        else:
            lines.append("*None - all shop NPCs working!*")
        lines.append("")
        
        lines.append("### Medium Priority (Quest NPCs)")
        lines.append("")
        medium_priority = [n for n in self.categories["NEEDS_SCRIPT"] if not n.get("has_shop")]
        if medium_priority:
            for npc in medium_priority[:10]:
                lines.append(f"- **{npc['name']}** (ID: {npc['id']}) - {npc.get('reason', 'Needs script')}")
            if len(medium_priority) > 10:
                lines.append(f"- *...and {len(medium_priority) - 10} more*")
        else:
            lines.append("*None - all quest NPCs working!*")
        lines.append("")
        
        # Version note
        lines.append("## 📝 Notes")
        lines.append("")
        lines.append("- **JMS v0.20 Content**: This analysis reflects content from JMS v0.20 beta")
        lines.append("- **Shop NPCs**: Work automatically from WZ data - no scripts needed!")
        lines.append("- **Quest NPCs**: Require Python scripts in `data/Script/`")
        lines.append("- **Quest + Shop NPCs**: Script must manually call shop dialog")
        lines.append("")
        
        return "\n".join(lines)


def main():
    """Main entry point"""
    analyzer = NpcAnalyzer()
    analyzer.analyze_all()
    analyzer.save_reports()
    
    print("\n" + "=" * 60)
    print("✅ NPC Analysis Complete!")
    print("\nKey Findings:")
    print(f"  🏪 Shop NPCs (auto-work): {len(analyzer.categories['SHOP_ONLY'])}")
    print(f"  📜 Quest NPCs (working): {len(analyzer.categories['QUEST_ONLY'])}")
    print(f"  ❌ Needs Implementation: {len(analyzer.categories['NEEDS_SCRIPT'])}")
    print(f"  ⬜ Decoration (no action): {len(analyzer.categories['DECORATION'])}")


if __name__ == "__main__":
    main()
