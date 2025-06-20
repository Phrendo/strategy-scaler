"""
Trading Strategy Scaling Calculator - Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import traceback

# Import our custom modules
from calculator import StrategyCalculator
from visualizations import VisualizationEngine

# Page configuration
st.set_page_config(
    page_title="Trading Strategy Scaling Calculator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load the custom CSS theme."""
    css_file = Path("theme.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'calculator' not in st.session_state:
    st.session_state.calculator = StrategyCalculator()
if 'viz_engine' not in st.session_state:
    st.session_state.viz_engine = VisualizationEngine()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'calculations_done' not in st.session_state:
    st.session_state.calculations_done = False
if 'last_csv_input' not in st.session_state:
    st.session_state.last_csv_input = ''
if 'trigger_calculation' not in st.session_state:
    st.session_state.trigger_calculation = False
if 'sample_data_loaded' not in st.session_state:
    st.session_state.sample_data_loaded = None

def load_sample_data():
    """Load the sample data for testing."""
    try:
        sample_file = Path("design/SOURCE_DATA_EXAMPLE.csv")
        if sample_file.exists():
            with open(sample_file, 'r') as f:
                return f.read()
    except Exception as e:
        st.error(f"Error loading sample data: {str(e)}")
    return None

def display_metrics(metrics: dict):
    """Display performance metrics in a formatted layout."""
    if not metrics:
        return
    
    # Original Strategy Metrics
    st.subheader("📊 Original Strategy Performance")
    orig = metrics['original']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">${orig['total_pnl']:,.2f}</div>
            <div class="custom-metric-label">Total P&L</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">{orig['win_rate']:.1%}</div>
            <div class="custom-metric-label">Win Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">${orig['avg_win']:,.2f}</div>
            <div class="custom-metric-label">Avg Win</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">${orig['max_drawdown']:,.2f}</div>
            <div class="custom-metric-label">Max Drawdown</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Scaled Strategy Metrics
    st.subheader("🚀 Scaled Strategy Performance")
    scaled = metrics['scaled']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">${scaled['final_capital']:,.2f}</div>
            <div class="custom-metric-label">Final Capital</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">{scaled['total_return_pct']:,.1f}%</div>
            <div class="custom-metric-label">Total Return</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">${scaled['avg_win']:,.2f}</div>
            <div class="custom-metric-label">Avg Scaled Win</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">{scaled['max_drawdown_pct']:,.1f}%</div>
            <div class="custom-metric-label">Max Drawdown %</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Position Sizing Metrics
    st.subheader("⚖️ Position Sizing Details")
    pos = metrics['position_sizing']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">${pos['max_loss_used']:,.2f}</div>
            <div class="custom-metric-label">Max Loss Used</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">{pos['risk_percentage']:.1%}</div>
            <div class="custom-metric-label">Risk Per Trade</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">{pos['max_position_size']:,}</div>
            <div class="custom-metric-label">Max Position Size</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-value">{pos['avg_position_size']:,.1f}</div>
            <div class="custom-metric-label">Avg Position Size</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.title("📈 Trading Strategy Scaling Calculator")
    st.markdown("**Calculate the performance of your trading strategy with proper position sizing and compounding**")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data input section
        st.subheader("📁 Data Input")

        # Data input
        csv_input = st.text_area(
            "Paste Data (CSV or Tab-Delimited)",
            height=200,
            placeholder="Date,PnL\n2024-01-01,1.50\n2024-01-02,-2.30\n\nOr tab-delimited from Excel/SSMS:\nDate\tPnL\n2024-01-01\t1.50\n2024-01-02\t-2.30\n\nPress Enter after pasting to auto-calculate!",
            key="csv_input",
            help="Supports CSV, tab-delimited (Excel), or semicolon-delimited data. Just copy and paste from Excel, SSMS, or any spreadsheet! Press Enter to auto-calculate."
        )

        # Sample data button (moved below input field)
        if st.button("🔄 Load Sample Data", help="Load the provided sample data for testing"):
            sample_data = load_sample_data()
            if sample_data:
                st.session_state.sample_data_loaded = sample_data
                st.success("Sample data loaded! It will be used for calculation.")
                # Auto-trigger calculation when sample data is loaded
                st.session_state.trigger_calculation = True
        
        # Calculation parameters
        st.subheader("💰 Parameters")
        starting_capital = st.number_input(
            "Starting Capital ($)",
            min_value=1.0,
            value=100.0,
            step=10.0,
            format="%.2f"
        )
        
        risk_percentage = st.number_input(
            "Risk Percentage (%)",
            min_value=0.1,
            max_value=100.0,
            value=10.0,
            step=0.1,
            format="%.1f"
        ) / 100  # Convert to decimal

        # Determine which data to use
        data_to_use = csv_input
        if st.session_state.sample_data_loaded:
            data_to_use = st.session_state.sample_data_loaded
            st.session_state.sample_data_loaded = None  # Clear after using

        # Auto-calculation logic: detect when data changes
        auto_calculate = False
        if data_to_use.strip() and data_to_use != st.session_state.get('last_csv_input', ''):
            st.session_state.last_csv_input = data_to_use
            auto_calculate = True

        # Check for manual trigger (from sample data button)
        if st.session_state.get('trigger_calculation', False):
            auto_calculate = True
            st.session_state.trigger_calculation = False

        # Calculate button
        calculate_button = st.button("🚀 Calculate Scaling", type="primary")

        # Determine if we should calculate
        should_calculate = calculate_button or auto_calculate
    
    # Main content area
    if should_calculate and data_to_use.strip():
        try:
            with st.spinner("Processing data and calculating scaling..."):
                # Parse the CSV data
                original_data = st.session_state.calculator.parse_csv_data(data_to_use)
                st.session_state.data_loaded = True
                
                # Calculate scaling
                scaled_data = st.session_state.calculator.calculate_scaling(
                    original_data, starting_capital, risk_percentage
                )
                
                # Calculate metrics
                metrics = st.session_state.calculator.calculate_performance_metrics()
                st.session_state.calculations_done = True
                
                st.success(f"✅ Successfully processed {len(original_data)} trading days!")
                
        except Exception as e:
            st.error(f"❌ Error processing data: {str(e)}")
            st.session_state.data_loaded = False
            st.session_state.calculations_done = False
    
    # Display results if calculations are done
    if st.session_state.calculations_done:
        # Get data from calculator
        original_data = st.session_state.calculator.original_data
        scaled_data = st.session_state.calculator.scaled_data
        metrics = st.session_state.calculator.calculate_performance_metrics()
        starting_capital = st.session_state.calculator.starting_capital
        
        # Display metrics
        display_metrics(metrics)
        
        # Create visualizations
        st.header("📊 Visualizations")
        
        # Two-column layout for side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Original Strategy")

            # Original equity curve
            try:
                orig_equity_fig = st.session_state.viz_engine.create_equity_curve(
                    original_data, "Original Strategy - Equity Curve", "original", starting_capital
                )
                st.plotly_chart(orig_equity_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating equity curve: {str(e)}")

            # Original daily waterfall
            try:
                orig_daily_fig = st.session_state.viz_engine.create_daily_waterfall(
                    original_data, "Original Strategy - Daily P&L", "original", starting_capital
                )
                st.plotly_chart(orig_daily_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating daily waterfall: {str(e)}")

            # Original weekly waterfall
            try:
                orig_weekly_data = st.session_state.calculator.get_weekly_data("original")
                orig_weekly_fig = st.session_state.viz_engine.create_weekly_waterfall(
                    orig_weekly_data, "Original Strategy - Weekly P&L"
                )
                st.plotly_chart(orig_weekly_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating weekly waterfall: {str(e)}")
        
        with col2:
            st.subheader("🚀 Scaled Strategy")

            # Scaled equity curve
            try:
                scaled_equity_fig = st.session_state.viz_engine.create_equity_curve(
                    scaled_data, "Scaled Strategy - Equity Curve", "scaled"
                )
                st.plotly_chart(scaled_equity_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating scaled equity curve: {str(e)}")

            # Scaled daily waterfall
            try:
                scaled_daily_fig = st.session_state.viz_engine.create_daily_waterfall(
                    scaled_data, "Scaled Strategy - Daily P&L", "scaled"
                )
                st.plotly_chart(scaled_daily_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating scaled daily waterfall: {str(e)}")

            # Scaled weekly waterfall
            try:
                scaled_weekly_data = st.session_state.calculator.get_weekly_data("scaled")
                scaled_weekly_fig = st.session_state.viz_engine.create_weekly_waterfall(
                    scaled_weekly_data, "Scaled Strategy - Weekly P&L"
                )
                st.plotly_chart(scaled_weekly_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating scaled weekly waterfall: {str(e)}")
        
        # Additional charts
        st.subheader("📊 Additional Analysis")

        # Comparison chart
        try:
            comparison_fig = st.session_state.viz_engine.create_comparison_chart(original_data, scaled_data, starting_capital)
            st.plotly_chart(comparison_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating comparison chart: {str(e)}")

        # Position size chart
        try:
            position_fig = st.session_state.viz_engine.create_position_size_chart(scaled_data)
            st.plotly_chart(position_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating position size chart: {str(e)}")
        
        # Data tables
        st.subheader("📋 Detailed Data")
        
        tab1, tab2 = st.tabs(["Original Data", "Scaled Data"])
        
        with tab1:
            st.dataframe(original_data, use_container_width=True)
        
        with tab2:
            st.dataframe(scaled_data, use_container_width=True)
    
    elif not st.session_state.data_loaded:
        # Welcome message
        st.info("👋 Welcome! Please paste your CSV data in the sidebar - it will auto-calculate when you press Enter!")

        # Instructions
        st.subheader("📖 How to Use")
        st.markdown("""
        1. **Prepare your data**: Ensure you have daily P&L data with Date and PnL columns
        2. **Copy from source**:
           - **Excel**: Select your data and copy (Ctrl+C)
           - **SSMS**: Copy query results directly
           - **CSV files**: Copy the content
        3. **Paste data**: Paste into the text area in the sidebar and **press Enter** - it will auto-calculate!
        4. **Set parameters**: Configure your starting capital and risk percentage (optional - defaults work great)
        5. **Auto-calculation**: The app automatically processes your data when you paste and press Enter
        6. **Analyze**: Review the performance metrics and visualizations

        **Sample Data**: Click 'Load Sample Data' to try the calculator with provided example data.

        **Supported Formats**: CSV, Tab-delimited (Excel), Semicolon-delimited - the app auto-detects the format!

        **💡 Pro Tip**: Just paste your data and press Enter - no need to click buttons!
        """)

if __name__ == "__main__":
    main()
