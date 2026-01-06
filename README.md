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

<img width="1918" height="1020" alt="Screenshot 2026-01-06 104440" src="https://github.com/user-attachments/assets/223cc5d5-45b5-40a1-8ff4-1d188ee10a76" />
<img width="1918" height="1020" alt="Screenshot 2026-01-06 104440" src="https://github.com/user-attachments/assets/5351b355-bfa3-482b-a811-e1150da9894e" />
<img width="1918" height="1016" alt="Screenshot 2026-01-06 104652" src="https://github.com/user-attachments/assets/eca96354-018f-4925-ac9a-4741d79d4522" />
<img width="1918" height="1018" alt="Screenshot 2026-01-06 104641" src="https://github.com/user-attachments/assets/dba44581-f593-4bfa-b4a2-7bcef1aecb98" />
<img width="1918" height="1020" alt="Screenshot 2026-01-06 104545" src="https://github.com/user-attachments/assets/6e2d0c22-ccd5-4760-9f9f-7aa1a977644a" />

