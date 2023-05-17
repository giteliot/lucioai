from flask import Flask, request, render_template
from model.dog import Dog
import torch
import json

app = Flask(__name__)
model = None  # we'll load the model later
num_possible_commands = 10

moves = {
    "JUMP",
    "CROUCH",
    "SIT",
    "WALK"
}

dog = Dog(moves, num_possible_commands)


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
@app.route('/command', methods=['GET'])
def predict():
    input_data = request.args['command']
    dog.update_vocabulary(input_data)
    output_action = dog.predict(input_data)
    return output_action;

@app.route('/voice_command', methods=['POST'])
def predict_from_voice():
    input_voice = request.form['voice']
    print(input_voice)
    # output_action = dog.predict(input_data)
    return 'ROLLING_RIGHT';

@app.route('/train', methods=['POST'])
def train():
    command = request.form['command']
    action = request.form['action']
    reward = request.form['reward']

    dog.learn(command, action, reward)
    return "OK"


if __name__ == '__main__':
    # Load the model
    model = torch.load('model.pth', map_location=torch.device('cpu'))
    app.run(debug=True)
