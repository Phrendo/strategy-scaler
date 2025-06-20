"""
Trading Strategy Scaling Calculator - Visualization Components
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any


class ChartTheme:
    """Matrix-themed chart styling for consistent dark theme across all visualizations."""
    
    # Color scheme
    BG_PRIMARY = '#000000'
    BG_SECONDARY = '#111111'
    ACCENT_PRIMARY = '#00ff41'
    ACCENT_SECONDARY = '#00cc33'
    TEXT_PRIMARY = '#ffffff'
    TEXT_SECONDARY = '#cccccc'
    TEXT_MUTED = '#888888'
    GRID_COLOR = '#333333'
    
    @classmethod
    def get_layout_template(cls) -> Dict[str, Any]:
        """Get the standard layout template for all charts."""
        return {
            'plot_bgcolor': cls.BG_PRIMARY,
            'paper_bgcolor': cls.BG_PRIMARY,
            'font': {'color': cls.TEXT_PRIMARY, 'family': 'Arial, sans-serif'},
            'xaxis': {
                'gridcolor': cls.GRID_COLOR,
                'linecolor': cls.GRID_COLOR,
                'tickcolor': cls.TEXT_SECONDARY,
                'title': {'font': {'color': cls.TEXT_PRIMARY}},
                'tickfont': {'color': cls.TEXT_SECONDARY}
            },
            'yaxis': {
                'gridcolor': cls.GRID_COLOR,
                'linecolor': cls.GRID_COLOR,
                'tickcolor': cls.TEXT_SECONDARY,
                'title': {'font': {'color': cls.TEXT_PRIMARY}},
                'tickfont': {'color': cls.TEXT_SECONDARY}
            },
            'legend': {
                'font': {'color': cls.TEXT_PRIMARY},
                'bgcolor': cls.BG_SECONDARY,
                'bordercolor': cls.GRID_COLOR,
                'borderwidth': 1
            },
            'title': {'font': {'color': cls.ACCENT_PRIMARY, 'size': 16}}
        }


class VisualizationEngine:
    """Creates all chart visualizations for the trading strategy calculator."""
    
    def __init__(self):
        self.theme = ChartTheme()
    
    def create_equity_curve(self, data: pd.DataFrame, title: str, data_type: str = 'scaled', starting_capital: float = 100.0) -> go.Figure:
        """
        Create equity curve chart showing cumulative performance over time.
        
        Args:
            data: DataFrame with trading data
            title: Chart title
            data_type: 'original' or 'scaled'
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        if data_type == 'original':
            # For original data, show cumulative P&L + starting capital
            y_values = starting_capital + data['PnL'].cumsum()
            y_title = "Account Balance"
            line_color = self.theme.ACCENT_SECONDARY
        else:
            # For scaled data, show ending bankroll
            y_values = data['EndingBR']
            y_title = "Account Balance"
            line_color = self.theme.ACCENT_PRIMARY
        
        # Add equity curve
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=y_values,
            mode='lines',
            name='Equity Curve',
            line=dict(color=line_color, width=2),
            hovertemplate='<b>Date:</b> %{x}<br><b>' + y_title + ':</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # Calculate and add drawdown
        running_max = y_values.expanding().max()
        drawdown = y_values - running_max
        
        # Add drawdown as filled area (only if there are drawdowns)
        if drawdown.min() < 0:
            fig.add_trace(go.Scatter(
                x=data['Date'],
                y=drawdown,
                mode='lines',
                name='Drawdown',
                line=dict(color='#ff4444', width=1),
                fill='tozeroy',
                fillcolor='rgba(255, 68, 68, 0.3)',
                hovertemplate='<b>Date:</b> %{x}<br><b>Drawdown:</b> $%{y:,.2f}<extra></extra>'
            ))
        
        # Apply theme
        layout = self.theme.get_layout_template()
        layout.update({
            'title': title,
            'xaxis_title': 'Date',
            'yaxis_title': y_title,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**layout)
        return fig
    
    def create_daily_waterfall(self, data: pd.DataFrame, title: str, data_type: str = 'scaled', starting_capital: float = 100.0) -> go.Figure:
        """
        Create daily waterfall chart showing cumulative progression with individual day contributions.

        Args:
            data: DataFrame with trading data
            title: Chart title
            data_type: 'original' or 'scaled'
            starting_capital: Starting capital for original data

        Returns:
            Plotly figure object
        """
        if data_type == 'original':
            pnl_values = data['PnL']
            # Calculate cumulative values starting from starting capital
            cumulative = starting_capital + pnl_values.cumsum()
            base_values = [starting_capital] + cumulative.iloc[:-1].tolist()
        else:
            pnl_values = data['Scaled_PnL']
            # Use the actual starting and ending bankroll values
            cumulative = data['EndingBR']
            base_values = data['StartingBR'].tolist()

        # Create waterfall chart using Plotly's waterfall trace
        fig = go.Figure()

        # Prepare data for waterfall
        x_values = data['Date'].tolist()
        y_values = pnl_values.tolist()

        # Create colors based on positive/negative values
        colors = [self.theme.ACCENT_PRIMARY if x >= 0 else '#ff4444' for x in y_values]

        # Add waterfall trace
        fig.add_trace(go.Waterfall(
            x=x_values,
            y=y_values,
            measure=['relative'] * len(y_values),
            text=[f'${x:,.2f}' for x in y_values],
            textposition='outside',
            connector={'line': {'color': self.theme.GRID_COLOR, 'width': 1}},
            increasing={'marker': {'color': self.theme.ACCENT_PRIMARY}},
            decreasing={'marker': {'color': '#ff4444'}},
            name='Daily P&L',
            hovertemplate='<b>Date:</b> %{x}<br><b>P&L:</b> $%{y:,.2f}<br><b>Running Total:</b> $%{base:,.2f}<extra></extra>'
        ))

        # Apply theme
        layout = self.theme.get_layout_template()
        layout.update({
            'title': title,
            'xaxis_title': 'Date',
            'yaxis_title': 'P&L Contribution',
            'showlegend': False
        })

        fig.update_layout(**layout)
        return fig
    
    def create_weekly_waterfall(self, weekly_data: pd.DataFrame, title: str) -> go.Figure:
        """
        Create weekly waterfall chart showing cumulative weekly progression.

        Args:
            weekly_data: DataFrame with weekly aggregated data
            title: Chart title

        Returns:
            Plotly figure object
        """
        if weekly_data.empty:
            # Return empty chart if no data
            fig = go.Figure()
            layout = self.theme.get_layout_template()
            layout.update({'title': title + ' (No Data)'})
            fig.update_layout(**layout)
            return fig

        # Determine the P&L column name - weekly data preserves original column names
        if 'Scaled_PnL' in weekly_data.columns:
            pnl_col = 'Scaled_PnL'
        elif 'PnL' in weekly_data.columns:
            pnl_col = 'PnL'
        else:
            # Fallback: use the second column (after Week)
            pnl_col = weekly_data.columns[1] if len(weekly_data.columns) > 1 else weekly_data.columns[0]

        pnl_values = weekly_data[pnl_col]

        fig = go.Figure()

        # Create waterfall chart
        fig.add_trace(go.Waterfall(
            x=weekly_data['Week_Start'],
            y=pnl_values,
            measure=['relative'] * len(pnl_values),
            text=[f'${x:,.2f}' for x in pnl_values],
            textposition='outside',
            connector={'line': {'color': self.theme.GRID_COLOR, 'width': 1}},
            increasing={'marker': {'color': self.theme.ACCENT_PRIMARY}},
            decreasing={'marker': {'color': '#ff4444'}},
            name='Weekly P&L',
            hovertemplate='<b>Week:</b> %{x}<br><b>P&L:</b> $%{y:,.2f}<extra></extra>'
        ))

        # Apply theme
        layout = self.theme.get_layout_template()
        layout.update({
            'title': title,
            'xaxis_title': 'Week',
            'yaxis_title': 'Weekly P&L Contribution',
            'showlegend': False
        })

        fig.update_layout(**layout)
        return fig
    
    def create_position_size_chart(self, data: pd.DataFrame) -> go.Figure:
        """
        Create chart showing position size over time.
        
        Args:
            data: DataFrame with scaled trading data
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Add position size line
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data['Position_Size'],
            mode='lines+markers',
            name='Position Size',
            line=dict(color=self.theme.ACCENT_SECONDARY, width=2),
            marker=dict(size=4, color=self.theme.ACCENT_PRIMARY),
            hovertemplate='<b>Date:</b> %{x}<br><b>Position Size:</b> %{y}<extra></extra>'
        ))
        
        # Apply theme
        layout = self.theme.get_layout_template()
        layout.update({
            'title': 'Position Size Over Time',
            'xaxis_title': 'Date',
            'yaxis_title': 'Position Size (Contracts)',
            'showlegend': False
        })
        
        fig.update_layout(**layout)
        return fig
    
    def create_comparison_chart(self, original_data: pd.DataFrame, scaled_data: pd.DataFrame, starting_capital: float = 100.0) -> go.Figure:
        """
        Create comparison chart showing original vs scaled equity curves.
        
        Args:
            original_data: DataFrame with original trading data
            scaled_data: DataFrame with scaled trading data
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Original cumulative P&L + starting capital
        original_cumulative = starting_capital + original_data['PnL'].cumsum()
        fig.add_trace(go.Scatter(
            x=original_data['Date'],
            y=original_cumulative,
            mode='lines',
            name='Original Strategy',
            line=dict(color=self.theme.TEXT_SECONDARY, width=2),
            hovertemplate='<b>Date:</b> %{x}<br><b>Account Balance:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # Scaled equity curve
        fig.add_trace(go.Scatter(
            x=scaled_data['Date'],
            y=scaled_data['EndingBR'],
            mode='lines',
            name='Scaled Strategy',
            line=dict(color=self.theme.ACCENT_PRIMARY, width=2),
            hovertemplate='<b>Date:</b> %{x}<br><b>Account Balance:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # Apply theme
        layout = self.theme.get_layout_template()
        layout.update({
            'title': 'Strategy Comparison: Original vs Scaled',
            'xaxis_title': 'Date',
            'yaxis_title': 'Value',
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**layout)
        return fig
