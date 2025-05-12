# FINTENDO: HOT GIRL FINANCE - FULL APP
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --------------------
# Page Setup
# --------------------
st.set_page_config(page_title="🍬 Fintendo: Hot Girl Finance", layout="centered")
st_autorefresh(interval=3000, limit=None, key="fintendo-refresh")

brands = ["ARTIZIA", "YSL", "CARTIER"]

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


# --------------------
# Gossip
# --------------------
hot_goss = [
    {"brand": "ARTIZIA", "effect": 1, "headline": "ARTIZIA went viral on TikTok — everything's sold out 💖"},
    {"brand": "ARTIZIA", "effect": -1, "headline": "ARTIZIA exposed for low-quality stitch drama 💅"},
    {"brand": "YSL", "effect": 1, "headline": "YSL lip oil now officially hotter than your ex 🔥"},
    {"brand": "YSL", "effect": -1, "headline": "YSL caught copying Dior again. Fashion week flopped 😬"},
    {"brand": "CARTIER", "effect": 1, "headline": "Kylie Jenner spotted in CARTIER — prices skyrocket 💎"},
    {"brand": "CARTIER", "effect": -1, "headline": "CARTIER drops in clout after fake bracelet scandal 💔"},
]

# --------------------
# Price generator
# --------------------
def generate_next_price(price, brand):
    drama = 0
    if st.session_state.current_gossip["brand"] == brand:
        drama = st.session_state.current_gossip["effect"] * 1.5
    return round(price + np.random.uniform(-2, 2) + drama, 2)

# --------------------
# XP + Level
# --------------------
def get_level(xp):
    if xp >= 350:
        return "👑 Fashion Finance Queen"
    elif xp >= 200:
        return "💼 Style Fund Strategist"
    elif xp >= 100:
        return "📈 Retail Investor Baddie"
    else:
        return "👝 Shopaholic"

# --------------------
# Update Prices + Gossip
# --------------------
now = datetime.now()

if now - st.session_state.last_gossip_update > timedelta(seconds=15):
    st.session_state.current_gossip = random.choice(hot_goss)
    st.session_state.last_gossip_update = now

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

    # 🛑 Auto-sell based on stop-loss or take-profit rules
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

    if net >= 1500:
        st.session_state.xp += 50

    # 💸 Dividends payout every 5 update cycles
    st.session_state.dividend_counter += 1
    if st.session_state.dividend_counter >= 5:
        for b in brands:
            if st.session_state.closet[b] > 0:
                dividend = 0.5 * st.session_state.closet[b]
                st.session_state.allowance += dividend
                st.toast(f"✨ You received ${dividend:.2f} in dividends from {b} 💸")
        st.session_state.dividend_counter = 0


# --------------------
# Main App UI
# --------------------
st.title("💅 Fintendo: Hot Girl Finance")
st.caption("Where being pretty *and* rich is the only strategy. 💖")

st.subheader("🗞️ Gossip Report")
st.info(f"**{st.session_state.current_gossip['headline']}**", icon="👛")

st.subheader("📈 What's Trending")
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

num_brands_owned = sum(1 for qty in st.session_state.closet.values() if qty > 0)
with st.expander("🌈 Closet Diversity Score"):
    if num_brands_owned == 3:
        st.success("Closet fully diversified! You’re a fashion economist queen 💅")
    elif num_brands_owned == 2:
        st.info("Nice mix! But could glam harder with that third brand.")
    elif num_brands_owned == 1:
        st.warning("All eggs in one Birkin, babe. That’s risky!")
    else:
        st.info("You need to start shopping to slay the strategy 💖")

st.subheader("📈 Your Glow-Up Speed (CAGR)")

net_history = st.session_state.net_worth_history

if len(net_history) >= 2 and net_history[0] > 0:
    initial = net_history[0]
    final = net_history[-1]
    n = len(net_history) / 20  # assuming 1 update = 3s, 20 updates ≈ 1 minute

    cagr = ((final / initial) ** (1 / n)) - 1
    st.success(f"📈 Estimated CAGR: {cagr * 100:.2f}% per minute")
else:
    st.info("Need more glow-up data to estimate your slay velocity ✨")

st.subheader("🕳️ Max Drawdown (Drama Tracker)")

net_worth = pd.Series(st.session_state.net_worth_history)

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


st.subheader("🥧 Closet Value Allocation")

closet_values = {
    b: st.session_state.closet[b] * st.session_state.prices[b] for b in brands
}
total_value = sum(closet_values.values())

if total_value > 0:
    value_df = pd.DataFrame({
        "Brand": list(closet_values.keys()),
        "Value": list(closet_values.values())
    })
    value_df.set_index("Brand", inplace=True)
    st.pyplot(value_df.plot.pie(y="Value", autopct="%.1f%%", legend=False, ylabel="").figure)
else:
    st.info("Buy some glam to unlock the closet pie chart 💖")

st.subheader("🧮 Closet Rebalancer")

closet_values = {b: st.session_state.closet[b] * st.session_state.prices[b] for b in brands}
total_value = sum(closet_values.values())

if total_value == 0:
    st.info("Build your closet before rebalancing, babe 💅")
else:
    ideal = total_value / len(brands)
    st.markdown("Target: **33.3% per brand** for a perfectly balanced closet ⚖️")

    rebalance_rows = []
    for b in brands:
        current = closet_values[b]
        diff = ideal - current
        action = "Buy" if diff > 0 else "Sell"
        units = abs(diff) / st.session_state.prices[b]
        rebalance_rows.append([b, f"${current:.2f}", f"${ideal:.2f}", f"{action} ~{abs(units):.1f}"])

    df = pd.DataFrame(rebalance_rows, columns=["Brand", "Current Value", "Target Value", "Suggested Action"])
    st.dataframe(df, use_container_width=True)


st.subheader("🏆 Glow-Up Progress")
st.progress(min(st.session_state.xp % 100, 100), text=f"XP: {st.session_state.xp}")
st.info(f"🌟 Title: {get_level(st.session_state.xp)}")

st.subheader("🛒 Time to Shop or Flip")
choice = st.selectbox("Pick a brand", brands)
qty = st.number_input("How many?", min_value=1, value=1)
col1, col2 = st.columns(2)

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

with col2:
    if st.button("📦 Resell on Depop"):
        if st.session_state.closet[choice] >= qty:
            earned = qty * st.session_state.prices[choice]
            bought_prices = st.session_state.buys[choice][:qty]
            st.session_state.buys[choice] = st.session_state.buys[choice][qty:]
            profit = earned - sum(bought_prices)
            # Track sale history
            st.session_state.sale_history.append({
                "brand": choice,
                "qty": qty,
                "profit": profit,
                "price": st.session_state.prices[choice],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.session_state.closet[choice] -= qty
            st.session_state.allowance += earned
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

st.subheader("🛑 Risk Settings")

for b in brands:
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.stop_loss_enabled[b] = st.checkbox(f"{b}: Enable Stop-Loss (10%)", value=st.session_state.stop_loss_enabled[b], key=f"sl_{b}")
    with col2:
        st.session_state.take_profit_enabled[b] = st.checkbox(f"{b}: Enable Take-Profit (20%)", value=st.session_state.take_profit_enabled[b], key=f"tp_{b}")

st.subheader("📋 Trade Journal")

with st.expander("🧾 View Sale History"):
    if st.session_state.sale_history:
        history_df = pd.DataFrame(st.session_state.sale_history)
        st.dataframe(history_df[::-1], use_container_width=True)
    else:
        st.info("No trades yet, boo. Buy and resell to track your glow-up 💅")

# --------------------
# Trend & Price Charts
# --------------------
st.subheader("📊 Net Worth Over Time")
if st.session_state.net_worth_history:
    st.line_chart(pd.Series(st.session_state.net_worth_history, name="Net Worth"))
else:
    st.info("No glow-up data yet, queen 💅 Start investing to see your rise!")

st.subheader("📈 Trend Vibes: Moving Average Crossovers")

for b in brands:
    history = pd.Series(st.session_state.history[b])
    if len(history) >= 10:
        short_ma = history.rolling(window=3).mean()
        long_ma = history.rolling(window=10).mean()

        crossover_signal = ""
        if short_ma.iloc[-2] < long_ma.iloc[-2] and short_ma.iloc[-1] > long_ma.iloc[-1]:
            crossover_signal = "📈 Buy Signal!"
        elif short_ma.iloc[-2] > long_ma.iloc[-2] and short_ma.iloc[-1] < long_ma.iloc[-1]:
            crossover_signal = "📉 Sell Signal!"

        st.markdown(f"**{b}** {crossover_signal}")
        st.line_chart(pd.DataFrame({
            "Price": history,
            "3-period MA": short_ma,
            "10-period MA": long_ma
        }))
    else:
        st.markdown(f"**{b}** — not enough glam history yet for analysis 😮‍💨")

st.subheader("🎯 Buy & Sell Zones")

for b in brands:
    history = pd.Series(st.session_state.history[b])
    if len(history) >= 10:
        current = history.iloc[-1]
        recent_high = history[-10:].max()
        recent_low = history[-10:].min()

        # Define zones
        if current <= recent_low * 1.05:
            zone = "👛 Buy Zone"
        elif current >= recent_high * 0.95:
            zone = "🛍️ Sell Zone"
        else:
            zone = "😐 Neutral"

        st.markdown(f"**{b}**: {zone} — Current: ${current:.2f}, Range: ${recent_low:.2f} - ${recent_high:.2f}")
    else:
        st.markdown(f"**{b}**: Not enough glam history for a zone vibe check 💅")


# ----------------------------------
# Capital Gains + Yeild Dashboard
# ----------------------------------
st.subheader("📈 Capital Gains + Dividend Yields")
st.markdown("Here's how your closet is doing in terms of capital gains and dividend yields:")

rows = []
for b in brands:
    qty = st.session_state.closet[b]
    buys = st.session_state.buys[b]
    price = st.session_state.prices[b]

    if qty > 0 and buys:
        avg_buy = round(sum(buys) / len(buys), 2)
        cap_gain = round(((price - avg_buy) / avg_buy) * 100, 2) if avg_buy > 0 else 0
        yield_pct = round((0.5 / price) * 100, 2)  # assuming $0.50 per unit held
        rows.append([b, f"${avg_buy}", f"${price:.2f}", f"{cap_gain}%", f"{yield_pct}%"])

if rows:
    df = pd.DataFrame(rows, columns=["Brand", "Avg Buy", "Current", "Capital Gain %", "Yield %"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("Buy something to start tracking gains & income, baddie 💖")

# --------------------
# 💅 Analytics Dashboard
# --------------------
st.subheader("📊 Closet Analytics (aka: Finance for Baddies)")

st.markdown("Here's how your closet is doing in dollar terms — profits, losses, and glow-up energy:")

# Add buy history tracker if not already set
if "buys" not in st.session_state:
    st.session_state.buys = {b: [] for b in brands}  # list of purchase prices

analytics_cols = ["Brand", "Total Items", "Avg Buy Price", "Current Price", "Total Spent", "Current Value", "Gain/Loss", "Glow Rating"]
analytics_data = []

for b in brands:
    qty = st.session_state.closet[b]
    buys = st.session_state.buys[b]
    if qty > 0 and buys:
        avg_buy = round(sum(buys) / len(buys), 2)
        total_spent = round(sum(buys), 2)
        current_val = round(qty * st.session_state.prices[b], 2)
        pnl = round(current_val - total_spent, 2)
        gain_pct = round((pnl / total_spent) * 100, 2) if total_spent > 0 else 0

        if pnl > 0:
            badge = f"💖 +{gain_pct}%"
        elif pnl < 0:
            badge = f"💔 {gain_pct}%"
        else:
            badge = "😐 0%"

        analytics_data.append([
            b, qty, f"${avg_buy}", f"${st.session_state.prices[b]:.2f}",
            f"${total_spent}", f"${current_val}", f"${pnl}", badge
        ])

if analytics_data:
    df = pd.DataFrame(analytics_data, columns=analytics_cols)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Start shopping to unlock analytics, babe 💅")

st.subheader("📉 Risk Analysis (aka: Spicy Scores)")

risk_rows = []
risk_free_rate = 0.1  # risk-free return per update cycle (can be adjusted)

for b in brands:
    prices = pd.Series(st.session_state.history[b])
    if len(prices) > 5:
        returns = prices.pct_change().dropna()
        vol = returns.std() * 100  # standard deviation as %
        mean_return = returns.mean() * 100
        sharpe = round((mean_return - risk_free_rate) / vol, 2) if vol > 0 else 0
        spice = "🌶" if vol > 4 else "🧊"
        risk_rows.append([b, f"{vol:.2f}%", f"{mean_return:.2f}%", sharpe, spice])

if risk_rows:
    risk_df = pd.DataFrame(risk_rows, columns=["Brand", "Volatility %", "Avg Return %", "Sharpe Ratio", "Vibe"])
    st.dataframe(risk_df, use_container_width=True)
else:
    st.info("Start building a closet to measure brand risk 💼")

st.subheader("📊 Drama vs Return Chart")

rvr = []
for b in brands:
    prices = pd.Series(st.session_state.history[b])
    if len(prices) > 5:
        returns = prices.pct_change().dropna()
        vol = returns.std() * 100
        mean_return = returns.mean() * 100
        rvr.append({"Brand": b, "Volatility": vol, "Return": mean_return})

rvr_df = pd.DataFrame(rvr)

if not rvr_df.empty:
    st.scatter_chart(rvr_df, x="Volatility", y="Return", color="Brand")
else:
    st.info("Need more price drama to plot this chart 💅")

# --------------------
# Sidebar Guide
# --------------------
st.sidebar.title("📚 Hot Girl Finance Guide")
st.sidebar.markdown("""
Welcome to **Hot Girl Finance 101** 💅  
Where we turn confusing finance talk into shopping, gossip, and glow-ups.

---

### 💖 What is this game?
This is your *closet-coded crash course* in investing.

---

### 📈 Stocks = Designer Brands  
Buying ARTIZIA or YSL is like buying stock IRL. Slay when it trends.

### 🧸 Portfolio = Closet  
Diversify that closet, babe — don’t put all your glam in one Birkin.

### 💳 Allowance = Cash  
You get starting $$ to glow it up. Spend wisely.

### 🛒 Buy Low, Resell High  
Sell at a profit = win. Resell at a loss? Still a learning slay.

### 📜 Gossip = Market News  
Rumors move prices. TikTok is the new Bloomberg.

### 📅 Net Worth = Rich Girl Score  
Cash + Closet Value = Net Worth. Simple as that.

### 🏆 XP = Confidence  
Invest more, learn more, glow more. Level up to fund manager fantasy.

---

## 💵 Fundamentals

### 💵 Capital Gains  
Your glow-up in dollar form.
- Bought ARTIZIA at $90  
- Now it's $110  
- You gained $20 (+22%) 🤑

### 💸 Dividend Yield  
Free money for being loyal.
- Brands pay $0.50 per item
- If price is $100, that's a 0.5% yield
- The more you hold, the more you glow ✨

### 📋 Trade Journal  
Your shopping history — but fiscally fierce.
- Every resale is logged
- Learn, reflect, or flex 💅

---

## 📊 Market Behavior

### 📉 Volatility (Spicy Score 🌶)  
How dramatic the brand is:
- High = risky & chaotic
- Low = chill & stable queen

### 📈 Sharpe Ratio (Smart Slay Score)  
How much return you get *per unit of risk*.

""")
st.sidebar.latex(r"""
\text{Sharpe} = \frac{\text{Return} - \text{Risk-Free Rate}}{\text{Volatility}}
""")
st.sidebar.markdown("""
- Bigger = smarter gains 💼  
- Think: glam reward ÷ chaos

### 📊 Drama vs Return  
Visual cheat sheet:
- X = Volatility  
- Y = Return  
- Each dot = a brand

**How to read it:**
- 🔥 Top-right = risky but hot  
- 😬 Bottom-right = chaotic flop  
- 💼 Top-left = rare investing baddie

---

## 🛑 Risk Controls

### Stop-Loss (10%)  
Auto-sells a brand if price drops 10% from what you paid.  
Save your glam from market disasters 🛡️

### Take-Profit (20%)  
Auto-sells when price hits +20%.  
Secure the bag, queen 🎯

You can toggle these per brand in your control panel.

---

## 🥧 Portfolio Strategy

### Closet Value Allocation  
Your closet, but weighted by value not quantity.
- 3 CARTIER = rich girl power 👑  
- 3 ARITZIA = still iconic, just cheaper

See where your glam is concentrated 💼

### 📈 CAGR (Glow-Up Rate)  
How fast your net worth is compounding.

""")
st.sidebar.latex(r"""
\text{CAGR} = \left( \frac{\text{Final}}{\text{Initial}} \right)^{1/n} - 1
""")
st.sidebar.markdown("""
- Starts slow, builds momentum  
- Compounding = queen behavior 👑  
- The higher your CAGR, the faster you're slaying.

### 🧮 Closet Rebalancer
Helps you stay fashionably diversified.

- Calculates how much value each brand holds
- Suggests what to buy/sell to reach balance
- Slay smarter, not harder 💼💅

### 📈 Moving Average Crossovers
Two trendlines = one powerful vibe check.

- **3-Period MA** = recent glam  
- **10-Period MA** = overall mood

**Buy Signal:** when short MA crosses above long  
**Sell Signal:** when it drops below

Gives you trend-following energy 💼

### 🕳️ Max Drawdown
Your worst dip from peak net worth.

- Shows how much your glow-up reversed  
- Emotional damage — but quantified 😭  
- Big drawdowns = high volatility = more risk

### 🎯 Buy & Sell Zones
Glam-coded support/resistance zones.

- 👛 **Buy Zone** = price near recent low  
- 🛍️ **Sell Zone** = price near recent high  
- 😐 Neutral = hold your Birkin for now

Helps you spot when a brand is overhyped or undervalued.
""")
