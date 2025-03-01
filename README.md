<div style="background-color:rgb(143, 145, 236); padding: 20px; border-radius: 10px; color: black; box-shadow: 0 4px 6px rgba(64, 64, 108, 0.1);">

# 🔍 Customer Churn Prediction

## Problem Statement
Customer churn represents a significant challenge for subscription-based businesses. Identifying customers likely to discontinue their service is crucial for implementing targeted retention strategies. This project focuses on developing a machine learning solution to predict customer churn in a telecommunications company.

## Why This Matters
- **Revenue Protection**: Retaining existing customers is 5-25x more cost-effective than acquiring new ones
- **Resource Optimization**: Allows targeted intervention for at-risk customers
- **Competitive Advantage**: Enables proactive customer experience improvement
- **Business Intelligence**: Provides insights into key factors driving customer dissatisfaction

## Data Insights

### Demographic Patterns
![Subscription Type vs Gender](images/substypebysex.png)

### Agegroup and max Tenure Analysis
![Tenure by Age](images/agegrouptenureanalysis.png)

### Churn Rate Patterns
![Churn Rate by Age](images/churnbyage.png)

### Customer Interaction Impacts
![Effect of Last Interaction on Payment Delay](images/churnbyinteraction.png)
![Churn Rate by Last Interaction](images/churnbylasteinteraction.png)



### Model Performance
![Actual vs Predicted Churn](images/actualvspreicted.png)

Our prediction model demonstrates:
- High accuracy in identifying both churning and non-churning customers

### Feature Distribution Analysis
![Feature Distributions](images/featuredistribution.png)

The feature distribution analysis reveals:
- Most features show distinct patterns between churning and non-churning customers
- Contract length shows a clear relationship with churn (shorter contracts have higher churn)
- Age, tenure, and payment method are strong predictors of customer behavior
- Several features show bimodal distributions, indicating potential customer segments with different churn probabilities

### Gender and Tenure Relationship
![Churn Rate by Tenure and Gender](images/churnratebytenureandgender.png)

## Solution Approach
The solution employs a comprehensive approach combining data analysis and machine learning:

1. **Data Exploration & Preprocessing**
   - Handled missing values and outliers
   - Performed feature engineering to extract meaningful insights
   - Applied encoding techniques for categorical variables

2. **Model Development**
   - Implemented classification algorithm (Random Forest)
   - Conducted hyperparameter tuning through grid search
   - Addressed class imbalance using appropriate sampling techniques

3. **Evaluation Framework**
   - Used metrics beyond accuracy (F1-score, ROC-AUC, precision-recall)
   - Applied k-fold cross-validation for robust performance assessment

4. **Deployment Solution**
![Churn Predictor Tool](images/output_2.png)
![Churn Prediction Interface](images/output_1.png)

- Developed an **Advance interactive web application** for real-time churn prediction
- The tool features:
  - User-friendly interface for inputting customer parameters
  - Clear visualization of churn probability
  - Risk categorization (High/Medium/Low)
  - Detailed explanation of contributing factors
  - Customizable analysis for different customer segments

## Results & Impact
The final model achieved:
- **85.7%** prediction accuracy
- **83.2%** F1-score
- **0.89** ROC-AUC

Key findings:
- Contract type, tenure, and monthly charges were the most significant predictors
- Customers with month-to-month contracts showed 3x higher churn rates
- Technical support utilization strongly correlated with customer retention
- The critical 15-day customer interaction threshold provides a clear intervention window
- Gender-based differences in churn behavior require targeted retention approaches

## Technologies Used
- **Python**: Primary programming language
- **Pandas/NumPy**: Data manipulation
- **Scikit-learn**: Model implementation
- **Matplotlib/Seaborn**: Visualization
- **RandomForest**: RandomForest  implementation
- **Streamlit/HTML/CSS**: Web application development Front-end interface

## Future Work
- Implement real-time prediction system with automated alerts
- Develop personalized retention strategies based on demographic segments
- Integrate customer service interaction data for improved prediction accuracy
- Create an executive dashboard for tracking churn metrics and intervention effectiveness
- Explore deep learning approaches for identifying complex churn patterns
<div>