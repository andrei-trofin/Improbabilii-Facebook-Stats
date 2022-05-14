from flask import Flask, request, jsonify, render_template
import pandas as pd
import jinja2
import pickle

def is_positive_integer(input_value):
    if input_value == int(input_value):
        return True
    else:
        return False

app = Flask(__name__)
model = pickle.load(open('../models/best_model.p', 'rb'))
scaler = pickle.load(open('../models/scaler.p', 'rb'))

prediction_text = "Your online marketing will bring you a number of {} going and a number of {} interested."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            invited_noreply = int(request.form['invited_noreply'])
            days_of_promoting = int(request.form['days_of_promoting'])
            page_posts = int(request.form['page_posts'])
            visitor_posts = int(request.form['visitor_posts'])

            user_data = pd.DataFrame({'invited_noreply': invited_noreply,
                                    'days_of_promoting': days_of_promoting,
                                    'page_posts': page_posts,
                                    'visitor_posts': visitor_posts}, index=[0])
            user_data[user_data.columns] = scaler.transform(user_data)

            prediction = model.predict(user_data)

            # If we achieve negative values then raise an error_results
            if prediction[0][0] < 0 or prediction[0][1] < 1:
                return render_template('index.html', error_results="The values you entered resulted in a negative prediction of the model. Please try other values.")

            attending_count = int(prediction[0][0])
            interested_count = int(prediction[0][1])
            return render_template('index.html', prediction_results=prediction_text.format(attending_count, interested_count))
        except:
            return render_template('index.html', error_results="Please make sure you entered a positive integer in each of the form fields.")


if __name__ == '__main__':
	app.run(debug=True)
