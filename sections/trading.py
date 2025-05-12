import streamlit as st
import pandas as pd
from datetime import datetime


def render_trading_panel():
    st.subheader("🛒 Time to Shop or Flip")

    brands = list(st.session_state.prices.keys())
    choice = st.selectbox("✨ Pick your glam:", brands)
    qty = st.number_input("How many?", min_value=1, value=1)
    col1, col2 = st.columns(2)

    # Buy Button
    with col1:
        if st.button("🛍️ Add to Cart"):
            cost = qty * st.session_state.prices[choice]
            if st.session_state.allowance >= cost:
                st.session_state.allowance -= cost
                st.session_state.closet[choice] += qty
                for _ in range(qty):
                    st.session_state.buys[choice].append(st.session_state.prices[choice])
                st.session_state.xp += 10
                st.success(f"Slayed {qty}x {choice} 💖")
            else:
                st.warning("Not enough allowance, boo 😭")

    # Sell Button
    with col2:
        if st.button("📦 Resell on Depop"):
            if st.session_state.closet[choice] >= qty:
                earned = qty * st.session_state.prices[choice]
                bought_prices = st.session_state.buys[choice][:qty]
                st.session_state.buys[choice] = st.session_state.buys[choice][qty:]
                profit = earned - sum(bought_prices)
                st.session_state.closet[choice] -= qty
                st.session_state.allowance += earned
                st.session_state.sale_history.append({
                    "brand": choice,
                    "qty": qty,
                    "profit": profit,
                    "price": st.session_state.prices[choice],
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                if profit > 0:
                    st.session_state.xp += 15
                    st.success(f"Profit babe 💰 (+15 XP)")
                elif profit < 0:
                    st.session_state.xp += 5
                    st.info(f"Sold at a loss, but hey, still learning (+5 XP)")
                else:
                    st.session_state.xp += 10
                    st.info("Broke even — cute but neutral 😎")
            else:
                st.warning("You don't even own that much, bestie")

    # Stop-loss / Take-Profit Toggles
    st.subheader("🛑 Risk Settings")
    for b in brands:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.stop_loss_enabled[b] = st.checkbox(
                f"{b}: Enable Stop-Loss (10%)",
                value=st.session_state.stop_loss_enabled[b],
                key=f"sl_{b}"
            )
        with col2:
            st.session_state.take_profit_enabled[b] = st.checkbox(
                f"{b}: Enable Take-Profit (20%)",
                value=st.session_state.take_profit_enabled[b],
                key=f"tp_{b}"
            )

    # Trade Journal
    st.subheader("📋 Trade Journal")
    with st.expander("🧾 View Sale History"):
        if st.session_state.sale_history:
            df = pd.DataFrame(st.session_state.sale_history)
            st.dataframe(df[::-1], use_container_width=True)
        else:
            st.info("No trades yet, boo. Buy and resell to track your glow-up 💅")
