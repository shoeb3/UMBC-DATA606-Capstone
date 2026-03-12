# Predicting H-1B Visa Approval Outcomes and Salary Competitiveness Using U.S. Labor Market Data

## 1. Title and Author

| Field | Detail |
|-------|--------|
| **Project Title** | Predicting H-1B Visa Approval Outcomes and Salary Competitiveness Using U.S. Labor Market Data |
| **Course** | UMBC Data Science Master Degree Capstone – DATA 606 |
| **Advisor** | Dr. Chaojie (Jay) Wang |
| **Author** | Mohammad Shoeb Ahmed |
| **GitHub Repo** | https://github.com/shoeb3/UMBC-DATA606-Capstone/ |
| **LinkedIn** | https://www.linkedin.com/in/msa2/ |

---

## 2. Background

### 2.1 What is it about?

The H-1B visa is the United States' primary non-immigrant classification for foreign nationals employed in "specialty occupations" — positions that typically require at least a bachelor's degree in a specific technical or professional field such as computer science, engineering, medicine, or finance. Before an employer can file an H-1B petition with U.S. Citizenship and Immigration Services (USCIS), they must first obtain a certified **Labor Condition Application (LCA)** from the U.S. Department of Labor (DOL).

The LCA certification process verifies three key employer commitments:
1. The employer will pay at least the **prevailing wage** — the DOL-defined average market rate for the occupation and geographic area.
2. The working conditions of the H-1B worker will not adversely affect similarly employed U.S. workers.
3. There is no ongoing strike or lockout in the occupation at the place of employment.

This project focuses entirely on the LCA stage. The dataset used is the DOL's publicly released **OFLC Performance Data**, which records every LCA petition filed during a fiscal year, including the employer, job title, offered wage, prevailing wage, location, and final case determination.

### 2.2 Why does it matter?

The H-1B program is one of the most important and contested workforce policy mechanisms in the United States:

- H-1B workers contribute an estimated **$86 billion annually** to U.S. GDP.
- The program employs hundreds of thousands of professionals in software engineering, data science, medicine, and research.
- Demand consistently exceeds the annual **85,000 cap** (65,000 regular + 20,000 for U.S. master's degree holders), making the lottery one of the most consequential selection mechanisms in the labor market.

**Major Policy Shift — March 2026:** The H-1B program underwent a structural overhaul between 2024 and 2026. The new **beneficiary-centric model** fundamentally changed how registrations are selected in the lottery:

- Previously: selection was a purely random lottery among all valid registrations.
- Now: petitions offering **higher wages relative to the prevailing wage** receive statistical priority in selection.

This means the **Wage Ratio** (offered wage divided by prevailing wage) has become the single most strategically important variable in the H-1B process. Employers who offer above-market wages gain a measurable advantage. IT staffing firms that historically relied on high-volume, lower-wage petitions now face systematic disadvantage.

This policy context creates a clear, real-world use case for machine learning: **predict whether an LCA will be certified and quantify how salary competitiveness affects that outcome**, enabling both employers and foreign professionals to make data-driven decisions.

### 2.3 Research Questions

1. **Prediction:** Can a machine learning model accurately predict the `CASE_STATUS` (Certified vs. Not Certified) of an H-1B LCA petition using features available at filing time?
2. **Wage Competitiveness:** How significant is the **Wage Ratio** (offered wage / prevailing wage) in determining certification success under the 2025–2026 regulatory framework?
3. **Geographic & Occupational Patterns:** Which U.S. states and job roles show the highest demand and approval rates in FY2025?
4. **Employer Behavior:** Do IT staffing firms show systematically different wage and certification patterns compared to Big Tech companies, and how does this interact with the new 2026 rules?

---

## 3. Data

### 3.1 Data Sources

- **Primary Source:** U.S. Department of Labor (DOL), Office of Foreign Labor Certification (OFLC) Performance Data
- **Direct Link:** [DOL OFLC Performance Data (FY2025)](https://www.dol.gov/agencies/eta/foreign-labor/performance)
- **Format:** Microsoft Excel (.xlsx), published quarterly
- **Access:** Publicly available — no authentication required

The DOL OFLC dataset is the authoritative, complete record of every LCA filing. Because disclosure is mandated by federal law, the dataset has no sampling bias — every petition is recorded.

### 3.2 Data Characteristics

| Property | Detail |
|----------|--------|
| **Files Used** | FY2025 Q1, Q2, Q3, Q4 |
| **Q1 Rows** | 107,414 |
| **Q2 Rows** | 132,133 |
| **Q3 Rows** | 238,425 |
| **Q4 Rows** | 118,580 |
| **Combined Total** | 596,552 petitions |
| **After H-1B Filter** | 582,271 petitions |
| **Columns** | ~98 (varies slightly by quarter) |
| **Time Period** | October 2024 – September 2025 |
| **Row Granularity** | One row = one LCA petition |

### 3.3 Data Dictionary — Key Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `CASE_NUMBER` | String | Unique DOL case identifier | I-200-24366-578757 |
| `CASE_STATUS` | Categorical | Final DOL determination | Certified, Denied, Withdrawn |
| `RECEIVED_DATE` | Date | Date DOL received the petition | 2024-10-15 |
| `DECISION_DATE` | Date | Date DOL issued a decision | 2024-10-20 |
| `VISA_CLASS` | Categorical | Visa program type | H-1B, H-1B1, E-3 |
| `EMPLOYER_NAME` | String | Sponsoring company name | Amazon, Infosys, Google |
| `EMPLOYER_STATE` | Categorical | State where employer is located | CA, TX, NY |
| `JOB_TITLE` | String | Free-text occupation title as filed | Software Developer |
| `SOC_TITLE` | String | DOL standardized occupation name | Software Developers |
| `FULL_TIME_POSITION` | Categorical | Full-time or part-time role | Y / N |
| `WAGE_RATE_OF_PAY_FROM` | Numeric | Offered salary (single value in this dataset) | 110000 |
| `WAGE_UNIT_OF_PAY` | Categorical | Pay frequency of offered wage | Year, Month, Hour |
| `PREVAILING_WAGE` | Numeric | DOL-mandated minimum wage for this role and location | 95000 |
| `PW_UNIT_OF_PAY` | Categorical | Pay frequency of prevailing wage | Year |

**Note:** `WAGE_RATE_OF_PAY_TO` does not exist in this dataset. Employers in FY2025 report a single wage value, not a range.

**Engineered Features (created during EDA):**

| Feature | Formula | Purpose |
|---------|---------|---------|
| `TARGET` | 1 if `CASE_STATUS == 'Certified'`, else 0 | Binary classification label |
| `ANNUAL_WAGE` | `WAGE_RATE_OF_PAY_FROM × pay-period multiplier` | Wage normalized to annual |
| `ANNUAL_PREVAILING_WAGE` | `PREVAILING_WAGE` (already annual in DOL data) | Benchmark for comparison |
| `WAGE_RATIO` | `ANNUAL_WAGE / ANNUAL_PREVAILING_WAGE` | Core policy metric under 2026 rules |
| `PROCESSING_DAYS` | `DECISION_DATE − RECEIVED_DATE` | Days from filing to decision |
| `IS_FULL_TIME` | 1 if `FULL_TIME_POSITION == 'Y'`, else 0 | Binary full-time indicator |
| `WAGE_ABOVE_PREVAILING` | 1 if `ANNUAL_WAGE > ANNUAL_PREVAILING_WAGE` | Above-market wage flag |
| `ANNUAL_WAGE_CAPPED` | `ANNUAL_WAGE` clipped at 1st–99th percentile | Outlier-handled wage for modeling |
| `QUARTER` | Derived from `RECEIVED_DATE` | Calendar quarter of filing |

**Target Variable:** `TARGET` — Binary: **Certified (1)** vs. **Not Certified (0)**

### 3.4 Why FY2025 Data?

FY2025 data is used exclusively because:

1. **Regulatory alignment:** The 2024–2026 H-1B overhaul replaced the random lottery with a wage-priority model. Training on pre-2024 data would model an obsolete system.
2. **Recency:** The end deliverable is a real-time Streamlit prediction tool — predictions from old data would mislead current applicants.
3. **Schema stability:** Recent quarters have the most complete and consistent column structures.

---

## 4. Exploratory Data Analysis (EDA)

### 4.1 Data Cleansing & Preparation

The raw dataset required eight distinct cleaning steps before analysis could begin.

#### Step 1 — Load and Merge Quarterly Files

All four FY2025 quarterly Excel files were loaded individually and concatenated into a single master DataFrame. A `QUARTER` column (1–4) was later derived from `RECEIVED_DATE` to preserve the temporal origin of each record.

```
Q1: 107,414 rows  |  Q2: 132,133 rows  |  Q3: 238,425 rows  |  Q4: 118,580 rows
Combined: 596,552 rows x 100 columns
```

#### Step 2 — Scope Filter: H-1B Only

The raw LCA dataset includes multiple visa types: H-1B, H-1B1 (Chile/Singapore treaty workers), and E-3 (Australian professionals). All non-H-1B records were removed.

```
After H-1B filter: 582,271 rows
```

#### Step 3 — Binary Target Variable Encoding

The raw `CASE_STATUS` field contains four possible values. For binary classification, these were collapsed as follows:

| Original Status | Count | Target |
|----------------|-------|--------|
| Certified | 539,444 | 1 |
| Certified - Withdrawn | 30,111 | 0 |
| Withdrawn | 9,211 | 0 |
| Denied | 3,505 | 0 |

Only a `Certified` outcome means the petition achieved its purpose. `Certified - Withdrawn` cases (employer later cancelled despite approval) are coded 0 because the position was ultimately not filled.

#### Step 4 — Missing Value Audit and Column Dropping

A full null-value audit was performed. Columns exceeding 50% missing data were dropped entirely. Identifier columns with no predictive value were also removed.

- Columns dropped due to >50% missing: ~8–12 columns (administrative optional fields)
- Also dropped: `CASE_NUMBER`, `VISA_CLASS`, `PREPARER_LAST_NAME`, `PREPARER_FIRST_NAME`, `PREPARER_MIDDLE_INITIAL`
- **No values were imputed or filled** — the strategy was to drop uninformative columns and retain only analytical features.

#### Step 5 — Data Type Corrections

- Date columns converted from string/object to `datetime64` using `pd.to_datetime(errors='coerce')`
- Wage columns cleaned by stripping `$` and `,` characters, then cast to `float64`
- Invalid/unparseable values silently converted to `NaN` via `errors='coerce'`

#### Step 6 — Wage Annualization

DOL data stores wages in multiple pay period units. All wages were converted to annual equivalents:

| Pay Unit | Multiplier Applied |
|----------|--------------------|
| Year | × 1 |
| Month | × 12 |
| Bi-Weekly | × 26 |
| Week | × 52 |
| Hour | × 2,080 |

#### Step 7 — Feature Engineering

Four new analytical features were derived:

- **`WAGE_RATIO`** — offered wage divided by prevailing wage; the central metric under 2026 lottery rules
- **`PROCESSING_DAYS`** — integer days from `RECEIVED_DATE` to `DECISION_DATE`
- **`IS_FULL_TIME`** — binary flag from `FULL_TIME_POSITION`
- **`WAGE_ABOVE_PREVAILING`** — binary flag indicating whether the employer offers above the DOL minimum
- **`QUARTER`** — integer 1–4, derived from `RECEIVED_DATE` month

#### Step 8 — Outlier Handling

Extreme wage values (data-entry errors such as $1/year or $10M/year) were identified using the 1st and 99th percentiles. Wages were Winsorized at these bounds and stored in `ANNUAL_WAGE_CAPPED`. The raw column is preserved for reference.

```
Wages below ~$X and above ~$Y were capped (exact values printed at runtime)
Final cleaned dataset: 582,271 rows
Certified: 539,444 (92.6%)  |  Not Certified: 42,827 (7.4%)
```

---

### 4.2 Visualizations and Interpretations

#### 4.2.1 Missing Value Audit

A horizontal bar chart displays the percentage of missing values for each column, with a red dashed line marking the 50% drop threshold. Columns to the right of this line were removed from the dataset.

**Interpretation:** High-null columns are exclusively optional administrative fields that employers are not legally required to complete. Their absence is structural, not random — dropping them is the correct approach rather than attempting imputation.

---

#### 4.2.2 Target Variable Distribution

A side-by-side bar chart and pie chart show the certified vs. not-certified split.

| Outcome | Count | Percentage |
|---------|-------|------------|
| Certified | 539,444 | 92.6% |
| Not Certified | 42,827 | 7.4% |

**Interpretation:** The class imbalance is severe. A naive model that always predicts "Certified" would achieve 92.6% accuracy while being completely useless for identifying denied cases. Model evaluation must rely on F1-score, AUC-ROC, and Precision-Recall rather than accuracy.

---

#### 4.2.3 Case Status Breakdown (All Four Categories)

A bar chart shows all raw `CASE_STATUS` values before binarization.

**Interpretation:** Pure denials (3,505 cases, 0.6%) are extremely rare. The DOL's LCA function is primarily administrative wage-compliance checking — it almost never rejects an application outright. The actual competitive bottleneck is the USCIS lottery, not this stage. Under the 2026 rules, winning that lottery depends on wage ratio.

---

#### 4.2.4 Annual Wage Distribution

A histogram with KDE line shows the overall wage distribution. A KDE density comparison shows certified vs. denied cases on the same axis.

- Median offered wage: approximately **$119,000**
- Distribution is right-skewed, pulled upward by physician and research scientist salaries
- The two outcome groups show visible separation, with not-certified cases clustering at lower wages

**Interpretation:** Higher wages are associated with certification. This relationship is expected — employers offering below the prevailing wage are the ones most at risk of denial.

---

#### 4.2.5 Wage Ratio Analysis

A histogram of wage ratio distribution (filtered to 0.5–3.0) and a box plot comparing certified vs. denied groups.

- Certified median wage ratio: ~1.05–1.10 (above prevailing wage)
- Denied median wage ratio: near or below 1.00

The dashed red line at 1.0 marks the prevailing wage threshold.

**Interpretation:** This is the most policy-relevant visualization in the project. Certified petitions consistently offer above the prevailing wage. Under the 2026 beneficiary-centric rules, this ratio is the explicit lottery selection criterion — making it the most important predictive feature in the model.

---

#### 4.2.6 Geographic Analysis (Top 20 States)

Side-by-side bar charts: application volume by state, and certification rate by state.

**Top states by volume:** California, Texas, New Jersey, New York, Washington

**Interpretation:** Volume concentration reflects tech industry geography. Certification rates are broadly uniform across states because the DOL applies the same wage standard nationally. However, state is still a valuable model feature because it correlates with prevailing wage levels — a Software Developer in San Jose has a much higher prevailing wage than in Texas, which affects wage ratio calculations.

---

#### 4.2.7 Top 20 Sponsoring Employers

Two charts: petition volume by employer, and median offered wage by employer.

**Top by volume:** Infosys, TCS, Wipro, Cognizant, HCL (IT staffing firms)

**Top by median wage:** Google, Amazon, Microsoft, Meta (Big Tech)

**Interpretation:** This is the most practically significant finding. IT staffing companies dominate volume but pay near the DOL minimum. Big Tech pays well above it. The 2026 lottery directly penalizes the first group and rewards the second. Understanding this split is core to the project's policy contribution.

---

#### 4.2.8 Top 15 SOC Occupations

Charts showing volume and median wage by DOL occupation category.

**Most common:** Software Developers, Computer Systems Analysts, Computer Occupations (All Other)

**Highest median wage:** Physicians, Computer and Information Research Scientists

**Interpretation:** H-1B is not just a tech visa. Medical professionals and researchers are significant users. SOC Title is a high-cardinality feature (hundreds of unique values) that requires target encoding, not one-hot encoding.

---

#### 4.2.9 Full-Time vs. Part-Time

Three charts: count comparison, certification rate comparison, wage distribution comparison.

- Full-time: ~98% of all petitions
- Full-time median wage significantly higher
- Certification rate marginally higher for full-time

**Interpretation:** Part-time H-1B roles are rare and lower-compensated. The `IS_FULL_TIME` flag is a modest but valid predictor to include.

---

#### 4.2.10 Quarterly Trends

Three charts: application volume per quarter, certification rate per quarter, median wage per quarter.

- Q3 (April–June) has the highest volume, aligned with the USCIS lottery window
- Certification rate is stable at ~92–93% across all quarters
- Median wages are consistent quarter-over-quarter

**Interpretation:** Filing quarter does not affect LCA outcomes. The Q3 volume spike reflects employer behavior around the annual lottery deadline, not any change in DOL standards or wage practices.

---

#### 4.2.11 Correlation Matrix

A heatmap of Pearson correlations among: `TARGET`, `ANNUAL_WAGE_CAPPED`, `ANNUAL_PREVAILING_WAGE`, `WAGE_RATIO`, `IS_FULL_TIME`, `WAGE_ABOVE_PREVAILING`, `PROCESSING_DAYS`.

**Key findings:**
- `WAGE_RATIO` has the strongest positive correlation with `TARGET`
- `ANNUAL_WAGE` and `ANNUAL_PREVAILING_WAGE` are highly intercorrelated — use `WAGE_RATIO` instead to avoid multicollinearity
- `PROCESSING_DAYS` has near-zero correlation with target and represents post-decision data leakage — exclude from model

---

#### 4.2.12 Wage Ratio Violin Plot

A violin plot shows the full distribution shape of wage ratios for certified vs. denied cases.

**Interpretation:** Certified cases have a wider distribution skewed above 1.0, with a visible upper tail of high-paying petitions. Denied cases cluster tightly near or below 1.0. The violin shape makes the group difference more visually apparent than a box plot, confirming that `WAGE_RATIO` carries strong predictive signal.

---

#### 4.2.13 State-Level Median Wages (Top 15 States)

A horizontal bar chart with wage labels for the top 15 states by application volume.

**Top:** California, Washington, New York — highest median wages reflecting Big Tech concentration and cost of living.

**Interpretation:** The ~$40,000 wage gap between top and bottom states within the top 15 justifies geographic encoding as a model feature. State-level wage variation directly affects prevailing wage thresholds and therefore wage ratio calculations.

---

### 4.3 Key Findings Summary

| Metric | Value |
|--------|-------|
| Total H-1B Petitions (FY2025) | 582,271 |
| Overall Certification Rate | 92.6% |
| Median Offered Annual Wage | ~$119,000 |
| Average Wage Ratio | ~1.1 |
| Employers Paying Above Prevailing Wage | ~69% |
| Full-Time Positions | ~98% |
| Unique Employers | ~70,000 |
| Most Common SOC Occupation | Software Developers |

**Modeling Implications:**

1. **Class imbalance** (92.6% certified) — must use SMOTE or class weights; evaluate with F1 and AUC-ROC, not accuracy
2. **Wage Ratio** — strongest numeric predictor; central to 2026 lottery policy
3. **Employer Name and SOC Title** — high-cardinality; use target encoding
4. **State** — meaningful geographic wage variation; include as feature
5. **Processing Days** — data leakage (post-decision); exclude from model
6. **Denied cases are very rare** (0.6%) — model must be tuned to detect this minority class

---

## 5. Next Steps

| Phase | Tasks |
|-------|-------|
| **Feature Engineering** | Target-encode `EMPLOYER_NAME` and `SOC_TITLE`; map states to 4 census regions |
| **Model Training** | Logistic Regression (baseline), Random Forest, XGBoost |
| **Evaluation** | AUC-ROC, F1-score, Precision-Recall curve, Confusion Matrix |
| **Explainability** | SHAP value analysis — identify most influential features per prediction |
| **Deployment** | Streamlit web app — interactive H-1B success probability calculator |

---



*Project Report — UMBC DATA 606 Capstone, Assignment 03*
*Author: Mohammad Shoeb Ahmed | March 2026*
