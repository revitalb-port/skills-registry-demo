---
name: run-self-service
description: Execute Port self-service actions like provisioning infrastructure, creating services, or triggering workflows. Acts as an interface for Port actions.
user-invocable: true
version: 1.0.0
---

# Run Self-Service Action Skill

Execute Port self-service actions through natural language interface.

## When to Use

- User wants to create cloud infrastructure
- Provisioning a new service or environment
- Triggering any Port self-service action

## Execution Process

### Step 1: Discover Available Actions

```
list_actions()
```

Find actions matching user intent.

### Step 2: Get Action Schema

```
get_action(identifier="action-name")
```

Retrieve:
- Required inputs
- Input types and validation
- Approval requirements

### Step 3: Collect User Inputs

For each required input, prompt the user:
- Use the input's title and description
- Show enum options if available
- Validate format (email, URL, etc.)

Present like a form:
```
📝 Create New Service

Service Name: [required]
> 

Team: [required, select one]
  • platform-team
  • payments-team  
  • growth-team

Environment: [required, select one]
  • development
  • staging
  • production

Description: [optional]
> 
```

### Step 4: Validate Inputs

Before submission:
- Check required fields
- Validate formats
- Confirm with user

### Step 5: Execute Action

```
run_action(identifier="action-name", properties={
  "service_name": "user-input",
  "team": "selected-team",
  "environment": "selected-env"
})
```

### Step 6: Monitor Execution

If action is async:
```
get_action_run(run_id="run-123")
```

Report status: pending → running → success/failure

## Example Interactions

**User**: "I need a new S3 bucket"

**Agent**:
1. Finds `provision_s3_bucket` action
2. Gets schema: bucket_name, region, access_level
3. Prompts:
   ```
   📝 Provision S3 Bucket
   
   Bucket Name: [required]
   > 
   
   Region: [required, select one]
     • us-east-1
     • eu-west-1
   
   Access Level: [required, select one]
     • private
     • public-read
   ```
4. Executes action
5. Reports: "✅ Bucket created: my-bucket.s3.amazonaws.com"

**User**: "Create a new microservice"

**Agent**:
1. Finds `scaffold_service` action
2. Collects: name, language, team, repo visibility
3. Executes
4. Reports: "✅ Service created with repo, CI pipeline, and Port entity"

## Form-Like Experience

When collecting inputs:
- Show one input at a time for clarity
- Provide defaults where available
- Show validation errors inline
- Confirm before execution

## Quality Checklist

- [ ] Found correct action for user intent
- [ ] Retrieved complete input schema
- [ ] Collected all required inputs
- [ ] Validated input formats
- [ ] Confirmed before execution
- [ ] Reported execution status
