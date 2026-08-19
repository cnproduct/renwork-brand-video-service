---
name: "svg-logo-designer"
description: "Specializes in vector logo design with graphic mark, wordmark, and lettermark exploration. Invoke when user needs a logo, brand mark, icon design, or editable SVG vector output."
---

# SVG Logo Designer

A professional vector logo design skill that generates clean, scalable SVG logos with full editability. Supports multiple logo directions and ensures production-ready output.

## Core Capabilities

### 1. Graphic Concept Generation & Outline Optimization
- Generate logo concepts based on brand name, industry, and personality keywords
- Explore multiple directions: geometric marks, abstract symbols, pictorial marks, monograms
- Optimize vector outlines for clean curves, proper proportions, and visual balance
- Use SVG primitives (`<path>`, `<circle>`, `<rect>`, `<polygon>`, `<g>`) to construct forms

### 2. Negative Space Handling & Black-White Inversion Testing
- Design with intentional negative space relationships (figure-ground)
- Test every logo in pure black on white AND white on black to verify legibility
- Ensure the logo works without gradients or color dependency
- Validate that negative space doesn't create unintended optical artifacts

### 3. Small-Size Recognizability Verification (32px)
- Render the logo at 32x32px, 16x16px, and favicon scale to verify recognizability
- Simplify detail at small sizes — remove strokes thinner than 2px, merge close elements
- Provide a simplified "small mark" variant if the full logo loses clarity
- Test against common background colors for contrast

### 4. Editable SVG Vector File Output
- Output well-structured, semantic SVG with named groups (`<g id="...">`)
- Use relative path coordinates for portability
- Include `<defs>` for reusable elements, gradients, and patterns
- Embed metadata: viewBox, title, desc for accessibility
- Avoid rasterized elements — everything must be pure vector

## Workflow

1. **Requirements Intake**: Collect brand name, tagline, industry, personality traits, color preferences, and reference styles
2. **Concept Exploration**: Generate 3-5 distinct logo directions as rough SVG sketches
3. **Refinement**: Develop the chosen direction with optimized outlines and proportions
4. **Negative Space Test**: Render black-on-white and white-on-black versions
5. **Small-Size Test**: Render at 32px and 16px; create simplified variant if needed
6. **Final Delivery**: Output clean, commented SVG with variants (full, monochrome, small)

## SVG Output Standards

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img">
  <title>Brand Name Logo</title>
  <desc>Brief description of the logo concept</desc>
  <defs>
    <!-- Reusable elements, gradients, patterns -->
  </defs>
  <g id="logo-mark">
    <!-- Vector paths -->
  </g>
  <g id="logo-text">
    <!-- Wordmark text as paths -->
  </g>
</svg>
```

## Design Principles
- **Simplicity**: Fewer elements = stronger recognition. Aim for 1-3 core shapes.
- **Scalability**: If it doesn't work at 32px, it's too complex.
- **Timelessness**: Avoid trends that date quickly. Focus on geometric fundamentals.
- **Versatility**: Must work in monochrome, reversed, and full color.

## Variants to Deliver
| Variant | Purpose |
|---------|---------|
| Full color | Primary brand usage |
| Monochrome (black) | Print, documents |
| Reversed (white) | Dark backgrounds |
| Small mark (32px optimized) | Favicon, app icon, avatar |
| Horizontal lockup | Headers, letterheads |
| Stacked lockup | Square contexts, social profiles |
