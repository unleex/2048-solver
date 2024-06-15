import keyboard
import mss 
import numpy as np
import pyautogui
from PIL import Image
import os

TILE_PHOTO_CROPPING = 30 # cut edges of a tile that tesseract handles as symbols like '_', '/', 'i', etc.
TILE_PHOTO_PAD_WIDTH = 70 # because tesseract can't process small images. values higher than 100 stop working
FIELD_SIZE = 4
INSTRUCTION = """
Select your 2048 field. Point your mouse on field's corner and press right shift. Then repeat for the opposite corner. 
If you selected corner incorrectly, press backspace and select it again. 
While selecting field and in further algorithm work, don't move(scroll, zoom) your screen AT ALL!
If you want to stop solving, press space"""
MAX_FIELD_X_Y_DIFFERENCE = 50
EXCEEDED_MAX_FIELD_X_Y_DIFFERENCE_MSG = "Selected field doesn't look like a square. Try to select more accurately."

def set_field_pos() -> dict[str, int]:
    print(INSTRUCTION)
    field_corners_xy = []
    keyboard.add_hotkey('shift', lambda: field_corners_xy.append((pyautogui.position().x, pyautogui.position().y)))
    keyboard.add_hotkey('backspace', lambda: field_corners_xy.pop())
    while len(field_corners_xy) < 2:
        ...
    field_corners_xy = np.array(field_corners_xy)
    right = np.max(field_corners_xy[:, 0])
    left = np.min(field_corners_xy[:, 0])
    upper = np.min(field_corners_xy[:, 1])
    bottom = np.max(field_corners_xy[:, 1])

    width = right - left
    height = bottom - upper
    assert abs(width - height) < MAX_FIELD_X_Y_DIFFERENCE, EXCEEDED_MAX_FIELD_X_Y_DIFFERENCE_MSG
    
    #keyboard.remove_hotkey('shift')
    #keyboard.remove_hotkey('backspace')
    return {'top': upper, 'left': left, 'width': width, 'height': height}


def read_field(field_pos) -> np.ndarray:
    tile_size = field_pos['width']//FIELD_SIZE
    field = np.zeros((FIELD_SIZE, FIELD_SIZE))
    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            with mss.mss() as screenshotter:
                pixels = screenshotter.grab(
                       {'top': field_pos['top'] + i * tile_size, 
                       'left': field_pos['left'] + j * tile_size,  
                       'height': tile_size,
                       'width': tile_size 
                       }
                )
                pixels = np.asarray(pixels)
                shape = pixels.shape
                cropped_pixels = pixels[TILE_PHOTO_CROPPING:pixels.shape[0]- TILE_PHOTO_CROPPING,
                                        TILE_PHOTO_CROPPING:pixels.shape[1]- TILE_PHOTO_CROPPING] # crop RGB values
                padded_pixels = np.pad(
                    cropped_pixels, 
                    pad_width=((TILE_PHOTO_PAD_WIDTH, TILE_PHOTO_PAD_WIDTH),
                               (TILE_PHOTO_PAD_WIDTH, TILE_PHOTO_PAD_WIDTH),
                               (0,0)
                               ), # pad RGB values with 255 (white) and leave alpha channel 
                    constant_values=255)
                Image.fromarray(padded_pixels).save(f'reading_field/field_photo.png')
                command = f"tesseract --psm 7 reading_field/field_photo.png reading_field/field_values -l eng"
                os.system(command)
                with open('reading_field/field_values.txt') as f:
                    value = f.read().replace('\n', '')  
                field[i][j] = value if value.isdigit() else 0
    return field

def send_move(move):
    move_to_key = {'u': 'up', 'd': 'down', 'l': 'left', 'r': 'right'}
    pyautogui.press(move_to_key[move])
