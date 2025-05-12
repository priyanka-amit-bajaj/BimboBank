import streamlit as st
import pandas as pd

def render_trend_tools():
    brands = list(st.session_state.prices.keys())

    st.subheader("📈 Trend Vibes: Moving Average Crossovers")

    for b in brands:
        history = pd.Series(st.session_state.history[b])
        if len(history) >= 10:
            short_ma = history.rolling(window=3).mean()
            long_ma = history.rolling(window=10).mean()

            signal = ""
            if short_ma.iloc[-2] < long_ma.iloc[-2] and short_ma.iloc[-1] > long_ma.iloc[-1]:
                signal = "📈 Buy Signal!"
            elif short_ma.iloc[-2] > long_ma.iloc[-2] and short_ma.iloc[-1] < long_ma.iloc[-1]:
                signal = "📉 Sell Signal!"

            st.markdown(f"**{b}** {signal}")
            st.line_chart(pd.DataFrame({
                "Price": history,
                "3-period MA": short_ma,
                "10-period MA": long_ma
            }))
        else:
            st.markdown(f"**{b}** — not enough glam history yet 😮‍💨")

    st.subheader("🎯 Buy & Sell Zones")

    for b in brands:
        history = pd.Series(st.session_state.history[b])
        if len(history) >= 10:
            current = history.iloc[-1]
            recent_high = history[-10:].max()
            recent_low = history[-10:].min()

            if current <= recent_low * 1.05:
                zone = "👛 Buy Zone"
            elif current >= recent_high * 0.95:
                zone = "🛍️ Sell Zone"
            else:
                zone = "😐 Neutral"

            st.markdown(f"**{b}**: {zone} — Current: ${current:.2f}, Range: ${recent_low:.2f} - ${recent_high:.2f}")
        else:
            st.markdown(f"**{b}**: Not enough glam history for a zone vibe check 💅")

    st.subheader("📉 Risk Analysis (aka: Spicy Scores)")
    risk_rows = []
    risk_free_rate = 0.1  # risk-free return per update cycle

    for b in brands:
        prices = pd.Series(st.session_state.history[b])
        if len(prices) > 5:
            returns = prices.pct_change().dropna()
            vol = returns.std() * 100
            mean_return = returns.mean() * 100
            sharpe = round((mean_return - risk_free_rate) / vol, 2) if vol > 0 else 0
            spice = "🌶" if vol > 4 else "🧊"
            risk_rows.append([b, f"{vol:.2f}%", f"{mean_return:.2f}%", sharpe, spice])

    if risk_rows:
        df = pd.DataFrame(risk_rows, columns=["Brand", "Volatility %", "Avg Return %", "Sharpe Ratio", "Vibe"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Start building a closet to measure brand risk 💼")

    st.subheader("📊 Drama vs Return Chart")
    rvr_data = []

    for b in brands:
        prices = pd.Series(st.session_state.history[b])
        if len(prices) > 5:
            returns = prices.pct_change().dropna()
            vol = returns.std() * 100
            mean_return = returns.mean() * 100
            rvr_data.append({"Brand": b, "Volatility": vol, "Return": mean_return})

    rvr_df = pd.DataFrame(rvr_data)

    if not rvr_df.empty:
        st.scatter_chart(rvr_df, x="Volatility", y="Return", color="Brand")
    else:
        st.info("Need more price drama to plot this chart 💅")
