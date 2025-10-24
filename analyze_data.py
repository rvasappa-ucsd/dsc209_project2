import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Load the data
df = pd.read_csv('CCRB-Complaint-Data_202007271729/allegations_202007271729.csv')

print("Dataset loaded successfully!")
print(f"Total records: {len(df)}")
print(f"Year range: {df['year_received'].min()} - {df['year_received'].max()}")

# Create substantiated flag
df['is_substantiated'] = df['board_disposition'].str.contains('Substantiated', na=False)

# Calculate yearly statistics
yearly_stats = df.groupby('year_received').agg({
    'complaint_id': 'count',
    'is_substantiated': ['sum', 'mean']
}).reset_index()

yearly_stats.columns = ['year', 'total_allegations', 'substantiated_count', 'substantiation_rate']
yearly_stats['substantiation_rate'] = yearly_stats['substantiation_rate'] * 100

# Filter to 2000-2019 (exclude 2020 incomplete data and very old data)
yearly_stats_filtered = yearly_stats[(yearly_stats['year'] >= 2000) & (yearly_stats['year'] <= 2019)]

print("\nYearly substantiation rates (2000-2019):")
print(yearly_stats_filtered[['year', 'substantiation_rate']].tail(10))

# Calculate by ethnicity
ethnicity_stats = df.groupby(['complainant_ethnicity', 'year_received']).agg({
    'complaint_id': 'count',
    'is_substantiated': 'mean'
}).reset_index()

# Calculate by allegation type
fado_stats = df.groupby(['fado_type', 'year_received']).agg({
    'complaint_id': 'count',
    'is_substantiated': 'mean'
}).reset_index()

# Export processed data
yearly_stats_filtered.to_json('yearly_stats.json', orient='records')
print("\nData analysis complete! Ready to create visualizations.")
