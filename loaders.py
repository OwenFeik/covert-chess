import json
import pygame

def get_config(setting = None):
    with open('resources/config.json', 'r') as f:
        config = json.load(f)
    if setting:
        try:
            return config[setting]
        except KeyError:
            print(f'Setting {setting} not found.')
            raise SystemExit
    return config

# Adapted from https://www.pygame.org/wiki/Spritesheet
class Spritesheet():
    def __init__(self, filename, scalefactor = 1):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit

        self.scalefactor = scalefactor

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if self.scalefactor > 1:
            w, h = image.get_size()
            image = pygame.transform.scale(image, (w * self.scalefactor, h * self.scalefactor))

        return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, rect, image_count):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)

    @staticmethod
    def get_pieces():
        file = get_config('spritesheet')
        return Spritesheet(file, 4).load_strip((0, 0, 16, 16), 12)

def get_colours():
    with open(get_config('colours'), 'r') as f:
        return json.load(f)
