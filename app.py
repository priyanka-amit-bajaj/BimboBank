# BimboBank: HOT GIRL FINANCE
import streamlit as st
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Import section modules
from sections import dashboard, trading, analytics, trends
from utils.state import init_session_state, update_prices_and_gossip
from sections.sidebar import render_sidebar

# Page setup
st.set_page_config(page_title="BimboBank", layout="wide")
st_autorefresh(interval=3000, limit=None, key="fintendo-refresh")

# Initialize session state
init_session_state()

# Price update logic
update_prices_and_gossip()

# Main title + gossip bar
st.title("🍬 BimboBank: Hot Girl Finance")
st.caption("Where being pretty *and* rich is the only strategy. 💖")
st.info(f"**{st.session_state.current_gossip['headline']}**", icon="👛")

# Tabs layout
tabs = st.tabs(["🏠 Dashboard", "🛒 Trading", "📊 Analytics", "📈 Trend Tools"])

with tabs[0]:
    dashboard.render_dashboard()

with tabs[1]:
    trading.render_trading_panel()

with tabs[2]:
    analytics.render_analytics_panel()

with tabs[3]:
    trends.render_trend_tools()

# Sidebar
render_sidebar()
