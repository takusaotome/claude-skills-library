# Flow Error Reference Table

Quick lookup table for common Salesforce Flow errors with immediate solutions.

## How to Use This Table

1. **Find your error message** in the Quick Lookup Table below
2. **Note the Error Code** (e.g., E001, D001)
3. **Jump to Detailed Solution** section for fix pattern and code examples

---

## Quick Lookup Table

| Error Code | Error Message Fragment | Category | Severity | Quick Fix |
|------------|----------------------|----------|----------|-----------|
| **E001** | "hasn't been set or assigned" | Variable Reference | ERROR | Declare variable or fix typo |
| **E002** | "element was not found" | Element Reference | ERROR | Update connector to existing element |
| **E003** | "different data type" | Type Mismatch | ERROR | Match variable type to assigned value |
| **E004** | "assign a collection to a variable that isn't" | Collection Mismatch | ERROR | Use collection variable or getFirstRecordOnly |
| **E005** | "look up a value" + null | Null Reference | ERROR | Set default value or check IsNull |
| **E006** | "circular reference or infinite loop" | Circular Reference | ERROR | Add exit condition or use Loop element |
| **D001** | "INVALID_TYPE_ON_FIELD_IN_RECORD" | Field Type | DEPLOY ERROR | Check field API name and type |
| **D002** | "INVALID_FIELD_OR_REFERENCE" | Field Not Found | DEPLOY ERROR | Verify field exists on object |
| **D003** | "FLOW_ACTIVE_VERSION_NOT_FOUND" | Missing Active | DEPLOY ERROR | Activate Flow after deployment |
| **D004** | "REQUIRED_FIELD_MISSING" | Required Field | DEPLOY ERROR | Populate all required fields |
| **D005** | "CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY" | Permission Issue | DEPLOY ERROR | Check user permissions and FLS |
| **G001** | DML statement inside loop | Governor Limit | WARNING | Move DML outside loop, batch update |
| **G002** | SOQL query inside loop | Governor Limit | WARNING | Query before loop, filter in memory |
| **G003** | "Too many SOQL queries" | Governor Limit | RUNTIME ERROR | Reduce Get Records elements |
| **G004** | "Too many DML statements" | Governor Limit | RUNTIME ERROR | Batch operations, reduce DML calls |
| **M001** | "processType" mismatch | Metadata | DEPLOY ERROR | Match processType to Flow type |
| **M002** | Missing apiVersion | Metadata | DEPLOY ERROR | Add apiVersion tag |
| **M003** | Missing status | Metadata | DEPLOY ERROR | Add status tag (Draft/Active) |
| **F001** | Formula syntax error | Formula | ERROR | Check formula syntax and functions |
| **F002** | "FIELD_CUSTOM_VALIDATION_EXCEPTION" | Validation Rule | RUNTIME ERROR | Review validation rules on object |
| **S001** | Screen required field empty | Screen Input | RUNTIME ERROR | Mark field as required or validate |

---

## Detailed Solutions

### Variable Reference Errors

#### E001: Variable Not Set or Assigned

**Full Error Message:**
```
The flow failed to access the value for {!myVariable} because it hasn't been set or assigned.
```

**Cause:** Variable used before being declared or assigned a value

**Solution:**
```xml
<!-- Declare variable -->
<variables>
    <name>myVariable</name>
    <dataType>String</dataType>
    <value>
        <stringValue>default</stringValue>  <!-- Set default -->
    </value>
</variables>

<!-- OR assign before use -->
<assignments>
    <name>Assignment_Initialize</name>
    <assignmentItems>
        <assignToReference>myVariable</assignToReference>
        <operator>Assign</operator>
        <value>
            <stringValue>initial value</stringValue>
        </value>
    </assignmentItems>
</assignments>
```

**Validation:** `python3 validate_flow.py MyFlow.flow-meta.xml` (catches E001 errors)

---

#### E002: Element Not Found

**Full Error Message:**
```
The flow tried to reference {elementName} via a connection, but the element was not found.
```

**Cause:** Connector points to renamed or deleted element

**Solution:**
```xml
<!-- Update connector to existing element -->
<connector>
    <targetReference>Existing_Element_Name</targetReference>
</connector>
```

**Prevention:** Update all connectors when renaming elements

---

#### E003: Type Mismatch

**Full Error Message:**
```
The referenced resource has a different data type than the value being assigned.
```

**Cause:** Assigning wrong type (e.g., Text to Number variable)

**Solution:**
```xml
<!-- Match types -->
<variables>
    <name>recordCount</name>
    <dataType>Number</dataType>  <!-- Number type -->
</variables>

<assignments>
    <assignmentItems>
        <assignToReference>recordCount</assignToReference>
        <operator>Assign</operator>
        <value>
            <numberValue>10</numberValue>  <!-- Number value -->
        </value>
    </assignmentItems>
</assignments>

<!-- OR use conversion formula -->
<assignments>
    <assignmentItems>
        <assignToReference>recordCount</assignToReference>
        <operator>Assign</operator>
        <value>
            <elementReference>Formula_Convert_To_Number</elementReference>  <!-- VALUE({!textVar}) -->
        </value>
    </assignmentItems>
</assignments>
```

---

#### E004: Collection/Single Value Mismatch

**Full Error Message:**
```
The flow tried to assign a collection to a variable that isn't a collection.
```

**Cause:** Get Records returns collection, assigned to single-value variable

**Solution:**
```xml
<!-- Option 1: Use collection variable -->
<variables>
    <name>colAccounts</name>
    <dataType>SObject</dataType>
    <isCollection>true</isCollection>  <!-- Collection -->
    <objectType>Account</objectType>
</variables>

<!-- Option 2: Get only first record -->
<recordLookups>
    <name>Get_First_Account</name>
    <getFirstRecordOnly>true</getFirstRecordOnly>  <!-- Single record -->
    <object>Account</object>
</recordLookups>
```

---

### Deployment Errors

#### D001: INVALID_TYPE_ON_FIELD_IN_RECORD

**Full Error Message:**
```
INVALID_TYPE_ON_FIELD_IN_RECORD: Invalid data type for field {FieldName}
```

**Cause:** Variable type doesn't match Salesforce field type

**Solution:**
1. Check field type in Setup → Object Manager → [Object] → Fields
2. Match variable dataType to field type:
   - Text field → String variable
   - Number field → Number variable
   - Currency field → Currency variable
   - Date field → Date variable (not DateTime!)
   - Checkbox field → Boolean variable

---

#### D002: INVALID_FIELD_OR_REFERENCE

**Full Error Message:**
```
INVALID_FIELD_OR_REFERENCE: No such column '{FieldName}' on entity
```

**Cause:** Field doesn't exist on object (typo, wrong API name, field deleted, no access)

**Solution:**
1. Verify field API name: Setup → Object Manager → [Object] → Fields
2. Check field-level security: User has Read access
3. Correct field reference:
   ```xml
   <inputAssignments>
       <field>Account_Name__c</field>  <!-- Correct API name with __c -->
   </inputAssignments>
   ```

---

#### D003: FLOW_ACTIVE_VERSION_NOT_FOUND

**Full Error Message:**
```
This flow doesn't have an active version.
```

**Cause:** Flow deployed but not activated

**Solution:**
1. Deploy Flow
2. Activate: Setup → Flows → [Flow Name] → Activate

---

#### D005: CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY

**Full Error Message:**
```
CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY: {ObjectName}: insufficient access rights on object
```

**Cause:** User/running user lacks object or field-level permissions

**Solution:**
1. Check Profile/Permission Set has access:
   - Object: Read, Create, Edit permissions
   - Fields: Field-Level Security = Visible/Editable
2. For Record-Triggered Flows, check object permissions for System Administrator (Flow runs as system)

---

### Governor Limit Errors

#### G001: DML in Loop

**Validation Warning:**
```
[W001] DML in Loop: recordUpdates element inside loop
```

**Cause:** DML operation (Create/Update/Delete) inside loop body

**Solution:**
```xml
<!-- BAD -->
<loops>
    <recordUpdates>
        <name>Update_Account</name>  <!-- ❌ DML in loop -->
    </recordUpdates>
</loops>

<!-- GOOD -->
<loops>
    <assignments>
        <name>Add_To_Collection</name>  <!-- ✅ Collect in loop -->
    </assignments>
</loops>
<recordUpdates>
    <name>Update_All_Accounts</name>  <!-- ✅ DML after loop -->
</recordUpdates>
```

**Limit:** 150 DML statements per transaction

---

#### G002: SOQL in Loop

**Validation Warning:**
```
[W002] SOQL in Loop: recordLookups element inside loop
```

**Cause:** Get Records inside loop body

**Solution:**
```xml
<!-- BAD -->
<loops>
    <recordLookups>
        <name>Get_Related</name>  <!-- ❌ SOQL in loop -->
    </recordLookups>
</loops>

<!-- GOOD -->
<recordLookups>
    <name>Get_All_Related</name>  <!-- ✅ Query before loop -->
</recordLookups>
<loops>
    <decisions>
        <name>Filter_In_Memory</name>  <!-- ✅ Filter in loop -->
    </decisions>
</loops>
```

**Limit:** 100 SOQL queries per transaction

---

### Metadata Errors

#### M001: processType Mismatch

**Deployment Error:**
```
processType value doesn't match Flow type
```

**Cause:** Wrong processType in metadata file

**Solution:**
```xml
<!-- Screen Flow -->
<processType>Flow</processType>

<!-- Record-Triggered Flow -->
<processType>AutoLaunchedFlow</processType>
<triggerType>RecordAfterSave</triggerType>

<!-- Schedule-Triggered Flow -->
<processType>AutoLaunchedFlow</processType>
<start>
    <scheduledPaths>...</scheduledPaths>
</start>

<!-- Autolaunched Flow -->
<processType>AutoLaunchedFlow</processType>
```

---

#### M002/M003: Missing Required Metadata

**Deployment Error:**
```
Missing required field: apiVersion or status
```

**Solution:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>  <!-- Required -->
    <status>Draft</status>         <!-- Required: Draft or Active -->
    <label>My Flow</label>
</Flow>
```

---

### Formula Errors

#### F001: Formula Syntax Error

**Error Message:**
```
Syntax error: unexpected token 'xxx'
```

**Cause:** Invalid formula syntax

**Common Mistakes:**
```
❌ {!Variable}             → Use in assignments, not formulas
✅ Variable                → Correct in formula

❌ IF(condition, true)     → Missing false branch
✅ IF(condition, true, false)  → Correct

❌ VALUE({!Amount__c})     → Amount__c already Number type
✅ TEXT({!Amount__c})      → Convert Number to Text
```

**Test:** Use Formula Builder in Flow to validate syntax

---

## Quick Command Reference

```bash
# Validate Flow
python3 scripts/validate_flow.py MyFlow.flow-meta.xml --format text

# Generate metadata
python3 scripts/generate_flow_metadata.py MyFlow.flow --type recordTriggeredFlow --api-version 60.0

# Deploy Flow
python3 scripts/deploy_flow.py --source-dir flows/ --target-org sandbox --validate-only

# Check sf CLI
sf --version
sf org list
```

---

## Emergency Troubleshooting Steps

If Flow deployment fails:

1. **Run validation script** → Catch 90% of errors before deployment
   ```bash
   python3 scripts/validate_flow.py MyFlow.flow-meta.xml
   ```

2. **Check Debug Logs** → See runtime errors
   ```
   Setup → Debug Logs → New → Select User → Set Workflow = DEBUG
   ```

3. **Verify permissions** → Object/field access
   ```
   Setup → Permission Sets → [Your Permission Set] → Object Settings
   ```

4. **Check metadata** → apiVersion, status, processType
   ```bash
   cat MyFlow.flow-meta.xml | grep -E "(apiVersion|status|processType)"
   ```

5. **Test in sandbox first** → Never deploy untested Flows to production

---

**Last Updated:** 2025-01-09
**Version:** 1.0
**For detailed explanations, see:** `references/variable_reference_patterns.md`
