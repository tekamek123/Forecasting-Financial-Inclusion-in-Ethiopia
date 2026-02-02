#!/usr/bin/env python3
"""
Event Impact Modeling for Ethiopia Financial Inclusion Project
Task 3: Model how events affect financial inclusion indicators
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set styling
plt.style.use('seaborn-v0_8-whitegrid')
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83']

class EventImpactModel:
    """
    Comprehensive event impact modeling system for financial inclusion indicators
    """
    
    def __init__(self, impact_matrix, impact_events):
        """
        Initialize the event impact model
        
        Parameters:
        - impact_matrix: DataFrame of event-indicator impacts
        - impact_events: DataFrame of event details with timing
        """
        self.impact_matrix = impact_matrix
        self.impact_events = impact_events.sort_values('event_date')
        self.validation_results = {}
        
    def apply_event_effect(self, base_value, event_impact, months_since_event, effect_type='gradual'):
        """
        Apply event effect to base value over time
        
        Parameters:
        - base_value: Original indicator value
        - event_impact: Magnitude of impact (positive or negative)
        - months_since_event: Months since event occurred
        - effect_type: 'gradual', 'immediate', 'delayed'
        """
        if months_since_event < 0:
            return base_value
        
        if effect_type == 'immediate':
            return base_value * (1 + event_impact)
        
        elif effect_type == 'gradual':
            effect_duration = 12
            if months_since_event >= effect_duration:
                return base_value * (1 + event_impact)
            else:
                effect_fraction = months_since_event / effect_duration
                return base_value * (1 + event_impact * effect_fraction)
        
        elif effect_type == 'delayed':
            peak_month = 6
            if months_since_event <= peak_month:
                effect_fraction = months_since_event / peak_month
            else:
                decay_rate = 0.1
                effect_fraction = np.exp(-decay_rate * (months_since_event - peak_month))
            return base_value * (1 + event_impact * effect_fraction)
        
        return base_value
    
    def predict_indicator(self, indicator_code, base_values, dates, effect_type='gradual'):
        """
        Predict indicator values considering all event effects
        
        Parameters:
        - indicator_code: Target indicator (e.g., 'ACC_OWNERSHIP')
        - base_values: Base values without events
        - dates: Corresponding dates for predictions
        - effect_type: Type of effect function to use
        """
        predictions = []
        
        for date, base_val in zip(dates, base_values):
            current_value = base_val
            
            # Apply effects from all events that have occurred
            for _, event in self.impact_events.iterrows():
                if pd.notna(event['event_date']):
                    months_since = (date - event['event_date']).days / 30.44
                    
                    # Get impact magnitude for this indicator
                    if event['event_name'] in self.impact_matrix.index:
                        impact = self.impact_matrix.loc[event['event_name'], indicator_code]
                        
                        if impact != 0:
                            # Adjust for lag
                            lag_months = event['lag_months']
                            adjusted_months = months_since - lag_months
                            
                            # Apply effect
                            current_value = self.apply_event_effect(
                                current_value, impact, adjusted_months, effect_type
                            )
            
            predictions.append(current_value)
        
        return np.array(predictions)
    
    def validate_model(self, indicator_code, observations, effect_type='gradual'):
        """
        Validate model against historical data
        
        Parameters:
        - indicator_code: Target indicator to validate
        - observations: Historical observation data
        - effect_type: Type of effect function
        """
        print(f"🧪 VALIDATING MODEL FOR {indicator_code}")
        
        # Get historical data for this indicator
        indicator_data = observations[observations['indicator_code'] == indicator_code].sort_values('observation_date')
        
        if len(indicator_data) < 3:
            print(f"❌ Insufficient data for {indicator_code}")
            return None
        
        # Create baseline from early data (before major events)
        early_data = indicator_data[indicator_data['observation_date'].dt.year < 2016]
        
        if len(early_data) < 2:
            print(f"❌ Insufficient pre-2016 data for {indicator_code}")
            return None
        
        # Calculate baseline trend
        early_years = early_data['observation_date'].dt.year.values
        early_values = early_data['value_numeric'].values / 100  # Convert to decimal
        
        # Simple linear trend
        trend_slope = (early_values[-1] - early_values[0]) / (early_years[-1] - early_years[0])
        base_2015 = early_values[-1]
        
        print(f"   Pre-2016 trend: {trend_slope:.4f} per year")
        print(f"   2015 baseline: {base_2015:.3f} ({base_2015*100:.1f}%)")
        
        # Create prediction timeline
        prediction_years = np.arange(2015, 2026)
        prediction_dates = [pd.Timestamp(f'{year}-06-30') for year in prediction_years]
        
        # Create baseline values (continuing pre-2016 trend)
        base_values = [base_2015 + trend_slope * (year - 2015) for year in prediction_years]
        
        # Apply event effects
        predicted_values = self.predict_indicator(
            indicator_code, base_values, prediction_dates, effect_type
        )
        
        # Get actual values for comparison
        actual_values = []
        actual_years = []
        for year in prediction_years:
            year_data = indicator_data[indicator_data['observation_date'].dt.year == year]
            if len(year_data) > 0:
                actual_values.append(year_data.iloc[0]['value_numeric'] / 100)
                actual_years.append(year)
        
        # Calculate validation metrics
        if actual_values:
            # Align predicted and actual values
            aligned_pred = []
            aligned_actual = []
            
            for i, year in enumerate(prediction_years):
                if year in actual_years:
                    aligned_pred.append(predicted_values[i])
                    aligned_actual.append(actual_values[actual_years.index(year)])
            
            if aligned_pred:
                aligned_pred = np.array(aligned_pred)
                aligned_actual = np.array(aligned_actual)
                
                mae = np.mean(np.abs(aligned_pred - aligned_actual))
                mape = np.mean(np.abs((aligned_pred - aligned_actual) / aligned_actual)) * 100
                
                validation_result = {
                    'indicator': indicator_code,
                    'mae': mae,
                    'mape': mape,
                    'baseline_trend': trend_slope,
                    'base_2015': base_2015,
                    'prediction_years': prediction_years,
                    'prediction_dates': prediction_dates,
                    'base_values': base_values,
                    'predicted_values': predicted_values,
                    'actual_years': actual_years,
                    'actual_values': actual_values,
                    'aligned_pred': aligned_pred,
                    'aligned_actual': aligned_actual
                }
                
                self.validation_results[indicator_code] = validation_result
                
                print(f"   ✅ Validation complete - MAE: {mae:.4f}, MAPE: {mape:.2f}%")
                return validation_result
        
        print(f"❌ Validation failed for {indicator_code}")
        return None
    
    def plot_validation(self, indicator_code, save_path=None):
        """
        Plot validation results for an indicator
        """
        if indicator_code not in self.validation_results:
            print(f"❌ No validation results for {indicator_code}")
            return
        
        result = self.validation_results[indicator_code]
        
        plt.figure(figsize=(14, 7))
        
        # Plot baseline trend
        plt.plot(result['prediction_years'], np.array(result['base_values'])*100, 
                'g--', label='Baseline (No Events)', linewidth=2, alpha=0.7)
        
        # Plot predicted with events
        plt.plot(result['prediction_years'], result['predicted_values']*100, 
                'b-', label='Predicted (With Events)', linewidth=3, marker='o')
        
        # Plot actual values
        if result['actual_values']:
            plt.plot(result['actual_years'], np.array(result['actual_values'])*100, 
                    'r-', label='Actual', linewidth=3, marker='s', markersize=8)
        
        # Add event markers
        for _, event in self.impact_events.iterrows():
            if pd.notna(event['event_date']) and event['target_indicator'] == indicator_code:
                event_year = event['event_date'].year
                plt.axvline(x=event_year, color='orange', linestyle=':', alpha=0.7)
                plt.text(event_year, plt.ylim()[1]*0.9, event['event_name'][:15] + '...', 
                        rotation=90, fontsize=8, ha='right')
        
        plt.title(f'Model Validation: {indicator_code} (2015-2025)', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Value (%)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Plot saved to {save_path}")
        
        plt.show()
    
    def create_association_matrix_heatmap(self, save_path=None):
        """
        Create heatmap of event-indicator associations
        """
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.impact_matrix, 
                    annot=True, 
                    fmt='.2f',
                    cmap='RdBu_r', 
                    center=0,
                    cbar_kws={'label': 'Impact Magnitude'},
                    linewidths=0.5)
        
        plt.title('Event-Indicator Association Matrix\\n(Positive values = increase, Negative values = decrease)', 
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Financial Inclusion Indicators', fontsize=12)
        plt.ylabel('Events', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Heatmap saved to {save_path}")
        
        plt.show()
    
    def summarize_validation_results(self):
        """
        Summarize all validation results
        """
        if not self.validation_results:
            print("❌ No validation results available")
            return
        
        print("📊 VALIDATION SUMMARY:")
        print("   Indicator |    MAE |   MAPE | Trend/Year | Status")
        print("   ----------|--------|--------|------------|--------")
        
        for indicator, result in self.validation_results.items():
            mae = result['mae']
            mape = result['mape']
            trend = result['baseline_trend']
            
            # Status based on MAPE
            if mape < 5:
                status = "✅ Excellent"
            elif mape < 10:
                status = "🟡 Good"
            elif mape < 20:
                status = "🟠 Fair"
            else:
                status = "❌ Poor"
            
            print(f"   {indicator:10s} | {mae:6.4f} | {mape:6.2f}% | {trend:+10.4f} | {status}")
        
        # Overall assessment
        avg_mape = np.mean([r['mape'] for r in self.validation_results.values()])
        print(f"\\n🎯 OVERALL PERFORMANCE:")
        print(f"   Average MAPE: {avg_mape:.2f}%")
        
        if avg_mape < 5:
            print("   🏆 Model performance: Excellent")
        elif avg_mape < 10:
            print("   👍 Model performance: Good")
        elif avg_mape < 20:
            print("   ⚠️  Model performance: Fair")
        else:
            print("   ❌ Model performance: Poor - needs refinement")

def load_and_prepare_data():
    """
    Load and prepare data for event impact modeling
    """
    print("📊 LOADING DATA FOR EVENT IMPACT MODELING")
    
    # Load datasets
    df_main = pd.read_excel('data/processed/ethiopia_fi_unified_data_enriched.xlsx')
    df_impact = pd.read_excel('data/processed/impact_links_enriched.xlsx')
    
    # Prepare data
    df_main['observation_date'] = pd.to_datetime(df_main['observation_date'], errors='coerce')
    observations = df_main[df_main['record_type'] == 'observation']
    events = df_main[df_main['record_type'] == 'event']
    
    print(f"   Main records: {len(df_main)}")
    print(f"   Observations: {len(observations)}")
    print(f"   Events: {len(events)}")
    print(f"   Impact links: {len(df_impact)}")
    
    # Join impact links with event details
    event_lookup = events.set_index('record_id').to_dict('index')
    impact_with_events = []
    
    for _, link in df_impact.iterrows():
        event_details = event_lookup.get(link['parent_id'], {})
        impact_with_events.append({
            'event_name': event_details.get('indicator', 'Unknown Event'),
            'event_date': event_details.get('observation_date'),
            'event_category': event_details.get('category'),
            'target_indicator': link['indicator_code'],
            'direction': link['impact_direction'],
            'magnitude': link['impact_magnitude'],
            'lag_months': link['lag_months'],
            'confidence': link['confidence']
        })
    
    df_impact_events = pd.DataFrame(impact_with_events)
    df_impact_events['event_date'] = pd.to_datetime(df_impact_events['event_date'])
    
    print(f"   ✅ Impact-event relationships: {len(df_impact_events)}")
    
    return observations, df_impact_events

def create_event_indicator_matrix(df_impact_events):
    """
    Create event-indicator association matrix
    """
    print("🏗️ BUILDING EVENT-INDICATOR MATRIX")
    
    # Define key indicators
    key_indicators = [
        'ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'ACC_MOBILE_PEN', 'ACC_INTERNET_PEN',
        'USG_P2P_COUNT', 'USG_DIGITAL_PAYMENT', 'USG_ACTIVE_RATE',
        'AFF_GDP_PCAP', 'AFF_URBAN_RATE'
    ]
    
    # Create matrix
    event_names = df_impact_events['event_name'].unique()
    matrix_data = []
    
    for event in event_names:
        row = {'event_name': event}
        event_impacts = df_impact_events[df_impact_events['event_name'] == event]
        
        for indicator in key_indicators:
            impact = event_impacts[event_impacts['target_indicator'] == indicator]
            if len(impact) > 0:
                impact_row = impact.iloc[0]
                effect_value = impact_row['magnitude'] if impact_row['direction'] == 'increase' else -impact_row['magnitude']
                row[indicator] = effect_value
            else:
                row[indicator] = 0
        
        matrix_data.append(row)
    
    impact_matrix = pd.DataFrame(matrix_data).set_index('event_name')
    
    print(f"   Matrix shape: {impact_matrix.shape}")
    print(f"   Events: {len(event_names)}")
    print(f"   Indicators: {len(key_indicators)}")
    
    return impact_matrix

def main():
    """
    Main function to run event impact modeling
    """
    print("🇪🇹 ETHIOPIA FINANCIAL INCLUSION - EVENT IMPACT MODELING")
    print("=" * 60)
    
    # Load data
    observations, df_impact_events = load_and_prepare_data()
    
    # Create association matrix
    impact_matrix = create_event_indicator_matrix(df_impact_events)
    
    # Save matrix
    impact_matrix.to_csv('reports/event_indicator_matrix.csv')
    print("💾 Association matrix saved to reports/event_indicator_matrix.csv")
    
    # Initialize model
    impact_model = EventImpactModel(impact_matrix, df_impact_events)
    print(f"🤖 Event impact model initialized with {len(impact_model.impact_events)} events")
    
    # Create reports directory
    import os
    os.makedirs('reports/figures', exist_ok=True)
    
    # Create association matrix heatmap
    impact_model.create_association_matrix_heatmap('reports/figures/event_indicator_heatmap.png')
    
    # Validate model on key indicators
    key_indicators = ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'ACC_MOBILE_PEN', 'USG_P2P_COUNT']
    
    for indicator in key_indicators:
        result = impact_model.validate_model(indicator, observations, effect_type='gradual')
        if result:
            impact_model.plot_validation(indicator, f'reports/figures/validation_{indicator}.png')
    
    # Summarize results
    impact_model.summarize_validation_results()
    
    print("\\n🎯 EVENT IMPACT MODELING COMPLETE!")
    print("📁 Results saved to reports/ directory")
    print("📊 Association matrix: reports/event_indicator_matrix.csv")
    print("📈 Validation plots: reports/figures/")
    print("🚀 Ready for forecasting phase!")

if __name__ == "__main__":
    main()
