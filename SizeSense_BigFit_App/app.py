import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="SizeSense | BigFit", page_icon="👕", layout="wide")
st.title("👕 SizeSense — BigFit Inventory Agent")
st.caption("Size-aware inventory monitoring • Demo prototype")

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

with st.sidebar:
    st.header("Controls")
    st.write("Upload an inventory CSV to explore your stock.")
    uploaded = st.file_uploader("Inventory CSV", type=["csv"])
    st.info("Demo mode uses sample data. Recommendations are suggestions only.")

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

st.subheader("Today's Attention")
c1, c2, c3, c4 = st.columns(4)
stock_col = "Stock" if "Stock" in inventory.columns else None
demand_col = "Weekly Demand" if "Weekly Demand" in inventory.columns else None
if stock_col:
    c1.metric("Products tracked", len(inventory))
    c2.metric("Units in stock", int(pd.to_numeric(inventory[stock_col], errors="coerce").fillna(0).sum()))
    if demand_col:
        stock = pd.to_numeric(inventory[stock_col], errors="coerce").fillna(0)
        demand = pd.to_numeric(inventory[demand_col], errors="coerce").fillna(0)
        c3.metric("Low-stock items", int((stock < demand).sum()))
        c4.metric("Out of stock", int((stock <= 0).sum()))
    else:
        c3.metric("Low-stock items", "—")
        c4.metric("Out of stock", int((pd.to_numeric(inventory[stock_col], errors="coerce").fillna(0) <= 0).sum()))
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
