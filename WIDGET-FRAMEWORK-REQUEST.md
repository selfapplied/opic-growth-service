# Tiddler + React Recombined Widget Framework

## Overview

A unified widget framework combining TiddlyWiki tiddler architecture with React components, featuring hardware-style controls for configuration and WebGL visualization support.

## Core Concept

**Recombined** — widgets that can be decomposed into tiddlers and recomposed into React components, maintaining bidirectional sync between tiddler data and React state.

## Architecture

### Tiddler Integration
- Each widget configuration stored as a tiddler
- Tiddler fields map to React props
- Changes in React update tiddler, changes in tiddler update React
- Self-contained widget definitions (tiddler + React component)

### React Components
- Pure functional components where possible
- State management via tiddler sync
- Composable widget system
- Hot-reloadable configurations

## Widget Types

### Backpanels
- Configuration surfaces
- Grid-based layout system
- Collapsible sections
- Nested panel support
- Export/import configurations as tiddlers

### Dials and Knobs
- Continuous value controls
- Rotary dials with visual feedback
- Precision adjustment modes
- Value ranges and constraints
- Smooth interpolation
- MIDI-style control support

### Sequencers
- Step-based button grids
- Pattern editing
- Playback controls
- Loop and pattern management
- Visual feedback for active steps
- Export patterns as tiddler data

### Buttons
- Momentary and toggle modes
- Visual state feedback
- Button groups and matrices
- Macro buttons (trigger sequences)
- Customizable appearance

## WebGL Support

### Visualization Layer
- WebGL canvas for widget rendering
- Hardware-accelerated graphics
- Custom shaders for visual effects
- Real-time parameter visualization
- 3D knob/dial rendering option
- Performance-optimized rendering

### Integration Points
- Widget values drive WebGL uniforms
- Visual feedback from WebGL to widgets
- Shared state between React and WebGL
- Canvas overlays for widget controls

## Configuration System

### Tiddler Schema
```yaml
title: Widget-Configuration-Example
type: application/json

widgets:
  - type: backpanel
    id: main-config
    layout: grid
    children:
      - type: knob
        id: frequency
        min: 20
        max: 20000
        value: 440
        label: "Frequency"
      - type: sequencer
        id: pattern-1
        steps: 16
        pattern: [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
```

### React Component Mapping
- Tiddler → React props mapping
- Bidirectional data binding
- Change detection and sync
- Conflict resolution

## Use Cases

1. **OPIC Field Configuration**
   - Visual control panel for field parameters
   - Real-time adjustment with WebGL visualization
   - Save configurations as tiddlers

2. **JIT Model Configuration**
   - Kernel loading strategy controls
   - Environment adaptation sliders
   - Domain selection sequencers

3. **Growth Visualization**
   - Interactive parameter exploration
   - Pattern editing for growth sequences
   - WebGL-rendered field visualizations

## Technical Requirements

### Dependencies
- React (latest)
- TiddlyWiki tiddler parser
- WebGL context management
- State synchronization layer

### Performance
- 60fps WebGL rendering
- Smooth widget interactions
- Efficient tiddler serialization
- Minimal re-renders

### Browser Support
- Modern browsers with WebGL
- ES6+ JavaScript
- CSS Grid/Flexbox

## Implementation Phases

### Phase 1: Core Framework
- Tiddler ↔ React sync layer
- Basic widget components (knob, button)
- Simple backpanel layout

### Phase 2: Advanced Controls
- Sequencer component
- Complex dial/knob variants
- Nested backpanels

### Phase 3: WebGL Integration
- WebGL context setup
- Widget-to-WebGL binding
- Basic visualization shaders

### Phase 4: Polish & Optimization
- Performance tuning
- Advanced visual effects
- Documentation and examples

## Integration with Existing Systems

### OPIC Field
- Widget configurations become field parameters
- Real-time field manipulation
- Visual field representation

### JIT Language Model
- Model configuration interface
- Kernel selection controls
- Strategy adjustment panels

### Growth System
- Growth pattern editors
- Parameter exploration tools
- Visualization controls

## Design Principles

- **Reversibility** — widget state ↔ tiddler data
- **Composability** — widgets combine into larger interfaces
- **Performance** — smooth interactions, efficient rendering
- **Resonance** — visual feedback matches parameter changes
- **Empathy** — intuitive controls, clear visual language

## Example Usage

```javascript
import { WidgetFramework } from '@opic/widgets';
import { TiddlerStore } from '@opic/tiddlers';

const store = new TiddlerStore();
const framework = new WidgetFramework({ store });

// Load configuration from tiddler
const config = await store.getTiddler('MyWidgetConfig');

// Render widget panel
framework.render('main-panel', config, {
  onUpdate: (widgetId, value) => {
    // Sync back to tiddler
    store.updateTiddler('MyWidgetConfig', widgetId, value);
  }
});
```

## Future Enhancements

- MIDI device integration
- OSC protocol support
- Custom widget builder
- Widget marketplace (shareable tiddler configs)
- Multi-user collaborative editing
- Mobile touch support
- Haptic feedback integration

