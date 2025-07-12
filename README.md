# MEWS to Google Sheets Sync

Automated data synchronization tool that connects MEWS Property Management System with Google Sheets. This integration enables automated extraction, transformation, and loading of hospitality data including reservations and paymentsinto organized Google Sheets for analysis and reporting.

## Key Features
- 🔄 Automated sync between MEWS and Google Sheets
- 📊 Real-time data extraction from MEWS API
- 📋 Organized data presentation in Google Sheets
- ⚡ Efficient data transformation and validation
- 🔍 Comprehensive error handling 
- 📅 Customizable sync scheduling

## Technical Overview
- Python-based implementation
- MEWS API integration
- Google Sheets API integration
- Modular and maintainable codebase
- Secure credential management

## Use Cases
- Daily reservation reports
- Payment tracking and reconciliation
- Occupancy analysis
- Revenue monitoring
- Custom reporting solutions

## Requirements
- Python 3.9+
- Google Cloud Project
- MEWS API credentials
- Google Sheets API enabled
- Required Python packages:
  - google-api-python-client
  - oauth2client
  - pandas
  - python-dotenv
  - requests

## Quick Start
```bash
# Clone repository
git clone [repository-url]

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

## Project Structure
```
mews-sheets-sync/
├── src/
│   ├── config.py          # Configuration management
│   ├── mews_client.py     # MEWS API integration
│   └── sheets_client.py   # Google Sheets integration
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## Contributing

### CONFIDENTIAL AND PROPRIETARY

This repository contains confidential and proprietary information about Nomading Camp.
Access is restricted to authorized personnel only.

## Access Requirements
- Manager approval needed
- Access is monitored

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
