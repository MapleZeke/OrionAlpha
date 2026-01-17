#!/usr/bin/env python3
"""
WZ File Scanner for OrionAlpha
Scans all WZ XML files and catalogs game content (NPCs, items, mobs, maps, quests, etc.)
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
import json

class WzScanner:
    def __init__(self, data_path="data"):
        self.data_path = Path(data_path)
        self.inventory = {
            "npcs": {},
            "items": {},
            "mobs": {},
            "maps": {},
            "skills": {},
            "quests": {},
            "strings": {},
            "etc": {}
        }
    
    def scan_all(self):
        """Scan all WZ directories"""
        print("🔍 Scanning WZ files...")
        
        # Scan each WZ directory
        wz_dirs = {
            "Character": self.scan_character,
            "Item": self.scan_items,
            "Mob": self.scan_mobs,
            "Map": self.scan_maps,
            "Npc": self.scan_npcs,
            "Skill": self.scan_skills,
            "String": self.scan_strings,
            "Etc": self.scan_etc,
            "Quest": self.scan_quests
        }
        
        for dir_name, scan_func in wz_dirs.items():
            dir_path = self.data_path / dir_name
            if dir_path.exists():
                print(f"  📁 Scanning {dir_name}/")
                scan_func(dir_path)
        
        return self.inventory
    
    def scan_xml_file(self, xml_file):
        """Parse a single XML file and return the tree"""
        try:
            tree = ET.parse(xml_file)
            return tree.getroot()
        except Exception as e:
            print(f"    ⚠️  Error parsing {xml_file}: {e}")
            return None
    
    def scan_npcs(self, npc_dir):
        """Scan NPC WZ files"""
        for xml_file in npc_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                npc_id = xml_file.stem
                self.inventory["npcs"][npc_id] = {
                    "id": npc_id,
                    "file": str(xml_file.relative_to(self.data_path)),
                    "properties": self._extract_properties(root)
                }
    
    def scan_items(self, item_dir):
        """Scan Item WZ files"""
        for xml_file in item_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                item_id = xml_file.stem
                category = xml_file.parent.name
                self.inventory["items"][item_id] = {
                    "id": item_id,
                    "category": category,
                    "file": str(xml_file.relative_to(self.data_path)),
                    "properties": self._extract_properties(root)
                }
    
    def scan_mobs(self, mob_dir):
        """Scan Mob WZ files"""
        for xml_file in mob_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                mob_id = xml_file.stem
                self.inventory["mobs"][mob_id] = {
                    "id": mob_id,
                    "file": str(xml_file.relative_to(self.data_path)),
                    "properties": self._extract_properties(root)
                }
    
    def scan_maps(self, map_dir):
        """Scan Map WZ files"""
        for xml_file in map_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                map_id = xml_file.stem
                self.inventory["maps"][map_id] = {
                    "id": map_id,
                    "file": str(xml_file.relative_to(self.data_path)),
                    "properties": self._extract_properties(root)
                }
    
    def scan_skills(self, skill_dir):
        """Scan Skill WZ files"""
        for xml_file in skill_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                skill_id = xml_file.stem
                self.inventory["skills"][skill_id] = {
                    "id": skill_id,
                    "file": str(xml_file.relative_to(self.data_path)),
                    "properties": self._extract_properties(root)
                }
    
    def scan_quests(self, quest_dir):
        """Scan Quest WZ files - CRITICAL for quest detection"""
        for xml_file in quest_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                quest_id = xml_file.stem
                quest_data = self._extract_quest_data(root)
                self.inventory["quests"][quest_id] = {
                    "id": quest_id,
                    "file": str(xml_file.relative_to(self.data_path)),
                    **quest_data
                }
    
    def scan_strings(self, string_dir):
        """Scan String WZ files for names/descriptions"""
        for xml_file in string_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                string_type = xml_file.stem
                self.inventory["strings"][string_type] = {
                    "file": str(xml_file.relative_to(self.data_path)),
                    "entries": self._extract_string_entries(root)
                }
    
    def scan_etc(self, etc_dir):
        """Scan Etc WZ files"""
        for xml_file in etc_dir.rglob("*.xml"):
            root = self.scan_xml_file(xml_file)
            if root:
                etc_type = xml_file.stem
                self.inventory["etc"][etc_type] = {
                    "file": str(xml_file.relative_to(self.data_path)),
                    "properties": self._extract_properties(root)
                }
    
    def scan_character(self, char_dir):
        """Scan Character WZ files (equipment, etc.)"""
        # Character data is already handled by ItemInfo.load() in the server
        pass
    
    def _extract_properties(self, node):
        """Extract properties from XML node"""
        props = {}
        for child in node:
            if child.tag == "imgdir":
                name = child.get("name", "unknown")
                props[name] = self._extract_properties(child)
            else:
                name = child.get("name", child.tag)
                value = child.get("value", "")
                props[name] = value
        return props
    
    def _extract_quest_data(self, root):
        """Extract quest-specific data"""
        quest_info = {
            "name": "",
            "description": "",
            "requirements": {},
            "rewards": {},
            "npcs": []
        }
        
        # Look for quest-specific structure
        for child in root:
            if child.tag == "imgdir":
                section = child.get("name", "")
                if section == "info":
                    quest_info.update(self._extract_properties(child))
                elif section == "say":
                    quest_info["dialogue"] = self._extract_properties(child)
                elif section == "act":
                    quest_info["rewards"] = self._extract_properties(child)
                elif section == "check":
                    quest_info["requirements"] = self._extract_properties(child)
        
        return quest_info
    
    def _extract_string_entries(self, root):
        """Extract string entries (names, descriptions)"""
        entries = {}
        for child in root:
            if child.tag == "imgdir":
                entry_id = child.get("name", "")
                entry_data = {}
                for subchild in child:
                    key = subchild.get("name", "")
                    value = subchild.get("value", "")
                    entry_data[key] = value
                entries[entry_id] = entry_data
        return entries
    
    def save_report(self, output_file="analysis/reports/wz_inventory.json"):
        """Save inventory to JSON file"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Generate summary stats
        summary = {
            "total_npcs": len(self.inventory["npcs"]),
            "total_items": len(self.inventory["items"]),
            "total_mobs": len(self.inventory["mobs"]),
            "total_maps": len(self.inventory["maps"]),
            "total_skills": len(self.inventory["skills"]),
            "total_quests": len(self.inventory["quests"]),
            "string_files": len(self.inventory["strings"]),
            "etc_files": len(self.inventory["etc"])
        }
        
        output = {
            "summary": summary,
            "inventory": self.inventory
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ WZ inventory saved to {output_file}")
        print(f"\n📊 Summary:")
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        return output

if __name__ == "__main__":
    scanner = WzScanner()
    scanner.scan_all()
    scanner.save_report()
