# Trading Strategy Scaling Calculator - Design Document

## Project Overview

This application calculates the performance of a trading strategy with proper position sizing and compounding. It takes historical trading data (daily P&L values) and applies a risk-based position sizing algorithm to show how the strategy would perform with compounding over time.

## Core Functionality

1. **Data Input**
   - Paste in CSV data directly into the application
   - Validate data format and structure
   - Expected Format: CSV with two columns - "Date" and "PnL"
   - Header may sometimes be present, header names may vary. - allow for this. We are after the Date values and the PnL values.
   - This data is in the form of one row per day. So its the daily sum.

2. **Calculation Engine**
   - We offer the user two input variables:
     - Starting capital
     - Risk percentage
   - We compound this daily, rounding the multiplier DOWN to the nearest whole number before applying it to the PnL.
   - We compound in order, oldest to newest.
   - Effectively, each row of the data as a StartingBR, Cnt, NetResult and EndingBR -- each day the EndingBR becomes the next day's StartingBR.

3. **Visualization**
   - Two sided display:
        - Original P&L data
        - Scaled P&L data after applying position sizing and compounding
   - Both sides of the display will have:
        - A line chart the equit curve and drawdown
        - A daily waterfall chart with no total bar
        - A weekly waterfall chart with no total bar


## Technology Stack

### Frontend
- **Streamlit**: Python-based UI framework
  - Provides interactive data input forms
  - Implement proper compounding formulas
  - Displays visualizations and results
  - Offers intuitive user experience

### Data Processing
- **Pandas**: For data manipulation and analysis
- **NumPy**: For numerical operations
- **Plotly**: For data visualization

## Calculation Methodology

### Position Sizing Algorithm

The position sizing algorithm follows these principles:

1. **Risk-Based Sizing**: Position size is determined by the percentage of current capital risked per trade -- which is the max loss of the sample.
2. **Whole-Number Positions**: Only whole-number position sizes are used (no fractional positions) - rounded down
3. **Daily Compounding**: Capital is updated after each trade, affecting subsequent position sizes

### Detailed Algorithm

1. Calculate the maximum loss in the sample data to determine risk per unit
2. For each trading day:
   - Calculate position size by dividing (current capital × risk percentage) by maximum loss
   - Use floor function to ensure whole-number position sizing (round down)
   - Multiply the day's original P&L by the position size to get the scaled P&L
   - Add the scaled P&L to the running capital
   - Use updated capital for next day's position sizing calculation

### Mathematical Formula

Position Size = FLOOR((Current Capital × Risk Percentage) ÷ Maximum Loss)
Daily P&L = Original P&L × Position Size
Updated Capital = Previous Capital + Daily P&L

### Performance Metrics

The application calculates the following metrics:
- Total return (absolute and percentage)
- Maximum drawdown
- Win rate
- Average win/loss
- Maximum position size
- Average position size
- Risk-adjusted return metrics

## Development Roadmap

### Phase 1: Core Calculation Engine
- Implement the position sizing and compounding algorithm
- Create data processing pipeline
- Develop unit tests for calculation accuracy
- Sample files are included in design folder (Source and Scaled if starting with 100, .10 risk)

### Phase 2: Frontend Implementation
- Develop Streamlit interface
- Implement data visualization components
- Create user input forms and controls

### Phase 3: Testing and Refinement
- Comprehensive testing with various datasets
- Performance optimization
- User experience improvements
