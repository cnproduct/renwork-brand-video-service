---
name: "skill-finder"
description: "AI-powered skill discovery tool that automatically searches and matches extension skills to tasks. Invoke when user needs to find a skill for a specific task or wants to discover available capabilities."
---

# Skill Finder (找Skill的Skill)

An AI-driven skill discovery and matching skill that automatically retrieves and recommends the most relevant skills for any given task, ensuring users always leverage the right tools.

## Core Capabilities

### 1. Automatic Skill Retrieval
- Scan all installed skills in `.trae/skills/` and global skill directories
- Parse each skill's `SKILL.md` frontmatter (name, description) and body content
- Build an in-memory index of skill capabilities and trigger conditions
- Match task descriptions against skill descriptions using semantic similarity

### 2. Task-to-Skill Matching
- Accept a natural language task description as input
- Analyze task intent, required capabilities, and context
- Rank candidate skills by relevance score
- Return top matches with confidence scores and usage rationale

### 3. Skill Gap Detection
- Identify tasks that no existing skill covers
- Recommend creating new skills for uncovered capabilities
- Suggest skill names and descriptions based on the gap analysis

### 4. Skill Chain Recommendations
- For complex multi-step tasks, recommend a sequence of skills to chain
- Identify skill dependencies and execution order
- Suggest data handoff formats between chained skills

## Matching Algorithm

```
1. Extract keywords and intent from task description
2. Score each skill:
   - Description match (weight: 40%)
   - Capability keyword match (weight: 30%)
   - Trigger condition match (weight: 20%)
   - Recency/usage frequency (weight: 10%)
3. Return skills with score > 0.5, sorted descending
```

## Workflow

1. **Index Skills**: Scan and parse all available `SKILL.md` files
2. **Analyze Task**: Extract intent, capabilities needed, and constraints
3. **Match & Rank**: Score all skills against the task
4. **Recommend**: Return top 3-5 matches with rationale
5. **Gap Check**: If no good match, suggest new skill creation

## Discovery Sources

| Source | Path | Scope |
|--------|------|-------|
| Project skills | `.trae/skills/*/SKILL.md` | Current project |
| Global skills | `~/.trae-cn/builtin/global/skills/*/SKILL.md` | All projects |
| Plugin skills | `~/.trae-cn/plugins/*/skills/*/SKILL.md` | Plugin-provided |

## Output Format

```
Recommended Skills for: "<task description>"

1. [skill-name] (score: 0.95)
   Why: <one-sentence rationale>
   Invoke: <how to trigger this skill>

2. [skill-name] (score: 0.82)
   Why: <one-sentence rationale>
   Invoke: <how to trigger this skill>

Skill Chain Suggestion:
  Step 1: skill-a → <output>
  Step 2: skill-b → <output>
  Step 3: skill-c → <final output>
```

## Best Practices
- **Be specific in task descriptions**: More context yields better matches
- **Chain skills for complex workflows**: Don't expect one skill to do everything
- **Create skills for gaps**: If no match, use `skill-creator` to fill the gap
- **Keep descriptions updated**: Stale skill descriptions lead to poor matches
