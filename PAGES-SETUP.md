# GitHub Pages Setup

## Enable GitHub Pages

The workflow will fail until GitHub Pages is enabled in the repository settings.

### Steps to Enable:

1. Go to repository Settings → Pages
2. Under "Source", select **"GitHub Actions"**
3. Save the settings

### Alternative: Enable via GitHub CLI

```bash
gh api repos/selfapplied/opic-growth-service/pages \
  -X POST \
  -f source='{"branch":"main","path":"/"}'
```

Note: This may require repository admin permissions.

### Verify Setup

After enabling, the workflow should succeed. Check:
- Settings → Pages should show "GitHub Actions" as source
- Actions tab should show successful deployments
- Site should be available at: `https://selfapplied.github.io/opic-growth-service/`

