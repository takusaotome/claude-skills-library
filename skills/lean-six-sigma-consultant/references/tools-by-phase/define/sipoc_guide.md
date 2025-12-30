# SIPOC Diagram Guide

## Overview

SIPOC is a high-level process mapping tool used in the Define phase to understand the major elements of a process before detailed mapping. The acronym represents the five elements of a process from a systems perspective.

## What SIPOC Stands For

| Letter | Element | Description |
|--------|---------|-------------|
| **S** | Suppliers | Who provides inputs to the process |
| **I** | Inputs | What materials, information, or resources enter the process |
| **P** | Process | The high-level steps (5-7 steps) |
| **O** | Outputs | What the process produces |
| **C** | Customers | Who receives the outputs |

## Purpose

- Provide a high-level view of the process
- Establish process boundaries (start and end)
- Identify key stakeholders
- Create common understanding among team
- Prepare for detailed process mapping
- Support scope definition

## When to Use

- At the beginning of a project (Define phase)
- When team members have different understanding of the process
- When establishing project scope
- Before detailed process mapping
- When communicating with stakeholders about the process

## How to Create a SIPOC

### Step 1: Identify the Process
- Give the process a clear name
- Define the process at a high level
- Ensure alignment with project scope

### Step 2: Define the Process Steps (P)
Start with the Process column:
- Use 5-7 high-level steps
- Begin each step with an action verb
- Keep steps at the same level of detail
- Identify clear start and end points

**Example Process Steps**:
1. Receive order
2. Verify inventory
3. Pick items
4. Pack shipment
5. Ship to customer
6. Confirm delivery

### Step 3: Identify the Outputs (O)
- What does the process produce?
- What deliverables go to the customer?
- Include both products and information

**Types of Outputs**:
- Physical products
- Services delivered
- Information/documents
- Decisions made

### Step 4: Identify the Customers (C)
- Who receives each output?
- Include both internal and external customers
- Consider all stakeholders who receive value

**Types of Customers**:
- External customers (paying customers)
- Internal customers (next process)
- Regulatory bodies
- Other stakeholders

### Step 5: Identify the Inputs (I)
- What is needed to execute the process?
- What materials, information, resources are required?
- Include both tangible and intangible inputs

**Types of Inputs**:
- Raw materials
- Information/data
- Documents
- Specifications
- Equipment
- Human resources

### Step 6: Identify the Suppliers (S)
- Who provides each input?
- Include both internal and external suppliers
- Link suppliers to specific inputs

**Types of Suppliers**:
- External vendors
- Internal departments
- Systems/databases
- Previous processes

## SIPOC Format

### Standard Format (Horizontal)

```
┌──────────┬──────────┬──────────────┬──────────┬──────────┐
│ Supplier │  Input   │   Process    │  Output  │ Customer │
├──────────┼──────────┼──────────────┼──────────┼──────────┤
│ [S1]     │ [I1]     │ 1. Step 1    │ [O1]     │ [C1]     │
│ [S2]     │ [I2]     │ 2. Step 2    │ [O2]     │ [C2]     │
│ [S3]     │ [I3]     │ 3. Step 3    │ [O3]     │ [C3]     │
│          │ [I4]     │ 4. Step 4    │          │          │
│          │          │ 5. Step 5    │          │          │
└──────────┴──────────┴──────────────┴──────────┴──────────┘
```

### Alternative Format (Detailed Mapping)

```
Suppliers → Inputs → [Process Box] → Outputs → Customers
                     ↓
              1. Step 1
              2. Step 2
              3. Step 3
              4. Step 4
              5. Step 5
```

## Example: Order Fulfillment SIPOC

### Process: Order Fulfillment

| Suppliers | Inputs | Process | Outputs | Customers |
|-----------|--------|---------|---------|-----------|
| Customers | Customer order | 1. Receive and validate order | Confirmed order | Warehouse |
| ERP System | Product specifications | 2. Check inventory availability | Inventory status | Customer service |
| Warehouse | Inventory | 3. Pick items from warehouse | Picked items | Shipping dept |
| Packaging supplier | Packaging materials | 4. Pack and label shipment | Packed shipment | Carrier |
| Carrier (UPS, FedEx) | Shipping labels | 5. Ship to customer | Shipped order | Customer |
| | Delivery confirmation | 6. Confirm delivery | Delivery confirmation | Customer |
| | | | Invoice | Accounting |

## Example: Loan Application SIPOC

### Process: Loan Application Processing

| Suppliers | Inputs | Process | Outputs | Customers |
|-----------|--------|---------|---------|-----------|
| Applicant | Loan application | 1. Receive application | Application received | Applicant |
| Credit bureau | Credit report | 2. Verify information | Verified data | Underwriting |
| Employer | Employment verification | 3. Assess creditworthiness | Credit assessment | Loan officer |
| IT Systems | Decision rules | 4. Make lending decision | Approval/Denial | Applicant |
| Legal | Loan documents | 5. Prepare documentation | Loan package | Applicant |
| | | 6. Fund loan | Disbursed funds | Applicant, Branch |

## Tips for Effective SIPOCs

### Do's
- Start with the Process column (easier to work from)
- Keep it high-level (5-7 steps maximum)
- Use action verbs for process steps
- Be specific about inputs and outputs
- Include both internal and external customers/suppliers
- Get team consensus on the SIPOC

### Don'ts
- Don't make it too detailed (that comes later)
- Don't include sub-steps
- Don't skip any columns
- Don't assume everyone knows the process
- Don't finalize without stakeholder review

## Connecting SIPOC to Other Tools

### SIPOC → Project Charter
- Outputs become basis for primary metric (Y)
- Customers inform VOC collection
- Process boundaries define project scope

### SIPOC → VOC/CTQ
- Customers identified → Gather their voice
- Outputs → What do customers care about?
- CTQs emerge from customer requirements

### SIPOC → Detailed Process Map
- High-level steps → Expand into detailed map
- Inputs/Outputs → Verify in detailed mapping
- Start/End points established

## SIPOC Validation Checklist

- [ ] Process has clear start and end points
- [ ] 5-7 high-level steps (not too detailed)
- [ ] All inputs have identified suppliers
- [ ] All outputs have identified customers
- [ ] Internal and external customers included
- [ ] Team agrees on the SIPOC
- [ ] Aligns with project scope

## Common Mistakes

1. **Too detailed**: Including 15-20 steps (keep to 5-7)
2. **Missing steps**: Jumping from start to end
3. **Vague inputs/outputs**: "Stuff" instead of specific items
4. **Forgetting internal customers**: Only listing external
5. **Not linking suppliers to inputs**: Generic supplier list
6. **Process scope mismatch**: SIPOC doesn't match charter scope
