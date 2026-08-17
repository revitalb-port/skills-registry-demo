---
name: port-architecture-design
description: Build tech/system architecture diagram slides in Port's Anchor visual language. Use this whenever you need to visualize system topology — services, databases, queues, networks/VPCs, third-party tools, and how Port's Context Lake/Catalog integrates with a customer's or product's stack — as a clean, professional architecture slide (boxes, groupings, and connectors, NOT a step-by-step process flow). Triggers include architecture diagram, system diagram, integration diagram, "how does Port fit into our stack", reference architecture, technical topology, infra diagram, or any request to show what systems/services exist and how they connect. If the request is instead about a sequential agentic/automation process (ticket → agent → approval → merge), use port-workflows-design instead.
---

# Skill: Port Architecture Diagrams

Use this to build a system/tech architecture diagram slide in Port's Anchor visual language — the topology counterpart to `port-workflows-design`'s process-flow diagrams.

## When to use this vs. port-workflows-design

- **This skill (architecture)**: "what exists and how is it connected" — services, databases, networks, Port's Catalog/Context Lake, third-party tools, showing structure/topology at a point in time. Layout is spatial (grouped boxes, containment, connectors going any direction), not a left-to-right sequence.
- **port-workflows-design**: "what happens, in order" — a ticket becomes an agent action becomes a human approval becomes a merge. Layout is a strict horizontal step chain.
- If a request has both (e.g. "show our architecture AND the agent workflow that runs on top of it"), build two slides, one per skill, rather than merging conventions.

## ⚠️ Verify against the real Anchor bundle before building

This skill's visual spec is extrapolated from `port-workflows-design`'s documented tokens and conventions (`port-workflows-design/SKILL.md`), since no architecture-specific `.dc.html` reference build or the live `colors_and_type.css` / `styles.css` / `_ds_bundle.js` files were available when this skill was authored. Before the first real build:
1. Load the actual Anchor bundle (`colors_and_type.css`, `styles.css`, `_ds_bundle.js`) and confirm the token names below exist and resolve as expected (`--anchor-background-primary`, `--anchor-border-low`, `--anchor-border-high`, `--anchor-text-high/medium/low`, `--anchor-purple-low/high`, `--anchor-green-low`, `--radius`, `--shadow-card`).
2. If any token differs or an architecture-specific reference build (e.g. `*.Architecture Diagram.dc.html`) exists in the project, prefer that over this document and update this SKILL.md to cite it directly, the way `port-workflows-design` cites its three reference builds.
3. Flag to the user that this check happened, briefly — don't silently assume the tokens matched.

## Frame

- Fixed slide canvas: `1280x720`, centered content, `padding: 64px 72px`.
- White background (`--anchor-background-primary`), no gradients, no heavy borders.
- Load the Port Anchor bundle and use `var(--anchor-*)` tokens only — never invent colors.

## Title

- Top-left aligned (not centered), big and bold: `font-size: 40px; font-weight: 500`.
- If a customer/brand co-owns the diagram, put their logo to the RIGHT of the title text with a thin 1px vertical divider between them (`height ~76px`), both vertically centered as one row, logo sized to ~72–90px tall so it reads as visually equal in weight to the title.
- Optional one-line subtitle below the title (14px, `--anchor-text-medium`) only if the diagram needs a scoping statement (e.g. "Production environment — us-east-1"). Otherwise omit; keep copy minimal and let the diagram speak.

## Layout model (spatial, not sequential)

Architecture diagrams are laid out as **nested/grouped regions with a free-form connector graph**, not a fixed grid of columns:

- **Zones**: large rounded-rect containers representing a boundary — a VPC, a customer's cloud account, "Customer Environment" vs. "Port Cloud", a Kubernetes cluster, etc. Zone border: 1px dashed `var(--anchor-border-low)`, `border-radius: var(--radius)`, no fill or a very faint tint. Zone label sits in the top-left corner of the zone, 12px/500, `--anchor-text-medium`, uppercase with slight letter-spacing (~0.04em) to read as a category label rather than a node title.
- **Nodes**: individual services/systems live inside zones (or standalone if they belong to no zone — e.g. an external SaaS tool). Use the same node styling as the workflow skill for consistency:
  - `64x64px` rounded-square tile (`border-radius: var(--radius)`), 1px `var(--anchor-border-low)` border, `box-shadow: var(--shadow-card)`.
  - Icon centered inside, ~27–30px.
  - Tile background = tinted categorical low color matching the actor type: `--anchor-purple-low` for AI/agent components (starburst glyph in `--anchor-purple-high`), `--anchor-green-low` for Port components (Catalog, Context Lake, orchestration), plain white for third-party logos (AWS, Kubernetes, Datadog, GitHub, Snowflake, etc. — full-color brand marks, never re-tinted).
  - Node title sits ABOVE or BELOW the tile depending on layout density (above by default, matching the workflow skill), 13px/500, `--anchor-text-high`, center-aligned in a fixed-height wrapper.
  - Optional small caption (10px, `--anchor-text-medium`) for a clarifying detail (e.g. "reads via MCP", "webhook on merge").
- **Grouping without a full zone**: when several nodes belong together but don't need a heavy boundary (e.g. "observability tools"), use a lighter dashed-line cluster or simply tighter spacing plus a shared small caption underneath, rather than a full zone box — reserve zones for real security/network/account boundaries.

### Sizing and density

- Default grid: think in terms of a loose 12-column canvas within the padded content area; snap zones and nodes to that grid for alignment, but don't render grid lines.
- If more than ~12–14 nodes are needed, split across two zones side by side rather than shrinking tiles below ~48px — shrunk-below-48px tiles stop reading as tiles and start reading as clutter.
- Leave visible breathing room between zones (~32–40px gutters) — architecture diagrams read worse than workflow diagrams when cramped, since the eye has to trace connectors in multiple directions instead of one.

## Connectors

- Default connector: thin line (`1.5px`, `--anchor-border-high`), routed orthogonally (right-angle bends) rather than diagonally where possible — this is the main visual difference from the workflow skill's straight horizontal arrows, since architecture connectors commonly need to turn corners between zones.
- Arrowhead: small solid triangle at the receiving end. Use a double-ended arrow only when the relationship is genuinely bidirectional (e.g. sync read/write) — don't default to double-ended out of laziness.
- Label connectors sparingly and only when the relationship isn't obvious from the nodes themselves (e.g. "MCP", "webhook", "REST", "Kafka") — small text (10px, `--anchor-text-low`), centered on the line with a small white background cutout so the line doesn't visually cut through the label.
- Avoid crossing connectors where possible by reordering nodes within a zone; a small amount of crossing is acceptable in dense diagrams but should never exceed 2–3 crossings on one slide.

## Port's role in the diagram

- Represent Port as one or more `--anchor-green-low` tiles using the Port logo (`assets/port-logo.svg`), typically the Catalog/orchestration layer sitting either centrally (if Port is the integration hub) or clearly at one edge (if Port is one integration among many).
- If the diagram needs to show Port's Context Lake specifically, reuse the workflow skill's Context Lake sub-block convention: thin vertical line + small downward triangle, small white card (`~210–250px` wide, same tile border/shadow) with Port logo + "Context Lake" (13px/500), "Semantic Layer + MCP" (11px, `--anchor-text-medium`), then a row of small (16–18px) provider logos underneath.

## Icons

- Use official brand marks (AWS, GCP, Azure, Kubernetes, Docker, GitHub, GitLab, Datadog, New Relic, Grafana, Snowflake, Slack, ServiceNow, Jira, PagerDuty, etc.) — real logo art, not re-colored generic shapes. Ask the user for the exact logo file if one isn't already in `assets/`.
- Port logo: the green/black glyph, `currentColor`-able, from `assets/port-logo.svg`.
- Generic/unbranded components (e.g. "internal service", "custom microservice") get a plain neutral icon (box/server glyph) in `--anchor-text-medium`, not a brand mark.
- AI/agent components: the same purple starburst/sparkle glyph used in the workflow skill, for visual consistency across both diagram types.

## Legend (optional, use when zone/color meaning isn't self-evident)

- Small legend in the bottom-right or bottom-left corner: a short vertical list of swatch + label pairs (e.g. purple swatch → "AI/Agent", green swatch → "Port", dashed box → "Customer VPC"), 10px text, `--anchor-text-medium`.
- Only include this if the diagram has more than ~2 non-obvious visual conventions in play; skip it for simple diagrams to avoid clutter.

## Build steps

1. `dc_write` a new `<name> Architecture Diagram.dc.html`, set `d_props_json` to `{"$preview":{"width":1280,"height":720}}`.
2. Confirm/load the real Anchor bundle per the verification note above.
3. Copy any missing brand assets into `assets/` before referencing them.
4. Sketch the zone layout first (what boundaries exist, what's inside each) before placing individual nodes — get the topology right before the visual polish.
5. Compose title row → zones → nodes within zones → connectors → optional legend, reusing the exact inline-style values above so architecture diagrams feel like siblings of the workflow diagrams in the same deck.
6. Sanity-check: no connector should cross more than 2–3 others, no tile below ~48px, every zone label present, Port's role visually clear at a glance.
