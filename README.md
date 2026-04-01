# 📦 Supply Chain Network Optimization Dashboard

A dynamic and interactive **Supply Chain Optimization system** built using **Operations Research (Linear Programming)** and **Streamlit**.

This project helps optimize shipment planning between **Factories → Warehouses → Customers** by minimizing transportation costs while satisfying real-world constraints.

---

## 🚀 Features

- 🔄 Dynamic network size (user-defined number of factories, warehouses, customers)
- 📥 User input for supply, demand, capacity, and costs
- 📊 Optimization using Linear Programming (PuLP)
- 📈 Graphical visualization:
  - Shipment bar charts
  - Network flow diagram (no overlapping edges)
- 💰 Displays optimal transportation cost
- ⚡ Real-time computation and visualization

---

## 🧠 Optimization Model

The system minimizes total transportation cost:

Minimize:

Z = Σ (Factory → Warehouse Cost × Shipment)  
  + Σ (Warehouse → Customer Cost × Shipment)

### Subject to:

- Supply constraints (Factories)
- Demand constraints (Customers)
- Flow conservation (Warehouses)
- Capacity constraints (Warehouses)

---

## 🖥️ Tech Stack

- **Python**
- **Streamlit** (Dashboard UI)
- **PuLP** (Linear Programming)
- **Pandas** (Data handling)
- **Matplotlib** (Charts)
- **NetworkX** (Graph visualization)

---

## 📂 Project Structure

```

Supply-Chain-Optimization/
│
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
└── README.md           # Project documentation

````

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pranavpatil2316/supply_chain
cd supply_chain
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python -m streamlit run app.py
```

### 4️⃣ Open in Browser

```
http://localhost:8501
```

---

## 📊 How It Works

1. Select number of:

   * Factories
   * Warehouses
   * Customers

2. Enter:

   * Supply
   * Demand
   * Capacity
   * Transportation costs

3. Click **"Run Optimization"**

4. View:

   * Optimal shipment plan
   * Total cost
   * Graphical visualization

---

## 🎯 Use Cases

* Logistics & Supply Chain Optimization
* Transportation Planning
* Operations Research Projects
* Academic Demonstrations
* Decision Support Systems

---

## 🔥 Key Highlights

* Dynamic scalable model (not fixed size)
* Clean visualization with non-overlapping network graph
* Real-world constraint modeling
* Interactive dashboard for decision-making

---


## 💼 Resume Description

**Supply Chain Network Optimization (Operations Research Project)**

* Developed a dynamic multi-echelon supply chain model using Linear Programming
* Built an interactive dashboard using Streamlit for real-time decision-making
* Optimized transportation cost under supply, demand, and capacity constraints
* Visualized network flow using graph-based techniques

---
