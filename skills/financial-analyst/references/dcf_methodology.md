# DCF Valuation Methodology Guide

## Overview

Discounted Cash Flow (DCF) analysis is a fundamental valuation method that estimates the present value of an investment based on its expected future cash flows. This guide provides step-by-step methodology for conducting rigorous DCF analysis.

---

## 1. Core Principles

### 1.1 Time Value of Money

Money today is worth more than the same amount in the future because:
- It can be invested to earn returns
- There is risk of not receiving future payments
- Inflation erodes purchasing power

### 1.2 DCF Formula

```
DCF Value = Σ (CFt / (1 + r)^t) + Terminal Value / (1 + r)^n

Where:
- CFt = Cash flow at time t
- r = Discount rate (WACC or required return)
- n = Number of projection periods
```

---

## 2. Step-by-Step DCF Process

### Step 1: Project Free Cash Flows

**Free Cash Flow to Firm (FCFF):**
```
FCFF = EBIT × (1 - Tax Rate)
       + Depreciation & Amortization
       - Capital Expenditures
       - Change in Working Capital
```

**Free Cash Flow to Equity (FCFE):**
```
FCFE = FCFF
       - Interest Expense × (1 - Tax Rate)
       + Net Borrowing
```

**Projection Guidelines:**
- Explicit forecast period: 5-10 years typically
- Early years: More detailed, use specific drivers
- Later years: Transition toward normalized growth

### Step 2: Determine Discount Rate

**Weighted Average Cost of Capital (WACC):**
```
WACC = (E/V × Re) + (D/V × Rd × (1 - Tc))

Where:
- E = Market value of equity
- D = Market value of debt
- V = E + D (Total value)
- Re = Cost of equity
- Rd = Cost of debt
- Tc = Corporate tax rate
```

**Cost of Equity (CAPM):**
```
Re = Rf + β × (Rm - Rf)

Where:
- Rf = Risk-free rate (10-year Treasury)
- β = Beta (systematic risk)
- Rm = Expected market return
- (Rm - Rf) = Market risk premium (typically 5-7%)
```

**Typical WACC Ranges:**
| Company Type | WACC Range |
|-------------|------------|
| Large, stable | 6-8% |
| Medium risk | 8-10% |
| Growth companies | 10-12% |
| Emerging/Risky | 12-15%+ |

### Step 3: Calculate Terminal Value

**Method 1: Gordon Growth Model (Perpetuity)**
```
Terminal Value = FCFn × (1 + g) / (WACC - g)

Where:
- FCFn = Final year cash flow
- g = Long-term growth rate (typically 2-3%, ≤ GDP growth)
```

**Method 2: Exit Multiple**
```
Terminal Value = EBITDAn × EV/EBITDA Multiple
```

**Guidance:**
- Terminal value often represents 60-80% of total DCF value
- Use conservative growth rates (2-3% maximum)
- Cross-check with exit multiples for reasonableness

### Step 4: Calculate Present Value

Discount all cash flows and terminal value to present:

```
PV = Σ (CFt / (1 + WACC)^t) + TV / (1 + WACC)^n
```

### Step 5: Derive Enterprise and Equity Value

```
Enterprise Value = Sum of PV of all cash flows

Equity Value = Enterprise Value
             - Net Debt
             - Minority Interests
             - Preferred Stock

Per Share Value = Equity Value / Shares Outstanding
```

---

## 3. Key Investment Metrics

### 3.1 Net Present Value (NPV)

**Formula:**
```
NPV = -Initial Investment + Σ (CFt / (1 + r)^t)
```

**Decision Rule:**
| NPV | Decision |
|-----|----------|
| > 0 | Accept - Project creates value |
| = 0 | Indifferent - Meets hurdle rate exactly |
| < 0 | Reject - Project destroys value |

### 3.2 Internal Rate of Return (IRR)

**Definition:** The discount rate at which NPV = 0

**Calculation Method (Newton-Raphson):**
```python
def calculate_irr(cash_flows, guess=0.10):
    rate = guess
    for _ in range(100):
        npv = sum(cf / (1 + rate)**t for t, cf in enumerate(cash_flows))
        if abs(npv) < 0.0001:
            return rate
        derivative = sum(-t * cf / (1 + rate)**(t+1) for t, cf in enumerate(cash_flows))
        rate = rate - npv / derivative
    return rate
```

**Decision Rule:**
| IRR vs WACC | Decision |
|-------------|----------|
| IRR > WACC | Accept |
| IRR < WACC | Reject |

**IRR Limitations:**
- Multiple IRRs possible with non-conventional cash flows
- Assumes reinvestment at IRR (may be unrealistic)
- Cannot compare mutually exclusive projects of different sizes

### 3.3 Payback Period

**Simple Payback:**
```
Years until cumulative cash flow ≥ Initial Investment
```

**Discounted Payback:**
```
Years until cumulative discounted cash flow ≥ Initial Investment
```

**Decision Rule:**
- Shorter payback = Lower risk
- Typical targets: 3-5 years for capital projects

---

## 4. Sensitivity Analysis

### 4.1 Single-Variable Sensitivity

Test NPV impact by varying one assumption at a time:

| Variable | -20% | -10% | Base | +10% | +20% |
|----------|------|------|------|------|------|
| Revenue | | | NPV | | |
| COGS | | | NPV | | |
| WACC | | | NPV | | |

### 4.2 Scenario Analysis

**Define scenarios:**
- **Best Case:** Optimistic assumptions
- **Base Case:** Most likely assumptions
- **Worst Case:** Conservative assumptions

Calculate NPV, IRR, Payback for each scenario.

### 4.3 Break-Even Analysis

Find values where NPV = 0:
- Minimum revenue required
- Maximum acceptable cost
- Highest viable discount rate

---

## 5. Common Errors to Avoid

### 5.1 Cash Flow Errors
- Including non-cash expenses (depreciation) as cash outflows
- Double-counting interest (in cash flows AND discount rate)
- Ignoring working capital changes
- Using accounting profits instead of cash flows

### 5.2 Discount Rate Errors
- Using WACC for equity-only cash flows (or vice versa)
- Not adjusting for project-specific risk
- Using historical rates without current market consideration
- Inconsistent treatment of inflation (real vs. nominal)

### 5.3 Terminal Value Errors
- Growth rate exceeding GDP/inflation
- Inappropriate exit multiples
- Not testing sensitivity to terminal assumptions
- Ignoring terminal value's large impact on total value

### 5.4 General Errors
- Inconsistent time periods (fiscal vs. calendar year)
- Currency mismatches
- Ignoring taxes or using wrong tax rates
- Not documenting assumptions

---

## 6. Best Practices

### 6.1 Documentation
- Document all assumptions with sources
- Show sensitivity to key variables
- Provide comparable transaction/company data
- Include sanity checks

### 6.2 Validation
- Cross-check with comparable company multiples
- Verify against recent transaction values
- Test reasonableness of implied growth rates
- Review with fresh eyes after initial analysis

### 6.3 Presentation
- Lead with key metrics (NPV, IRR, Payback)
- Show sensitivity/scenario ranges
- Highlight key assumptions and risks
- Provide clear recommendation with rationale

---

## 7. Quick Reference Tables

### Discount Rate Selection

| Risk Level | WACC Range | Example |
|-----------|------------|---------|
| Very Low | 5-7% | Government contracts, regulated utilities |
| Low | 7-9% | Established businesses, stable industries |
| Medium | 9-12% | Growth companies, competitive markets |
| High | 12-15% | Startups, emerging markets |
| Very High | 15%+ | Turnarounds, distressed assets |

### Terminal Growth Rate

| Scenario | Growth Rate |
|----------|-------------|
| Conservative | 1-2% |
| Moderate | 2-3% |
| Optimistic | 3-4% |
| Maximum | GDP growth rate |

### Investment Decision Matrix

| NPV | IRR vs WACC | Payback | Decision |
|-----|-------------|---------|----------|
| + | > WACC | Short | Strong Accept |
| + | > WACC | Long | Accept with caution |
| + | < WACC | - | Review assumptions |
| - | < WACC | Long | Reject |
