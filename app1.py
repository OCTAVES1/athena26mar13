import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Config & Theme
st.set_page_config(layout="wide", page_title="Covert Channel Monitor", page_icon="🛡️")

# 2. Header Section
st.title("Layer 2 Network Analytics: Covert Channel Monitor")
st.caption("Monitor local Layer 2 traffic for clandestine communications matching atypical EtherTypes.")

# Data Loading & Error Handling
csv_file = "ids_alert_log.csv"
num_covert_packets = 0
df_csv = pd.DataFrame()

if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
    st.success("🟢 Network Secure. No 0x0806 packets detected yet.")
else:
    try:
        df_csv = pd.read_csv(csv_file)
        if df_csv.empty:
            st.success("🟢 Network Secure. No 0x0860 packets detected yet.")
        else:
            num_covert_packets = len(df_csv)
    except pd.errors.EmptyDataError:
        st.success("🟢 Network Secure. No 0x0860 packets detected yet.")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# 3. Top Row Layout
col1, col2 = st.columns([0.35, 0.65])

# 4. Column 1: Protocol Distribution
with col1:
    st.subheader("Protocol Distribution")
    
    protocols = ['TCP', 'ARP', 'IPv4', '0x0860']
    values = [350, 320, 310, num_covert_packets]
    
    # Colors mapping
    color_map = {
        'TCP': '#FFA500',    # Orange
        'ARP': '#008000',    # Green
        'IPv4': '#0000FF',   # Blue
        '0x0860': '#FF0000'  # Bright Red
    }
    
    fig_donut = px.pie(
        names=protocols, 
        values=values, 
        hole=0.5,
        color=protocols,
        color_discrete_map=color_map
    )
    
    # Position the legend to the right of the donut
    fig_donut.update_layout(
        legend=dict(orientation="v", yanchor="auto", y=0.5, xanchor="left", x=1.0),
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# 5. Column 2: Traffic Arrival Timeline
with col2:
    st.subheader("Traffic Arrival Timeline")
    
    ids_mode = st.toggle("Activate IDS Mode (Highlight Suspect Protocols)")
    
    if num_covert_packets > 0 and 'Time' in df_csv.columns:
        timestamps = df_csv['Time'].tolist()
        sequence = list(range(1, num_covert_packets + 1))
        
        df_timeline = pd.DataFrame({
            'Timestamp': timestamps,
            'Packet Sequence': sequence
        })
        fig_line = px.line(df_timeline, x='Timestamp', y='Packet Sequence')
    else:
        df_timeline = pd.DataFrame({'Timestamp': [], 'Packet Sequence': []})
        fig_line = px.line(x=[0], y=[0])
        fig_line.update_traces(visible=False)
        fig_line.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
    
    # Appearance: bright, glowing light blue/cyan, transparent background
    glowing_cyan = '#00FFFF'
    suspect_highlight = '#FF0000'
    
    line_color = suspect_highlight if ids_mode else glowing_cyan
    
    fig_line.update_traces(line=dict(color=line_color, width=3))
    
    fig_line.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Packet Sequence",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_line, use_container_width=True)

# 6. Bottom Row: Clandestine Intercept Feed
st.subheader("Clandestine Intercept Feed")

if num_covert_packets > 0:
    df_feed = pd.DataFrame()
    if 'Time' in df_csv.columns:
        df_feed['Timestamp'] = df_csv['Time']
    if 'Source_MAC' in df_csv.columns:
        df_feed['Source MAC'] = df_csv['Source_MAC']
    if 'Destination_MAC' in df_csv.columns:
        df_feed['Target MAC'] = df_csv['Destination_MAC']
        
    df_feed['Protocol'] = '0x0860'
    df_feed['Decoded Payload'] = 'EXFILTRATION_INIT'
    
    # Reverse the dataframe so the newest alerts appear at the top
    df_feed = df_feed.iloc[::-1].reset_index(drop=True)
    
    st.dataframe(df_feed, use_container_width=True)
else:
    # Empty feed if no packets
    df_feed = pd.DataFrame(columns=['Timestamp', 'Source MAC', 'Target MAC', 'Protocol', 'Decoded Payload'])
    st.dataframe(df_feed, use_container_width=True)

import time
time.sleep(2)
st.rerun()
