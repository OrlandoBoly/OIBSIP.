            Retail Sales — Exploratory Data Analysis & Dashboard
A end-to-end data analytics project performing Exploratory Data Analysis (EDA) on a retail sales dataset, culminating in an interactive Streamlit dashboard with Business Overview and Customer RFM Analysis pages.

                Project Overview
This project uncovers patterns, trends, and actionable insights from retail transaction data to help businesses make informed decisions. It covers the full analytics pipeline — from raw data loading and cleaning through to an interactive web dashboard.

               Project Structure
  1. retail_analysis.ipynb    -    Main Jupyter notebook (EDA)
  2. app.py                   -   Streamlit dashboard app
  3. retail_sales_dataset.csv -   Dataset

                Dataset
The dataset contains retail transaction records with the following columns:
ColumnDescriptionTransaction IDUnique transaction identifierDateDate of purchaseCustomer IDUnique customer identifierGenderCustomer genderAgeCustomer ageProduct CategoryCategory of purchased productQuantityNumber of units purchasedPrice per UnitUnit price of the productTotal AmountTotal transaction value

                 Key Analysis Areas

1. Data Loading & Cleaning — Load and inspect the dataset, handle missing values and data types
2. Descriptive Statistics — Mean, median, mode, and standard deviation across key metrics
3. Time Series Analysis — Sales trends over time using line plots
4. Customer & Product Analysis — Demographics breakdown and purchasing behaviour by category
5. Visualization — Bar charts, line plots, and heatmaps
6. Recommendations — Actionable insights drawn from the EDA findings


              Dashboard
Built with Streamlit, the dashboard features two pages:

1. Business Overview — Revenue trends, top-performing categories (e.g. Electronics with $156,905 revenue), and key KPIs
2. Customer RFM Analysis — Recency, Frequency, and Monetary segmentation of customers


             Tech Stack

1. Python 3.13 
2. Pandas — data manipulation 
3. Matplotlib / Seaborn — visualisation 
4. Streamlit — interactive dashboard 
5. Jupyter Notebook — EDA environment


           Objectives

1. Apply EDA techniques to a real-world retail dataset
2. Derive meaningful insights from customer and product data
3. Build and deploy an interactive data dashboard
4. Practice end-to-end data analytics workflow
