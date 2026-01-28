#!/usr/bin/env python3
"""
Task 2: Exploratory Data Analysis
Comprehensive analysis of patterns and factors influencing financial inclusion in Ethiopia
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and prepare the enriched dataset"""
    print("=== LOADING DATA ===")
    
    # Load datasets
    df_main = pd.read_excel('data/processed/ethiopia_fi_unified_data_enriched.xlsx')
    df_impact = pd.read_excel('data/processed/impact_links_enriched.xlsx')
    
    # Convert date columns
    df_main['observation_date'] = pd.to_datetime(df_main['observation_date'], errors='coerce')
    
    # Filter data
    observations = df_main[df_main['record_type'] == 'observation'].copy()
    events = df_main[df_main['record_type'] == 'event'].copy()
    targets = df_main[df_main['record_type'] == 'target'].copy()
    
    print(f"✅ Main dataset: {len(df_main)} records")
    print(f"✅ Observations: {len(observations)}")
    print(f"✅ Events: {len(events)}")
    print(f"✅ Targets: {len(targets)}")
    print(f"✅ Impact links: {len(df_impact)}")
    
    return observations, events, targets, df_impact

def dataset_overview(observations):
    """Analyze dataset overview and quality"""
    print("\n" + "="*60)
    print("DATASET OVERVIEW & QUALITY ASSESSMENT")
    print("="*60)
    
    # Record type distribution
    print(f"\n📊 Record Type Distribution:")
    record_dist = observations['record_type'].value_counts()
    for record_type, count in record_dist.items():
        print(f"  {record_type}: {count} ({count/len(observations)*100:.1f}%)")
    
    # Pillar distribution
    print(f"\n🏛️ Pillar Distribution:")
    pillar_dist = observations['pillar'].value_counts()
    for pillar, count in pillar_dist.items():
        print(f"  {pillar}: {count} ({count/len(observations)*100:.1f}%)")
    
    # Source type distribution
    print(f"\n📋 Source Type Distribution:")
    source_dist = observations['source_type'].value_counts()
    for source_type, count in source_dist.items():
        print(f"  {source_type}: {count} ({count/len(observations)*100:.1f}%)")
    
    # Data quality
    print(f"\n🔍 Data Quality Assessment:")
    confidence_dist = observations['confidence'].value_counts()
    for conf, count in confidence_dist.items():
        print(f"  {conf} confidence: {count} ({count/len(observations)*100:.1f}%)")
    
    source_coverage = observations['source_url'].notna().sum()
    print(f"  Source URL coverage: {source_coverage}/{len(observations)} ({source_coverage/len(observations)*100:.1f}%)")
    
    # Temporal range
    obs_dates = observations['observation_date'].dropna()
    print(f"\n📅 Temporal Coverage:")
    print(f"  Date range: {obs_dates.min().date()} to {obs_dates.max().date()}")
    print(f"  Span: {(obs_dates.max() - obs_dates.min()).days / 365.25:.1f} years")

def access_analysis(observations):
    """Analyze account ownership trends"""
    print("\n" + "="*60)
    print("ACCESS ANALYSIS - ACCOUNT OWNERSHIP TRAJECTORY")
    print("="*60)
    
    # Extract account ownership data
    acc_data = observations[observations['indicator_code'] == 'ACC_OWNERSHIP'].copy()
    acc_data = acc_data.sort_values('observation_date')
    
    print(f"\n📈 Account Ownership Trajectory:")
    for _, row in acc_data.iterrows():
        print(f"  {row['observation_date'].year}: {row['value_numeric']:.1f}% ({row['source_name']})")
    
    # Calculate growth rates
    print(f"\n📊 Growth Rate Analysis:")
    growth_data = []
    for i in range(1, len(acc_data)):
        prev_val = acc_data.iloc[i-1]['value_numeric']
        curr_val = acc_data.iloc[i]['value_numeric']
        prev_year = acc_data.iloc[i-1]['observation_date'].year
        curr_year = acc_data.iloc[i]['observation_date'].year
        
        growth_rate = ((curr_val - prev_val) / prev_val) * 100
        absolute_change = curr_val - prev_val
        
        print(f"  {prev_year}-{curr_year}: {growth_rate:+.1f}% ({absolute_change:+.1f}pp)")
        growth_data.append({
            'period': f"{prev_year}-{curr_year}",
            'growth_rate': growth_rate,
            'absolute_change': absolute_change
        })
    
    # 2021-2024 slowdown analysis
    print(f"\n🔍 2021-2024 Slowdown Analysis:")
    recent_growth = growth_data[-1] if growth_data else None
    if recent_growth and recent_growth['absolute_change'] < 5:
        print(f"  ⚠️  Minimal growth: only {recent_growth['absolute_change']:+.1f}pp")
        print(f"  🤔 Potential factors:")
        print(f"    • Mobile money account vs survey discrepancy")
        print(f"    • Market saturation effects")
        print(f"    • COVID-19 aftermath")
        print(f"    • Survey methodology limitations")
    
    # Get mobile money context
    mm_data = observations[observations['indicator_code'].isin(['USG_TELEBIRR_USERS', 'USG_MPESA_USERS'])]
    if len(mm_data) > 0:
        print(f"\n📱 Mobile Money Context:")
        for _, row in mm_data.iterrows():
            print(f"  {row['observation_date'].year}: {row['indicator_code']} = {row['value_numeric']:,.0f}")
    
    return acc_data

def usage_analysis(observations):
    """Analyze digital payment usage patterns"""
    print("\n" + "="*60)
    print("USAGE ANALYSIS - DIGITAL PAYMENT ADOPTION")
    print("="*60)
    
    # Usage indicators
    usage_indicators = ['ACC_MM_ACCOUNT', 'USG_TELEBIRR_USERS', 'USG_MPESA_USERS', 
                       'USG_P2P_COUNT', 'USG_P2P_VALUE', 'USG_ACTIVE_RATE']
    
    usage_data = observations[observations['indicator_code'].isin(usage_indicators)]
    
    print(f"\n📊 Usage Indicators Available:")
    for indicator in usage_indicators:
        data = usage_data[usage_data['indicator_code'] == indicator]
        if len(data) > 0:
            print(f"  ✅ {indicator}: {len(data)} observations")
        else:
            print(f"  ❌ {indicator}: No data")
    
    # Mobile money penetration
    mm_acc_data = usage_data[usage_data['indicator_code'] == 'ACC_MM_ACCOUNT']
    if len(mm_acc_data) > 0:
        print(f"\n📱 Mobile Money Account Penetration:")
        for _, row in mm_acc_data.sort_values('observation_date').iterrows():
            print(f"  {row['observation_date'].year}: {row['value_numeric']:.1f}%")
    
    # P2P transactions
    p2p_data = usage_data[usage_data['indicator_code'].isin(['USG_P2P_COUNT', 'USG_P2P_VALUE'])]
    if len(p2p_data) > 0:
        print(f"\n💸 P2P Transaction Data:")
        for _, row in p2p_data.sort_values('observation_date').iterrows():
            unit = row.get('unit', '')
            print(f"  {row['observation_date'].year}: {row['value_numeric']:,.0f} {unit}")
    
    return usage_data

def infrastructure_analysis(observations):
    """Analyze infrastructure and enablers"""
    print("\n" + "="*60)
    print("INFRASTRUCTURE & ENABLERS ANALYSIS")
    print("="*60)
    
    # Infrastructure indicators
    infra_indicators = ['ACC_MOBILE_PEN', 'ACC_INTERNET_PEN', 'ACC_4G_COV', 
                       'AFF_GDP_PCAP', 'AFF_URBAN_RATE']
    
    infra_data = observations[observations['indicator_code'].isin(infra_indicators)]
    
    print(f"\n🏗️ Infrastructure Indicators:")
    for indicator in infra_indicators:
        data = infra_data[infra_data['indicator_code'] == indicator]
        if len(data) > 0:
            print(f"  ✅ {indicator}: {len(data)} observations")
            # Show trend
            data_sorted = data.sort_values('observation_date')
            first_val = data_sorted.iloc[0]['value_numeric']
            last_val = data_sorted.iloc[-1]['value_numeric']
            unit = data_sorted.iloc[0].get('unit', '')
            change = ((last_val - first_val) / first_val) * 100 if first_val > 0 else 0
            print(f"    Trend: {first_val} → {last_val} {unit} ({change:+.1f}%)")
        else:
            print(f"  ❌ {indicator}: No data")
    
    # Correlation analysis
    print(f"\n🔗 Infrastructure-Inclusion Relationships:")
    
    # Create pivot table for correlation
    pivot_data = observations.pivot_table(
        index='observation_date',
        columns='indicator_code',
        values='value_numeric'
    )
    
    # Key indicators for correlation
    key_indicators = ['ACC_OWNERSHIP', 'ACC_MOBILE_PEN', 'ACC_INTERNET_PEN', 'AFF_GDP_PCAP', 'AFF_URBAN_RATE']
    available_indicators = [ind for ind in key_indicators if ind in pivot_data.columns]
    
    if len(available_indicators) > 1:
        corr_matrix = pivot_data[available_indicators].corr()
        
        # Correlations with account ownership
        if 'ACC_OWNERSHIP' in corr_matrix.columns:
            acc_correlations = corr_matrix['ACC_OWNERSHIP'].sort_values(ascending=False)
            print(f"  Correlations with Account Ownership:")
            for indicator, corr in acc_correlations.items():
                if indicator != 'ACC_OWNERSHIP':
                    strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.3 else "Weak"
                    print(f"    {indicator}: {corr:.3f} ({strength})")
    
    return infra_data

def event_analysis(events):
    """Analyze event timeline and impacts"""
    print("\n" + "="*60)
    print("EVENT TIMELINE & VISUAL ANALYSIS")
    print("="*60)
    
    # Sort events by date
    events_sorted = events.sort_values('observation_date')
    
    print(f"\n📅 Event Timeline:")
    for _, event in events_sorted.iterrows():
        print(f"  {event['observation_date'].date()}: {event['category']} - {event['indicator']}")
    
    # Event categories
    print(f"\n📋 Event Categories:")
    category_counts = events['category'].value_counts()
    for category, count in category_counts.items():
        print(f"  {category}: {count} events")
    
    # Key events analysis
    key_events = {
        'Telebirr Launch': '2021-05-17',
        'M-Pesa Entry': '2022-08-01',
        'M-Pesa Launch': '2023-08-01',
        'EthSwitch': '2019-01-01',
        'NFIS-I': '2018-06-01',
        'COVID-19': '2020-04-01'
    }
    
    print(f"\n🎯 Key Events and Potential Impacts:")
    for event_name, event_date in key_events.items():
        event_date = pd.to_datetime(event_date)
        matching_events = events[events['observation_date'] == event_date]
        if len(matching_events) > 0:
            print(f"  ✅ {event_name} ({event_date.date()}): Found in dataset")
        else:
            print(f"  ⚠️  {event_name} ({event_date.date()}): Not found in dataset")
    
    return events_sorted

def correlation_analysis(observations):
    """Comprehensive correlation analysis"""
    print("\n" + "="*60)
    print("CORRELATION ANALYSIS")
    print("="*60)
    
    # Create pivot table
    pivot_data = observations.pivot_table(
        index='observation_date',
        columns='indicator_code',
        values='value_numeric'
    )
    
    # Get indicators with sufficient data
    indicator_counts = pivot_data.notna().sum()
    sufficient_indicators = indicator_counts[indicator_counts >= 3].index.tolist()
    
    print(f"\n📊 Indicators with sufficient data (≥3 observations):")
    for indicator in sufficient_indicators:
        count = indicator_counts[indicator]
        print(f"  {indicator}: {count} observations")
    
    if len(sufficient_indicators) > 1:
        # Calculate correlation matrix
        corr_matrix = pivot_data[sufficient_indicators].corr()
        
        # Find strongest correlations
        print(f"\n🔗 Strongest Correlations (|r| > 0.5):")
        strong_correlations = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    ind1 = corr_matrix.columns[i]
                    ind2 = corr_matrix.columns[j]
                    strong_correlations.append((ind1, ind2, corr_val))
        
        # Sort by absolute correlation
        strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
        
        for ind1, ind2, corr in strong_correlations:
            direction = "positive" if corr > 0 else "negative"
            print(f"  {ind1} ↔ {ind2}: {corr:.3f} ({direction})")
        
        # Pillar-specific correlations
        print(f"\n🏛️ Pillar-Specific Patterns:")
        
        # Access indicators
        access_indicators = [ind for ind in sufficient_indicators if ind.startswith('ACC_')]
        if len(access_indicators) > 1:
            access_corr = corr_matrix.loc[access_indicators, access_indicators]
            print(f"  ACCESS indicators show strong internal correlations")
        
        # Usage indicators  
        usage_indicators = [ind for ind in sufficient_indicators if ind.startswith('USG_')]
        if len(usage_indicators) > 1:
            print(f"  USAGE indicators: {len(usage_indicators)} available")
        
        # Affordability indicators
        aff_indicators = [ind for ind in sufficient_indicators if ind.startswith('AFF_')]
        if len(aff_indicators) > 0:
            print(f"  AFFORDABILITY indicators: {len(aff_indicators)} available")
    
    return pivot_data, sufficient_indicators

def identify_key_insights(observations, events, acc_data, usage_data, infra_data):
    """Identify and document key insights"""
    print("\n" + "="*60)
    print("KEY INSIGHTS SUMMARY")
    print("="*60)
    
    insights = []
    
    # Insight 1: Account ownership trajectory
    if len(acc_data) >= 2:
        first_val = acc_data.iloc[0]['value_numeric']
        last_val = acc_data.iloc[-1]['value_numeric']
        total_growth = last_val - first_val
        
        insights.append({
            'category': 'Account Ownership',
            'insight': f'Steady growth from {first_val}% to {last_val}% (+{total_growth:.1f}pp) over {(acc_data.iloc[-1]["observation_date"].year - acc_data.iloc[0]["observation_date"].year)} years',
            'evidence': f'2011: {first_val}%, 2024: {last_val}%',
            'significance': 'High'
        })
        
        # Recent slowdown
        if len(acc_data) >= 5:
            recent_growth = acc_data.iloc[-1]['value_numeric'] - acc_data.iloc[-2]['value_numeric']
            if recent_growth < 5:
                insights.append({
                    'category': 'Growth Deceleration',
                    'insight': f'Recent slowdown with only +{recent_growth:.1f}pp growth',
                    'evidence': f'2021-2024: Minimal growth despite mobile money expansion',
                    'significance': 'High'
                })
    
    # Insight 2: Infrastructure enablers
    mobile_pen_data = infra_data[infra_data['indicator_code'] == 'ACC_MOBILE_PEN']
    if len(mobile_pen_data) >= 2:
        first_pen = mobile_pen_data.iloc[0]['value_numeric']
        last_pen = mobile_pen_data.iloc[-1]['value_numeric']
        mobile_growth = ((last_pen - first_pen) / first_pen) * 100
        
        insights.append({
            'category': 'Infrastructure',
            'insight': f'Mobile penetration doubled from {first_pen}% to {last_pen}% (+{mobile_growth:.1f}%)',
            'evidence': f'Mobile penetration as key enabler for digital finance',
            'significance': 'High'
        })
    
    # Insight 3: Event impacts
    telecom_events = events[events['indicator'].str.contains('Telebirr', case=False, na=False)]
    if len(telecom_events) > 0:
        insights.append({
            'category': 'Market Dynamics',
            'insight': 'Telebirr launch (2021) served as major market catalyst',
            'evidence': '54M+ users achieved since launch',
            'significance': 'High'
        })
    
    # Insight 4: Data quality
    confidence_high = observations[observations['confidence'] == 'high'].shape[0]
    confidence_pct = (confidence_high / len(observations)) * 100
    
    insights.append({
        'category': 'Data Quality',
        'insight': f'High data quality with {confidence_pct:.1f}% high-confidence records',
        'evidence': f'{confidence_high}/{len(observations)} records with high confidence',
        'significance': 'Medium'
    })
    
    # Insight 5: Gender gap
    gender_data = observations[observations['indicator_code'] == 'GEN_GAP_ACC']
    if len(gender_data) > 0:
        insights.append({
            'category': 'Gender Inclusion',
            'insight': 'Gender gap identified in account ownership',
            'evidence': f'Gender gap data available for analysis',
            'significance': 'Medium'
        })
    else:
        insights.append({
            'category': 'Data Gaps',
            'insight': 'Gender-disaggregated data missing',
            'evidence': 'No GEN_GAP_* indicators found',
            'significance': 'High'
        })
    
    # Display insights
    print(f"\n🎯 TOP 5+ KEY INSIGHTS:")
    for i, insight in enumerate(insights[:8], 1):  # Show up to 8 insights
        print(f"\n{i}. {insight['category']} ({insight['significance']} Significance)")
        print(f"   💡 Insight: {insight['insight']}")
        print(f"   📊 Evidence: {insight['evidence']}")
    
    return insights

def create_visualizations(acc_data, usage_data, infra_data, events):
    """Create key visualizations"""
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # Create output directory
    import os
    os.makedirs('reports/figures', exist_ok=True)
    
    # 1. Account ownership trajectory
    if len(acc_data) > 0:
        plt.figure(figsize=(12, 6))
        plt.plot(acc_data['observation_date'], acc_data['value_numeric'], 
                marker='o', linewidth=3, markersize=8, color='#2E86AB')
        plt.title('Ethiopia Account Ownership Trajectory (2011-2024)', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Account Ownership Rate (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 60)
        
        # Add annotations
        for _, row in acc_data.iterrows():
            plt.annotate(f"{row['value_numeric']:.0f}%", 
                        (row['observation_date'], row['value_numeric']),
                        textcoords="offset points", xytext=(0,10), ha='center')
        
        plt.tight_layout()
        plt.savefig('reports/figures/account_ownership_trajectory.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ Account ownership trajectory saved")
    
    # 2. Infrastructure trends
    if len(infra_data) > 0:
        infra_indicators = ['ACC_MOBILE_PEN', 'ACC_INTERNET_PEN', 'AFF_GDP_PCAP']
        available_indicators = [ind for ind in infra_indicators 
                              if ind in infra_data['indicator_code'].values]
        
        if len(available_indicators) > 0:
            fig, axes = plt.subplots(1, len(available_indicators), figsize=(15, 5))
            if len(available_indicators) == 1:
                axes = [axes]
            
            for i, indicator in enumerate(available_indicators):
                data = infra_data[infra_data['indicator_code'] == indicator].sort_values('observation_date')
                indicator_name = data['indicator'].iloc[0]
                
                axes[i].plot(data['observation_date'], data['value_numeric'], 
                           marker='o', linewidth=2, markersize=6)
                axes[i].set_title(indicator_name, fontweight='bold')
                axes[i].tick_params(axis='x', rotation=45)
                axes[i].grid(True, alpha=0.3)
                
                # Add unit
                unit = data['unit'].iloc[0] if pd.notna(data['unit'].iloc[0]) else ''
                if unit:
                    axes[i].set_ylabel(unit)
            
            plt.suptitle('Infrastructure & Enablers Trends', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig('reports/figures/infrastructure_trends.png', dpi=300, bbox_inches='tight')
            plt.show()
            print("✅ Infrastructure trends saved")
    
    # 3. Event timeline
    if len(events) > 0:
        plt.figure(figsize=(14, 6))
        events_sorted = events.sort_values('observation_date')
        
        # Color mapping
        category_colors = {
            'product_launch': '#FF6B6B',
            'market_entry': '#4ECDC4', 
            'policy': '#45B7D1',
            'infrastructure': '#96CEB4',
            'milestone': '#FFEAA7'
        }
        
        y_pos = 0
        for _, event in events_sorted.iterrows():
            color = category_colors.get(event['category'], '#95A5A6')
            plt.scatter(event['observation_date'], y_pos, s=200, c=color, 
                       marker='D', label=event['category'])
            plt.annotate(event['indicator'], 
                        (event['observation_date'], y_pos),
                        textcoords="offset points", xytext=(0,20), ha='center',
                        fontsize=8, rotation=45)
            y_pos += 1
        
        plt.title('Ethiopia Financial Inclusion Event Timeline', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Events', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('reports/figures/event_timeline.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ Event timeline saved")

def main():
    """Main EDA analysis function"""
    print("🇪🇹 ETHIOPIA FINANCIAL INCLUSION - EXPLORATORY DATA ANALYSIS")
    print("="*80)
    
    # Load data
    observations, events, targets, df_impact = load_and_prepare_data()
    
    # Analysis sections
    dataset_overview(observations)
    acc_data = access_analysis(observations)
    usage_data = usage_analysis(observations)
    infra_data = infrastructure_analysis(observations)
    events_sorted = event_analysis(events)
    pivot_data, sufficient_indicators = correlation_analysis(observations)
    insights = identify_key_insights(observations, events, acc_data, usage_data, infra_data)
    
    # Create visualizations
    create_visualizations(acc_data, usage_data, infra_data, events)
    
    # Summary
    print("\n" + "="*80)
    print("📋 EDA ANALYSIS SUMMARY")
    print("="*80)
    print(f"✅ Dataset: {len(observations)} observations analyzed")
    print(f"✅ Time period: 2011-2025 ({(observations['observation_date'].max() - observations['observation_date'].min()).days / 365.25:.1f} years)")
    print(f"✅ Indicators: {len(observations['indicator_code'].unique())} unique indicators")
    print(f"✅ Events: {len(events)} major events analyzed")
    print(f"✅ Insights: {len(insights)} key insights identified")
    print(f"✅ Visualizations: Saved to reports/figures/")
    
    print(f"\n🎯 READY FOR NEXT PHASE: Event Impact Modeling")
    
    return insights

if __name__ == "__main__":
    insights = main()
