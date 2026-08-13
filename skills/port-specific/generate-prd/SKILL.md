---
name: generate-prd
description: Generate a Product Requirements Document for a work item using Port's service catalog context. Use when creating a PRD, enriching a ticket, or preparing a work item for development.
user-invocable: true
version: 1.0.0
---

# Generate PRD Skill

Create engineering-ready Product Requirements Documents using Port's service catalog data.

## When to Use

- Creating a PRD for a new feature
- Enriching a Jira/Linear ticket with requirements
- Preparing a work item for development sprint

## PRD Generation Process

### Step 1: Gather Context from Port

Query the target service:
```
get_entity(blueprint="service", identifier="target-service", include=[
  "tier", "team", "depends_on", "readme_url", "codeowners"
])
```

Get recent incidents (for risk context):
```
list_entities(blueprint="incident", query={
  primary_service: "target-service",
  created_at: "<90d"
})
```

### Step 2: Structure the PRD

```markdown
# PRD: [Feature Name]

## Overview
**Service**: [service-name]
**Team**: [team from Port]
**Tier**: [service tier]
**Target Release**: [date]

## Problem Statement
[What problem does this solve?]

## User Stories
As a [user type], I want to [action] so that [benefit].

## Requirements

### Functional Requirements
1. [Requirement with acceptance criteria]
2. [Requirement with acceptance criteria]

### Non-Functional Requirements
- **Performance**: [metrics]
- **Availability**: [SLA based on tier]
- **Security**: [requirements]

## Technical Considerations

### Dependencies
[List from Port's depends_on relation]

### Risk Assessment
Based on incident history:
- [Risk 1 from past incidents]
- [Risk 2]

### CODEOWNERS
[From Port data - who needs to review]

## Success Metrics
- [Metric 1]
- [Metric 2]

## Out of Scope
- [What we're NOT building]
```

### Step 3: Tier-Based Requirements

Adjust requirements based on service tier:

| Tier | Availability SLA | Performance | Testing |
|------|-----------------|-------------|---------|
| Tier1-Critical | 99.99% | <100ms p99 | Full E2E, load test |
| Tier2-Core | 99.9% | <500ms p99 | Integration tests |
| Tier3-Supporting | 99% | <1s p99 | Unit tests |

### Step 4: Risk Analysis

Flag risks based on:
1. **Recent incidents** on the service
2. **Number of dependencies**
3. **Service tier** (higher tier = more risk)
4. **Change complexity**

### Step 5: Update Work Item

If integrated with Jira/Linear, call the appropriate action:
```
run_action("enrich_work_item", {
  work_item_id: "PROJ-123",
  prd_content: "[generated PRD]",
  risk_level: "medium"
})
```

## Quality Checklist

- [ ] Used actual service data from Port
- [ ] Requirements match service tier
- [ ] Listed real dependencies
- [ ] Analyzed incident history for risks
- [ ] Identified correct CODEOWNERS
- [ ] Clear acceptance criteria
