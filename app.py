from flask import Flask, render_template
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

app = Flask(__name__)

def get_db_data():
    """Query the games table from the database"""
    conn = sqlite3.connect('browns_data.db')
    df = pd.read_sql_query("SELECT * FROM games", conn)
    conn.close()
    return df

@app.route('/')
def index():
    """Home page with overview statistics"""
    df = get_db_data()
    
    # Calculate accuracy metrics
    browns_correct = (df['12_Percent_Score'] > df['Opp_12_Percent_Score']) == (df['Win_Loss_Bool'] == 1)
    accuracy = (browns_correct.sum() / len(df)) * 100
    
    browns_wins = df['Win_Loss_Bool'].sum()
    browns_losses = len(df) - browns_wins
    
    stats = {
        'total_games': len(df),
        'browns_wins': int(browns_wins),
        'browns_losses': int(browns_losses),
        'accuracy': f"{accuracy:.1f}%"
    }
    
    return render_template('index.html', stats=stats)

@app.route('/api/scatter-plot')
def scatter_plot():
    """Scatter plot comparing Browns vs Opponent 12% scores"""
    df = get_db_data()
    
    # Color code by win/loss
    colors = ['red' if w == 0 else 'green' for w in df['Win_Loss_Bool']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['12_Percent_Score'],
        y=df['Opp_12_Percent_Score'],
        mode='markers',
        marker=dict(
            size=10,
            color=colors,
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        text=[f"Week {w}<br>vs {o}<br>Result: {r}" 
              for w, o, r in zip(df['Week'], df['Opponent'], df['Result'])],
        hovertemplate='<b>%{text}</b><br>Browns 12%: %{x:.2f}<br>Opponent 12%: %{y:.2f}<extra></extra>'
    ))
    
    # Add diagonal reference line (equal scores)
    max_val = max(df['12_Percent_Score'].max(), df['Opp_12_Percent_Score'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(dash='dash', color='gray'),
        name='Equal Score Line',
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title='Browns 12% Score vs Opponent 12% Score<br><sub>Green = Win | Red = Loss</sub>',
        xaxis_title='Browns 12% Score',
        yaxis_title='Opponent 12% Score',
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240,0.5)',
        height=600
    )
    
    return json.loads(fig.to_json())

@app.route('/api/accuracy-chart')
def accuracy_chart():
    """Chart showing prediction accuracy"""
    df = get_db_data()
    
    # Check if higher 12% score correlates with wins
    browns_higher = df['12_Percent_Score'] > df['Opp_12_Percent_Score']
    browns_won = df['Win_Loss_Bool'] == 1
    
    # Calculate accuracy for when Browns had higher score
    correct_higher = (browns_higher & browns_won) | (~browns_higher & ~browns_won)
    accuracy_higher = (correct_higher.sum() / len(df)) * 100
    
    # Breakdown
    browns_predicted_win = browns_higher.sum()
    browns_actual_win = browns_won.sum()
    correct_predictions = correct_higher.sum()
    
    fig = go.Figure()
    
    categories = ['Predicted Wins', 'Actual Wins', 'Correct Predictions']
    values = [browns_predicted_win, browns_actual_win, correct_predictions]
    colors_chart = ['#1f77b4', '#2ca02c', '#ff7f0e']
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker=dict(color=colors_chart),
        text=values,
        textposition='auto'
    ))
    
    fig.update_layout(
        title=f'12% Rule Accuracy: {accuracy_higher:.1f}%<br><sub>Games where higher 12% score predicted the winner</sub>',
        yaxis_title='Number of Games',
        hovermode='x unified',
        height=500,
        showlegend=False
    )
    
    return json.loads(fig.to_json())

@app.route('/api/weekly-comparison')
def weekly_comparison():
    """Week-by-week comparison of scores and results"""
    df = get_db_data()
    
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{}]]
    )
    
    # Add Browns scores
    fig.add_trace(go.Bar(
        x=df['Week'],
        y=df['12_Percent_Score'],
        name='Browns 12% Score',
        marker_color='#8B4513',
        hovertemplate='Week %{x}<br>Browns: %{y:.2f}<extra></extra>'
    ))
    
    # Add Opponent scores
    fig.add_trace(go.Bar(
        x=df['Week'],
        y=df['Opp_12_Percent_Score'],
        name='Opponent 12% Score',
        marker_color='#FFB6C1',
        hovertemplate='Week %{x}<br>Opponent: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Weekly 12% Score Comparison',
        xaxis_title='Week',
        yaxis_title='12% Score',
        barmode='group',
        hovermode='x unified',
        height=500
    )
    
    return json.loads(fig.to_json())

@app.route('/api/score-distribution')
def score_distribution():
    """Distribution of 12% scores for wins vs losses"""
    df = get_db_data()
    
    wins_df = df[df['Win_Loss_Bool'] == 1]
    losses_df = df[df['Win_Loss_Bool'] == 0]
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=wins_df['12_Percent_Score'],
        name='Wins',
        marker_color='green',
        opacity=0.7,
        nbinsx=8
    ))
    
    fig.add_trace(go.Histogram(
        x=losses_df['12_Percent_Score'],
        name='Losses',
        marker_color='red',
        opacity=0.7,
        nbinsx=8
    ))
    
    fig.update_layout(
        title='Distribution of Browns 12% Scores by Outcome',
        xaxis_title='12% Score',
        yaxis_title='Frequency',
        barmode='overlay',
        hovermode='x unified',
        height=500
    )
    
    return json.loads(fig.to_json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
