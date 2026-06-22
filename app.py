import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    df = pd.read_csv('meter_data.csv', thousands=',')
    return df


df = load_data()

st.title("📊 Customer Analytics Portal")

# --- 1. Sidebar Filters ---
st.sidebar.header("Filters")

# Segment selection with "Total" option
all_segments = ['Total'] + sorted(df['Customer Segment'].unique().tolist())
selected_segment = st.sidebar.selectbox("Select Segment:", all_segments)

# Meter Type filter
selected_meter = st.sidebar.multiselect(
    "Select Meter Model:",
    options=df['Meter Model'].unique(),
    default=df['Meter Model'].unique()
)

# Apply filters
if selected_segment == 'Total':
    filtered = df.copy()
else:
    filtered = df[df['Customer Segment'] == selected_segment]

filtered = filtered[filtered['Meter Model'].isin(selected_meter)]

# --- 2. Advanced Numerical Filters ---
st.sidebar.subheader("Advanced Ranges")
if st.sidebar.checkbox("Filter by Bill Range"):
    min_b = st.sidebar.number_input("Min Bill", value=0)
    max_b = st.sidebar.number_input("Max Bill", value=1000000)
    filtered = filtered[(filtered['Bill Amount'] >= min_b) & (filtered['Bill Amount'] <= max_b)]

# --- 3. Dashboard Display ---
count = len(filtered)
if count > 0:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Accounts", f"{count:,}")
        st.metric("Avg. Bill Amount", f"{filtered['Bill Amount'].sum() / count:,.0f} IQD")
    with col2:
        st.metric("Total Consumption", f"{filtered['Current Meter Consumption'].sum():,.0f} kWh")
        st.metric("Avg. Consumption", f"{filtered['Current Meter Consumption'].sum() / count:,.2f} kWh")

    st.dataframe(filtered, use_container_width=True)
else:
    st.warning("No data found with current filters.")