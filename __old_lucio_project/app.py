from flask import Flask, request, render_template
from model.dog import Dog
import torch
import json

app = Flask(__name__)
model = None  # we'll load the model later
# actually represents the max size of the soundwave
num_possible_commands = 100

moves = {
    "JUMP",
    "CROUCH",
    "SIT",
    "WALK"
}

waves = []

dog = Dog(moves, num_possible_commands)


def preprocess_input(input_data):
    # Implement this function to preprocess the input data (e.g. convert it to a tensor)
    return torch.tensor([float(input_data)])


def postprocess_output(output_tensor):
    # Implement this function to postprocess the output data (e.g. convert it to a string)
    return str(output_tensor.item())


def process_input(input_data):
    return get_random_seq()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/command', methods=['POST'])
def post_wave():
    input_wave = json.loads(request.form['wave'])
    output_action = dog.predict(input_wave[:num_possible_commands])
    return output_action;

@app.route('/save', methods=['POST'])
def save():
    input_wave = json.loads(request.form['wave'])
    waves.append(input_wave)
    CMD = 'VAI'
    with open(f'{CMD}.csv', 'w') as f:
        for w in waves:
            f.write(f"{w};{CMD}\n")
    return str(len(waves));

@app.route('/train', methods=['POST'])
def train():
    command = json.loads(request.form['command'])
    action = request.form['action']
    reward = request.form['reward']

    dog.learn(command, action, reward)
    return "OK"


if __name__ == '__main__':
    # Load the model
    model = torch.load('model.pth', map_location=torch.device('cpu'))
    app.run(debug=True)
