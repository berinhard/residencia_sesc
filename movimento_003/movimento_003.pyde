# Author: Berin
# Sketches repo: https://github.com/berinhard/sketches
img, img_cover = None, None

from random import choice, shuffle
from copy import deepcopy
    
    
cell_size = 4

VALUES = []

class Tile(object):
    
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.pixels = []
        self.is_shuffable = True
        
    def read_tile(self):
        for x in range(self.x, self.x + self.tile_size):
            for y in range(self.y, self.y + self.tile_size): 
                cover_pixel = img_cover.get(x, y)
                if cover_pixel:
                    self.is_shuffable = False
                self.pixels.append(img.get(x, y))
                
    def draw_tile(self):        
        current_pixel = 0
        for x in range(self.x, self.x + self.tile_size):
            for y in range(self.y, self.y + self.tile_size):
                c = self.pixels[current_pixel]
                set(x, y, c)
                current_pixel += 1


class TilesLine(object):
    
    def __init__(self, line_y, tiles_size):
        self.line_y = line_y
        self.tiles_size = tiles_size
        self.tiles = []
        self.original_tiles = []
        self.shuffled = False

    def populate(self):
        for x in range(0, width, self.tiles_size):
            tile = Tile(x, self.line_y, self.tiles_size)
            tile.read_tile()
            self.tiles.append(tile)
        self.original_tiles = deepcopy(self.tiles)
            
    def shuffle(self):
        if not self.shuffled:
            new_tiles_order = []
            self.shuffled = True
            
            shuffable_tiles = [t for t in self.tiles if t.is_shuffable]
            for i, tile in enumerate(self.tiles):
                if tile.is_shuffable:
                    x = i * self.tiles_size 
                    pos = int(random(len(shuffable_tiles)))
                    tile = shuffable_tiles.pop(pos)
                    tile.x = x
                new_tiles_order.append(tile)
        else:
            self.shuffled = False
            new_tiles_order = deepcopy(self.original_tiles)

        self.tiles = new_tiles_order    
            
    def draw(self):
        to_draw = self.tiles
        for tile in to_draw:
            tile.draw_tile()
                
            
            
class Building(object):
    
    def __init__(self, tiles_size):
        self.tiles_size = tiles_size
        self.tile_lines = []
        self.current_line = 0
        
    def populate(self):
        for y in range(0, height, self.tiles_size):
            tile_line = TilesLine(y, self.tiles_size)
            tile_line.populate()
            self.tile_lines.append(tile_line)
                
    def draw_distort(self):
        tile_line = self.tile_lines[self.current_line]
        tile_line.shuffle()
        tile_line.draw()
        self.current_line += 1
        if self.current_line == len(self.tile_lines):
            self.current_line = 0
            

def settings():
    global img, img_cover

    img = loadImage('data/img.jpg')
    img_cover = loadImage('data/cover.png')

    size(img.width, img.height - 1)
    


def setup():
    stroke(color(234, 239, 242))
    colorMode(HSB, 100)
    strokeWeight(1)
    stroke(1, 0, 0)
    noFill()
    image(img, 0, 0)
    
    global building
    building = Building(cell_size)
    print('Populating tiles grid...')
    building.populate()
    print('Done!')
    #frameRate(5)
    
def save_video_frames(frame_rate, seconds, stop_run=True, extension="png", log_frame=True):
    """
    GIST: https://gist.github.com/berinhard/d2ef20f361f70b7c0a216957d993efb2
    Save the required number of frames given for `seconds` with the given `frame_rate`.
    stop_run: calls noLoop() after saving all frames
    extension: file extension
    log_frame: enables logging in the terminal
    """
    num_frames = frame_rate * seconds

    if log_frame:
        print("{} /  {} - {}%".format(
            frameCount, int(num_frames), int(frameCount * 100 / num_frames)
        ))
    if frameCount <= num_frames:
        frame_name ="#" * (len(str(num_frames)))
        saveFrame("{}.{}".format(frame_name, extension))
    elif stop_run:
        noLoop()
    
    
def draw():                
    building.draw_distort()
    #noFill()
    #for x in range(0, width, cell_size):
    #    for y in range(0, height, cell_size):
    #        stroke(27, 27, 27, 180)
    #        rect(x, y, cell_size, cell_size)
    image(img_cover, 0, 0)
    save_video_frames(24, 60)
