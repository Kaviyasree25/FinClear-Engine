# FinClear: Intelligent Post-Trade Settlement & Netting Engine

##  Overview
FinClear is an advanced simulation of a **Post-Trade Financial Infrastructure** system. It demonstrates how a central clearinghouse (like DTCC) can optimize market liquidity through **Multilateral Netting** and manage risk using **AI-driven Anomaly Detection**.

##  Key Features
- **Kafka-Style Ingestion:** Simulates high-volume trade streams from various counterparties (JPMorgan, Goldman Sachs, etc.).
- **AI Risk Engine:** Uses an **Isolation Forest (Machine Learning)** model to detect "Fat-Finger" errors or fraudulent trade patterns before they settle.
- **Multilateral Netting Algorithm:** Aggregates thousands of individual transactions into single net obligations, reducing required liquidity by up to 90%.
- **T+1 Settlement Logic:** Implements the modern industry standard for next-day trade finalization.

##  Tech Stack
- **Language:** Python 3.10+
- **Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn
- **Visualization:** Plotly, Streamlit

##  Impact
By applying netting logic, the system demonstrates a significant reduction in **Gross Settlement Volume**, minimizing the "Settlement Risk" and operational overhead for participating banks.
