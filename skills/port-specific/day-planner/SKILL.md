---
name: day-planner
description: Plan your day by querying Port for your assigned tasks, on-call status, pending PRs, and upcoming deployments. Prioritizes tasks over incidents.
user-invocable: true
version: 1.0.0
---

# Day Planner Skill

Get a personalized daily overview of your work using Port data.

## When to Use

- Starting your work day
- Planning sprint work
- Checking priorities during on-call

## Planning Process

### Step 1: Get User Context

Identify current user's email and query:
```
list_entities(blueprint="_user", query={
  email: "user@company.com"
})
```

### Step 2: Tasks & Work Items (Priority)

```
list_entities(blueprint="task", query={
  assignee: "user@company.com",
  status: ["todo", "in_progress"]
})
```

Sort by:
1. Due date (soonest first)
2. Priority (P0 > P1 > P2)
3. Sprint commitment

### Step 3: On-Call Status

Check if user is on-call:
```
list_entities(blueprint="service", query={
  on_call: "user@company.com"
})
```

### Step 4: Pending PRs

```
list_entities(blueprint="pull_request", query={
  $or: [
    { author: "user@company.com", status: "open" },
    { reviewers: { $contains: "user@company.com" }, status: "needs_review" }
  ]
})
```

### Step 5: Incidents (Lower Priority)

Only show active incidents:
```
list_entities(blueprint="incident", query={
  assignee: "user@company.com",
  status: ["alert", "investigating"]
})
```

### Step 6: Upcoming Deployments

```
list_entities(blueprint="deployment", query={
  scheduled_by: "user@company.com",
  status: "scheduled",
  scheduled_for: "<24h"
})
```

## Output Format

```markdown
# 📅 Your Day: [Date]

## 🎯 Focus Tasks
| Task | Priority | Due | Sprint |
|------|----------|-----|--------|
| PROJ-123: Implement auth | P0 | Today | Sprint 12 |
| PROJ-124: Update docs | P1 | Tomorrow | Sprint 12 |

## 📝 PRs Needing Attention
### Your PRs Waiting for Review
- [#456](link) - Add caching layer (2 approvals needed)

### PRs You Need to Review
- [#789](link) - Fix payment bug (@alice, requested 2h ago)

## 🔔 On-Call
You are on-call for: **payment-api**, **checkout-service**

## 🚀 Scheduled Deployments
| Time | Service | Version |
|------|---------|---------|
| 14:00 | payment-api | v2.3.5 |

## 🚨 Active Incidents
| Incident | Severity | Service |
|----------|----------|---------|
| INC-456 | Sev3 | user-api |

## Recommendations
1. Focus on PROJ-123 (due today)
2. Review PR #789 (blocking @alice)
3. Prepare for 14:00 deployment
```

## Note on Priorities

This skill prioritizes tasks over incidents because:
- Incidents have dedicated triage/investigation skills
- Day planning should focus on planned work
- Active incidents surface separately with alerts

## Quality Checklist

- [ ] Retrieved all assigned tasks
- [ ] Checked on-call status
- [ ] Found pending PR reviews
- [ ] Listed scheduled deployments
- [ ] Prioritized by due date and urgency
