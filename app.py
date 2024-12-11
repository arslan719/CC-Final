
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    # Replace with your actual file loading mechanism
    data = pd.read_csv('clean_data.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()

# Sidebar for filters
st.sidebar.header("Filters")
state = st.sidebar.selectbox("Select State", data['State'].unique())
county = st.sidebar.selectbox("Select County", data[data['State'] == state]['County'].unique())
start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max())
analysis_type = st.sidebar.selectbox("Select Analysis", [
    "Linegraph Overview",
    "Best/Worst 5 States",
    "Rolling Average by Categories",
    "Correlation Heatmap Between Metrics",
    "Year-over-Year Comparison",
    "Daily Change Percentage",
    "Category Comparison"
])

filtered_data = data[(data['State'] == state) & (data['County'] == county) &
                     (data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

# Dashboard Title
st.title("Human Mobility Dashboard")

if analysis_type == "Linegraph Overview":
    st.header("Linegraph Overview of Change in Moblility")
    metric = st.selectbox("Select a Metric to Analyze", [
        'Retail_recreation', 'Grocery_Pharmacy', 'Parks', 'Transit', 'Workplace', 'Residential'
    ])
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Date'], filtered_data[metric], label=metric)
    plt.xlabel('Date')
    plt.ylabel(metric)
    plt.title(f'{metric} Over Time in {county}, {state}')
    plt.legend()
    st.pyplot(plt)

elif analysis_type == "Best/Worst 5 States":
    st.header("Best/Worst 5 States in Complience with Policies")
    metric = st.selectbox("Select a Metric", [
        'Retail_recreation', 'Grocery_Pharmacy', 'Parks', 'Transit', 'Workplace', 'Residential'
    ])
    state_summary = data.groupby('State')[metric].mean().sort_values(ascending=False)
    top_5 = state_summary.head(5)
    bottom_5 = state_summary.tail(5)
    st.subheader("Worst 5 States")
    st.bar_chart(top_5)
    st.subheader("Best 5 States")
    st.bar_chart(bottom_5)

elif analysis_type == "Rolling Average by Categories":
    st.header("Rolling Average by Categories")
    metric = st.selectbox("Select a Metric", [
        'Retail_recreation', 'Grocery_Pharmacy', 'Parks', 'Transit', 'Workplace', 'Residential'
    ])
    window_size = st.slider("Select Rolling Window Size", min_value=3, max_value=30, value=7)
    filtered_data[f'{metric}_Rolling'] = filtered_data[metric].rolling(window=window_size).mean()
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Date'], filtered_data[f'{metric}_Rolling'], label=f'{metric} Rolling Avg')
    plt.xlabel('Date')
    plt.ylabel(f'{metric} Rolling Avg')
    plt.title(f'{metric} Rolling Average ({window_size}-day) in {county}, {state}')
    plt.legend()
    st.pyplot(plt)

elif analysis_type == "Correlation Heatmap Between Metrics":
    st.header("Correlation of Categories")
    metrics = ['Retail_recreation', 'Grocery_Pharmacy', 'Parks', 'Transit', 'Workplace', 'Residential']
    correlation_data = filtered_data[metrics].corr()
    plt.figure(figsize=(10, 5))
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Heatmap")
    st.pyplot(plt)

elif analysis_type == "Year-over-Year Comparison":
    st.header("Year-over-Year Comparison")
    metric = st.selectbox("Select a Metric", [
        'Retail_recreation', 'Grocery_Pharmacy', 'Parks', 'Transit', 'Workplace', 'Residential'
    ])
    filtered_data['Year'] = filtered_data['Date'].dt.year
    yearly_summary = filtered_data.groupby('Year')[metric].mean()
    plt.figure(figsize=(10, 5))
    plt.bar(yearly_summary.index, yearly_summary.values)
    plt.xlabel('Year')
    plt.ylabel(metric)
    plt.title(f'Year-over-Year Comparison of {metric} in {county}, {state}')
    st.pyplot(plt)

elif analysis_type == "Daily Change Percentage":
    st.header("Daily Change Percentage")
    metric = st.selectbox("Select a Metric", [
        'Retail_recreation', 'Grocery_Pharmacy', 'Parks', 'Transit', 'Workplace', 'Residential'
    ])
    filtered_data['Daily_Change'] = filtered_data[metric].pct_change() * 100
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Date'], filtered_data['Daily_Change'], label=f'{metric} Daily Change (%)')
    plt.xlabel('Date')
    plt.ylabel('Daily Change (%)')
    plt.title(f'Daily Change Percentage of {metric} in {county}, {state}')
    plt.legend()
    st.pyplot(plt)

elif analysis_type == "Category Comparison":
    st.header("Category Comparison")
    categories = st.multiselect("Select Categories to Compare", [
        'Retail_recreation', 'Grocery_Pharmacy', 'Parks', 'Transit', 'Workplace', 'Residential'
    ])
    if len(categories) >= 2:
        plt.figure(figsize=(10, 5))
        for category in categories:
            plt.plot(filtered_data['Date'], filtered_data[category], label=category)
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.title(f'Category Comparison in {county}, {state}')
        plt.legend()
        st.pyplot(plt)
    else:
        st.write("Please select at least two categories for comparison.")
