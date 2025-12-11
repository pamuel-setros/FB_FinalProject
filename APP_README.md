# 12% Rule Analysis Web App

A Flask-based interactive web application that visualizes the accuracy of the "12% Rule" for predicting Cleveland Browns game outcomes.

## Features

The web app includes four interactive visualizations:

1. **Scatter Plot Analysis** - Compares Browns 12% Score vs Opponent 12% Score
   - Green dots = Wins, Red dots = Losses
   - Shows correlation between score differential and game outcome
   - Includes reference line for equal scores

2. **Prediction Accuracy** - Shows how well the 12% rule predicts winners
   - Compares predicted wins (based on higher 12% score) vs actual wins
   - Displays overall accuracy percentage

3. **Weekly Comparison** - Bar chart of week-by-week score matchups
   - Allows visual tracking of score changes throughout the season
   - Easy identification of dominant and weak performances

4. **Score Distribution** - Histogram of 12% scores by game outcome
   - Shows distribution of Browns scores in wins vs losses
   - Helps identify optimal score ranges for winning

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

### 3. Open in Browser
Navigate to `http://localhost:5000` to view the interactive dashboard

## Data Source

The app uses data from `browns_data.db`, an SQLite database containing:
- **games table**: Merged data with Browns and opponent statistics
- **browns_stats table**: Browns game statistics
- **opponents_stats table**: Opponent game statistics

## Understanding the 12% Rule

The 12% Rule is a metric designed to predict game outcomes based on key performance factors including:
- Sacks
- Turnovers
- Penalties
- Dropped passes
- Critical errors

A higher 12% score indicates better team performance and is expected to correlate with winning games.

## Analysis Insights

The application provides visual evidence of:
- How often higher 12% scores predict wins
- Whether the rule is consistent across the season
- Performance trends and outliers
- Relative performance vs opponents
