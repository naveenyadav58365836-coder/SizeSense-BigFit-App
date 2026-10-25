import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="SizeSense | BigFit", page_icon="👕", layout="wide")
st.title("👕 SizeSense — BigFit Inventory Agent")
st.caption("Size-aware inventory monitoring • Demo prototype")

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

with st.sidebar:
    st.markdown("### BIGFIT INVENTORY AGENT")
    st.markdown("---")
    st.markdown("*WORKSPACE*")
    
    # Navigation menu widget
    page = st.radio(
        "Workspace Menu",
        [
            "Today's Attention",
            "Size Mix Explorer",
            "Transfer Planner",
            "Ageing & Markdown",
            "Demand Shifts",
            "Promotions & Festivals",
            "Supplier Compare",
            "Agent Chat",
            "Action Log"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.header("Controls")
    uploaded = st.file_uploader("Upload Inventory CSV", type=["csv"])

if uploaded:
    inventory = pd.read_csv(uploaded)
else:
    inventory = pd.DataFrame({
        "Product": ["Classic Tee", "Relaxed Hoodie", "Straight Jeans", "Polo Shirt", "Joggers"],
        "Size": ["M", "XL", "L", "S", "XXL"],
        "Store": ["Central", "Central", "North", "South", "North"],
        "Stock": [24, 3, 8, 17, 2],
        "Weekly Demand": [12, 9, 10, 7, 6],
        "Unit Price": [499, 1299, 1499, 799, 999],
    })

st.title("Today's Attention")
st.caption("The decisions that protect sales and keep stock healthy.")

# Banner Box
st.markdown("""
<div style="background-color: #0b3d2e; color: white; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
    <h3 style="margin: 0 0 10px 0; color: #ffffff;">Good morning, merchandising team.</h3>
    <p style="margin: 0 0 12px 0; font-size: 15px; color: #d0e7de;">
        Prioritize the sizes customers actually need — not just the total units on the shelf.<br>
        <strong>3 recommended moves are ready for your review.</strong>
    </p>
    <span style="background-color: #165b46; color: #a3e6cd; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">
        ● DEMO DATA • RULE-BASED
    </span>
</div>
""", unsafe_allow_html=True)

# Process Metrics Data
stock_col = "Stock" if "Stock" in inventory.columns else None
demand_col = "Weekly Demand" if "Weekly Demand" in inventory.columns else None

if stock_col:
    stock = pd.to_numeric(inventory[stock_col], errors="coerce").fillna(0)
    demand = pd.to_numeric(inventory[demand_col], errors="coerce").fillna(0) if demand_col else pd.Series(0, index=inventory.index)
    
    out_of_stock = int((stock <= 0).sum())
    low_stock = int(((stock > 0) & (stock < demand)).sum()) if demand_col else 0
    total_units = int(stock.sum())
    
    # Grid Row 1 (3 Columns)
    c1, c2, c3 = st.columns(3)
    c1.metric(label="⚠️ Stock-out risk", value=f"{out_of_stock}", delta="↑ 4 vs last review", delta_color="inverse")
    c2.metric(label="📦 Overstock value", value="₹4.8L", delta="Network stock value")
    c3.metric(label="⏱️ Aged stock value", value="₹82K", delta="Stock over 90 days", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Grid Row 2 (3 Columns)
    c4, c5, c6 = st.columns(3)
    c4.metric(label="🏷️ Promo gap", value="126 units", delta="Kartika Sale · 4 days away")
    c5.metric(label="✓ Pending approvals", value="3", delta="Actions need your sign-off")
    c6.metric(label="📊 Total Units Tracked", value=f"{total_units:,}", delta=f"{len(inventory)} Products")
else:
    st.warning("Add a 'Stock' column to calculate inventory metrics.")

left, right = st.columns([1.5, 1])
with left:
    st.subheader("Inventory Explorer")
    st.dataframe(inventory, use_container_width=True, hide_index=True)
with right:
    st.subheader("Stock by size")
    if "Size" in inventory.columns and stock_col:
        chart = inventory.groupby("Size")[stock_col].sum()
        st.bar_chart(chart)
    else:
        st.write("Include 'Size' and 'Stock' columns to see the chart.")

st.subheader("Suggested Actions")
if stock_col and demand_col:
    work = inventory.copy()
    work[stock_col] = pd.to_numeric(work[stock_col], errors="coerce").fillna(0)
    work[demand_col] = pd.to_numeric(work[demand_col], errors="coerce").fillna(0)
    work["Status"] = work.apply(lambda r: "Urgent replenishment" if r[stock_col] <= 0 else ("Review replenishment" if r[stock_col] < r[demand_col] else "Stock looks adequate"), axis=1)
    st.dataframe(work[[c for c in ["Product", "Size", "Store", "Stock", "Weekly Demand", "Status"] if c in work.columns]], use_container_width=True, hide_index=True)
else:
    st.write("Add 'Stock' and 'Weekly Demand' columns for basic replenishment suggestions.")

st.caption("Prototype only: verify recommendations before making purchasing or stock-transfer decisions.")
