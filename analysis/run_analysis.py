#!/usr/bin/env python3
"""
Main analysis runner - executes all analysis tools
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.wz_scanner import WzScanner
from analysis.script_analyzer import ScriptAnalyzer
from analysis.quest_detector import QuestDetector
from analysis.feature_matrix import FeatureMatrix
from analysis.npc_analyzer import NpcAnalyzer

def main():
    print("🚀 OrionAlpha Feature Analysis Toolkit\n")
    print("=" * 60)
    
    # Step 1: Scan WZ files
    print("\n📦 Step 1: Scanning WZ files...")
    scanner = WzScanner()
    scanner.scan_all()
    scanner.save_report()
    
    # Step 2: Analyze scripts
    print("\n🎭 Step 2: Analyzing NPC scripts...")
    analyzer = ScriptAnalyzer()
    analyzer.analyze_all()
    analyzer.save_report()
    
    # Step 3: Detect quest gaps
    print("\n📋 Step 3: Detecting quest implementation gaps...")
    detector = QuestDetector()
    detector.load_data()
    detector.detect_gaps()
    detector.save_report()
    
    # Step 4: Analyze NPCs
    print("\n🎭 Step 4: Analyzing NPC categories...")
    npc_analyzer = NpcAnalyzer()
    npc_analyzer.analyze_all()
    npc_analyzer.save_reports()
    
    # Step 5: Generate feature matrix
    print("\n📊 Step 5: Generating feature completeness report...")
    matrix = FeatureMatrix()
    matrix.load_all_data()
    matrix.save_report()
    
    print("\n" + "=" * 60)
    print("✅ Analysis complete! Check analysis/reports/ for results")
    print("\nGenerated files:")
    print("  - analysis/reports/wz_inventory.json")
    print("  - analysis/reports/script_analysis.json")
    print("  - analysis/reports/quest_gaps.json")
    print("  - analysis/reports/npc_analysis.json")
    print("  - analysis/reports/NPC_REPORT.md")
    print("  - analysis/reports/FEATURE_REPORT.md")

if __name__ == "__main__":
    main()
