# Variable & Element Reference Patterns

Complete guide for preventing and fixing variable/element reference errors in Salesforce Flows.

## Overview

Variable and element reference errors are the #1 cause of Flow deployment failures (45-60% of all deployment errors). This guide catalogs the most common errors, their root causes, fix patterns, and prevention strategies.

**Use this guide when**:
- Debugging reference errors before deployment
- Understanding validation script error messages
- Establishing coding standards for Flow development
- Training team members on Flow best practices

---

## Reference Error Catalog

### Error #1: Undeclared Variable Reference

**Frequency:** 25% of all Flow errors (Very Common)

**Error Message:**
```
The flow failed to access the value for myVariable because it hasn't been set or assigned.
```

**Root Cause:**
- Variable referenced in element but never declared in Flow variables section
- Typo in variable name (e.g., `totalAmout` vs `totalAmount`)
- Variable was deleted but references remain

**Fix Pattern:**

**Scenario A: Variable missing entirely**
```xml
<!-- BAD: Variable not declared -->
<assignments>
    <name>Assignment_Calculate</name>
    <assignmentItems>
        <assignToReference>totalAmount</assignToReference>  <!-- ❌ Variable doesn't exist -->
        <operator>Assign</operator>
        <value>
            <numberValue>100</numberValue>
        </value>
    </assignmentItems>
</assignments>

<!-- GOOD: Declare variable first -->
<variables>
    <name>totalAmount</name>
    <dataType>Number</dataType>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
    <scale>2</scale>
</variables>

<assignments>
    <name>Assignment_Calculate</name>
    <assignmentItems>
        <assignToReference>totalAmount</assignToReference>  <!-- ✅ Variable exists -->
        <operator>Assign</operator>
        <value>
            <numberValue>100</numberValue>
        </value>
    </assignmentItems>
</assignments>
```

**Scenario B: Typo in variable name**
```xml
<!-- BAD: Typo in reference -->
<assignmentItems>
    <assignToReference>totalAmout</assignToReference>  <!-- ❌ Typo: 'Amout' -->
</assignmentItems>

<!-- GOOD: Correct spelling -->
<assignmentItems>
    <assignToReference>totalAmount</assignToReference>  <!-- ✅ Correct -->
</assignmentItems>
```

**Prevention Checklist:**
- [ ] Run `validate_flow.py` before deployment to catch undeclared variables
- [ ] Use consistent naming conventions (camelCase for variables)
- [ ] Copy-paste variable names instead of retyping
- [ ] Use Flow Builder's variable picker (reduces typos)
- [ ] Document all variables at top of Flow with descriptions

---

### Error #2: Invalid Element Reference in Connector

**Frequency:** 18% of all Flow errors (Very Common)

**Error Message:**
```
The flow tried to reference Screen_2 via a connection, but the element was not found.
```

**Root Cause:**
- Element renamed but connector not updated
- Element deleted but connector remains
- Typo in targetReference
- Wrong element type referenced (e.g., referencing a choice instead of an element)

**Fix Pattern:**

```xml
<!-- BAD: Element 'Screen_Confirmation' doesn't exist -->
<connector>
    <targetReference>Screen_Confirmation</targetReference>  <!-- ❌ Element not found -->
</connector>

<!-- GOOD: Reference existing element -->
<screens>
    <name>Screen_Confirm</name>  <!-- Element exists -->
    <label>Confirmation Screen</label>
</screens>

<connector>
    <targetReference>Screen_Confirm</targetReference>  <!-- ✅ Matches existing element -->
</connector>
```

**Common Mistake: Referencing Choice Instead of Screen**
```xml
<!-- BAD: Referencing choice name directly -->
<connector>
    <targetReference>choiceYes</targetReference>  <!-- ❌ This is a choice, not an element -->
</connector>

<!-- GOOD: Reference the next element, choice determines path -->
<decisions>
    <name>Decision_Confirmation</name>
    <defaultConnector>
        <targetReference>Screen_Error</targetReference>
    </defaultConnector>
    <rules>
        <name>Rule_User_Confirmed</name>
        <conditionLogic>and</conditionLogic>
        <conditions>
            <leftValueReference>choiceYes</leftValueReference>  <!-- ✅ Choice used in condition -->
            <operator>EqualTo</operator>
            <rightValue>
                <booleanValue>true</booleanValue>
            </rightValue>
        </conditions>
        <connector>
            <targetReference>Screen_Success</targetReference>  <!-- ✅ Connects to element -->
        </connector>
    </rules>
</decisions>
```

**Prevention Checklist:**
- [ ] Update all connectors when renaming elements
- [ ] Use Find & Replace when renaming elements (in XML)
- [ ] Run validation after deleting any element
- [ ] Keep element names descriptive (Screen_Input, Assignment_Calculate)
- [ ] Use consistent naming pattern (Type_Purpose)

---

### Error #3: Type Mismatch (Wrong Data Type)

**Frequency:** 15% of all Flow errors (Common)

**Error Message:**
```
An error occurred when executing a flow interview. The flow tried to update this reference but it didn't exist: myVariable. The referenced resource has a different data type than the value being assigned.
```

**Root Cause:**
- Assigning Text value to Number variable
- Assigning single value to Collection variable
- Assigning wrong SObject type to typed variable
- Date/DateTime confusion

**Fix Pattern:**

**Scenario A: Text vs Number**
```xml
<!-- BAD: Text assigned to Number variable -->
<variables>
    <name>recordCount</name>
    <dataType>Number</dataType>  <!-- Type: Number -->
</variables>

<assignments>
    <assignmentItems>
        <assignToReference>recordCount</assignToReference>
        <operator>Assign</operator>
        <value>
            <stringValue>10</stringValue>  <!-- ❌ String value -->
        </value>
    </assignmentItems>
</assignments>

<!-- GOOD: Number assigned to Number variable -->
<assignments>
    <assignmentItems>
        <assignToReference>recordCount</assignToReference>
        <operator>Assign</operator>
        <value>
            <numberValue>10</numberValue>  <!-- ✅ Number value -->
        </value>
    </assignmentItems>
</assignments>
```

**Scenario B: Single Value vs Collection**
```xml
<!-- BAD: Collection variable used as single value -->
<variables>
    <name>colAccounts</name>
    <dataType>SObject</dataType>
    <isCollection>true</isCollection>  <!-- It's a collection -->
    <objectType>Account</objectType>
</variables>

<recordCreates>
    <name>Create_Opportunity</name>
    <inputAssignments>
        <field>AccountId</field>
        <value>
            <elementReference>colAccounts.Id</elementReference>  <!-- ❌ Can't use collection ID directly -->
        </value>
    </inputAssignments>
</recordCreates>

<!-- GOOD: Use loop to process collection OR get first element -->
<!-- Option 1: Loop through collection -->
<loops>
    <name>Loop_Accounts</name>
    <collectionReference>colAccounts</collectionReference>
    <iterationOrder>Asc</iterationOrder>
    <nextValueConnector>
        <targetReference>Create_Opportunity</targetReference>
    </nextValueConnector>
</loops>

<recordCreates>
    <name>Create_Opportunity</name>
    <inputAssignments>
        <field>AccountId</field>
        <value>
            <elementReference>Loop_Accounts.Id</elementReference>  <!-- ✅ Current item from loop -->
        </value>
    </inputAssignments>
</recordCreates>

<!-- Option 2: Get first element -->
<assignments>
    <name>Assignment_Get_First</name>
    <assignmentItems>
        <assignToReference>firstAccount</assignToReference>
        <operator>Assign</operator>
        <value>
            <elementReference>colAccounts</elementReference>  <!-- ✅ Collection -->
        </value>
    </assignmentItems>
    <!-- Add filter to get FIRST using formula -->
</assignments>
```

**Prevention Checklist:**
- [ ] Match variable dataType to assigned value type
- [ ] Use Number for numeric values, not Text
- [ ] Use Currency for money values (auto-formats)
- [ ] Be explicit: Date vs DateTime
- [ ] Test with sample data to catch type mismatches early

---

### Error #4: Collection/Single Value Confusion

**Frequency:** 12% of all Flow errors (Common)

**Error Message:**
```
The flow tried to assign a collection to a variable that isn't a collection.
```

**Root Cause:**
- Get Records returns collection, assigned to single-value variable
- Loop item used outside loop context
- Misunderstanding isCollection flag

**Fix Pattern:**

```xml
<!-- BAD: Get Records returns collection, assigned to single variable -->
<variables>
    <name>selectedAccount</name>
    <dataType>SObject</dataType>
    <isCollection>false</isCollection>  <!-- Single value -->
    <objectType>Account</objectType>
</variables>

<recordLookups>
    <name>Get_Accounts</name>
    <assignNullValuesIfNoRecordsFound>false</assignNullValuesIfNoRecordsFound>
    <connector>
        <targetReference>Assignment_Store</targetReference>
    </connector>
    <object>Account</object>
    <storeOutputAutomatically>false</storeOutputAutomatically>
</recordLookups>

<assignments>
    <name>Assignment_Store</name>
    <assignmentItems>
        <assignToReference>selectedAccount</assignToReference>
        <operator>Assign</operator>
        <value>
            <elementReference>Get_Accounts</elementReference>  <!-- ❌ Collection assigned to single variable -->
        </value>
    </assignmentItems>
</assignments>

<!-- GOOD Option 1: Use collection variable -->
<variables>
    <name>colAccounts</name>
    <dataType>SObject</dataType>
    <isCollection>true</isCollection>  <!-- ✅ Collection variable -->
    <objectType>Account</objectType>
</variables>

<recordLookups>
    <name>Get_Accounts</name>
    <assignNullValuesIfNoRecordsFound>false</assignNullValuesIfNoRecordsFound>
    <connector>
        <targetReference>Assignment_Store</targetReference>
    </connector>
    <object>Account</object>
    <storeOutputAutomatically>false</storeOutputAutomatically>
</recordLookups>

<assignments>
    <name>Assignment_Store</name>
    <assignmentItems>
        <assignToReference>colAccounts</assignToReference>
        <operator>Assign</operator>
        <value>
            <elementReference>Get_Accounts</elementReference>  <!-- ✅ Collection to collection -->
        </value>
    </assignmentItems>
</assignments>

<!-- GOOD Option 2: Limit Get Records to single record -->
<recordLookups>
    <name>Get_First_Account</name>
    <assignNullValuesIfNoRecordsFound>false</assignNullValuesIfNoRecordsFound>
    <connector>
        <targetReference>Assignment_Store</targetReference>
    </connector>
    <object>Account</object>
    <queriedFields>Id</queriedFields>
    <queriedFields>Name</queriedFields>
    <sortField>CreatedDate</sortField>
    <sortOrder>Asc</sortOrder>
    <storeOutputAutomatically>false</storeOutputAutomatically>
    <getFirstRecordOnly>true</getFirstRecordOnly>  <!-- ✅ Returns single record -->
</recordLookups>

<assignments>
    <name>Assignment_Store</name>
    <assignmentItems>
        <assignToReference>selectedAccount</assignToReference>
        <operator>Assign</operator>
        <value>
            <elementReference>Get_First_Account</elementReference>  <!-- ✅ Single to single -->
        </value>
    </assignmentItems>
</assignments>
```

**Prevention Checklist:**
- [ ] Always use collection variables for Get Records output
- [ ] Use `getFirstRecordOnly=true` if you need only one record
- [ ] Prefix collection variables with `col` (colAccounts, colOpportunities)
- [ ] Check isCollection flag when declaring variables
- [ ] Loop through collections, don't assign directly to single variables

---

### Error #5: Null Reference (Variable Never Set)

**Frequency:** 10% of all Flow errors (Common)

**Error Message:**
```
An error occurred while the flow tried to look up a value of type String using ({!myVariable}).
```

**Root Cause:**
- Variable declared but never assigned a value
- Conditional path didn't execute (variable not set)
- Get Records found 0 records, variable is null
- Screen skipped, input variables not set

**Fix Pattern:**

```xml
<!-- BAD: Variable used without being set -->
<variables>
    <name>userEmail</name>
    <dataType>String</dataType>
</variables>
<!-- Variable never assigned -->

<recordCreates>
    <name>Create_Contact</name>
    <inputAssignments>
        <field>Email</field>
        <value>
            <elementReference>userEmail</elementReference>  <!-- ❌ Variable is null -->
        </value>
    </inputAssignments>
</recordCreates>

<!-- GOOD: Set default value or check for null -->
<!-- Option 1: Default value -->
<variables>
    <name>userEmail</name>
    <dataType>String</dataType>
    <value>
        <stringValue>noreply@example.com</stringValue>  <!-- ✅ Default value -->
    </value>
</variables>

<!-- Option 2: Check for null before using -->
<decisions>
    <name>Decision_Check_Email</name>
    <defaultConnector>
        <targetReference>Assignment_Set_Default_Email</targetReference>
    </defaultConnector>
    <rules>
        <name>Rule_Email_Has_Value</name>
        <conditionLogic>and</conditionLogic>
        <conditions>
            <leftValueReference>userEmail</leftValueReference>
            <operator>IsNull</operator>
            <rightValue>
                <booleanValue>false</booleanValue>  <!-- ✅ Check if NOT null -->
            </rightValue>
        </conditions>
        <connector>
            <targetReference>Create_Contact</targetReference>
        </connector>
    </rules>
</decisions>

<assignments>
    <name>Assignment_Set_Default_Email</name>
    <assignmentItems>
        <assignToReference>userEmail</assignToReference>
        <operator>Assign</operator>
        <value>
            <stringValue>noreply@example.com</stringValue>  <!-- ✅ Set default -->
        </value>
    </assignmentItems>
</assignments>
```

**Prevention Checklist:**
- [ ] Set default values for all variables
- [ ] Check IsNull before using optional variables
- [ ] Use Fault Connectors on Get Records (handle 0 results)
- [ ] Validate Screen inputs with required fields
- [ ] Test all conditional paths to ensure variables are set

---

### Error #6: Circular Reference

**Frequency:** 5% of all Flow errors (Occasional)

**Error Message:**
```
The flow contains a circular reference or infinite loop.
```

**Root Cause:**
- Connector points back to previous element creating infinite loop
- Recursive subflow call without exit condition
- Decision rule that always loops back to itself

**Fix Pattern:**

```xml
<!-- BAD: Circular reference -->
<decisions>
    <name>Decision_Check_Count</name>
    <rules>
        <name>Rule_Count_Too_Low</name>
        <conditions>
            <leftValueReference>recordCount</leftValueReference>
            <operator>LessThan</operator>
            <rightValue>
                <numberValue>10</numberValue>
            </rightValue>
        </conditions>
        <connector>
            <targetReference>Assignment_Increment</targetReference>  <!-- Goes to Assignment -->
        </connector>
    </rules>
</decisions>

<assignments>
    <name>Assignment_Increment</name>
    <assignmentItems>
        <assignToReference>recordCount</assignToReference>
        <operator>Add</operator>
        <value>
            <numberValue>1</numberValue>
        </value>
    </assignmentItems>
    <connector>
        <targetReference>Decision_Check_Count</targetReference>  <!-- ❌ Goes back to Decision: infinite loop -->
    </connector>
</assignments>

<!-- GOOD: Use Loop element or add exit condition -->
<!-- Option 1: Use Loop (recommended) -->
<loops>
    <name>Loop_Process_Records</name>
    <collectionReference>colRecords</collectionReference>
    <iterationOrder>Asc</iterationOrder>
    <nextValueConnector>
        <targetReference>Assignment_Process</targetReference>  <!-- ✅ Loop handles iteration -->
    </nextValueConnector>
    <noMoreValuesConnector>
        <targetReference>End</targetReference>
    </noMoreValuesConnector>
</loops>

<!-- Option 2: Add exit condition -->
<decisions>
    <name>Decision_Check_Count</name>
    <defaultConnector>
        <targetReference>End</targetReference>  <!-- ✅ Exit if no rule matches -->
    </defaultConnector>
    <rules>
        <name>Rule_Continue</name>
        <conditionLogic>and</conditionLogic>
        <conditions>
            <leftValueReference>recordCount</leftValueReference>
            <operator>LessThan</operator>
            <rightValue>
                <numberValue>10</numberValue>
            </rightValue>
        </conditions>
        <conditions>
            <leftValueReference>maxIterations</leftValueReference>
            <operator>LessThan</operator>
            <rightValue>
                <numberValue>100</numberValue>  <!-- ✅ Safety limit -->
            </rightValue>
        </conditions>
        <connector>
            <targetReference>Assignment_Increment</targetReference>
        </connector>
    </rules>
</decisions>
```

**Prevention Checklist:**
- [ ] Use Loop element instead of manual iteration
- [ ] Add maximum iteration counter as safety
- [ ] Ensure every loop has an exit condition
- [ ] Draw Flow diagram to visualize connections
- [ ] Test with edge cases (0 records, 1 record, 200 records)

---

### Error #7-10: Additional Common Errors (Summary)

**Error #7: Field Not Found on SObject (8%)**
- **Cause**: Referencing field that doesn't exist on object (typo, wrong API name, field deleted)
- **Fix**: Verify field API name in Setup, use correct field name, check field permissions

**Error #8: Invalid Formula Syntax (6%)**
- **Cause**: Syntax error in formula (missing parentheses, wrong function name, type mismatch in operations)
- **Fix**: Validate formula in Formula Builder, test with sample data, check function documentation

**Error #9: Incorrect Object Type in Get Records (4%)**
- **Cause**: Filtering by field that doesn't exist on queried object, relationship notation incorrect
- **Fix**: Verify field exists on object, use correct relationship syntax (Account.Name, not AccountName)

**Error #10: Screen Field Reference Error (3%)**
- **Cause**: Screen output not stored to variable, screen skipped so output is null
- **Fix**: Always store screen outputs to variables, check required fields, validate screen was displayed

---

## Variable Declaration Best Practices

### Naming Conventions

**Variables (camelCase):**
```
✅ GOOD:
- totalAmount
- selectedAccount
- isApproved
- recordCount
- colOpportunities (collection prefix)

❌ BAD:
- TotalAmount (PascalCase - use for elements)
- total_amount (snake_case - don't use)
- amt (too short, unclear)
- var1 (non-descriptive)
```

**Elements (PascalCase_With_Underscores):**
```
✅ GOOD:
- Screen_Input_Details
- Assignment_Calculate_Total
- Decision_Check_Status
- Get_Related_Opportunities

❌ BAD:
- screenInputDetails (camelCase - use for variables)
- screen1 (non-descriptive)
- Assignment1 (non-descriptive)
```

### Type Selection Guide

| Use Case | Data Type | Example |
|----------|-----------|---------|
| Whole numbers (count, quantity) | Number (scale=0) | recordCount: 42 |
| Decimals (percentage, rating) | Number (scale=2) | discountPercent: 15.50 |
| Money values | Currency | totalPrice: $1,234.56 |
| Text (names, descriptions) | String | customerName: "Acme Corp" |
| Yes/No flags | Boolean | isApproved: true |
| Date only (no time) | Date | birthDate: 1990-01-15 |
| Date with time | DateTime | createdDateTime: 2025-01-09T13:30:00Z |
| Single record | SObject (isCollection=false) | selectedAccount |
| Multiple records | SObject (isCollection=true) | colAccounts |
| Complex objects | Apex-Defined | customApexObject |

### Initialization Patterns

**Always Set Default Values:**
```xml
<!-- Text variables -->
<variables>
    <name>errorMessage</name>
    <dataType>String</dataType>
    <value>
        <stringValue></stringValue>  <!-- Empty string, not null -->
    </value>
</variables>

<!-- Number variables -->
<variables>
    <name>recordCount</name>
    <dataType>Number</dataType>
    <scale>0</scale>
    <value>
        <numberValue>0</numberValue>  <!-- Zero, not null -->
    </value>
</variables>

<!-- Boolean variables -->
<variables>
    <name>hasError</name>
    <dataType>Boolean</dataType>
    <value>
        <booleanValue>false</booleanValue>  <!-- Explicit false, not null -->
    </value>
</variables>

<!-- Collection variables -->
<variables>
    <name>colResults</name>
    <dataType>SObject</dataType>
    <isCollection>true</isCollection>
    <objectType>Account</objectType>
    <!-- Collections start as empty, no default value needed -->
</variables>
```

---

## Scope and Visibility Rules

### Variable Scope

**Global Scope**: Variables are accessible anywhere in the Flow after declaration
- Declared in "Variables" section
- Available in all elements
- Persist throughout Flow execution

**Loop Scope**: Loop iteration variable only accessible within loop
```xml
<loops>
    <name>Loop_Accounts</name>
    <collectionReference>colAccounts</collectionReference>
    <iterationOrder>Asc</iterationOrder>
    <!-- Loop_Accounts is only accessible within loop body -->
</loops>

<!-- ❌ Cannot reference Loop_Accounts outside loop -->
<assignments>
    <name>Assignment_After_Loop</name>
    <assignmentItems>
        <assignToReference>lastAccount</assignToReference>
        <operator>Assign</operator>
        <value>
            <elementReference>Loop_Accounts</elementReference>  <!-- ERROR: Loop variable out of scope -->
        </value>
    </assignmentItems>
</assignments>

<!-- ✅ Store loop item to Flow variable inside loop -->
<loops>
    <name>Loop_Accounts</name>
    <collectionReference>colAccounts</collectionReference>
    <nextValueConnector>
        <targetReference>Assignment_Store_Current</targetReference>
    </nextValueConnector>
</loops>

<assignments>
    <name>Assignment_Store_Current</name>
    <assignmentItems>
        <assignToReference>currentAccount</assignToReference>  <!-- Flow variable -->
        <operator>Assign</operator>
        <value>
            <elementReference>Loop_Accounts</elementReference>  <!-- ✅ Loop variable inside loop -->
        </value>
    </assignmentItems>
</assignments>
```

### Input/Output Variables

**Input Variables**: Set when Flow starts
- `isInput=true`
- Passed from button, Process Builder, Apex, or other Flow
- Must be set before Flow runs (or use default value)

**Output Variables**: Returned when Flow completes
- `isOutput=true`
- Accessible to calling process
- Useful for subflows returning calculated values

```xml
<!-- Input variable example -->
<variables>
    <name>inputAccountId</name>
    <dataType>String</dataType>
    <isInput>true</isInput>
    <isOutput>false</isOutput>
</variables>

<!-- Output variable example -->
<variables>
    <name>outputMessage</name>
    <dataType>String</dataType>
    <isInput>false</isInput>
    <isOutput>true</isOutput>
</variables>
```

---

## Troubleshooting Guide

### Debugging Strategy

**Step 1: Run Validation Script**
```bash
python3 validate_flow.py MyFlow.flow-meta.xml --format markdown > report.md
```

**Step 2: Check Validation Report**
- Fix all ERROR items first
- Address WARNINGS for best practices
- Re-run validation until clean

**Step 3: Enable Debug Logs (if deployed)**
```
1. Setup → Debug Logs → New
2. Select traced entity (User or Automated Process)
3. Set log filters:
   - Workflow: DEBUG
   - Apex Code: FINE
4. Run Flow
5. Review log: Setup → Debug Logs → View → Filter "FLOW_"
```

**Step 4: Look for These Log Entries**
```
FLOW_CREATE_INTERVIEW_BEGIN
FLOW_ELEMENT_BEGIN: Screen_Input
FLOW_ELEMENT_ERROR: Assignment_1 - Variable 'totalAmount' not found
FLOW_CREATE_INTERVIEW_ERROR
```

### Common Debug Patterns

**Pattern 1: Variable Not Set**
```
DEBUG|Variable {!myVar} is null
→ Check: Is variable assigned before use?
→ Fix: Add Assignment or set default value
```

**Pattern 2: Wrong Element Referenced**
```
DEBUG|Element Screen_2 not found in connection
→ Check: Was element renamed or deleted?
→ Fix: Update connector targetReference
```

**Pattern 3: Type Mismatch**
```
DEBUG|Cannot assign Text value to Number variable
→ Check: Variable dataType vs assigned value type
→ Fix: Match types or use formula to convert (TEXT(), VALUE())
```

### Quick Reference Checklist

Before deployment, verify:
- [ ] All variables declared before use
- [ ] All element references valid (no orphaned connectors)
- [ ] Variable types match assigned values
- [ ] Collections vs single values used correctly
- [ ] Default values set for all variables
- [ ] No circular references or infinite loops
- [ ] Fault connectors on elements that can fail (Get Records, Create Records)
- [ ] Naming conventions followed (camelCase variables, PascalCase elements)
- [ ] Validation script passes with 0 errors

---

## Additional Patterns (Coming Soon)

<!-- TODO: Add new patterns as discovered through usage -->

**Future Topics**:
- Platform Events in Flows
- Record-Triggered Flow recursion patterns
- Complex formula debugging techniques
- Cross-object variable references
- Apex-defined data types in Flows

**Contribution Template**:
```
### Error #XX: [Error Name]

**Frequency:** [Percentage]
**Error Message:** [Exact message]
**Root Cause:** [Why it happens]
**Fix Pattern:** [Code example]
**Prevention Checklist:** [Steps to avoid]
```

---

**Last Updated:** 2025-01-09
**Version:** 1.0
**Maintained by:** salesforce-flow-expert skill
