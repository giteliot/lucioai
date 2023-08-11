import pygame
from PIL import Image, ImageSequence
import os

# background static image

bg_image = pygame.image.load("resources/train_room_background.png")
bg_image = pygame.transform.scale(bg_image, (400, 400))

# lucio base

frame = pygame.image.load("resources/lucio/base.png")
frame = pygame.transform.scale(frame, (150, 225))
lucio_base = [frame]*8

# lucio animations, 8 frames

frame = pygame.image.load("resources/lucio/crouch.png")
frame = pygame.transform.scale(frame, (150, 225))
lucio_crouch = [frame]*8

frame = pygame.image.load("resources/lucio/sit.png")
frame = pygame.transform.scale(frame, (150, 225))
lucio_sit = [frame]*8

# lucio animations from .gif


output_frames_dir = "resources/lucio/jump"
os.makedirs(output_frames_dir, exist_ok=True)

gif = Image.open("resources/lucio/jump.gif")

lucio_jump = []

for frame_index, frame in enumerate(ImageSequence.Iterator(gif)):
    output_frame_path = os.path.join(output_frames_dir, f"frame_{frame_index:04d}.png")
    frame.save(output_frame_path)
    frame = pygame.image.load(output_frame_path)
    frame = pygame.transform.scale(frame, (150, 225))
    lucio_jump.append(frame)
lucio_jump.append(lucio_base[0])


output_frames_dir = "resources/lucio/walk"
os.makedirs(output_frames_dir, exist_ok=True)

gif = Image.open("resources/lucio/walk.gif")

lucio_walk = []

for frame_index, frame in enumerate(ImageSequence.Iterator(gif)):
    output_frame_path = os.path.join(output_frames_dir, f"frame_{frame_index:04d}.png")
    frame.save(output_frame_path)
    frame = pygame.image.load(output_frame_path)
    frame = pygame.transform.scale(frame, (150, 225))
    lucio_walk.append(frame)

lucio_walk = lucio_walk*4
