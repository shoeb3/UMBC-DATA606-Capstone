# Predicting H-1B Visa Approval Outcomes Using U.S. Labor Market Data

**Author:** Mohammad Shoeb Ahmed
**Course:** UMBC Data Science Master Degree Capstone, DATA 606
**Advisor:** Dr. Chaojie (Jay) Wang
**Semester:** Spring 2026

**YouTube Presentation:** [Link TBD]
**Final Presentation:** [H1B_Prediction_Presentation.pptx](https://github.com/shoeb3/UMBC-DATA606-Capstone/blob/main/docs/Predicting_H1B_Approval_Outcomes_Presentation.pptx)
**GitHub Repository:** [https://github.com/shoeb3/UMBC-DATA606-Capstone/](https://github.com/shoeb3/UMBC-DATA606-Capstone/)

## Background

Every year, many foreign specialists who wish to come into the United States on a work permit visa opt for the H-1B visa. This is the most frequently used employment non-immigrant visa used by individuals who work in occupations that require four years of post-secondary education in fields such as software engineering, data analytics, medicine, or finance. Before applying for an H-1B visa, one is expected to acquire clearance on the Labor Condition Application, LCA. The LCA is utilized as a prevailing wage test to ensure that the individual earns the prevailing wage for that specific position in that particular geographical location.

H-1B has very high stakes. There is much greater demand than there are available visas under the cap of 85,000 per year, and as such, H-1B's lottery has become one of the most important selection methods in the United States labor market. This has been due to some recent changes in the regulation of the program. From 2024 to 2026, the lottery has undergone a very major reform in its workings, which saw the switch to a lottery that was based on the ratio of the offered wage.

This project grew out of that policy context. The question we tried to answer was whether machine learning could predict LCA certification outcomes using only information available at filing time, and whether it could quantify how wage competitiveness, employer track record, and attorney history influence those outcomes. The practical goal was a tool that employers and immigration professionals could use to assess denial risk before submitting a petition.

## Data Sources

Data for this research was obtained from U.S. Department of Labor’s Office of Foreign Labor Certification Performance Data, which is a public database containing all petitions for an LCA filed in any fiscal year. The data set contains information on the employer name, occupation, wage offered, prevailing wage, site of work, and decision on the case. Since the disclosure is mandatory by federal law, all cases are included in the data set with no exceptions made.

All data sets from FY2025, including quarters 1-4, October 2024 to September 2025, were utilized.

| Quarter | Rows |
|---------|------|
| Q1 (Oct to Dec 2024) | 107,414 |
| Q2 (Jan to Mar 2025) | 132,133 |
| Q3 (Apr to Jun 2025) | 238,425 |
| Q4 (Jul to Sep 2025) | 118,580 |
| Combined total | 596,552 |

After filtering to H-1B petitions only, the working dataset came to 582,271 rows and 99 columns. We focused on FY2025 specifically because it reflects the new wage-priority lottery rules. Using data from earlier years would have meant modeling a system that no longer exists.

## Data Elements

The table below describes the key columns from the raw DOL dataset that were used in this project.

| Column | Type | Description |
|--------|------|-------------|
| CASE_STATUS | Categorical | Final DOL outcome: Certified, Denied, or Withdrawn |
| EMPLOYER_NAME | String | Sponsoring company |
| EMPLOYER_STATE | Categorical | State where employer is located |
| SOC_TITLE | String | DOL standardized occupation title |
| WAGE_RATE_OF_PAY_FROM | Numeric | Offered salary |
| WAGE_UNIT_OF_PAY | Categorical | Pay period: Year, Month, Hour, etc. |
| PREVAILING_WAGE | Numeric | DOL mandated minimum wage for this role and location |
| PW_UNIT_OF_PAY | Categorical | Pay period of prevailing wage |
| FULL_TIME_POSITION | Categorical | Y or N |
| RECEIVED_DATE | Date | Date DOL received the petition |
| AGENT_ATTORNEY_LAST_NAME | String | Representing attorney if any |
| PW_WAGE_LEVEL | Categorical | Prevailing wage tier, Level I through IV |
| WORKSITE_STATE | Categorical | State where work is actually performed |

Beyond the raw columns, we created the following features during the project.

| Feature | Description |
|---------|-------------|
| TARGET | 1 if Certified, 0 otherwise |
| ANNUAL_WAGE | Offered wage converted to annual |
| ANNUAL_PREVAILING_WAGE | Prevailing wage converted to annual |
| WAGE_RATIO | Offered wage divided by prevailing wage |
| ANNUAL_WAGE_CAPPED | Wage clipped at 1st to 99th percentile |
| IS_FULL_TIME | Binary flag from FULL_TIME_POSITION |
| QUARTER | Filing quarter derived from RECEIVED_DATE |
| EMP_CERT_RATE | Employer historical certification rate, computed on training data only |
| SOC_CERT_RATE | Occupation historical certification rate, computed on training data only |
| STATE_CERT_RATE | State historical certification rate, computed on training data only |
| ATTY_CERT_RATE | Attorney historical certification rate, computed on training data only |
| HAS_ATTORNEY | 1 if petition was filed with an attorney |
| PW_LEVEL | Numeric encoding of prevailing wage tier, 1 through 4 |
| STATE_MISMATCH | 1 if worksite state differs from employer state |
| WAGE_VS_SOC_MEDIAN | Difference between offered wage and occupation median wage |

## Results of EDA

The dataset is large and fairly one-sided. Of the 582,271 H-1B petitions in FY2025, 92.6% were certified. The median annual wage was $119,309 and there were 69,871 unique employers in the data.

That 92.6% certification rate is not just a statistic — it is the central challenge of this project. A model that predicts certified for every single case would be 92% accurate while being completely useless in practice. Looking at the raw case statuses, only 3,505 cases are true outright denials. The bulk of the non-certified cases are employer-initiated withdrawals (9,211) and certified-withdrawn cases (30,111) where the employer cancelled a petition that had already been approved.

The wage story is interesting but not as clean as we initially hoped. Denied petitions have a mean annual wage of $116,928 compared to $127,076 for certified ones, and there is a lot of overlap between the two groups. The wage ratio is a bit more telling — denied cases average a ratio of 1.085 versus 1.051 for certified cases — but even that is not enough on its own to reliably predict outcomes. Individual wage values, it turned out, are weak predictors.

What really matters is who the employer is. IT staffing firms like Infosys (median wage $92,581), Tata ($86,923), and HCL ($108,098) file enormous volumes of petitions but pay wages much closer to the DOL minimum than Big Tech companies like Meta ($203,350), Google ($184,000), and Apple ($174,462). This gap between staffing firms and direct employers turned out to be the strongest signal in the entire dataset. After we engineered the employer certification rate feature, its correlation with the target reached 0.57.

Geographically, California, Texas, New Jersey, and New York see the most filings. Washington state has the highest certification rate at 96.7%, which makes sense given how dominated it is by large tech companies. Median wages vary quite a bit by state too — from $154,000 in California down to $90,667 in Maryland among the top 15 states.

One data quality issue we caught early was the prevailing wage annualization problem. The DOL stores prevailing wages in different pay period units. If you skip the annualization step and divide a $100,000 annual offered wage by a $50 per hour prevailing wage, you get a ratio of 2,000 instead of something close to 1.05. That bug was causing the raw average wage ratio to appear as 274 and making it negatively correlated with the target. We fixed it by multiplying all prevailing wages by the appropriate annual factor using the PW_UNIT_OF_PAY column.

After adding the employer, occupation, and state certification rate features, the correlation picture changed dramatically. EMP_CERT_RATE at 0.57, ATTY_CERT_RATE at 0.25, SOC_CERT_RATE at 0.22, and STATE_CERT_RATE at 0.11 became the dominant signals. Historical certification patterns are simply far more predictive than any individual wage value.

## Results of ML

We trained three models on a stratified 149,999-row sample from the full dataset, with an 80/20 train and test split that preserved the 92.6% to 7.4% class ratio. In total we used 21 features after encoding. SMOTE was originally part of the pipeline to oversample denial cases, but after fixing the data leakage issue the feature set became weaker, and the synthetic denial cases were adding noise rather than signal. We removed SMOTE and used scale_pos_weight of 12.6 inside XGBoost instead to push the model to pay more attention to the minority class.

The key alteration carried out on the pipeline involved resolving the issue of data leakage. This involved calculating the variables EMP_CERT_RATE, SOC_CERT_RATE, and STATE_CERT_RATE before the split into train and test sets using all of the available data. In effect, the model will learn the outcome of the testing set during its learning phase. Following the computation of their values using only the training set, the correlation coefficient of the employment certification rate dropped from 0.57 to 0.37, while the AUC went down from 0.917 to 0.780.

| Model | Accuracy | AUC-ROC | Recall-Denial | Precision-Denial | F1-Denial |
|-------|----------|---------|--------------|-----------------|----------|
| Logistic Regression | 81.43% | 0.8044 | 0.5766 | 0.2153 | 0.3135 |
| Random Forest | 84.14% | 0.7559 | 0.5000 | 0.2319 | 0.3168 |
| XGBoost (t=0.50) | 92.65% | 0.7800 | 0.0000 | 0.0000 | 0.0000 |
| XGBoost F-beta (t=0.89) | 82.51% | 0.7800 | 0.5539 | 0.2228 | 0.3178 |

One of the most unexpected results was that the probability output of XGBoost always fell within the range of 0.677 to 0.901, meaning that the typical threshold value of 0.50 identified none of the denials. This makes sense when you think about it — the model learned that almost everything gets certified, so it outputs high probabilities for nearly everything. To find the right operating point, we swept thresholds from 0.05 to 0.92 in fine steps and used F-beta scoring with beta equal to 2 to weight recall twice as much as precision. A threshold of 0.89 was selected, which catches 55.4% of denials at a precision of 22.3%.

Looking at feature importance, employer identity runs the show. EMPLOYER_NAME_ENC (0.287) and EMP_CERT_RATE (0.256) together account for more than 54% of total importance. IS_LARGE_EMPLOYER (0.159) and EMP_PETITION_COUNT (0.139) round out the top four. ATTY_CERT_RATE at 0.008 is small but meaningful — it confirms that adding attorney history was the right call. Almost all of the wage features came in below 1%, which reinforces the EDA conclusion that wages are weak individual predictors.

## Conclusion

As can be observed from the figures, the best performer was Logistic Regression with AUC of 0.804, which makes it not only interpretable but also accurate. The second place belongs to the optimized XGBoost model with a threshold for denial recall at 55.4%, while the AUC score was 0.780. These are real results; it is valuable to detect more than 50% of petitioners that might get denial on such a small number of denials in the data (0.6%).

The bigger insight from this project is structural. Over 54% of the model's predictive power comes from employer identity. It is really asking one question: does this employer have a history of compliance problems? That mirrors how the real H-1B process actually works, where IT staffing firms face higher scrutiny precisely because of patterns built up over years of filings.

The fact that XGBoost's probabilities all cluster between 0.677 and 0.901 also tells us something important. The LCA stage is not where meaningful denial happens. The DOL approves almost everything. The real competitive pressure is at the USCIS lottery, where the 2026 wage-priority rules now determine who gets in.

## Limitations

There are a few honest limitations worth noting. The biggest one is that the model depends heavily on employer history. For a company filing for the first time, the employer certification rate defaults to the global mean of 0.926, which gives the model nothing useful to work with. New filers are essentially invisible to it.

The rarity of true denials is also a problem. Only 3,505 petitions were genuine outright denials out of over half a million. Our target variable bundles those together with withdrawals, which happen for completely different reasons. A cleaner model would separate them, but that would need a much larger pool of true denials to train on.

It is also worth being honest about what the LCA stage actually represents. Because 92.6% of applications are certified regardless, a pre-filing tool built on this data has limited standalone value. The USCIS lottery is where the real attrition happens, and that data is not public in the same way.

Finally, the narrow probability range means the model cannot give confident individual predictions. At threshold 0.89, precision is only 22.3%, so the majority of flagged cases will turn out to be fine. For most use cases, treating it as a risk flag rather than a definitive prediction is the right framing.

## Future Research Directions

A very important next step would be access to petition-level data from USCIS that would measure outcomes not only at the LCA verification stage but also at the visa adjudication level. This will allow modeling all of the factors affecting the H-1B process and its final success or failure.

Building employer trend features over multiple years would also help a lot. Right now the employer certification rate is a static snapshot. A company whose compliance record is improving over time looks the same as one that is getting worse, and those are very different risk profiles.

The attorney feature showed real promise with a correlation of 0.25. A deeper dive into attorney-level patterns, firm specialization, and case type could surface meaningful signal that the current feature only scratches the surface of.

Training a separate model on only the 3,505 true denial cases rather than bundling them with withdrawals would produce a cleaner and more honest signal. Getting enough data for that would require pulling in multiple years of records or augmenting with external sources.

Last, the most practically useful extension would be shifting the prediction target from LCA certification to lottery selection probability based on wage ratio. That is the question employers actually need answered under the 2026 rules, and it is where this kind of modeling would have the clearest real-world impact.

*UMBC DATA 606 Capstone, Spring 2026*
*Mohammad Shoeb Ahmed*
