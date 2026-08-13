---
name: triage-incident
description: Analyze incidents in Alert stage and suggest severity, business impact, affected services, communications, and response team. Use when triaging incidents, evaluating incident severity, or when the user asks to analyze incident impact.
user-invocable: true
version: 1.0.0
---

# Triage Incident Skill

Triage production incidents using AI analysis to suggest severity, calculate business impact, and draft communications.

## When to Use

- Incident is in Alert stage and needs triage
- Analyzing incident severity or impact
- Preparing incident for investigation phase

## Triage Process

### Step 1: Gather Context

Collect via Port MCP:
1. **Incident details**: Title, description, alert source
2. **Primary service**: Tier, dependencies, ownership
3. **Monitoring data**: Error rates, affected customers
4. **Timing**: Business hours vs off-hours

### Step 2: Determine Severity

| Level | Criteria | Examples |
|-------|----------|----------|
| Sev1 | Complete tier1 outage, >$10K/hour | Database crash, auth broken |
| Sev2 | Partial tier1 or tier2 outage | Payments failing, search down |
| Sev3 | Minor degradation, internal | Slow dashboard, export broken |
| Sev4 | Minimal impact, cosmetic | UI typo, styling bug |

### Step 3: Calculate Business Impact

Provide:
- Customer impact (estimated users)
- Revenue impact ($/hour)
- SLA implications
- Reputation risk

### Step 4: Recommend Response Team

Query Port for:
1. Service's `on_call` relation
2. Service `owner` relation
3. Team escalation for sev1/sev2

### Step 5: Draft Communications

**Internal message:**
```
🚨 Incident: [Title]
Severity: [Level]
Impact: [Brief description]
Response: [Owner] leading, [Team] engaged
ETA: [Timeline]
```

**Status page (customer-facing):**
```
We're experiencing issues with [feature]. 
Our team is actively working on a fix.
We'll provide an update within [time].
```

### Step 6: Submit via Port Action

Call `update_incident_triage` with:
- `ai_suggested_severity`
- `business_impact`
- `internal_comms_message`
- `status_page_message`
- `ai_suggested_owner`
- `ai_suggested_response_team`

## Port MCP Queries

```
list_entities(blueprint="incident", identifiers=["incident-id"])
list_entities(blueprint="service", include=["on_call", "owner", "team"])
list_entities(blueprint="deployment", query={service: "x", deployed_at: ">1h ago"})
```

## Quality Checklist

- [ ] Severity rationale is data-driven
- [ ] Impact includes metrics
- [ ] Found actual on-call via Port
- [ ] Messages are clear and actionable
