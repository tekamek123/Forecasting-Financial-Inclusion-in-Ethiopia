# Forecasting Financial Inclusion in Ethiopia

## Overview

A comprehensive forecasting system that tracks Ethiopia's digital financial transformation using time series methods. Built for Selam Analytics and their consortium of stakeholders including development finance institutions, mobile money operators, and the National Bank of Ethiopia.

## Business Context

Ethiopia is undergoing rapid digital financial transformation:
- **Telebirr**: 54+ million users since 2021 launch
- **M-Pesa**: 10+ million users since 2023 market entry
- **Digital P2P transfers**: Now surpass ATM cash withdrawals
- **Current Challenge**: Only 49% of Ethiopian adults have financial accounts (2024 Global Findex)

## Project Objectives

### Primary Questions
1. What drives financial inclusion in Ethiopia?
2. How do events (product launches, policy changes, infrastructure investments) affect inclusion outcomes?
3. How did financial inclusion rates change in 2025 and what are the projections for 2026-2027?

### Core Indicators (World Bank Global Findex Framework)

#### Access - Account Ownership Rate
> "The share of adults (age 15+) who report having an account (by themselves or together with someone else) at a bank or another type of financial institution or report personally using a mobile money service in the past 12 months."

**Ethiopia's Trajectory:**
| Year | Account Ownership | Change |
|------|-------------------|---------|
| 2011 | 14% | — |
| 2014 | 22% | +8pp |
| 2017 | 35% | +13pp |
| 2021 | 46% | +11pp |
| 2024 | 49% | +3pp |

#### Usage - Digital Payment Adoption Rate
> "The share of adults who report using mobile money, a debit or credit card, or a mobile phone to make a payment from an account, or report using the internet to pay bills or to buy something online, in the past 12 months."

**Ethiopia's 2024 Indicators:**
- Mobile money account ownership: 9.45%
- Made or received digital payment: ~35%
- Used account to receive wages: ~15%

## Data Structure

### Primary Dataset: `ethiopia_fi_unified_data`
Unified schema where all records share the same structure:

| record_type | Count | Description |
|-------------|-------|-------------|
| observation | 30 | Measured values (Findex surveys, operator reports, infrastructure data) |
| event | 10 | Policies, product launches, market entries, milestones |
| impact_link | 14 | Modeled relationships between events and indicators |
| target | 3 | Official policy goals (e.g., NFIS-II targets) |

**Key Design Principle**: Events are categorized by type but NOT pre-assigned to pillars. Their effects are captured through `impact_link` records to maintain data objectivity.

### Supporting Files
- `reference_codes` - Valid values for all categorical fields
- `README.md` - Schema documentation
- `Additional Data Points Guide` - Data enrichment guidance with four sheets:
  - A. Alternative Baselines (IMF FAS, G20 indicators, GSMA, ITU, NBE reports)
  - B. Direct Correlation (active accounts, agent density, POS terminals, transaction volumes)
  - C. Indirect Correlation (smartphone penetration, data affordability, gender gap, urbanization)
  - D. Market Nuances (Ethiopia-specific context and dynamics)

## Project Deliverables

1. **Data Understanding & Enrichment**
   - Analyze the provided financial inclusion dataset
   - Enrich with additional relevant indicators using the Data Enrichment Guide

2. **Pattern Analysis**
   - Analyze patterns and relationships in Ethiopia's inclusion data
   - Identify key drivers and correlations

3. **Event Impact Modeling**
   - Model how different events affect inclusion indicators
   - Use comparable country evidence for impact estimation

4. **Forecasting System**
   - Build models to forecast Access and Usage indicators for 2025-2027
   - Include appropriate confidence bounds

5. **Interactive Dashboard**
   - Present findings through an interactive visualization interface
   - Translate technical analysis into policy insights

## Technical Approach

### Skills Development
- Working with unified data schemas
- Exploratory data analysis with sparse time series
- Event impact estimation using comparable country evidence
- Regression modeling with intervention variables
- Forecasting with limited historical data
- Interactive dashboard development

### Knowledge Areas
- Global Findex methodology and definitions
- Ethiopia's digital payment ecosystem (Telebirr, M-Pesa, EthSwitch, Fayda)
- Policy impact assessment approaches
- Working with uncertainty in data-limited contexts

## Ethiopia Market Context

### Unique Characteristics
- **P2P Dominance**: Used for commerce, not just transfers
- **Mobile Money-Only Users**: Rare (~0.5%)
- **Bank Account Accessibility**: Easily accessible
- **Credit Penetration**: Very low levels

### Key Players
- **Telebirr**: Leading mobile money platform
- **M-Pesa**: Recent market entrant with rapid growth
- **EthSwitch**: National payment switch
- **Fayda**: Digital ID system

## Project Structure

```
week10/
├── README.md                          # This file
├── data/                              # Data directory
│   ├── ethiopia_fi_unified_data.csv   # Primary dataset
│   ├── reference_codes.csv            # Code definitions
│   └── additional_data_guide.xlsx     # Data enrichment guidance
├── notebooks/                         # Analysis notebooks
├── src/                              # Source code
│   ├── data_processing.py            # Data cleaning and enrichment
│   ├── modeling.py                   # Forecasting models
│   └── dashboard.py                   # Interactive dashboard
├── reports/                          # Analysis reports
└── requirements.txt                   # Python dependencies
```

## Getting Started

1. **Setup Environment**
   ```bash
   pip install -r requirements.txt
   ```

2. **Load Data**
   ```python
   import pandas as pd
   data = pd.read_csv('data/ethiopia_fi_unified_data.csv')
   ```

3. **Run Analysis**
   - See `notebooks/` for exploratory analysis
   - See `src/` for modeling and forecasting code

## Team

**Tutors:**
- Kerod
- Mahbubah  
- Filimon

---

*This project represents a unique opportunity to contribute to Ethiopia's financial inclusion journey through data-driven insights and forecasting.*
