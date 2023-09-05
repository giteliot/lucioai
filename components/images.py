import pygame
from PIL import Image, ImageSequence
import os
# background static image

bg_image = pygame.image.load("resources/train_room_background.png")
bg_image = pygame.transform.scale(bg_image, (800, 400))

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
RATIO_LUCIO = 0.7

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

output_frames_dir = "resources/mad_bat/"
os.makedirs(output_frames_dir, exist_ok=True)

gif = Image.open("resources/mad_bat.gif")

RATIO_BAT = 0.8

mad_bat = []
for frame_index, frame in enumerate(ImageSequence.Iterator(gif)):
    output_frame_path = os.path.join(output_frames_dir, f"frame_{frame_index:04d}.png")
    frame.save(output_frame_path)
    frame = pygame.image.load(output_frame_path)
    frame = pygame.transform.scale(frame, (int(320*RATIO_BAT), (438*RATIO_BAT)))
    mad_bat.append(frame)

# os.rmdir()
frame = pygame.image.load("resources/evil_cat.png")
frame = pygame.transform.scale(frame, (90, 90))
evil_cat = [frame]*2

frame = pygame.image.load("resources/end_pole.png")
frame = pygame.transform.scale(frame, (90, 90))
end_pole = [frame]*2