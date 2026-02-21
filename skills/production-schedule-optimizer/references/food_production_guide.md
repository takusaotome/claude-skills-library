# Food Production Guide

## Table of Contents
- [Shelf Life Based Production Frequency](#shelf-life-based-production-frequency)
- [FEFO Overview](#fefo-overview)
- [Baseline Quantities](#baseline-quantities)
- [HACCP Considerations](#haccp-considerations)

---

## Shelf Life Based Production Frequency

### Core Formula

```
production_count = min(ceil(7 / shelf_life_days), 7)
```

This determines how many times per week a product must be manufactured to ensure freshness. The formula ensures that product is always available within its shelf life window.

### Frequency Lookup Table

| Shelf Life (days) | Production Count (per week) | Interval (days) | Rationale |
|-------------------|-----------------------------|-----------------|-----------|
| 1 | 7 | 1 | Must produce daily; no carryover possible |
| 2 | 4 | 1 | Produce every ~1.75 days; rounded up for safety |
| 3 | 3 | 2 | Produce every 2.3 days; 3 runs covers the week |
| 4 | 2 | 3 | Produce twice weekly; each batch covers ~3.5 days |
| 5 | 2 | 3 | Produce twice weekly; each batch covers ~3.5 days |
| 6 | 2 | 3 | Produce twice weekly; comfortable coverage |
| 7 | 1 | 7 | Produce once weekly; full-week coverage |
| 14 | 1 | 7 | Produce once weekly; extended shelf life |

### Examples

**Grilled Chicken (shelf_life=1):**
- production_count = min(ceil(7/1), 7) = 7
- Must produce every single day
- No buffer for production delays

**Sandwich Bread (shelf_life=2):**
- production_count = min(ceil(7/2), 7) = min(4, 7) = 4
- Produce 4 times per week (e.g., MON, TUE, WED, THU)
- Each batch covers approximately 1.75 days

**Tomato Sauce (shelf_life=5):**
- production_count = min(ceil(7/5), 7) = min(2, 7) = 2
- Produce twice per week (e.g., MON, THU)
- Each batch covers 3.5 days with overlap margin

**House Dressing (shelf_life=7):**
- production_count = min(ceil(7/7), 7) = min(1, 7) = 1
- Produce once per week (e.g., MON)
- Full week coverage from single production run

### Safety Margin

The ceil() function in the formula provides a built-in safety margin. For shelf_life=3, the mathematical frequency is 2.33, but we round up to 3. This means product is always available before the previous batch expires.

---

## FEFO Overview

### First Expiry First Out

FEFO (First Expiry First Out) is the standard inventory rotation method for perishable goods. Unlike FIFO (First In First Out), FEFO considers the actual expiration date rather than the production date.

### Integration with Scheduling

The scheduler integrates FEFO principles through:

1. **Sort priority**: Products with shorter shelf life are scheduled with higher priority (shelf_life_days ASC in the sort key)
2. **Day distribution**: Short-shelf-life products get evenly spaced production days to avoid gaps in availability
3. **Production frequency**: The formula automatically increases production frequency for shorter shelf lives

### Practical Implications

- Products with shelf_life=1 must be produced and consumed on the same day
- Products with shelf_life=2 can bridge one overnight period
- Weekend production gaps require shelf_life >= 3 to avoid Monday morning stockouts (unless weekend production is scheduled)

---

## Baseline Quantities

### Minimum Lot Size (base_qty)

The base_qty represents the minimum economically viable production quantity. It accounts for:

1. **Equipment setup time**: Fixed overhead regardless of batch size
2. **Material minimums**: Minimum ingredient quantities for recipe integrity
3. **Quality control**: Minimum sample size for testing
4. **Packaging runs**: Minimum quantities for packaging efficiency

### When Demand is Less Than base_qty

If `qty_per_run < base_qty`, the scheduler still produces one full lot (base_qty units). The surplus can be:

1. **Redistributed**: Sent to other outlets or channels
2. **Buffered**: Used as safety stock for the next production cycle
3. **Discounted**: Sold at reduced price before expiration

The scheduler does not reduce lot size below base_qty. This is a deliberate design decision to maintain quality and efficiency standards.

### Lot Count Calculation

```
lot_count = ceil(qty_per_run / base_qty)
duration_minutes = lot_count * prep_time_min
```

Partial lots require full prep_time_min because:
- Equipment cleaning between lots takes the same time regardless
- Temperature cycles cannot be shortened
- Quality inspection procedures are per-lot

---

## HACCP Considerations

### Temperature Zones and Room Assignment

HACCP (Hazard Analysis Critical Control Points) requires strict temperature control during food production. Room assignment should respect temperature zone compatibility:

| Zone | Temperature Range | Typical Rooms | Products |
|------|-------------------|---------------|----------|
| Hot | > 60C | BROTH, SAUCE | Soups, sauces, cooked items |
| Ambient | 20-25C | BAKERY | Bread, pastries, dry goods |
| Cold | 0-5C | COLD | Salads, dressings, cold items |
| Frozen | < -18C | FREEZER | Frozen products |

### Cross-Contamination Prevention

Room assignment in the scheduler inherently supports allergen and contamination control:

1. **Allergen segregation**: Products with different allergen profiles should be assigned to different rooms
2. **Raw/cooked separation**: Raw meat processing (MEAT room) must be physically separated from ready-to-eat areas (COLD room)
3. **room_codes restriction**: The products.csv `room_codes` field encodes which rooms are safe for each product

### Cleaning Time Between Products

When different products are manufactured sequentially in the same room, cleaning time may be required. The scheduler should account for:

- **Same category**: Minimal cleaning (5-10 min) between similar products
- **Different category**: Standard cleaning (15-30 min) between different product types
- **Allergen changeover**: Full sanitization (30-60 min) when switching allergen profiles

Currently, cleaning time is not explicitly modeled but can be approximated by adding buffer time to `prep_time_min` for products that typically follow different-category items.

### Documentation Requirements

HACCP compliance requires traceability. The schedule output should include:
- Production timestamp (date + time slot)
- Room assignment (temperature zone verification)
- Staff assignment (trained personnel verification)
- Batch/lot identification for recall capability
