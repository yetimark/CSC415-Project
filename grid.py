# These are the data structures for holding information about a position on the display

# A cell is now a tuple in the format (x,y)
# In the end I really want the coordinates on the graph so this will be less cumbersome

# A Grid is basically a 2D array of cells. It also has some extra fancy bells and whistles

class Grid:
    def __init__(self, rows=20, collumns=100):
        self.cells = []
        for i in range(rows):
            self.cells.append([])

            for j in range(collumns):
                self.cells[i].append((i, j))

        # -- since we are using tuples (a primitive) (0,0) == self.cells[0][0] --
        middle_row = rows // 2 
        self.cursor = (collumns // 2, middle_row)
        self.start = (collumns // 8, middle_row)
        self.end = ((collumns // 8) * 7, middle_row)
        self.walls = []


    def move_cursor(self, cell):
        self.cursor = cell


    def is_cursor(self, cell):
        if cell == self.cursor:
            return True
        else:
            return False


    def change_start(self, cell):
        self.start = cell


    def is_start(self, cell):
        if cell == self.start:
            return True
        else:
            return False


    def change_end(self, cell):
        self.end = cell


    def is_end(self, cell):
        if cell == self.end:
            return True
        else:
            return False

    
    def add_wall(self, cell):
        self.walls.append(cell)


    def remove_wall(self, cell):
        self.walls.remove(cell)


    def is_wall(self, cell):
        return_val = False
        for wall in walls:
            if cell == wall:
                return_val = True
                break
        return return_val
 


    # used to check allignment before adding visuals
    def display(self):
        print('***** Printing Grid *****')
        print('cursor:', self.cursor)
        print('start:', self.start)
        print('end:', self.end)
        print('walls:', self.walls)
        for i in range(len(self.cells)):
            row_print = ''

            for j in range(len(self.cells[i])):
                row_print += f'{self.cells[i][j]} | '

            print(row_print)



grid = Grid()
grid.display()

