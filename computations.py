"""
This file handles all the computations of the program.

All the corresponding global mean sea level values are in mm.
The details of each computation is in its function docstring.

This file is Copyright (c) 2020 Yousuf Hassan, Aaditya Mandal, Faraz Hossein, and Dinkar Verma.
"""

import csv
import pprint
from typing import Dict, List
import python_ta
import pygame
import sys
import time
from typing import Tuple


def read_csv(filename: str) -> Dict[str, float]:
    """ Read the csv file and return a dictionary mapping the years to the global mean
    sea levels.
    """
    average_data = {}
    with open(filename) as file:
        reader = csv.reader(file)

        for _ in range(0, 8):  # skip over the first 8 rows
            next(reader)

        for row in reader:
            if row[4] != '':
                average_data[row[0]] = float(row[4])
            elif row[3] != '':
                average_data[row[0]] = float(row[3])
            elif row[2] != '':
                average_data[row[0]] = float(row[2])
            else:
                average_data[row[0]] = float(row[1])

        return average_data


def mean_sea_level_change(csv_data: Dict[str, float]) -> Dict[str, float]:
    """ Calculate the average global mean sea level for each year and return a dictionary
    mapping the years to the average global mean sea levels for that year.

    This function calculates the average global mean sea level by adding all the values
    for a specific year and then dividing it by the total amount of values.


    """
    average_data = {}

    for year in csv_data:
        whole_year = year[0:4]
        if whole_year not in average_data:
            average_data[whole_year] = [csv_data[year]]
        else:
            average_data[whole_year].append(csv_data[year])

    for year in average_data:
        average_data[year] = round(sum(average_data[year]) / len(average_data[year]), 2)

    return average_data


def predict_2021_2080(sea_level_2020: float) -> Dict[str, float]:
    """ Predict the global mean sea level for each year from 2021 to 2080 and return a
    dictionary mapping the years to the global mean sea level for that year.

    According to NASA, the rate of change is 3.3mm per year.
    """
    data_2021 = {'2020': sea_level_2020}

    for year in range(2021, 2081):
        data_2021[str(year)] = round(data_2021[str(year - 1)] + 3.3, 2)

    return data_2021


def predict_2081_2100(sea_level_2080: float) -> Dict[str, float]:
    """ Predict the global mean sea level for each year from 2081 to 2100 and return a
    dictionary mapping the years to the global mean sea level for that year.

    The rate of change is on average 12mm per year from 2080-2100 (Church et al).
    """
    data_2081 = {'2080': sea_level_2080}

    for year in range(2081, 2101):
        data_2081[str(year)] = round(data_2081[str(year - 1)] + 12.0, 2)

    return data_2081


def combine_data(data_1993: Dict[str, float], data_2021: Dict[str, float],
                 data_2081: Dict[str, float]) -> Dict[str, float]:
    """ Return a combination of all three dictionaries.
    """
    data_1993.update(data_2021)
    data_1993.update(data_2081)

    return data_1993


def factor_contribution(total_data: Dict[str, float]) -> Dict[str, List[float]]:
    """Return a dictionary mapping the years to a list containing global mean sea level
    change.

    The 0th index of the list is the global mean sea level rise due to the ocean heat capacity.
    The 1st index of the list is the global mean sea level rise due to melting glaciers.
    The 2nd index of the list is the global mean sea level rise due to melting ice sheets.

    After performing calculations on Table 13.1, we find that on average, roughly 41% of the global
    mean sea level rise is a result of thermal expansion due to ocean heat contents, 35% is a
    result of melting glaciers, and 24% is a result of melting ice sheets (Church et al. 1151).
    """
    factor_data = {}

    for year in total_data:
        heat_capacity_contribution = round(0.41 * total_data[year], 2)
        glaciers_contribution = round(0.35 * total_data[year], 2)
        ice_sheets_contribution = round(0.24 * total_data[year], 2)
        factor_data[year] = [heat_capacity_contribution, glaciers_contribution,
                             ice_sheets_contribution]

    return factor_data


pygame.init()  # Initializing pygame

# Setting variables for various RGB colours
LIGHT_GREY = (201, 201, 201)
BLACK = (0, 0, 0)
LIGHT_BLUE = (151, 203, 255)
WHITE = (255, 255, 255)
WATER = (51, 187, 255)
RED = (255, 0, 0)

# Setting up pygame window
SCREENWIDTH = 600
SCREENHEIGHT = 600
display_surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)

# Loading in all images
image = pygame.image.load('male.png')
female = pygame.image.load('female.png')
venice = pygame.image.load('venice2.jpeg')
new_york = pygame.image.load('newyork.jpg')
amsterdam = pygame.image.load('Amsterdam.png')
ocean = pygame.image.load('realocean.jpg')
sky = pygame.image.load('sky.jpg')
home_screen = pygame.image.load('homescreenimage.jpg')
water = pygame.image.load('ocean.png')

# Transforming the dimensions of various images
real_ocean = pygame.transform.scale(ocean, (600, 178))
female1 = pygame.transform.scale(female, (600, 550))
sky_1 = pygame.transform.scale(sky, (600, 600))
home_screen1 = pygame.transform.scale(home_screen, (600, 600))
new_york1 = pygame.transform.scale(new_york, (600, 600))
amsterdam1 = pygame.transform.scale(amsterdam, (600, 600))

# Setting up fonts and pygame display caption
font = pygame.font.SysFont('arial', 30)
font2 = pygame.font.SysFont('cambria', 50)
font3 = pygame.font.SysFont('arial', 15)
pygame.display.set_caption("Sea Level Rise Simulator")

# Organizing the yearly data
data = read_csv('Datasets/global_mean_sea_level.csv')
data_1993_2020 = mean_sea_level_change(data)
data_2021_2080 = predict_2021_2080(data_1993_2020['2020'])
data_2081_2100 = predict_2081_2100(data_2021_2080['2080'])
data = combine_data(data_1993_2020, data_2021_2080, data_2081_2100)

scale_human_data = {}
scale_venice_data = {}
scale_newyork_data = {}
scale_amsterdam_data = {}

for i in data:
    scale_human_data[i] = data[i] / 3
    scale_venice_data[i] = data[i] / 13
    scale_newyork_data[i] = data[i] / 60
    scale_amsterdam_data[i] = data[i] / 20

current_year = 1993


class Button:
    """A class representing a clickable button in the pygame display.

    Instance Attributes:
        - color: RGB tuple of a valid color (color of the button)
        - x: The center x value of the button
        - y: The center y value of the button
        - width: The width of the button
        - height: The height of the button
        - name: The name displayed on the button

    Representation Invariants:
        - len(self.color) == 3
        - 0 <= self.color[0] <= 255
        - 0 <= self.color[1] <= 255
        - 0 <= self.color[2] <= 255
        - self.width >= 0
        - self.height >= 0
    """
    color: Tuple[int, int, int]
    x: int
    y: int
    width: int
    height: int
    name = str

    def __init__(self, color: Tuple[int, int, int], x: float, y: float, width: int, height: int, name: str) -> None:
        """Initialize a new button with the specified parameters

        Preconditions:
            - len(color) == 3
            - 0 <= color[0] <= 255
            - 0 <= color[1] <= 255
            - 0 <= color[2] <= 255
            - width >= 0
            - height >= 0
        """
        self.color = color
        self.x = int(x - (width / 2))
        self.y = int(y - (height / 2))
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window) -> None:
        """method to draw the button on the screen"""
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.name != '':
            text1 = font.render(self.name, True, (0, 0, 0))
            screen.blit(text1, (
                self.x + (self.width / 2 - text1.get_width() / 2),
                self.y + (self.height / 2 - text1.get_height() / 2)))

    def over_button(self, position) -> bool:
        """Determine whether position of mouse is over the button or not"""
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True

        return False


Main = True
homeScreen = True
Demo = False
simulationVenice = False
simulationTwo = False
simulationThree = False
simulationFour = False

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

button1 = Button(LIGHT_GREY, SCREENWIDTH / 4, SCREENHEIGHT / 2, 275, 75, 'Human Simulation')
button2 = Button(LIGHT_GREY, SCREENWIDTH * (3 / 4), 400, 275, 75, 'Venice Simulation')
button3 = Button(LIGHT_GREY, SCREENWIDTH * (3 / 4), SCREENHEIGHT / 2, 275, 75, 'New York Simulation')
button4 = Button(LIGHT_GREY, SCREENWIDTH / 4, 400, 275, 75, 'Amsterdam Simulation')

demo_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')
venice_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')
newyork_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')
amsterdam_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')

while Main is True:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            Main = False
            pygame.quit()
            sys.exit()

    # Home Screen
    while homeScreen is True:
        display_surface.blit(home_screen1, (0, 0))
        button1.draw(display_surface)
        button2.draw(display_surface)
        button3.draw(display_surface)
        button4.draw(display_surface)
        title_text = font2.render('Sea Level Rise Simulator', True, BLACK)
        title_text_rect = title_text.get_rect(center=(SCREENWIDTH / 2, 125))
        screen.blit(title_text, title_text_rect)

        # --- Main event loop
        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:  # If user clicked close
                homeScreen = False  # Flag that we are done so we exit this loop
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.over_button(pos) is True:
                    homeScreen = False
                    Demo = True
                if button2.over_button(pos) is True:
                    homeScreen = False
                    simulationVenice = True
                if button3.over_button(pos) is True:
                    homeScreen = False
                    simulationTwo = True
                if button4.over_button(pos) is True:
                    homeScreen = False
                    simulationThree = True

            if event.type == pygame.MOUSEMOTION:
                if button1.over_button(pos) is True:
                    button1.color = LIGHT_BLUE
                elif button2.over_button(pos) is True:
                    button2.color = LIGHT_BLUE
                elif button3.over_button(pos) is True:
                    button3.color = LIGHT_BLUE
                elif button4.over_button(pos) is True:
                    button4.color = LIGHT_BLUE
                else:
                    button1.color = LIGHT_GREY
                    button2.color = LIGHT_GREY
                    button3.color = LIGHT_GREY
                    button4.color = LIGHT_GREY

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Human Demo
    while Demo is True:
        display_surface.blit(sky_1, (0, 0))
        demo_back_button.draw(display_surface)
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:  # If user clicked close
                Demo = False  # Flag that we are done so we exit this loop
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if demo_back_button.over_button(pos) is True:
                    Demo = False
                    homeScreen = True
                    current_year = 1993

            if event.type == pygame.MOUSEMOTION:
                if demo_back_button.over_button(pos) is True:
                    demo_back_button.color = LIGHT_BLUE
                else:
                    demo_back_button.color = LIGHT_GREY

        # --- Go ahead and update the screen with what we've drawn.
        water_height = 600
        keys = pygame.key.get_pressed()
        if 1993 < current_year < 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.1)
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.1)

        if current_year == 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.1)

        if current_year == 1993:
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.1)

        # Code to change the years
        year_label = font.render(('Year: ' + str(current_year)), True, BLACK, LIGHT_GREY)
        year_textRect = year_label.get_rect()
        year_textRect.center = (540, 15)
        display_surface.blit(year_label, year_textRect)

        display_surface.blit(image, (100, 28))
        display_surface.blit(female1, (100, 70))

        year_string = str(current_year)
        # Water part

        scale_factor = (water_height - int(scale_human_data[year_string]))
        display_surface.blit(water, (0, scale_factor))
        # pygame.draw.rect(display_surface, WATER, (0, scale_factor, 1000, 1000))

        # Line at bottom
        pygame.draw.line(display_surface, BLACK, (0, 800), (1000, 800), 3)

        human_height_text = font.render('5\'9', True, BLACK)
        human_height_text_rect = human_height_text.get_rect(center=(196, 14))
        female_height_text = font.render('5\'3', True, BLACK)
        female_height_text_rect = female_height_text.get_rect(center=(400, 76))
        screen.blit(human_height_text, human_height_text_rect)
        screen.blit(female_height_text, female_height_text_rect)

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(15)

    # Simulation Venice
    while simulationVenice is True:
        display_surface.fill(WHITE)
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:  # If user clicked close
                simulationVenice = False  # Flag that we are done so we exit this loop
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if venice_back_button.over_button(pos) is True:
                    simulationVenice = False
                    homeScreen = True
                    current_year = 1993

            if event.type == pygame.MOUSEMOTION:
                if venice_back_button.over_button(pos) is True:
                    venice_back_button.color = LIGHT_BLUE
                else:
                    venice_back_button.color = LIGHT_GREY

        # --- Go ahead and update the screen with what we've drawn.
        water_height = 535
        display_surface.blit(venice, (-200, 0))
        newyork_back_button.draw(display_surface)
        keys = pygame.key.get_pressed()
        if 1993 < current_year < 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.1)
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.1)

        if current_year == 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.1)

        if current_year == 1993:
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.1)

        # Code to change the years
        year_label = font.render(('Year: ' + str(current_year)), True, BLACK, LIGHT_GREY)
        year_textRect = year_label.get_rect()
        year_textRect.center = (540, 15)
        display_surface.blit(year_label, year_textRect)

        year_string = str(current_year)
        # Water part
        scale_factor = (water_height - int(scale_venice_data[year_string]))
        display_surface.blit(real_ocean, (0, scale_factor))
        venice_back_button.draw(display_surface)
        # pygame.draw.rect(display_surface, WATER, (0, scale_factor, 1000, 1000))

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Simulation Two
    while simulationTwo is True:
        display_surface.fill(WHITE)
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:  # If user clicked close
                simulationTwo = False  # Flag that we are done so we exit this loop
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if newyork_back_button.over_button(pos) is True:
                    simulationTwo = False
                    homeScreen = True
                    current_year = 1993

            if event.type == pygame.MOUSEMOTION:
                if newyork_back_button.over_button(pos) is True:
                    newyork_back_button.color = LIGHT_BLUE
                else:
                    newyork_back_button.color = LIGHT_GREY
        water_height = 532
        display_surface.blit(new_york1, (0, 0))
        newyork_back_button.draw(display_surface)
        keys = pygame.key.get_pressed()
        if 1993 < current_year < 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.08)
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.08)

        if current_year == 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.08)

        if current_year == 1993:
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.08)

        # Code to change the years
        year_label = font.render(('Year: ' + str(current_year)), True, BLACK, LIGHT_GREY)
        year_textRect = year_label.get_rect()
        year_textRect.center = (540, 15)
        display_surface.blit(year_label, year_textRect)

        year_string = str(current_year)
        # Water part
        scale_factor = (water_height - int(scale_newyork_data[year_string]))
        display_surface.blit(real_ocean, (0, scale_factor))
        # pygame.draw.rect(display_surface, WATER, (0, scale_factor, 1000, 1000))

        if current_year == 2100:
            title_text = font3.render('This may not look like a significant change compared to the size', True,
                                      BLACK)
            title_text_rect = title_text.get_rect(center=(SCREENWIDTH / 2, 50))
            screen.blit(title_text, title_text_rect)
            title_text2 = font3.render('of the Statue of Liberty Island, but throughout time, as the water rises,',
                                       True, BLACK)
            title_text_rect2 = title_text2.get_rect(center=(SCREENWIDTH / 2, 70))
            screen.blit(title_text2, title_text_rect2)
            title_text3 = font3.render('the water will begin to seep into the concrete foundation and '
                                       'break it down, causing structural damage',
                                       True, BLACK)
            title_text_rect3 = title_text3.get_rect(center=(SCREENWIDTH / 2, 90))
            screen.blit(title_text3, title_text_rect3)

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Simulation Three
    while simulationThree is True:
        display_surface.fill(WHITE)
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:  # If user clicked close
                simulationThree = False  # Flag that we are done so we exit this loop
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if amsterdam_back_button.over_button(pos) is True:
                    simulationThree = False
                    homeScreen = True
                    current_year = 1993

            if event.type == pygame.MOUSEMOTION:
                if amsterdam_back_button.over_button(pos) is True:
                    amsterdam_back_button.color = LIGHT_BLUE
                else:
                    amsterdam_back_button.color = LIGHT_GREY
        water_height = 525
        display_surface.blit(amsterdam1, (0, 0))
        amsterdam_back_button.draw(display_surface)

        keys = pygame.key.get_pressed()
        if 1993 < current_year < 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.1)
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.1)

        if current_year == 2100:
            if keys[pygame.K_LEFT]:
                current_year += -1
                time.sleep(0.1)

        if current_year == 1993:
            if keys[pygame.K_RIGHT]:
                current_year += 1
                time.sleep(0.1)

        # Code to change the years
        year_label = font.render(('Year: ' + str(current_year)), True, BLACK, LIGHT_GREY)
        year_textRect = year_label.get_rect()
        year_textRect.center = (540, 15)
        display_surface.blit(year_label, year_textRect)

        year_string = str(current_year)
        # Water part
        scale_factor = (water_height - int(scale_amsterdam_data[year_string]))
        display_surface.blit(real_ocean, (0, scale_factor))
        # pygame.draw.rect(display_surface, WATER, (0, scale_factor, 1000, 1000))

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)


if __name__ == '__main__':
    data = read_csv('Datasets/global_mean_sea_level.csv')
    data_1993_2020 = mean_sea_level_change(data)
    data_2021_2080 = predict_2021_2080(data_1993_2020['2020'])
    data_2081_2100 = predict_2081_2100(data_2021_2080['2080'])
    combined_data = combine_data(data_1993_2020, data_2021_2080, data_2081_2100)
    pprint.pprint(combined_data)
    pprint.pprint(factor_contribution(combined_data))


python_ta.check_all(config={
    'extra-imports': ['csv', 'Dict', 'List', 'pprint'],  # the names (strs) of imported modules
    'allowed-io': ['read_csv'],  # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['R1705', 'C0200']
})
