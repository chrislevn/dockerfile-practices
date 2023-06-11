# app.py
from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Read the data file
data = pd.read_csv('./layoffs.csv')

@app.route('/')
def home():
    industry_df = data.groupby('industry').sum()['total_laid_off']
    fig = px.bar(industry_df.sort_values(ascending=False), title='Layoffs v/s Industry', text_auto=True)

    # Convert the plotly figure to a PNG image
    image_stream = io.BytesIO()
    fig.write_image(image_stream, format='png')
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return render_template('index.html', chart_image=encoded_image)

if __name__ == '__main__':
    load_dotenv()
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
