#!/usr/bin/env python3
"""
Standalone NPC Analysis Runner
Run this to analyze just NPCs without running the full analysis suite
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.npc_analyzer import NpcAnalyzer

def main():
    print("🎭 OrionAlpha NPC Categorization Tool")
    print("=" * 60)
    
    analyzer = NpcAnalyzer()
    analyzer.analyze_all()
    analyzer.save_reports()
    
    print("\n" + "=" * 60)
    print("✅ NPC Analysis Complete!")
    print("\nGenerated files:")
    print("  - analysis/reports/npc_analysis.json")
    print("  - analysis/reports/NPC_REPORT.md")
    
    # Print actionable summary
    print("\n📋 Actionable Summary:")
    print("-" * 40)
    
    needs_work = analyzer.categories.get("NEEDS_SCRIPT", [])
    if needs_work:
        print(f"\n❌ {len(needs_work)} NPCs need implementation:")
        for npc in needs_work[:5]:
            print(f"   - {npc['name']} (ID: {npc['id']})")
        if len(needs_work) > 5:
            print(f"   - ...and {len(needs_work) - 5} more (see NPC_REPORT.md)")
    else:
        print("\n✅ All NPCs are implemented!")
    
    shop_only = analyzer.categories.get("SHOP_ONLY", [])
    print(f"\n🏪 {len(shop_only)} Shop NPCs work automatically (no script needed)")
    
    quest_only = analyzer.categories.get("QUEST_ONLY", [])
    print(f"\n📜 {len(quest_only)} Quest NPCs have working scripts")
    
    decoration = analyzer.categories.get("DECORATION", [])
    print(f"\n⬜ {len(decoration)} NPCs are decoration (no interaction)")


if __name__ == "__main__":
    main()
