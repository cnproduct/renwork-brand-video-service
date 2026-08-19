---
name: "brand-motion"
description: "Defines brand motion design guidelines including animation curves, durations, and micro-interaction patterns. Invoke when user needs motion design specs, animation guidelines, or interaction rhythm rules for a brand."
---

# Brand Motion

A motion design specification skill that defines how a brand moves — animation curves, timing, transitions, and micro-interactions — creating a kinetic identity that reinforces the brand personality across digital touchpoints.

## Core Capabilities

### 1. Motion Personality Definition
- Map brand personality to motion characteristics (energetic vs. calm, playful vs. precise)
- Define motion principles: 3-5 guiding rules (e.g., "Always arrive, never appear")
- Create a motion spectrum: where the brand sits on fast↔slow, linear↔organic, subtle↔expressive

### 2. Easing & Timing System
- Define standard easing curves (cubic-bezier values) for each interaction type
- Set duration scale: micro (100-200ms), standard (200-400ms), expressive (400-800ms)
- Create timing tokens for: entrances, exits, state changes, loops, emphasis

### 3. Micro-Interaction Patterns
- Define button press/hover/release animations
- Specify page transition styles (fade, slide, scale, morph)
- Design loading states and skeleton screens
- Create success/error/celebration animations
- Define scroll-triggered animations

### 4. Logo Animation
- Design logo intro/reveal animation
- Define logo transition between states (color → monochrome → reversed)
- Create looping logo animation for splash screens
- Specify logo motion do's and don'ts

## Industry Motion Adaptation

| Industry | Motion Energy | Duration Range | Easing Style | Signature Pattern |
|----------|--------------|----------------|-------------|-------------------|
| Tech/SaaS | Smooth, fluid | 200-300ms | ease-out | Data viz animations, smooth state transitions |
| Food & Beverage | Playful, bouncy | 300-500ms | spring/bounce | Appetizing reveals, ingredient animations |
| Fashion | Elegant, slow | 400-800ms | ease-in-out | Slow fades, parallax, editorial reveals |
| Finance | Subtle, precise | 150-250ms | ease-in-out | Number counters, chart builds, subtle confirms |
| Healthcare | Gentle, soothing | 400-600ms | ease-in-out | Soft fades, gentle slides, calming pulses |
| Education | Encouraging, celebratory | 200-400ms | ease-out + overshoot | Achievement animations, progress celebrations |
| Entertainment | Bold, dramatic | 300-700ms | custom/dramatic | Splash screens, reveal animations |
| Hospitality | Warm, graceful | 300-500ms | ease-in-out | Smooth welcomes, gentle transitions |

## Standard Motion Tokens

```json
{
  "easing": {
    "standard": "cubic-bezier(0.4, 0.0, 0.2, 1)",
    "decelerate": "cubic-bezier(0.0, 0.0, 0.2, 1)",
    "accelerate": "cubic-bezier(0.4, 0.0, 1, 1)",
    "spring": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
    "smooth": "cubic-bezier(0.45, 0.05, 0.55, 0.95)"
  },
  "duration": {
    "micro": 150,
    "short": 200,
    "standard": 300,
    "long": 500,
    "expressive": 800
  },
  "patterns": {
    "fade_in": { "opacity": [0, 1], "duration": "short", "easing": "decelerate" },
    "slide_up": { "transform": "translateY(20px)→0", "duration": "standard", "easing": "decelerate" },
    "scale_in": { "transform": "scale(0.95)→1", "duration": "short", "easing": "spring" },
    "press": { "transform": "scale(1)→0.97", "duration": "micro", "easing": "standard" }
  }
}
```

## Motion Principles Template

Each brand should define 3-5 motion principles:

```
Example (Healthcare brand):
1. "Always arrive gently" — no sudden appearances, everything fades in softly
2. "Breathe, don't bounce" — organic ease-in-out, no spring overshoots
3. "Guide, don't distract" — motion directs attention, never competes with content
4. "Calm in, calm out" — entrances and exits use the same soothing curve
5. "Pulse with care" — loading states use slow, gentle pulses, not spinners
```

## Workflow

1. **Brand Context**: Analyze brand personality and industry motion profile
2. **Motion Personality**: Define energy level and motion principles
3. **Token System**: Create easing curves and duration scale
4. **Pattern Library**: Define micro-interaction patterns
5. **Logo Animation**: Design logo reveal and transition specs
6. **Guidelines Document**: Compile into motion section of brand guide

## Output Deliverables

| Deliverable | Format | Purpose |
|-------------|--------|---------|
| Motion Guidelines | HTML | Animation rules and principles |
| Motion Tokens | JSON | Machine-readable timing/easing tokens |
| Pattern Library | SVG/CSS | Code-ready animation examples |
| Logo Animation Spec | SVG/JSON | Logo motion specification |

## CSS Variable Output

```css
:root {
  --ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
  --ease-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1);
  --ease-spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --duration-micro: 150ms;
  --duration-short: 200ms;
  --duration-standard: 300ms;
  --duration-long: 500ms;
  --duration-expressive: 800ms;
}
```
