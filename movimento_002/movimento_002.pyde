img, img_cover = None, None

# Author: Berin
# Sketches repo: https://github.com/berinhard/sketches

from random import choice


def settings():
    global img, img_cover

    img = loadImage('data/img.jpg')
    img_cover = loadImage('data/cover.png')

    size(img.width, img.height - 1)

def setup():
    stroke(color(234, 239, 242))
    colorMode(HSB, 100)
    strokeWeight(1.25)
    
noise_factor = 78.5 

def draw():
    global noise_factor
    
    image(img, 0, 0)
    pass
    for y in range(0, height, 2):
        skip_y = True
         
        noise_y = int(map(y, 62, height, 1, 18))
        max_x = 100 + int(noise((frameCount + noise_y) / noise_factor) * width)
        c = map(y, 62, height, 0, 100)
        stroke(c, 80, 80)
        line(0, y, max_x, y)
    
    image(img_cover, 0, 0)
    
    #save_video_frames(24, 60)
    
    
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
    
    
    
def keyPressed():
    global noise_factor 
    
    coded = key == CODED
    if coded and keyCode == UP:
        noise_factor += 1
    elif coded and keyCode == DOWN:
        noise_factor -= 1
        
    print(noise_factor)
