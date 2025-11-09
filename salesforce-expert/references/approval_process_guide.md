# Salesforce Approval Process Guide

## Overview

This guide covers Salesforce approval process configuration, common issues, automation patterns, and troubleshooting strategies based on real-world implementations.

## Approval Process Architecture

### Components

1. **Initial Submission Actions** - Execute when record submitted
2. **Approval Steps** - One or more sequential or parallel approval stages
3. **Final Approval Actions** - Execute when all approvals granted
4. **Final Rejection Actions** - Execute when record rejected
5. **Recall Actions** - Execute when submitter recalls submission

### Process Behavior

- **Active/Inactive**: Only one active process per object (or multiple with entry criteria)
- **Entry Criteria**: Determines which records can be submitted
- **Filter Criteria**: Determines which records auto-submit to this process
- **Order**: Processes evaluated in order when multiple exist

## Common Configuration Patterns

### Pattern 1: Single-Step Approval

**Use Case**: Simple manager approval for expense reports

```
Entry Criteria: Amount > 1000
Approver: Direct Manager (User: Manager field)
Final Approval: Update Status = "Approved"
Final Rejection: Update Status = "Rejected"
```

**Configuration Steps**:
1. Setup → Approval Processes → Expense__c → New Approval Process
2. Entry Criteria: `Amount__c > 1000`
3. Approver: Automatically assign to: User field → `Manager__c`
4. Final Approval Actions: Field Update → Status = "Approved"
5. Final Rejection Actions: Field Update → Status = "Rejected"

### Pattern 2: Multi-Step Sequential Approval

**Use Case**: Contract approval requiring Legal then Finance approval

```
Step 1: Legal Review
- Entry Criteria: All Contracts
- Approver: Legal Team Queue
- Rejection behavior: Final Rejection

Step 2: Finance Review
- Entry Criteria: Contract Value > 100,000
- Approver: Finance Director
- Rejection behavior: Final Rejection
```

**Configuration**:
```
Process Entry Criteria: Record Type = "Contract"

Step 1: Legal Review
- Automatically assign to: Queue → Legal_Team
- Reject Behavior: Final Rejection

Step 2: Finance Review (if Step 1 approved)
- Step Criteria: Contract_Value__c > 100000
- Automatically assign to: User → Finance Director
- Reject Behavior: Final Rejection
```

### Pattern 3: Parallel Approval

**Use Case**: Discount approval requiring both Sales VP and Finance approval

```
Step 1: Sales VP & Finance (Unanimous)
- Approvers: Role → Sales VP, Role → Finance VP
- Requires: All approvers must approve
- Rejection: Any rejection = Final Rejection
```

**Configuration**:
```
Step 1: Executive Approval
- Approve/reject based on: Unanimous approval
- Approvers:
  1. Role → Sales VP
  2. Role → Finance VP
- Reject Behavior: Final Rejection
```

### Pattern 4: Conditional Approval Steps

**Use Case**: Opportunity discount approval with tiered thresholds

```
Step 1: Manager Approval (10-20% discount)
- Step Criteria: Discount_Percent__c >= 10 AND Discount_Percent__c < 20
- Approver: Opportunity Owner Manager

Step 2: VP Approval (20-30% discount)
- Step Criteria: Discount_Percent__c >= 20 AND Discount_Percent__c < 30
- Approver: Regional VP

Step 3: Executive Approval (30%+ discount)
- Step Criteria: Discount_Percent__c >= 30
- Approver: CEO
```

## Submission Methods

### 1. Manual Submission (Standard UI)

User clicks "Submit for Approval" button on record detail page.

**Requirements**:
- Button must be on page layout
- User must have edit access to record
- Record must meet entry criteria
- Record must not be currently pending approval

### 2. Apex Submission

```apex
// Submit record for approval programmatically
Approval.ProcessSubmitRequest req = new Approval.ProcessSubmitRequest();
req.setObjectId(recordId);
req.setSubmitterId(UserInfo.getUserId());
req.setProcessDefinitionNameOrId('My_Approval_Process'); // Optional: specific process
req.setComments('Auto-submitted via integration');

Approval.ProcessResult result = Approval.process(req);

if (result.isSuccess()) {
    System.debug('Submitted for approval: ' + result.getInstanceId());
} else {
    System.debug('Submission failed: ' + result.getErrors()[0].getMessage());
}
```

**Common Use Cases**:
- Auto-submit records created via integration
- Submit child records when parent approved
- Batch submission of multiple records

### 3. Process Builder / Flow Submission

**Process Builder**:
- Action: Submit for Approval
- Specify: Object and approval process (optional)

**Flow**:
- Element: Submit for Approval
- Set: Record ID, Submitter ID, Process Name

### 4. Email-to-Case Auto-Submission

Configure approval process with "Submit for approval when created via" → Email.

## Approval Actions

### Field Updates

**Common Patterns**:
```
Initial Submission:
- Status = "Pending Approval"
- Locked__c = TRUE
- Submitted_Date__c = TODAY()

Final Approval:
- Status = "Approved"
- Approved_Date__c = TODAY()
- Approved_By__c = [Last Approver]

Final Rejection:
- Status = "Rejected"
- Locked__c = FALSE
- Rejection_Reason__c = [Rejection Comments]

Recall:
- Status = "Draft"
- Locked__c = FALSE
```

### Email Alerts

Send notifications at each stage:
- Submitter: "Your request has been submitted"
- Approver: "You have a pending approval request"
- Submitter on Approval: "Your request was approved"
- Submitter on Rejection: "Your request was rejected"

**Best Practice**: Use Email Templates with merge fields:
```
Hi {!Opportunity.Owner.FirstName},

Your Opportunity {!Opportunity.Name} requiring {!Opportunity.Discount_Percent__c}%
discount has been submitted for approval.

Amount: {!Opportunity.Amount}
Stage: {!Opportunity.StageName}
```

### Tasks

Create follow-up tasks on approval/rejection:
```
Final Approval Action:
- Create Task
- Assigned To: Opportunity Owner
- Subject: "Process approved contract for {!Opportunity.Name}"
- Due Date: TODAY() + 7
```

### Outbound Messages

Trigger external system integration:
```
Final Approval:
- Send outbound message to ERP system
- Payload: Opportunity data
- Endpoint: https://erp.company.com/api/orders
```

## Approval Assignment

### 1. User Field

Assign to user specified in a field on the record.

```
Approver: User → Direct_Manager__c
```

**Pros**: Flexible, dynamic based on record
**Cons**: Requires maintaining user field, null handling

### 2. Queue

Assign to a queue for any member to approve.

```
Approver: Queue → Discount_Approval_Queue
```

**Pros**: Load balancing, no single point of failure
**Cons**: Less accountability, slower response

### 3. Role

Assign to all users in a role.

```
Approver: Role → Regional_Sales_Manager
```

**Pros**: Automatic as org changes, any can approve
**Cons**: Can be slow if many in role

### 4. Role and Subordinates

Assign to role hierarchy.

```
Approver: Role and Subordinates → Sales_Director
```

**Pros**: Covers entire hierarchy
**Cons**: Very broad access

### 5. Related User

Assign based on related record's user field.

```
Approver: Related User → Account.Owner
```

**Use Case**: Invoice approval by Account Owner

### 6. Apex-Based Dynamic Assignment

```apex
global class CustomApprovalRouter implements Process.Plugin {

    global Process.PluginResult invoke(Process.PluginRequest request) {
        // Get record ID from request
        Id recordId = (Id) request.inputParameters.get('recordId');

        // Query record and determine approver
        Opportunity opp = [SELECT Amount, Territory__c FROM Opportunity WHERE Id = :recordId];

        Id approverId;
        if (opp.Amount > 100000) {
            approverId = [SELECT Id FROM User WHERE Title = 'VP Sales' LIMIT 1].Id;
        } else {
            approverId = [SELECT Id FROM User WHERE Territory__c = :opp.Territory__c
                          AND Profile.Name = 'Sales Manager' LIMIT 1].Id;
        }

        // Return approver
        Map<String, Object> result = new Map<String, Object>();
        result.put('approverId', approverId);
        return new Process.PluginResult(result);
    }

    global Process.PluginDescribeResult describe() {
        Process.PluginDescribeResult result = new Process.PluginDescribeResult();
        result.inputParameters = new List<Process.PluginDescribeResult.InputParameter>{
            new Process.PluginDescribeResult.InputParameter('recordId',
                Process.PluginDescribeResult.ParameterType.ID, true)
        };
        result.outputParameters = new List<Process.PluginDescribeResult.OutputParameter>{
            new Process.PluginDescribeResult.OutputParameter('approverId',
                Process.PluginDescribeResult.ParameterType.ID)
        };
        return result;
    }
}
```

## Common Issues and Solutions

### Issue 1: "No applicable approval process was found"

**Symptoms**: User submits record but gets error message

**Root Causes**:
1. No active approval process for this object
2. Record doesn't meet entry criteria
3. Record already pending approval
4. Multiple processes exist but none match

**Troubleshooting**:
```apex
// Debug script to check approval processes
List<ProcessInstance> instances = [
    SELECT Status, TargetObjectId
    FROM ProcessInstance
    WHERE TargetObjectId = :recordId
];
System.debug('Current approval status: ' + instances);

// Check active processes
List<ProcessDefinition> processes = [
    SELECT Name, TableEnumOrId, State
    FROM ProcessDefinition
    WHERE TableEnumOrId = 'Opportunity'
    AND State = 'Active'
];
System.debug('Active processes: ' + processes.size());
```

**Solutions**:
```
1. Verify active process exists:
   Setup → Approval Processes → [Object] → Check "Active" status

2. Check entry criteria:
   - View process → Entry Criteria
   - Ensure record meets all conditions
   - Test with Debug Logs: Approval Process evaluation

3. Check record lock status:
   Query ProcessInstance for TargetObjectId = recordId
   If exists and Status = 'Pending', record already in approval

4. Simplify entry criteria:
   Temporarily set to "Formula evaluates to true: TRUE"
   to test if criteria issue
```

### Issue 2: Wrong Approver Assigned

**Symptoms**: Approval goes to unexpected user/queue

**Root Causes**:
1. User field is null or inactive user
2. Queue has no members
3. Role hierarchy changed
4. Multiple approval steps triggered

**Solutions**:
```
1. Validate user field:
   - Ensure field populated before submission
   - Check user is active: User.IsActive = true
   - Use validation rule to prevent null:
     ISBLANK(Manager__c)

2. Check queue membership:
   Setup → Queues → [Queue Name] → Queue Members
   Ensure active users in queue

3. Fallback approver:
   In process, specify "If approver not available"
   → Assign to: User → [Fallback User]

4. Debug assignment:
   Query ProcessInstanceWorkitem for approver:

   List<ProcessInstanceWorkitem> items = [
       SELECT ActorId, Actor.Name, ProcessInstance.TargetObjectId
       FROM ProcessInstanceWorkitem
       WHERE ProcessInstance.TargetObjectId = :recordId
   ];
   System.debug('Current approver: ' + items[0].Actor.Name);
```

### Issue 3: Approval Process Not Triggered Automatically

**Symptoms**: Record created but not auto-submitted

**Root Causes**:
1. Filter criteria not met
2. Created via API without triggering logic
3. Approval locked by another process
4. Validation rules preventing submission

**Solutions**:
```
1. Use Apex submission instead of filter criteria:
   trigger OpportunityTrigger on Opportunity (after insert, after update) {
       for (Opportunity opp : Trigger.new) {
           if (opp.Discount_Percent__c > 10 && !opp.IsInApprovalProcess__c) {
               Approval.ProcessSubmitRequest req = new Approval.ProcessSubmitRequest();
               req.setObjectId(opp.Id);
               req.setSubmitterId(opp.OwnerId);

               try {
                   Approval.process(req);
               } catch (Exception e) {
                   System.debug('Approval submission failed: ' + e.getMessage());
               }
           }
       }
   }

2. Check record lock state:
   Approval.LockResult lr = Approval.lock(recordId);
   // If fails, record may be locked by another process

3. Bypass validation on submission:
   DMLOptions dmlOpts = new DMLOptions();
   dmlOpts.EmailHeader.triggerUserEmail = false;
   // Note: Cannot bypass all validations, but can control email
```

### Issue 4: Cannot Edit Record After Rejection

**Symptoms**: Record remains locked after rejection

**Root Cause**: "Unlock record for editing" not configured in Final Rejection Actions

**Solution**:
```
1. Add Post-Rejection Action:
   Setup → Approval Process → Edit → Final Rejection Actions
   → Add: Unlock Record for Editing

2. Or use Field Update:
   Final Rejection Actions → Field Update
   Field: Locked__c
   Value: FALSE

3. Manual unlock via Apex:
   Approval.UnlockResult ulr = Approval.unlock(recordId);
   if (ulr.isSuccess()) {
       System.debug('Record unlocked');
   }
```

### Issue 5: Can Bypass Approval by Direct Edit

**Symptoms**: Users can edit approved records without re-approval

**Root Cause**: No validation rule preventing edits after approval

**Solution**:
```
1. Validation Rule - Prevent edits to approved records:

   Rule Name: Prevent_Edit_After_Approval
   Formula:
   AND(
       ISCHANGED(Discount_Percent__c),
       TEXT(Status__c) = 'Approved',
       $Profile.Name <> 'System Administrator'
   )
   Error Message: Cannot edit approved record. Please submit for re-approval.

2. Or lock record via Process Builder:
   When: Record Updated AND Status = 'Approved'
   Action: Lock Record

3. Trigger-based approach:
   trigger OpportunityTrigger on Opportunity (before update) {
       for (Opportunity opp : Trigger.new) {
           Opportunity oldOpp = Trigger.oldMap.get(opp.Id);

           if (opp.Status__c == 'Approved' &&
               opp.Discount_Percent__c != oldOpp.Discount_Percent__c) {
               opp.addError('Cannot edit approved discount. Submit for re-approval.');
           }
       }
   }
```

## Testing Approval Processes

### Test Class Pattern

```apex
@isTest
public class ApprovalProcessTest {

    @testSetup
    static void setup() {
        // Create test users
        Profile salesProfile = [SELECT Id FROM Profile WHERE Name = 'Sales User' LIMIT 1];

        User salesRep = new User(
            FirstName = 'Test',
            LastName = 'Sales Rep',
            Email = 'testrep@test.com',
            Username = 'testrep@test.com.dev',
            Alias = 'trep',
            ProfileId = salesProfile.Id,
            TimeZoneSidKey = 'America/New_York',
            LocaleSidKey = 'en_US',
            EmailEncodingKey = 'UTF-8',
            LanguageLocaleKey = 'en_US'
        );
        insert salesRep;

        User manager = new User(
            FirstName = 'Test',
            LastName = 'Manager',
            Email = 'testmgr@test.com',
            Username = 'testmgr@test.com.dev',
            Alias = 'tmgr',
            ProfileId = salesProfile.Id,
            TimeZoneSidKey = 'America/New_York',
            LocaleSidKey = 'en_US',
            EmailEncodingKey = 'UTF-8',
            LanguageLocaleKey = 'en_US'
        );
        insert manager;

        // Set manager relationship
        salesRep.ManagerId = manager.Id;
        update salesRep;
    }

    @isTest
    static void testApprovalSubmission() {
        User salesRep = [SELECT Id FROM User WHERE Username = 'testrep@test.com.dev' LIMIT 1];

        // Create opportunity as sales rep
        System.runAs(salesRep) {
            Opportunity opp = new Opportunity(
                Name = 'Test Opp',
                StageName = 'Prospecting',
                CloseDate = Date.today().addDays(30),
                Amount = 100000,
                Discount_Percent__c = 15
            );
            insert opp;

            // Submit for approval
            Test.startTest();
            Approval.ProcessSubmitRequest req = new Approval.ProcessSubmitRequest();
            req.setObjectId(opp.Id);
            req.setSubmitterId(salesRep.Id);

            Approval.ProcessResult result = Approval.process(req);
            Test.stopTest();

            // Verify submission
            System.assert(result.isSuccess(), 'Approval submission should succeed');
            System.assertNotEquals(null, result.getInstanceId(), 'Should have process instance');

            // Verify record locked
            opp = [SELECT Id, IsLocked FROM Opportunity WHERE Id = :opp.Id];
            System.assert(opp.IsLocked, 'Record should be locked during approval');

            // Verify pending work item created
            List<ProcessInstanceWorkitem> workItems = [
                SELECT Id, ActorId
                FROM ProcessInstanceWorkitem
                WHERE ProcessInstance.TargetObjectId = :opp.Id
            ];
            System.assertEquals(1, workItems.size(), 'Should have one pending approval');
        }
    }

    @isTest
    static void testApprovalApprove() {
        User salesRep = [SELECT Id FROM User WHERE Username = 'testrep@test.com.dev' LIMIT 1];
        User manager = [SELECT Id FROM User WHERE Username = 'testmgr@test.com.dev' LIMIT 1];

        Opportunity opp;

        // Create and submit
        System.runAs(salesRep) {
            opp = new Opportunity(
                Name = 'Test Opp',
                StageName = 'Prospecting',
                CloseDate = Date.today().addDays(30),
                Amount = 100000,
                Discount_Percent__c = 15
            );
            insert opp;

            Approval.ProcessSubmitRequest req = new Approval.ProcessSubmitRequest();
            req.setObjectId(opp.Id);
            Approval.process(req);
        }

        // Approve as manager
        System.runAs(manager) {
            // Get work item
            ProcessInstanceWorkitem workItem = [
                SELECT Id, ProcessInstanceId
                FROM ProcessInstanceWorkitem
                WHERE ProcessInstance.TargetObjectId = :opp.Id
                LIMIT 1
            ];

            // Approve
            Test.startTest();
            Approval.ProcessWorkitemRequest req = new Approval.ProcessWorkitemRequest();
            req.setWorkitemId(workItem.Id);
            req.setAction('Approve');
            req.setComments('Approved for testing');

            Approval.ProcessResult result = Approval.process(req);
            Test.stopTest();

            // Verify approval
            System.assert(result.isSuccess(), 'Approval should succeed');

            // Verify status updated (depends on final approval actions)
            opp = [SELECT Id, Status__c FROM Opportunity WHERE Id = :opp.Id];
            System.assertEquals('Approved', opp.Status__c, 'Status should be Approved');
        }
    }

    @isTest
    static void testApprovalReject() {
        User salesRep = [SELECT Id FROM User WHERE Username = 'testrep@test.com.dev' LIMIT 1];
        User manager = [SELECT Id FROM User WHERE Username = 'testmgr@test.com.dev' LIMIT 1];

        Opportunity opp;

        // Create and submit
        System.runAs(salesRep) {
            opp = new Opportunity(
                Name = 'Test Opp',
                StageName = 'Prospecting',
                CloseDate = Date.today().addDays(30),
                Amount = 100000,
                Discount_Percent__c = 15
            );
            insert opp;

            Approval.ProcessSubmitRequest req = new Approval.ProcessSubmitRequest();
            req.setObjectId(opp.Id);
            Approval.process(req);
        }

        // Reject as manager
        System.runAs(manager) {
            ProcessInstanceWorkitem workItem = [
                SELECT Id
                FROM ProcessInstanceWorkitem
                WHERE ProcessInstance.TargetObjectId = :opp.Id
                LIMIT 1
            ];

            Test.startTest();
            Approval.ProcessWorkitemRequest req = new Approval.ProcessWorkitemRequest();
            req.setWorkitemId(workItem.Id);
            req.setAction('Reject');
            req.setComments('Discount too high');

            Approval.ProcessResult result = Approval.process(req);
            Test.stopTest();

            // Verify rejection
            System.assert(result.isSuccess(), 'Rejection should succeed');

            // Verify status and unlock
            opp = [SELECT Id, Status__c, IsLocked FROM Opportunity WHERE Id = :opp.Id];
            System.assertEquals('Rejected', opp.Status__c, 'Status should be Rejected');
            System.assertEquals(false, opp.IsLocked, 'Record should be unlocked after rejection');
        }
    }
}
```

## Best Practices

### 1. Design Principles

- **Single Responsibility**: One approval process per business rule
- **Clear Entry Criteria**: Make it obvious which records enter which process
- **Fail-Safe Defaults**: Always specify fallback approvers
- **Audit Trail**: Use Status fields and History tracking

### 2. Performance Optimization

- **Limit Approval Steps**: Maximum 3-5 steps for performance
- **Use Queues for Load Balancing**: Don't assign to single users for high volume
- **Batch Submissions**: Submit multiple records in single transaction when possible
- **Avoid Recursive Triggers**: Don't trigger approval from approval actions

### 3. User Experience

- **Clear Notifications**: Send email alerts at each stage
- **Status Visibility**: Show approval status on page layouts
- **Mobile Support**: Test approval on Salesforce Mobile App
- **Reassignment**: Allow approval reassignment for OOO scenarios

### 4. Security

- **Least Privilege**: Only grant "Modify All" to admins
- **Lock Records**: Always lock during approval
- **Validation Rules**: Prevent bypassing approval by direct edit
- **Audit**: Enable Setup Audit Trail for process changes

### 5. Documentation

Document for each approval process:
- **Purpose**: Business justification
- **Entry Criteria**: Which records qualify
- **Approvers**: Who approves at each step
- **Actions**: What happens on approval/rejection
- **Testing**: How to test in sandbox

## Monitoring and Maintenance

### Monitoring Queries

```apex
// Pending approvals by approver
SELECT Actor.Name, COUNT(Id) cnt
FROM ProcessInstanceWorkitem
GROUP BY Actor.Name
ORDER BY COUNT(Id) DESC

// Approval process performance
SELECT ProcessDefinition.Name,
       AVG(ElapsedTimeInDays) avgDays,
       COUNT(Id) total
FROM ProcessInstance
WHERE CreatedDate = LAST_N_DAYS:30
GROUP BY ProcessDefinition.Name

// Stuck approvals (>7 days)
SELECT TargetObject.Name,
       ProcessDefinition.Name,
       CreatedDate,
       (SELECT Actor.Name FROM Workitems)
FROM ProcessInstance
WHERE Status = 'Pending'
AND CreatedDate < LAST_N_DAYS:7

// Rejection rate
SELECT ProcessDefinition.Name,
       COUNT(Id) total,
       SUM(CASE WHEN Status = 'Rejected' THEN 1 ELSE 0 END) rejected
FROM ProcessInstance
WHERE CreatedDate = LAST_N_DAYS:90
GROUP BY ProcessDefinition.Name
```

### Maintenance Tasks

**Weekly**:
- Review pending approvals >3 days old
- Check for inactive approvers in processes

**Monthly**:
- Review approval process performance metrics
- Audit rejection reasons and patterns
- Update approver assignments based on org changes

**Quarterly**:
- Review and update entry criteria
- Optimize approval steps
- Train new approvers

## References

- [Salesforce Help: Approval Processes](https://help.salesforce.com/s/articleView?id=sf.approvals_overview.htm)
- [Trailhead: Approval Processes](https://trailhead.salesforce.com/content/learn/modules/business_process_automation)
- [Developer Guide: Apex Approval Processing](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_approvals.htm)
