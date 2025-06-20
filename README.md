# Trading Strategy Scaling Calculator

A comprehensive web application built with Streamlit that calculates the performance of trading strategies with proper position sizing and compounding. Features a sleek jet black theme with matrix green highlights.

## Features

### 🚀 Core Functionality
- **Position Sizing Algorithm**: Risk-based position sizing with whole-number positions (rounded down)
- **Daily Compounding**: Capital updates after each trade, affecting subsequent position sizes
- **Flexible Data Input**: Supports CSV, tab-delimited (Excel), and semicolon-delimited formats
- **Auto-Detection**: Automatically detects delimiter type from pasted data
- **Auto-Calculation**: Automatically processes data when you paste and press Enter
- **One-Click Loading**: Sample data button for instant testing

### 📊 Visualizations
- **Side-by-Side Comparison**: Original vs scaled strategy performance (includes starting capital)
- **Equity Curves**: Shows cumulative performance with drawdown visualization
- **Daily Waterfall Charts**: True waterfall charts showing cumulative P&L progression
- **Weekly Waterfall Charts**: Weekly aggregated waterfall performance
- **Position Size Tracking**: Shows position size changes over time

### 📈 Performance Metrics
- Total return (absolute and percentage)
- Maximum drawdown and drawdown percentage
- Win rate and average win/loss
- Position sizing statistics (max, average, minimum)
- Risk-adjusted return metrics

### 🎨 Design
- **Matrix Theme**: Jet black background with matrix green highlights
- **Responsive Layout**: Side-by-side panels for easy comparison
- **CSS Theming**: Easily customizable color scheme via `theme.css`
- **Professional UI**: Clean, modern interface optimized for data analysis

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation
1. Clone or download the project
2. Run the setup:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running the Application
- **Easy Start**: Double-click `run_app.bat`
- **Manual Start**: 
  ```bash
  .venv\Scripts\activate
  streamlit run app.py
  ```
- **Testing**: Double-click `run_test.bat` or run `python test_calculator.py`

## How to Use

### 1. Data Preparation
Prepare your daily P&L data with Date and PnL columns. The app supports:
- **CSV format**: `Date,PnL`
- **Tab-delimited** (Excel): Copy directly from Excel spreadsheets
- **SSMS results**: Copy query results directly from SQL Server Management Studio
- **Semicolon-delimited**: European CSV format

### 2. Data Input
- **Copy from Excel**: Select your data range and copy (Ctrl+C)
- **Copy from SSMS**: Copy query results directly
- **Paste**: Paste into the text area in the sidebar and **press Enter**
- **Auto-Calculate**: The app automatically processes your data when you press Enter
- **Sample Data**: Click "Load Sample Data" to try with provided examples (auto-calculates)

### 3. Configuration
- **Starting Capital**: Set your initial capital amount
- **Risk Percentage**: Set the percentage of capital to risk per trade

### 4. Analysis
- Review comprehensive performance metrics
- Compare original vs scaled strategy performance
- Analyze equity curves and drawdown patterns
- Examine daily and weekly P&L distributions

## Calculation Methodology

### Position Sizing Formula
```
Position Size = FLOOR((Current Capital × Risk Percentage) ÷ Maximum Loss)
Daily P&L = Original P&L × Position Size
Updated Capital = Previous Capital + Daily P&L
```

### Key Principles
1. **Risk-Based Sizing**: Position size determined by percentage of current capital risked
2. **Maximum Loss**: Uses the largest single-day loss in the dataset for risk calculation
3. **Whole Numbers**: Only whole-number position sizes (no fractional positions)
4. **Daily Compounding**: Capital updated after each trade, affecting subsequent positions

## File Structure

```
├── app.py                 # Main Streamlit application
├── calculator.py          # Core calculation engine
├── visualizations.py      # Chart generation and theming
├── theme.css             # Matrix theme styling
├── requirements.txt      # Python dependencies
├── test_calculator.py    # Test suite
├── run_app.bat          # Easy app launcher
├── run_test.bat         # Easy test runner
├── design/              # Design documents and sample data
│   ├── new_design.md
│   ├── SOURCE_DATA_EXAMPLE.csv
│   └── SCALED_100_10_DATA_EXAMPLE.csv
└── README.md           # This file
```

## Customization

### Theme Colors
Edit `theme.css` to customize the color scheme:
```css
:root {
    --bg-primary: #000000;        /* Main background */
    --accent-primary: #00ff41;    /* Matrix green */
    --text-primary: #ffffff;      /* Text color */
    /* ... other variables ... */
}
```

### Adding New Metrics
Extend the `calculate_performance_metrics()` method in `calculator.py` to add new performance calculations.

## Testing

The application includes comprehensive tests:
- **Sample Data Validation**: Tests against provided sample data
- **Tab-Delimited Support**: Verifies Excel/SSMS compatibility
- **Edge Cases**: Handles invalid data gracefully
- **Calculation Accuracy**: Validates against expected results

Run tests with: `python test_calculator.py`

## Dependencies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **Plotly**: Interactive data visualization

## License

This project is provided as-is for educational and analysis purposes.

## Support

For issues or questions, refer to the test suite and sample data for expected formats and behavior.
