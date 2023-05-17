import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import calendar

# Load the data
ghcn = pd.read_csv("data/GHCN_USC00045532_USW00023257.csv", parse_dates=['date'])

year_to_plot = ghcn['year'].max()
last_date = ghcn['date'].max()

# Extract data for the current year
this_year = ghcn[ghcn['year'] == year_to_plot].reset_index(drop=True)

# Calculate the daily summary statistics for all years except the current year
daily_summary_stats = ghcn[ghcn['year'] != year_to_plot][['day_of_year', 'PRCP', 'TMAX', 'TMIN']] \
    .melt(id_vars='day_of_year', var_name='name', value_name='value') \
    .groupby(['day_of_year', 'name']) \
    .agg(max_value=('value', 'max'),
         min_value=('value', 'min'),
         x5=('value', lambda x: np.nanquantile(x, 0.05)),
         x20=('value', lambda x: np.nanquantile(x, 0.2)),
         x40=('value', lambda x: np.nanquantile(x, 0.4)),
         x60=('value', lambda x: np.nanquantile(x, 0.6)),
         x80=('value', lambda x: np.nanquantile(x, 0.8)),
         x95=('value', lambda x: np.nanquantile(x, 0.95))) \
    .reset_index()


# Find the day of the year for the start of each month
month_breaks = (ghcn[ghcn['year'] == 2019]
    .groupby('month', as_index=False)
    .apply(lambda x: x[x['day_of_year'] == x['day_of_year'].min()])
    .loc[:, ['month', 'day_of_year']]
    .assign(month_name=lambda x: x['month'].apply(lambda y: calendar.month_abbr[y])))

# Extract records set this year
record_status_this_year = this_year[['day_of_year', 'PRCP', 'TMAX', 'TMIN']] \
    .melt(id_vars='day_of_year', var_name='name', value_name='this_year') \
    .merge(daily_summary_stats.drop(columns=['x5', 'x20', 'x40', 'x60', 'x80', 'x95']), on=['day_of_year', 'name']) \
    .assign(record_status=lambda df: np.where(df['this_year'] > df['max_value'], 'max', np.where(df['this_year'] < df['min_value'], 'min', 'none'))) \
    .query("record_status != 'none' & name == 'TMAX'")

# Plot the maximum temperature graph
fig, ax = plt.subplots(figsize=(8, 4))

max_temp = daily_summary_stats[daily_summary_stats['name'] == 'TMAX']

# Plot the ribbons for various percentiles
ax.fill_between(max_temp['day_of_year'], max_temp['min_value'], max_temp['x5'], color='#FDDBC7')
ax.fill_between(max_temp['day_of_year'], max_temp['x5'], max_temp['x20'], color='#F4A582')
ax.fill_between(max_temp['day_of_year'], max_temp['x20'], max_temp['x40'], color='#D6604D')
ax.fill_between(max_temp['day_of_year'], max_temp['x40'], max_temp['x60'], color='#B2182B')
ax.fill_between(max_temp['day_of_year'], max_temp['x60'], max_temp['x80'], color='#D6604D')
ax.fill_between(max_temp['day_of_year'], max_temp['x80'], max_temp['x95'], color='#F4A582')
ax.fill_between(max_temp['day_of_year'], max_temp['x95'], max_temp['max_value'], color='#FDDBC7')

# Plot the line for this year's data
ax.plot(this_year['day_of_year'], this_year['TMAX'], color='black', alpha=0.75, label=f'{year_to_plot}')

# Plot the scatter for record-setting temperatures
for record_type, color in zip(['max', 'min'], ['#C41305', '#0091D0']):
    record_data = record_status_this_year[record_status_this_year['record_status'] == record_type]
    ax.scatter(record_data['day_of_year'], record_data['this_year'], color=color, marker='o', label=f'{record_type.capitalize()} Temperature Record')

# Set axis labels and title
ax.set_xlabel('Day of Year')
ax.set_ylabel('Maximum Temperature (°F)')
ax.set_title(f'Maximum Temperature for {year_to_plot} (through {last_date.date()})\nRecord-setting Temperatures Highlighted')

# Set x-axis tick marks and labels
# xtick_dates = [pd.to_datetime(f'{year_to_plot}-{i}-01') for i in month_breaks['month']]
# xtick_labels = month_breaks['month_name'].tolist()
# ax.set_xticks(mdates.date2num(xtick_dates))
# ax.set_xticklabels(xtick_labels)
ax.set_xticks(month_breaks['day_of_year'])
ax.set_xticklabels(month_breaks['month_name'])

# Set the y-axis tick formatter to include degree symbol
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d°'))

# Add legend
ax.legend(loc='upper left')
ax.set_xlim(0, 366)
ax.set_ylim(10,120)

# Add grid lines
plt.grid(axis = 'x', color = 'black', linestyle = '--', linewidth = 0.5)
plt.grid(axis = 'y', color = 'grey', linewidth = 0.5)

# Show plot
plt.show()

# Save plot
fig.savefig("graphs/DailyHighTemp_USC00045532_USW00023257.png", dpi=300, bbox_inches='tight')

# Close plot
plt.close()
