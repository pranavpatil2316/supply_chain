import streamlit as st
import pandas as pd
import pulp
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(page_title="Supply Chain Optimizer", layout="wide")

st.title("📦 Supply Chain Network Optimization Dashboard")

# -----------------------------
# USER INPUT (NETWORK SIZE)
# -----------------------------
st.sidebar.header("⚙️ Network Size")

num_factories = st.sidebar.number_input("Number of Factories", 1, 10, 2)
num_warehouses = st.sidebar.number_input("Number of Warehouses", 1, 10, 2)
num_customers = st.sidebar.number_input("Number of Customers", 1, 10, 2)

factories = [f"F{i+1}" for i in range(num_factories)]
warehouses = [f"W{i+1}" for i in range(num_warehouses)]
customers = [f"C{i+1}" for i in range(num_customers)]

# -----------------------------
# INPUT DATA
# -----------------------------
st.sidebar.header("📥 Input Data")

# Supply
st.sidebar.subheader("Factory Supply")
supply = {}
for f in factories:
    supply[f] = st.sidebar.number_input(f"Supply {f}", value=100)

# Capacity
st.sidebar.subheader("Warehouse Capacity")
capacity = {}
for w in warehouses:
    capacity[w] = st.sidebar.number_input(f"Capacity {w}", value=120)

# Demand
st.sidebar.subheader("Customer Demand")
demand = {}
for c in customers:
    demand[c] = st.sidebar.number_input(f"Demand {c}", value=80)

# Costs
st.sidebar.subheader("Cost: Factory → Warehouse")
cost_fw = {}
for f in factories:
    for w in warehouses:
        cost_fw[(f, w)] = st.sidebar.number_input(f"{f} → {w}", value=5)

st.sidebar.subheader("Cost: Warehouse → Customer")
cost_wc = {}
for w in warehouses:
    for c in customers:
        cost_wc[(w, c)] = st.sidebar.number_input(f"{w} → {c}", value=5)

# -----------------------------
# RUN OPTIMIZATION
# -----------------------------
if st.button("🚀 Run Optimization"):

    model = pulp.LpProblem("SupplyChain", pulp.LpMinimize)

    # Decision variables
    x = pulp.LpVariable.dicts("FW", cost_fw.keys(), lowBound=0)
    y = pulp.LpVariable.dicts("WC", cost_wc.keys(), lowBound=0)

    # Objective
    model += (
        pulp.lpSum(cost_fw[i] * x[i] for i in cost_fw) +
        pulp.lpSum(cost_wc[j] * y[j] for j in cost_wc)
    )

    # Constraints
    for f in factories:
        model += pulp.lpSum(x[(f, w)] for w in warehouses) <= supply[f]

    for c in customers:
        model += pulp.lpSum(y[(w, c)] for w in warehouses) >= demand[c]

    for w in warehouses:
        model += (
            pulp.lpSum(x[(f, w)] for f in factories) ==
            pulp.lpSum(y[(w, c)] for c in customers)
        )

    for w in warehouses:
        model += pulp.lpSum(x[(f, w)] for f in factories) <= capacity[w]

    model.solve()

    st.success("✅ Optimization Completed!")

    # -----------------------------
    # RESULTS
    # -----------------------------
    results_fw = pd.DataFrame(
        [(i, j, x[(i, j)].value()) for (i, j) in cost_fw],
        columns=["Factory", "Warehouse", "Quantity"]
    )

    results_wc = pd.DataFrame(
        [(j, k, y[(j, k)].value()) for (j, k) in cost_wc],
        columns=["Warehouse", "Customer", "Quantity"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Factory → Warehouse")
        st.dataframe(results_fw)

    with col2:
        st.subheader("🚚 Warehouse → Customer")
        st.dataframe(results_wc)

    st.subheader("💰 Total Cost")
    st.write(f"Optimal Cost = {pulp.value(model.objective)}")

    # -----------------------------
    # BAR CHART
    # -----------------------------
    st.subheader("📊 Shipment Chart")

    fig, ax = plt.subplots(figsize=(8, 4))

    labels = results_fw["Factory"] + "-" + results_fw["Warehouse"]
    values = results_fw["Quantity"]

    bars = ax.bar(labels, values)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f'{round(height,1)}',
                ha='center', va='bottom')

    plt.xticks(rotation=30)
    plt.xlabel("Routes")
    plt.ylabel("Quantity")

    st.pyplot(fig)

    # -----------------------------
    # NETWORK GRAPH (FINAL FIX)
    # -----------------------------
    st.subheader("🌐 Network Flow")

    G = nx.DiGraph()

    # Zig-zag positioning
    for i, f in enumerate(factories):
        G.add_node(f, pos=(0, i * 3))

    for i, w in enumerate(warehouses):
        G.add_node(w, pos=(2, i * 3 + 1.5))

    for i, c in enumerate(customers):
        G.add_node(c, pos=(4, i * 3))

    # Add edges
    for (f, w) in cost_fw:
        flow = x[(f, w)].value()
        if flow > 0:
            G.add_edge(f, w, weight=round(flow, 1))

    for (w, c) in cost_wc:
        flow = y[(w, c)].value()
        if flow > 0:
            G.add_edge(w, c, weight=round(flow, 1))

    pos = nx.get_node_attributes(G, 'pos')
    edge_labels = nx.get_edge_attributes(G, 'weight')

    fig2, ax2 = plt.subplots(figsize=(12, 6))

    node_colors = []
    for node in G.nodes():
        if node.startswith("F"):
            node_colors.append("lightgreen")
        elif node.startswith("W"):
            node_colors.append("orange")
        else:
            node_colors.append("lightblue")

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3000)
    nx.draw_networkx_labels(G, pos)

    # Split edges (key fix)
    edges_fw = [(u, v) for u, v in G.edges() if u.startswith("F")]
    edges_wc = [(u, v) for u, v in G.edges() if u.startswith("W")]

    nx.draw_networkx_edges(G, pos, edgelist=edges_fw,
                           connectionstyle='arc3,rad=0.2',
                           arrows=True)

    nx.draw_networkx_edges(G, pos, edgelist=edges_wc,
                           connectionstyle='arc3,rad=-0.2',
                           arrows=True)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    st.pyplot(fig2)