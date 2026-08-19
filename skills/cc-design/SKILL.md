---
name: "cc-design"
description: "Controls overall design language consistency across projects and deliverables. Invoke when user needs to enforce brand consistency, audit design adherence, or unify visual style across assets."
---

# CC Design (Consistency Controller)

A design governance skill that ensures visual and brand consistency across all design outputs — logos, mockups, documents, and code — by maintaining a single source of truth for design language.

## Core Capabilities

### 1. Design Language Definition
- Define a master design language document covering color, typography, spacing, shape, motion
- Establish rules for composition, hierarchy, and visual rhythm
- Create reusable design patterns and component specifications
- Set quality gates: every asset must pass consistency checks before delivery

### 2. Cross-Asset Consistency Auditing
- Scan all SVG, HTML, and image assets against the master design language
- Detect color drift (off-palette colors), typography misuse, spacing violations
- Generate a consistency report with specific violations and fixes
- Flag assets that deviate from established brand guidelines

### 3. Design Token Management
- Maintain a central `design-tokens.json` as the single source of truth
- Tokens cover: colors, typography, spacing, radii, shadows, breakpoints
- Sync tokens across SVG files, HTML/CSS, and brand documents
- Version control token changes with semantic versioning

### 4. Unified Output Standards
- Enforce consistent file naming, folder structure, and export settings
- Standardize SVG structure (viewBox, grouping, naming conventions)
- Ensure all deliverables reference the same token definitions
- Generate a design QA checklist for each delivery milestone

## Consistency Check Rules

| Dimension | Rule | Detection Method |
|-----------|------|-----------------|
| Color | Must match palette tokens (±2% tolerance) | Hex comparison against tokens |
| Typography | Must use defined font families and sizes | Font-family and size audit |
| Spacing | Must follow modular scale (4px/8px base) | Layout measurement |
| Stroke | Consistent stroke weights per context | Path stroke-width audit |
| Corner Radius | Must use defined radius tokens | Shape rx/ry audit |
| Logo Usage | Clear space, min size, color rules met | Logo placement audit |

## Workflow

1. **Define Language**: Create or load master design language specification
2. **Generate Tokens**: Produce `design-tokens.json` from specification
3. **Audit Assets**: Scan all project assets against tokens
4. **Report & Fix**: Generate violations report; apply automated fixes where possible
5. **Validate**: Re-scan to confirm all issues resolved
6. **Lock**: Freeze the design language for the current project phase

## Design Token Structure

```json
{
  "color": {
    "primary": { "value": "#0066FF", "name": "Brand Blue" },
    "secondary": { "value": "#00C4B4", "name": "Accent Teal" },
    "neutral": {
      "gray-900": "#1A1A2E",
      "gray-600": "#6B7280",
      "gray-100": "#F3F4F6"
    }
  },
  "typography": {
    "heading": { "family": "Inter", "weight": 700, "sizes": [48, 36, 24, 20, 16] },
    "body": { "family": "Inter", "weight": 400, "sizes": [16, 14, 12] }
  },
  "spacing": { "base": 4, "scale": [4, 8, 12, 16, 24, 32, 48, 64] },
  "radius": { "sm": 4, "md": 8, "lg": 16, "full": 9999 }
}
```

## Best Practices
- **Single source of truth**: Never hardcode values — always reference tokens
- **Audit early, audit often**: Run consistency checks after every design iteration
- **Document exceptions**: If a deviation is intentional, document why
- **Automate where possible**: Use scripts to detect common violations
