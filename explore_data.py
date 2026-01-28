#!/usr/bin/env python3
"""
Data Exploration Script for Ethiopia Financial Inclusion Dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime

def main():
    print("=== ETHIOPIA FINANCIAL INCLUSION DATA EXPLORATION ===\n")
    
    # Load the main dataset
    file_path = 'data/raw/ethiopia_fi_unified_data.xlsx'
    
    try:
        # Check available sheets
        excel_file = pd.ExcelFile(file_path)
        print(f"Available sheets: {excel_file.sheet_names}")
        
        # Load the main data sheet
        df_main = pd.read_excel(file_path, sheet_name='ethiopia_fi_unified_data')
        print(f"\nMain dataset shape: {df_main.shape}")
        
        # Show column structure
        print(f"\nColumns ({len(df_main.columns)}):")
        for i, col in enumerate(df_main.columns):
            print(f"{i+1:2d}. {col}")
        
        # Record type distribution
        print(f"\nRecord type distribution:")
        record_counts = df_main['record_type'].value_counts()
        for record_type, count in record_counts.items():
            print(f"  {record_type}: {count} ({count/len(df_main)*100:.1f}%)")
        
        # Show sample of each record type
        print(f"\n=== SAMPLE DATA ===")
        
        # Observations
        observations = df_main[df_main['record_type'] == 'observation']
        print(f"\nObservations sample ({len(observations)} records):")
        if len(observations) > 0:
            cols_to_show = ['indicator_code', 'indicator', 'value_numeric', 'observation_date', 'source_name']
            available_cols = [col for col in cols_to_show if col in observations.columns]
            print(observations[available_cols].head())
        
        # Events
        events = df_main[df_main['record_type'] == 'event']
        print(f"\nEvents sample ({len(events)} records):")
        if len(events) > 0:
            cols_to_show = ['event_date', 'category', 'description', 'source_name']
            available_cols = [col for col in cols_to_show if col in events.columns]
            print(events[available_cols].head())
        
        # Targets
        targets = df_main[df_main['record_type'] == 'target']
        print(f"\nTargets sample ({len(targets)} records):")
        if len(targets) > 0:
            cols_to_show = ['indicator_code', 'indicator', 'value_numeric', 'target_date']
            available_cols = [col for col in cols_to_show if col in targets.columns]
            print(targets[available_cols].head())
        
        # Load impact links
        if 'Impact_sheet' in excel_file.sheet_names:
            df_impact = pd.read_excel(file_path, sheet_name='Impact_sheet')
            print(f"\nImpact links dataset shape: {df_impact.shape}")
            print(f"Impact links columns: {list(df_impact.columns)}")
            print(f"Impact links sample:")
            print(df_impact.head())
        
        # Load reference codes
        ref_codes = pd.read_excel('data/raw/reference_codes.xlsx')
        print(f"\nReference codes shape: {ref_codes.shape}")
        print(f"Reference codes columns: {list(ref_codes.columns)}")
        print(f"Reference codes sample:")
        print(ref_codes.head(10))
        
        print(f"\n=== EXPLORATION COMPLETE ===")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
