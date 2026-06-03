# 📈 DataSight Analytics

**Algorithmic Career Intelligence & Skill-Gap Analysis Dashboard**

DataSight Analytics is an offline, pure-Python data processing engine and interactive dashboard built to bridge the gap between academic skill sets and real-time market demands. By processing thousands of real-world job postings, the system mathematically calculates a user's market competitiveness, projects potential salary ROI for upskilling, and identifies active corporate hiring targets.

---

## 🚀 Live Demo
**https://datasight-analytics.streamlit.app/**

---

## ✨ Core Features

* **Algorithmic Competency Scoring:** Parses a user's raw technology stack and cross-references it against market datasets to generate a precise "Market Competitiveness Index."
* **Salary ROI Predictor:** Dynamically calculates the user's median market value and projects the exact financial impact (ROI) of closing their primary skill deficit.
* **Interactive Data Visualization:** Utilizes `Altair` to render sleek, grid-less visualizations of real-time core technology demands.
* **Corporate Matchmaker:** Extracts and ranks top hiring entities actively seeking the user's specific competency cluster.
* **Executive Strategy Export:** Features a native PDF generation engine (`FPDF2`) to compile and download a personalized, data-driven career blueprint.
* **Premium UI/UX:** Custom CSS injection completely overhauls the default Streamlit interface, delivering a modern, deep-slate "Glassmorphism" aesthetic.

---

## 🛠️ Technology Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (with custom CSS injection)
* **Backend Engine:** Pure Python
* **Data Processing:** [Pandas](https://pandas.pydata.org/)
* **Data Visualization:** [Altair](https://altair-viz.github.io/)
* **PDF Generation:** [FPDF2](https://pyfpdf.github.io/fpdf2/)

---

## 📂 System Architecture

The software is engineered with a strict separation of concerns, ensuring high performance without relying on external APIs.

* `app.py`: The presentation layer. Handles state management, UI rendering, caching, and PDF generation.
* `logic.py`: The processing engine. Handles regex tokenization, DataFrame filtering, and mathematical gap analysis.
* `dataset.csv`: The compressed market intelligence data source.

---

## 💻 Local Installation & Usage

To run this application locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/DataSight-Analytics.git](https://github.com/YOUR_GITHUB_USERNAME/DataSight-Analytics.git)
   cd DataSight-Analytics