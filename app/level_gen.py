import random

class Level:

    def __init__(self, size, enemies, boxes, items, preset = None):
        self.size = size
        self.num_enemies = enemies
        self.num_boxes = boxes
        self.num_items = items
        self.wormholes = False
        self.preset = preset
        self.map = self.generate_level()
        

    def blocks_in_radius(self, map, pos):
        above_row = pos[1] - 1
        below_row = pos[1] + 1
        block_count = 0 
        if above_row >= 0:
            for x_pos in range(pos[0] - 1, pos[0] + 2):
                try:
                    if map[above_row][x_pos] == 'B':
                        block_count += 1
                except IndexError:
                    block_count += 3
                
        if below_row < self.size[1]:
            for x_pos in range(pos[0] - 1, pos[0] + 2):
                try:
                    if map[below_row][x_pos] == 'B':
                        block_count += 1
                except IndexError:
                    block_count += 3
        try:
            if map[pos[1]][pos[0] + 1] == 'B':
                block_count += 1
        except IndexError:
            pass
        try:
            if map[pos[1]][pos[0] - 1] == 'B':
                block_count += 1
        except IndexError:
            pass

        return block_count
        
    def enough_blocks(self, map):
        block_count = 0
        total_space = self.size[0] * self.size[1]
        for row in map:
            block_count += row.count('B')
        if block_count / total_space < .5:
            return False
        else:
            return True

    def gen_start_end(self, map):
        for symbol in ['@', '%']:
            on_path = False
            while not on_path:
                
                cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                if map[cursor[1]][cursor[0]] == 'B':
                    on_path = True
            map[cursor[1]][cursor[0]] = symbol
            if symbol == '@':
                self.start_coords = cursor
            else:
                self.end_coords = cursor


        return map

    def gen_enemies(self, map):
        self.enemy_coords = []
        for i in range(self.num_enemies):
            on_path = False
            while not on_path:
                cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                if map[cursor[1]][cursor[0]] == 'B':
                    on_path = True
            map[cursor[1]][cursor[0]] = '!'
            self.enemy_coords.append((cursor[0], cursor[1]))
        return map

    def gen_boxes(self, map):
        self.box_coords = []
        for i in range(self.num_boxes):
            on_path = False
            while not on_path:
                cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                if map[cursor[1]][cursor[0]] == 'B':
                    on_path = True
            map[cursor[1]][cursor[0]] = '8'
            self.box_coords.append((cursor[0], cursor[1]))
        return map

    def gen_items(self, map):
        self.item_coords = []
        for i in range(self.num_items):
            on_path = False
            while not on_path:
                cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                if map[cursor[1]][cursor[0]] == 'B':
                    on_path = True
            map[cursor[1]][cursor[0]] = '$'
            self.item_coords.append((cursor[0], cursor[1]))
        return map

    def gen_wormholes(self, map):
        self.wormhole_coords = []
        for i in range(2):
            on_path = False
            while not on_path:
                cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                if map[cursor[1]][cursor[0]] == 'B':
                    on_path = True
            map[cursor[1]][cursor[0]] = '&'
            self.wormhole_coords.append((cursor[0], cursor[1]))
        return map
    
    def gen_vending(self, map):
        self.vending_coords = ()
        if random.randint(1, 2):
            on_path = False
            while not on_path:
                cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                if map[cursor[1]][cursor[0]] == 'B':
                    on_path = True
            map[cursor[1]][cursor[0]] = '9'
            self.vending_coords = (cursor[0], cursor[1])
        return map


    def generate_level(self):
        if self.preset == None:
            map = [['#' for column in range(self.size[0])] for row in range(self.size[1])]

            first_path = True

            while not self.enough_blocks(map):
                if first_path:
                    cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                else:
                    on_path = False
                    while not on_path:
                        cursor = [random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)]
                        if map[cursor[1]][cursor[0]] == 'B':
                            on_path = True

                stop_path = False
                direction = random.randint(0, 3)
                while not stop_path:
                    try:
                        if self.blocks_in_radius(map, cursor) <= 3:
                            map[cursor[1]][cursor[0]] = 'B'
                            first_path = False
                        else:
                            stop_path = True
                        if direction == 0:
                            cursor[0] += 1
                        elif direction == 1:
                            cursor[1] -= 1
                        elif direction == 2:
                            cursor[0] -= 1
                        elif direction == 3:
                            cursor[1] += 1
                        if cursor[0] < 0 or cursor[1] < 0:
                            stop_path = True
                        if random.randint(0, 1) == 0:
                            direction = random.randint(0, 3)
                        
                    except IndexError:
                        stop_path = True
            map = self.gen_vending(map)
        else:
            map = self.preset
            
        map = self.gen_start_end(map)
        map = self.gen_enemies(map)
        map = self.gen_boxes(map)
        map = self.gen_items(map)
        
        if random.randint(0, 1) == 1:
            self.wormholes = True
            map = self.gen_wormholes(map)

        return map

    def display(self):
        for row in self.map:
            print(row)
            
            
            



def Main():
    level = Level((10, 10), 3, 3, 3)
    level.display()
if __name__ in '__main__':
    Main()