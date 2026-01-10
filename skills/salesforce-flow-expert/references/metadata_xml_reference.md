# Flow Metadata XML Reference

Complete reference for Flow-meta.xml structure, required elements, and API version differences.

## Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>
    <description>Flow description</description>
    <label>Flow Label</label>
    <processType>Flow</processType>
    <status>Draft</status>

    <!-- Variables, Elements, etc. -->
</Flow>
```

---

## Required vs Optional Elements

### Required Fields

| Element | Description | Valid Values |
|---------|-------------|--------------|
| `apiVersion` | Salesforce API version | 50.0-70.0 (typically 58.0-61.0) |
| `status` | Flow activation status | Draft, Active, Obsolete, InvalidDraft |
| `processType` | Type of Flow | Flow, AutoLaunchedFlow, Workflow, etc. |
| `label` | Human-readable name | Any string (max 80 chars) |

### Optional But Recommended

| Element | Description | Example |
|---------|-------------|---------|
| `description` | Flow purpose/notes | "Automated discount calculation" |
| `interviewLabel` | Interview display name | "{!$Flow.CurrentDateTime}" |
| `processMetadataValues` | Builder-only metadata | Process Builder compatibility |

---

## processType Values

| Flow Type | processType Value | Additional Requirements |
|-----------|------------------|-------------------------|
| Screen Flow | `Flow` | None |
| Record-Triggered | `AutoLaunchedFlow` | `<start>` with `<triggerType>` |
| Schedule-Triggered | `AutoLaunchedFlow` | `<start>` with `<scheduledPaths>` |
| Autolaunched | `AutoLaunchedFlow` | None (input/output variables) |
| Platform Event-Triggered | `AutoLaunchedFlow` | `<start>` with `<triggerType>RecordAfterSave` |

---

## Element Ordering Requirements

**CRITICAL**: Elements MUST appear in this order in XML (alphabetical within categories).

### Metadata Section (Top)
```xml
<apiVersion>60.0</apiVersion>
<description>...</description>
<interviewLabel>...</interviewLabel>
<label>...</label>
<processType>...</processType>
<status>...</status>
```

### Variables Section
```xml
<variables>
    <name>myVariable</name>
    <dataType>String</dataType>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
</variables>
```

### Start Section (for triggered flows)
```xml
<start>
    <!-- Configuration depends on trigger type -->
</start>
```

### Elements Section (Alphabetically)
- `actionCalls`
- `assignments`
- `choices`
- `decisions`
- `loops`
- `recordCreates`
- `recordDeletes`
- `recordLookups`
- `recordUpdates`
- `screens`
- `subflows`
- `waits`

**Note**: Wrong order causes deployment failure with cryptic errors.

---

## Variable Declaration

### Basic Variable
```xml
<variables>
    <name>totalAmount</name>
    <dataType>Currency</dataType>
    <scale>2</scale>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
</variables>
```

### Data Types

| dataType | Use For | Additional Fields |
|----------|---------|-------------------|
| `String` | Text | maxlength (optional) |
| `Number` | Integer/decimal | `scale` (decimal places, default 0) |
| `Currency` | Money | `scale` (decimal places, default 2) |
| `Boolean` | True/false | None |
| `Date` | Date only | None |
| `DateTime` | Date + time | None |
| `SObject` | Salesforce record | `objectType` (required) |
| `Apex` | Apex-defined class | `apexClass` (required) |

### Collection Variable
```xml
<variables>
    <name>colAccounts</name>
    <dataType>SObject</dataType>
    <isCollection>true</isCollection>
    <objectType>Account</objectType>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
</variables>
```

### Input/Output Variables
```xml
<!-- Input -->
<variables>
    <name>inputAccountId</name>
    <dataType>String</dataType>
    <isInput>true</isInput>
    <isOutput>false</isOutput>
</variables>

<!-- Output -->
<variables>
    <name>outputMessage</name>
    <dataType>String</dataType>
    <isInput>false</isInput>
    <isOutput>true</isOutput>
</variables>
```

---

## API Version Differences

### v60.0+ (Spring '24)
- Enhanced Fault handling
- Improved Performance optimization
- New element types

### v58.0-59.0 (2023)
- Record-Triggered Flow improvements
- Platform Event triggers
- Enhanced debugging

### v56.0-57.0 (2022)
- Before-Save optimization (`<optimizeForPerformance>`)
- Fast Field Updates
- Improved bulkification

### v50.0-55.0 (Pre-2022)
- Basic Flow functionality
- Process Builder migration support

**Recommendation**: Use latest supported version (60.0-61.0) for new Flows.

---

## Common Metadata Errors

### Error 1: Wrong Element Order
```xml
<!-- BAD: status before processType -->
<Flow>
    <apiVersion>60.0</apiVersion>
    <status>Draft</status>
    <processType>Flow</processType>  <!-- ❌ Wrong order -->
</Flow>

<!-- GOOD: Alphabetical order -->
<Flow>
    <apiVersion>60.0</apiVersion>
    <processType>Flow</processType>
    <status>Draft</status>  <!-- ✅ Correct order -->
</Flow>
```

### Error 2: Missing Required Field
```xml
<!-- BAD: Missing apiVersion -->
<Flow>
    <label>My Flow</label>
    <status>Draft</status>
</Flow>

<!-- GOOD: All required fields -->
<Flow>
    <apiVersion>60.0</apiVersion>
    <label>My Flow</label>
    <processType>Flow</processType>
    <status>Draft</status>
</Flow>
```

### Error 3: Invalid processType for Flow Type
```xml
<!-- BAD: Screen Flow with AutoLaunchedFlow -->
<Flow>
    <apiVersion>60.0</apiVersion>
    <processType>AutoLaunchedFlow</processType>  <!-- ❌ Wrong for Screen Flow -->
    <screens>...</screens>
</Flow>

<!-- GOOD: Screen Flow with correct processType -->
<Flow>
    <apiVersion>60.0</apiVersion>
    <processType>Flow</processType>  <!-- ✅ Correct -->
    <screens>...</screens>
</Flow>
```

---

## Flow Type-Specific Metadata

### Screen Flow
```xml
<Flow>
    <apiVersion>60.0</apiVersion>
    <processType>Flow</processType>
    <status>Draft</status>
    <label>My Screen Flow</label>

    <!-- Screens and user interaction -->
    <screens>...</screens>
</Flow>
```

### Record-Triggered Flow
```xml
<Flow>
    <apiVersion>60.0</apiVersion>
    <processType>AutoLaunchedFlow</processType>
    <status>Draft</status>
    <label>Account After Insert</label>

    <start>
        <object>Account</object>
        <recordTriggerType>Create</recordTriggerType>
        <triggerType>RecordAfterSave</triggerType>

        <!-- Entry criteria (optional) -->
        <filterLogic>and</filterLogic>
        <filters>
            <field>Type</field>
            <operator>EqualTo</operator>
            <value><stringValue>Customer</stringValue></value>
        </filters>
    </start>
</Flow>
```

### Schedule-Triggered Flow
```xml
<Flow>
    <apiVersion>60.0</apiVersion>
    <processType>AutoLaunchedFlow</processType>
    <status>Draft</status>
    <label>Daily Cleanup</label>

    <start>
        <object>Opportunity</object>
        <scheduledPaths>
            <name>Daily_Path</name>
            <pathType>AsyncAfterCommit</pathType>
            <schedule>
                <frequency>Daily</frequency>
                <startDate>2025-01-01</startDate>
                <startTime>02:00:00</startTime>
            </schedule>
        </scheduledPaths>
    </start>
</Flow>
```

---

## Deployment Package Structure

### Minimal Package
```
force-app/main/default/flows/
├── MyFlow.flow-meta.xml
```

### Full SFDX Package
```
force-app/
└── main/
    └── default/
        ├── flows/
        │   ├── MyFlow.flow-meta.xml
        │   └── AnotherFlow.flow-meta.xml
        └── package.xml
```

### package.xml Example
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>MyFlow</members>
        <members>AnotherFlow</members>
        <name>Flow</name>
    </types>
    <version>60.0</version>
</Package>
```

---

## Validation Checklist

Before deploying:
- [ ] `apiVersion` present and valid (50.0-70.0)
- [ ] `status` present (Draft or Active)
- [ ] `processType` matches Flow type
- [ ] `label` present
- [ ] Elements in correct alphabetical order
- [ ] Variables declared before use
- [ ] No duplicate element names
- [ ] All required fields for element types
- [ ] Proper namespace (`xmlns="http://soap.sforce.com/2006/04/metadata"`)

---

**Last Updated:** 2025-01-09
**Version:** 1.0
