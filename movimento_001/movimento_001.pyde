# Author: Berin
# Sketches repo: https://github.com/berinhard/sketches

img, img_cover = None, None

from random import choice

GRID_SIZE = 80

class CellsPath(object):
    """
    Class to hold a path to bre drawed at the screen
    The path contains cells that are linked to each other as a maze path
    """

    def __init__(self, path_color):
        self.cells = []
        self.path_color = path_color
        self.c_alpha = random(100, 200)
        self.stroke_weight = random(2, 5)

    @property
    def rgb(self):
        return red(self.path_color), green(self.path_color), blue(self.path_color)

    def __len__(self):
        return len(self.cells)

    def add_new_step(self, cell):
        self.cells.append((cell))

    def display(self):
        if len(self) <= 1:
            return

        r, g, b = self.rgb
        strokeWeight(self.stroke_weight)
        stroke(color(r, g, b, self.c_alpha))
        beginShape()
        for cell in self.cells:
            vertex(cell.x, cell.y)
        endShape()


class Cell(object):
    """
    A single position in a grid that can be linked to neighbor grids
    """

    def __init__(self, x, y, border, spacing):
        """
        index_x: Cell's column position (not in pixel)
        index_y: Cell's line position (not in pixel)
        border and spacing are used to convert the indexes to x-y coordinates
        """
        self.index_x, self.index_y = x, y
        self.border = border
        self.spacing = spacing

    @property
    def x(self):
        return self.border + self.spacing / 2 + self.index_x * self.spacing

    @property
    def y(self):
        return self.border + self.spacing / 2 + self.index_y * self.spacing

    @property
    def is_at_top_section(self):
        return self.y < 600  # split area

    @property
    def line_num(self):
        return int(self.index_y / 8)

    @property
    def line_color(self):
        if self.is_at_top_section:
            return color(255, 255, 255)
        else:
            return color(0, 0, 0)

    def __eq__(self, cell):
        return self.x == cell.x and self.y == cell.y

    def neighbors(self, grid_size):
        if self.is_at_top_section:
            x_range = [1]
            y_range = [0, 1]
        else:
            x_range = [0, 1]
            y_range = [1]

        if 0 < self.index_x < grid_size:
            x_range.append(-1)
        if 0 < self.index_y < grid_size:
            y_range.append(-1)

        for x in x_range:
            for y in y_range:
                if abs(x - y) == 2 and self.is_at_top_section:
                    continue  # do not cross lines

                new_y = self.index_y + y
                neigh = Cell(self.index_x + x, self.index_y + y, self.border, self.spacing)
                if self.is_at_top_section != neigh.is_at_top_section:
                    continue
                if neigh != self:
                    yield neigh

class Maze(object):

    def __init__(self, grid_size):
        self.visited_cells = []
        self.unvisited_cells = []
        self.cells_stack = []
        self._current_cell = None
        self.grid_size = grid_size
        self.current_path = None
        self.live_paths = []
        self.reset_path()

    @property
    def current_cell(self):
        return self._current_cell

    @current_cell.setter
    def current_cell(self, cell):
        self._current_cell = cell
        if cell in self.unvisited_cells:
            self.unvisited_cells.remove(cell)

    def init_cells(self, border, spacing):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                new_cell = Cell(x, y, border, spacing)
                if new_cell.y > height or new_cell.x > width:
                    continue
                self.unvisited_cells.append(Cell(x, y, border, spacing))

        self.current_cell = choice(self.unvisited_cells)

    def break_wall(self):
        if not self.current_path:
            self.current_path = CellsPath(self.current_cell.line_color)
            self.live_paths.append(self.current_path)

        if not self.unvisited_cells:
            return

        self.current_path.add_new_step(self.current_cell)
        self.visited_cells.append(self.current_cell)

        neighbors = [n for n in self.current_cell.neighbors(self.grid_size) if n in self.unvisited_cells]
        go_to_new_cell = (not neighbors and self.unvisited_cells) or len(self.current_path) > self.max_path_length
        if go_to_new_cell:
            self.current_cell = choice(self.unvisited_cells)
            self.reset_path()
        else:
            self.current_cell = choice(neighbors)

    def reset_path(self):
        self.current_path = None
        self.max_path_length = random(5, 15)

    def display(self):
        for p in self.live_paths:
            p.display()



def settings():
    global img, img_cover

    img = loadImage('data/img.jpg')
    img_cover = loadImage('data/cover.png')

    size(img.width, img.height)

def setup():
    global maze

    strokeCap(ROUND)
    strokeWeight(4)
    noFill()

    border = 5
    spacing = (width - border * 2) / float(GRID_SIZE)
    maze = Maze(GRID_SIZE)
    maze.init_cells(border, spacing)

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
    global maze
    
    image(img, 0, 0)
    maze.break_wall()
    maze.display()
    image(img_cover, 0, 0)
    if not maze.unvisited_cells:
        maze = Maze(GRID_SIZE)
        maze.init_cells(border, spacing)
        
    #save_video_frames(60, 24)
