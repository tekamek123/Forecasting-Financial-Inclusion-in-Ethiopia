#!/usr/bin/env python3
"""
Detailed Analysis of Ethiopia Financial Inclusion Dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime

def main():
    print("=== DETAILED DATA ANALYSIS ===\n")
    
    # Load datasets
    df_main = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx', sheet_name='ethiopia_fi_unified_data')
    df_impact = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx', sheet_name='Impact_sheet')
    ref_codes = pd.read_excel('data/raw/reference_codes.xlsx')
    
    print("1. TEMPORAL ANALYSIS")
    print("=" * 50)
    
    # Convert date columns
    df_main['observation_date'] = pd.to_datetime(df_main['observation_date'], errors='coerce')
    
    # Temporal range of observations
    observations = df_main[df_main['record_type'] == 'observation']
    obs_dates = observations['observation_date'].dropna()
    
    if len(obs_dates) > 0:
        print(f"Observation date range: {obs_dates.min().date()} to {obs_dates.max().date()}")
        print(f"Observation span: {(obs_dates.max() - obs_dates.min()).days / 365.25:.1f} years")
        
        # Observations by year
        obs_by_year = obs_dates.dt.year.value_counts().sort_index()
        print(f"\nObservations by year:")
        for year, count in obs_by_year.items():
            print(f"  {year}: {count} observations")
    
    print(f"\n2. INDICATOR ANALYSIS")
    print("=" * 50)
    
    # Unique indicators
    indicators = observations['indicator_code'].value_counts()
    print(f"Total unique indicators: {len(indicators)}")
    print(f"\nIndicator coverage:")
    for indicator, count in indicators.items():
        indicator_name = observations[observations['indicator_code'] == indicator]['indicator'].iloc[0]
        print(f"  {indicator}: {count} observations - {indicator_name}")
    
    # Pillar distribution
    pillar_counts = observations['pillar'].value_counts()
    print(f"\nPillar distribution in observations:")
    for pillar, count in pillar_counts.items():
        print(f"  {pillar}: {count} observations")
    
    print(f"\n3. EVENT ANALYSIS")
    print("=" * 50)
    
    events = df_main[df_main['record_type'] == 'event']
    print(f"Total events: {len(events)}")
    
    # Event categories
    event_categories = events['category'].value_counts()
    print(f"\nEvent categories:")
    for category, count in event_categories.items():
        print(f"  {category}: {count} events")
    
    # Events with dates
    events['event_date'] = pd.to_datetime(events['observation_date'], errors='coerce')  # Using observation_date as event_date
    event_dates = events['event_date'].dropna()
    
    if len(event_dates) > 0:
        print(f"\nEvent date range: {event_dates.min().date()} to {event_dates.max().date()}")
        
        # Events by year
        events_by_year = event_dates.dt.year.value_counts().sort_index()
        print(f"Events by year:")
        for year, count in events_by_year.items():
            print(f"  {year}: {count} events")
    
    # Show event details
    print(f"\nEvent details:")
    for _, event in events.iterrows():
        print(f"  {event.get('category', 'Unknown')}: {event.get('indicator', 'No description')}")
        if pd.notna(event.get('observation_date')):
            print(f"    Date: {event['observation_date'].date()}")
        if pd.notna(event.get('source_name')):
            print(f"    Source: {event['source_name']}")
        print()
    
    print(f"4. TARGET ANALYSIS")
    print("=" * 50)
    
    targets = df_main[df_main['record_type'] == 'target']
    print(f"Total targets: {len(targets)}")
    
    for _, target in targets.iterrows():
        print(f"  {target['indicator_code']}: {target['value_numeric']}")
        print(f"    {target['indicator']}")
        print(f"    Target date: {target.get('observation_date', 'Not specified')}")
        print()
    
    print(f"5. IMPACT LINKS ANALYSIS")
    print("=" * 50)
    
    print(f"Total impact links: {len(df_impact)}")
    
    # Impact directions
    impact_directions = df_impact['impact_direction'].value_counts()
    print(f"\nImpact directions:")
    for direction, count in impact_directions.items():
        print(f"  {direction}: {count} links")
    
    # Pillars in impact links
    impact_pillars = df_impact['pillar'].value_counts()
    print(f"\nPillars in impact links:")
    for pillar, count in impact_pillars.items():
        print(f"  {pillar}: {count} links")
    
    # Impact magnitude summary
    if 'impact_magnitude' in df_impact.columns:
        print(f"\nImpact magnitude summary:")
        mag_stats = df_impact['impact_magnitude'].describe()
        for stat, value in mag_stats.items():
            print(f"  {stat}: {value}")
    
    print(f"\n6. DATA QUALITY ASSESSMENT")
    print("=" * 50)
    
    # Missing values analysis
    print("Missing values in main dataset:")
    missing_data = df_main.isnull().sum()
    missing_percentage = (missing_data / len(df_main)) * 100
    
    for col, missing_count in missing_data.items():
        if missing_count > 0:
            print(f"  {col}: {missing_count} ({missing_percentage[col]:.1f}%)")
    
    # Confidence levels
    confidence_dist = df_main['confidence'].value_counts()
    print(f"\nConfidence level distribution:")
    for conf, count in confidence_dist.items():
        print(f"  {conf}: {count} records")
    
    print(f"\n7. REFERENCE CODES SUMMARY")
    print("=" * 50)
    
    ref_fields = ref_codes['field'].value_counts()
    print("Reference code fields:")
    for field, count in ref_fields.items():
        print(f"  {field}: {count} codes")
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Ready for data enrichment phase!")

if __name__ == "__main__":
    main()
