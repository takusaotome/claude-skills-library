---
name: salesforce-expert
description: Expert guidance for Salesforce system development and operations management. Use this skill when working with Salesforce configuration, customization, bug analysis, troubleshooting access/permission issues, designing system architecture, or implementing custom Apex/LWC development. Covers sharing settings, approval processes, trigger patterns, integration design, and data modeling best practices.
---

# Salesforce Expert

## Overview

This skill provides comprehensive guidance for Salesforce system development and operations management, covering configuration, customization, bug analysis, architecture design, and custom development patterns. Use this skill when encountering Salesforce-specific challenges, designing solutions, or troubleshooting issues related to permissions, approval processes, integrations, or custom code.

## When to Use This Skill

Invoke this skill when:

- **Settings & Customization**: Configuring sharing settings, approval processes, validation rules, page layouts, or record types
- **Bug Analysis & Troubleshooting**: Diagnosing access denied issues, approval process errors, missing relationships, or integration failures
- **Architecture Design**: Planning data models, object relationships, integration patterns, or scalability strategies
- **Custom Development**: Implementing Apex triggers, batch jobs, Lightning Web Components, or REST APIs
- **Security & Permissions**: Resolving OWD settings, sharing rules, role hierarchy, or field-level security issues
- **Performance Optimization**: Addressing governor limit issues, slow queries, or large data volume challenges

## Core Capabilities

### 1. Sharing Settings & Access Control

Troubleshoot and configure Salesforce's multi-layered security model.

**Common Scenarios**:

**Issue: User cannot access related records**
```
Example: Opportunity Owner changed, but new owner cannot see related Contacts

Diagnosis Process:
1. Check Contact OWD setting (Setup → Sharing Settings)
2. Verify Contact ownership
3. Check role hierarchy relationship
4. Review sharing rules
5. Query ContactShare records for access grants

Solutions:
- Change Contact OWD to "Controlled by Parent"
- Create sharing rule based on Opportunity Owner
- Implement Apex sharing in trigger
- Add user to Account Team
```

**Issue: Lead conversion sharing**
```
Example: After Lead conversion, converter loses access to created Contact/Account

Solutions:
- Enable "Grant Access Using Hierarchies"
- Create sharing rules for converters
- Implement team-based sharing
- Use Apex to grant manual sharing
```

**Reference**: Load `references/sharing_settings_guide.md` for comprehensive troubleshooting checklist, common access patterns, Apex sharing code examples, and performance considerations.

**Key Apex Pattern**:
```apex
// Share Contact with Opportunity Owner
public static void shareContactWithOwner(Id contactId, Id ownerId) {
    ContactShare share = new ContactShare(
        ContactId = contactId,
        UserOrGroupId = ownerId,
        ContactAccessLevel = 'Read',
        RowCause = Schema.ContactShare.RowCause.Manual
    );
    insert share;
}
```

### 2. Approval Process Configuration & Troubleshooting

Design, implement, and debug approval processes.

**Common Scenarios**:

**Issue: "No applicable approval process was found"**
```
Diagnosis:
1. Verify active approval process exists for object
2. Check entry criteria matches record
3. Confirm record not already in approval
4. Review filter criteria if using auto-submission

Debug Query:
SELECT Name, TableEnumOrId, State
FROM ProcessDefinition
WHERE TableEnumOrId = 'Opportunity' AND State = 'Active'
```

**Issue: Wrong approver assigned**
```
Solutions:
- Validate user field is populated and user active
- Check queue membership
- Specify fallback approver in process
- Implement Apex-based dynamic assignment
```

**Issue: Can bypass approval by direct edit**
```
Solution: Validation Rule
AND(
    ISCHANGED(Discount_Percent__c),
    TEXT(Status__c) = 'Approved',
    $Profile.Name <> 'System Administrator'
)
Error: Cannot edit approved record. Submit for re-approval.
```

**Reference**: Load `references/approval_process_guide.md` for approval patterns (single-step, multi-step, parallel, conditional), submission methods, action configuration, testing strategies, and monitoring queries.

**Apex Submission Pattern**:
```apex
Approval.ProcessSubmitRequest req = new Approval.ProcessSubmitRequest();
req.setObjectId(recordId);
req.setSubmitterId(UserInfo.getUserId());
req.setComments('Submitted via automation');

Approval.ProcessResult result = Approval.process(req);
if (result.isSuccess()) {
    System.debug('Submitted: ' + result.getInstanceId());
}
```

### 3. Custom Development Best Practices

Implement scalable, maintainable Apex and Lightning Web Components.

**Trigger Handler Pattern**:
```apex
// Trigger (minimal logic)
trigger OpportunityTrigger on Opportunity (before insert, before update,
                                          after insert, after update) {
    OpportunityTriggerHandler.execute();
}

// Handler (all business logic)
public class OpportunityTriggerHandler {

    private static Boolean isExecuting = false;

    public static void execute() {
        if (isExecuting) return; // Prevent recursion

        isExecuting = true;
        try {
            if (Trigger.isBefore) {
                if (Trigger.isInsert) handleBeforeInsert(Trigger.new);
                else if (Trigger.isUpdate) handleBeforeUpdate(Trigger.new, Trigger.oldMap);
            } else if (Trigger.isAfter) {
                if (Trigger.isInsert) handleAfterInsert(Trigger.new);
                else if (Trigger.isUpdate) handleAfterUpdate(Trigger.new, Trigger.oldMap);
            }
        } finally {
            isExecuting = false;
        }
    }

    private static void handleAfterUpdate(List<Opportunity> newOpps,
                                         Map<Id, Opportunity> oldMap) {
        List<Id> ownerChangedOpps = new List<Id>();

        for (Opportunity opp : newOpps) {
            if (opp.OwnerId != oldMap.get(opp.Id).OwnerId) {
                ownerChangedOpps.add(opp.Id);
            }
        }

        if (!ownerChangedOpps.isEmpty()) {
            OpportunityService.shareRelatedContactsWithNewOwner(ownerChangedOpps);
        }
    }
}
```

**Service Layer Pattern**:
```apex
public class OpportunityService {

    public static void shareRelatedContactsWithNewOwner(List<Id> opportunityIds) {
        // Query opportunities with contacts
        Map<Id, Opportunity> oppMap = new Map<Id, Opportunity>([
            SELECT Id, OwnerId, Customer_Tenant_Name__c
            FROM Opportunity
            WHERE Id IN :opportunityIds
            AND Customer_Tenant_Name__c != null
        ]);

        List<ContactShare> shares = new List<ContactShare>();

        for (Opportunity opp : oppMap.values()) {
            shares.add(new ContactShare(
                ContactId = opp.Customer_Tenant_Name__c,
                UserOrGroupId = opp.OwnerId,
                ContactAccessLevel = 'Read',
                RowCause = Schema.ContactShare.RowCause.Manual
            ));
        }

        if (!shares.isEmpty()) {
            Database.insert(shares, false);
        }
    }
}
```

**Lightning Web Component Pattern**:
```javascript
// opportunityList.js
import { LightningElement, wire } from 'lwc';
import getOpportunities from '@salesforce/apex/OpportunityController.getOpportunities';

export default class OpportunityList extends LightningElement {
    opportunities;
    error;

    @wire(getOpportunities)
    wiredOpportunities({ error, data }) {
        if (data) {
            this.opportunities = data;
            this.error = undefined;
        } else if (error) {
            this.error = error;
            this.opportunities = undefined;
        }
    }
}
```

**Reference**: Load `references/custom_development_patterns.md` for trigger frameworks, batch apex, queueable patterns, LWC communication, testing strategies, and governor limit optimization.

### 4. Architecture Design & Data Modeling

Design scalable, maintainable Salesforce architectures.

**Object Relationship Decision Matrix**:

| Criteria | Master-Detail | Lookup |
|----------|---------------|--------|
| Child independence | No | Yes |
| Roll-up summaries | Yes | No |
| Reparenting | No | Yes |
| Sharing inheritance | Yes | No |
| Delete cascade | Yes | No |

**Many-to-Many Pattern (Junction Object)**:
```
Project (Master) ←─ Project_Assignment (Junction) ─→ Resource (Master)

Project_Assignment__c:
- Project__c (Master-Detail to Project)
- Resource__c (Master-Detail to Resource)
- Role__c (Picklist: Developer, QA, PM)
- Allocation_Percent__c (Number: 0-100)
- Start_Date__c, End_Date__c
```

**Governor Limit Optimization**:
```apex
// BAD - SOQL in loop
for (Opportunity opp : Trigger.new) {
    Account acc = [SELECT Name FROM Account WHERE Id = :opp.AccountId];
    opp.Account_Name__c = acc.Name;
}

// GOOD - Bulkified with Map
Set<Id> accountIds = new Set<Id>();
for (Opportunity opp : Trigger.new) {
    accountIds.add(opp.AccountId);
}

Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name FROM Account WHERE Id IN :accountIds
]);

for (Opportunity opp : Trigger.new) {
    if (accountMap.containsKey(opp.AccountId)) {
        opp.Account_Name__c = accountMap.get(opp.AccountId).Name;
    }
}
```

**Integration Pattern - REST API**:
```apex
@RestResource(urlMapping='/api/opportunities/*')
global with sharing class OpportunityAPI {

    @HttpGet
    global static OpportunityResponse getOpportunity() {
        RestRequest req = RestContext.request;
        String oppId = req.requestURI.substring(req.requestURI.lastIndexOf('/') + 1);

        try {
            Opportunity opp = [
                SELECT Id, Name, Amount, StageName
                FROM Opportunity WHERE Id = :oppId LIMIT 1
            ];
            return new OpportunityResponse(true, 'Success', opp);
        } catch (Exception e) {
            return new OpportunityResponse(false, e.getMessage(), null);
        }
    }

    @HttpPost
    global static OpportunityResponse createOpportunity(OpportunityRequest reqBody) {
        try {
            Opportunity opp = new Opportunity(
                Name = reqBody.name,
                Amount = reqBody.amount,
                StageName = reqBody.stage,
                CloseDate = reqBody.closeDate
            );
            insert opp;
            return new OpportunityResponse(true, 'Created', opp);
        } catch (Exception e) {
            RestContext.response.statusCode = 400;
            return new OpportunityResponse(false, e.getMessage(), null);
        }
    }
}
```

**Reference**: Load `references/architecture_best_practices.md` for data modeling strategies, LDV design, indexing, governor limit patterns, integration patterns, security architecture, and testing strategies.

## Bug Analysis Workflow

When analyzing Salesforce bugs, follow this systematic approach:

### 1. Gather Context
- Record type and object involved
- User role and profile
- Error message (exact wording)
- Steps to reproduce
- Expected vs actual behavior

### 2. Categorize Issue
- **Access/Permissions**: Cannot view/edit records
- **Data Integrity**: Missing relationships, incorrect calculations
- **Process Automation**: Approval, workflow, validation errors
- **Integration**: API failures, callout errors
- **UI/UX**: Page layout, Lightning component issues

### 3. Diagnose Root Cause

**For Access Issues**:
1. Check OWD: Setup → Sharing Settings → Object Default Access
2. Check Record Ownership: Who owns the record?
3. Check Role Hierarchy: Is user above owner?
4. Check Sharing Rules: Any applicable rules?
5. Check Manual Shares: Query [Object]Share records
6. Check Profile/Permission Sets: Object-level and field-level access

**For Approval Issues**:
1. Verify active process exists
2. Check entry criteria matches record
3. Verify approver assignment logic
4. Check user/queue active status
5. Query ProcessInstance for current state

**For Relationship Issues**:
1. Verify relationship type (Lookup vs Master-Detail)
2. Check Related Lists on page layout
3. Query junction objects if many-to-many
4. Verify field-level security on lookup fields

### 4. Propose Solutions

Provide multiple options ranked by:
- **Quick Fix**: Immediate workaround
- **Proper Solution**: Addresses root cause
- **Long-term**: Architectural improvement

Include code examples when applicable.

### 5. Document Fix

Include:
- Root cause analysis
- Solution implemented
- Testing steps
- Deployment considerations

## Best Practices

### Security

1. **Always use `with sharing`** unless specific reason
2. **Check CRUD/FLS** before DML operations
3. **Use `Security.stripInaccessible()`** for dynamic queries
4. **Principle of Least Privilege** for profiles and permission sets

### Performance

1. **Bulkify all code** - handle 200 records
2. **Avoid SOQL in loops** - use Maps for lookup
3. **Batch DML operations** - single insert/update/delete
4. **Use aggregate queries** instead of iterating in Apex
5. **Offload heavy processing** to Queueable or Batch

### Maintainability

1. **Separate concerns** - Trigger → Handler → Service
2. **Single responsibility** - One class/method, one purpose
3. **Test business logic** - Not just code coverage
4. **Document complex logic** - Comments and method headers
5. **Version control** - Use SFDX and Git

### Testing

1. **Test Data Factory** - Centralized test data creation
2. **Bulk Testing** - Always test with 200 records
3. **Mock Callouts** - HttpCalloutMock for API tests
4. **@testSetup** - Reuse test data across methods
5. **85%+ Coverage** - Test business logic thoroughly

## Resources

This skill includes comprehensive reference documentation:

### references/

**sharing_settings_guide.md**
- Organization-Wide Defaults (OWD) recommendations
- Common access issues with solutions
- Role hierarchy patterns
- Sharing rules (owner-based and criteria-based)
- Manual sharing via Apex
- Teams (Account Team, Opportunity Team)
- Troubleshooting checklist
- Performance and security best practices

**approval_process_guide.md**
- Approval process configuration patterns
- Single-step, multi-step, parallel, conditional approvals
- Submission methods (manual, Apex, Flow)
- Approval actions and assignments
- Common issues and solutions
- Testing strategies
- Monitoring and maintenance

**custom_development_patterns.md**
- Trigger handler and framework patterns
- Service layer pattern
- Batch Apex and Queueable patterns
- Lightning Web Components (wire, imperative, pub/sub)
- Testing patterns (factory, bulk, mock callouts)
- Bulkification and governor limit optimization
- Error handling and logging

**architecture_best_practices.md**
- Data modeling (Master-Detail vs Lookup, junction objects)
- Large Data Volume (LDV) design
- Governor limit management
- Scalability patterns
- Integration patterns (REST API, Platform Events)
- Security architecture
- Testing and CI/CD strategies

Load these references as needed to inform your analysis and solutions.

## Examples

### Example 1: Access Issue

**User Request**: "Manager created Opportunity, assigned to Rep. Rep cannot see related Contact."

**Analysis**:
1. Contact OWD is Private
2. Contact owned by Manager
3. Rep is not above Manager in role hierarchy
4. No sharing rule grants access

**Solution Options**:

**Option 1: Change OWD** (Quick)
```
Setup → Sharing Settings → Contact → "Controlled by Parent"
- Contact access inherits from Account
- If Rep has Opportunity, they get Account and Contact access
```

**Option 2: Sharing Rule** (Moderate)
```
Setup → Sharing Settings → Contact → New Sharing Rule
Based on: Opportunity Owner
Share with: Opportunity Owner's Role
Access: Read
```

**Option 3: Apex Trigger** (Long-term)
```apex
trigger OpportunityTrigger on Opportunity (after update) {
    for (Opportunity opp : Trigger.new) {
        if (opp.OwnerId != Trigger.oldMap.get(opp.Id).OwnerId) {
            ContactShare share = new ContactShare(
                ContactId = opp.Customer_Tenant_Name__c,
                UserOrGroupId = opp.OwnerId,
                ContactAccessLevel = 'Read',
                RowCause = Schema.ContactShare.RowCause.Manual
            );
            insert share;
        }
    }
}
```

### Example 2: Approval Process Error

**User Request**: "Getting 'No applicable approval process found' when submitting Residential Opportunity."

**Analysis**:
1. Check active processes: `SELECT Name FROM ProcessDefinition WHERE TableEnumOrId = 'Opportunity' AND State = 'Active'`
2. Review entry criteria: Must match record
3. Verify record not already in approval

**Solution**:
```
1. Activate approval process:
   Setup → Approval Processes → Opportunity → [Process Name] → Activate

2. Verify entry criteria:
   Entry Criteria: RecordType.Name = 'Residential'

3. Test with debug:
   Debug Logs → Set trace flag for user → Submit record → Review "Approval Process" entries
```

### Example 3: Integration Design

**User Request**: "Design REST API for external system to create Opportunities."

**Solution**:
```apex
@RestResource(urlMapping='/api/v1/opportunities/*')
global with sharing class OpportunityAPI {

    @HttpPost
    global static APIResponse createOpportunity(OpportunityRequest req) {
        Savepoint sp = Database.setSavepoint();

        try {
            // Validate required fields
            if (String.isBlank(req.name) || req.closeDate == null) {
                throw new ValidationException('Missing required fields');
            }

            // Find or create Account
            Account acc = findOrCreateAccount(req.accountName);

            // Create Opportunity
            Opportunity opp = new Opportunity(
                Name = req.name,
                AccountId = acc.Id,
                Amount = req.amount,
                StageName = req.stage != null ? req.stage : 'Prospecting',
                CloseDate = req.closeDate,
                External_ID__c = req.externalId
            );

            insert opp;

            return new APIResponse(true, 'Opportunity created', opp.Id);

        } catch (Exception e) {
            Database.rollback(sp);
            RestContext.response.statusCode = 400;
            return new APIResponse(false, e.getMessage(), null);
        }
    }

    private static Account findOrCreateAccount(String accountName) {
        List<Account> accounts = [
            SELECT Id FROM Account WHERE Name = :accountName LIMIT 1
        ];

        if (accounts.isEmpty()) {
            Account acc = new Account(Name = accountName);
            insert acc;
            return acc;
        }
        return accounts[0];
    }

    global class OpportunityRequest {
        public String name;
        public String accountName;
        public Decimal amount;
        public String stage;
        public Date closeDate;
        public String externalId;
    }

    global class APIResponse {
        public Boolean success;
        public String message;
        public String opportunityId;

        public APIResponse(Boolean success, String message, String oppId) {
            this.success = success;
            this.message = message;
            this.opportunityId = oppId;
        }
    }
}

// Test with cURL:
// curl -X POST https://instance.salesforce.com/services/apexrest/api/v1/opportunities/
//   -H "Authorization: Bearer TOKEN"
//   -H "Content-Type: application/json"
//   -d '{"name":"API Test Opp","accountName":"Test Account","amount":50000,"closeDate":"2025-12-31"}'
```

---

**Note**: This skill provides guidance and code examples. Always test solutions in a sandbox environment before deploying to production. Follow your organization's deployment and change management processes.
