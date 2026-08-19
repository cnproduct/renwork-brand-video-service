---
name: "figma-tools"
description: "Directly modifies Figma source files while preserving vector editability. Invoke when user needs to edit Figma designs programmatically, export assets, or sync design tokens."
---

# Figma Tools

A skill for programmatically interacting with Figma files — modifying source designs, extracting assets, and preserving full vector editability throughout the workflow.

## Core Capabilities

### 1. Source File Modification
- Read and parse Figma file structure via Figma REST API
- Modify component properties, styles, and layout
- Create new frames, components, and instances
- Update text content, colors, and effects programmatically

### 2. Vector Editability Preservation
- All modifications preserve Figma's native vector structure (no flattening)
- Maintain component instances and auto-layout relationships
- Keep layers, groups, and boolean operations intact
- Preserve design tokens (color styles, text styles, effect styles)

### 3. Asset Export
- Export nodes as SVG, PNG, PDF at specified scales
- Batch export with consistent naming conventions
- Export design tokens as JSON for developer handoff

### 4. Design Token Sync
- Extract color styles, text styles, and spacing tokens from Figma
- Sync tokens between Figma and code (CSS variables, Tailwind config, etc.)
- Detect and report token drift between design and implementation

## Prerequisites
- Figma Personal Access Token (required for API access)
- File key from the target Figma file URL

## API Endpoints Used
| Endpoint | Purpose |
|----------|---------|
| `GET /v1/files/:file_key` | Read full file structure |
| `GET /v1/images/:file_key` | Export nodes as images |
| `GET /v1/file_components/:file_key` | List components |
| `GET /v1/file_styles/:file_key` | List styles |
| `POST /v1/files/:file_key/variables` | Write variables (requires Pro tier) |

## Workflow

1. **Authenticate**: Validate Figma token and file access
2. **Read Structure**: Fetch file JSON and parse node tree
3. **Identify Targets**: Locate nodes to modify by name or ID
4. **Apply Changes**: Modify properties while preserving structure
5. **Export**: Generate required output formats
6. **Verify**: Confirm changes in Figma and validate vector integrity

## Best Practices
- Always read the current file state before modifying
- Use node IDs for precise targeting (names can be ambiguous)
- Export at 1x, 2x, 4x for raster; 1x for vector
- Group related changes into single operations to minimize API calls
- Preserve component variants and properties
