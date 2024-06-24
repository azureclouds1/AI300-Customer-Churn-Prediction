from flask import Flask, request, render_template
from model import Model
import re

app = Flask(__name__)

# Method 1: Via HTML Form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
    
        form_input = dict(request.form)
        print(form_input)

        model_inputs_list = ['tenure_months', 'num_referrals', 'total_long_distance_fee', 'total_monthly_fee', 
                        'total_charges_quarter', 'age', 'num_dependents','has_internet_service', 
                        'has_unlimited_data', 'has_premium_tech_support', 'has_online_security', 
                        'paperless_billing', 'senior_citizen', 'married', 'contract_type', 
                        'payment_method']
        
        model_inputs = []

        try:
            for i in model_inputs_list:
                if(re.match('^[0-9\.]*$',form_input[i]) and bool(form_input[i])): #check if all positive integer/float input and empty value
                    features = round(float(form_input[i]))
                    model_inputs.append(features)
                else:
                    model_inputs.append(0) #append blank value to prevent error
            print(model_inputs)
            prediction = Model().predict(model_inputs)
            return render_template('index.html', prediction=prediction)
        
        except:
            print('Input Injection Error Alert!!!')
            model_inputs = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1] #return to default values if error
            error_message = 'Prediction Failed. Please check your input values and try again.'
            return render_template('index.html', prediction=error_message)

    return render_template('index.html')


# Method 2: Via POST API
@app.route('/api/predict', methods=['POST'])
def predict():
    request_data = request.get_json()

    print(request_data)

    model_inputs_list = ['tenure_months', 'num_referrals', 'total_long_distance_fee', 'total_monthly_fee', 
                        'total_charges_quarter', 'age', 'num_dependents','has_internet_service', 
                        'has_unlimited_data', 'has_premium_tech_support', 'has_online_security', 
                        'paperless_billing', 'senior_citizen', 'married', 'contract_type', 
                        'payment_method']
        
    model_inputs = []

    try:
        for i in model_inputs_list:
            if(re.match('^[0-9\.]*$',request_data[i]) and bool(request_data[i])): #check if all positive integer/float input and empty value
                features = round(float(request_data[i]))
                model_inputs.append(features)
            else:
                model_inputs.append(0) #append blank value to prevent error
        print(model_inputs)
        prediction = Model().predict(model_inputs)
        return {'prediction': str(prediction)}
    
    except:
        print('Input Injection Error Alert!!!')
        model_inputs = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1] #return to default values if error
        error_message = 'Prediction Failed. Please check your input values and try again.'
        return {'prediction': error_message}

if __name__ == '__main__':
    app.run(debug=True)