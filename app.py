from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained pipeline
pipeline = joblib.load('svm_model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    data_df = pd.DataFrame([data])
    
    # Convert numerical values to proper data types
    numerical_columns = [
        'Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts',
        'Num_Credit_Card', 'Interest_Rate', 'Delay_from_due_date',
        'Num_of_Delayed_Payment', 'Changed_Credit_Limit', 'Num_Credit_Inquiries',
        'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age',
        'Total_EMI_per_month', 'Amount_invested_monthly', 'Monthly_Balance',
        'Count_Auto Loan', 'Count_Credit-Builder Loan', 'Count_Personal Loan',
        'Count_Home Equity Loan', 'Count_Not Specified', 'Count_Mortgage Loan',
        'Count_Student Loan', 'Count_Debt Consolidation Loan', 'Count_Payday Loan'
    ]
    for col in numerical_columns:
        data_df[col] = pd.to_numeric(data_df[col])
    
    # Predict using the pipeline
    prediction = pipeline.predict(data_df)
    return render_template('index.html', prediction_text='Predicted Credit Score: {}'.format(prediction[0]))

if __name__ == "__main__":
    app.run(debug=True)
