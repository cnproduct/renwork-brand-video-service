---
name: "brandvision"
description: "Master brand design orchestrator combining industry adaptation, logo creation, brand system packaging, voice, imagery, motion, consistency control, and scene delivery. Invoke when user needs brand identity design, visual system, or complete brand workflow for any industry."
---

# BrandVision

A master orchestrator that unifies the complete brand design pipeline — from industry analysis to final delivery — by coordinating 11 specialized sub-skills into a seamless AI-driven workflow. Auto-adapts to different industries with pre-built visual system profiles.

## Philosophy

BrandVision treats brand design as systems engineering: every asset must be consistent, every decision must be traceable to a design token, and every output must be production-ready. The orchestrator ensures no step is skipped, no inconsistency slips through, and the visual system automatically matches the target industry's conventions while enabling strategic differentiation.

## Sub-Skill Architecture (11 Skills)

```
                         ┌─────────────────────┐
                         │    brandvision      │  ← Master Orchestrator
                         │    (this skill)     │
                         └──────────┬──────────┘
                                    │
          ┌─────────────────────────┼──────────────────────────┐
          │                         │                          │
          ▼                         ▼                          ▼
  ┌──────────────────┐    ┌──────────────────┐      ┌──────────────────┐
  │industry-brand-   │    │  skill-finder    │      │   svg-logo-      │
  │adapt              │    │  需求分析/匹配    │      │   designer       │
  │行业自适应(Phase 0)│    │                  │      │   图形生成        │
  └──────────────────┘    └──────────────────┘      └──────────────────┘
          │                                                    │
          │              ┌─────────────────────────────────────┘
          │              │
          │              ▼
          │     ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
          │     │    brandkit      │  │  brand-voice     │  │  brand-imagery   │
          │     │  品牌系统包装     │  │  品牌语调与口吻   │  │  品牌图像方向     │
          │     └──────────────────┘  └──────────────────┘  └──────────────────┘
          │              │                    │                    │
          │              └────────────────────┼────────────────────┘
          │                                   │
          │              ┌────────────────────┘
          │              │
          │              ▼
          │     ┌──────────────────┐  ┌──────────────────┐
          │     │  brand-motion    │  │    cc-design     │
          │     │  品牌动效规范     │  │  一致性管控       │
          │     └──────────────────┘  └──────────────────┘
          │                                   │
          └───────────────────────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   figma-tools    │
                     │  源文件/场景落地   │
                     └──────────────────┘
```

## Full Workflow Pipeline (7 Phases)

### Phase 0: Industry Adaptation
**Skill:** `industry-brand-adapt`
- Parse user's brand description to identify the target industry
- Load the matching industry profile (10+ pre-built profiles)
- Auto-configure: color palette, typography, imagery style, tone, motion, iconography, accessibility level
- Run competitor color analysis and suggest differentiation strategy
- Output: Industry-specific `design-tokens.json` as the foundation for all downstream phases

**Supported Industries:** Tech/SaaS, Food & Beverage, Fashion/Retail, Finance/Fintech, Healthcare, Education, Hospitality, Real Estate, Entertainment, Beauty/Cosmetics

### Phase 1: Discovery & Research
**Skills:** `skill-finder` + `research-guide` (if available)
- Analyze full brand requirements (name, industry, personality, audience, competitors)
- Match the task to the right combination of sub-skills
- Research competitor visual systems and market positioning
- Identify capability gaps and plan the workflow
- Output: A skill execution plan with ordered steps and research brief

### Phase 2: Logo Creation
**Skill:** `svg-logo-designer`
- Generate 3-5 logo concept directions as SVG, constrained by industry color palette from Phase 0
- Refine the chosen direction with optimized outlines
- Test negative space and black-white inversion
- Verify 32px small-size recognizability
- Output: Editable SVG logo with variants (full color, monochrome, reversed, small mark)

### Phase 3: Brand System Packaging
**Skills:** `brandkit` + `brand-voice` + `brand-imagery` + `brand-motion` (parallel)
- **brandkit**: Color palette, typography scale, spacing system, logo usage rules, application mockups
- **brand-voice**: Brand personality, tone of voice guide, messaging framework, copywriting rules
- **brand-imagery**: Photography direction, illustration style, icon system, mood board prompts
- **brand-motion**: Animation curves, timing system, micro-interaction patterns, logo animation spec
- All four run in parallel, each consuming the industry tokens from Phase 0
- Output: Complete brand guide + voice guide + imagery guide + motion guide + all token files

### Phase 4: Consistency Control
**Skill:** `cc-design`
- Define master design language from Phase 3 outputs
- Consolidate all token files (color, typography, voice, imagery, motion) into a unified `design-tokens.json`
- Audit ALL assets (SVG logos, HTML guides, mockups, copy samples) against tokens
- Fix violations and re-validate
- Output: Consistency report + locked master token file

### Phase 5: Scene Delivery
**Skills:** `figma-tools` + `frontend-design-deslop` (if available)
- Apply brand system to Figma source files (if applicable)
- Use `frontend-design-deslop` to ensure web/UI applications have distinctive, non-generic design that matches brand personality
- Export assets at required resolutions
- Sync design tokens to code (CSS variables, Tailwind config)
- Output: Figma-updated files + branded UI + exported assets + code tokens

### Phase 6: Documentation & Presentation
**Skills:** `html-report` + `html-deck` (if available)
- Compile all brand guidelines into a professional HTML brand book
- Generate a brand proposal presentation deck
- Create downloadable asset package
- Output: Brand book HTML + presentation deck + asset bundle

## Enhanced Orchestration Rules

### When to Run Full Pipeline
Trigger the complete 7-phase pipeline when the user asks for:
- "为[行业]设计一个品牌" / "design a brand for [industry]"
- "完整的品牌视觉系统" / "complete visual identity system"
- "从Logo到应用的全套品牌设计" / "full brand design from logo to applications"
- Any request mentioning an industry + brand/design/visual

### When to Run Partial Pipeline
| Request Type | Phases | Skills Used |
|-------------|--------|-------------|
| Industry analysis only | Phase 0 | `industry-brand-adapt` |
| Logo only (industry known) | Phase 0 + 2 | `industry-brand-adapt` → `svg-logo-designer` |
| Brand guide only (logo exists) | Phase 0 + 3 + 4 | `industry-brand-adapt` → `brandkit`+`brand-voice`+`brand-imagery`+`brand-motion` → `cc-design` |
| Consistency audit only | Phase 4 | `cc-design` |
| Figma editing only | Phase 5 | `figma-tools` |
| Find the right skill | Phase 1 | `skill-finder` |
| Brand voice only | Phase 0 + 3 (voice) | `industry-brand-adapt` → `brand-voice` |
| Motion design only | Phase 0 + 3 (motion) | `industry-brand-adapt` → `brand-motion` |

### Industry Auto-Detection
When the user mentions an industry keyword, BrandVision auto-routes to Phase 0:

| Keyword Triggers | Industry Profile |
|-----------------|-----------------|
| 科技/技术/SaaS/software/app | Tech/SaaS |
| 餐饮/食品/咖啡/restaurant/food | Food & Beverage |
| 时尚/服装/零售/fashion/retail | Fashion/Retail |
| 金融/银行/保险/finance/bank/fintech | Finance/Fintech |
| 医疗/健康/医院/healthcare/medical | Healthcare |
| 教育/培训/学校/education/learning | Education |
| 酒店/旅游/hospitality/hotel | Hospitality |
| 房地产/物业/real estate/property | Real Estate |
| 娱乐/影视/游戏/entertainment/gaming | Entertainment |
| 美容/化妆/beauty/cosmetics | Beauty/Cosmetics |

### Data Handoff Between Phases
| From → To | Handoff Artifact |
|-----------|-----------------|
| Phase 0 → Phase 2 | Industry design tokens (color constraints, typography) |
| Phase 0 → Phase 3 | Industry tokens (all 10 dimensions) |
| Phase 0 → Phase 4 | Accessibility level, audit baseline |
| Phase 1 → Phase 2 | Requirements brief + competitor analysis |
| Phase 2 → Phase 3 | SVG logo files + variant set |
| Phase 3 → Phase 4 | Brand guide + voice guide + imagery guide + motion guide + all tokens |
| Phase 4 → Phase 5 | Locked master token file + audited asset list |
| Phase 5 → Phase 6 | Final assets + branded UI + code tokens |

## Quick Start Decision Tree

```
User Request
    │
    ├─ Mentions industry? ──Yes──→ Phase 0 (industry-brand-adapt)
    │       │                          │
    │       No                         ▼
    │       │                  Has existing logo?
    │       ▼                  │
    │  Run Phase 1         ──No──→ Phase 2 (svg-logo-designer)
    │  (skill-finder)          │
    │       │                  Yes
    │       ▼                  ▼
    │  Needs full system? ──Yes──→ Phase 3 (brandkit + voice + imagery + motion)
    │       │                       │
    │       No                      ▼
    │       ▼                  Phase 4 (cc-design audit)
    │  Run specific skill          │
    │                              ▼
    │                  Needs delivery? ──Yes──→ Phase 5 + Phase 6
    │                                      │
    │                                      No
    │                                      ▼
    └────────────────────────── Deliver brand guide + tokens
```

## Sub-Skill Reference (11 Skills)

| Skill | Phase | Role | Key Output |
|-------|-------|------|------------|
| `industry-brand-adapt` | 0 | Industry-specific visual system auto-adaptation | Industry design tokens JSON |
| `skill-finder` | 1 | Requirements analysis & skill matching | Execution plan |
| `svg-logo-designer` | 2 | Vector logo creation | Editable SVG + variants |
| `brandkit` | 3 | Brand system packaging (color/type/spacing) | HTML brand guide + tokens |
| `brand-voice` | 3 | Brand voice, tone & messaging | Voice guide + message house |
| `brand-imagery` | 3 | Photography, illustration & icon direction | Imagery guide + mood prompts |
| `brand-motion` | 3 | Motion design & micro-interaction specs | Motion tokens + pattern library |
| `cc-design` | 4 | Design consistency control & auditing | Audit report + locked tokens |
| `figma-tools` | 5 | Figma source file editing & asset export | Updated Figma + exported assets |
| `frontend-design-deslop` | 5 | Non-generic, brand-distinctive UI design | Branded web/UI (runtime skill) |
| `html-report` + `html-deck` | 6 | Documentation & presentation | Brand book + presentation deck |

## System Skill Integration (Runtime)

BrandVision also leverages these system-level skills when available at runtime:

| System Skill | Usage in Pipeline |
|---------------|------------------|
| `dynamic-ui` | Inline visual comparison of logo directions, color ratios, audit results |
| `research-guide` | Structured competitor and market research in Phase 1 |
| `frontend-design-deslop` | Ensuring web applications have distinctive brand personality in Phase 5 |
| `html-report` | Generating the final brand guideline document in Phase 6 |
| `html-deck` | Generating brand proposal presentations in Phase 6 |
| `doc-writing-guide` | Standardizing brand guide document writing |
| `TRAE-code-mode-orchestrator` | Parallel execution of Phase 3 sub-skills and batch auditing in Phase 4 |

## Token Architecture

All phases produce and consume a unified token structure:

```json
{
  "industry": "healthcare",
  "color": { "primary": "#2A9D8F", "secondary": "#A8DADC", "neutral": {} },
  "typography": { "heading": {}, "body": {} },
  "spacing": { "base": 4, "scale": [4, 8, 12, 16, 24, 32, 48, 64] },
  "radius": { "sm": 4, "md": 8, "lg": 16 },
  "voice": { "archetype": "Caregiver", "formality": 0.3, "rules": {} },
  "imagery": { "photography": {}, "illustration": {}, "icons": {} },
  "motion": { "easing": {}, "duration": {}, "patterns": {} },
  "accessibility": { "level": "AAA", "min_contrast": 7.0, "min_font_size": 16 }
}
```

## Naming Convention for Deliverables
```
{brand-name}_industry_profile.json
{brand-name}_logo_primary.svg
{brand-name}_logo_monochrome.svg
{brand-name}_logo_reversed.svg
{brand-name}_logo_smallmark.svg
{brand-name}_brand_guide.html
{brand-name}_voice_guide.html
{brand-name}_imagery_guide.html
{brand-name}_motion_guide.html
{brand-name}_design_tokens.json
{brand-name}_app_icon.svg
{brand-name}_scene_{context}.svg
{brand-name}_presentation.html
```

## Best Practices
- **Always start with Phase 0** for industry-specific requests — it sets the foundation for everything
- **Run Phase 3 sub-skills in parallel** — brandkit, brand-voice, brand-imagery, brand-motion are independent
- **Never skip Phase 4** (cc-design) — consistency is the most common failure point
- **Deliver tokens, not just visuals** — machine-readable JSON enables developer handoff
- **Test at 32px early** — a logo that fails at small size must be redesigned, not patched
- **Respect industry conventions but enable differentiation** — follow the 80/20 rule (80% industry-appropriate, 20% distinctive)
- **Document every decision** — the brand guide must explain WHY, not just WHAT
- **Accessibility is non-negotiable for medical/education** — auto-enforce WCAG AAA
