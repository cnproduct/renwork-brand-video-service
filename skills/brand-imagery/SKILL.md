---
name: "brand-imagery"
description: "Defines brand photography direction, illustration style, and visual mood guidelines. Invoke when user needs brand imagery guidelines, mood boards, photography direction, or illustration style specs."
---

# Brand Imagery

A visual direction skill that defines how a brand looks beyond its logo — photography style, illustration approach, icon system, and mood — ensuring every image reinforces the brand identity.

## Core Capabilities

### 1. Photography Direction
- Define photography style: editorial, lifestyle, product, architectural, abstract
- Specify lighting direction: natural, studio, dramatic, soft, high-key, low-key
- Set color treatment: vibrant, muted, monochrome, duotone, film grain
- Define composition rules: subject placement, depth of field, negative space
- Create mood board references with keyword descriptions for AI image generation

### 2. Illustration Style
- Define illustration approach: flat, isometric, line art, 3D, hand-drawn, abstract
- Specify color usage within illustrations (palette adherence)
- Set stroke weight, corner style, and detail level conventions
- Define character style guidelines (if applicable): proportions, expressions, diversity

### 3. Icon System Design
- Choose icon style: outline, filled, duotone, 3D
- Define stroke width, corner radius, and grid size
- Establish naming conventions and categorization
- Create usage rules: when to use icons vs. illustrations vs. photos

### 4. Image Treatment Rules
- Define overlay/gradient rules for text-on-image legibility
- Set aspect ratio standards for each platform (social, web, print)
- Establish cropping guidelines and focal point rules
- Create duotone/color overlay presets using brand colors

## Industry Imagery Adaptation

| Industry | Photography Style | Lighting | Color Treatment | Illustration |
|----------|------------------|----------|-----------------|-------------|
| Tech/SaaS | UI screenshots, collaboration scenes | Bright, clean | Vibrant, high contrast | Isometric, geometric |
| Food & Beverage | Food close-ups, steam/drip textures | Warm, appetizing | High saturation, warm tones | Playful, hand-drawn |
| Fashion | Editorial, model storytelling | Dramatic or soft beauty | Varies by segment | Minimal or none |
| Finance | Architecture, professional scenes | Even, professional | Muted, trustworthy | Data visualization |
| Healthcare | Real patient-doctor scenes, clean spaces | Soft, natural | Calming, cool tones | Friendly, rounded |
| Education | Learning scenes, diverse people | Bright, optimistic | Warm, encouraging | Friendly, colorful |
| Hospitality | Spaces, food, ambiance | Warm, inviting | Warm, rich tones | Elegant or none |
| Real Estate | Architecture, interiors, aerial | Natural, golden hour | Clean, premium | Minimal floor plans |

## Workflow

1. **Brand Context**: Analyze brand personality, industry, and target audience
2. **Photography Direction**: Define style, lighting, color treatment, composition
3. **Illustration Style**: Choose approach, define conventions
4. **Icon System**: Design icon style specifications
5. **Mood Board**: Generate AI image prompts for reference imagery
6. **Guidelines Document**: Compile into imagery section of brand guide

## AI Image Generation Prompts

Generate ready-to-use prompts for brand-consistent imagery:

```
Photography Prompt Template:
"[STYLE] photography of [SUBJECT], [LIGHTING] lighting, [COLOR_TREATMENT] color treatment,
[COMPOSITION] composition, [MOOD] mood, shot on [CAMERA/LENS],
brand colors: [PRIMARY_COLOR], [SECONDARY_COLOR]"

Example (Healthcare):
"Lifestyle photography of a doctor consulting with a patient in a modern clinic,
soft natural lighting, calming cool-toned color treatment,
medium shot with generous negative space, reassuring and professional mood,
shot on Canon EOS R5 50mm f/1.8, brand colors: #2A9D8F, #A8DADC"
```

## Output Deliverables

| Deliverable | Format | Purpose |
|-------------|--------|---------|
| Imagery Guidelines | HTML | Photography/illustration/icon rules |
| Mood Board Prompts | Text | AI image generation prompts |
| Icon Specifications | JSON | Icon system token definitions |
| Reference Grid | HTML | Visual examples by category |
| Image Tokens | JSON | Machine-readable style parameters |

## Image Token Structure

```json
{
  "photography": {
    "style": "lifestyle",
    "lighting": "soft natural",
    "color_treatment": "calming cool tones",
    "composition": "medium shot, generous negative space",
    "aspect_ratios": { "hero": "16:9", "social": "1:1", "card": "4:3" }
  },
  "illustration": {
    "style": "isometric geometric",
    "stroke_width": "2px",
    "corner_style": "rounded",
    "palette_adherence": "strict"
  },
  "icons": {
    "style": "outline",
    "stroke_width": "1.5px",
    "grid": "24x24",
    "corner_radius": "2px"
  }
}
```
