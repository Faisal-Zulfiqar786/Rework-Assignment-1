"""
# Assignment 1: Data Visualization

1. Import the required libraries: pandas and matplotlib.pyplot
2. Load the household power consumption dataset from UCI Machine Learning Repository and store it in the "data" variable.
3. Extract the data for the first week of January 2007 and store it in the "subset" variable.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
data = pd.read_csv(url, delimiter=";", parse_dates={"DateTime": ["Date", "Time"]}, infer_datetime_format=True, na_values=["?", "nan", "NA", "N/A"])
data = data.dropna() # Remove any rows with missing values

# Extract data for the first week of January 2007
start_date = "2007-01-01"
end_date = "2007-01-07"
subset = data[(data["DateTime"] >= start_date) & (data["DateTime"] <= end_date)]

"""4. Set the index of the dataframe to the datetime column.
5. Resample the data to daily frequency.
6. Extract the year 2007 from the data and store it in the "data_2007" variable.
7. Plot the submetering data for each day in 2007 using matplotlib.pyplot.
"""

# Set the index of the dataframe to the datetime column
data.set_index('DateTime', inplace=True)

# Resample the data to daily frequency
data_daily = data.resample('D').sum()

# Extract the year 2007 from the data
data_2007 = data_daily.loc['2007']

# Plot the submetering data for each day in 2007
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(data_2007['Sub_metering_1'], label='Sub_metering_1')
ax.plot(data_2007['Sub_metering_2'], label='Sub_metering_2')
ax.plot(data_2007['Sub_metering_3'], label='Sub_metering_3')
ax.set_title('Energy Consumption in 2007')
ax.set_xlabel('Date')
ax.set_ylabel('Energy Consumption (kWh)')
ax.legend()
plt.show()

"""8. Define a function "plot_multiple_lines" that takes a dataframe, x column, y columns, title, xlabel and ylabel as arguments and plots multiple line graphs using matplotlib.pyplot.
9. Call the "plot_multiple_lines" function to plot multiple line graphs showing energy consumption values over time for the "subset" dataframe.
"""

# Function to plot multiple line graphs
def plot_multiple_lines(df, x_col, y_cols, title, xlabel, ylabel):
    """
    Plots multiple line graphs given a dataframe and column names for x and y axes
    """
    plt.figure(figsize=(10,6))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for y_col in y_cols:
        plt.plot(df[x_col], df[y_col], label=y_col)
    plt.legend()
    plt.show()


# Plot multiple line graphs showing energy consumption values over time
plot_multiple_lines(subset, "DateTime", ["Global_active_power", "Global_reactive_power", "Voltage"], 
                    "Energy consumption values over time (Jan 1-7, 2007)", "Date and time", "Energy consumption (kW)")

"""10. Calculate the percentage of time different appliances were being used and store it in the "time_spent_on_appliances" variable.
11. Plot a pie chart showing the percentage of time different appliances were being used using matplotlib.pyplot.
12. Calculate the percentage of time power was consumed during different hours of the day and store it in the "time_spent_in_hours" variable.
13. Plot a pie chart showing the percentage of time power was consumed during different hours of the day using matplotlib.pyplot.
14. Group the data by day of the week and sum the power consumption.
15. Plot a pie chart showing the percentage of time power was consumed on different days of the week using matplotlib.pyplot.
"""

# Pie chart showing the percentage of time different appliances were being used (e.g., lighting, heating, refrigeration, etc.)
appliances = ["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]
time_spent_on_appliances = []
for appliance in appliances:
    time_spent_on_appliances.append(subset[appliance].sum())

plt.figure(figsize=(8,6))
plt.pie(time_spent_on_appliances, labels=appliances, autopct='%1.1f%%')
plt.title("Percentage of time different appliances were being used")
plt.legend()
plt.show()

# Pie chart showing the percentage of time power was consumed during different hours of the day (e.g., morning, afternoon, evening, night).
hour_ranges = [(0, 6), (6, 12), (12, 18), (18, 24)]
time_spent_in_hours = []
for hour_range in hour_ranges:
    time_spent_in_hours.append(subset[(subset["DateTime"].dt.hour >= hour_range[0]) & (subset["DateTime"].dt.hour < hour_range[1])]["Global_active_power"].sum())

plt.figure(figsize=(8,6))
plt.pie(time_spent_in_hours, labels=["12am-6am", "6am-12pm", "12pm-6pm", "6pm-12am"], autopct='%1.1f%%')
plt.title("Percentage of time power was consumed during different hours of the day")
plt.legend()
plt.show()

# Group the data by day of the week and sum the power consumption
grouped = subset.groupby(subset["DateTime"].dt.day_name())["Global_active_power"].sum()

# Plot the pie chart
plt.figure(figsize=(8, 6))
plt.pie(grouped, labels=grouped.index, autopct="%1.1f%%")
plt.title("Percentage of Time Power was Consumed on Different Days of the Week")
plt.legend(loc="best")
plt.show()

"""16. Define a function "plot_scatter" that takes a dataframe, x column, y column, title, xlabel and ylabel as arguments and plots a scatter plot using matplotlib.pyplot.
17. Call the "plot_scatter" function to plot a scatter plot for each feature separately against the output variable.6
"""

# Function to plot a scatter plot
def plot_scatter(df, x_col, y_col, title, xlabel, ylabel):
    """
    Plots a scatter plot given a dataframe and column names for x and y axes
    """
    plt.figure(figsize=(10,6))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.scatter(df[x_col], df[y_col])
    plt.show()

# Plot a scatter plot for each feature separately against the output variable
y_col = "Global_active_power"
for col in subset.columns:
    if col != "DateTime" and col != y_col:
        plot_scatter(subset, col, y_col, f"{col} vs. {y_col} (Jan 1-7, 2007)", col, y_col)