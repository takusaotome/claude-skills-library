---
name: salesforce-flow-expert
description: Expert guidance for Salesforce Flow implementation from design through deployment. Use this skill when building Screen Flows, Record-Triggered Flows, Schedule-Triggered Flows, or Autolaunched Flows. Covers Flow design patterns, metadata XML generation, variable/element reference validation, governor limit optimization, and sf CLI deployment. Critical for preventing reference errors (undeclared variables, invalid element references) and deployment failures. Use when creating new Flows, debugging Flow errors, optimizing Flow performance, or deploying Flows to production.
---

# Salesforce Flow Expert

## Overview

This skill provides comprehensive guidance for Salesforce Flow implementation, from initial design through production deployment. It emphasizes preventing the most common Flow errors—particularly variable and element reference issues—through automated validation, proper metadata generation, and deployment best practices. Use this skill to build robust, error-free Flows that deploy successfully on the first attempt.

## When to Use This Skill

Invoke this skill when:

- **Flow Development**: Creating new Screen Flows, Record-Triggered Flows, Schedule-Triggered Flows, or Autolaunched Flows
- **Error Prevention**: Validating Flows before deployment to catch reference errors, type mismatches, or undeclared variables
- **Debugging**: Troubleshooting "Element not found", "Variable not declared", or type mismatch errors
- **Deployment**: Deploying Flows to sandbox or production using sf CLI with proper error handling
- **Optimization**: Identifying governor limit issues (DML in loops, SOQL in loops) and implementing bulkification patterns
- **Metadata Management**: Generating or troubleshooting Flow-meta.xml files with correct structure and API versions

## Core Capabilities

### 1. Flow Design & Pattern Selection

Choose the right Flow type and design pattern for your requirements.

**Flow Type Decision Matrix**:

| Flow Type | Trigger | Best For | User Interaction |
|-----------|---------|----------|------------------|
| **Screen Flow** | User clicks button/link | Guided processes, data collection | Yes |
| **Record-Triggered** | Record create/update/delete | Automated business logic | No |
| **Schedule-Triggered** | Time-based schedule | Batch processing, cleanup | No |
| **Autolaunched** | Called by other automation | Reusable logic, sub-flows | No |

**Common Design Patterns**:

**Pattern 1: Wizard Pattern** (Screen Flow)
```
Screen 1 (Input) → Decision → Screen 2A/2B → Assignment → Create Records → Screen 3 (Confirmation)
```

**Pattern 2: Before-Save Trigger** (Record-Triggered)
```
Trigger: Before Update → Decision → Assignment (Update Fields) → End
```

**Pattern 3: Batch Processing** (Schedule-Triggered)
```
Start → Get Records (Filter) → Loop → Update Records (Batch) → End
```

**Variable Naming Conventions**:
- Use **camelCase** for variables: `totalAmount`, `selectedAccount`, `recordCount`
- Use **PascalCase** for elements: `Screen_Input_Details`, `Assignment_Calculate_Total`
- Prefix collections with `col`: `colAccounts`, `colOpportunities`
- Prefix boolean variables with `is` or `has`: `isApproved`, `hasError`

**Example - Screen Flow Variable Setup**:
```xml
<variables>
    <name>selectedAccountId</name>
    <dataType>String</dataType>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
</variables>

<variables>
    <name>colOpportunities</name>
    <dataType>SObject</dataType>
    <isCollection>true</isCollection>
    <objectType>Opportunity</objectType>
</variables>
```

**Reference**: Load `references/flow_types_guide.md` for detailed patterns, examples, and best practices for each Flow type.

### 2. Flow Metadata XML Generation

Generate correct Flow-meta.xml files with proper structure and API version compatibility.

**Why Metadata Matters**:
Flow deployment requires both the Flow definition (`.flow`) and metadata file (`.flow-meta.xml`). Incorrect metadata structure causes deployment failures even if the Flow logic is perfect.

**Use the Generation Script**:
```bash
cd scripts/
python3 generate_flow_metadata.py ../MyFlow.flow \
  --type recordTriggeredFlow \
  --api-version 60.0 \
  --status Draft \
  --output ../MyFlow.flow-meta.xml
```

**Manual Metadata Structure** (when needed):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>
    <status>Draft</status>
    <processType>AutoLaunchedFlow</processType>
    <label>My Flow Label</label>
    <description>Flow description</description>
</Flow>
```

**Key Metadata Fields**:
- `apiVersion`: Must match your org's API version (typically 58.0-61.0)
- `status`: `Draft` or `Active`
- `processType`: Must match Flow type (see reference guide)
- `label`: Human-readable name (required)

**Reference**: Load `references/metadata_xml_reference.md` for complete metadata structure, required vs optional elements, API version differences, and troubleshooting common metadata errors.

### 3. Pre-Deployment Validation

**CRITICAL**: Validate Flows before deployment to catch 90%+ of errors upfront, especially variable/element reference errors.

**Use the Validation Script**:
```bash
cd scripts/
python3 validate_flow.py ../MyFlow.flow-meta.xml --format markdown
```

**Validation Categories**:

#### 3.1 Reference Validation (Priority 1)

The #1 cause of Flow deployment failures. The validator detects:

**Error Type 1: Undeclared Variable**
```
[E001] Undeclared Variable: 'totalAmout' referenced in Assignment_1
       → Did you mean 'totalAmount'? (declared on line 45)
       → Fix: Rename 'totalAmout' to 'totalAmount' in Assignment_1
```

**Error Type 2: Invalid Element Reference**
```
[E002] Invalid Element Reference: 'Screen_2' in Connector but element not found
       → Available elements: Screen_Input, Screen_Confirm, Assignment_1
       → Fix: Update Connector to reference existing element name
```

**Error Type 3: Type Mismatch**
```
[E003] Type Mismatch: Variable 'count' (Text) assigned Number value
       → Variable type: Text
       → Assignment value type: Number
       → Fix: Change variable 'count' to Number type or convert value to Text
```

**Error Type 4: Collection vs Single Value**
```
[E004] Collection/Single Value Mismatch: 'colAccounts' (Collection) used in single value context
       → Variable 'colAccounts' is a collection (isCollection=true)
       → Used in: Assignment expects single Account object
       → Fix: Use Loop to iterate or Get Records with FIRST operator
```

#### 3.2 Governor Limit Validation

**Critical Patterns to Avoid**:

**DML in Loop** (ERROR):
```xml
<!-- BAD: DML inside Loop -->
<loops>
    <name>Loop_Through_Accounts</name>
    <recordUpdates>
        <name>Update_Account</name>  <!-- ❌ Causes governor limit error -->
    </recordUpdates>
</loops>
```

**Correct Pattern**:
```xml
<!-- GOOD: Collect in loop, DML after -->
<loops>
    <name>Loop_Through_Accounts</name>
    <assignments>
        <name>Add_To_Collection</name>  <!-- ✅ Collect changes -->
    </assignments>
</loops>
<recordUpdates>
    <name>Update_All_Accounts</name>  <!-- ✅ Batch update after loop -->
</recordUpdates>
```

**SOQL in Loop** (WARNING):
```
[W001] SOQL in Loop: Get_Records element 'Get_Related_Opportunities' inside Loop_Through_Accounts
       → Risk: May exceed 100 SOQL query limit
       → Recommendation: Move Get Records before loop and filter in memory
```

#### 3.3 Metadata Validation

- API version compatibility check
- Required fields present (`apiVersion`, `status`, `processType`, `label`)
- Element ordering validation
- XML structure correctness

#### 3.4 Naming Convention Check

```
[W002] Naming Convention: Variable 'var1' should use camelCase (e.g., 'myVariable')
[W003] Naming Convention: Element 'screen1' should use PascalCase (e.g., 'Screen_Input')
```

**Example Validation Report**:
```
=== Flow Validation Report ===
Flow: MyScreenFlow.flow-meta.xml
API Version: 60.0
Status: ❌ FAILED (3 errors, 2 warnings)

ERRORS:
[E001] Undeclared Variable: 'totalAmout' referenced in Assignment_Calculate_Total
       → Did you mean 'totalAmount'?
[E002] Invalid Element Reference: 'Screen_2' in Connector_After_Input
[E003] Type Mismatch: Variable 'recordCount' (Text) assigned Number value

WARNINGS:
[W001] SOQL in Loop: Get_Records inside Loop_Process_Accounts
[W002] Naming Convention: Variable 'amt' should use descriptive camelCase

✅ Validation complete. Fix 3 errors before deployment.
```

**Reference**: Load `references/variable_reference_patterns.md` for comprehensive error catalog (Top 10 errors), root cause analysis, fix patterns, and prevention checklists.

### 4. Deployment & Troubleshooting

Deploy validated Flows using sf CLI with proper error handling and rollback capabilities.

**Prerequisites**:
```bash
# Verify sf CLI installed
sf --version

# Authenticate to org
sf org login web --alias my-sandbox
```

**Deployment Workflow**:

**Option 1: Manual Deployment** (Quick)
```bash
# Deploy single Flow
sf project deploy start --source-dir force-app/main/default/flows/MyFlow.flow-meta.xml --target-org my-sandbox

# Check deployment status
sf project deploy report --target-org my-sandbox
```

**Option 2: Automated Deployment with Validation** (Recommended)
```bash
cd scripts/
python3 deploy_flow.py \
  --source-dir ../flows/ \
  --target-org my-sandbox \
  --validate-only  # Dry run first

# If validation passes, deploy for real
python3 deploy_flow.py \
  --source-dir ../flows/ \
  --target-org my-sandbox
```

**Common Deployment Errors**:

**Error: "INVALID_TYPE_ON_FIELD_IN_RECORD"**
```
Cause: Variable type doesn't match field type
Fix: Check variable dataType matches target object field type
Example: Text variable assigned to Number field
```

**Error: "INVALID_FIELD_OR_REFERENCE"**
```
Cause: Referencing non-existent field or variable
Fix: Run validate_flow.py to find undeclared references
```

**Error: "FLOW_ACTIVE_VERSION_NOT_FOUND"**
```
Cause: No active version exists when trying to run Flow
Fix: Activate Flow version after deployment: Setup → Flows → [Flow Name] → Activate
```

**Rollback Procedure**:
```bash
# If deployment fails, rollback to previous version
sf project deploy start \
  --source-dir backups/flows_backup_20250109/ \
  --target-org my-sandbox
```

**Reference**: Load `references/deployment_guide.md` for complete sf CLI command reference, advanced deployment workflows, error handling patterns, and rollback procedures.

## Workflow: Design to Deployment

Follow this end-to-end workflow for error-free Flow implementation:

**Phase 1: Design** (10-20 minutes)
1. Determine Flow type using decision matrix (Capability 1)
2. Sketch Flow logic on paper or whiteboard
3. Define variables with proper naming conventions
4. Identify data operations (Get, Create, Update, Delete)

**Phase 2: Build** (30-60 minutes)
5. Create Flow in Flow Builder (Setup → Flows → New Flow)
6. Implement business logic following design patterns
7. Test manually in sandbox with sample data
8. Export Flow files (`.flow` and `.flow-meta.xml`)

**Phase 3: Validate** (5 minutes)
9. Run validation script:
   ```bash
   python3 scripts/validate_flow.py MyFlow.flow-meta.xml --format markdown > validation_report.md
   ```
10. Review validation report and fix all errors
11. Re-run validation until clean (0 errors)

**Phase 4: Deploy** (5-10 minutes)
12. Deploy to sandbox with validation:
    ```bash
    python3 scripts/deploy_flow.py --source-dir flows/ --target-org sandbox --validate-only
    ```
13. If validation passes, deploy for real:
    ```bash
    python3 scripts/deploy_flow.py --source-dir flows/ --target-org sandbox
    ```
14. Activate Flow in target org
15. Test Flow in sandbox before promoting to production

**Phase 5: Production** (10 minutes)
16. Repeat validation and deployment for production org
17. Monitor Flow runs: Setup → Flows → [Flow Name] → Run History
18. Set up Debug Logs if issues occur

## Best Practices

### Security

1. **Use `$Setup` variables** for system context: `$Setup.User.Id`, `$Setup.Organization.Name`
2. **Respect record-level security**: Flow runs in system context by default (respects OWD but not sharing rules)
3. **Validate user input** in Screen Flows before DML operations
4. **Use Apex @InvocableMethod** for sensitive operations requiring `with sharing`

### Performance

1. **Bulkify all operations**: Design Flows to handle up to 200 records per transaction
2. **Avoid SOQL in loops**: Query once before loop, filter in memory
3. **Batch DML operations**: Collect records in loop, update outside loop
4. **Use Fast Field Updates** for simple field changes in Record-Triggered Flows (Before-Save triggers)
5. **Limit Flow depth**: Avoid nesting Flows more than 2 levels deep

### Maintainability

1. **Use descriptive names**: `Assignment_Calculate_Total_With_Tax` not `Assignment_1`
2. **Add descriptions** to all elements explaining their purpose
3. **Version control**: Store Flow files in Git with meaningful commit messages
4. **Document decisions**: Add Flow description explaining business logic and assumptions
5. **Test with bulk data**: Always test with 200 records to validate governor limits

### Error Handling

1. **Use Fault Connectors** on elements that can fail (Get Records, Create Records)
2. **Create error variables**: `hasError` (Boolean), `errorMessage` (Text)
3. **Display error screens** to users in Screen Flows
4. **Log errors** to custom Error_Log__c object for debugging
5. **Set default values** for variables to prevent null reference errors

## Resources

This skill includes comprehensive scripts and reference documentation:

### scripts/

**validate_flow.py** (Primary Script)
- Comprehensive pre-deployment validation
- Detects variable/element reference errors
- Governor limit analysis
- Generates detailed reports (text, JSON, markdown)
- Use before every deployment to catch 90%+ of errors

**generate_flow_metadata.py**
- Creates Flow-meta.xml files with correct structure
- Handles API version compatibility
- Supports all Flow types
- Use when metadata is missing or corrupted

**deploy_flow.py**
- Automated deployment via sf CLI
- Pre-deployment validation checks
- Error parsing and rollback support
- Use for CI/CD pipelines and batch deployments

**extract_flow_elements.py**
- Parses Flow XML to extract structure
- Lists variables, elements, connections
- Generates dependency graphs
- Use for documentation and analysis

### references/

**variable_reference_patterns.md** (Most Important)
- Top 10 most common variable/element reference errors
- Each error includes: frequency, message, root cause, fix pattern, prevention checklist
- Variable declaration best practices
- Scope and visibility rules
- Comprehensive troubleshooting guide

**flow_types_guide.md**
- Detailed guide for each Flow type (Screen, Record-Triggered, Schedule-Triggered, Autolaunched)
- Design patterns with complete examples
- When to use each type
- Common pitfalls and how to avoid them

**metadata_xml_reference.md**
- Complete Flow-meta.xml structure reference
- Element ordering requirements (critical for deployment success)
- API version differences
- Common metadata errors and fixes

**governor_limits_optimization.md**
- DML and SOQL optimization patterns
- Anti-patterns vs correct patterns with code examples
- Bulkification checklist
- Performance monitoring queries

**deployment_guide.md**
- sf CLI command reference
- Deployment workflows (manual, automated, CI/CD)
- Error handling and troubleshooting
- Rollback procedures

Load these references as needed to inform your Flow development and troubleshooting.

### assets/

**flow_metadata_templates/**
- XML templates for each Flow type
- Use as starting point for manual metadata creation

**deployment_configs/**
- package.xml template for deployment
- sfdx-project.json template for SFDX projects

**error_reference_table.md**
- Quick lookup table mapping error messages to solutions
- Use when troubleshooting specific deployment errors

---

**Note**: Always test Flows in a sandbox environment before deploying to production. Use the validation script before every deployment to catch errors early. Follow your organization's change management and deployment processes.
