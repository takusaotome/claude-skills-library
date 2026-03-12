# GHG Emission Factors Reference

## Overview

This document provides commonly used emission factors for calculating greenhouse gas (GHG) emissions in sustainability reporting. Emission factors convert activity data (e.g., fuel consumption, electricity use) into CO2-equivalent emissions.

**Important Notes**:
- Emission factors vary by region, fuel type, and year
- Always use the most recent factors available for your region
- Document sources and methodologies in your GHG inventory
- Consider getting third-party verification for reported emissions

## Scope 1: Direct Emissions

### Stationary Combustion (Fuel)

| Fuel Type | Emission Factor | Unit | CO2 | CH4 | N2O |
|-----------|-----------------|------|-----|-----|-----|
| Natural Gas | 53.06 | kg CO2e/MMBtu | 53.02 | 0.001 | 0.0001 |
| Diesel/Gas Oil | 73.96 | kg CO2e/MMBtu | 73.84 | 0.003 | 0.0006 |
| LPG (Propane) | 62.87 | kg CO2e/MMBtu | 62.76 | 0.003 | 0.0006 |
| Heating Oil | 73.25 | kg CO2e/MMBtu | 73.15 | 0.003 | 0.0006 |
| Coal (Bituminous) | 93.28 | kg CO2e/MMBtu | 93.10 | 0.011 | 0.0016 |

**Alternative Units**:
| Fuel Type | Emission Factor | Unit |
|-----------|-----------------|------|
| Natural Gas | 1.93 | kg CO2e/m³ |
| Natural Gas | 2.02 | kg CO2e/therm |
| Diesel | 2.68 | kg CO2e/liter |
| Gasoline | 2.31 | kg CO2e/liter |
| LPG | 1.51 | kg CO2e/liter |

### Mobile Combustion (Vehicles)

| Vehicle Type | Emission Factor | Unit |
|--------------|-----------------|------|
| Gasoline Passenger Car | 0.21 | kg CO2e/km |
| Diesel Passenger Car | 0.17 | kg CO2e/km |
| Light-Duty Truck (Gasoline) | 0.27 | kg CO2e/km |
| Heavy-Duty Truck (Diesel) | 0.89 | kg CO2e/km |
| Motorcycle | 0.11 | kg CO2e/km |

**By Fuel**:
| Fuel | Emission Factor | Unit |
|------|-----------------|------|
| Gasoline | 8.78 | kg CO2e/gallon (US) |
| Diesel | 10.21 | kg CO2e/gallon (US) |
| Gasoline | 2.32 | kg CO2e/liter |
| Diesel | 2.70 | kg CO2e/liter |

### Refrigerants (Fugitive Emissions)

| Refrigerant | GWP (100-year) | Common Uses |
|-------------|----------------|-------------|
| HFC-134a | 1,430 | Vehicle AC, commercial refrigeration |
| R-410A | 2,088 | Residential AC |
| R-404A | 3,922 | Commercial refrigeration |
| R-407C | 1,774 | Commercial AC |
| CO2 (R-744) | 1 | Low-GWP alternative |
| Ammonia (R-717) | 0 | Industrial refrigeration |

**Calculation**: Emissions (tCO2e) = Refrigerant Leakage (kg) × GWP / 1000

## Scope 2: Indirect Energy Emissions

### Electricity (Grid Average by Region)

**United States (2022 eGRID)**:
| Region | Emission Factor | Unit |
|--------|-----------------|------|
| US Average | 0.386 | kg CO2e/kWh |
| CAMX (California) | 0.225 | kg CO2e/kWh |
| ERCT (Texas) | 0.398 | kg CO2e/kWh |
| RFCW (Midwest) | 0.499 | kg CO2e/kWh |
| NYCW (New York) | 0.238 | kg CO2e/kWh |
| SRSO (Southeast) | 0.411 | kg CO2e/kWh |

**International (IEA 2022)**:
| Country/Region | Emission Factor | Unit |
|----------------|-----------------|------|
| World Average | 0.494 | kg CO2e/kWh |
| EU-27 | 0.256 | kg CO2e/kWh |
| China | 0.582 | kg CO2e/kWh |
| India | 0.708 | kg CO2e/kWh |
| Japan | 0.471 | kg CO2e/kWh |
| UK | 0.207 | kg CO2e/kWh |
| Germany | 0.385 | kg CO2e/kWh |
| France | 0.056 | kg CO2e/kWh |
| Brazil | 0.085 | kg CO2e/kWh |
| Canada | 0.120 | kg CO2e/kWh |
| Australia | 0.656 | kg CO2e/kWh |

### Location-Based vs Market-Based Reporting

**Location-Based Method**:
- Uses average grid emission factor for the location
- Reflects actual physical electricity flows
- Required disclosure under GRI 305

**Market-Based Method**:
- Reflects renewable energy purchases and contracts
- Uses contractual instruments (RECs, PPAs, green tariffs)
- Also required under GRI 305

**Market-Based Hierarchy**:
1. Energy attribute certificates (RECs, GOs, I-RECs)
2. Direct contracts (PPAs) with generators
3. Supplier-specific emission factors
4. Residual mix (grid minus tracked instruments)
5. Location-based (if none of above available)

### Steam, Heating, Cooling

| Energy Type | Emission Factor | Unit |
|-------------|-----------------|------|
| Steam (from natural gas) | 0.067 | kg CO2e/kWh |
| District Heating (avg) | 0.18 | kg CO2e/kWh |
| District Cooling (avg) | 0.15 | kg CO2e/kWh |

## Scope 3: Value Chain Emissions

### Category 1: Purchased Goods and Services

**Spend-Based Method** (when supplier data unavailable):
| Sector | Emission Factor | Unit |
|--------|-----------------|------|
| Agriculture | 0.50 | kg CO2e/$ spent |
| Mining & Extraction | 0.35 | kg CO2e/$ spent |
| Manufacturing - General | 0.25 | kg CO2e/$ spent |
| Manufacturing - Chemicals | 0.45 | kg CO2e/$ spent |
| Professional Services | 0.10 | kg CO2e/$ spent |
| Transportation & Logistics | 0.40 | kg CO2e/$ spent |
| Technology & Telecom | 0.15 | kg CO2e/$ spent |

### Category 4 & 9: Transportation

| Mode | Emission Factor | Unit |
|------|-----------------|------|
| Road Freight (truck) | 0.062 | kg CO2e/tonne-km |
| Rail Freight | 0.022 | kg CO2e/tonne-km |
| Sea Freight (container) | 0.016 | kg CO2e/tonne-km |
| Air Freight | 0.602 | kg CO2e/tonne-km |

### Category 6: Business Travel

| Mode | Emission Factor | Unit |
|------|-----------------|------|
| Air Travel - Short Haul (<3hrs) | 0.255 | kg CO2e/passenger-km |
| Air Travel - Medium Haul (3-6hrs) | 0.156 | kg CO2e/passenger-km |
| Air Travel - Long Haul (>6hrs) | 0.150 | kg CO2e/passenger-km |
| Rail Travel | 0.041 | kg CO2e/passenger-km |
| Rental Car | 0.171 | kg CO2e/km |
| Taxi/Ride-share | 0.149 | kg CO2e/km |
| Hotel Stay | 20.0 | kg CO2e/night |

### Category 7: Employee Commuting

| Mode | Emission Factor | Unit |
|------|-----------------|------|
| Car (average) | 0.17 | kg CO2e/km |
| Bus | 0.089 | kg CO2e/km |
| Subway/Metro | 0.041 | kg CO2e/km |
| Work from Home | 0.5-2.0 | kg CO2e/day |

## Global Warming Potentials (GWP)

Used to convert other GHGs to CO2-equivalent:

| Gas | GWP (100-year, AR5) | GWP (100-year, AR6) |
|-----|---------------------|---------------------|
| CO2 | 1 | 1 |
| CH4 (Methane) | 28 | 27.9 |
| N2O (Nitrous Oxide) | 265 | 273 |
| SF6 | 23,500 | 25,200 |
| NF3 | 16,100 | 17,400 |

## Data Sources

### Primary Sources
- **US EPA**: [Emission Factors Hub](https://www.epa.gov/climateleadership/ghg-emission-factors-hub)
- **IPCC**: AR6 GWP values, emission factor guidance
- **IEA**: World Energy Outlook, electricity emission factors by country
- **GHG Protocol**: Scope 3 calculation guidance, emission factor databases
- **DEFRA**: UK Government conversion factors (widely used internationally)

### Emission Factor Databases
- **US EPA eGRID**: US regional electricity factors
- **IEA CO2 Emissions from Fuel Combustion**: International electricity
- **Ecoinvent**: LCA database (paid)
- **DEFRA Conversion Factors**: Comprehensive UK factors

## Calculation Examples

### Example 1: Natural Gas Consumption
```
Consumption: 10,000 m³/year
Emission Factor: 1.93 kg CO2e/m³
Emissions = 10,000 × 1.93 = 19,300 kg CO2e = 19.3 tCO2e
```

### Example 2: Electricity (Location-Based)
```
Consumption: 500,000 kWh/year
Location: Texas (ERCT)
Emission Factor: 0.398 kg CO2e/kWh
Emissions = 500,000 × 0.398 = 199,000 kg CO2e = 199 tCO2e
```

### Example 3: Business Travel (Air)
```
Route: New York to London (5,570 km, long-haul)
Passengers: 50 employees
Emission Factor: 0.150 kg CO2e/passenger-km
Emissions = 5,570 × 2 (round trip) × 50 × 0.150 = 83,550 kg CO2e = 83.6 tCO2e
```

## Best Practices

1. **Use region-specific factors** when available
2. **Document all assumptions and sources**
3. **Update factors annually** (use most recent available)
4. **Prefer primary data** over spend-based estimates
5. **Get third-party verification** for material emission sources
6. **Report methodology transparently** in sustainability reports
