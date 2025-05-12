import streamlit as st

def render_sidebar():
    st.sidebar.title("📚 Hot Girl Finance Guide")
    st.sidebar.markdown("""
Welcome to **Hot Girl Finance 101** 💅  
Where we turn confusing finance talk into shopping, gossip, and glow-ups.

---

### 💖 What is this game?
Your *closet-coded crash course* in investing.

---

### 📈 Stocks = Designer Brands  
Buying ARTIZIA or YSL = investing. Slay when they trend.

### 🧸 Closet = Portfolio  
Hold a lil’ of everything. Diversify that glam.

### 💳 Allowance = Cash  
You start with $1000. Use it to glow up wisely.

### 🛍️ Buy Low, Sell High  
Profit when the trends shift.  
Loss? Still a learning slay.

### 📰 Gossip = Market News  
Rumors move prices. TikTok > Bloomberg.

### 📅 Net Worth = Rich Girl Score  
Cash + Closet Value = Your glow-up 💖

### 🏆 XP = Confidence  
Buy? Sell? Win? Level up and unlock new baddie titles.

---

### 🛑 Risk Settings

**Stop-Loss (10%)**  
If your brand drops 10% from what you paid, it automatically sells.  
🛡️ Protects your closet from glam catastrophes.

**Take-Profit (20%)**  
If a brand pops +20%, it sells to lock in gains.  
💼 Secures your slay so you don’t fumble the bag.

### 💡 When to Use Them:

- Turn on **Stop-Loss** if you're scared of dramatic flops 😬  
- Use **Take-Profit** to capture profits when a brand goes viral 📈  
- Mix and match depending on your glam tolerance 💅

---

## 💵 Closet Insights

### 💵 Capital Gains  
The glow-up of your investment:
- Bought ARTIZIA at $90  
- Now it's $110 → +22% gain 🤑

### 💸 Dividend Yield  
Free money just for holding glam:
- $0.50 paid regularly
- More you hold = more you earn ✨

### 📋 Trade Journal  
Track your flips, wins, and oopsies.  
Glam + accountability.

---

## 📊 Market Behavior

### 📉 Volatility (Spicy Score 🌶)  
How dramatic a brand is:
- High = chaos, high risk  
- Low = boring, stable queen

### 📈 Sharpe Ratio (Smart Slay Score)  
How worth it your risk is.

""")
    st.sidebar.latex(r"""
\text{Sharpe} = \frac{\text{Return} - \text{Risk-Free Rate}}{\text{Volatility}}
""")
    st.sidebar.markdown("""
- Bigger = better risk-adjusted glam
- Think: reward ÷ chaos

### 🎯 Buy & Sell Zones  
Support/resistance made aesthetic:
- 👛 Buy = near recent low  
- 🛍️ Sell = near recent high  
- 😐 Neutral = hold your Birkin

---

## 📊 Portfolio Strategy

### 🥧 Closet Value Allocation  
See how much glam is in each brand — by $ not items.

### 🧮 Closet Rebalancer  
Helps you fix fashion imbalance.
- Suggests what to buy/sell to slay 33.3% split

### 📈 CAGR (Glow-Up Rate)  
How fast you're leveling up financially.

""")
    st.sidebar.latex(r"""
\text{CAGR} = \left( \frac{\text{Final}}{\text{Initial}} \right)^{1/n} - 1
""")
    st.sidebar.markdown("""
- Slow start → compounding queen  
- Bigger CAGR = bigger bag

### 🕳️ Max Drawdown  
Tracks your biggest loss dip from a peak 😭  
Emotional damage, but make it quantifiable.

---

Now go forth and trade like the legend you are 💼👛✨
""")
