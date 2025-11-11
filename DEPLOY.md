# Deployment Instructions

## Current Status

✅ Repository initialized  
✅ All files committed  
✅ Ready for deployment  

## Deploy to GitHub

### Option 1: New Repository

1. **Create repository on GitHub:**
   - Go to https://github.com/new
   - Name: `zetacore` (or your preferred name)
   - Description: "OPIC Field Growth Service — Autopoietic Witness"
   - Choose Public or Private
   - **Do NOT** initialize with README (we already have one)

2. **Push to GitHub:**
   ```bash
   cd /Users/joelstover/whitepaper
   git remote add origin https://github.com/YOUR_USERNAME/zetacore.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Actions:**
   - Go to repository Settings → Actions → General
   - Ensure "Allow all actions and reusable workflows" is enabled
   - Save

4. **Optional: Add OpenAI API Key:**
   - Go to Settings → Secrets → Actions → New repository secret
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
   - Add secret

### Option 2: Existing Repository

If you already have a GitHub repository:

```bash
cd /Users/joelstover/whitepaper
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Verify Deployment

After pushing:

1. **Check GitHub Actions:**
   - Go to Actions tab in your repository
   - You should see "Daily OPIC Growth" workflow
   - First run will happen at next scheduled time (noon UTC)
   - Or trigger manually: Actions → Daily OPIC Growth → Run workflow

2. **Verify Files:**
   - Check that `.github/workflows/opic_growth.yml` exists
   - Check that `scripts/` directory contains all Python files
   - Check that `tiddlers/` directory exists

3. **Test Locally First (Recommended):**
   ```bash
   # Test growth detection
   python3 scripts/opic_growth.py
   
   # Test SVG update
   python3 scripts/update_svg.py tiddlers/OPIC-Field-Specification-1.0.tid
   
   # Test visualizations
   python3 scripts/growth_visualizer.py growth timeline
   ```

## What Happens Next

Once deployed:

- **Daily at noon UTC:** Workflow runs automatically
- **Growth snapshots:** Created in `growth/YYYY-MM-DD.yaml`
- **Visualizations:** Updated in `diagrams/`
- **Master tiddler:** SVG updated automatically
- **Growth log:** `GROWTH.md` appended daily

## Monitoring

Watch your field grow:

- **GitHub Actions:** See daily runs in Actions tab
- **growth/:** Browse daily snapshots
- **GROWTH.md:** Read human-readable log
- **diagrams/:** View timeline and ring visualizations

## Troubleshooting

**Workflow doesn't run:**
- Check Actions tab for errors
- Verify workflow file is in `.github/workflows/`
- Check Python version compatibility

**No layers detected:**
- Ensure tiddlers have `opic` or `architecture` in content
- Check YAML format matches expected structure
- Verify file paths in scripts

**AI gloss fails:**
- Check `OPENAI_API_KEY` secret is set correctly
- System falls back to manual gloss automatically
- Check API quota/limits

## Next Steps

1. Push to GitHub (see commands above)
2. Enable GitHub Actions
3. (Optional) Add OpenAI API key
4. Wait for first daily run or trigger manually
5. Watch your OPIC field grow!

---

**Ready to deploy?** Run the git commands above to push to your repository.

