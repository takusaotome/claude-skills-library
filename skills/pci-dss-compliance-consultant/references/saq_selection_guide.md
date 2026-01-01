# SAQ Selection Guide

Guide for selecting the appropriate PCI DSS Self-Assessment Questionnaire (SAQ) type.

## Overview

Self-Assessment Questionnaires (SAQs) are validation tools for merchants and service providers who are not required to undergo a full on-site assessment. The correct SAQ depends on how you accept payment cards and your payment processing methods.

## SAQ Decision Tree

```
START
│
├─ Do you store, process, or transmit cardholder data?
│  │
│  ├─ NO → You may not need PCI DSS compliance
│  │       (Confirm with acquirer)
│  │
│  └─ YES ↓
│
├─ Are you a SERVICE PROVIDER?
│  │
│  ├─ YES → SAQ D for Service Providers
│  │
│  └─ NO (Merchant) ↓
│
├─ How do you accept payments?
│  │
│  ├─ Card-Not-Present (E-commerce/MOTO) only
│  │  │
│  │  ├─ Fully outsourced to PCI DSS compliant third party?
│  │  │  │
│  │  │  ├─ YES - Payment page hosted entirely by third party
│  │  │  │  │
│  │  │  │  └─ Does your website impact security of payment?
│  │  │  │     │
│  │  │  │     ├─ NO (redirect/iframe) → SAQ A
│  │  │  │     │
│  │  │  │     └─ YES (elements on your page) → SAQ A-EP
│  │  │  │
│  │  │  └─ NO → SAQ C-VT or SAQ D
│  │  │
│  │  └─ Virtual Terminal Only?
│  │     │
│  │     ├─ YES - Web-based virtual terminal from third party
│  │     │       No electronic CHD storage → SAQ C-VT
│  │     │
│  │     └─ NO → SAQ D
│  │
│  ├─ Card-Present (Face-to-Face) only
│  │  │
│  │  ├─ Using P2PE validated solution?
│  │  │  │
│  │  │  └─ YES → SAQ P2PE
│  │  │
│  │  ├─ Standalone dial-out terminals only?
│  │  │  │
│  │  │  └─ YES (no IP connection) → SAQ B
│  │  │
│  │  ├─ IP-connected standalone terminals?
│  │  │  │
│  │  │  └─ YES (no e-commerce) → SAQ B-IP
│  │  │
│  │  └─ Payment application systems?
│  │     │
│  │     └─ YES (connected to internet, no CHD storage) → SAQ C
│  │
│  └─ Both Card-Present and Card-Not-Present
│     │
│     └─ → SAQ D (most likely)
│
└─ None of the above clearly apply → SAQ D
```

---

## SAQ Types Detailed

### SAQ A - Card-Not-Present, Fully Outsourced

**Eligibility Criteria**:
- E-commerce or mail/telephone-order merchants only
- All payment processing entirely outsourced to PCI DSS validated third parties
- Merchant website does not receive cardholder data
- All payment page elements are from the compliant third party
- No electronic storage of cardholder data

**Typical Scenarios**:
- Website redirects customer to payment provider's hosted page
- Website uses iframe that loads entirely from payment provider
- Mail order/telephone order with calls transferred to payment provider

**Question Count**: ~22 questions

**Key Requirements Covered**:
- 2: Secure configurations for systems
- 9: Physical security (if applicable)
- 12: Policies and incident response

---

### SAQ A-EP - E-commerce with Partial Outsourcing

**Eligibility Criteria**:
- E-commerce merchants only
- Payment processing outsourced to PCI DSS validated third party
- BUT: Merchant website has elements that could impact payment security
- Merchant website does not receive cardholder data directly
- No electronic storage of cardholder data

**Typical Scenarios**:
- Website with JavaScript that interacts with payment form
- Website with embedded payment form (not pure redirect/iframe)
- Website using payment APIs with client-side integration

**Question Count**: ~191 questions

**Key Requirements Covered**:
- 1: Network security controls
- 2: Secure configurations
- 6: Secure systems and software
- 11: Security testing (vulnerability scanning)
- 12: Policies and procedures

---

### SAQ B - Imprint or Standalone Dial-Out Terminals

**Eligibility Criteria**:
- Standalone dial-out terminals only (not IP-connected)
- OR manual imprint machines only
- No electronic cardholder data storage
- No e-commerce

**Typical Scenarios**:
- Small retail with traditional dial-up credit card terminal
- Merchants using manual card imprint machines (knuckle busters)

**Question Count**: ~41 questions

**Key Requirements Covered**:
- 3: Account data protection (retention/disposal)
- 7: Access restriction
- 9: Physical security
- 12: Policies and procedures

---

### SAQ B-IP - Standalone IP-Connected Payment Terminals

**Eligibility Criteria**:
- Standalone, IP-connected point-of-interaction (POI) terminals
- POI devices are not connected to other systems
- POI devices validated by PCI PTS
- No electronic cardholder data storage
- No e-commerce

**Typical Scenarios**:
- Retail with IP-connected credit card terminals
- Restaurants with standalone wireless (IP) terminals
- PIN entry devices (PED) connected via IP

**Question Count**: ~82 questions

**Key Requirements Covered**:
- 1: Network security controls (for terminal network)
- 2: Secure configurations
- 4: Transmission encryption
- 9: Physical security
- 12: Policies and procedures

---

### SAQ C - Payment Application Systems

**Eligibility Criteria**:
- Payment application connected to the internet
- No electronic cardholder data storage
- No e-commerce channel
- Payment application system is isolated

**Typical Scenarios**:
- Retail POS systems connected to internet for processing
- Hospitality management systems with payment capabilities
- Restaurant systems with integrated payments

**Question Count**: ~160 questions

**Key Requirements Covered**:
- 1: Network security controls
- 2: Secure configurations
- 3: Account data protection
- 4: Transmission encryption
- 5: Malware protection
- 6: Secure systems and software
- 7-8: Access control and authentication
- 9: Physical security
- 10: Logging and monitoring
- 11: Security testing
- 12: Policies and procedures

---

### SAQ C-VT - Virtual Terminal Only

**Eligibility Criteria**:
- Process cardholder data only via virtual terminal
- Virtual terminal is provided by third-party service provider
- Virtual terminal accessed via web browser
- No electronic cardholder data storage
- No e-commerce

**Typical Scenarios**:
- Call center using web-based payment portal
- Small business taking phone orders via provider's web interface
- Service businesses entering card data for phone payments

**Question Count**: ~79 questions

**Key Requirements Covered**:
- 2: Secure configurations (workstation)
- 3: Account data protection
- 6: Secure systems
- 9: Physical security
- 12: Policies and procedures

---

### SAQ D - All Other Merchants and Service Providers

**Eligibility Criteria**:
- Service providers (any)
- Merchants that don't qualify for other SAQ types
- Merchants that store cardholder data electronically
- Any merchant with complex payment environments

**When SAQ D Applies**:
- You store cardholder data electronically
- You have multiple payment channels not covered by single SAQ
- You're a service provider handling cardholder data
- Your payment environment is complex

**Question Count**: ~329 questions (merchants) or ~347 (service providers)

**Key Requirements Covered**:
- ALL 12 requirements fully

---

### SAQ P2PE - Point-to-Point Encryption

**Eligibility Criteria**:
- Use ONLY hardware payment terminals included in PCI-listed P2PE solution
- No electronic cardholder data access (decryption happens at processor)
- P2PE solution provider manages decryption environment
- No e-commerce

**Typical Scenarios**:
- Retail using validated P2PE terminals
- Hospitality using P2PE-validated hardware
- Any business using complete P2PE solution

**Question Count**: ~33 questions

**Key Requirements Covered**:
- 3: Account data protection (P2PE specific)
- 9: Physical security (terminal protection)
- 12: Policies and procedures

---

## SAQ Comparison Matrix

| SAQ | E-commerce | Card Present | Stores CHD | Questions | Complexity |
|-----|------------|--------------|------------|-----------|------------|
| A | Yes | No | No | ~22 | Low |
| A-EP | Yes | No | No | ~191 | Medium |
| B | No | Yes (dial) | No | ~41 | Low |
| B-IP | No | Yes (IP) | No | ~82 | Low-Med |
| C | No | Yes | No | ~160 | Medium |
| C-VT | No | Yes (VT) | No | ~79 | Low-Med |
| D | Any | Any | Any | ~329 | High |
| P2PE | No | Yes (P2PE) | No | ~33 | Low |

---

## Common Selection Mistakes

### Mistake 1: Choosing SAQ A when you have JavaScript

**Problem**: Your checkout page has JavaScript that interacts with the payment form, even if you don't receive CHD directly.

**Correct Choice**: SAQ A-EP

### Mistake 2: Ignoring back-office systems

**Problem**: Even if POS is standalone, back-office systems may store CHD.

**Correct Choice**: May require SAQ D or multiple SAQs

### Mistake 3: Mixing channels without considering scope

**Problem**: E-commerce + retail = complex environment

**Correct Choice**: Usually SAQ D or segment environments for separate SAQs

### Mistake 4: Assuming tokenization eliminates requirements

**Problem**: Even with tokenization, you may handle CHD briefly

**Correct Choice**: Depends on where/how tokenization occurs

---

## Steps to Select Your SAQ

### Step 1: Inventory Payment Channels

List all ways you accept payment cards:
- [ ] E-commerce website
- [ ] Mail order
- [ ] Telephone order
- [ ] In-person (retail)
- [ ] Mobile point of sale
- [ ] Virtual terminal
- [ ] Other: ____________

### Step 2: Identify Payment Flow

For each channel, document:
- Where does cardholder data enter?
- Where does it go?
- Is it stored anywhere?
- Who handles the data?

### Step 3: Review Eligibility Criteria

For each potential SAQ, verify:
- [ ] All eligibility criteria met
- [ ] No excluded scenarios apply
- [ ] Environment matches SAQ assumptions

### Step 4: Consult with Acquirer

- Confirm selected SAQ type
- Get approval if uncertain
- Document agreement

### Step 5: Complete SAQ

- Answer all applicable questions
- Gather supporting evidence
- Address any "No" responses

---

## Hybrid Environments

If you have multiple payment channels:

**Option 1: Single SAQ D**
- Cover entire environment with comprehensive SAQ
- Simpler administration
- More questions to answer

**Option 2: Network Segmentation + Multiple SAQs**
- Segment each payment channel
- Complete appropriate SAQ for each
- More complex but potentially fewer total questions

**Example**:
```
Retail POS (segmented) → SAQ B-IP
E-commerce (separate) → SAQ A or A-EP
Combined must still be validated
```

---

## Service Provider Considerations

If you are a service provider:

1. **Always SAQ D** for service providers
2. Must complete annually
3. Quarterly ASV scans required
4. Penetration testing required
5. May need full ROC depending on transaction volume

---

## Questions to Ask Your Payment Provider

1. "Is our integration SAQ A eligible, or does it require SAQ A-EP?"
2. "Are your terminals PCI PTS validated?"
3. "Is this a validated P2PE solution?"
4. "Where does tokenization occur in the payment flow?"
5. "What is your PCI DSS compliance status? Can you provide your AOC?"

---

## Next Steps After Selection

1. Download the appropriate SAQ from [PCI SSC](https://www.pcisecuritystandards.org/)
2. Review all questions before starting
3. Gather evidence for "Yes" responses
4. Document compensating controls for any requirements not met
5. Complete Attestation of Compliance (AOC)
6. Submit to acquirer/payment brand as required
