#!/usr/bin/env python3
"""
Data Enrichment Script for Ethiopia Financial Inclusion Dataset
Adds new observations, events, and impact links based on enrichment log
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_new_observations():
    """Create new observation records based on enrichment log"""
    
    observations = []
    
    # 1. Historical Account Ownership (2011 Global Findex)
    observations.append({
        'record_id': 'OBS_031',
        'record_type': 'observation',
        'category': np.nan,
        'pillar': 'ACCESS',
        'indicator': 'Account Ownership Rate',
        'indicator_code': 'ACC_OWNERSHIP',
        'indicator_direction': np.nan,
        'value_numeric': 14.0,
        'value_text': np.nan,
        'value_type': 'percentage',
        'unit': '%',
        'observation_date': pd.Timestamp('2011-12-31'),
        'period_start': np.nan,
        'period_end': np.nan,
        'fiscal_year': np.nan,
        'gender': np.nan,
        'location': np.nan,
        'region': np.nan,
        'source_name': 'World Bank Global Findex Database 2011',
        'source_type': 'survey',
        'source_url': 'https://globalfindex.worldbank.org/',
        'confidence': 'high',
        'related_indicator': np.nan,
        'relationship_type': np.nan,
        'impact_direction': np.nan,
        'impact_magnitude': np.nan,
        'impact_estimate': np.nan,
        'lag_months': np.nan,
        'evidence_basis': np.nan,
        'comparable_country': np.nan,
        'collected_by': 'Data Science Team',
        'collection_date': pd.Timestamp('2025-01-28'),
        'original_text': '14% of adults in Ethiopia have an account (2011)',
        'notes': 'Baseline data for Ethiopia financial inclusion journey'
    })
    
    # 2. Mobile Phone Penetration Time Series
    mobile_pen_data = [
        (2015, 38.5), (2016, 42.1), (2017, 46.8), (2018, 51.2),
        (2019, 56.7), (2020, 62.3), (2021, 68.9), (2022, 74.5)
    ]
    
    for i, (year, value) in enumerate(mobile_pen_data):
        observations.append({
            'record_id': f'OBS_{32+i:03d}',
            'record_type': 'observation',
            'category': np.nan,
            'pillar': 'ACCESS',
            'indicator': 'Mobile Subscription Penetration',
            'indicator_code': 'ACC_MOBILE_PEN',
            'indicator_direction': np.nan,
            'value_numeric': value,
            'value_text': np.nan,
            'value_type': 'percentage',
            'unit': '%',
            'observation_date': pd.Timestamp(f'{year}-12-31'),
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'ITU World Telecommunication/ICT Indicators',
            'source_type': 'official_statistics',
            'source_url': 'https://www.itu.int/en/ITU-D/Statistics/Pages/default.aspx',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': f'Mobile phone penetration: {value}% in {year}',
            'notes': 'Key enabler for digital financial inclusion'
        })
    
    # 3. Internet Access Data
    internet_pen_data = [
        (2015, 2.1), (2016, 3.8), (2017, 8.6), (2018, 15.3),
        (2019, 18.6), (2020, 24.0), (2021, 29.7), (2022, 35.2)
    ]
    
    for i, (year, value) in enumerate(internet_pen_data):
        observations.append({
            'record_id': f'OBS_{40+i:03d}',
            'record_type': 'observation',
            'category': np.nan,
            'pillar': 'ACCESS',
            'indicator': 'Internet Access Penetration',
            'indicator_code': 'ACC_INTERNET_PEN',
            'indicator_direction': np.nan,
            'value_numeric': value,
            'value_text': np.nan,
            'value_type': 'percentage',
            'unit': '%',
            'observation_date': pd.Timestamp(f'{year}-12-31'),
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'ITU World Telecommunication/ICT Indicators',
            'source_type': 'official_statistics',
            'source_url': 'https://www.itu.int/en/ITU-D/Statistics/Pages/default.aspx',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': f'Internet penetration: {value}% in {year}',
            'notes': 'Prerequisite for digital payment adoption'
        })
    
    # 4. GDP per Capita
    gdp_data = [
        (2015, 860), (2016, 880), (2017, 770), (2018, 850),
        (2019, 950), (2020, 930), (2021, 990), (2022, 1030)
    ]
    
    for i, (year, value) in enumerate(gdp_data):
        observations.append({
            'record_id': f'OBS_{48+i:03d}',
            'record_type': 'observation',
            'category': np.nan,
            'pillar': 'AFFORDABILITY',
            'indicator': 'GDP per Capita',
            'indicator_code': 'AFF_GDP_PCAP',
            'indicator_direction': np.nan,
            'value_numeric': value,
            'value_text': np.nan,
            'value_type': 'currency',
            'unit': 'USD',
            'observation_date': pd.Timestamp(f'{year}-12-31'),
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'World Bank World Development Indicators',
            'source_type': 'official_statistics',
            'source_url': 'https://databank.worldbank.org/source/world-development-indicators',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': f'GDP per capita: ${value} in {year}',
            'notes': 'Economic context for financial inclusion'
        })
    
    # 5. Urbanization Rate
    urban_data = [
        (2015, 20.1), (2016, 20.6), (2017, 21.1), (2018, 21.6),
        (2019, 22.1), (2020, 22.6), (2021, 23.1), (2022, 23.6)
    ]
    
    for i, (year, value) in enumerate(urban_data):
        observations.append({
            'record_id': f'OBS_{56+i:03d}',
            'record_type': 'observation',
            'category': np.nan,
            'pillar': 'AFFORDABILITY',
            'indicator': 'Urbanization Rate',
            'indicator_code': 'AFF_URBAN_RATE',
            'indicator_direction': np.nan,
            'value_numeric': value,
            'value_text': np.nan,
            'value_type': 'percentage',
            'unit': '%',
            'observation_date': pd.Timestamp(f'{year}-12-31'),
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'UN World Urbanization Prospects',
            'source_type': 'official_statistics',
            'source_url': 'https://population.un.org/wup/',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': f'Urbanization rate: {value}% in {year}',
            'notes': 'Urbanization correlates with financial service access'
        })
    
    return observations

def create_new_events():
    """Create new event records based on enrichment log"""
    
    events = [
        {
            'record_id': 'EVT_011',
            'record_type': 'event',
            'category': 'infrastructure',
            'pillar': np.nan,  # Events don't have pillar assignment
            'indicator': 'EthSwitch Establishment',
            'indicator_code': np.nan,
            'indicator_direction': np.nan,
            'value_numeric': np.nan,
            'value_text': np.nan,
            'value_type': np.nan,
            'unit': np.nan,
            'observation_date': pd.Timestamp('2019-01-01'),  # Using observation_date as event_date
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'EthSwitch Annual Report',
            'source_type': 'company_report',
            'source_url': 'https://www.ethswitch.com/',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': 'National payment switch operator EthSwitch established',
            'notes': 'Critical infrastructure development for digital payments'
        },
        {
            'record_id': 'EVT_012',
            'record_type': 'event',
            'category': 'policy',
            'pillar': np.nan,
            'indicator': 'NFIS-I Launch',
            'indicator_code': np.nan,
            'indicator_direction': np.nan,
            'value_numeric': np.nan,
            'value_text': np.nan,
            'value_type': np.nan,
            'unit': np.nan,
            'observation_date': pd.Timestamp('2018-06-01'),
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'National Bank of Ethiopia',
            'source_type': 'policy_document',
            'source_url': 'https://www.nbe.gov.et/',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': 'National Financial Inclusion Strategy I (2018-2022) launched',
            'notes': 'First comprehensive financial inclusion strategy'
        },
        {
            'record_id': 'EVT_013',
            'record_type': 'event',
            'category': 'milestone',
            'pillar': np.nan,
            'indicator': 'COVID-19 Digital Finance Acceleration',
            'indicator_code': np.nan,
            'indicator_direction': np.nan,
            'value_numeric': np.nan,
            'value_text': np.nan,
            'value_type': np.nan,
            'unit': np.nan,
            'observation_date': pd.Timestamp('2020-04-01'),
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'NBE COVID-19 Response Report',
            'source_type': 'regulatory_report',
            'source_url': 'https://www.nbe.gov.et/',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': 'COVID-19 pandemic accelerates digital finance adoption',
            'notes': 'Major external shock affecting financial inclusion patterns'
        },
        {
            'record_id': 'EVT_014',
            'record_type': 'event',
            'category': 'policy',
            'pillar': np.nan,
            'indicator': 'Banking Sector Liberalization',
            'indicator_code': np.nan,
            'indicator_direction': np.nan,
            'value_numeric': np.nan,
            'value_text': np.nan,
            'value_type': np.nan,
            'unit': np.nan,
            'observation_date': pd.Timestamp('2016-09-01'),
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'National Bank of Ethiopia',
            'source_type': 'policy_document',
            'source_url': 'https://www.nbe.gov.et/',
            'confidence': 'high',
            'related_indicator': np.nan,
            'relationship_type': np.nan,
            'impact_direction': np.nan,
            'impact_magnitude': np.nan,
            'impact_estimate': np.nan,
            'lag_months': np.nan,
            'evidence_basis': np.nan,
            'comparable_country': np.nan,
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': 'Banking sector liberalization policy implemented',
            'notes': 'Policy change affecting financial sector competition'
        }
    ]
    
    return events

def create_new_impact_links():
    """Create new impact link records based on enrichment log"""
    
    impact_links = [
        {
            'record_id': 'IMP_0015',
            'parent_id': 'EVT_013',  # COVID-19 Digital Finance Acceleration
            'record_type': 'impact_link',
            'category': np.nan,
            'pillar': 'USAGE',
            'indicator': np.nan,
            'indicator_code': np.nan,
            'indicator_direction': np.nan,
            'value_numeric': np.nan,
            'value_text': np.nan,
            'value_type': np.nan,
            'unit': np.nan,
            'observation_date': np.nan,
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'Global Findex COVID-19 Impact Studies',
            'source_type': 'research_study',
            'source_url': 'https://globalfindex.worldbank.org/',
            'confidence': 'high',
            'related_indicator': 'USG_P2P_COUNT',
            'relationship_type': 'causal',
            'impact_direction': 'increase',
            'impact_magnitude': 'high',
            'impact_estimate': np.nan,
            'lag_months': 6,
            'evidence_basis': 'comparable_country_analysis',
            'comparable_country': 'Kenya, Nigeria',
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': 'COVID-19 accelerated digital payment adoption globally',
            'notes': 'COVID-19 impact on P2P transaction growth'
        },
        {
            'record_id': 'IMP_0016',
            'parent_id': 'EVT_011',  # EthSwitch Establishment
            'record_type': 'impact_link',
            'category': np.nan,
            'pillar': 'ACCESS',
            'indicator': np.nan,
            'indicator_code': np.nan,
            'indicator_direction': np.nan,
            'value_numeric': np.nan,
            'value_text': np.nan,
            'value_type': np.nan,
            'unit': np.nan,
            'observation_date': np.nan,
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'Payment Switch Infrastructure Studies',
            'source_type': 'research_study',
            'source_url': 'https://www.bis.org/',
            'confidence': 'medium',
            'related_indicator': 'ACC_MM_ACCOUNT',
            'relationship_type': 'enabling',
            'impact_direction': 'increase',
            'impact_magnitude': 'medium',
            'impact_estimate': np.nan,
            'lag_months': 12,
            'evidence_basis': 'comparable_country_analysis',
            'comparable_country': 'Rwanda',
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': 'National payment infrastructure enables mobile money growth',
            'notes': 'EthSwitch impact on mobile money account adoption'
        },
        {
            'record_id': 'IMP_0017',
            'parent_id': 'EVT_012',  # NFIS-I Launch
            'record_type': 'impact_link',
            'category': np.nan,
            'pillar': 'ACCESS',
            'indicator': np.nan,
            'indicator_code': np.nan,
            'indicator_direction': np.nan,
            'value_numeric': np.nan,
            'value_text': np.nan,
            'value_type': np.nan,
            'unit': np.nan,
            'observation_date': np.nan,
            'period_start': np.nan,
            'period_end': np.nan,
            'fiscal_year': np.nan,
            'gender': np.nan,
            'location': np.nan,
            'region': np.nan,
            'source_name': 'Financial Inclusion Strategy Impact Assessments',
            'source_type': 'policy_analysis',
            'source_url': 'https://www.worldbank.org/',
            'confidence': 'medium',
            'related_indicator': 'ACC_OWNERSHIP',
            'relationship_type': 'policy_effect',
            'impact_direction': 'increase',
            'impact_magnitude': 'medium',
            'impact_estimate': np.nan,
            'lag_months': 24,
            'evidence_basis': 'comparable_country_analysis',
            'comparable_country': 'Tanzania',
            'collected_by': 'Data Science Team',
            'collection_date': pd.Timestamp('2025-01-28'),
            'original_text': 'National strategies show 2-3 year implementation lag',
            'notes': 'NFIS-I impact on account ownership growth'
        }
    ]
    
    return impact_links

def main():
    """Main function to enrich the dataset"""
    
    print("=== DATA ENRICHMENT PROCESS ===\n")
    
    # Load existing data
    df_main = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx', sheet_name='ethiopia_fi_unified_data')
    df_impact = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx', sheet_name='Impact_sheet')
    
    print(f"Original main dataset: {len(df_main)} records")
    print(f"Original impact links: {len(df_impact)} records")
    
    # Create new records
    new_observations = create_new_observations()
    new_events = create_new_events()
    new_impact_links = create_new_impact_links()
    
    print(f"\nAdding {len(new_observations)} new observations")
    print(f"Adding {len(new_events)} new events")
    print(f"Adding {len(new_impact_links)} new impact links")
    
    # Convert to DataFrames
    df_new_obs = pd.DataFrame(new_observations)
    df_new_events = pd.DataFrame(new_events)
    df_new_impact = pd.DataFrame(new_impact_links)
    
    # Combine with existing data
    df_main_enriched = pd.concat([df_main, df_new_obs, df_new_events], ignore_index=True)
    df_impact_enriched = pd.concat([df_impact, df_new_impact], ignore_index=True)
    
    print(f"\nEnriched main dataset: {len(df_main_enriched)} records")
    print(f"Enriched impact links: {len(df_impact_enriched)} records")
    
    # Save enriched datasets
    df_main_enriched.to_excel('data/processed/ethiopia_fi_unified_data_enriched.xlsx', index=False)
    df_impact_enriched.to_excel('data/processed/impact_links_enriched.xlsx', index=False)
    
    print(f"\n✅ Enriched datasets saved to data/processed/")
    
    # Summary of additions
    print(f"\n=== ENRICHMENT SUMMARY ===")
    print(f"New indicators added:")
    print(f"  - ACC_INTERNET_PEN: Internet Access Penetration")
    print(f"  - AFF_GDP_PCAP: GDP per Capita")
    print(f"  - AFF_URBAN_RATE: Urbanization Rate")
    
    print(f"\nNew events added:")
    print(f"  - EthSwitch Establishment (2019)")
    print(f"  - NFIS-I Launch (2018)")
    print(f"  - COVID-19 Digital Finance Acceleration (2020)")
    print(f"  - Banking Sector Liberalization (2016)")
    
    print(f"\nNew impact links added:")
    print(f"  - COVID-19 impact on P2P transactions")
    print(f"  - EthSwitch impact on mobile money accounts")
    print(f"  - NFIS-I impact on account ownership")
    
    print(f"\n✅ Data enrichment completed successfully!")
    
    return True

if __name__ == "__main__":
    main()
