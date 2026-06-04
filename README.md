# 📈 DataSight Analytics

**Algorithmic Career Intelligence & Predictive Skill-Gap Dashboard**

DataSight Analytics is an offline, pure-Python Big Data processing ecosystem built to bridge the gap between academic skill sets and real-time market demands. By leveraging machine learning, automated data ingestion, and multidimensional data visualization, the system mathematically calculates a user's market competitiveness, projects AI-driven salary forecasts, and identifies active corporate hiring targets.

---

## 🚀 Live Demo
**https://datasight-analytics.streamlit.app/**

---

## ✨ Core Innovations

* **AI-Driven Financial Forecasting:** Utilizes a pre-trained `scikit-learn` Random Forest Regressor to predict highly personalized market value and salary ROI based on complex skill combinations.
* **Automated Data Ingestion Engine:** Features a standalone `BeautifulSoup4` web scraping pipeline engineered to extract, clean, and synchronize unstructured job market data into structured datasets.
* **Multi-Dimensional Gap Analysis:** Deploys `Plotly` radar (spider-web) charts to visually overlay a user's specific competency cluster against structural market demands.
* **Algorithmic Competency Scoring:** Parses a user's raw technology stack and cross-references it against market datasets using deterministic regex tokenization to generate a precise "Competitiveness Index."
* **Executive Strategy Export:** Features a native PDF generation engine (`FPDF2`) to compile and download a personalized, data-driven career blueprint.
* **Stateless Architecture:** Engineered entirely without external databases or heavy APIs, prioritizing zero-latency in-memory processing via Pandas and Streamlit session states.

---

## 🛠️ Technology Stack

* **Frontend & State Management:** [Streamlit](https://streamlit.io/) (with custom CSS injection)
* **Machine Learning:** [Scikit-Learn](https://scikit-learn.org/) & [Joblib](https://joblib.readthedocs.io/)
* **Data Ingestion (Web Scraping):** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) & Requests
* **Data Processing:** [Pandas](https://pandas.pydata.org/)
* **Data Visualization:** [Plotly](https://plotly.com/python/) & [Altair](https://altair-viz.github.io/)
* **PDF Generation:** [FPDF2](https://pyfpdf.github.io/fpdf2/)

---

## 📂 System Architecture (The 3-Part Ecosystem)

The software is engineered with a strict separation of concerns, operating as a continuous data pipeline:

1. **The Ingestion Layer (`scraper.py`):** An independent pipeline that extracts live market nodes from job boards, cleans the data, and updates the core dataset.
2. **The AI Layer (`train_model.py`):** An offline machine learning script that trains a Random Forest model on the latest dataset, exporting its logic (`.pkl`) for low-latency production use.
3. **The Presentation Layer (`app.py` & `logic.py`):** The user-facing dashboard that loads the AI models into RAM, handles state management, UI rendering, and multidimensional visualization.

---

## 💻 Local Installation & Usage

To run this application locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tanjilhasanemon/DataSight-Analytics.git](https://github.com/tanjilhasanemon/DataSight-Analytics.git)
<<<<<<< HEAD
   cd DataSight-Analytics
=======
   cd DataSight-Analytics
>>>>>>> 82e5187f2bab695be4afb6acc4948e72b39477be
