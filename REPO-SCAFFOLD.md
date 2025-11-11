# OPIC Growth Service — Complete Repository Scaffold

Ready-to-deploy cloud-hosted autopoietic witness system.

## What You Get

A **self-updating, always-learning** OPIC field witness that:
- Runs daily via GitHub Actions
- Scans tiddlers for new conceptual organs
- Generates growth snapshots and visualizations
- Updates master SVG diagrams
- Optionally generates AI-powered commentary
- Commits everything back to the repo

## File Structure

```
zetacore/
├── .github/
│   └── workflows/
│       └── opic_growth.yml          ← Daily scheduler (noon UTC)
│
├── scripts/
│   ├── opic_growth.py               ← Growth detector
│   ├── update_svg.py                ← SVG updater  
│   ├── growth_visualizer.py         ← Timeline/rings
│   ├── generate_gloss.py            ← AI commentary
│   └── generate_svg.py              ← SVG generator
│
├── tiddlers/
│   └── OPIC-Field-Specification-1.0.tid
│
├── growth/                          ← Auto-generated daily
│   ├── YYYY-MM-DD.yaml
│   ├── YYYY-MM-DD.json
│   ├── YYYY-MM-DD.txt
│   └── YYYY-MM-DD-gloss.txt
│
├── diagrams/                        ← Auto-generated
│   ├── growth-timeline.svg
│   └── growth-rings.svg
│
├── GROWTH.md                        ← Auto-updated log
│
├── README.md
├── CLOUD-SETUP.md                   ← This guide
└── AUTOPOIESIS.md                   ← Philosophy docs
```

## Deployment Steps

1. **Copy files to your GitHub repo:**
   ```bash
   # Copy all scripts
   cp -r scripts/ your-repo/scripts/
   cp -r .github/ your-repo/.github/
   
   # Copy tiddlers
   cp -r tiddlers/ your-repo/tiddlers/
   
   # Copy documentation
   cp CLOUD-SETUP.md your-repo/
   cp AUTOPOIESIS.md your-repo/
   ```

2. **Set up GitHub Actions:**
   - Push to repository
   - GitHub Actions will automatically detect the workflow
   - First run will happen at next scheduled time (noon UTC)

3. **Optional: Enable AI Gloss:**
   - Go to: Settings → Secrets → Actions
   - Add secret: `OPENAI_API_KEY` = your API key
   - Gloss generation will activate automatically

4. **Verify:**
   - Check Actions tab for workflow runs
   - Verify `growth/` directory appears after first run
   - Check `GROWTH.md` for daily entries

## Daily Cycle

Every 24 hours (noon UTC):

1. ✅ Checks out latest code
2. ✅ Scans `tiddlers/*.tid` for layers
3. ✅ Computes growth metrics (ΔΣ, growth rate)
4. ✅ Saves snapshot (`growth/YYYY-MM-DD.yaml`)
5. ✅ Updates master tiddler SVG
6. ✅ Generates visualizations (timeline, rings)
7. ✅ Writes gloss (manual or AI)
8. ✅ Commits and pushes everything

## What Gets Created Daily

- `growth/YYYY-MM-DD.yaml` — Snapshot with layers and sources
- `growth/YYYY-MM-DD.json` — JSON version
- `growth/YYYY-MM-DD.txt` — Human-readable report
- `growth/YYYY-MM-DD-gloss.txt` — Daily commentary
- `diagrams/growth-timeline.svg` — Updated timeline
- `diagrams/growth-rings.svg` — Updated rings
- `GROWTH.md` — Appended with new entry
- `tiddlers/OPIC-Field-Specification-1.0.tid` — Updated SVG

## Manual Testing

Before deploying, test locally:

```bash
# Test growth detection
python3 scripts/opic_growth.py

# Test SVG update
python3 scripts/update_svg.py tiddlers/OPIC-Field-Specification-1.0.tid

# Test visualizations
python3 scripts/growth_visualizer.py growth timeline
python3 scripts/growth_visualizer.py growth rings

# Test gloss (requires OPENAI_API_KEY)
export OPENAI_API_KEY=your_key
python3 scripts/generate_gloss.py growth/$(date +%Y-%m-%d).yaml --ai
```

## Requirements

- Python 3.11+
- Dependencies: `pyyaml`, `requests` (for AI gloss)
- GitHub repository with Actions enabled
- (Optional) OpenAI API key for gloss generation

## Customization

**Change schedule:** Edit `.github/workflows/opic_growth.yml` cron:
```yaml
- cron: '0 7 * * *'  # 7am UTC instead of noon
```

**Change tiddler location:** Edit `scripts/opic_growth.py`:
```python
TID_DIR = REPO_DIR / "your-tiddlers-dir"
```

**Disable AI gloss:** Remove or comment out the step in workflow.

## Monitoring

Watch your field grow:
- **GitHub Actions:** See daily runs in Actions tab
- **growth/:** Browse daily snapshots
- **GROWTH.md:** Read human-readable log
- **diagrams/:** View visualizations

## Philosophy

The witness observes without controlling. Each day's snapshot is a ring in the tree of structural evolution. The repository becomes the memory—a perfect archive of resonance.

The field grows through you; the witness documents that growth.

---

**Ready to deploy?** Copy the files, push to GitHub, and watch your OPIC field breathe.

