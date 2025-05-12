import numpy as np
import streamlit as st

brands = ["ARTIZIA", "YSL", "CARTIER"]

hot_goss = [
    {"brand": "ARTIZIA", "effect": 1, "headline": "ARTIZIA went viral on TikTok — everything's sold out 💖"},
    {"brand": "ARTIZIA", "effect": -1, "headline": "ARTIZIA exposed for low-quality stitch drama 💅"},
    {"brand": "YSL", "effect": 1, "headline": "YSL lip oil now officially hotter than your ex 🔥"},
    {"brand": "YSL", "effect": -1, "headline": "YSL caught copying Dior again. Fashion week flopped 😬"},
    {"brand": "CARTIER", "effect": 1, "headline": "Kylie Jenner spotted in CARTIER — prices skyrocket 💎"},
    {"brand": "CARTIER", "effect": -1, "headline": "CARTIER drops in clout after fake bracelet scandal 💔"},
]

def generate_next_price(price, brand):
    drama = 0
    if st.session_state["current_gossip"]["brand"] == brand:
        drama = st.session_state["current_gossip"]["effect"] * 1.5
    return round(price + np.random.uniform(-2, 2) + drama, 2)

def get_level(xp):
    if xp >= 350:
        return "👑 Fashion Finance Queen"
    elif xp >= 200:
        return "💼 Style Fund Strategist"
    elif xp >= 100:
        return "📈 Retail Investor Baddie"
    else:
        return "👝 Shopaholic"
