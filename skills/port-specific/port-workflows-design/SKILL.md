---
name: port-workflows-design
description: Build horizontal, agentic-workflow diagram slides in Port's Anchor visual language. Use this whenever you need to visualize step-by-step automated processes (ticket → agent → human approval → agent → merge, incident → triage → investigation, request → provisioning, etc.) as a clean, professional workflow diagram. Triggers include workflow visualization, agentic process flows, automation pipelines, orchestration diagrams, or any multi-step agent/system interaction that needs a visual narrative.
---

# Skill: Port Workflow Diagrams

Use this to build a horizontal, agentic-workflow diagram slide in Port's Anchor visual language (see `tad Workflow Diagram.dc.html`, `SRE Agent Workflow Diagram.dc.html`, `Cloud IaC Workflow Diagram.dc.html` for reference builds).

## When to use
Any time you need to show a step-by-step automated/agentic process (ticket → agent → human approval → agent → merge, incident → triage → investigation, request → provisioning, etc.) as a single clean slide.

## Frame
- Fixed slide canvas: `1280x720`, centered content, `padding: 64px 72px`.
- White background (`--anchor-background-primary`), no gradients, no heavy borders.
- Load the Port Anchor bundle (`colors_and_type.css`, `styles.css`, `_ds_bundle.js`) and use `var(--anchor-*)` tokens only — never invent colors.

## Title
- Top-left aligned (not centered) — big and bold: `font-size: 40px; font-weight: 500`.
- If a customer/brand co-owns the story, put their logo to the RIGHT of the title text with a thin 1px vertical divider between them (`height ~76px`), both vertically centered as one row. Size the logo so it reads as visually equal in weight to the title (~72–90px tall) — don't shrink it into an afterthought.
- No subtitle needed once the diagram is legible on its own; keep copy minimal.

## Main flow (any number of steps, left to right)
- CSS grid: alternating fixed node columns (`~130-150px`) and flexible arrow columns (`1fr`) — for N steps, that's `2N-1` grid columns (node, arrow, node, arrow, … node). Add/remove node+arrow pairs freely; the pattern doesn't assume a fixed count.
- If the step count makes tiles feel cramped at 1280px width, shrink node column width slightly (down to ~110px) and/or tile size (down to ~56px) before adding a second row — keep everything on one row/one arrow chain if at all possible, since that's the core visual signature.
- Each node: a `64x64px` rounded-square tile (`border-radius: var(--radius)`), 1px `var(--anchor-border-low)` border, `box-shadow: var(--shadow-card)`. Icon centered inside, ~27-30px.
  - Tile background = tinted categorical low color that matches the actor: `--anchor-purple-low` for AI/agent steps (starburst/sparkle glyph in `--anchor-purple-high`), `--anchor-green-low` for Port-logo steps, plain white for third-party logos (GitHub, Slack, Cursor, ServiceNow, etc. — full-color brand marks, never re-tinted).
- Step title sits ABOVE the tile, dark gray (`--anchor-text-high`), 13px/500, center-aligned, in a fixed-height wrapper so multi-line titles keep tiles aligned.
- Optional small caption BELOW a tile (10px, `--anchor-text-medium`) for a clarifying detail (e.g. "Entity created — status 'In Progress'").
- Arrows between nodes: a thin horizontal line (`1.5px`, `--anchor-border-high`) with a small solid triangular arrowhead at the end, vertically centered on the tile row (not the label row).

## Context Lake sub-blocks
- Hang below any step where the agent pulls/pushes context (usually the agent steps) — zero, one, or several per diagram, each anchored under its own node's grid column.
- Thin vertical line + small downward triangle arrow dropping from the tile.
- Small white card below (`~210-250px` wide), same tile border/shadow style: Port logo + "Context Lake" (13px/500), then "Semantic Layer + MCP" (11px, `--anchor-text-medium`), then a row of small (16-18px) provider logos with an optional one-line caption (10px, `--anchor-text-low`) describing what's read/written.

## Human-in-the-loop
- Prefer showing this implicitly via the step itself (e.g. a "Human review & approval" or "Request recorded in Port" step) rather than a separate floating pill+arrow annotation — it reads as cleaner and less redundant.

## Icons
- Use official brand marks (GitHub, Slack, Jira, ServiceNow, Cursor, AWS, Kubernetes, Grafana, New Relic, GitLab) — real logo art, not re-colored generic shapes. Ask the user for the exact logo file if one isn't already in `assets/`.
- Port logo: the green/black glyph, `currentColor`-able, from `assets/port-logo.svg`.
- Agent/AI steps: a purple starburst/sparkle glyph (no vendor logo — represents the LangGraph/planning agent generically).

## Orchestration line (optional)
- A full-width label under the flow ("Port — orchestration, MCP context, Slack updates, human approvals") can be added, but this project ultimately removed it as visual clutter — default to leaving it OUT unless asked for.

## Build steps
1. `dc_write` a new `<Name> Workflow Diagram.dc.html`, set `d_props_json` to `{"$preview":{"width":1280,"height":720}}`.
2. Copy any missing brand assets into `assets/` before referencing them.
3. Compose title row → main stage grid → Context Lake grid, reusing the exact inline-style values above so all workflow diagrams in the deck feel identical.