# COVID-19 TREND TRACKING
![CI](https://github.com/merytpeters/covid19-trend-tracker-west-africa/actions/workflows/ci.yml/badge.svg)

## Overview
COVID-19 Trend Tracker (West Africa Edition) is a web application for tracking and visualizing COVID-19 trends across West African countries. It provides up-to-date statistics, charts, and insights to help users understand the pandemic's impact in the region.

## Features
- Real-time COVID-19 data for West African countries
- Interactive charts and visualizations
- RESTful API built with FastAPI
- Modern frontend (Typescript)
- Continuous integration with GitHub Actions

## Project Structure
- `server/` — FastAPI backend, API, and data processing
- `client/` — Frontend application
- `docs/` — Documentation and resources

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js & npm (for frontend)

### Backend Setup
```bash
cd server
python -m venv covid-venv
source covid-venv/bin/activate
pip install -r requirements.txt
# or use pyproject.toml with pip or poetry
```

### Frontend Setup
```bash
cd client/covid-19-trend-tracker
npm install
npm start
```

## Usage
- Start the backend server: `uvicorn main:app --reload`
- Access the frontend at `http://localhost:3000`

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License
