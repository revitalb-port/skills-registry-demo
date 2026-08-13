---
name: service-health-check
description: Query Port's service catalog to get a comprehensive health overview of a service including scorecard status, recent incidents, deployments, and dependencies.
user-invocable: true
version: 1.0.0
---

# Service Health Check Skill

Get a comprehensive health overview of any service using Port's catalog.

## When to Use

- Before deploying to a service
- During on-call rotation handoff
- Investigating service issues
- Planning capacity or changes

## Health Check Process

### Step 1: Basic Service Info

```
get_entity(blueprint="service", identifier="service-name", include=[
  "tier", "team", "owner", "on_call", 
  "depends_on", "repository", "scorecard_status"
])
```

### Step 2: Scorecard Status

Check production readiness:
```
get_entity(blueprint="service", identifier="service-name")
# Look at scorecard properties:
# - has_readme
# - has_runbook
# - has_monitoring
# - has_slo
# - security_scan_passed
```

### Step 3: Recent Incidents

```
list_entities(blueprint="incident", query={
  primary_service: "service-name",
  created_at: ">30d"
})
```

Count by severity and calculate MTTR.

### Step 4: Recent Deployments

```
list_entities(blueprint="deployment", query={
  service: "service-name",
  deployed_at: ">7d"
})
```

### Step 5: Dependency Health

For each dependency:
```
get_entity(blueprint="service", identifier="dep-service")
```

Check their health status recursively.

## Output Format

```markdown
# Service Health: [service-name]

## Overview
| Property | Value |
|----------|-------|
| Tier | Tier1-Critical |
| Team | payments-team |
| Owner | alice@company.com |
| On-Call | bob@company.com |

## 📊 Scorecard: 4/5 Passing
| Check | Status |
|-------|--------|
| Has README | ✅ |
| Has Runbook | ✅ |
| Has Monitoring | ✅ |
| Has SLO | ✅ |
| Security Scan | ❌ Last scan failed |

## 🚨 Incidents (Last 30 Days)
| Severity | Count | MTTR |
|----------|-------|------|
| Sev1 | 0 | - |
| Sev2 | 1 | 45min |
| Sev3 | 2 | 2h |

## 🚀 Recent Deployments
| Date | Version | Status |
|------|---------|--------|
| 2026-05-04 | v2.3.5 | ✅ Success |
| 2026-05-02 | v2.3.4 | ✅ Success |

## 🔗 Dependencies
| Service | Health | Tier |
|---------|--------|------|
| user-api | 🟢 Healthy | Tier1 |
| db-primary | 🟢 Healthy | Tier1 |
| cache-redis | 🟡 Degraded | Tier2 |

## Recommendations
1. Fix failing security scan
2. Monitor cache-redis degradation
```

## Quality Checklist

- [ ] Retrieved all scorecard data
- [ ] Calculated incident metrics
- [ ] Checked all dependencies
- [ ] Provided actionable recommendations
