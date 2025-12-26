# Salesforce Custom Development Patterns

## Overview

This guide covers Apex development best practices, common patterns for triggers, controllers, batch jobs, Lightning Web Components (LWC), and testing strategies for enterprise Salesforce applications.

## Apex Trigger Patterns

### Handler Pattern (Best Practice)

Separate business logic from trigger context using a handler class.

**Trigger File** (Minimal logic):
```apex
trigger OpportunityTrigger on Opportunity (before insert, before update,
                                          after insert, after update) {
    OpportunityTriggerHandler.execute();
}
```

**Handler Class** (All business logic):
```apex
public class OpportunityTriggerHandler {

    public static void execute() {
        if (Trigger.isBefore) {
            if (Trigger.isInsert) {
                handleBeforeInsert(Trigger.new);
            } else if (Trigger.isUpdate) {
                handleBeforeUpdate(Trigger.new, Trigger.oldMap);
            }
        } else if (Trigger.isAfter) {
            if (Trigger.isInsert) {
                handleAfterInsert(Trigger.new);
            } else if (Trigger.isUpdate) {
                handleAfterUpdate(Trigger.new, Trigger.oldMap);
            }
        }
    }

    private static void handleBeforeInsert(List<Opportunity> newOpps) {
        // Validation and field updates before insert
        validateDiscounts(newOpps);
        setDefaultValues(newOpps);
    }

    private static void handleBeforeUpdate(List<Opportunity> newOpps,
                                          Map<Id, Opportunity> oldMap) {
        // Validation and field updates before update
        validateStageProgression(newOpps, oldMap);
    }

    private static void handleAfterInsert(List<Opportunity> newOpps) {
        // Create related records, sharing, integrations
        createContactRoles(newOpps);
        shareWithAccountTeam(newOpps);
    }

    private static void handleAfterUpdate(List<Opportunity> newOpps,
                                         Map<Id, Opportunity> oldMap) {
        // React to field changes
        handleOwnerChange(newOpps, oldMap);
    }

    private static void validateDiscounts(List<Opportunity> opps) {
        for (Opportunity opp : opps) {
            if (opp.Discount_Percent__c > 30) {
                opp.addError('Discount cannot exceed 30% without approval');
            }
        }
    }

    private static void handleOwnerChange(List<Opportunity> newOpps,
                                         Map<Id, Opportunity> oldMap) {
        List<Id> changedOwnerOpps = new List<Id>();

        for (Opportunity opp : newOpps) {
            if (opp.OwnerId != oldMap.get(opp.Id).OwnerId) {
                changedOwnerOpps.add(opp.Id);
            }
        }

        if (!changedOwnerOpps.isEmpty()) {
            // Delegate to service class
            OpportunityService.shareRelatedContactsWithNewOwner(changedOwnerOpps);
        }
    }
}
```

**Benefits**:
- Testable: Can test handler logic independently
- Maintainable: Clear separation of concerns
- Reusable: Handler methods can be called from other contexts
- Debuggable: Easier to trace execution flow

### Trigger Framework Pattern

For large orgs with many triggers, use a framework for consistency.

**ITriggerHandler Interface**:
```apex
public interface ITriggerHandler {
    void beforeInsert(List<SObject> newRecords);
    void beforeUpdate(List<SObject> newRecords, Map<Id, SObject> oldRecordsMap);
    void beforeDelete(Map<Id, SObject> oldRecordsMap);
    void afterInsert(List<SObject> newRecords);
    void afterUpdate(List<SObject> newRecords, Map<Id, SObject> oldRecordsMap);
    void afterDelete(Map<Id, SObject> oldRecordsMap);
    void afterUndelete(List<SObject> newRecords);
}
```

**TriggerDispatcher**:
```apex
public class TriggerDispatcher {

    public static void run(ITriggerHandler handler) {
        if (handler == null) return;

        if (Trigger.isBefore) {
            if (Trigger.isInsert) {
                handler.beforeInsert(Trigger.new);
            } else if (Trigger.isUpdate) {
                handler.beforeUpdate(Trigger.new, Trigger.oldMap);
            } else if (Trigger.isDelete) {
                handler.beforeDelete(Trigger.oldMap);
            }
        } else if (Trigger.isAfter) {
            if (Trigger.isInsert) {
                handler.afterInsert(Trigger.new);
            } else if (Trigger.isUpdate) {
                handler.afterUpdate(Trigger.new, Trigger.oldMap);
            } else if (Trigger.isDelete) {
                handler.afterDelete(Trigger.oldMap);
            } else if (Trigger.isUndelete) {
                handler.afterUndelete(Trigger.new);
            }
        }
    }
}
```

**Trigger Implementation**:
```apex
trigger OpportunityTrigger on Opportunity (before insert, before update, before delete,
                                          after insert, after update, after delete, after undelete) {
    TriggerDispatcher.run(new OpportunityTriggerHandler());
}
```

**Handler Implementation**:
```apex
public class OpportunityTriggerHandler implements ITriggerHandler {

    public void beforeInsert(List<SObject> newRecords) {
        List<Opportunity> opps = (List<Opportunity>) newRecords;
        validateDiscounts(opps);
    }

    public void beforeUpdate(List<SObject> newRecords, Map<Id, SObject> oldRecordsMap) {
        // Implementation
    }

    public void beforeDelete(Map<Id, SObject> oldRecordsMap) {
        // Implementation
    }

    public void afterInsert(List<SObject> newRecords) {
        // Implementation
    }

    public void afterUpdate(List<SObject> newRecords, Map<Id, SObject> oldRecordsMap) {
        // Implementation
    }

    public void afterDelete(Map<Id, SObject> oldRecordsMap) {
        // Implementation
    }

    public void afterUndelete(List<SObject> newRecords) {
        // Implementation
    }

    private void validateDiscounts(List<Opportunity> opps) {
        // Business logic
    }
}
```

### Recursion Prevention

Prevent infinite loops when triggers call operations that re-trigger themselves.

**Static Variable Pattern**:
```apex
public class OpportunityTriggerHandler {

    private static Boolean isExecuting = false;

    public static void execute() {
        if (isExecuting) {
            return; // Exit to prevent recursion
        }

        isExecuting = true;

        try {
            // Trigger logic
            if (Trigger.isAfter && Trigger.isUpdate) {
                handleAfterUpdate(Trigger.new, Trigger.oldMap);
            }
        } finally {
            isExecuting = false; // Reset flag
        }
    }
}
```

**Set-Based Recursion Control** (For specific record tracking):
```apex
public class TriggerRecursionControl {

    private static Set<Id> processedOpportunityIds = new Set<Id>();

    public static Boolean isAlreadyProcessed(Id recordId) {
        return processedOpportunityIds.contains(recordId);
    }

    public static void markAsProcessed(Id recordId) {
        processedOpportunityIds.add(recordId);
    }

    public static void reset() {
        processedOpportunityIds.clear();
    }
}

// Usage in handler
public static void handleAfterUpdate(List<Opportunity> newOpps,
                                     Map<Id, Opportunity> oldMap) {
    for (Opportunity opp : newOpps) {
        if (!TriggerRecursionControl.isAlreadyProcessed(opp.Id)) {
            TriggerRecursionControl.markAsProcessed(opp.Id);

            // Perform logic that might cause recursion
            if (opp.OwnerId != oldMap.get(opp.Id).OwnerId) {
                handleOwnerChange(opp);
            }
        }
    }
}
```

## Service Layer Pattern

Separate business logic from trigger/controller code for reusability.

**Service Class**:
```apex
public class OpportunityService {

    /**
     * Share related Contacts with new Opportunity Owner
     * Can be called from Trigger, Controller, or Batch
     */
    public static void shareRelatedContactsWithNewOwner(List<Id> opportunityIds) {
        // Query opportunities with related contacts
        Map<Id, Opportunity> oppMap = new Map<Id, Opportunity>([
            SELECT Id, OwnerId, Customer_Tenant_Name__c
            FROM Opportunity
            WHERE Id IN :opportunityIds
            AND Customer_Tenant_Name__c != null
        ]);

        List<ContactShare> shares = new List<ContactShare>();

        for (Opportunity opp : oppMap.values()) {
            // Check if share already exists
            List<ContactShare> existingShares = [
                SELECT Id
                FROM ContactShare
                WHERE ContactId = :opp.Customer_Tenant_Name__c
                AND UserOrGroupId = :opp.OwnerId
                AND RowCause = :Schema.ContactShare.RowCause.Manual
            ];

            if (existingShares.isEmpty()) {
                shares.add(new ContactShare(
                    ContactId = opp.Customer_Tenant_Name__c,
                    UserOrGroupId = opp.OwnerId,
                    ContactAccessLevel = 'Read',
                    RowCause = Schema.ContactShare.RowCause.Manual
                ));
            }
        }

        if (!shares.isEmpty()) {
            Database.SaveResult[] results = Database.insert(shares, false);

            // Log errors
            for (Database.SaveResult result : results) {
                if (!result.isSuccess()) {
                    System.debug('ContactShare insert failed: ' + result.getErrors());
                }
            }
        }
    }

    /**
     * Calculate Opportunity probability based on Stage
     */
    public static void updateProbability(List<Opportunity> opportunities) {
        Map<String, Decimal> stageProbability = new Map<String, Decimal>{
            'Prospecting' => 10,
            'Qualification' => 25,
            'Needs Analysis' => 40,
            'Proposal' => 60,
            'Negotiation' => 80,
            'Closed Won' => 100,
            'Closed Lost' => 0
        };

        for (Opportunity opp : opportunities) {
            if (stageProbability.containsKey(opp.StageName)) {
                opp.Probability = stageProbability.get(opp.StageName);
            }
        }
    }
}
```

**Usage from Trigger**:
```apex
public class OpportunityTriggerHandler {

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

**Usage from Controller**:
```apex
public class OpportunityController {

    @AuraEnabled
    public static void reassignOpportunity(Id oppId, Id newOwnerId) {
        Opportunity opp = [SELECT Id, OwnerId FROM Opportunity WHERE Id = :oppId];
        opp.OwnerId = newOwnerId;
        update opp;

        // Service method handles sharing
        OpportunityService.shareRelatedContactsWithNewOwner(new List<Id>{oppId});
    }
}
```

## Batch Apex Patterns

### Standard Batch Implementation

```apex
public class OpportunityCleanupBatch implements Database.Batchable<SObject> {

    private Date cutoffDate;

    public OpportunityCleanupBatch(Date cutoffDate) {
        this.cutoffDate = cutoffDate;
    }

    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Name, StageName, CloseDate
            FROM Opportunity
            WHERE CloseDate < :cutoffDate
            AND StageName NOT IN ('Closed Won', 'Closed Lost')
        ]);
    }

    public void execute(Database.BatchableContext bc, List<Opportunity> scope) {
        for (Opportunity opp : scope) {
            opp.StageName = 'Closed Lost';
            opp.Loss_Reason__c = 'Stale - No Activity';
        }

        Database.SaveResult[] results = Database.update(scope, false);

        // Log errors
        for (Integer i = 0; i < results.size(); i++) {
            if (!results[i].isSuccess()) {
                System.debug('Failed to update Opportunity ' + scope[i].Id +
                           ': ' + results[i].getErrors());
            }
        }
    }

    public void finish(Database.BatchableContext bc) {
        // Send completion email
        AsyncApexJob job = [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed
            FROM AsyncApexJob
            WHERE Id = :bc.getJobId()
        ];

        Messaging.SingleEmailMessage email = new Messaging.SingleEmailMessage();
        email.setToAddresses(new String[]{'admin@company.com'});
        email.setSubject('Opportunity Cleanup Batch Completed');
        email.setPlainTextBody('Status: ' + job.Status +
                              '\nRecords Processed: ' + job.JobItemsProcessed +
                              '\nErrors: ' + job.NumberOfErrors);
        Messaging.sendEmail(new Messaging.SingleEmailMessage[]{email});
    }
}

// Execute batch
Database.executeBatch(new OpportunityCleanupBatch(Date.today().addDays(-90)), 200);
```

### Iterable Batch (Custom Iterator)

For complex data sources or external integrations:

```apex
public class ExternalDataBatch implements Database.Batchable<ExternalDataWrapper>,
                                         Database.AllowsCallouts {

    public Iterable<ExternalDataWrapper> start(Database.BatchableContext bc) {
        return new ExternalDataIterator();
    }

    public void execute(Database.BatchableContext bc, List<ExternalDataWrapper> scope) {
        List<Account> accountsToUpsert = new List<Account>();

        for (ExternalDataWrapper data : scope) {
            accountsToUpsert.add(new Account(
                External_Id__c = data.externalId,
                Name = data.name,
                Phone = data.phone
            ));
        }

        Database.upsert(accountsToUpsert, Account.External_Id__c, false);
    }

    public void finish(Database.BatchableContext bc) {
        // Completion logic
    }
}

public class ExternalDataIterator implements Iterator<ExternalDataWrapper>,
                                             Iterable<ExternalDataWrapper> {

    private List<ExternalDataWrapper> dataList;
    private Integer index = 0;

    public ExternalDataIterator() {
        // Fetch data from external source
        this.dataList = fetchExternalData();
    }

    public Boolean hasNext() {
        return index < dataList.size();
    }

    public ExternalDataWrapper next() {
        return dataList[index++];
    }

    public Iterator<ExternalDataWrapper> iterator() {
        return this;
    }

    private List<ExternalDataWrapper> fetchExternalData() {
        // Make HTTP callout to external API
        HttpRequest req = new HttpRequest();
        req.setEndpoint('https://api.external.com/data');
        req.setMethod('GET');

        Http http = new Http();
        HttpResponse res = http.send(req);

        // Parse response and return wrapper objects
        return (List<ExternalDataWrapper>) JSON.deserialize(
            res.getBody(),
            List<ExternalDataWrapper>.class
        );
    }
}

public class ExternalDataWrapper {
    public String externalId;
    public String name;
    public String phone;
}
```

### Stateful Batch (Maintain State Across Batches)

```apex
public class OpportunitySummaryBatch implements Database.Batchable<SObject>,
                                               Database.Stateful {

    private Decimal totalAmount = 0;
    private Integer recordCount = 0;

    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Amount
            FROM Opportunity
            WHERE StageName = 'Closed Won'
            AND CloseDate = THIS_YEAR
        ]);
    }

    public void execute(Database.BatchableContext bc, List<Opportunity> scope) {
        for (Opportunity opp : scope) {
            totalAmount += opp.Amount != null ? opp.Amount : 0;
            recordCount++;
        }
    }

    public void finish(Database.BatchableContext bc) {
        System.debug('Total Won Amount: ' + totalAmount);
        System.debug('Total Won Deals: ' + recordCount);
        System.debug('Average Deal Size: ' + (totalAmount / recordCount));

        // Store summary in custom object
        Annual_Summary__c summary = new Annual_Summary__c(
            Year__c = String.valueOf(Date.today().year()),
            Total_Amount__c = totalAmount,
            Record_Count__c = recordCount,
            Average_Deal_Size__c = totalAmount / recordCount
        );
        insert summary;
    }
}
```

## Queueable Apex Pattern

For asynchronous processing with chaining capability:

```apex
public class OpportunityIntegrationQueueable implements Queueable, Database.AllowsCallouts {

    private List<Id> opportunityIds;

    public OpportunityIntegrationQueueable(List<Id> opportunityIds) {
        this.opportunityIds = opportunityIds;
    }

    public void execute(QueueableContext context) {
        List<Opportunity> opps = [
            SELECT Id, Name, Amount, StageName
            FROM Opportunity
            WHERE Id IN :opportunityIds
        ];

        for (Opportunity opp : opps) {
            // Make callout to external system
            HttpRequest req = new HttpRequest();
            req.setEndpoint('https://api.external.com/opportunities');
            req.setMethod('POST');
            req.setHeader('Content-Type', 'application/json');
            req.setBody(JSON.serialize(opp));

            Http http = new Http();
            HttpResponse res = http.send(req);

            if (res.getStatusCode() == 200) {
                System.debug('Successfully synced: ' + opp.Name);
            } else {
                System.debug('Sync failed: ' + res.getBody());
            }
        }

        // Chain another job if needed
        List<Id> remainingOpps = getNextBatch();
        if (!remainingOpps.isEmpty() && !Test.isRunningTest()) {
            System.enqueueJob(new OpportunityIntegrationQueueable(remainingOpps));
        }
    }

    private List<Id> getNextBatch() {
        // Logic to get next batch of opportunities
        return new List<Id>();
    }
}

// Enqueue from trigger
if (!oppIds.isEmpty()) {
    System.enqueueJob(new OpportunityIntegrationQueueable(oppIds));
}
```

## Lightning Web Components (LWC)

### Wire Service Pattern

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

```html
<!-- opportunityList.html -->
<template>
    <lightning-card title="Opportunities">
        <template if:true={opportunities}>
            <template for:each={opportunities} for:item="opp">
                <div key={opp.Id}>
                    <p>{opp.Name} - {opp.Amount}</p>
                </div>
            </template>
        </template>
        <template if:true={error}>
            <p>Error: {error.body.message}</p>
        </template>
    </lightning-card>
</template>
```

```apex
// OpportunityController.cls
public with sharing class OpportunityController {

    @AuraEnabled(cacheable=true)
    public static List<Opportunity> getOpportunities() {
        return [
            SELECT Id, Name, Amount, StageName, CloseDate
            FROM Opportunity
            WHERE OwnerId = :UserInfo.getUserId()
            ORDER BY CloseDate DESC
            LIMIT 10
        ];
    }
}
```

### Imperative Apex Call Pattern

```javascript
// opportunityCreator.js
import { LightningElement } from 'lwc';
import createOpportunity from '@salesforce/apex/OpportunityController.createOpportunity';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class OpportunityCreator extends LightningElement {
    name = '';
    amount = 0;
    stage = 'Prospecting';

    handleNameChange(event) {
        this.name = event.target.value;
    }

    handleAmountChange(event) {
        this.amount = event.target.value;
    }

    handleStageChange(event) {
        this.stage = event.target.value;
    }

    async handleCreate() {
        try {
            const result = await createOpportunity({
                name: this.name,
                amount: this.amount,
                stage: this.stage
            });

            this.dispatchEvent(
                new ShowToastEvent({
                    title: 'Success',
                    message: 'Opportunity created: ' + result.Id,
                    variant: 'success'
                })
            );

            // Reset form
            this.name = '';
            this.amount = 0;
            this.stage = 'Prospecting';

        } catch (error) {
            this.dispatchEvent(
                new ShowToastEvent({
                    title: 'Error creating opportunity',
                    message: error.body.message,
                    variant: 'error'
                })
            );
        }
    }
}
```

```apex
public with sharing class OpportunityController {

    @AuraEnabled
    public static Opportunity createOpportunity(String name, Decimal amount, String stage) {
        try {
            Opportunity opp = new Opportunity(
                Name = name,
                Amount = amount,
                StageName = stage,
                CloseDate = Date.today().addDays(30)
            );
            insert opp;
            return opp;

        } catch (Exception e) {
            throw new AuraHandledException('Error creating opportunity: ' + e.getMessage());
        }
    }
}
```

### Pub/Sub Pattern (Component Communication)

```javascript
// pubsub.js (Utility Module)
const events = {};

const subscribe = (eventName, callback) => {
    if (!events[eventName]) {
        events[eventName] = [];
    }
    events[eventName].push(callback);
};

const unsubscribe = (eventName, callback) => {
    if (events[eventName]) {
        events[eventName] = events[eventName].filter(fn => fn !== callback);
    }
};

const publish = (eventName, payload) => {
    if (events[eventName]) {
        events[eventName].forEach(callback => {
            callback(payload);
        });
    }
};

export { subscribe, unsubscribe, publish };
```

**Publisher Component**:
```javascript
import { LightningElement } from 'lwc';
import { publish } from 'c/pubsub';

export default class OpportunitySelector extends LightningElement {
    handleOpportunitySelect(event) {
        const opportunityId = event.target.dataset.id;

        publish('opportunitySelected', {
            opportunityId: opportunityId
        });
    }
}
```

**Subscriber Component**:
```javascript
import { LightningElement } from 'lwc';
import { subscribe, unsubscribe } from 'c/pubsub';

export default class OpportunityDetail extends LightningElement {
    opportunityId;

    connectedCallback() {
        this.handleOpportunitySelect = this.handleOpportunitySelect.bind(this);
        subscribe('opportunitySelected', this.handleOpportunitySelect);
    }

    disconnectedCallback() {
        unsubscribe('opportunitySelected', this.handleOpportunitySelect);
    }

    handleOpportunitySelect(event) {
        this.opportunityId = event.opportunityId;
        // Load opportunity details
    }
}
```

## Testing Patterns

### Test Data Factory

```apex
@isTest
public class TestDataFactory {

    public static User createUser(String profileName, String alias) {
        Profile prof = [SELECT Id FROM Profile WHERE Name = :profileName LIMIT 1];

        User u = new User(
            FirstName = 'Test',
            LastName = alias,
            Email = alias + '@test.com',
            Username = alias + '@test.com.dev' + System.currentTimeMillis(),
            Alias = alias,
            ProfileId = prof.Id,
            TimeZoneSidKey = 'America/New_York',
            LocaleSidKey = 'en_US',
            EmailEncodingKey = 'UTF-8',
            LanguageLocaleKey = 'en_US'
        );
        insert u;
        return u;
    }

    public static Account createAccount(String name, Boolean doInsert) {
        Account acc = new Account(
            Name = name,
            Industry = 'Technology',
            AnnualRevenue = 1000000
        );

        if (doInsert) {
            insert acc;
        }
        return acc;
    }

    public static List<Opportunity> createOpportunities(Integer count,
                                                       Account acc,
                                                       Boolean doInsert) {
        List<Opportunity> opps = new List<Opportunity>();

        for (Integer i = 0; i < count; i++) {
            opps.add(new Opportunity(
                Name = 'Test Opp ' + i,
                AccountId = acc.Id,
                StageName = 'Prospecting',
                CloseDate = Date.today().addDays(30),
                Amount = 10000 * (i + 1)
            ));
        }

        if (doInsert) {
            insert opps;
        }
        return opps;
    }
}
```

### Bulk Testing Pattern

```apex
@isTest
public class OpportunityTriggerTest {

    @testSetup
    static void setup() {
        Account acc = TestDataFactory.createAccount('Test Account', true);
        TestDataFactory.createOpportunities(200, acc, true);
    }

    @isTest
    static void testBulkUpdate() {
        List<Opportunity> opps = [SELECT Id, StageName FROM Opportunity];

        Test.startTest();
        for (Opportunity opp : opps) {
            opp.StageName = 'Closed Won';
        }
        update opps;
        Test.stopTest();

        // Verify trigger logic executed for all records
        opps = [SELECT Id, Probability FROM Opportunity];
        for (Opportunity opp : opps) {
            System.assertEquals(100, opp.Probability, 'Probability should be 100 for Closed Won');
        }
    }
}
```

### Mock Callout Pattern

```apex
@isTest
global class OpportunityIntegrationMock implements HttpCalloutMock {

    global HTTPResponse respond(HTTPRequest req) {
        HttpResponse res = new HttpResponse();
        res.setHeader('Content-Type', 'application/json');

        if (req.getEndpoint().contains('/opportunities')) {
            res.setStatusCode(200);
            res.setBody('{"status":"success","id":"EXT-12345"}');
        } else {
            res.setStatusCode(404);
            res.setBody('{"status":"error","message":"Not found"}');
        }

        return res;
    }
}

@isTest
public class OpportunityIntegrationTest {

    @isTest
    static void testSuccessfulCallout() {
        Test.setMock(HttpCalloutMock.class, new OpportunityIntegrationMock());

        Account acc = TestDataFactory.createAccount('Test', true);
        Opportunity opp = new Opportunity(
            Name = 'Test Opp',
            AccountId = acc.Id,
            StageName = 'Closed Won',
            CloseDate = Date.today()
        );

        Test.startTest();
        insert opp;
        System.enqueueJob(new OpportunityIntegrationQueueable(new List<Id>{opp.Id}));
        Test.stopTest();

        // Verify integration marked as successful
        opp = [SELECT Id, Integration_Status__c FROM Opportunity WHERE Id = :opp.Id];
        System.assertEquals('Success', opp.Integration_Status__c);
    }
}
```

## Best Practices

### 1. Bulkification

Always write bulkified code to handle 200 records:

```apex
// BAD - SOQL in loop
for (Opportunity opp : Trigger.new) {
    Account acc = [SELECT Id, Name FROM Account WHERE Id = :opp.AccountId];
    opp.Account_Name__c = acc.Name;
}

// GOOD - Bulkified
Set<Id> accountIds = new Set<Id>();
for (Opportunity opp : Trigger.new) {
    accountIds.add(opp.AccountId);
}

Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name
    FROM Account
    WHERE Id IN :accountIds
]);

for (Opportunity opp : Trigger.new) {
    if (accountMap.containsKey(opp.AccountId)) {
        opp.Account_Name__c = accountMap.get(opp.AccountId).Name;
    }
}
```

### 2. Governor Limits

- **SOQL Queries**: Max 100 per transaction
- **DML Statements**: Max 150 per transaction
- **Heap Size**: 6 MB synchronous, 12 MB asynchronous
- **CPU Time**: 10 seconds synchronous, 60 seconds asynchronous

**Use Collections Efficiently**:
```apex
// Create maps for fast lookup
Map<Id, Account> accountMap = new Map<Id, Account>(accounts);

// Use Sets for uniqueness
Set<Id> oppIds = new Set<Id>();
for (Opportunity opp : Trigger.new) {
    oppIds.add(opp.Id);
}

// Batch DML operations
List<Contact> contactsToUpdate = new List<Contact>();
// ... populate list
update contactsToUpdate; // Single DML for all
```

### 3. Security

**Always use `with sharing`** unless specific reason:
```apex
public with sharing class OpportunityController {
    // Respects user's sharing rules and permissions
}
```

**Check CRUD and FLS**:
```apex
if (!Schema.sObjectType.Opportunity.isCreateable()) {
    throw new SecurityException('No create access');
}

if (!Schema.sObjectType.Opportunity.fields.Amount.isAccessible()) {
    throw new SecurityException('No read access to Amount field');
}
```

**Use `Security.stripInaccessible()`**:
```apex
List<Opportunity> opps = [SELECT Id, Name, Amount FROM Opportunity];

SObjectAccessDecision decision = Security.stripInaccessible(
    AccessType.READABLE,
    opps
);

return decision.getRecords();
```

### 4. Error Handling

```apex
try {
    insert opportunities;
} catch (DmlException e) {
    for (Integer i = 0; i < e.getNumDml(); i++) {
        System.debug('Error on record ' + i + ': ' + e.getDmlMessage(i));
    }
    throw e;
} catch (Exception e) {
    System.debug('Unexpected error: ' + e.getMessage());
    throw new AuraHandledException('Failed to create opportunities');
}
```

### 5. Logging and Debugging

```apex
public class Logger {

    public static void log(String level, String message, Exception e) {
        Log__c log = new Log__c(
            Level__c = level,
            Message__c = message,
            Exception_Type__c = e != null ? e.getTypeName() : null,
            Stack_Trace__c = e != null ? e.getStackTraceString() : null,
            Timestamp__c = System.now()
        );

        Database.insert(log, false); // Don't fail if logging fails
    }

    public static void error(String message, Exception e) {
        log('ERROR', message, e);
    }

    public static void info(String message) {
        log('INFO', message, null);
    }
}

// Usage
try {
    // Business logic
} catch (Exception e) {
    Logger.error('Failed to process opportunity', e);
    throw e;
}
```

## References

- [Apex Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/)
- [Lightning Web Components Developer Guide](https://developer.salesforce.com/docs/component-library/documentation/en/lwc)
- [Apex Design Patterns](https://developer.salesforce.com/wiki/apex_design_patterns)
- [Trigger and Bulk Request Best Practices](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_triggers_bestpract.htm)
