---
name: investigate-incident
description: Perform root cause analysis for incidents by querying Port entities - deployments, services, PRs, monitoring data, and past incidents. Use when investigating incidents or finding why an incident occurred.
user-invocable: true
version: 1.0.0
---

# Investigate Incident Skill

Perform systematic root cause analysis using Port's service catalog data.

## When to Use

- Incident has been triaged and needs investigation
- Finding root cause of production issues
- Correlating deployments with incidents

## Investigation Process

### Step 1: Timeline Construction

Query Port to build a timeline:

1. **Recent deployments** (last 24h):
   ```
   list_entities(blueprint="deployment", query={
     service: "affected-service",
     deployed_at: ">24h ago"
   })
   ```

2. **Recent PRs merged**:
   ```
   list_entities(blueprint="pull_request", query={
     service: "affected-service",
     merged_at: ">24h ago"
   })
   ```

3. **Config changes** (if tracked):
   ```
   list_entities(blueprint="config_change", query={
     service: "affected-service"
   })
   ```

### Step 2: Correlation Analysis

Check if incident timing correlates with:
- Deploy time (most common cause)
- Traffic spike
- Dependency failure
- Config change

### Step 3: Dependency Check

Query service dependencies:
```
get_entity(blueprint="service", identifier="affected-service", include=["depends_on"])
```

For each dependency, check:
- Health status
- Recent incidents
- Error rates

### Step 4: Historical Pattern Matching

Find similar past incidents:
```
list_entities(blueprint="incident", query={
  primary_service: "affected-service",
  created_at: "<30d"
})
```

Look for:
- Same error patterns
- Same time of day
- Same trigger conditions

### Step 5: Root Cause Determination

Document:
1. **What changed**: The specific change that caused the issue
2. **Why it failed**: The mechanism of failure
3. **Why it wasn't caught**: Gap in testing/review

### Step 6: Update Incident

Call `update_incident_investigation` with:
- `root_cause_summary`
- `related_deployment` (if applicable)
- `related_pr` (if applicable)
- `timeline_markdown`
- `investigation_notes`

## Output Format

```markdown
# Root Cause Analysis: [Incident ID]

## Summary
[One paragraph explanation]

## Timeline
| Time | Event |
|------|-------|
| 14:15 | PR #123 merged |
| 14:20 | Deployment v2.3.4 completed |
| 14:23 | First error alerts |

## Root Cause
[Detailed technical explanation]

## Related Changes
- PR: #123 - "Add currency field"
- Deployment: v2.3.4

## Recommendations
1. [Specific actionable item]
2. [Specific actionable item]
```

## Quality Checklist

- [ ] Built complete timeline
- [ ] Checked all recent deployments
- [ ] Analyzed dependencies
- [ ] Found correlated change
- [ ] Documented root cause clearly
