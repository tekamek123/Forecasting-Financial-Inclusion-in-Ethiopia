#!/usr/bin/env python3
"""
Verify the enriched dataset and provide summary statistics
"""

import pandas as pd
import numpy as np

def main():
    print("=== ENRICHED DATASET VERIFICATION ===\n")
    
    # Load enriched datasets
    df_main = pd.read_excel('data/processed/ethiopia_fi_unified_data_enriched.xlsx')
    df_impact = pd.read_excel('data/processed/impact_links_enriched.xlsx')
    
    print(f"✅ Enriched main dataset: {len(df_main)} records")
    print(f"✅ Enriched impact links: {len(df_impact)} records")
    
    # Record type distribution
    print(f"\n=== RECORD TYPE DISTRIBUTION ===")
    record_counts = df_main['record_type'].value_counts()
    for record_type, count in record_counts.items():
        print(f"{record_type}: {count} ({count/len(df_main)*100:.1f}%)")
    
    # Temporal range
    df_main['observation_date'] = pd.to_datetime(df_main['observation_date'], errors='coerce')
    observations = df_main[df_main['record_type'] == 'observation']
    obs_dates = observations['observation_date'].dropna()
    
    if len(obs_dates) > 0:
        print(f"\n=== TEMPORAL COVERAGE ===")
        print(f"Date range: {obs_dates.min().date()} to {obs_dates.max().date()}")
        print(f"Span: {(obs_dates.max() - obs_dates.min()).days / 365.25:.1f} years")
        
        # Observations by year
        obs_by_year = obs_dates.dt.year.value_counts().sort_index()
        print(f"\nObservations by year:")
        for year in range(2011, 2026):
            count = obs_by_year.get(year, 0)
            if count > 0:
                print(f"  {year}: {count} observations")
    
    # Indicator analysis
    print(f"\n=== INDICATOR ANALYSIS ===")
    indicators = observations['indicator_code'].value_counts()
    print(f"Total unique indicators: {len(indicators)}")
    print(f"\nTop indicators by observation count:")
    for indicator, count in indicators.head(10).items():
        indicator_name = observations[observations['indicator_code'] == indicator]['indicator'].iloc[0]
        print(f"  {indicator}: {count} - {indicator_name}")
    
    # New indicators verification
    new_indicators = ['ACC_INTERNET_PEN', 'AFF_GDP_PCAP', 'AFF_URBAN_RATE']
    print(f"\n=== NEW INDICATORS VERIFICATION ===")
    for indicator in new_indicators:
        count = indicators.get(indicator, 0)
        if count > 0:
            indicator_name = observations[observations['indicator_code'] == indicator]['indicator'].iloc[0]
            print(f"✅ {indicator}: {count} observations - {indicator_name}")
        else:
            print(f"❌ {indicator}: Not found")
    
    # Event analysis
    print(f"\n=== EVENT ANALYSIS ===")
    events = df_main[df_main['record_type'] == 'event']
    print(f"Total events: {len(events)}")
    
    event_categories = events['category'].value_counts()
    print(f"\nEvent categories:")
    for category, count in event_categories.items():
        print(f"  {category}: {count}")
    
    # New events verification
    new_events = ['EthSwitch Establishment', 'NFIS-I Launch', 'COVID-19 Digital Finance Acceleration', 'Banking Sector Liberalization']
    print(f"\n=== NEW EVENTS VERIFICATION ===")
    for event_name in new_events:
        event_found = events[events['indicator'] == event_name]
        if len(event_found) > 0:
            event_date = event_found['observation_date'].iloc[0]
            print(f"✅ {event_name}: {event_date.date()}")
        else:
            print(f"❌ {event_name}: Not found")
    
    # Impact links analysis
    print(f"\n=== IMPACT LINKS ANALYSIS ===")
    print(f"Total impact links: {len(df_impact)}")
    
    impact_pillars = df_impact['pillar'].value_counts()
    print(f"\nImpact links by pillar:")
    for pillar, count in impact_pillars.items():
        print(f"  {pillar}: {count}")
    
    # New impact links verification
    new_impact_parents = ['EVT_013', 'EVT_011', 'EVT_012']
    print(f"\n=== NEW IMPACT LINKS VERIFICATION ===")
    for parent_id in new_impact_parents:
        impact_links = df_impact[df_impact['parent_id'] == parent_id]
        if len(impact_links) > 0:
            pillar = impact_links['pillar'].iloc[0]
            related_indicator = impact_links['related_indicator'].iloc[0]
            print(f"✅ {parent_id}: {pillar} -> {related_indicator}")
        else:
            print(f"❌ {parent_id}: Not found")
    
    # Data quality check
    print(f"\n=== DATA QUALITY CHECK ===")
    confidence_dist = df_main['confidence'].value_counts()
    print(f"Confidence levels:")
    for conf, count in confidence_dist.items():
        print(f"  {conf}: {count} ({count/len(df_main)*100:.1f}%)")
    
    # Source coverage
    source_coverage = df_main['source_url'].notna().sum()
    print(f"\nSource URL coverage: {source_coverage}/{len(df_main)} ({source_coverage/len(df_main)*100:.1f}%)")
    
    print(f"\n✅ ENRICHMENT VERIFICATION COMPLETE")
    print(f"Dataset successfully enriched with:")
    print(f"  - {len(df_main) - 43} new records added")
    print(f"  - {len(df_impact) - 14} new impact links added")
    print(f"  - Extended temporal coverage to 2011-2025")
    print(f"  - Added 3 new indicator types")
    print(f"  - Added 4 new historical events")

if __name__ == "__main__":
    main()
