import streamlit as st
import pandas as pd
import plotly.express as px

# Site Config
st.set_page_config(
    page_title="Group 16: Prototype Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
        [data-testid="stMetricValue"] { color: #fabd2f; }
        [data-testid="stMetricDelta"] { color: #fb4934; }
        [data-testid="stSidebar"] {
            min-width: 80px; max-width: 80px;
            transition: all 0.2s ease-in-out;
            background-color: #3c3836 !important;
        }
        [data-testid="stSidebar"]:hover { min-width: 320px; max-width: 320px; }
        [data-testid="stSidebar"] .element-container, [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stRadio, [data-testid="stSidebar"] .stCheckbox,
        [data-testid="stSidebar"] .stMultiSelect { opacity: 0; transition: opacity 0.2s ease-in-out; }
        [data-testid="stSidebar"]:hover .element-container, [data-testid="stSidebar"]:hover .stMarkdown,
        [data-testid="stSidebar"]:hover .stRadio, [data-testid="stSidebar"]:hover .stCheckbox,
        [data-testid="stSidebar"]:hover .stMultiSelect { opacity: 1; }

        ::-webkit-scrollbar {
            display: none;
        }
        html {
            scrollbar-width: none;
        }
        [data-testid="stSidebarUserContent"] {
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
        [data-testid="stSidebarUserContent"]::-webkit-scrollbar {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_parquet('part-00000-cb8e687c-aeb8-4716-8c68-5061bd34f1b3-c000.snappy.parquet')
    data['congestion_index'] = data['total_traffic_volume'] / data['avg_road_length_km']
    return data

df = load_data()

# Sidebar
st.sidebar.markdown("## Group 16 Prototype")
st.sidebar.title("Control Panel")
page = st.sidebar.radio("Analyses", ["Overview", "Authority Analysis", "Trends", "System Details"])

authorities = sorted(df['local_authority_name'].unique().tolist())
select_all = st.sidebar.checkbox("Select all Authorities")
if select_all:
    selected_auth = st.sidebar.multiselect("Authorities", options=authorities, default=authorities)
else:
    selected_auth = st.sidebar.multiselect("Authorities", options=authorities)

# Page Logic
if page == "Overview":
    st.title("Traffic Density Analysis")
    years = sorted(df['year'].unique())
    target_year = st.select_slider("Select Monitoring Year", options=years, value=max(years))
    current_df = df[df['year'] == target_year]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Regional Volume", f"{current_df['total_traffic_volume'].sum():,.0f}")
    col2.metric("Mean Congestion Index", f"{current_df['congestion_index'].mean():.2f}")
    col3.metric("Monitored Nodes", f"{len(current_df)}")

    fig_heat = px.density_heatmap(current_df, x="avg_road_length_km", y="total_traffic_volume", 
                                  template="plotly_dark", color_continuous_scale="Viridis")
    st.plotly_chart(fig_heat, use_container_width=True)

elif page == "Trends":
    st.title("Longitudinal Traffic Trends")
    trend_df = df[df['local_authority_name'].isin(selected_auth)]
    fig_line = px.line(trend_df, x="year", y="total_traffic_volume", color="local_authority_name",
                       template="plotly_dark", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

elif page == "System Details":
    st.markdown("## EMR & Spark Details")
    
    # System Details Cards
    col1, col2 = st.columns(2)
    with col1:
        st.success("Spark Job Status: COMPLETED")
        st.info("Storage: AWS S3 (Snappy Parquet)")
    with col2:
        st.warning("Cluster Type: m5.xlarge (Multi-node)")
        st.info("Application ID: application_1768398156808_0001")
    
    st.divider()

    # Download Processed Data
    st.markdown("## Data Export")
    st.download_button(
        label="Download Spark-Processed Data (.csv)", 
        data=df.to_csv(index=False), 
        file_name="processed_traffic_data.csv",
        mime="text/csv"
    )

    st.divider()

    # Logs
    st.markdown("## Standard Error Logs (stderr.gz)")
    st.markdown("#### 1. Cluster Initialization")
    st.code("""
26/01/14 14:25:17 INFO SparkContext: Running Spark version 3.5.6-amzn-1
26/01/14 14:25:17 INFO SparkContext: OS info Linux, 6.1.158-178.288.amzn2023.x86_64, amd64
26/01/14 14:25:17 INFO SparkContext: Java version 17.0.17
    """)
    
    st.markdown("#### 2. Job Execution Performance")
    st.code("""
26/01/14 14:25:27 INFO TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 2093 ms
26/01/14 14:25:27 INFO DAGScheduler: Job 0 finished: csv took 3.212606 s
    """)

    st.markdown("## Standard Output Logs (stdout.gz)")
    st.code("""
+--------------------+----+--------------------+------------------+
|local_authority_name|year|total_traffic_volume|avg_road_length_km|
+--------------------+----+--------------------+------------------+
|           Hampshire|2019|     1.0328812188E10|           8997.04|
|               Essex|2019|     1.0040556947E10|            8284.8|
+--------------------+----+--------------------+------------------+
    """)

# Authority Analysis
else: 
    st.title("Authority Analysis")
    auth_df = df[df['local_authority_name'].isin(selected_auth)]
    if not auth_df.empty:
        st.plotly_chart(px.box(auth_df, x="local_authority_name", y="congestion_index", template="plotly_dark"))
        st.dataframe(auth_df, use_container_width=True)
    else:
        st.warning("Please select at least one Authority from the sidebar.")
