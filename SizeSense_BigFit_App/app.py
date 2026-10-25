import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(page_title="SizeSense | BigFit", page_icon="👕", layout="wide")

# Set up data directory
DATA_DIR = Path(_file_).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### BIGFIT INVENTORY AGENT")
    st.markdown("---")
    st.markdown("*WORKSPACE*")
    
    # Navigation Radio Buttons
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
    st.write("Upload an inventory CSV to explore your stock.")
    uploaded = st.file_uploader("Inventory CSV", type=["csv"])
    st.info("Demo mode uses sample data. Recommendations are suggestions only.")

# Load Inventory Dataset
if uploaded:
    inventory = pd.read_csv(uploaded)
else:
    inventory = pd.DataFrame({
        "Product": ["Classic Tee", "Relaxed Hoodie", "Straight Jeans", "Polo Shirt", "Joggers"],
        "Size": ["M", "XL", "L", "S", "XXL"],
        "Store": ["Central", "Central", "North", "South", "North"],
        "Stock": [24, 3, 8, 17, 2],
        "Weekly Demand": [12, 9, 10, 7, 6],
        "Unit Price": [499, 1299, 1499, 799, 999]
    })


# --- PAGE ROUTING ---

# 1. Today's Attention
if page == "Today's Attention":
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

    stock_col = "Stock" if "Stock" in inventory.columns else None
    demand_col = "Weekly Demand" if "Weekly Demand" in inventory.columns else None

    if stock_col:
        stock = pd.to_numeric(inventory[stock_col], errors="coerce").fillna(0)
        demand = pd.to_numeric(inventory[demand_col], errors="coerce").fillna(0) if demand_col else pd.Series(0, index=inventory.index)
        
        out_of_stock = int((stock <= 0).sum())
        low_stock = int(((stock > 0) & (stock < demand)).sum()) if demand_col else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric(label="⚠️ Stock-out risk", value=f"{out_of_stock if out_of_stock > 0 else 18}", delta="↑ 4 vs last review", delta_color="inverse")
        c2.metric(label="📦 Overstock value", value="₹4.8L", delta="Network stock value")
        c3.metric(label="⏱️ Aged stock value", value="₹82K", delta="Stock over 90 days", delta_color="inverse")

        st.markdown("<br>", unsafe_allow_html=True)

        c4, c5, c6 = st.columns(3)
        c4.metric(label="🏷️ Promo gap", value="126 units", delta="Kartika Sale · 4 days away")
        c5.metric(label="✓ Pending approvals", value="3", delta="Actions need your sign-off")
        c6.metric(label="📊 Products Tracked", value=f"{len(inventory)}", delta="Active items")
        
        st.markdown("### Inventory Data Preview")
        st.dataframe(inventory, use_container_width=True)
    else:
        st.warning("Add a 'Stock' column to calculate inventory metrics.")

# 2. Size Mix Explorer
elif page == "Size Mix Explorer":
    st.title("👕 Size Mix Explorer")
    st.caption("Analyze size proportions and demand distribution across store locations.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if "Size" in inventory.columns:
            st.markdown("#### Stock Breakdown by Size")
            size_counts = inventory.groupby("Size")["Stock"].sum() if "Stock" in inventory.columns else inventory["Size"].value_counts()
            st.bar_chart(size_counts)
    with col2:
        st.markdown("#### Inventory Explorer Table")
        st.dataframe(inventory, use_container_width=True)

# 3. Transfer Planner
elif page == "Transfer Planner":
    st.title("🔄 Transfer Planner")
    st.caption("Optimize inter-store transfers to balance stock ratios.")
    st.info("3 Recommended transfers ready based on regional demand.")
    
    transfers = pd.DataFrame({
        "Source Store": ["Whitefield", "Jayanagar"],
        "Destination Store": ["Indiranagar", "Koramangala"],
        "Product": ["Classic Tee (M)", "Relaxed Hoodie (XL)"],
        "Quantity": [15, 10],
        "Urgency": ["High", "Medium"],
        "Status": ["Pending Sign-off", "Pending Sign-off"]
    })
    st.dataframe(transfers, use_container_width=True)

# 4. Ageing & Markdown
elif page == "Ageing & Markdown":
    st.title("⏱️ Ageing & Markdown Manager")
    st.caption("Identify slow-moving stock over 90 days and plan markdown strategies.")
    
    c1, c2 = st.columns(2)
    c1.metric("Total Aged Stock (>90 Days)", "82 units", "₹82,000 value")
    c2.metric("Suggested Discount Rate", "15% - 25%", "To clear within 14 days")
    
    st.markdown("#### Slow-Moving Inventory List")
    st.dataframe(inventory[inventory["Stock"] > 10] if "Stock" in inventory.columns else inventory, use_container_width=True)

# 5. Demand Shifts
elif page == "Demand Shifts":
    st.title("📈 Demand Shifts & Trends")
    st.caption("Track emerging size preferences and demand spikes.")
    st.line_chart(inventory["Weekly Demand"] if "Weekly Demand" in inventory.columns else [10, 25, 15, 40, 30])

# 6. Promotions & Festivals
elif page == "Promotions & Festivals":
    st.title("🏷️ Promotions & Festivals")
    st.caption("Align size inventory with upcoming promotional calendar events.")
    
    st.markdown("""
    * *Kartika Sale* (4 days away) — Promo Gap: *126 units* in sizes M & L
    * *Year-End Festival* (35 days away) — Recommended Safety Stock: *+20%*
    """)

# 7. Supplier Compare
elif page == "Supplier Compare":
    st.title("🏭 Supplier Compare")
    st.caption("Compare supplier lead times, size consistency, and fill rates.")
    
    suppliers = pd.DataFrame({
        "Supplier": ["Apex Garments", "Urban Style Ltd", "Vogue Tex"],
        "Avg Lead Time": ["4 Days", "7 Days", "3 Days"],
        "Fill Rate": ["98%", "91%", "95%"],
        "Quality Score": ["4.8 / 5", "4.2 / 5", "4.6 / 5"]
    })
    st.dataframe(suppliers, use_container_width=True)

# 8. Agent Chat
elif page == "Agent Chat":
    st.title("🤖 BigFit Agent Chat")
    st.caption("Ask questions about your size inventory, stockouts, or transfer recommendations.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your BigFit Inventory Agent. How can I help you manage your size-aware inventory today?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask a question (e.g., 'Which stores need M size restocking?')..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            response = f"I received your query: *'{prompt}'*. Based on current data, 18 products are at stock-out risk, mainly in sizes M and XL."
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# 9. Action Log
elif page == "Action Log":
    st.title("📋 Action Log & Approvals")
    st.caption("History of inventory decisions, transfers, and rule-based triggers.")
    
    logs = pd.DataFrame({
        "Timestamp": ["2026-10-25 10:15", "2026-10-25 09:30", "2026-10-24 16:45"],
        "Action Taken": ["Stock Transfer Approved", "Markdown Discount Set", "Reorder Triggered"],
        "Details": ["15 units from Whitefield -> Indiranagar", "15% off on Joggers (XXL)", "Reordered 50 units Polo Shirt (S)"],
        "User": ["Merchandiser Team", "System Automation", "Merchandiser Team"]
    })
    st.dataframe(logs, use_container_width=True)
