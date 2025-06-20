"""
Trading Strategy Scaling Calculator - Core Calculation Engine
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple, Dict, Any
import io


class StrategyCalculator:
    """Core calculation engine for trading strategy scaling with position sizing and compounding."""
    
    def __init__(self):
        self.original_data = None
        self.scaled_data = None
        self.max_loss = None
        self.starting_capital = None
        self.risk_percentage = None
    
    def parse_csv_data(self, csv_content: str) -> pd.DataFrame:
        """
        Parse CSV or tab-delimited data with flexible header detection and date parsing.
        Supports data copied from Excel, SSMS, or standard CSV files.

        Args:
            csv_content: Raw CSV or tab-delimited content as string

        Returns:
            DataFrame with Date and PnL columns
        """
        try:
            # Auto-detect delimiter (comma, tab, or semicolon)
            delimiter = ','
            if '\t' in csv_content and csv_content.count('\t') > csv_content.count(','):
                delimiter = '\t'
            elif ';' in csv_content and csv_content.count(';') > csv_content.count(','):
                delimiter = ';'

            # Try to read the data with detected delimiter
            df = pd.read_csv(io.StringIO(csv_content), delimiter=delimiter)
            
            # Remove any unnamed columns or empty rows
            df = df.dropna(how='all')
            
            # Find date and PnL columns (case insensitive, flexible naming)
            date_col = None
            pnl_col = None
            
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if any(keyword in col_lower for keyword in ['date', 'time', 'day']):
                    date_col = col
                elif any(keyword in col_lower for keyword in ['pnl', 'p&l', 'profit', 'loss', 'return', 'result']):
                    pnl_col = col
            
            if date_col is None or pnl_col is None:
                # If headers not found, assume first two columns are Date and PnL
                if len(df.columns) >= 2:
                    date_col = df.columns[0]
                    pnl_col = df.columns[1]
                else:
                    raise ValueError("Could not identify Date and PnL columns")
            
            # Create clean dataframe
            clean_df = pd.DataFrame({
                'Date': df[date_col],
                'PnL': pd.to_numeric(df[pnl_col], errors='coerce')
            })
            
            # Remove rows with invalid PnL values
            clean_df = clean_df.dropna(subset=['PnL'])
            
            # Parse dates
            clean_df['Date'] = pd.to_datetime(clean_df['Date'], errors='coerce')
            clean_df = clean_df.dropna(subset=['Date'])
            
            # Sort by date
            clean_df = clean_df.sort_values('Date').reset_index(drop=True)
            
            if len(clean_df) == 0:
                raise ValueError("No valid data rows found after parsing")
            
            return clean_df
            
        except Exception as e:
            raise ValueError(f"Error parsing CSV data: {str(e)}")
    
    def calculate_scaling(self, data: pd.DataFrame, starting_capital: float, risk_percentage: float) -> pd.DataFrame:
        """
        Apply position sizing and compounding to the trading data.
        
        Args:
            data: DataFrame with Date and PnL columns
            starting_capital: Initial capital amount
            risk_percentage: Risk percentage per trade (0.1 = 10%)
            
        Returns:
            DataFrame with scaling calculations
        """
        self.starting_capital = starting_capital
        self.risk_percentage = risk_percentage
        self.original_data = data.copy()
        
        # Calculate maximum loss (most negative PnL value)
        self.max_loss = abs(data['PnL'].min())
        
        if self.max_loss == 0:
            raise ValueError("Maximum loss is zero - cannot calculate position sizing")
        
        # Initialize result dataframe
        result = data.copy()
        result['StartingBR'] = 0.0
        result['Position_Size'] = 0
        result['Scaled_PnL'] = 0.0
        result['EndingBR'] = 0.0
        result['Cumulative_PnL'] = 0.0
        
        current_capital = starting_capital
        
        for i in range(len(result)):
            # Starting bankroll for this day
            result.loc[i, 'StartingBR'] = current_capital
            
            # Calculate position size: FLOOR((Current Capital × Risk %) ÷ Max Loss)
            position_size = int(np.floor((current_capital * risk_percentage) / self.max_loss))
            result.loc[i, 'Position_Size'] = position_size
            
            # Calculate scaled P&L
            scaled_pnl = result.loc[i, 'PnL'] * position_size
            result.loc[i, 'Scaled_PnL'] = scaled_pnl
            
            # Update capital
            current_capital += scaled_pnl
            result.loc[i, 'EndingBR'] = current_capital
            
            # Calculate cumulative P&L from starting capital
            result.loc[i, 'Cumulative_PnL'] = current_capital - starting_capital
        
        self.scaled_data = result
        return result
    
    def calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics for both original and scaled data."""
        if self.original_data is None or self.scaled_data is None:
            return {}
        
        # Original data metrics
        original_total_pnl = self.original_data['PnL'].sum()
        original_wins = (self.original_data['PnL'] > 0).sum()
        original_losses = (self.original_data['PnL'] < 0).sum()
        original_win_rate = original_wins / len(self.original_data) if len(self.original_data) > 0 else 0
        original_avg_win = self.original_data[self.original_data['PnL'] > 0]['PnL'].mean() if original_wins > 0 else 0
        original_avg_loss = self.original_data[self.original_data['PnL'] < 0]['PnL'].mean() if original_losses > 0 else 0
        
        # Calculate original drawdown
        original_cumsum = self.original_data['PnL'].cumsum()
        original_running_max = original_cumsum.expanding().max()
        original_drawdown = original_cumsum - original_running_max
        original_max_drawdown = original_drawdown.min()
        
        # Scaled data metrics
        scaled_total_pnl = self.scaled_data['Scaled_PnL'].sum()
        scaled_final_capital = self.scaled_data['EndingBR'].iloc[-1]
        scaled_total_return_pct = (scaled_final_capital - self.starting_capital) / self.starting_capital * 100
        
        scaled_wins = (self.scaled_data['Scaled_PnL'] > 0).sum()
        scaled_losses = (self.scaled_data['Scaled_PnL'] < 0).sum()
        scaled_win_rate = scaled_wins / len(self.scaled_data) if len(self.scaled_data) > 0 else 0
        scaled_avg_win = self.scaled_data[self.scaled_data['Scaled_PnL'] > 0]['Scaled_PnL'].mean() if scaled_wins > 0 else 0
        scaled_avg_loss = self.scaled_data[self.scaled_data['Scaled_PnL'] < 0]['Scaled_PnL'].mean() if scaled_losses > 0 else 0
        
        # Calculate scaled drawdown
        scaled_running_max = self.scaled_data['EndingBR'].expanding().max()
        scaled_drawdown = self.scaled_data['EndingBR'] - scaled_running_max
        scaled_max_drawdown = scaled_drawdown.min()
        scaled_max_drawdown_pct = (scaled_max_drawdown / scaled_running_max.max() * 100) if scaled_running_max.max() > 0 else 0
        
        # Position sizing metrics
        max_position_size = self.scaled_data['Position_Size'].max()
        avg_position_size = self.scaled_data['Position_Size'].mean()
        min_position_size = self.scaled_data['Position_Size'].min()
        
        return {
            'original': {
                'total_pnl': original_total_pnl,
                'win_rate': original_win_rate,
                'avg_win': original_avg_win,
                'avg_loss': original_avg_loss,
                'max_drawdown': original_max_drawdown,
                'total_trades': len(self.original_data)
            },
            'scaled': {
                'starting_capital': self.starting_capital,
                'final_capital': scaled_final_capital,
                'total_pnl': scaled_total_pnl,
                'total_return_pct': scaled_total_return_pct,
                'win_rate': scaled_win_rate,
                'avg_win': scaled_avg_win,
                'avg_loss': scaled_avg_loss,
                'max_drawdown': scaled_max_drawdown,
                'max_drawdown_pct': scaled_max_drawdown_pct,
                'total_trades': len(self.scaled_data)
            },
            'position_sizing': {
                'max_loss_used': self.max_loss,
                'risk_percentage': self.risk_percentage,
                'max_position_size': max_position_size,
                'avg_position_size': avg_position_size,
                'min_position_size': min_position_size
            }
        }
    
    def get_weekly_data(self, data_type: str = 'scaled') -> pd.DataFrame:
        """
        Aggregate data by week for weekly waterfall charts.
        
        Args:
            data_type: 'original' or 'scaled'
            
        Returns:
            DataFrame with weekly aggregated data
        """
        if data_type == 'original' and self.original_data is not None:
            df = self.original_data.copy()
            pnl_col = 'PnL'
        elif data_type == 'scaled' and self.scaled_data is not None:
            df = self.scaled_data.copy()
            pnl_col = 'Scaled_PnL'
        else:
            return pd.DataFrame()
        
        # Add week information
        df['Week'] = df['Date'].dt.to_period('W')
        
        # Group by week and sum P&L
        weekly = df.groupby('Week')[pnl_col].sum().reset_index()
        weekly['Week_Start'] = weekly['Week'].dt.start_time
        
        return weekly
