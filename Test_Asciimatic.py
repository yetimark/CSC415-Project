# NOT USED IN SOLUTION
# This script was made to see what asciimatics would be useful for


from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText

# creating and playing special effects within a screen
def demo(screen):
    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            screen.height // 2 - 8),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            screen.height // 2 + 3),
        Stars(screen, (screen.width + screen.height) // 2)
    ]
    screen.play([Scene(effects, 500)])

# this is what displays a screen. I think am guessing refreshing what the screen has will be the way to go.
Screen.wrapper(demo)