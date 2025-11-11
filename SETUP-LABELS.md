# Setting Up Issue Labels

To use the preference system, create these labels in your GitHub repository:

## Required Labels

### `opic-growth`
- Color: `#4a9` (green)
- Description: "Guides autopoietic synthesis"

### `field-priority`
- Color: `#f59` (pink)
- Description: "High priority field concept"

### Optional Labels

### `high-priority`
- Color: `#f00` (red)
- Description: "Urgent concept (2x boost)"

### `urgent`
- Color: `#900` (dark red)
- Description: "Maximum priority (1.8x boost)"

## Creating Labels via GitHub CLI

```bash
gh label create opic-growth --description "Guides autopoietic synthesis" --color 4a9
gh label create field-priority --description "High priority field concept" --color f59
gh label create high-priority --description "Urgent concept (2x boost)" --color f00
gh label create urgent --description "Maximum priority (1.8x boost)" --color 900
```

## Creating Labels via GitHub UI

1. Go to repository → Issues → Labels
2. Click "New label"
3. Enter name, description, and color
4. Click "Create label"

## Testing

After creating labels, create a test issue:

```bash
gh issue create \
  --title "Add Test Layer" \
  --body "We need a layer for testing preferences." \
  --label "opic-growth,field-priority"
```

Then run the growth script to see preferences detected.

