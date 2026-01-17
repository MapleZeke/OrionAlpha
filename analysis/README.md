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

# Generate feature report
python3 analysis/feature_matrix.py
```

## Output

All reports are saved to `analysis/reports/`:

- `wz_inventory.json` - Complete WZ file inventory
- `script_analysis.json` - NPC script completion status
- `quest_gaps.json` - Quest implementation gaps
- `FEATURE_REPORT.md` - Human-readable feature report

## Interpretation

### Script Status

- **Complete**: Fully implemented, no TODOs
- **Partial**: Has TODO comments, needs completion
- **Stubbed**: Just a placeholder ("Sorry, I am not coded yet")

### Quest System

Compares quests defined in WZ files vs implemented in NPC scripts to identify missing quest handlers.
