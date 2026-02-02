# Ethiopia Financial Inclusion Dashboard

Interactive Streamlit dashboard for visualizing Ethiopia's financial inclusion forecasts and analysis results.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit installed
- Project dependencies installed

### Installation

1. **Install dependencies:**
```bash
# From project root directory
pip install -r requirements.txt
```

2. **Navigate to dashboard directory:**
```bash
cd dashboard
```

3. **Run the dashboard:**
```bash
streamlit run app.py
```

4. **Open in browser:**
- Dashboard will automatically open at `http://localhost:8501`
- Or manually navigate to `http://localhost:8501`

## 📊 Dashboard Features

### 📋 Navigation Pages

1. **📊 Overview** - Key metrics and insights
2. **📈 Trends Analysis** - Interactive time series and channel comparisons
3. **🔮 Forecasts** - 2025-2027 projections with confidence intervals
4. **🎯 Inclusion Projections** - NFIS target progress and scenarios
5. **⚡ Event Impact Analysis** - Policy and market event impacts
6. **📋 Methodology** - Data sources and modeling approach

### 🎯 Key Features

#### Overview Page
- **Key Metrics Cards**: Account ownership, digital payment usage, P2P/ATM ratio, growth rates
- **Growth Trajectory Insights**: Historical progress and trends
- **Target Progress**: NFIS 2025 target tracking
- **Recent Events Timeline**: Key policy and market events
- **Interactive Charts**: Account ownership trend visualization

#### Trends Analysis Page
- **Date Range Selector**: Customizable time period analysis
- **Interactive Time Series**: Account ownership and digital payment trends
- **Channel Comparison**: Bank accounts vs mobile money vs digital wallets
- **Growth Rate Analysis**: Annual growth rate calculations
- **Multi-indicator Views**: Side-by-side trend comparisons

#### Forecasts Page
- **Model Selection**: Baseline, event-augmented, optimistic, pessimistic scenarios
- **Forecast Visualizations**: Historical + projected trends
- **Confidence Intervals**: 95% confidence bands
- **Key Milestones**: Year-by-year projections
- **Target Comparison**: NFIS goal tracking

#### Inclusion Projections Page
- **Scenario Selector**: Optimistic/base/pessimistic scenarios
- **Progress Visualization**: Historical + projected paths to targets
- **Projection Summary Tables**: Detailed forecast data
- **Key Q&A**: Answers to consortium questions
- **Gap Analysis**: Target achievement assessment

#### Event Impact Analysis Page
- **Event Timeline**: Visual event markers on trends
- **Impact Summary Table**: Event details and estimated impacts
- **Impact Magnitude Charts**: Bar charts of event effects
- **Event Type Analysis**: Policy vs market entry impacts

#### Methodology Page
- **Data Sources**: Comprehensive data inventory
- **Modeling Approach**: Technical methodology
- **Key Assumptions**: Model assumptions and limitations
- **Uncertainty Assessment**: Confidence intervals and scenarios

### 📥 Data Download

Download functionality for:
- **Historical Data**: Raw observation data
- **Forecast Data**: Projection results
- **Event Data**: Event impact database

## 🛠️ Technical Requirements

### Dependencies
- `streamlit`: Dashboard framework
- `pandas`: Data manipulation
- `plotly`: Interactive visualizations
- `numpy`: Numerical operations
- `openpyxl`: Excel file reading

### Data Files
The dashboard expects these data files:
- `../data/processed/ethiopia_fi_unified_data_enriched.xlsx` - Main dataset
- `../reports/forecast_summary_2025_2027.csv` - Forecast results

### File Structure
```
dashboard/
├── app.py              # Main Streamlit application
├── README.md           # This file
└── requirements.txt    # Dashboard-specific dependencies

../data/processed/     # Processed data files
../reports/            # Forecast results and figures
```

## 🎨 Customization

### Styling
The dashboard uses custom CSS for:
- Metric cards with colored borders
- Insight boxes with highlighting
- Responsive layout
- Professional color scheme

### Data Integration
To integrate new data:
1. Update data loading functions in `app.py`
2. Modify data processing logic
3. Update visualizations accordingly

### Adding New Pages
1. Add page to navigation sidebar
2. Create new `elif page == "Page Name":` block
3. Implement page content and visualizations

## 📱 Mobile Responsiveness

The dashboard is designed for:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout
- **Mobile**: Responsive design with scrollable content

## 🔧 Troubleshooting

### Common Issues

1. **Data file not found**
   - Ensure data files are in correct locations
   - Check file paths in `load_data()` functions
   - Dashboard will show sample data if files missing

2. **Port already in use**
   ```bash
   # Use different port
   streamlit run app.py --server.port 8502
   ```

3. **Dependencies missing**
   ```bash
   # Install missing packages
   pip install streamlit plotly pandas numpy openpyxl
   ```

4. **Slow loading**
   - Data is cached using `@st.cache_data`
   - First load may be slower
   - Subsequent loads should be faster

### Performance Tips
- Use data caching for large datasets
- Limit date range selections for better performance
- Clear cache if data updated: Streamlit → Settings → Clear cache

## 📊 Data Sources

### Primary Sources
- **World Bank Global Findex Database**: Financial inclusion indicators
- **National Bank of Ethiopia**: Regulatory data and statistics
- **Mobile Money Operators**: Usage and adoption metrics
- **Policy Documents**: NFIS implementation and digital finance strategy

### Data Updates
- Historical data: Updated as new Findex releases available
- Forecast data: Generated from modeling scripts
- Event data: Updated as new policies and market events occur

## 🔒 Security Considerations

- No sensitive personal data displayed
- All data is aggregated and anonymized
- No external API calls to sensitive systems
- Local deployment recommended for sensitive data

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Verify data file locations and formats
3. Review Streamlit documentation
4. Contact development team

## 🚀 Deployment Options

### Local Development
```bash
cd dashboard
streamlit run app.py
```

### Production Deployment
Options include:
- **Streamlit Cloud**: Easy cloud deployment
- **Docker**: Containerized deployment
- **Cloud Services**: AWS, GCP, Azure deployment
- **On-premise**: Internal server deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📈 Future Enhancements

Planned improvements:
- **Real-time data integration**: Live data feeds
- **Advanced analytics**: Machine learning predictions
- **User authentication**: Secure multi-user access
- **Export functionality**: PDF reports and custom exports
- **Mobile app**: Native mobile application
- **API integration**: External system connections

---

*Dashboard developed by Selam Analytics for Ethiopia Financial Inclusion Forecasting Project*
