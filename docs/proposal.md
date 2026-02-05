# Project Proposal: H-1B Visa Employment Policy & Salary Forecaster

## 1. Title and Author

* **Project Title:** H-1B Visa: Employment Policy & Salary Forecaster
* **Prepared for:** UMBC Data Science Master Degree Capstone by Dr. Chaojie (Jay) Wang
* **Author Name:** MOHAMMAD SHOEB AHMED
* **GitHub Repo:** https://github.com/shoeb3/UMBC-DATA606-Capstone/
* **LinkedIn Profile:** https://www.linkedin.com/in/msa2/


---

## 2. Background

### What is it about?
The H-1B visa program is a non-immigrant classification that allows U.S. employers to temporarily employ foreign professionals in "specialty occupations". This project focuses on the **Labor Condition Application (LCA)** phase, where employers must certify to the Department of Labor (DOL) that they will pay the required prevailing wage for the occupation and location.

### Why does it matter?
The program is critical to the U.S. economy, with H-1B holders contributing approximately **$86 billion annually**. Significant policy shifts in **March 2026** have transitioned the selection process toward a **beneficiary-centric model** that prioritizes higher-paid and higher-skilled workers. Understanding these variables is vital for both employers and international professionals navigating a highly competitive labor market.

### Research Questions
1. Can a machine learning model accurately predict the `CASE_STATUS` (Certified vs. Denied) of an H-1B petition based on 2025/2026 regulatory data?
2. How significant is the **Wage Ratio** (offered wage vs. prevailing wage) in determining certification success under current rules?
3. Which specific **job roles** and **geographic regions** show the highest demand and approval rates in the current fiscal year?

---

## 3. Data

### Data Sources
* **Primary Source:** U.S. Department of Labor (DOL) Office of Foreign Labor Certification (OFLC) Performance Data.
* **Direct Link:** [DOL OFLC Performance Data (FY2025/2026)](https://www.dol.gov/agencies/eta/foreign-labor/performance)

### Data Characteristics
* **Data Size:** Approximately 500 MB (merged quarterly files).
* **Data Shape:** ~594,000+ rows and 50+ columns for the 2025 fiscal year.
* **Time Period:** Fiscal Year **2025** (Q1–Q4) and **2026** (Q1).
* **What each row represents:** A single **Labor Condition Application (LCA)** filed by a U.S. employer on behalf of a prospective foreign worker.

### Data Dictionary (Key Columns)

| Column Name | Data Type | Definition | Potential Values |
| :--- | :--- | :--- | :--- |
| **CASE_STATUS** | Categorical | Final determination of the application | Certified, Denied, Withdrawn |
| **EMPLOYER_NAME** | String | Name of the sponsoring U.S. company | Amazon, Microsoft, Infosys, etc. |
| **JOB_TITLE** | String | Occupation title for the beneficiary | Software Developer, Data Scientist, etc. |
| **WAGE_RATE_OF_PAY** | Numerical | Annual salary offered to the worker | $60,000 - $250,000+ |
| **PREVAILING_WAGE** | Numerical | DOL-defined average wage for role/area | Level I to IV benchmarks |
| **WORKSITE_STATE** | Categorical | State where the employee will work | CA, TX, NY, WA, IL, etc. |

* **Target Variable:** `CASE_STATUS` (Binary Classification: Certified vs. Denied).
* **Predictor Features:** `JOB_TITLE`, `WAGE_RATE_OF_PAY`, `PREVAILING_WAGE`, `WORKSITE_STATE`, `EMPLOYER_NAME`, and derived metrics such as "Wage Ratio".

---

### Methodology Justification
I am utilizing **FY2025 and 2026 data** because the H-1B program underwent a structural transition in **2024–2025**. Using older data would train the model on an obsolete random lottery system. Current data reflects the **2026 wage-priority rules**, providing the accuracy required for a modern **Streamlit** success calculator.
