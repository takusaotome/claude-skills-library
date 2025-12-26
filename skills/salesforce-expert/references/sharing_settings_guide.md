# Salesforce Sharing Settings and Access Control Guide

## Overview

This guide covers Salesforce's sharing model, common access control issues, and troubleshooting strategies based on real-world implementation patterns.

## Organization-Wide Defaults (OWD)

### Common OWD Settings

**Private**
- Most restrictive
- Only record owner and users above in role hierarchy can access
- Common for: Account, Contact, Opportunity, Custom Objects with sensitive data

**Public Read Only**
- All users can view but not edit
- Common for: Products, Price Books, reference data

**Public Read/Write**
- All users can view and edit
- Common for: Shared resources, collaborative data

**Controlled by Parent**
- Contact/Case access controlled by related Account
- Common for: Contact (controlled by Account)

### Recommendation by Object Type

| Object | Recommended OWD | Rationale |
|--------|----------------|-----------|
| Account | Private | Business critical, customer data |
| Contact | Controlled by Parent | Inherits Account access |
| Opportunity | Private | Deal sensitivity |
| Lead | Private or Public Read/Write | Depends on sales process |
| Custom Objects (Financial) | Private | Sensitive data |

## Common Access Issues and Solutions

### Issue 1: User Cannot Access Related Records

**Scenario**: Opportunity Owner changed, but new owner cannot see related Contacts

**Root Causes**:
1. Contact OWD is Private
2. Contact owned by different user
3. No sharing rule for Contact access

**Solutions**:
```
Option 1: Change Contact OWD to "Controlled by Parent"
- Setup → Sharing Settings → Contact
- Default Access: Controlled by Parent Account
- Recalculate Sharing

Option 2: Create Sharing Rule
- Based on: Opportunity Owner
- Share: Related Account's Contacts
- Access Level: Read or Read/Write

Option 3: Manual Sharing via Apex
trigger OpportunityTrigger on Opportunity (after update) {
    // Share related Contacts when Opportunity Owner changes
}
```

### Issue 2: Lead Conversion Sharing

**Scenario**: After Lead conversion, the converter loses access to created Contact/Account

**Root Cause**:
- New Account/Contact owned by Lead Owner (not converter)
- Converter is not in role hierarchy above owner

**Solutions**:
```
Option 1: Implicit Sharing Configuration
- Setup → Sharing Settings
- Enable "Grant Access Using Hierarchies" for Contact/Account

Option 2: Sharing Rules
- Share Account/Contact with Lead Converter's role/group

Option 3: Team-Based Sharing
- Add Lead Converter to Account Team or Opportunity Team
```

### Issue 3: Cross-Object Access (Junction Objects)

**Scenario**: User can access Invoice but not related Opportunity

**Root Cause**:
- Invoice OWD allows access
- Opportunity OWD is Private and user is not owner

**Solutions**:
```
Option 1: Apex Sharing on Invoice Creation
trigger InvoiceTrigger on Invoice__c (after insert, after update) {
    // Share related Opportunity with Invoice Owner
    List<OpportunityShare> shares = new List<OpportunityShare>();
    for (Invoice__c inv : Trigger.new) {
        shares.add(new OpportunityShare(
            OpportunityId = inv.Opportunity__c,
            UserOrGroupId = inv.OwnerId,
            OpportunityAccessLevel = 'Read',
            RowCause = Schema.OpportunityShare.RowCause.Manual
        ));
    }
    insert shares;
}

Option 2: Sharing Rules
- Based on: Invoice Owner
- Share: Related Opportunity
- Access Level: Read Only

Option 3: Change Opportunity OWD
- Less recommended due to security implications
```

## Role Hierarchy

### Best Practices

1. **Mirror organizational structure**
   - Manager → Team Lead → Sales Rep
   - Regional Manager → Area Manager → Store Manager

2. **Grant Access Using Hierarchies**
   - Enabled by default for most objects
   - Managers can see subordinates' records
   - Cannot see peers' or superiors' records

3. **Avoid overly complex hierarchies**
   - Max 500 roles recommended
   - Deep hierarchies (>10 levels) impact performance

### Common Patterns

```
Example Hierarchy:
CEO
├─ Sales VP
│   ├─ West Sales Manager
│   │   ├─ West Sales Rep 1
│   │   └─ West Sales Rep 2
│   └─ East Sales Manager
│       ├─ East Sales Rep 1
│       └─ East Sales Rep 2
└─ Service VP
    ├─ Service Manager
    │   ├─ Service Rep 1
    │   └─ Service Rep 2
    └─ ...
```

## Sharing Rules

### Types of Sharing Rules

1. **Owner-Based Sharing Rules**
   - Share records owned by specific users/roles
   - Example: "Share Accounts owned by Sales Reps with Service Team"

2. **Criteria-Based Sharing Rules**
   - Share records matching criteria
   - Example: "Share Accounts with Annual Revenue > $1M with Executive Team"

### Best Practices

1. **Use Public Groups**
   - Create reusable groups instead of individual users
   - Easier to maintain

2. **Performance Consideration**
   - Limit number of sharing rules (<50 per object recommended)
   - Criteria-based rules require recalculation on field changes

3. **Recalculate After Changes**
   - Setup → Sharing Settings → Recalculate
   - Necessary after OWD changes or rule modifications

### Example Sharing Rules

```
Rule Name: Share_High_Value_Accounts
Type: Criteria-Based
Object: Account
Criteria: Annual Revenue >= 1000000
Share With: Executive Team (Public Group)
Access Level: Read Only
```

## Manual Sharing

### When to Use

- Ad-hoc access needs
- Temporary access
- User-initiated sharing (Share button)

### Apex Implementation

```apex
// Share Account with specific user
AccountShare share = new AccountShare();
share.AccountId = accountId;
share.UserOrGroupId = userId;
share.AccountAccessLevel = 'Read'; // Read, Edit
share.OpportunityAccessLevel = 'Read'; // For related Opportunities
share.CaseAccessLevel = 'Read'; // For related Cases
share.RowCause = Schema.AccountShare.RowCause.Manual;

insert share;
```

### Querying Sharing

```apex
// Find who has access to an Account
List<AccountShare> shares = [
    SELECT UserOrGroupId, AccountAccessLevel, RowCause
    FROM AccountShare
    WHERE AccountId = :accountId
];

// RowCause indicates how access was granted:
// - Owner: Record owner
// - Manual: Manual sharing
// - Rule: Sharing rule
// - Team: Account team
// - Territory: Territory-based sharing
```

## Teams (Account Team, Opportunity Team)

### Benefits

- Flexible access without complex sharing rules
- Team members can be added/removed easily
- Supports different roles and access levels

### Implementation

```apex
// Add user to Opportunity Team
OpportunityTeamMember member = new OpportunityTeamMember();
member.OpportunityId = oppId;
member.UserId = userId;
member.TeamMemberRole = 'Sales Engineer';
member.OpportunityAccessLevel = 'Edit';

insert member;
```

### Team Roles

Define team roles with specific access levels:
- Setup → Opportunity Settings → Opportunity Team Roles
- Assign: Read, Edit, or Private access

## Troubleshooting Checklist

When user cannot access a record:

- [ ] **Check OWD**: Setup → Sharing Settings → Object Default Access
- [ ] **Check Record Ownership**: Who owns the record?
- [ ] **Check Role Hierarchy**: Is user above owner in hierarchy?
- [ ] **Check Sharing Rules**: Setup → Sharing Settings → Object Sharing Rules
- [ ] **Check Manual Shares**: Query [Object]Share records
- [ ] **Check Team Membership**: Account Team, Opportunity Team, etc.
- [ ] **Check Profile/Permission Set**: Does user have object-level permissions?
- [ ] **Check Field-Level Security**: Can user see the fields?
- [ ] **Check Page Layout**: Is record type assigned to user's profile?

### Debug Commands

```apex
// Check effective sharing for a record
System.debug([SELECT Id, UserOrGroupId, AccountAccessLevel, RowCause
              FROM AccountShare WHERE AccountId = :accountId]);

// Check user's profile and permission sets
System.debug([SELECT Id, ProfileId, Profile.Name
              FROM User WHERE Id = :userId]);

// Check role hierarchy
System.debug([SELECT Id, Name, ParentRoleId
              FROM UserRole WHERE Id = :user.UserRoleId]);
```

## Performance Considerations

### Sharing Recalculation

- Triggered by: OWD changes, Role hierarchy changes, Sharing rule changes
- Can take hours for large orgs
- Monitor: Setup → System Overview → Sharing Calc Status

### Best Practices for Scale

1. **Minimize Sharing Rules**: <50 per object
2. **Use Groups Over Individual Users**: Reduces sharing rows
3. **Avoid Criteria-Based Rules on High-Volume Fields**: Triggers recalculation
4. **Defer Sharing for Batch Operations**: Use `Database.DMLOptions.allowFieldTruncation`
5. **Monitor Sharing Table Size**: Query [Object]Share record counts

## Security Best Practices

1. **Principle of Least Privilege**
   - Start with Private OWD
   - Grant access through sharing rules as needed

2. **Regular Access Audits**
   - Review who has access to sensitive records
   - Remove unnecessary manual shares

3. **Document Sharing Strategy**
   - Why each OWD setting was chosen
   - Purpose of each sharing rule

4. **Test with Different User Profiles**
   - Use "Login As" to verify access
   - Test edge cases (role changes, ownership transfers)

5. **Monitor Sharing Changes**
   - Setup Audit Trail tracks OWD/Sharing Rule changes
   - Alert on unexpected modifications

## References

- [Salesforce Help: Sharing Architecture](https://help.salesforce.com/s/articleView?id=sf.security_data_access.htm)
- [Trailhead: Data Security](https://trailhead.salesforce.com/content/learn/modules/data_security)
- [Developer Guide: Apex Sharing](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_bulk_sharing.htm)
