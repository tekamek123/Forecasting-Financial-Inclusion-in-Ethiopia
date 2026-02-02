#!/usr/bin/env python3
"""
Forecasting Access and Usage for Ethiopia Financial Inclusion Project
Task 4: Forecast Account Ownership and Digital Payment Usage for 2025-2027
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Set styling
plt.style.use('seaborn-v0_8-whitegrid')
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83']

class FinancialInclusionForecaster:
    """
    Comprehensive forecasting system for financial inclusion indicators
    """
    
    def __init__(self):
        self.targets = {
            'ACC_OWNERSHIP': {
                'name': 'Account Ownership Rate',
                'description': '% of adults with account at financial institution or mobile money',
                'target_nfis': 70  # NFIS target for 2025
            },
            'USG_DIGITAL_PAYMENT': {
                'name': 'Digital Payment Usage',
                'description': '% of adults who made or received digital payment',
                'target_nfis': 70  # NFIS target for 2025
            }
        }
        self.historical_data = {}
        self.baseline_models = {}
        self.forecasts = {}
        self.scenario_forecasts = {}
        
    def load_data(self):
        """Load and prepare data for forecasting"""
        print("📊 LOADING DATA FOR FORECASTING")
        
        # Load datasets
        df_main = pd.read_excel('data/processed/ethiopia_fi_unified_data_enriched.xlsx')
        df_main['observation_date'] = pd.to_datetime(df_main['observation_date'], errors='coerce')
        observations = df_main[df_main['record_type'] == 'observation']
        
        print(f"   Main records: {len(df_main)}")
        print(f"   Observations: {len(observations)}")
        
        # Extract historical data for targets
        for indicator in self.targets.keys():
            data = observations[observations['indicator_code'] == indicator].sort_values('observation_date')
            if len(data) > 0:
                self.historical_data[indicator] = {
                    'dates': data['observation_date'].values,
                    'years': data['observation_date'].dt.year.values,
                    'values': data['value_numeric'].values
                }
                print(f"   ✅ {indicator}: {len(data)} data points ({data['observation_date'].min().year}-{data['observation_date'].max().year})")
            else:
                print(f"   ❌ {indicator}: No data available")
        
        return observations
    
    def analyze_baseline_trends(self):
        """Analyze baseline trends for each target indicator"""
        print("\n📈 ANALYZING BASELINE TRENDS")
        
        for indicator, data in self.historical_data.items():
            print(f"\n   {self.targets[indicator]['name']}:")
            
            # Prepare data for regression
            years = data['years'].reshape(-1, 1)
            values = data['values']
            
            # Fit linear regression
            linear_model = LinearRegression()
            linear_model.fit(years, values)
            
            # Calculate performance metrics
            linear_pred = linear_model.predict(years)
            linear_mae = mean_absolute_error(values, linear_pred)
            linear_r2 = linear_model.score(years, values)
            
            print(f"      Linear Trend: y = {linear_model.coef_[0]:.3f}x + {linear_model.intercept_:.3f}")
            print(f"      MAE: {linear_mae:.2f}, R²: {linear_r2:.3f}")
            
            # Store model
            self.baseline_models[indicator] = {
                'linear': linear_model,
                'mae': linear_mae,
                'r2': linear_r2,
                'data': data
            }
            
            # Create visualization
            self._plot_baseline_trend(indicator)
    
    def _plot_baseline_trend(self, indicator):
        """Create baseline trend visualization"""
        data = self.baseline_models[indicator]['data']
        linear_model = self.baseline_models[indicator]['linear']
        
        plt.figure(figsize=(12, 6))
        plt.scatter(data['years'], data['values'], color='blue', s=100, label='Historical Data', zorder=5)
        
        # Plot linear trend
        trend_years = np.arange(min(data['years']), 2028)
        linear_trend = linear_model.predict(trend_years.reshape(-1, 1))
        plt.plot(trend_years, linear_trend, 'r--', label='Linear Trend', linewidth=2)
        
        # Add NFIS target
        plt.axhline(y=self.targets[indicator]['target_nfis'], color='orange', linestyle=':', 
                    label=f'NFIS Target ({self.targets[indicator]["target_nfis"]}%)', alpha=0.7)
        
        plt.title(f'{self.targets[indicator]["name"]} - Baseline Trend Analysis', fontsize=14, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Rate (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'reports/figures/baseline_trend_{indicator}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_forecasts(self, forecast_years=None):
        """Generate baseline forecasts for specified years"""
        if forecast_years is None:
            forecast_years = np.array([2025, 2026, 2027])
        
        print(f"\n🔮 GENERATING FORECASTS FOR {forecast_years}")
        
        for indicator, model_info in self.baseline_models.items():
            print(f"\n   {self.targets[indicator]['name']}:")
            
            # Baseline forecast
            linear_model = model_info['linear']
            baseline_forecast = linear_model.predict(forecast_years.reshape(-1, 1))
            
            # Calculate confidence intervals
            historical_values = model_info['data']['values']
            std_error = np.std(historical_values - linear_model.predict(model_info['data']['years'].reshape(-1, 1)))
            confidence_interval = 1.96 * std_error
            
            baseline_lower = baseline_forecast - confidence_interval
            baseline_upper = baseline_forecast + confidence_interval
            
            # Store forecasts
            self.forecasts[indicator] = {
                'years': forecast_years,
                'baseline': baseline_forecast,
                'baseline_lower': baseline_lower,
                'baseline_upper': baseline_upper,
                'confidence_interval': confidence_interval
            }
            
            # Display forecast table
            print(f"      Year | Forecast | Lower CI | Upper CI | NFIS Target | Gap")
            print(f"      -----|----------|----------|----------|-------------|-----")
            
            for i, year in enumerate(forecast_years):
                forecast_val = self.forecasts[indicator]['baseline'][i]
                lower_val = self.forecasts[indicator]['baseline_lower'][i]
                upper_val = self.forecasts[indicator]['baseline_upper'][i]
                target = self.targets[indicator]['target_nfis']
                gap = target - forecast_val
                
                print(f"      {year} | {forecast_val:8.1f} | {lower_val:8.1f} | {upper_val:8.1f} | {target:11.1f} | {gap:+4.1f}")
            
            # Create forecast visualization
            self._plot_forecast(indicator)
    
    def _plot_forecast(self, indicator):
        """Create forecast visualization"""
        data = self.baseline_models[indicator]['data']
        forecast_data = self.forecasts[indicator]
        
        plt.figure(figsize=(14, 7))
        
        # Historical data
        plt.scatter(data['years'], data['values'], color='blue', s=100, label='Historical Data', zorder=5)
        
        # Baseline forecast
        plt.plot(forecast_data['years'], forecast_data['baseline'], 'r--', 
                label='Baseline Forecast', linewidth=2, marker='o')
        plt.fill_between(forecast_data['years'], forecast_data['baseline_lower'], 
                        forecast_data['baseline_upper'], alpha=0.2, color='red', label='95% CI')
        
        # NFIS target
        plt.axhline(y=self.targets[indicator]['target_nfis'], color='orange', linestyle=':', 
                    label=f'NFIS Target ({self.targets[indicator]["target_nfis"]}%)', alpha=0.7, linewidth=2)
        
        plt.title(f'{self.targets[indicator]["name"]} Forecast (2025-2027)', fontsize=16, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Rate (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, max(100, self.targets[indicator]['target_nfis'] * 1.2))
        plt.tight_layout()
        plt.savefig(f'reports/figures/forecast_{indicator}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_scenarios(self, forecast_years=None):
        """Generate scenario-based forecasts"""
        if forecast_years is None:
            forecast_years = np.array([2025, 2026, 2027])
        
        # Define scenarios
        scenarios = {
            'optimistic': {
                'description': 'Accelerated digital adoption, successful policy implementation',
                'trend_multiplier': 1.3
            },
            'base': {
                'description': 'Current trends continue',
                'trend_multiplier': 1.0
            },
            'pessimistic': {
                'description': 'Slower adoption, implementation challenges',
                'trend_multiplier': 0.7
            }
        }
        
        print("\n📋 GENERATING SCENARIO ANALYSIS")
        print("   Scenarios defined:")
        for scenario, config in scenarios.items():
            print(f"      {scenario.title()}: {config['description']} (multiplier: {config['trend_multiplier']})")
        
        for indicator, model_info in self.baseline_models.items():
            print(f"\n   {self.targets[indicator]['name']}:")
            
            self.scenario_forecasts[indicator] = {}
            
            for scenario_name, config in scenarios.items():
                # Adjust baseline trend
                linear_model = model_info['linear']
                
                # Create adjusted model
                adjusted_model = LinearRegression()
                adjusted_model.coef_ = np.array([linear_model.coef_[0] * config['trend_multiplier']])
                adjusted_model.intercept_ = linear_model.intercept_
                
                # Generate forecast
                scenario_forecast = adjusted_model.predict(forecast_years.reshape(-1, 1))
                self.scenario_forecasts[indicator][scenario_name] = scenario_forecast
                
                print(f"      {scenario_name.title()}: {scenario_forecast[-1]:.1f}% (2027)")
            
            # Create scenario visualization
            self._plot_scenarios(indicator)
    
    def _plot_scenarios(self, indicator):
        """Create scenario analysis visualization"""
        data = self.baseline_models[indicator]['data']
        forecast_years = self.forecasts[indicator]['years']
        
        plt.figure(figsize=(14, 7))
        
        # Historical data
        plt.scatter(data['years'], data['values'], color='blue', s=100, label='Historical Data', zorder=5)
        
        # Scenario forecasts
        colors_scenarios = {'optimistic': 'green', 'base': 'blue', 'pessimistic': 'red'}
        
        for scenario_name, forecast_values in self.scenario_forecasts[indicator].items():
            plt.plot(forecast_years, forecast_values, 
                    color=colors_scenarios[scenario_name], 
                    label=f'{scenario_name.title()} Scenario', 
                    linewidth=2, marker='o')
        
        # NFIS target
        plt.axhline(y=self.targets[indicator]['target_nfis'], color='orange', linestyle=':', 
                    label=f'NFIS Target ({self.targets[indicator]["target_nfis"]}%)', alpha=0.7, linewidth=2)
        
        plt.title(f'{self.targets[indicator]["name"]} - Scenario Analysis (2025-2027)', fontsize=16, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Rate (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, max(100, self.targets[indicator]['target_nfis'] * 1.2))
        plt.tight_layout()
        plt.savefig(f'reports/figures/scenarios_{indicator}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_summary_table(self):
        """Create comprehensive forecast summary table"""
        print("\n📊 CREATING FORECAST SUMMARY TABLE")
        
        forecast_table = []
        forecast_years = self.forecasts[list(self.forecasts.keys())[0]]['years']
        
        for indicator in self.targets.keys():
            if indicator in self.forecasts:
                for i, year in enumerate(forecast_years):
                    row = {
                        'Indicator': self.targets[indicator]['name'],
                        'Year': year,
                        'Baseline_Forecast': self.forecasts[indicator]['baseline'][i],
                        'Lower_CI': self.forecasts[indicator]['baseline_lower'][i],
                        'Upper_CI': self.forecasts[indicator]['baseline_upper'][i],
                        'Optimistic': self.scenario_forecasts[indicator]['optimistic'][i],
                        'Base_Scenario': self.scenario_forecasts[indicator]['base'][i],
                        'Pessimistic': self.scenario_forecasts[indicator]['pessimistic'][i],
                        'NFIS_Target': self.targets[indicator]['target_nfis']
                    }
                    forecast_table.append(row)
        
        forecast_df = pd.DataFrame(forecast_table)
        
        # Display formatted table
        print("\n" + "="*110)
        print(f"{'Indicator':<25} {'Year':<6} {'Baseline':<10} {'Optimistic':<12} {'Pessimistic':<12} {'Target':<8}")
        print("="*110)
        
        for _, row in forecast_df.iterrows():
            print(f"{row['Indicator']:<25} {row['Year']:<6} {row['Baseline_Forecast']:<10.1f} "
                  f"{row['Optimistic']:<12.1f} {row['Pessimistic']:<12.1f} {row['NFIS_Target']:<8.1f}")
        
        # Save to CSV
        import os
        os.makedirs('reports', exist_ok=True)
        forecast_df.to_csv('reports/forecast_summary_2025_2027.csv', index=False)
        print(f"\n💾 Forecast table saved to reports/forecast_summary_2025_2027.csv")
        
        return forecast_df
    
    def generate_insights(self):
        """Generate key insights and interpretations"""
        print("\n🎯 KEY FORECASTING INSIGHTS")
        print("\n1. TARGET ACHIEVEMENT PROSPECTS:")
        
        for indicator, forecast_data in self.forecasts.items():
            target = self.targets[indicator]['target_nfis']
            baseline_2027 = forecast_data['baseline'][-1]
            gap = target - baseline_2027
            
            print(f"\n   {self.targets[indicator]['name']}:")
            print(f"      NFIS Target: {target}%")
            print(f"      2027 Forecast: {baseline_2027:.1f}% (gap: {gap:+.1f}pp)")
            
            if gap > 0:
                print(f"      Status: ⚠️  Target not reached (shortfall: {gap:.1f}pp)")
            else:
                print(f"      Status: ✅ Target exceeded (surplus: {abs(gap):.1f}pp)")
        
        print("\n2. SCENARIO RANGES:")
        for indicator in self.scenario_forecasts.keys():
            optimistic_2027 = self.scenario_forecasts[indicator]['optimistic'][-1]
            pessimistic_2027 = self.scenario_forecasts[indicator]['pessimistic'][-1]
            range_width = optimistic_2027 - pessimistic_2027
            
            print(f"   {self.targets[indicator]['name']}: {pessimistic_2027:.1f}% - {optimistic_2027:.1f}% (range: {range_width:.1f}pp)")
        
        print("\n3. UNCERTAINTY ASSESSMENT:")
        print("   • Limited historical data (only 5 Findex points over 13 years)")
        print("   • Confidence intervals reflect historical variance only")
        print("   • Scenario analysis captures structural uncertainty")
        print("   • External factors (policy, technology) not fully captured")
        
        print("\n4. POLICY IMPLICATIONS:")
        print("   • Current trajectory insufficient for NFIS targets")
        print("   • Optimistic scenario requires accelerated implementation")
        print("   • Monitoring and adjustment critical for target achievement")
        print("   • Event interventions could significantly improve outcomes")
        
        print("\n5. RECOMMENDATIONS:")
        print("   • Focus on optimistic scenario drivers: digital adoption, policy implementation")
        print("   • Implement monitoring framework to track progress")
        print("   • Consider additional interventions to close target gaps")
        print("   • Update forecasts annually with new data")

def main():
    """Main function to run forecasting analysis"""
    print("🇪🇹 ETHIOPIA FINANCIAL INCLUSION - FORECASTING ACCESS AND USAGE")
    print("=" * 60)
    
    # Initialize forecaster
    forecaster = FinancialInclusionForecaster()
    
    # Load data
    observations = forecaster.load_data()
    
    # Analyze baseline trends
    forecaster.analyze_baseline_trends()
    
    # Generate forecasts
    forecaster.generate_forecasts()
    
    # Generate scenarios
    forecaster.generate_scenarios()
    
    # Create summary table
    forecast_df = forecaster.create_summary_table()
    
    # Generate insights
    forecaster.generate_insights()
    
    print("\n🎉 FORECASTING ANALYSIS COMPLETE!")
    print("📁 Results saved to reports/ directory")
    print("📊 Forecast table: reports/forecast_summary_2025_2027.csv")
    print("📈 Visualizations: reports/figures/")
    print("🚀 Ready for Dashboard Development (Task 5)!")

if __name__ == "__main__":
    main()
