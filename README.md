# MEWS to Google Sheets Sync

Automated data synchronization tool that connects MEWS Property Management System with Google Sheets. This integration enables automated extraction, transformation, and loading of hospitality data including reservations and payments into organized Google Sheets for analysis and reporting.

## 🚀 Key Features
- 🔄 Automated sync between MEWS and Google Sheets
- 📊 Real-time data extraction from MEWS API
- 📋 Organized data presentation in Google Sheets
- ⚡ Efficient data transformation and validation
- 🔍 Comprehensive error handling with retry logic
- 📅 Customizable sync scheduling
- 🏗️ Modular and maintainable architecture

## 🏗️ Technical Overview
- **Python-based implementation** with type hints
- **Modular architecture** following separation of concerns
- **MEWS API integration** with robust error handling
- **Google Sheets API integration**
- **Secure credential management** via environment variables
- **Rate limiting protection** with automatic retries

## 📁 Project Structure
```
Automatizacion/
├── config.py                    # 🔧 Centralized configuration
├── main.py                      # 🚀 Main entry point
├── services/
│   └── report_generator.py      # 🎯 Main orchestrator
├── integrations/
│   └── mews/
│       ├── client.py            # 🌐 HTTP client
│       └── endpoints.py         # 📡 API endpoints
├── data/
│   ├── cleaners.py              # 🧹 Data validation & cleaning
│   └── transformers.py          # 🔄 Data transformation
├── reports/
│   └── sheet_writer.py          # 📊 Excel report generation
├── util/
│   └── utils.py                 # 🛠️ Common utilities
├── example_usage.py             # 📚 Usage examples
├── MIGRATION_GUIDE.md           # 📖 Migration documentation
└── sheets_client.py             # 📄 Legacy reference
```

## 🎯 Use Cases
- Daily reservation reports
- Payment tracking and reconciliation
- Occupancy analysis
- Revenue monitoring
- Custom reporting solutions

## 📋 Requirements
- Python 3.9+
- Google Cloud Project
- MEWS API credentials
- Google Sheets API enabled
- Required Python packages (see `requirements.txt`):
  - google-api-python-client
  - oauth2client
  - pandas
  - python-dotenv
  - requests
  - deep-translator
  - openpyxl

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Clone repository
git clone [repository-url]
cd Automatizacion

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
MEWS_API_BASE_URL=https://api.mews-demo.com/api/connector/v1
MEWS_CLIENT_TOKEN=your_client_token
MEWS_ACCESS_TOKEN=your_access_token
```

### 3. Run the Application
```bash
# Basic usage
python main.py

# Or use the example
python example_usage.py
```

## 📚 Usage Examples

### Basic Usage
```python
from services.report_generator import ReportGenerator
from config import CONFIG

# Create generator
generator = ReportGenerator(CONFIG)

# Generate report
success = generator.generate()
```

### Custom Configuration
```python
custom_config = CONFIG.copy()
custom_config.update({
    "START_DATE": "2025-01-01T00:00:00Z",
    "END_DATE": "2025-01-31T23:59:59Z",
    "SHEET_OUTPUT_PATH": "custom_report.xlsx"
})

generator = ReportGenerator(custom_config)
generator.generate()
```

## 🔧 Configuration

The application uses a centralized configuration system in `config.py`:

```python
CONFIG = {
    "API_BASE_URL": "https://api.mews-demo.com/api/connector/v1",
    "CLIENT_TOKEN": "your_client_token",
    "ACCESS_TOKEN": "your_access_token",
    "START_DATE": "2025-05-06T01:00:00Z",
    "END_DATE": "2025-05-08T23:00:00Z",
    "SHEET_OUTPUT_PATH": "reservas_mews.xlsx",
    "LIMITATION_COUNT": 30,
    "MAX_RETRIES": 5,
    "RATE_LIMIT_DELAY": 0.5
}
```

## 🏗️ Architecture Overview

### Services Layer
- **`ReportGenerator`**: Main orchestrator that coordinates the entire process

### Integrations Layer
- **`MewsClient`**: HTTP client for MEWS API communication
- **`endpoints.py`**: Specific API endpoint implementations

### Data Layer
- **`DataCleaner`**: Validates and cleans raw data
- **`ReservationTransformer`**: Transforms data to report format

### Reports Layer
- **`SheetWriter`**: Generates formatted Excel reports

### Utilities
- **`utils.py`**: Common utilities for HTTP requests, translations, and date handling

## 🔄 Migration from Legacy Code

If you're migrating from the old `sheets_client.py`:

1. **Read the migration guide**: `MIGRATION_GUIDE.md`
2. **Use the new architecture**: Follow the examples in `example_usage.py`
3. **Update your configuration**: Use the new `config.py` system
4. **Test thoroughly**: Ensure all functionality works as expected

## 🐛 Troubleshooting

### Common Issues
1. **API Connection Errors**: Check your tokens and network connection
2. **Rate Limiting**: The system automatically handles rate limits with retries
3. **Missing Dependencies**: Ensure all packages in `requirements.txt` are installed
4. **Configuration Errors**: Verify your `.env` file is properly configured

### Debug Mode
Enable debug logging by setting environment variables:
```bash
export DEBUG=true
python main.py
```

## 🤝 Contributing

### CONFIDENTIAL AND PROPRIETARY

This repository contains confidential and proprietary information about Nomading Camp.
Access is restricted to authorized personnel only.

### Development Guidelines
1. Follow the established architecture patterns
2. Add type hints to all functions
3. Include comprehensive error handling
4. Write tests for new functionality
5. Update documentation as needed

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support
For technical support or questions:
- Check the `MIGRATION_GUIDE.md` for migration help
- Review `example_usage.py` for usage examples
- Consult the documentation in each module
