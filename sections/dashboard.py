import streamlit as st
import pandas as pd
from utils.meta import get_level

def render_dashboard():
    st.subheader("📈 What's Trending")
    brands = list(st.session_state.prices.keys())
    cols = st.columns(len(brands))
    for i, brand in enumerate(brands):
        history = st.session_state.history[brand]
        if len(history) >= 6:
            ma = pd.Series(history).rolling(5).mean().iloc[-1]
            signal = "📉" if history[-1] < ma else "📈"
        else:
            signal = "🫶"
        with cols[i]:
            st.metric(label=f"{brand} {signal}", value=f"${st.session_state.prices[brand]:.2f}")

    st.subheader("🧸 Your Closet")
    st.write(f"💳 Allowance: ${st.session_state.allowance:.2f}")
    for b in brands:
        st.write(f"{b}: {st.session_state.closet[b]} items")

    net = st.session_state.allowance + sum(
        st.session_state.closet[b] * st.session_state.prices[b] for b in brands
    )
    st.success(f"💅 Net Worth: ${net:.2f} — you're glowing, babe!")

    # Closet Diversity
    num_owned = sum(1 for qty in st.session_state.closet.values() if qty > 0)
    with st.expander("🌈 Closet Diversity Score"):
        if num_owned == 3:
            st.success("Closet fully diversified! You’re a fashion economist queen 💅")
        elif num_owned == 2:
            st.info("Nice mix! But could glam harder with that third brand.")
        elif num_owned == 1:
            st.warning("All eggs in one Birkin, babe. That’s risky!")
        else:
            st.info("You need to start shopping to slay the strategy 💖")

    # XP + Glow-Up Title
    st.subheader("🏆 Glow-Up Progress")
    st.progress(min(st.session_state.xp % 100, 100), text=f"XP: {st.session_state.xp}")
    st.info(f"🌟 Title: {get_level(st.session_state.xp)}")

    # CAGR Estimator
    st.subheader("📈 Your Glow-Up Speed (CAGR)")
    history = st.session_state.net_worth_history
    if len(history) >= 2 and history[0] > 0:
        initial = history[0]
        final = history[-1]
        n = len(history) / 20  # assuming 1 update = 3s
        cagr = ((final / initial) ** (1 / n)) - 1
        st.success(f"📈 Estimated CAGR: {cagr * 100:.2f}% per minute")
    else:
        st.info("Need more glow-up data to estimate your slay velocity ✨")

    # Max Drawdown
    st.subheader("🕳️ Max Drawdown (Drama Tracker)")
    net_worth = pd.Series(history)
    if len(net_worth) >= 2:
        peak = net_worth[0]
        max_drawdown = 0
        for value in net_worth:
            if value > peak:
                peak = value
            drawdown = (value - peak) / peak
            max_drawdown = min(max_drawdown, drawdown)
        st.error(f"😮 Max Drawdown: {max_drawdown * 100:.2f}%")
    else:
        st.info("No dips to track yet — you’re either early or perfect 💅")
