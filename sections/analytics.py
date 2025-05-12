import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # ✅ safest backend for Streamlit
import matplotlib.pyplot as plt


def render_analytics_panel():
    brands = list(st.session_state.prices.keys())

    # Pie Chart
    st.subheader("🥧 Closet Value Allocation")
    closet_values = {
        b: st.session_state.closet[b] * st.session_state.prices[b] for b in brands
    }
    total_value = sum(closet_values.values())
    if total_value > 0:
        labels = []
        sizes = []
        colors = ["#FFC0CB", "#B19CD9", "#FFD700"]  # pastel pink, lilac, gold
        for b, val in closet_values.items():
            if val > 0:
                labels.append(f"{b} ({val/total_value:.1%})")
                sizes.append(val)

        fig, ax = plt.subplots(figsize=(3, 3))
        fig.patch.set_facecolor('#0e1117')  # dark background safely

        wedges, texts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )

        for text in texts:
            text.set_color('white')
            text.set_fontsize(10)

        st.pyplot(fig)
    else:
        st.info("Buy some glam to unlock the closet pie chart 💖")

    # Rebalancer
    st.subheader("🧮 Closet Rebalancer")
    if total_value == 0:
        st.info("Build your closet before rebalancing, babe 💅")
    else:
        ideal = total_value / len(brands)
        st.markdown("Target: **33.3% per brand** for a balanced closet ⚖️")

        rebalance_rows = []
        for b in brands:
            current = closet_values[b]
            diff = ideal - current
            action = "Buy" if diff > 0 else "Sell"
            units = abs(diff) / st.session_state.prices[b]
            rebalance_rows.append([b, f"${current:.2f}", f"${ideal:.2f}", f"{action} ~{abs(units):.1f}"])

        df = pd.DataFrame(rebalance_rows, columns=["Brand", "Current Value", "Target Value", "Suggested Action"])
        st.dataframe(df, use_container_width=True)

    # Capital Gains + Yield Table
    st.subheader("📈 Capital Gains + Dividend Yields")
    rows = []
    for b in brands:
        qty = st.session_state.closet[b]
        buys = st.session_state.buys[b]
        price = st.session_state.prices[b]
        if qty > 0 and buys:
            avg_buy = round(sum(buys) / len(buys), 2)
            cap_gain = round(((price - avg_buy) / avg_buy) * 100, 2) if avg_buy > 0 else 0
            yield_pct = round((0.5 / price) * 100, 2)  # assuming $0.50 per unit
            rows.append([b, f"${avg_buy}", f"${price:.2f}", f"{cap_gain}%", f"{yield_pct}%"])

    if rows:
        df = pd.DataFrame(rows, columns=["Brand", "Avg Buy", "Current", "Capital Gain %", "Yield %"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Buy something to start tracking gains & income, baddie 💖")

    # Closet Analytics Table
    st.subheader("📊 Closet Analytics (aka: Finance for Baddies)")
    analytics_rows = []

    for b in brands:
        qty = st.session_state.closet[b]
        buys = st.session_state.buys[b]
        price = st.session_state.prices[b]
        if qty > 0 and buys:
            avg_buy = round(sum(buys) / len(buys), 2)
            total_spent = round(sum(buys), 2)
            current_val = round(qty * price, 2)
            pnl = round(current_val - total_spent, 2)
            gain_pct = round((pnl / total_spent) * 100, 2) if total_spent > 0 else 0

            badge = "😐 0%"
            if pnl > 0:
                badge = f"💖 +{gain_pct}%"
            elif pnl < 0:
                badge = f"💔 {gain_pct}%"

            analytics_rows.append([
                b, qty, f"${avg_buy}", f"${price:.2f}",
                f"${total_spent}", f"${current_val}", f"${pnl}", badge
            ])

    if analytics_rows:
        df = pd.DataFrame(analytics_rows, columns=[
            "Brand", "Total Items", "Avg Buy Price", "Current Price",
            "Total Spent", "Current Value", "Gain/Loss", "Glow Rating"
        ])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Start shopping to unlock analytics, babe 💅")
