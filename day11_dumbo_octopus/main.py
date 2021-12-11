import os,sys
from copy import deepcopy

###################
## part 1
MAX = 9

def print_grid(data_grid):
    print(" ")
    for l in data_grid:
        list(map(lambda x: print("%3d" % x, end=""), l))
        print("")

def load_grid_from_file(file_name):
    with open(os.path.join(sys.path[0], file_name), "r") as file:
        lines = file.read().splitlines()
    return [list(map(int,x)) for x in lines]

def dots_xy_filtered(grid, lambda_filter):
    dots_xy = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if lambda_filter(grid[x][y]): dots_xy.append((x,y))
    return dots_xy

def adjacent_dots_xy(xy, max_x, max_y):
    x, y = xy[0], xy[1]
    xy_all = [(x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1), (x,y+1), (x+1,y-1), (x+1,y),(x+1,y+1)]
    ret = list(filter(lambda xy: xy[0] >= 0 and xy[1] >= 0 and xy[0] <= max_x and xy[1] <= max_y, xy_all))
    return ret

def dot_flash(grid, dots_xy_flash, flashing_xy):
    dots_xy = adjacent_dots_xy(flashing_xy, len(grid)-1, len(grid[0])-1)

    for xy in dots_xy:
        grid[xy[0]][xy[1]] += 1

    for xy in dots_xy:
        if grid[xy[0]][xy[1]] > MAX and xy not in dots_xy_flash:
            dots_xy_flash.append(xy)
            grid, dots_xy_flash = dot_flash(grid, dots_xy_flash, xy)
    return grid, dots_xy_flash

def one_step(grid):
    # all dots increase 1
    grid_ret = [list(map(lambda x: x+1, x)) for x in grid]

    # find the flashing dots
    grid_flash = [list(map(lambda x: 1 if x > MAX else 0, x)) for x in grid_ret]
    filter = lambda x: x == 1
    dots_xy_flash = dots_xy_filtered(grid_flash, filter)
    if len(dots_xy_flash) == 0: return 0, grid_ret

    # do flash
    dots_xy_flash_all = deepcopy(dots_xy_flash)
    for xy in dots_xy_flash:
        grid_ret, dots_xy_flash_all = dot_flash(grid_ret, dots_xy_flash_all, xy)

    # set flashed dots to 0
    grid_reset = [list(map(lambda x: x if x <= 9 else 0, x)) for x in grid_ret]
    return len(dots_xy_flash_all), grid_reset

def main_part1(grid, steps):
    count = 0
    for i in range(steps):
        count_step,grid = one_step(grid)
        count += count_step
    return count

grid = load_grid_from_file("input_sample.txt")
grid = load_grid_from_file("input.txt")
count = main_part1(grid, 100)
print("part1:", count)

##############################
## part 2

def is_all_flashed(grid):
    grid_sum = 0
    for l in grid:
        grid_sum += sum(l)
    return grid_sum == 0

def main_part2(grid, steps):
    for i in range(steps):
        count_step,grid = one_step(grid)
        if is_all_flashed(grid): return i + 1
    return 0 

step = main_part2(grid, 1000000000)
print("part1:", step)

    