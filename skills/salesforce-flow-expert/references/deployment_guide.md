# Salesforce Flow Deployment Guide

Complete guide for deploying Flows using sf CLI with error handling and rollback procedures.

## Prerequisites

### 1. Install sf CLI

```bash
# Check if installed
sf --version

# If not installed, download from:
# https://developer.salesforce.com/tools/salesforcecli
```

### 2. Authenticate to Org

```bash
# Production org
sf org login web --alias production

# Sandbox org
sf org login web --alias my-sandbox

# List authenticated orgs
sf org list

# Display current org info
sf org display --target-org my-sandbox
```

### 3. Prepare Flow Files

Ensure you have both files for each Flow:
- `FlowName.flow` - Flow definition
- `FlowName.flow-meta.xml` - Metadata file

---

## sf CLI Commands Reference

### Basic Deployment

**Deploy single Flow:**
```bash
sf project deploy start \
  --source-dir force-app/main/default/flows/MyFlow.flow-meta.xml \
  --target-org my-sandbox
```

**Deploy Flow directory:**
```bash
sf project deploy start \
  --source-dir force-app/main/default/flows/ \
  --target-org my-sandbox
```

**Validate without deploying (dry run):**
```bash
sf project deploy start \
  --source-dir flows/ \
  --target-org my-sandbox \
  --dry-run
```

### Advanced Deployment

**Deploy with tests:**
```bash
sf project deploy start \
  --source-dir flows/ \
  --target-org production \
  --test-level RunLocalTests
```

**Check deployment status:**
```bash
sf project deploy report --target-org my-sandbox
```

**Cancel deployment:**
```bash
sf project deploy cancel --target-org my-sandbox
```

---

## Deployment Workflows

### Workflow 1: Standard Deployment (Manual)

**Step 1: Validate locally**
```bash
python3 scripts/validate_flow.py flows/MyFlow.flow-meta.xml
```

**Step 2: Deploy to sandbox**
```bash
sf project deploy start \
  --source-dir flows/ \
  --target-org sandbox
```

**Step 3: Test in sandbox**
- Manually run Flow in sandbox
- Verify expected behavior
- Check Debug Logs if issues occur

**Step 4: Activate Flow**
- Setup → Flows → [Flow Name] → Activate

**Step 5: Deploy to production**
```bash
sf project deploy start \
  --source-dir flows/ \
  --target-org production \
  --test-level RunLocalTests
```

### Workflow 2: Automated Deployment (Recommended)

**Use deployment script:**
```bash
# Step 1: Validate (dry run)
python3 scripts/deploy_flow.py \
  --source-dir flows/ \
  --target-org sandbox \
  --validate-only

# Step 2: Deploy if validation passes
python3 scripts/deploy_flow.py \
  --source-dir flows/ \
  --target-org sandbox

# Step 3: Test, then deploy to production
python3 scripts/deploy_flow.py \
  --source-dir flows/ \
  --target-org production \
  --test-level RunLocalTests
```

**Advantages:**
- Runs pre-deployment validation automatically
- Parses and explains deployment errors
- Supports auto-rollback on failure
- Provides troubleshooting guidance

---

## Common Deployment Errors

### Error 1: INVALID_TYPE_ON_FIELD_IN_RECORD

**Message:**
```
INVALID_TYPE_ON_FIELD_IN_RECORD: Invalid data type for field Amount__c
```

**Cause:** Variable type doesn't match Salesforce field type

**Fix:**
1. Check field type: Setup → Object Manager → [Object] → Fields → [Field]
2. Match variable dataType to field type:
   - Text field → `<dataType>String</dataType>`
   - Number field → `<dataType>Number</dataType>`
   - Currency field → `<dataType>Currency</dataType>`
   - Date field → `<dataType>Date</dataType>` (NOT DateTime!)
   - Checkbox → `<dataType>Boolean</dataType>`

---

### Error 2: INVALID_FIELD_OR_REFERENCE

**Message:**
```
INVALID_FIELD_OR_REFERENCE: No such column 'Custom_Field__c' on entity Account
```

**Cause:** Field doesn't exist or user lacks access

**Fix:**
1. Verify field API name in Setup
2. Check field-level security (FLS)
3. Ensure field not deleted

---

### Error 3: FLOW_ACTIVE_VERSION_NOT_FOUND

**Message:**
```
This flow doesn't have an active version.
```

**Cause:** Flow deployed but not activated

**Fix:**
```
Setup → Flows → [Flow Name] → Activate
```

---

### Error 4: CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY

**Message:**
```
insufficient access rights on object Account
```

**Cause:** User/running user lacks permissions

**Fix:**
1. Check Profile/Permission Set has object permissions:
   - Read, Create, Edit access
2. Check field-level security (FLS): Visible/Editable
3. For Record-Triggered Flows, check System Admin permissions

---

### Error 5: FIELD_CUSTOM_VALIDATION_EXCEPTION

**Message:**
```
FIELD_CUSTOM_VALIDATION_EXCEPTION: Amount must be positive
```

**Cause:** Validation rule triggered

**Fix:**
1. Review validation rules on target object
2. Ensure Flow sets all required fields
3. Test with valid data

---

## Error Handling Strategies

### Strategy 1: Pre-Deployment Validation

**Always validate before deploying:**
```bash
python3 scripts/validate_flow.py MyFlow.flow-meta.xml --format markdown > report.md
```

Catches 90%+ of errors before deployment.

### Strategy 2: Debug Logs

**Enable Debug Logs:**
```
1. Setup → Debug Logs → New
2. Select Traced Entity: User or Automated Process
3. Set log levels:
   - Workflow: DEBUG
   - Apex Code: FINE
4. Run Flow
5. View log: Setup → Debug Logs → View
```

**Look for:**
```
FLOW_CREATE_INTERVIEW_BEGIN
FLOW_ELEMENT_BEGIN: Assignment_1
FLOW_ELEMENT_ERROR: Variable 'totalAmount' not found
FLOW_CREATE_INTERVIEW_ERROR
```

### Strategy 3: Incremental Deployment

Deploy Flows one at a time to isolate errors:
```bash
sf project deploy start --source-dir flows/Flow1.flow-meta.xml --target-org sandbox
sf project deploy start --source-dir flows/Flow2.flow-meta.xml --target-org sandbox
```

---

## Rollback Procedures

### Manual Rollback

**Option 1: Deploy previous version**
```bash
# Deploy from backup directory
sf project deploy start \
  --source-dir backups/flows_2025-01-09/ \
  --target-org my-sandbox
```

**Option 2: Deactivate broken Flow**
```
Setup → Flows → [Flow Name] → Deactivate
```

### Automated Rollback

**Use deployment script with auto-rollback:**
```bash
python3 scripts/deploy_flow.py \
  --source-dir flows/ \
  --target-org sandbox \
  --rollback-on-error
```

**Note:** Requires backup directory at `backups/[source_dir_name]_backup/`

---

## Best Practices

### Before Deployment

- [ ] Run `validate_flow.py` on all Flows
- [ ] Test Flows manually in sandbox
- [ ] Review governor limits (DML, SOQL counts)
- [ ] Check user permissions
- [ ] Create backup of existing Flows

### During Deployment

- [ ] Deploy to sandbox first
- [ ] Use `--validate-only` for dry run
- [ ] Deploy incrementally (one Flow at a time)
- [ ] Monitor deployment status
- [ ] Check Debug Logs if errors occur

### After Deployment

- [ ] Activate Flows in target org
- [ ] Test with real data in sandbox
- [ ] Monitor Flow run history
- [ ] Document any issues encountered
- [ ] Update version control (Git commit)

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy Flows to Sandbox

on:
  push:
    branches: [ develop ]
    paths:
      - 'force-app/main/default/flows/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install sf CLI
        run: |
          npm install -g @salesforce/cli

      - name: Authenticate to Sandbox
        run: |
          echo "${{ secrets.SF_AUTH_URL }}" > auth_url.txt
          sf org login sfdx-url --sfdx-url-file auth_url.txt --alias sandbox

      - name: Validate Flows
        run: |
          python3 scripts/validate_flow.py force-app/main/default/flows/*.flow-meta.xml

      - name: Deploy Flows
        run: |
          python3 scripts/deploy_flow.py \
            --source-dir force-app/main/default/flows/ \
            --target-org sandbox \
            --validate-only
```

---

## Troubleshooting Checklist

If deployment fails:

1. **Run validation script**
   ```bash
   python3 scripts/validate_flow.py <flow_file> --format text
   ```

2. **Check org connection**
   ```bash
   sf org display --target-org <org-alias>
   ```

3. **Review Debug Logs**
   ```
   Setup → Debug Logs → New → Run Flow → View Log
   ```

4. **Verify permissions**
   - Object: Read, Create, Edit
   - Fields: Field-Level Security
   - Profile/Permission Set assignments

5. **Check metadata**
   ```bash
   cat MyFlow.flow-meta.xml | grep -E "(apiVersion|status|processType)"
   ```

6. **Test in sandbox first**
   - Never deploy untested Flows to production

---

**Last Updated:** 2025-01-09
**Version:** 1.0
**For error reference, see:** `assets/error_reference_table.md`
