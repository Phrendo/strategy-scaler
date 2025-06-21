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
2. Set up the environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Running the Application

#### Development Mode
```bash
source .venv/bin/activate
streamlit run app.py
```

#### Production Deployment (Ubuntu with nginx)

1. **Install system dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip nginx
   ```

2. **Create a systemd service** (`/etc/systemd/system/strategy-scaler.service`):
   ```ini
   [Unit]
   Description=Trading Strategy Scaling Calculator
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/path/to/strategy-scaler
   Environment=PATH=/path/to/strategy-scaler/.venv/bin
   ExecStart=/path/to/strategy-scaler/.venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=multi-user.target
   ```

   **Note:** Replace `/path/to/strategy-scaler` with the actual path to your application directory.

3. **Configure nginx** (`/etc/nginx/sites-available/strategy-scaler`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # Replace with your domain

       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

4. **Configure firewall (if enabled):**
   ```bash
   sudo ufw allow 'Nginx Full'
   sudo ufw allow ssh
   sudo ufw --force enable
   ```

5. **Enable and start services:**
   ```bash
   # Enable nginx site
   sudo ln -s /etc/nginx/sites-available/strategy-scaler /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx

   # Enable and start the application
   sudo systemctl enable strategy-scaler
   sudo systemctl start strategy-scaler
   sudo systemctl status strategy-scaler
   ```

#### Service Management
```bash
# Check status
sudo systemctl status strategy-scaler

# View logs
sudo journalctl -u strategy-scaler -f

# Restart service
sudo systemctl restart strategy-scaler

# Stop service
sudo systemctl stop strategy-scaler
```

#### SSL/HTTPS Configuration (Recommended for Production)

For production deployments, configure SSL using Let's Encrypt:

1. **Install Certbot:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain SSL certificate:**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. **Auto-renewal:**
   ```bash
   sudo crontab -e
   # Add this line:
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

The nginx configuration will be automatically updated to redirect HTTP to HTTPS.

#### Troubleshooting

**Service won't start:**
```bash
# Check service logs
sudo journalctl -u strategy-scaler -n 50

# Check if port is in use
sudo netstat -tlnp | grep :8501

# Verify virtual environment
ls -la /path/to/strategy-scaler/.venv/bin/
```

**nginx errors:**
```bash
# Test nginx configuration
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

**Permission issues:**
```bash
# Ensure correct ownership
sudo chown -R www-data:www-data /path/to/strategy-scaler
```

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

Run tests with:
```bash
source .venv/bin/activate
python test_calculator.py
```

## Dependencies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **Plotly**: Interactive data visualization

## License

This project is provided as-is for educational and analysis purposes.

## Support

For issues or questions, refer to the test suite and sample data for expected formats and behavior.
