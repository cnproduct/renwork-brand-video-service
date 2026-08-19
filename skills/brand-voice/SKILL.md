---
name: "brand-voice"
description: "Generates brand voice, tone guidelines, and messaging frameworks. Invoke when user needs brand personality definition, tone of voice guide, tagline creation, or copywriting style rules."
---

# Brand Voice

A brand language and messaging skill that defines how a brand speaks across all touchpoints — from taglines to error messages — ensuring verbal consistency that matches the visual identity.

## Core Capabilities

### 1. Brand Personality Definition
- Map brand attributes to the 5-dimension personality model (Sincerity, Excitement, Competence, Sophistication, Rurality)
- Define brand archetype (Creator, Caregiver, Ruler, Jester, Sage, Innocent, Explorer, Outlaw, Magician, Hero, Lover, Everyman)
- Create a personality spectrum: where the brand sits on formal↔casual, serious↔playful, technical↔accessible axes

### 2. Tone of Voice Guidelines
- Generate a tone guide with "We sound like / We don't sound like" comparisons
- Create do/don't word lists with specific examples
- Define tone modulation by context (social media vs. documentation vs. error messages)
- Provide before/after copy examples for each touchpoint

### 3. Messaging Framework
- Brand promise (one sentence)
- Value proposition (elevator pitch)
- Supporting messages (3 key pillars)
- Proof points for each pillar
- Tagline options (3-5 directions)

### 4. Copywriting Style Rules
- Sentence length guidelines (min/max/average)
- Vocabulary level and reading difficulty target
- Active vs passive voice preference
- Emoji usage policy
- Capitalization and punctuation rules
- Industry-specific terminology glossary (preferred terms vs. avoided terms)

## Industry Voice Adaptation

| Industry | Voice Character | Vocabulary Level | Example Tone |
|----------|----------------|-----------------|--------------|
| Tech/SaaS | Confident, clear, jargon-aware | Professional but accessible | "Ship faster. Sleep better." |
| Finance | Authoritative, measured, transparent | Professional, precise | "Your wealth, built to last." |
| Healthcare | Empathetic, reassuring, clear | Plain language, 8th grade | "Care that listens." |
| Food & Beverage | Warm, sensory, inviting | Sensory, emotional | "Taste the moment." |
| Fashion | Aspirational, editorial, confident | Sophisticated, evocative | "Wear your story." |
| Education | Inspiring, clear, encouraging | Accessible, motivating | "Learn without limits." |
| Hospitality | Warm, welcoming, gracious | Warm, inviting | "Your home, away from home." |

## Workflow

1. **Brand Audit**: Review brand name, industry, target audience, and visual personality
2. **Personality Mapping**: Define brand archetype and personality dimensions
3. **Voice Definition**: Create the voice guide with do/don't examples
4. **Messaging Architecture**: Build the message house (promise → pillars → proof)
5. **Touchpoint Copy**: Generate sample copy for key touchpoints (website hero, about, social bio, error states)
6. **Voice Tokens**: Output machine-readable voice guidelines for consistency checking

## Output Deliverables

| Deliverable | Format | Purpose |
|-------------|--------|---------|
| Voice Guide | HTML | Comprehensive tone and voice document |
| Message House | JSON | Structured messaging architecture |
| Copy Samples | Text | Example copy for key touchpoints |
| Voice Tokens | JSON | Machine-readable style rules |
| Glossary | JSON | Preferred/avoided terminology |

## Voice Token Structure

```json
{
  "personality": {
    "archetype": "Creator",
    "dimensions": { "sincerity": 0.7, "excitement": 0.8, "competence": 0.9 },
    "formality": 0.3,
    "playfulness": 0.6
  },
  "rules": {
    "sentence_length": { "min": 5, "max": 20, "average": 12 },
    "reading_level": "8th grade",
    "voice": "active",
    "emoji_policy": "sparingly, never in error messages"
  },
  "vocabulary": {
    "preferred": ["empower", "simple", "fast"],
    "avoided": ["leverage", "synergy", "utilize"]
  }
}
```
