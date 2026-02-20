# Inventory Optimization Guide

## Key Inventory Metrics

### 1. Inventory Turnover Ratio

```
Inventory Turnover = Cost of Goods Sold (annual) / Average Inventory Value

Benchmark:
- Retail: 5-10x (higher for grocery, lower for luxury)
- Manufacturing: 4-8x
- High-tech: 8-15x

Low turnover -> Excess inventory, obsolescence risk
High turnover -> Efficient, but risk of stockouts
```

### 2. Days of Inventory (DOI)

```
DOI = (Average Inventory / COGS) * 365

Example: If inventory turnover = 6x -> DOI = 365/6 = 61 days
```

### 3. Inventory Carrying Cost

```
Annual Carrying Cost = Average Inventory Value * Carrying Cost %

Carrying Cost % typically includes:
- Cost of capital (8-12%)
- Storage cost (2-4%)
- Insurance (1-3%)
- Obsolescence/shrinkage (2-5%)
-> Total: 15-25% of inventory value

Example: $5M average inventory * 20% = $1M annual carrying cost
```

### 4. Service Level Achievement

```
Fill Rate = Orders Fulfilled Completely / Total Orders * 100%
Target: 95-99% depending on industry

Stockout Frequency = Number of Stockout Days / Total Days
```

### Inventory Health Assessment Template

| Category | Current Inventory | DOI | Turnover | Excess (>90 days) | Obsolete (>180 days) | Status |
|----------|-------------------|-----|----------|-------------------|----------------------|--------|
| Raw Materials | $[value] | [days] | [x] | $[value] | $[value] | [status] |
| WIP | $[value] | [days] | [x] | $[value] | $[value] | [status] |
| Finished Goods | $[value] | [days] | [x] | $[value] | $[value] | [status] |
| **Total** | **$[value]** | **[days]** | **[x]** | **$[value]** | **$[value]** | **[status]** |

---

## Safety Stock Calculation

**Safety Stock Formula** (for normally distributed demand):

```
SS = Z * sigma_DLT

Where:
- Z = Service level factor (Z-score)
  95% service level -> Z = 1.65
  97.5% service level -> Z = 1.96
  99% service level -> Z = 2.33

- sigma_DLT = Standard deviation of demand during lead time
  sigma_DLT = sqrt(LT * sigma_D^2 + D_avg^2 * sigma_LT^2)

  Where:
  - LT = Lead time (in days)
  - sigma_D = Standard deviation of daily demand
  - D_avg = Average daily demand
  - sigma_LT = Standard deviation of lead time (in days)
```

**Variable Definitions (IMPORTANT)**:
- `sigma_DLT`: Demand variability over the full lead time period (composite metric)
- `sigma_D`: Daily demand variability (demand-side uncertainty)
- `sigma_LT`: Lead time variability in days (supply-side uncertainty)

**Example Calculation**:
```
Product: Widget A
- Average daily demand (D_avg): 100 units
- Std dev of daily demand (sigma_D): 20 units
- Average lead time (LT): 14 days
- Std dev of lead time (sigma_LT): 3 days
- Target service level: 97.5% (Z = 1.96)

Step 1: Calculate sigma_DLT
sigma_DLT = sqrt(14 * 20^2 + 100^2 * 3^2)
sigma_DLT = sqrt(14 * 400 + 10,000 * 9)
sigma_DLT = sqrt(5,600 + 90,000)
sigma_DLT = sqrt(95,600)
sigma_DLT = 309 units

Step 2: Calculate Safety Stock
SS = 1.96 * 309 = 605 units

Step 3: Reorder Point
ROP = (Average Daily Demand * Lead Time) + Safety Stock
ROP = (100 * 14) + 605 = 2,005 units

Interpretation:
- When inventory reaches 2,005 units -> Place replenishment order
- Safety stock of 605 units provides 97.5% service level
```

---

## Economic Order Quantity (EOQ)

**EOQ Formula** (optimal order quantity to minimize total cost):

```
EOQ = sqrt(2 * D * S / H)

Where:
- D = Annual demand (units)
- S = Order cost per order ($)
- H = Holding cost per unit per year ($)

Total Cost = (D/Q * S) + (Q/2 * H)
Where Q = Order quantity
```

**Example**:
```
Product: Widget A
- Annual demand: 36,000 units
- Order cost: $150 per order
- Unit cost: $50
- Holding cost: 20% of unit cost = $10 per unit per year

EOQ = sqrt(2 * 36,000 * 150 / 10)
EOQ = sqrt(10,800,000 / 10)
EOQ = sqrt(1,080,000)
EOQ = 1,039 units

Number of orders per year = 36,000 / 1,039 = 35 orders
Order frequency = 365 / 35 = every 10.4 days

Total Cost at EOQ:
- Ordering cost: (36,000/1,039) * $150 = $5,196
- Holding cost: (1,039/2) * $10 = $5,195
- Total: $10,391

(Note: At EOQ, ordering cost = holding cost)
```

**EOQ Adjustments**:
- **Quantity Discounts**: Adjust EOQ if supplier offers price breaks
- **Storage Constraints**: May need to order less than EOQ due to warehouse space
- **Shelf Life**: Perishable items may require smaller orders
- **ABC Classification**: Calculate EOQ for A items, use simpler rules for B/C items

---

## Inventory Policy Design

### Policy by Product Category

**A Items (High Value)**:
- **Policy**: Continuous Review (s, Q) - Monitor constantly, order fixed quantity when reaching reorder point
- **Parameters**: Calculate EOQ and Safety Stock precisely
- **Review Frequency**: Daily monitoring

**B Items (Medium Value)**:
- **Policy**: Periodic Review (R, S) - Review at fixed intervals, order up to target level
- **Parameters**: Review weekly, order up to target inventory level
- **Review Frequency**: Weekly

**C Items (Low Value)**:
- **Policy**: Min-Max or Two-Bin System
- **Parameters**: Simple replenishment rules
- **Review Frequency**: Monthly or when bin empty

### Inventory Policy Documentation Template

Use `scripts/generate_inventory_policy.py` to generate, or use the template below:

| SKU | Category | Policy Type | Reorder Point | Order Qty | Max Stock | Review Freq |
|-----|----------|-------------|---------------|-----------|-----------|-------------|
| [sku] | A | Continuous (s,Q) | [calculated] | [EOQ] | [max] | Daily |
| [sku] | B | Periodic (R,S) | - | Variable | [target] | Weekly |
| [sku] | C | Min-Max | [min] | [fixed] | [max] | Monthly |
