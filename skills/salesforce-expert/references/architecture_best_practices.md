# Salesforce Architecture Best Practices

## Overview

This guide covers enterprise Salesforce architecture patterns including data modeling, scalability strategies, integration design, governor limit management, and system design principles.

## Data Modeling

### Object Relationship Patterns

#### Master-Detail vs Lookup

**Master-Detail Relationships**:

Use when:
- Child cannot exist without parent
- Need roll-up summary fields
- Want cascading deletes
- Sharing should inherit from parent

Limitations:
- Cannot reparent records after creation
- Master cannot be in many-to-many relationship
- Impacts governor limits (counted as parent operations)

```
Example: Invoice (Master) → Invoice_Line_Item (Detail)
- Line items cannot exist without invoice
- Invoice total = SUM(line_item.amount)
- Delete invoice → deletes all line items
```

**Lookup Relationships**:

Use when:
- Independent objects
- Optional relationship
- Need to reparent records
- Different sharing rules

```
Example: Opportunity (Lookup) → Account
- Opportunity can exist before Account assigned
- Can change Account on Opportunity
- Independent sharing settings
```

**Decision Matrix**:

| Criteria | Master-Detail | Lookup |
|----------|---------------|--------|
| Child independence | No | Yes |
| Roll-up summaries | Yes | No (use Flow/Apex) |
| Reparenting | No | Yes |
| Sharing inheritance | Yes | No |
| Delete cascade | Yes | No (unless configured) |
| Max per object | 2 master-details | 40 lookups |

### Many-to-Many Relationships (Junction Objects)

**Pattern**: Create junction object with two master-detail relationships

```
Example: Project-Resource Assignment

Project (Master) ←─ Project_Assignment (Junction) ─→ Resource (Master)

Project_Assignment__c:
- Project__c (Master-Detail to Project)
- Resource__c (Master-Detail to Resource)
- Role__c (Picklist: Developer, QA, PM)
- Allocation_Percent__c (Number: 0-100)
- Start_Date__c (Date)
- End_Date__c (Date)
```

**Benefits**:
- Both sides can have roll-up summaries
- Deleting either parent deletes junction record
- Can store additional metadata (role, dates, etc.)

**Considerations**:
- Sharing determined by both parents (most restrictive)
- Cannot have more than 2 master-detail relationships
- Reports can span all three objects

### Denormalization Patterns

#### When to Denormalize

Denormalize (store redundant data) when:
- Read operations significantly outnumber writes
- Cross-object calculations needed frequently
- Reports require fast performance
- Reduce API calls in integrations

**Pattern 1: Copy Parent Field to Child**

```
Problem: Reports on Opportunity need Account data

Solution:
Opportunity:
- Account_Name__c (Text, 255)
- Account_Industry__c (Text, 255)

Trigger: Copy from Account on Opportunity insert/update

Benefits:
- One query instead of join
- Report filters on Opportunity fields
- Faster page loads

Trade-off:
- Data can become stale if Account updates
- Need to maintain sync logic
```

**Pattern 2: Roll-up Summary (Without Master-Detail)**

```
Problem: Account needs SUM of Opportunity Amounts (but using Lookup)

Solution: Use Flow or Apex Trigger

Apex Trigger:
trigger OpportunityTrigger on Opportunity (after insert, after update, after delete) {
    Set<Id> accountIds = new Set<Id>();

    for (Opportunity opp : Trigger.isDelete ? Trigger.old : Trigger.new) {
        if (opp.AccountId != null) {
            accountIds.add(opp.AccountId);
        }
    }

    if (Trigger.isUpdate) {
        for (Opportunity opp : Trigger.old) {
            if (opp.AccountId != null) {
                accountIds.add(opp.AccountId);
            }
        }
    }

    if (!accountIds.isEmpty()) {
        AccountService.updateTotalOpportunityAmount(accountIds);
    }
}

Service:
public class AccountService {
    public static void updateTotalOpportunityAmount(Set<Id> accountIds) {
        Map<Id, Decimal> accountTotals = new Map<Id, Decimal>();

        for (AggregateResult ar : [
            SELECT AccountId, SUM(Amount) total
            FROM Opportunity
            WHERE AccountId IN :accountIds
            AND StageName != 'Closed Lost'
            GROUP BY AccountId
        ]) {
            accountTotals.put((Id)ar.get('AccountId'), (Decimal)ar.get('total'));
        }

        List<Account> accountsToUpdate = new List<Account>();
        for (Id accId : accountIds) {
            accountsToUpdate.add(new Account(
                Id = accId,
                Total_Opportunity_Amount__c = accountTotals.containsKey(accId)
                    ? accountTotals.get(accId)
                    : 0
            ));
        }

        update accountsToUpdate;
    }
}
```

### Large Data Volume (LDV) Design

#### Skinny Tables

Salesforce automatically creates skinny tables for:
- Frequently accessed fields
- Large tables (>1M records)
- Performance-critical queries

**Request from Salesforce Support** with:
- Object name
- Frequently queried fields (max 100)
- Use case and query patterns

**Benefits**:
- Faster queries on indexed fields
- Reduced query time by 50-80%

**Trade-offs**:
- Not real-time (replicated every few hours)
- Limited field selection

#### Data Archiving Strategy

```
Pattern: Archive old records to external system

1. Identify archiving criteria:
   - Closed Opportunities older than 5 years
   - Completed Cases older than 3 years
   - Inactive Accounts with no activity for 7 years

2. Archive process:
   a. Export to external data warehouse
   b. Verify data integrity
   c. Delete from Salesforce
   d. Store deletion log

3. Implementation:

public class DataArchivingBatch implements Database.Batchable<SObject> {

    private String objectName;
    private Date archiveBeforeDate;

    public DataArchivingBatch(String objectName, Date archiveBeforeDate) {
        this.objectName = objectName;
        this.archiveBeforeDate = archiveBeforeDate;
    }

    public Database.QueryLocator start(Database.BatchableContext bc) {
        String query = 'SELECT Id FROM ' + objectName +
                      ' WHERE LastModifiedDate < :archiveBeforeDate';
        return Database.getQueryLocator(query);
    }

    public void execute(Database.BatchableContext bc, List<SObject> scope) {
        // 1. Export to external system
        ArchiveService.exportToWarehouse(scope);

        // 2. Verify successful export
        if (ArchiveService.verifyExport(scope)) {
            // 3. Soft delete (move to recycle bin)
            Database.delete(scope, false);

            // 4. Log archival
            ArchiveService.logArchival(scope);
        }
    }

    public void finish(Database.BatchableContext bc) {
        // Send summary email
    }
}
```

#### Indexing Strategy

**Automatically Indexed Fields**:
- Id
- Name
- OwnerId
- CreatedDate
- SystemModstamp
- RecordType
- Master-Detail fields
- Lookup fields
- External ID fields
- Unique fields

**Custom Indexes** (Request from Support):
- High-volume queries on specific fields
- WHERE clause fields in selective queries

**Selective Queries** (Use indexes effectively):
```apex
// GOOD - Selective (uses index)
[SELECT Id FROM Account WHERE External_ID__c = '12345']

// BAD - Non-selective (table scan)
[SELECT Id FROM Account WHERE Name LIKE '%Test%']

// GOOD - Selective with multiple criteria
[SELECT Id FROM Opportunity
 WHERE CloseDate > :Date.today()
 AND StageName = 'Closed Won'
 AND Amount > 100000]
```

**Selectivity Threshold**: Query is selective if it returns <10% of records

## Scalability Patterns

### Governor Limit Management

#### SOQL Optimization

**Pattern 1: Query Only What You Need**
```apex
// BAD - Queries all fields
List<Opportunity> opps = [SELECT FIELDS(ALL) FROM Opportunity];

// GOOD - Queries specific fields
List<Opportunity> opps = [
    SELECT Id, Name, Amount, StageName
    FROM Opportunity
    WHERE OwnerId = :UserInfo.getUserId()
];
```

**Pattern 2: Aggregate Queries**
```apex
// BAD - Query all records, sum in Apex
List<Opportunity> opps = [SELECT Amount FROM Opportunity];
Decimal total = 0;
for (Opportunity opp : opps) {
    total += opp.Amount;
}

// GOOD - Use aggregate query
AggregateResult result = [
    SELECT SUM(Amount) total
    FROM Opportunity
][0];
Decimal total = (Decimal)result.get('total');
```

**Pattern 3: Query Relationships Efficiently**
```apex
// BAD - Separate queries
List<Account> accounts = [SELECT Id, Name FROM Account];
for (Account acc : accounts) {
    List<Opportunity> opps = [
        SELECT Id, Name
        FROM Opportunity
        WHERE AccountId = :acc.Id
    ];
}

// GOOD - Single query with subquery
List<Account> accounts = [
    SELECT Id, Name,
           (SELECT Id, Name FROM Opportunities)
    FROM Account
];
for (Account acc : accounts) {
    for (Opportunity opp : acc.Opportunities) {
        // Process
    }
}
```

#### DML Optimization

**Pattern: Batch DML Operations**
```apex
// BAD - DML in loop
for (Opportunity opp : Trigger.new) {
    Contact c = new Contact(
        FirstName = 'Auto',
        LastName = opp.Name,
        AccountId = opp.AccountId
    );
    insert c; // Multiple DML statements
}

// GOOD - Collect and batch
List<Contact> contactsToInsert = new List<Contact>();
for (Opportunity opp : Trigger.new) {
    contactsToInsert.add(new Contact(
        FirstName = 'Auto',
        LastName = opp.Name,
        AccountId = opp.AccountId
    ));
}
insert contactsToInsert; // Single DML
```

**Pattern: Database Methods for Partial Success**
```apex
Database.SaveResult[] results = Database.insert(records, false);

for (Integer i = 0; i < results.size(); i++) {
    if (!results[i].isSuccess()) {
        // Log error but continue processing
        System.debug('Failed: ' + records[i] + ' - ' + results[i].getErrors());
    }
}
```

#### Heap Size Management

**Pattern 1: Process Records in Chunks**
```apex
// BAD - Load all records in memory
List<Account> accounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account];

// GOOD - Process in batches
for (List<Account> accountBatch : [SELECT Id, Name FROM Account]) {
    // Process batch
    // Memory released after each iteration
}
```

**Pattern 2: Use Iterable for Large Results**
```apex
public class LargeDataProcessor {

    public void processAll() {
        // QueryLocator handles pagination automatically
        Iterator<Account> it = Database.getQueryLocator([
            SELECT Id, Name FROM Account
        ]).iterator();

        List<Account> batch = new List<Account>();

        while (it.hasNext()) {
            batch.add(it.next());

            if (batch.size() == 200) {
                processBatch(batch);
                batch.clear(); // Free memory
            }
        }

        if (!batch.isEmpty()) {
            processBatch(batch);
        }
    }

    private void processBatch(List<Account> accounts) {
        // Process batch
    }
}
```

#### CPU Time Limits

**Pattern 1: Optimize Loops**
```apex
// BAD - Nested loops O(n²)
for (Opportunity opp : opps) {
    for (Account acc : accounts) {
        if (opp.AccountId == acc.Id) {
            // Process
        }
    }
}

// GOOD - Use Map for O(n) lookup
Map<Id, Account> accountMap = new Map<Id, Account>(accounts);
for (Opportunity opp : opps) {
    Account acc = accountMap.get(opp.AccountId);
    if (acc != null) {
        // Process
    }
}
```

**Pattern 2: Offload Heavy Processing**
```apex
// Move heavy processing to Queueable/Batch
if (!System.isBatch() && !System.isFuture()) {
    System.enqueueJob(new HeavyProcessingQueueable(recordIds));
} else {
    // Already in async context, process directly
    processRecords(recordIds);
}
```

### Asynchronous Processing Strategy

#### Decision Matrix

| Requirement | Use |
|-------------|-----|
| Simple, one-off callout | @future |
| Callout with complex logic | Queueable |
| Process large data sets (>50K) | Batch Apex |
| Scheduled recurring job | Schedulable + Batch |
| Event-driven processing | Platform Events |
| Long-running integration | Continuation/Queueable chain |

#### Chaining Asynchronous Jobs

```apex
public class DataProcessingQueueable implements Queueable {

    private Integer currentBatch;
    private Integer totalBatches;

    public DataProcessingQueueable(Integer currentBatch, Integer totalBatches) {
        this.currentBatch = currentBatch;
        this.totalBatches = totalBatches;
    }

    public void execute(QueueableContext context) {
        // Process current batch
        Integer offset = currentBatch * 200;
        List<Account> accounts = [
            SELECT Id, Name
            FROM Account
            ORDER BY CreatedDate
            LIMIT 200
            OFFSET :offset
        ];

        processAccounts(accounts);

        // Chain next batch
        if (currentBatch < totalBatches - 1 && !Test.isRunningTest()) {
            System.enqueueJob(new DataProcessingQueueable(
                currentBatch + 1,
                totalBatches
            ));
        }
    }

    private void processAccounts(List<Account> accounts) {
        // Processing logic
    }
}

// Kick off chain
Integer totalRecords = [SELECT COUNT() FROM Account];
Integer totalBatches = (totalRecords / 200) + 1;
System.enqueueJob(new DataProcessingQueueable(0, totalBatches));
```

## Integration Patterns

### REST API Design

#### Inbound Integration (Salesforce as Server)

**Pattern: REST Resource with Proper HTTP Methods**

```apex
@RestResource(urlMapping='/api/opportunities/*')
global with sharing class OpportunityAPI {

    @HttpGet
    global static OpportunityResponse getOpportunity() {
        RestRequest req = RestContext.request;
        String opportunityId = req.requestURI.substring(
            req.requestURI.lastIndexOf('/') + 1
        );

        try {
            Opportunity opp = [
                SELECT Id, Name, Amount, StageName, CloseDate
                FROM Opportunity
                WHERE Id = :opportunityId
                LIMIT 1
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

    @HttpPatch
    global static OpportunityResponse updateOpportunity() {
        RestRequest req = RestContext.request;
        String opportunityId = req.requestURI.substring(
            req.requestURI.lastIndexOf('/') + 1
        );

        OpportunityRequest reqBody = (OpportunityRequest)JSON.deserialize(
            req.requestBody.toString(),
            OpportunityRequest.class
        );

        try {
            Opportunity opp = [SELECT Id FROM Opportunity WHERE Id = :opportunityId];

            if (reqBody.name != null) opp.Name = reqBody.name;
            if (reqBody.amount != null) opp.Amount = reqBody.amount;
            if (reqBody.stage != null) opp.StageName = reqBody.stage;

            update opp;

            opp = [SELECT Id, Name, Amount, StageName FROM Opportunity WHERE Id = :opp.Id];
            return new OpportunityResponse(true, 'Updated', opp);

        } catch (Exception e) {
            RestContext.response.statusCode = 400;
            return new OpportunityResponse(false, e.getMessage(), null);
        }
    }

    @HttpDelete
    global static OpportunityResponse deleteOpportunity() {
        RestRequest req = RestContext.request;
        String opportunityId = req.requestURI.substring(
            req.requestURI.lastIndexOf('/') + 1
        );

        try {
            Opportunity opp = [SELECT Id FROM Opportunity WHERE Id = :opportunityId];
            delete opp;

            return new OpportunityResponse(true, 'Deleted', null);

        } catch (Exception e) {
            RestContext.response.statusCode = 400;
            return new OpportunityResponse(false, e.getMessage(), null);
        }
    }

    global class OpportunityRequest {
        public String name;
        public Decimal amount;
        public String stage;
        public Date closeDate;
    }

    global class OpportunityResponse {
        public Boolean success;
        public String message;
        public Opportunity data;

        public OpportunityResponse(Boolean success, String message, Opportunity data) {
            this.success = success;
            this.message = message;
            this.data = data;
        }
    }
}
```

**API Versioning Strategy**:
```apex
@RestResource(urlMapping='/api/v1/opportunities/*')
global class OpportunityAPIv1 { }

@RestResource(urlMapping='/api/v2/opportunities/*')
global class OpportunityAPIv2 { }
```

#### Outbound Integration (Salesforce as Client)

**Pattern: Reusable HTTP Client Service**

```apex
public class HTTPClientService {

    private static final Integer TIMEOUT = 60000;

    public static HTTPResponse get(String endpoint, Map<String, String> headers) {
        return sendRequest('GET', endpoint, null, headers);
    }

    public static HTTPResponse post(String endpoint, String body, Map<String, String> headers) {
        return sendRequest('POST', endpoint, body, headers);
    }

    public static HTTPResponse put(String endpoint, String body, Map<String, String> headers) {
        return sendRequest('PUT', endpoint, body, headers);
    }

    public static HTTPResponse delete(String endpoint, Map<String, String> headers) {
        return sendRequest('DELETE', endpoint, null, headers);
    }

    private static HTTPResponse sendRequest(String method, String endpoint,
                                           String body, Map<String, String> headers) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint(endpoint);
        req.setMethod(method);
        req.setTimeout(TIMEOUT);

        if (headers != null) {
            for (String key : headers.keySet()) {
                req.setHeader(key, headers.get(key));
            }
        }

        if (body != null) {
            req.setBody(body);
        }

        Http http = new Http();

        try {
            HTTPResponse res = http.send(req);

            if (res.getStatusCode() >= 400) {
                throw new CalloutException('HTTP ' + res.getStatusCode() +
                                          ': ' + res.getBody());
            }

            return res;

        } catch (Exception e) {
            Logger.error('Callout failed: ' + endpoint, e);
            throw e;
        }
    }
}

// Usage
public class OpportunityIntegrationService {

    public static void syncToERP(Id opportunityId) {
        Opportunity opp = [
            SELECT Id, Name, Amount, StageName
            FROM Opportunity
            WHERE Id = :opportunityId
        ];

        String endpoint = 'https://erp.company.com/api/opportunities';
        String body = JSON.serialize(opp);

        Map<String, String> headers = new Map<String, String>{
            'Content-Type' => 'application/json',
            'Authorization' => 'Bearer ' + getAuthToken()
        };

        HTTPResponse res = HTTPClientService.post(endpoint, body, headers);

        if (res.getStatusCode() == 200) {
            System.debug('Successfully synced to ERP');
        }
    }

    private static String getAuthToken() {
        // Retrieve from Custom Metadata or Named Credential
        return 'token123';
    }
}
```

### Platform Events Pattern

**Pattern: Decouple Systems with Event-Driven Architecture**

```apex
// Define Platform Event
// Opportunity_Event__e (Platform Event object)
// Fields: Opportunity_Id__c, Action__c, Stage__c

// Publisher
public class OpportunityEventPublisher {

    public static void publishOpportunityChange(Id oppId, String action, String stage) {
        Opportunity_Event__e event = new Opportunity_Event__e(
            Opportunity_Id__c = oppId,
            Action__c = action,
            Stage__c = stage
        );

        Database.SaveResult result = EventBus.publish(event);

        if (!result.isSuccess()) {
            for (Database.Error error : result.getErrors()) {
                System.debug('Error publishing event: ' + error.getMessage());
            }
        }
    }
}

// Subscriber (Trigger)
trigger OpportunityEventTrigger on Opportunity_Event__e (after insert) {

    List<Task> tasksToCreate = new List<Task>();

    for (Opportunity_Event__e event : Trigger.new) {
        if (event.Action__c == 'Closed Won') {
            tasksToCreate.add(new Task(
                Subject = 'Follow up on won opportunity',
                WhatId = event.Opportunity_Id__c,
                Priority = 'High',
                Status = 'Not Started'
            ));
        }
    }

    if (!tasksToCreate.isEmpty()) {
        insert tasksToCreate;
    }
}
```

**Benefits**:
- Loose coupling between publishers and subscribers
- Asynchronous processing
- Scalability - multiple subscribers can listen
- Reliability - events retained for 72 hours

## Security Architecture

### Security Model Layers

1. **Organization Level**: Login IP ranges, session settings
2. **Object Level**: Profiles and Permission Sets
3. **Record Level**: OWD, Sharing Rules, Manual Sharing
4. **Field Level**: Field-Level Security (FLS)

### Principle of Least Privilege

**Pattern: Clone Minimal Profile**

```
Steps:
1. Clone Standard User profile
2. Remove all object permissions
3. Enable only required objects with minimal access
4. Use Permission Sets for additional access

Example:
Profile: Sales User Base
- No object access by default
- Basic login permissions

Permission Set: Opportunity Manager
- Opportunity: Create, Read, Edit, Delete
- Account: Read
- Contact: Read, Edit

Permission Set: Report Viewer
- Custom Report access
- Dashboard access
```

### Field-Level Encryption

**When to Use**:
- PII (Social Security Numbers, Credit Cards)
- Sensitive personal data (Health information)
- Compliance requirements (GDPR, HIPAA)

**Implementation**:
```
Setup → Platform Encryption → Encrypt Fields

Considerations:
- Cannot be used in: Filters, Formula fields, Roll-ups
- Search limitations (exact match only)
- Performance impact on large data volumes
```

## Testing Strategy

### Code Coverage Standards

- **Minimum**: 75% (Salesforce requirement)
- **Recommended**: 85%+
- **Best Practice**: Test business logic, not just coverage

### Test Data Isolation

**@testSetup for Shared Data**:
```apex
@isTest
public class OpportunityServiceTest {

    @testSetup
    static void setup() {
        // Created once, used by all test methods
        Account acc = new Account(Name = 'Test Account');
        insert acc;

        List<Opportunity> opps = new List<Opportunity>();
        for (Integer i = 0; i < 200; i++) {
            opps.add(new Opportunity(
                Name = 'Test Opp ' + i,
                AccountId = acc.Id,
                StageName = 'Prospecting',
                CloseDate = Date.today().addDays(30)
            ));
        }
        insert opps;
    }

    @isTest
    static void testBulkUpdate() {
        List<Opportunity> opps = [SELECT Id FROM Opportunity];
        // Test logic
    }
}
```

### Continuous Integration

**Deployment Pipeline**:
```
1. Developer Sandbox → Local Development
2. Integration Sandbox → Automated Tests + Code Review
3. UAT Sandbox → User Acceptance Testing
4. Production → Deployment via Change Set / SFDX
```

**SFDX CI/CD Pattern**:
```bash
# Authenticate to org
sfdx auth:jwt:grant --clientid $CLIENT_ID --jwtkeyfile $JWT_KEY --username $USERNAME

# Run all tests
sfdx force:apex:test:run --wait 10 --resultformat human --codecoverage

# Deploy to production
sfdx force:source:deploy --sourcepath force-app --targetusername prod --testlevel RunLocalTests --wait 30
```

## References

- [Salesforce Architects Core Resources](https://architect.salesforce.com/learn/learn)
- [Data Architecture and Management Designer Certification](https://trailhead.salesforce.com/credentials/dataarchitect)
- [Integration Architecture Designer Certification](https://trailhead.salesforce.com/credentials/integrationarchitect)
- [Platform Developer II Certification](https://trailhead.salesforce.com/credentials/platformdeveloperii)
