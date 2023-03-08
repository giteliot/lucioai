from flask import Flask, request, render_template
from model.dog import get_random_seq
import torch

app = Flask(__name__)
model = None  # we'll load the model later


def preprocess_input(input_data):
    # Implement this function to preprocess the input data (e.g. convert it to a tensor)
    return torch.tensor([float(input_data)])


def postprocess_output(output_tensor):
    # Implement this function to postprocess the output data (e.g. convert it to a string)
    return str(output_tensor.item())


def process_input(input_data):
    return get_random_seq()


# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')


# Define the route for the model prediction
@app.route('/command', methods=['POST'])
def predict():
    input_data = request.form['input']
    output_action = process_input(input_data)
    return render_template('index.html', input_text=input_data, action=output_action)


if __name__ == '__main__':
    # Load the model
    # model = torch.load('model.pth', map_location=torch.device('cpu'))
    # Start the Flask app
    app.run(debug=True)
