# LucioAI
Can Deep Learning learn like a dog?
This is a terrible attempt to create a deep learning training dog "simulator"

### Motivation
The initial idea is to use soundwaves as inputs for the training, i.e. teach commands to the virtual dog (Lucio) using the microphone on your machine.
This approach (obviously I would now say, but hindisght is 20/20) failed because of the incredible high that soundwaves representing the same word can have. 

Instead of throwing everything out, I decided to create a dumbed down version (mainly because I already had a cute doggo drawing), where the inputs are submitted via keyboard.

Even in this new version, making the nn learn fast enough to not bore the user to death, while still not making the gradient explode after just a few rounds, was not straightfoward. Maybe this says more about my ml skills than the actual difficult of the problem.

### Disclaimer
Code is spaghetti.

### How to Run
I'm using pipenv `2022.11.30` and python `3.7+`

From `lucioai` home folder:
`$ pipenv shell`
`$ pipenv install`
`$ python game.py`

### How To Play
Should be straightfoward enough by reading the bottom text, but the basic flow is:
![image1](./resources/readme/lucio_show_1.png)

1. press any key on your keyboard
2. look at the move that Lucio does in response
3. if you like it, press Q to reward Lucio, he will pregressively connect that move with the key you just pressed
4. if you don't, press E to give a negative feedback instead

Note that sometimes it will take awhile for Lucio to learn the possible moves (4 in total), as it is for a real doggo :)

![image2](./resources/readme/lucio_show_2.png)

Once you feel you trained Lucio enough, you can test it out on the field!

### Contacts
I don't think anyone would have a use for this, but in case you wanna contact me about it:
https://twitter.com/codewithnohands
