import streamlit as st
import random
import numpy as np
from datetime import datetime, timedelta
from .meta import hot_goss, generate_next_price

brands = ["ARTIZIA", "YSL", "CARTIER"]

def init_session_state():
    defaults = {
        "prices": {b: 100.0 for b in brands},
        "closet": {b: 0 for b in brands},
        "allowance": 1000.0,
        "history": {b: [100.0] for b in brands},
        "net_worth_history": [],
        "buys": {b: [] for b in brands},
        "last_update": datetime.now(),
        "last_gossip_update": datetime.now(),
        "current_gossip": {"brand": None, "effect": 0, "headline": "No juicy gossip yet 💅"},
        "xp": 0,
        "stop_loss_enabled": {b: False for b in brands},
        "take_profit_enabled": {b: False for b in brands},
        "sale_history": [],
        "dividend_counter": 0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def update_prices_and_gossip():
    now = datetime.now()

    # Update gossip every 15 seconds
    if now - st.session_state.last_gossip_update > timedelta(seconds=15):
        st.session_state.current_gossip = random.choice(hot_goss)
        st.session_state.last_gossip_update = now

    # Update prices every 3 seconds
    if now - st.session_state.last_update > timedelta(seconds=3):
        st.session_state.last_update = now

        for brand in brands:
            new_price = generate_next_price(st.session_state.prices[brand], brand)
            st.session_state.prices[brand] = new_price
            st.session_state.history[brand].append(new_price)

        net = st.session_state.allowance
        for b in brands:
            net += st.session_state.closet[b] * st.session_state.prices[b]
        st.session_state.net_worth_history.append(net)

        # Risk-based auto-sell logic
        for b in brands:
            if st.session_state.closet[b] > 0 and st.session_state.buys[b]:
                avg_buy = sum(st.session_state.buys[b]) / len(st.session_state.buys[b])
                current_price = st.session_state.prices[b]
                threshold_down = avg_buy * 0.9
                threshold_up = avg_buy * 1.2
                auto_sell = False
                reason = ""

                if st.session_state.stop_loss_enabled[b] and current_price <= threshold_down:
                    auto_sell = True
                    reason = "⛔ Stop-loss triggered"
                elif st.session_state.take_profit_enabled[b] and current_price >= threshold_up:
                    auto_sell = True
                    reason = "🎯 Take-profit triggered"

                if auto_sell:
                    qty = st.session_state.closet[b]
                    proceeds = qty * current_price
                    spent = sum(st.session_state.buys[b])
                    profit = proceeds - spent

                    st.session_state.closet[b] = 0
                    st.session_state.allowance += proceeds
                    st.session_state.buys[b] = []
                    st.session_state.sale_history.append({
                        "brand": b,
                        "qty": qty,
                        "profit": profit,
                        "price": current_price,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

                    st.toast(f"{reason}: Auto-sold all {b} for ${proceeds:.2f}")

        # XP bump
        if net >= 1500:
            st.session_state.xp += 50

        # Dividends every 5 update cycles
        st.session_state.dividend_counter += 1
        if st.session_state.dividend_counter >= 5:
            for b in brands:
                if st.session_state.closet[b] > 0:
                    dividend = 0.5 * st.session_state.closet[b]
                    st.session_state.allowance += dividend
                    st.toast(f"✨ You received ${dividend:.2f} in dividends from {b} 💸")
            st.session_state.dividend_counter = 0
