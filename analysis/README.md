# OrionAlpha Feature Analysis Toolkit

Comprehensive analysis tools for OrionAlpha game server to inventory WZ content and track implementation status.

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## Usage

Run all analysis tools:

```bash
cd /path/to/OrionAlpha
python3 analysis/run_analysis.py
```

Or run individual tools:

```bash
# Scan WZ files
python3 analysis/wz_scanner.py

# Analyze scripts
python3 analysis/script_analyzer.py

# Detect quest gaps
python3 analysis/quest_detector.py

# Analyze NPCs
python3 analysis/run_npc_analysis.py

# Generate feature report
python3 analysis/feature_matrix.py
```

## Output

All reports are saved to `analysis/reports/`:

- `wz_inventory.json` - Complete WZ file inventory
- `script_analysis.json` - NPC script completion status
- `quest_gaps.json` - Quest implementation gaps
- `npc_analysis.json` - NPC categorization data
- `NPC_REPORT.md` - Human-readable NPC report
- `FEATURE_REPORT.md` - Human-readable feature report

## Interpretation

### Script Status

- **Complete**: Fully implemented, no TODOs
- **Partial**: Has TODO comments, needs completion
- **Stubbed**: Just a placeholder ("Sorry, I am not coded yet")

### Quest System

Compares quests defined in WZ files vs implemented in NPC scripts to identify missing quest handlers.

## NPC Analysis Tool

Categorizes all NPCs by their interaction type:

### NPC Categories

| Category | Description | Action Needed |
|----------|-------------|---------------|
| `SHOP_ONLY` | Has shop items in WZ | ✅ Auto-works! |
| `QUEST_ONLY` | Has working quest script | ✅ Working |
| `QUEST_AND_SHOP` | Has both, script handles shop | ✅ Working |
| `DECORATION` | No interaction | ⬜ None needed |
| `NEEDS_SCRIPT` | Script missing or broken | ❌ Needs work |

### How It Works

The tool scans all NPCs from WZ files and categorizes them:

1. **Shop NPCs**: NPCs with shop items in WZ work automatically - no script needed!
2. **Quest NPCs**: NPCs with quest references need Python scripts
3. **Quest + Shop NPCs**: Scripts must manually handle shop dialog
4. **Decoration NPCs**: Visual only, no interaction needed

### Running NPC Analysis

```bash
# Run NPC analysis only
python3 analysis/run_npc_analysis.py

# Or run with full analysis suite
python3 analysis/run_analysis.py
```

### Output

- `analysis/reports/npc_analysis.json` - Full NPC categorization data
- `analysis/reports/NPC_REPORT.md` - Human-readable report with priorities

### Current Status (as of latest analysis)

**Overall Completion: 91.0%**

- ✅ **53 Quest NPCs** - Fully implemented with working scripts
- ✅ **21 Shop NPCs** - Auto-working from WZ data (no script needed)
- ⬜ **7 Decoration NPCs** - Visual only, no interaction needed
- ❌ **8 NPCs** - Still need script implementation:
  - 3 Job Advancement NPCs (change_swordman, change_magician, change_rogue)
  - 5 Refining/Crafting NPCs (refine_henesys, refine_perion, refine_perion2, refine_ellinia, refine_sleepy)

**Key Findings:**
- Zero orphan scripts (all scripts are referenced by NPCs)
- All shop-only NPCs work automatically from WZ data
- All functional NPCs (excluding decoration) are at 91% completion
- Remaining 8 NPCs have stub scripts with TODO comments for porting from JavaScript
