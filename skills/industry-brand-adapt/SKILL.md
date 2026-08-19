---
name: "industry-brand-adapt"
description: "Auto-adapts brand visual systems to specific industries using pre-built industry profiles. Invoke when user needs industry-specific brand colors, typography, imagery style, or tone calibration for any sector."
---

# Industry Brand Adapt

An industry-specific brand adaptation engine that auto-configures design tokens, visual direction, and tone based on the target industry. Contains pre-built profiles for 10+ industries with color psychology, typography conventions, imagery direction, and accessibility constraints.

## Core Capabilities

### 1. Industry Profile Database
Each industry profile contains 10 adaptation dimensions:

| Dimension | Description |
|-----------|-------------|
| Color Palette | Primary/secondary/neutral colors based on industry color psychology |
| Typography | Font families, weights, serif vs sans-serif conventions |
| Imagery Style | Photography vs illustration, lighting, mood, composition |
| Layout Density | Whitespace ratio, grid density, information hierarchy |
| Tone of Voice | Formal/casual/technical/playful, do/don't word lists |
| Motion Language | Animation duration, easing curves, energy level |
| Iconography | Stroke vs filled, corner radius, visual weight |
| Packaging/Environmental | Material, unboxing flow, spatial signage |
| Component Defaults | Button/card/form styles per industry convention |
| Accessibility Level | WCAG contrast minimums, font readability requirements |

### 2. Color Psychology Mapping
Maps industry → dominant emotion → recommended color palette:

```
Finance → Trust/Authority → Deep Blue (#003F7F) + Neutral Gray
Food & Beverage → Appetite/Energy → Red (#E63946) + Warm Yellow (#F4A261)
Healthcare → Care/Calm → Green (#2A9D8F) + Soft Blue (#A8DADC)
Tech/SaaS → Innovation/Clarity → Blue (#0066FF) or Breakout Multi-color
Fashion/Retail → Aspiration/Identity → Varies by segment (see below)
Education → Growth/Inspiration → Blue + Green + Warm Accent
Beauty → Femininity/Purity → Soft Pink (#FFB7C5) + Neutral
Hospitality → Warmth/Welcome → Warm Earth Tones
Real Estate → Stability/Premium → Navy + Gold
Entertainment → Excitement/Creativity → High Saturation Multi-color
```

### 3. Differentiation Detection
- Auto-compares against industry color clustering (e.g., "finance is 80% blue")
- Suggests breakout strategies: complementary accent, unexpected neutral, or full rebellion
- Provides a "category map" showing where the brand sits relative to competitors

### 4. Accessibility Auto-Configuration
- Medical/Education industries: auto-enforce WCAG AAA contrast (7:1)
- Auto-select HHS-recommended accessible fonts (Arial, Helvetica, Tahoma, Verdana, Calibri)
- Enforce minimum body text size (16px for medical/education)

## Industry Profiles

### Tech / SaaS
```json
{
  "color": {
    "primary": "#0066FF",
    "secondary": "#00C4B4",
    "neutral": { "dark": "#1A1A2E", "mid": "#6B7280", "light": "#F3F4F6" },
    "breakout_options": ["Cavendish Yellow + Black", "Signature Green", "Multi-color"]
  },
  "typography": {
    "heading": { "family": "Inter/SF Pro", "weight": 700, "type": "sans-serif" },
    "body": { "family": "Inter/Roboto", "weight": 400, "type": "sans-serif" }
  },
  "imagery": "UI screenshots, isometric illustrations, abstract geometry, collaboration scenes",
  "layout": "Clean, generous whitespace, 12-column grid",
  "tone": "Concise, optimistic, functional",
  "motion": "Smooth micro-interactions, 200-300ms, ease-out",
  "iconography": "Linear, 2px stroke, minimal",
  "accessibility": "WCAG AA (4.5:1)"
}
```

### Food & Beverage
```json
{
  "color": {
    "primary": "#E63946",
    "secondary": "#F4A261",
    "neutral": { "dark": "#2D2D2D", "mid": "#8B7355", "light": "#FFF8F0" },
    "warning": "Avoid brown in food contexts (biological decay association)"
  },
  "typography": {
    "heading": { "family": "Rounded/Custom Display", "weight": 700, "type": "sans-serif" },
    "body": { "family": "Friendly Sans-serif", "weight": 400 }
  },
  "imagery": "High-saturation food close-ups, steam/drip textures, dining scenes",
  "layout": "Warm, appetite-driven, bold imagery",
  "tone": "Warm, immediate, appetizing",
  "motion": "Playful, bounce, 300-500ms",
  "packaging": "Core touchpoint — plan unboxing/material/information hierarchy",
  "accessibility": "WCAG AA (4.5:1)"
}
```

### Fashion / Retail
```json
{
  "color": {
    "luxury_segment": "Neutral palette — Black/White/Beige (#1A1A1A, #FFFFFF, #F5F0EB)",
    "fast_fashion": "Bold — Red/Yellow high energy",
    "beauty_segment": "Soft Pink + White (#FFB7C5, #FFFFFF)"
  },
  "typography": {
    "luxury": { "family": "Thin Serif Display", "weight": 300, "tracking": "wide" },
    "fast_fashion": { "family": "Bold Sans-serif", "weight": 800 },
    "beauty": { "family": "Elegant Serif/Sans hybrid", "weight": 400 }
  },
  "imagery": "Editorial photography, model storytelling, material detail shots",
  "layout": "Luxury: large whitespace, minimal; Retail: information-dense, promotional",
  "tone": "Luxury: restrained elegance; Retail: energetic, trend-driven",
  "environmental": "Storefront and window display are key brand carriers",
  "accessibility": "WCAG AA (4.5:1)"
}
```

### Finance / Fintech
```json
{
  "color": {
    "primary": "#003F7F",
    "secondary": "#1A1A2E",
    "neutral": { "dark": "#0D1B2A", "mid": "#415A77", "light": "#E0E1DD" },
    "note": "Blue is industry consensus — differentiate via secondary/accent"
  },
  "typography": {
    "traditional": { "family": "Serif (Times/Garamond)", "weight": 600, "type": "serif" },
    "fintech": { "family": "Modern Sans-serif (Inter/DM Sans)", "weight": 600, "type": "sans-serif" }
  },
  "imagery": "Data visualizations, architecture, professional people scenes",
  "layout": "Structured, grid-heavy, authoritative",
  "tone": "Steady, trustworthy, restrained",
  "motion": "Subtle, professional, 150-250ms, ease-in-out",
  "accessibility": "WCAG AA+ (4.5:1 minimum, 7:1 for financial data)"
}
```

### Healthcare
```json
{
  "color": {
    "primary": "#2A9D8F",
    "secondary": "#A8DADC",
    "neutral": { "dark": "#1D3557", "mid": "#457B9D", "light": "#F1FAEE" },
    "sleep_wellness": "Cool, calming tones (Casper-style)"
  },
  "typography": {
    "heading": { "family": "Accessible Sans-serif (Arial/Helvetica/Calibri)", "weight": 600 },
    "body": { "family": "HHS-recommended (Tahoma/Verdana/Arial)", "weight": 400, "min_size": "16px" }
  },
  "imagery": "Real doctor-patient scenes, clean environments, soft lighting",
  "layout": "Clean, calming, generous whitespace",
  "tone": "Caring, trustworthy, calm, professional",
  "motion": "Gentle, soothing, 400-600ms, ease-in-out",
  "accessibility": "WCAG AAA (7:1) — highest priority",
  "iconography": "Rounded, filled, friendly"
}
```

### Education
```json
{
  "color": {
    "primary": "#0066FF",
    "secondary": "#2A9D8F",
    "accent": "#F4A261",
    "children_segment": "High-saturation multi-color"
  },
  "typography": {
    "heading": { "family": "Friendly Sans-serif (Nunito/Poppins)", "weight": 700 },
    "body": { "family": "High-readability Sans-serif", "weight": 400, "min_size": "16px" }
  },
  "imagery": "Learning scenes, illustrations, people stories",
  "layout": "Clear hierarchy, scannable, age-appropriate density",
  "tone": "Inspiring, approachable, authoritative but warm",
  "motion": "Encouraging, celebratory micro-interactions",
  "accessibility": "WCAG AA+ (4.5:1, with 16px body minimum)"
}
```

### Hospitality
```json
{
  "color": {
    "primary": "#C77D4A",
    "secondary": "#5C4033",
    "neutral": { "dark": "#3E2723", "mid": "#8D6E63", "light": "#FFF8E1" }
  },
  "typography": { "heading": "Elegant Serif", "body": "Warm Sans-serif" },
  "imagery": "Inviting spaces, food, ambiance, people enjoying",
  "tone": "Warm, welcoming, hospitable"
}
```

### Real Estate
```json
{
  "color": {
    "primary": "#1B3A5F",
    "secondary": "#C5A572",
    "neutral": { "dark": "#1A1A2E", "mid": "#7B8794", "light": "#F5F5F5" }
  },
  "typography": { "heading": "Authoritative Serif", "body": "Clean Sans-serif" },
  "imagery": "Architecture, interiors, aerial views",
  "tone": "Stable, premium, trustworthy"
}
```

### Entertainment
```json
{
  "color": {
    "primary": "#6C2BD9",
    "secondary": "#FF006E",
    "accent": "#FFBE0B",
    "style": "High saturation, multi-color, bold contrasts"
  },
  "typography": { "heading": "Bold Display/Custom", "body": "Clean Sans-serif" },
  "imagery": "Dynamic, vibrant, performance/concert scenes",
  "tone": "Exciting, creative, bold"
}
```

### Beauty / Cosmetics
```json
{
  "color": {
    "primary": "#FFB7C5",
    "secondary": "#F8E5E0",
    "neutral": { "dark": "#2D2D2D", "mid": "#BFA8A8", "light": "#FFFFFF" },
    "natural_segment": "Earth tones, botanical greens"
  },
  "typography": { "heading": "Elegant Serif/Sans hybrid", "body": "Light Sans-serif" },
  "imagery": "Product close-ups, skin textures, soft beauty lighting",
  "tone": "Feminine, pure, aspirational",
  "packaging": "Core touchpoint — tactile materials, minimal labels"
}
```

## Workflow

1. **Identify Industry**: Parse user's brand description to determine industry
2. **Load Profile**: Select the matching industry profile from the database
3. **Customize**: Adjust profile parameters based on user's specific brand personality
4. **Differentiate**: Run competitor color analysis; suggest breakout strategy if needed
5. **Apply Accessibility**: Auto-configure WCAG level and font requirements
6. **Output Tokens**: Generate industry-specific `design-tokens.json` for downstream skills

## Integration with BrandVision
- Called in **Phase 0** (before logo creation) to establish industry-appropriate design parameters
- Output tokens feed into `svg-logo-designer` (color constraints), `brandkit` (full system), and `cc-design` (audit baseline)
- Enables one command like "为一家医疗科技公司设计品牌" to auto-configure the entire pipeline
