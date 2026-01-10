# Governor Limits Optimization

Comprehensive guide for optimizing Flows to avoid governor limit errors and maximize performance.

## Governor Limits Overview

### Per-Transaction Limits

| Resource | Limit | Applies To |
|----------|-------|------------|
| **SOQL queries** | 100 | Get Records elements |
| **DML statements** | 150 | Create/Update/Delete Records |
| **Records per DML** | 10,000 | Batch size |
| **Total heap size** | 6 MB (sync) / 12 MB (async) | Variables, collections |
| **CPU time** | 10,000 ms | All processing |
| **Callouts** | 100 | External services |

**Key Rule**: Limits apply PER TRANSACTION, not per Flow run.
- Bulk operations (200 records) = 1 transaction
- Multiple Flows triggered = shared limits

---

## DML Optimization Patterns

### Anti-Pattern: DML in Loop

```xml
<!-- ❌ BAD: DML inside loop (150 DML limit exceeded with 200 records) -->
<loops>
    <name>Loop_Through_Accounts</name>
    <collectionReference>colAccounts</collectionReference>
    <iterationOrder>Asc</iterationOrder>

    <nextValueConnector>
        <targetReference>Update_Account</targetReference>  <!-- Runs 200 times! -->
    </nextValueConnector>
</loops>

<recordUpdates>
    <name>Update_Account</name>
    <inputReference>Loop_Through_Accounts</inputReference>  <!-- ❌ DML in loop -->
    <object>Account</object>
</recordUpdates>
```

**Error with 200 records:**
```
System.LimitException: Too many DML statements: 151
```

---

### Correct Pattern: Batch DML After Loop

```xml
<!-- ✅ GOOD: Collect in loop, batch DML after -->

<!-- Step 1: Collect records in loop -->
<loops>
    <name>Loop_Through_Accounts</name>
    <collectionReference>colAccounts</collectionReference>
    <iterationOrder>Asc</iterationOrder>

    <nextValueConnector>
        <targetReference>Assignment_Calculate</targetReference>
    </nextValueConnector>
    <noMoreValuesConnector>
        <targetReference>Update_All_Accounts</targetReference>  <!-- After loop -->
    </noMoreValuesConnector>
</loops>

<!-- Step 2: Process each record -->
<assignments>
    <name>Assignment_Calculate</name>
    <assignmentItems>
        <assignToReference>Loop_Through_Accounts.Discount__c</assignToReference>
        <operator>Assign</operator>
        <value>
            <elementReference>Formula_Calculate_Discount</elementReference>
        </value>
    </assignmentItems>
</assignments>

<!-- Step 3: Batch update AFTER loop (1 DML for all 200 records) -->
<recordUpdates>
    <name>Update_All_Accounts</name>
    <inputReference>colAccounts</inputReference>  <!-- ✅ Collection updated at once -->
    <object>Account</object>
</recordUpdates>
```

**Result**: 1 DML statement for 200 records ✅

---

### Pattern: Update Collection in Loop

When you need to modify records in a loop:

```xml
<!-- Create collection to store modified records -->
<variables>
    <name>colAccountsToUpdate</name>
    <dataType>SObject</dataType>
    <isCollection>true</isCollection>
    <objectType>Account</objectType>
</variables>

<loops>
    <name>Loop_Accounts</name>
    <collectionReference>colAccounts</collectionReference>

    <nextValueConnector>
        <targetReference>Decision_Check_Criteria</targetReference>
    </nextValueConnector>
    <noMoreValuesConnector>
        <targetReference>Update_Filtered_Accounts</targetReference>
    </noMoreValuesConnector>
</loops>

<!-- Process only matching records -->
<decisions>
    <name>Decision_Check_Criteria</name>
    <rules>
        <name>Meets_Criteria</name>
        <conditionLogic>and</conditionLogic>
        <conditions>
            <leftValueReference>Loop_Accounts.Status__c</leftValueReference>
            <operator>EqualTo</operator>
            <rightValue>
                <stringValue>Active</stringValue>
            </rightValue>
        </conditions>
        <connector>
            <targetReference>Assignment_Modify_And_Add</targetReference>
        </connector>
    </rules>
    <defaultConnector>
        <targetReference>Loop_Accounts</targetReference>  <!-- Skip this record -->
    </defaultConnector>
</decisions>

<!-- Modify and add to collection -->
<assignments>
    <name>Assignment_Modify_And_Add</name>
    <assignmentItems>
        <assignToReference>Loop_Accounts.Discount__c</assignToReference>
        <operator>Assign</operator>
        <value>
            <numberValue>10</numberValue>
        </value>
    </assignmentItems>
    <assignmentItems>
        <assignToReference>colAccountsToUpdate</assignToReference>
        <operator>Add</operator>  <!-- Add to collection -->
        <value>
            <elementReference>Loop_Accounts</elementReference>
        </value>
    </assignmentItems>
    <connector>
        <targetReference>Loop_Accounts</targetReference>
    </connector>
</assignments>

<!-- Batch update -->
<recordUpdates>
    <name>Update_Filtered_Accounts</name>
    <inputReference>colAccountsToUpdate</inputReference>
    <object>Account</object>
</recordUpdates>
```

---

## SOQL Optimization Patterns

### Anti-Pattern: SOQL in Loop

```xml
<!-- ❌ BAD: Get Records inside loop (100 SOQL limit exceeded with 200 accounts) -->
<loops>
    <name>Loop_Accounts</name>
    <collectionReference>colAccounts</collectionReference>

    <nextValueConnector>
        <targetReference>Get_Related_Opportunities</targetReference>  <!-- Runs 200 times! -->
    </nextValueConnector>
</loops>

<recordLookups>
    <name>Get_Related_Opportunities</name>
    <filters>
        <field>AccountId</field>
        <operator>EqualTo</operator>
        <value>
            <elementReference>Loop_Accounts.Id</elementReference>
        </value>
    </filters>
    <object>Opportunity</object>
</recordLookups>
```

**Error with 200 accounts:**
```
System.LimitException: Too many SOQL queries: 101
```

---

### Correct Pattern: Query Before Loop, Filter in Memory

```xml
<!-- ✅ GOOD: Query all related records once, filter in loop -->

<!-- Step 1: Get ALL Accounts -->
<recordLookups>
    <name>Get_Accounts</name>
    <object>Account</object>
    <queriedFields>Id</queriedFields>
    <queriedFields>Name</queriedFields>
    <storeOutputAutomatically>true</storeOutputAutomatically>
</recordLookups>

<!-- Step 2: Get ALL related Opportunities (1 SOQL query) -->
<recordLookups>
    <name>Get_All_Opportunities</name>
    <filters>
        <field>AccountId</field>
        <operator>In</operator>
        <value>
            <elementReference>Get_Accounts</elementReference>  <!-- All Account IDs -->
        </value>
    </filters>
    <object>Opportunity</object>
    <queriedFields>Id</queriedFields>
    <queriedFields>AccountId</queriedFields>
    <queriedFields>Amount</queriedFields>
    <storeOutputAutomatically>true</storeOutputAutomatically>
</recordLookups>

<!-- Step 3: Loop and filter in memory -->
<loops>
    <name>Loop_Accounts</name>
    <collectionReference>Get_Accounts</collectionReference>

    <nextValueConnector>
        <targetReference>Loop_Opportunities</targetReference>
    </nextValueConnector>
</loops>

<!-- Inner loop to find matching opportunities -->
<loops>
    <name>Loop_Opportunities</name>
    <collectionReference>Get_All_Opportunities</collectionReference>

    <nextValueConnector>
        <targetReference>Decision_Match_Account</targetReference>
    </nextValueConnector>
    <noMoreValuesConnector>
        <targetReference>Loop_Accounts</targetReference>
    </noMoreValuesConnector>
</loops>

<decisions>
    <name>Decision_Match_Account</name>
    <rules>
        <name>Opportunity_Matches_Account</name>
        <conditionLogic>and</conditionLogic>
        <conditions>
            <leftValueReference>Loop_Opportunities.AccountId</leftValueReference>
            <operator>EqualTo</operator>
            <rightValue>
                <elementReference>Loop_Accounts.Id</elementReference>
            </rightValue>
        </conditions>
        <connector>
            <targetReference>Assignment_Process_Opportunity</targetReference>
        </connector>
    </rules>
    <defaultConnector>
        <targetReference>Loop_Opportunities</targetReference>
    </defaultConnector>
</decisions>
```

**Result**: 2 SOQL queries for 200 accounts + 1000 opportunities ✅

---

## Loop Optimization

### Early Exit Pattern

Stop loop when condition met (avoid unnecessary processing):

```xml
<variables>
    <name>foundMatch</name>
    <dataType>Boolean</dataType>
    <value>
        <booleanValue>false</booleanValue>
    </value>
</variables>

<loops>
    <name>Loop_Find_Match</name>
    <collectionReference>colAccounts</collectionReference>

    <nextValueConnector>
        <targetReference>Decision_Check_Exit</targetReference>
    </nextValueConnector>
</loops>

<decisions>
    <name>Decision_Check_Exit</name>
    <rules>
        <name>Already_Found</name>
        <conditionLogic>and</conditionLogic>
        <conditions>
            <leftValueReference>foundMatch</leftValueReference>
            <operator>EqualTo</operator>
            <rightValue>
                <booleanValue>true</booleanValue>
            </rightValue>
        </conditions>
        <connector>
            <targetReference>End</targetReference>  <!-- Exit loop early -->
        </connector>
    </rules>
    <defaultConnector>
        <targetReference>Decision_Check_Match</targetReference>
    </defaultConnector>
</decisions>
```

### Chunked Processing Pattern

Process large datasets in chunks to avoid heap size limits:

```xml
<!-- Limit Get Records to reasonable batch size -->
<recordLookups>
    <name>Get_First_1000_Records</name>
    <object>Account</object>
    <getFirstRecordOnly>false</getFirstRecordOnly>
    <queriedFields>Id</queriedFields>
    <queriedFields>Name</queriedFields>
    <sortField>CreatedDate</sortField>
    <sortOrder>Asc</sortOrder>
    <limitToNumberOfRecords>1000</limitToNumberOfRecords>  <!-- Chunk size -->
</recordLookups>
```

For Schedule-Triggered Flows processing millions of records:
- Use batch Apex instead of Flow
- Or schedule multiple Flows with date filters

---

## Bulkification Checklist

Before deploying any Flow, verify:

### DML Operations
- [ ] No `recordCreates`, `recordUpdates`, or `recordDeletes` inside loops
- [ ] Collections used for batch operations (1 DML for all records)
- [ ] Total DML operations per transaction < 150

### SOQL Queries
- [ ] No `recordLookups` inside loops
- [ ] All queries before loops, filter in memory
- [ ] Total SOQL queries per transaction < 100

### Collection Processing
- [ ] Collections populated efficiently (Add operator, not repeated assignments)
- [ ] Large collections avoided (< 10,000 records)
- [ ] Memory-intensive operations minimized

### Performance
- [ ] Fast Field Updates used for Before-Save triggers (no DML needed)
- [ ] Decision logic optimized (avoid redundant checks)
- [ ] Formula complexity reasonable (< 5,000 characters)

---

## Performance Monitoring

### Check Flow Run History

```
Setup → Flows → [Flow Name] → Run History
```

Look for:
- **Bulk Errors**: Errors with 100+ records = bulkification issue
- **Timeout Errors**: CPU time exceeded = too complex
- **Limit Errors**: DML/SOQL limits = not optimized

### Debug Log Analysis

Enable Debug Logs:
```
Setup → Debug Logs → New → Select User → Workflow: DEBUG
```

Search for:
```
FLOW_ELEMENT_LIMIT_USAGE
```

Output example:
```
SOQL queries: 45 / 100
DML statements: 12 / 150
Heap size: 2.5 MB / 6 MB
CPU time: 3,400 ms / 10,000 ms
```

### Performance Best Practices

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| SOQL queries | < 50 | 50-80 | > 80 |
| DML statements | < 100 | 100-130 | > 130 |
| Heap size | < 3 MB | 3-5 MB | > 5 MB |
| CPU time | < 5,000 ms | 5,000-8,000 ms | > 8,000 ms |

---

## Common Optimization Scenarios

### Scenario 1: Cascade Updates

**Problem**: Update Account triggers Flow that updates 100 Opportunities (100 DML)

**Solution**:
```xml
<!-- Collect all Opportunities to update -->
<recordLookups>
    <name>Get_Related_Opportunities</name>
    <filters>
        <field>AccountId</field>
        <operator>EqualTo</operator>
        <value>
            <elementReference>$Record.Id</elementReference>
        </value>
    </filters>
    <object>Opportunity</object>
</recordLookups>

<!-- Loop to modify collection -->
<loops>
    <name>Loop_Update_Opportunities</name>
    <collectionReference>Get_Related_Opportunities</collectionReference>
    <nextValueConnector>
        <targetReference>Assignment_Update_Opportunity</targetReference>
    </nextValueConnector>
    <noMoreValuesConnector>
        <targetReference>Update_All_Opportunities</targetReference>
    </noMoreValuesConnector>
</loops>

<assignments>
    <name>Assignment_Update_Opportunity</name>
    <assignmentItems>
        <assignToReference>Loop_Update_Opportunities.Status__c</assignToReference>
        <operator>Assign</operator>
        <value>
            <stringValue>Updated</stringValue>
        </value>
    </assignmentItems>
</assignments>

<!-- Single DML for all Opportunities -->
<recordUpdates>
    <name>Update_All_Opportunities</name>
    <inputReference>Get_Related_Opportunities</inputReference>
    <object>Opportunity</object>
</recordUpdates>
```

**Result**: 1 SOQL + 1 DML (regardless of opportunity count)

---

### Scenario 2: Related Record Lookups

**Problem**: Loop through 200 Accounts, lookup Contact for each (200 SOQL)

**Solution**:
```xml
<!-- Get all Contacts in one query -->
<recordLookups>
    <name>Get_All_Contacts</name>
    <filters>
        <field>AccountId</field>
        <operator>In</operator>
        <value>
            <elementReference>colAccounts</elementReference>
        </value>
    </filters>
    <object>Contact</object>
</recordLookups>

<!-- Filter in loop using Decision -->
<loops>
    <name>Loop_Accounts</name>
    <collectionReference>colAccounts</collectionReference>
</loops>

<loops>
    <name>Loop_Contacts</name>
    <collectionReference>Get_All_Contacts</collectionReference>
</loops>

<decisions>
    <name>Decision_Match</name>
    <rules>
        <name>Contact_Belongs_To_Account</name>
        <conditions>
            <leftValueReference>Loop_Contacts.AccountId</leftValueReference>
            <operator>EqualTo</operator>
            <rightValue>
                <elementReference>Loop_Accounts.Id</elementReference>
            </rightValue>
        </conditions>
        <!-- Process matching contact -->
    </rules>
</decisions>
```

**Result**: 1 SOQL for all contacts ✅

---

**Last Updated:** 2025-01-09
**Version:** 1.0
