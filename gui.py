from tkinter import *
from time import sleep

class Rectangle:
    def __init__(self, x, y, min_x, min_y, max_x, max_y):
        self.x = x
        self.y = y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.type = 'open'

    def __str__(self):
        return 'X: {} Y: {} Type: {}'.format(self.x, self.y, self.type)

    def __eq__(self, other):
        if type(other) is Rectangle:
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y

    def set_type(self, rect_type):
        # open, start, finish, wall, frontier, path, explored
        if (self.type == 'start' or self.type == 'finish') and \
                (rect_type == 'frontier' or rect_type == 'path' \
                or rect_type == 'explored'):
            return
        self.type = rect_type

    def color(self):
        if self.type == 'wall':
            return 'black'
        if self.type == 'start':
            return 'green'
        if self.type == 'finish' or self.type == 'end':
            return 'red'
        if self.type == 'frontier' or self.type == 'boarder':
            return 'light slate blue'
        if self.type == 'explored':
            return 'cyan'
        if self.type == 'path':
            return 'orange'
        return 'white'

    def essential(self):
        if self.type == 'start' or self.type == 'finish' or self.type == 'wall':
            return True
        return False

class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Path Algorithm Visualizer")

        ### Constants ###
        dropdown_size = 20
        # Buttons
        height_label_size = 10
        width_label_size = 10
        # Height and Width
        self.default_height = 5
        self.default_width = 5
        self.max_height = 100
        self.max_width = 100
        self.min_height = 3
        self.min_width = 3
        # Colors
        self.background_color = 'white'
        self.line_color = 'black'
        # Run
        self.default_speed = 0.1

        ### Initialize class variables ###
        self.canvas_width = -1
        self.canvas_height = -1
        self.row_count = -1
        self.col_count = -1
        self.start_rect = None
        self.finish_rect = None
        self.start_or_finish = 0

        ### Set algorithm dropdown options ###
        self.populate_algorithms()
        # Create algorithm variable
        self.algorithm_variable = StringVar(self.master)
        self.algorithm_variable.set(self.possible_algorithms[0])
        # Create dropdown
        self.algorithm_dropdown = OptionMenu(self.master,
                self.algorithm_variable,
                *self.possible_algorithms)
        self.algorithm_dropdown.config(width=dropdown_size)
        # Make label
        self.algorithm_label = Label(self.master, text='Algorithm Selection')
        # Place on grid
        self.algorithm_label.grid(row=0, column=0)
        self.algorithm_dropdown.grid(row=1, column=0)

        ### Set height ###
        # Variable to hold height
        self.height_variable = IntVar(self.master, value=self.default_height)
        self.height_variable.trace('w', self.make_canvas)
        # Create entry with callback to make_canvas
        self.height_entry = Entry(self.master, width=height_label_size,
                textvariable=self.height_variable)
        # Make label
        self.height_label = Label(self.master, text='Grid Height')
        # Place on grid
        self.height_label.grid(row=0, column=1)
        self.height_entry.grid(row=1, column=1)

        ### Set width ###
        # Variable to hold width
        self.width_variable = IntVar(self.master, value=self.default_width)
        self.width_variable.trace('w', self.make_canvas)
        # Create entry with callback to make_canvas
        self.width_entry = Entry(self.master, width=width_label_size,
                textvariable=self.width_variable)
        # Make label
        self.width_label = Label(self.master, text='Grid Width')
        # Place on grid
        self.width_label.grid(row=0, column=2)
        self.width_entry.grid(row=1, column=2)

        ### Run Speed ###
        # Variable to hold speed
        self.speed_variable = DoubleVar(self.master, value=self.default_speed)
        # Create entry
        self.speed_entry = Entry(self.master, width=width_label_size,
                textvariable=self.speed_variable)
        # Make label
        self.speed_label = Label(self.master, text='Run Speed')
        # Place on grid
        self.speed_label.grid(row=0, column=3)
        self.speed_entry.grid(row=1, column=3)

        ### Reset grid button ###
        self.reset_button = Button(self.master,
                text='Reset Grid',
                command=self.reset_grid)
        self.reset_button.grid(row=1, column=4)

        ### Run Button ###
        self.run_button = Button(self.master, text='Run', command=self.run)
        self.run_button.grid(row=1, column=5)

        ### Make default canvas ###
        self.make_canvas()
        self.create_grid(force=True)

    def populate_algorithms(self):
        self.possible_algorithms = [
                'A*',
                'Depth First Search',
                'Dijkstra\'s',
                'Greedy Breadth First Search']

    def make_canvas(self, *args):
        ### Validate height and width ###
        # Get rows and cols
        try:
            height = self.height_variable.get()
            width = self.width_variable.get()
        except:
            return

        # If unchanged, ignore
        #if height == self.row_count and width == self.col_count:
        #    return

        # Validate bounds
        height = max(height, self.min_height)
        height = min(height, self.max_height)
        width = max(width, self.min_width)
        width = min(width, self.max_width)

        # Set value
        try:
            self.height_variable.set(height)
            self.width_variable.set(width)
        except:
            pass

        # Print
        try:
            print('Height: {}, Width: {}'.format(
                self.height_variable.get(),
                self.width_variable.get()))
        except:
            pass

        ### Remove Old Canvas ###
        try:
            self.canvas.grid_forget()
        except:
            pass

        ### Make Canvas ###
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.canvas = Canvas(self.master,
                #width=self.default_width,
                #height=self.default_height,
                bg=self.background_color)
        self.canvas.grid(row=2, columnspan=6, sticky=W+E+N+S, padx=5, pady=0)

        ### Make Bindings ###
        # Widget resize
        self.canvas.bind('<Configure>', self.create_grid)
        # left click on grid
        self.canvas.bind('<Button-1>', self.create_wall)
        # Left click and drag on grid
        self.canvas.bind('<B1-Motion>', self.create_wall)
        # Right click and drag on grid
        self.canvas.bind('<B3-Motion>', self.remove_wall)
        # Right click on grid
        self.canvas.bind('<Button-3>', self.create_start_finish_rect)

        ### Make grid ###
        self.create_grid()

    def create_grid(self, force=False, *args):
        # Get canvas width and height
        self.master.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Get number of rows and columns to produce
        try:
            rows = self.height_variable.get()
            cols = self.width_variable.get()
        except:
            pass

        # If no change, we good
        if self.canvas_width == width and self.canvas_height == height and self.row_count == rows and self.col_count == cols and force == False:
            return

        # Set row and col counds
        self.row_count = rows
        self.col_count = cols

        # Remember old width and height
        self.canvas_width = width
        self.canvas_height = height
        print('Canvas Height: {}, Width: {}'.format(height, width))

        # Remove old grid
        self.canvas.delete('all')


        # Create horizontal lines (rows)
        rows_space_between = height // rows
        # Create vertical lines (columns)
        cols_space_between = width // cols

        self.grid_xy_to_rect = {}
        self.grid_rect_to_xy = {}
        # make box class instead
        self.grid_spaces = []
        for y in range(rows):
            for x in range(cols):
                min_x = x * cols_space_between
                min_y = y * rows_space_between
                max_x = (x + 1) * cols_space_between
                max_y = (y + 1) * rows_space_between
                rect = Rectangle(x, y, min_x, min_y, max_x, max_y)
                self.color_rect(rect)
                self.grid_spaces.append(rect)
                self.grid_xy_to_rect[(x, y)] = rect
                for m_x in range(min_x, max_x):
                    for m_y in range(min_y, max_y):
                        self.grid_rect_to_xy[(m_x, m_y)] = rect

        self.start_rect = None
        self.finish_rect = None

    def color_rect(self, rect : Rectangle):
        print(rect)
        rect.rect = self.canvas.create_rectangle(
                rect.min_x, rect.min_y,
                rect.max_x, rect.max_y,
                fill=rect.color())

    def recolor_rect(self, rect : Rectangle):
        print(rect)
        self.canvas.itemconfig(rect.rect,
                fill= rect.color(),
                outline=self.line_color)
        self.canvas.update_idletasks()

    def create_wall(self, *args):
        # Grab event
        event = args[0]
        # Get coordinates
        x = event.x
        y = event.y
        print('Cursor X: {}, Y: {}'.format(x, y))
        # Get rectangle
        rect = self.grid_rect_to_xy[(x, y)]
        # Change rectangle to wall color
        rect.set_type('wall')
        self.recolor_rect(rect)

    def remove_wall(self, *args):
        # Grab event
        event = args[0]
        # Get coordinates
        x = event.x
        y = event.y
        # Get rectangle
        rect = self.grid_rect_to_xy[(x, y)]
        # Change rectangle to background color
        rect.set_type('open')
        self.recolor_rect(rect)

    def create_start_finish_rect(self, *args):
        # Grab event
        event = args[0]
        # Get coordinates
        x = event.x
        y = event.y
        # Get rectange
        rect = self.grid_rect_to_xy[(x, y)]
        # Make rectangle a start or finish rect
        #   if one already exists, reset the old one
        if self.start_or_finish % 2 == 0:
            rect.set_type('start')
            if self.start_rect is not None:
                self.start_rect.set_type('open')
                self.recolor_rect(self.start_rect)
            self.start_rect = rect
        else:
            rect.set_type('finish')
            if self.finish_rect is not None:
                self.finish_rect.set_type('open')
                self.recolor_rect(self.finish_rect)
            self.finish_rect = rect
        self.start_or_finish += 1
        self.recolor_rect(rect)

    def reset_grid(self):
        self.create_grid(force=True)

    def soft_reset_grid(self):
        '''Reset grid, but keep goal, finish, and walls
        '''
        for rect in self.grid_spaces:
            if not rect.essential():
                rect.set_type('open')
                self.recolor_rect(rect)

    def run(self):
        '''
        Class variables:
            self.algorithm_variable = current algorithm
        '''
        if self.start_rect == None or self.finish_rect == None:
            return

        self.soft_reset_grid()

        if self.algorithm_variable.get() == 'A*':
            self.algorithm_a_star()
        elif self.algorithm_variable.get() == 'Dijkstra\'s':
            self.algorith_dijkstra()
        elif self.algorithm_variable.get() == 'Depth First Search':
            self.algorithm_dfs()
        elif self.algorithm_variable.get() == 'Greedy Breadth First Search':
            self.algorithm_gbfs()


    def algorithm_a_star(self):
        from queue import PriorityQueue

        start = self.start_rect
        goal = self.finish_rect

        frontier = PriorityQueue()
        frontier.put((0, start))
        explored = set([start])
        parent = {}
        distance_from_start = {start: 0}

        while frontier.empty() == False and goal not in parent:
            self.rest()

            dist, current = frontier.get()
            print('{} {}'.format(dist, current))
            current.set_type('explored')
            self.recolor_rect(current)

            for near in self.cardinal_rects(current):
                if near not in explored:
                    near.set_type('frontier')
                    self.recolor_rect(near)
                    parent[near] = current
                    explored.add(near)
                    distance_from_start[near] = distance_from_start[current] + 1
                    distance = self.a_star_distance(near,
                            distance_from_start[near], goal)
                    frontier.put((distance, near))

        self.make_path(start, goal, parent)


    def algorith_dijkstra(self):
        from queue import Queue
        start = self.start_rect
        goal = self.finish_rect

        frontier = Queue()
        frontier.put(start)
        explored = set([start])
        parent = {}

        while frontier.empty() == False and goal not in parent:
            self.rest()

            current = frontier.get()
            current.set_type('explored')
            self.recolor_rect(current)

            for near in self.cardinal_rects(current):
                if near not in explored and near.type != 'wall':
                    parent[near] = current
                    frontier.put(near)
                    explored.add(near)
                    near.set_type('frontier')
                    self.recolor_rect(near)

        self.make_path(start, goal, parent)

    def algorithm_dfs(self):
        start = self.start_rect
        goal = self.finish_rect

        frontier = [start]
        explored = set([start])
        parent = {}

        while len(frontier) != 0 and goal not in parent:
            self.rest()

            current = frontier.pop()
            current.set_type('explored')
            self.recolor_rect(current)

            for near in self.cardinal_rects(current):
                if near not in explored:
                    near.set_type('frontier')
                    self.recolor_rect(near)
                    frontier.append(near)
                    parent[near] = current
                    explored.add(near)

        self.make_path(start, goal, parent)

    def algorithm_gbfs(self):
        from queue import PriorityQueue

        start = self.start_rect
        goal = self.finish_rect

        frontier = PriorityQueue()
        frontier.put((0, start))
        explored = set([start])
        parent = {}

        while frontier.empty() == False and goal not in parent:
            self.rest()

            current = frontier.get()[1]
            current.set_type('explored')
            self.recolor_rect(current)

            for near in self.cardinal_rects(current):
                if near not in explored:
                    near.set_type('frontier')
                    self.recolor_rect(near)
                    explored.add(near)
                    parent[near] = current
                    frontier.put((abs(goal.x - near.x) + abs(goal.y - near.y), near))

        self.make_path(start, goal, parent)


    def rest(self):
        try:
            sleep(self.speed_variable.get())
        except:
            pass

    def make_path(self, start : Rectangle, goal : Rectangle, parent : dict):
        if goal in parent:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.pop()
            path.reverse()
            path.pop()
            for rect in path:
                try:
                    sleep(self.speed_variable.get())
                except:
                    pass
                rect.set_type('path')
                self.recolor_rect(rect)

    def cardinal_rects(self, rect):
        rects = []
        x = rect.x
        y = rect.y

        if x - 1 >= 0:
            rects.append(self.grid_xy_to_rect[(x-1, y)])
        if x + 1 < self.col_count:
            rects.append(self.grid_xy_to_rect[(x+1, y)])
        if y - 1 >= 0:
            rects.append(self.grid_xy_to_rect[(x, y-1)])
        if y + 1 < self.row_count:
            rects.append(self.grid_xy_to_rect[(x, y+1)])

        final_rects = [r for r in rects if r.type != 'wall']

        return final_rects

    def a_star_distance(self, node : Rectangle,  start_dist : int,
            goal : Rectangle):
        return start_dist + abs(node.x - goal.x) + abs(node.y - goal.y)

root = Tk()
my_gui = GUI(root)
root.mainloop()
