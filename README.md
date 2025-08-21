# Data Engineering Challenge 🚀

## Indiamart Scraper 🛠️

A Scrapy-based web scraper for extracting product data from **Indiamart** and saving it into **MongoDB Atlas**.  
This project also demonstrates **ETL (Extract–Transform–Load)** and **EDA (Exploratory Data Analysis)** workflows.

---

## ✨ Features
- Scrapes product listings from [Indiamart](https://dir.indiamart.com)
- Extracts details like:
  - ✅ Product name  
  - ✅ Price  
  - ✅ Company  
  - ✅ Location  
  - ✅ Address  
  - ✅ Product link  
- Handles pagination automatically  
- Stores data directly into **MongoDB Atlas**  
- Can also export results to **JSON/CSV**  
- Configurable **search query** & **city**  
- Includes **ETL pipeline** and **EDA script** for insights  

---

## 📂 Project Structure

```bash
data_engineering_challenge/
│
├── tutorial/                  # Scrapy project
│   ├── spiders/
│   │   ├── indiamart.py       # Main spider
│   │   ├── __init__.py
│   ├── items.py               # Item schema
│   ├── middlewares.py         # (Optional) custom middlewares
│   ├── pipelines.py           # MongoDB pipeline integration
│   ├── settings.py            # Scrapy settings
│
├── data/                      # Output data
│   ├── raw/                   # Raw scraped data
│   ├── processed/             # Cleaned data
│
├── etl/
│   ├── etl_pipeline.py        # ETL (cleaning & transformation)
│
├── eda/
│   ├── product_eda.py         # Exploratory Data Analysis
│   ├── product_eda.ipynb      # (Optional) Jupyter notebook
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
