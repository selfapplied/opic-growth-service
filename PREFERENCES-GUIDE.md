# Issue-Based Growth Preferences

Guide the autopoietic witness by creating GitHub issues that express your intentions.

## How It Works

1. **Create GitHub Issues** with specific labels
2. **Describe concepts** you want prioritized
3. **Witness reads issues** and boosts matching synthesis
4. **Field grows** toward your expressed intentions

## Creating Preference Issues

### Basic Format

**Title:** Clear description of desired concept/layer  
**Labels:** `opic-growth` or `field-priority`  
**Body:** Description of what you want prioritized

### Example Issue

```
Title: Add Quantum Resonance Layer

Labels: opic-growth, field-priority

Body:
We need a layer that measures quantum resonance patterns 
across the OPIC field. This should track:
- Harmonic frequencies
- Resonance nodes
- Quantum coherence states
```

### Priority Labels

- `opic-growth` - General growth preference
- `field-priority` - High priority concept
- `high-priority` - Urgent concept (2x boost)
- `urgent` - Maximum priority (1.8x boost)

## What Gets Detected

The witness looks for:

1. **Explicit requests:**
   - "layer: ConceptName"
   - "concept: ConceptName"
   - "add: ConceptName"
   - "priority: ConceptName"

2. **Capitalized terms** in issue text (potential concepts)

3. **Pattern matching** with synthesized layers

## How Preferences Work

When the witness synthesizes layers:

1. **Reads all issues** with `opic-growth` or `field-priority` labels
2. **Extracts concepts** from titles and bodies
3. **Boosts confidence** of matching synthesized layers
4. **Lowers threshold** for preference-matched concepts (0.3 vs 0.4)

### Priority Multipliers

- Normal: 1.0x
- `field-priority`: 1.5x
- `high-priority`: 2.0x
- `urgent`: 1.8x

## Examples

### Example 1: Specific Layer Request

```
Title: Add Empathy Measurement Layer

Labels: opic-growth

Body:
The field needs a layer that measures empathy as reversibility.
This should track how reversible processes create empathetic connections.
```

### Example 2: Concept Priority

```
Title: Prioritize Curvature Analysis

Labels: field-priority, high-priority

Body:
We want to emphasize curvature (tan θ) measurements.
This concept should be prioritized in synthesis.
```

### Example 3: Multiple Concepts

```
Title: Add Multiple Resonance Concepts

Labels: opic-growth

Body:
We need layers for:
- Harmonic resonance
- Quantum resonance  
- Field resonance
- Symmetry resonance
```

## Local Preferences (Fallback)

If GitHub issues aren't available, create `PREFERENCES.md`:

```markdown
# Growth Preferences

- Quantum Resonance Layer
- Empathy Measurement
- Curvature Analysis
- Harmonic Patterns
```

## Viewing Active Preferences

The witness reports active preferences in each run:

```
Active Growth Preferences:
==================================================
issue #5:
  🔴 Quantum Resonance (priority: 2.0x)
     → Add Quantum Resonance Layer
  🟡 Harmonic Patterns (priority: 1.5x)
     → Prioritize Harmonic Analysis
```

## Best Practices

1. **Be specific** - Clear concept names work best
2. **Use labels** - Proper labels ensure detection
3. **Describe context** - Helps with matching
4. **Update issues** - Close when satisfied
5. **Combine labels** - Use multiple for emphasis

## Integration

Preferences are automatically:
- Read during each workflow run
- Applied to synthesis confidence
- Reported in growth logs
- Used to guide autonomous growth

The witness respects your intentions while maintaining autonomous synthesis.

