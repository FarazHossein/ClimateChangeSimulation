"""
This file is responsible for the pygame simulation component of the program.

This file is Copyright (c) 2020 Aaditya Mandal, Faraz Hossein, Dinkar Verma, and Yousuf Hassan.
"""

import pygame
import sys
import time
from computations import read_csv, mean_sea_level_change, predict_2021_2080, predict_2081_2100,\
    combine_data
from typing import Tuple
import python_ta


def run_simulation() -> None:
    """This function runs the pygame simulation component of the program.
    """
    pygame.init()  # Initializing pygame

    # Setting variables for various RGB colours
    LIGHT_GREY = (201, 201, 201)
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (151, 203, 255)
    WHITE = (255, 255, 255)
    # WATER = (51, 187, 255)
    # RED = (255, 0, 0)

    # Setting up pygame window
    SCREENWIDTH = 600
    SCREENHEIGHT = 600
    display_surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)

    # Loading in all images
    image = pygame.image.load('Images/male.png')
    female = pygame.image.load('Images/female.png')
    venice = pygame.image.load('Images/venice2.jpeg')
    new_york = pygame.image.load('Images/newyork.jpg')
    amsterdam = pygame.image.load('Images/Amsterdam.png')
    ocean = pygame.image.load('Images/realocean.jpg')
    sky = pygame.image.load('Images/sky.jpg')
    water = pygame.image.load('Images/ocean.png')
    home_screen = pygame.image.load('Images/homescreenimage.jpg')

    # Transforming various image sizes
    real_ocean = pygame.transform.scale(ocean, (600, 178))
    female1 = pygame.transform.scale(female, (600, 550))
    sky_1 = pygame.transform.scale(sky, (600, 600))
    home_screen1 = pygame.transform.scale(home_screen, (600, 600))
    new_york1 = pygame.transform.scale(new_york, (600, 600))
    amsterdam1 = pygame.transform.scale(amsterdam, (600, 600))

    # Setting up font and pygame display caption
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

    # Scaling data to fit visual models
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

        def __init__(self, color: Tuple[int, int, int], x: float, y: float, width: int, height: int,
                     name: str) -> None:
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

    # Setting main and homeScreen to True to begin pygame loops
    Main = True
    homeScreen = True
    Demo = False
    simulationVenice = False
    simulationTwo = False
    simulationThree = False
    # simulationFour = False

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # Creating four instances of button class which will appear on the home screen
    button1 = Button(LIGHT_GREY, SCREENWIDTH / 4, SCREENHEIGHT / 2, 275, 75, 'Human Simulation')
    button2 = Button(LIGHT_GREY, SCREENWIDTH * (3 / 4), 400, 275, 75, 'Venice Simulation')
    button3 = Button(LIGHT_GREY, SCREENWIDTH * (3 / 4), SCREENHEIGHT / 2, 275, 75,
                     'New York Simulation')
    button4 = Button(LIGHT_GREY, SCREENWIDTH / 4, 400, 275, 75, 'Amsterdam Simulation')

    # Creating four instances of button class which are back buttons
    demo_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')
    venice_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')
    newyork_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')
    amsterdam_back_button = Button(LIGHT_GREY, 50, 25, 100, 50, 'Back')

    # Main pygame loop
    while Main is True:
        for event in pygame.event.get():
            # pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                # Main = False
                pygame.quit()
                sys.exit()

        # Home screen loop
        while homeScreen is True:
            display_surface.blit(home_screen1, (0, 0))
            button1.draw(display_surface)
            button2.draw(display_surface)
            button3.draw(display_surface)
            button4.draw(display_surface)
            title_text = font2.render('Sea Level Rise Simulator', True, BLACK)
            title_text_rect = title_text.get_rect(center=(SCREENWIDTH / 2, 125))
            screen.blit(title_text, title_text_rect)

            # Main event loop
            for event in pygame.event.get():  # User did something
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:  # If user clicked close
                    # homeScreen = False  # Flag that we are done so we exit this loop
                    pygame.quit()
                    sys.exit()

                # Switching screens based on which button the user clicks
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

                # Highlighting the buttons to light blue if motion is detected over the buttons
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

            # Updating the screen with everything drawn
            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(60)

        # Human Simulation loop
        while Demo is True:
            display_surface.blit(sky_1, (0, 0))
            demo_back_button.draw(display_surface)

            # Main event loop
            for event in pygame.event.get():  # User did something
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:  # If user clicked close
                    # Demo = False  # Flag that we are done so we exit this loop
                    pygame.quit()
                    sys.exit()

                # Switching screens based on which button the user clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if demo_back_button.over_button(pos) is True:
                        Demo = False
                        homeScreen = True
                        current_year = 1993

                # Highlighting the buttons to light blue if motion is detected over the buttons
                if event.type == pygame.MOUSEMOTION:
                    if demo_back_button.over_button(pos) is True:
                        demo_back_button.color = LIGHT_BLUE
                    else:
                        demo_back_button.color = LIGHT_GREY

            # Increasing and decreasing water levels
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

            # Changing the year indicator
            year_label = font.render(('Year: ' + str(current_year)), True, BLACK, LIGHT_GREY)
            year_textRect = year_label.get_rect()
            year_textRect.center = (540, 15)
            display_surface.blit(year_label, year_textRect)

            # Displaying male and female model
            display_surface.blit(image, (100, 28))
            display_surface.blit(female1, (100, 70))

            year_string = str(current_year)

            # Increment the scale based on number of years
            scale_factor = (water_height - int(scale_human_data[year_string]))

            # Display correct position of water
            display_surface.blit(water, (0, scale_factor))

            # Line at bottom
            pygame.draw.line(display_surface, BLACK, (0, 800), (1000, 800), 3)

            # Drawing human heights on screen
            human_height_text = font.render('5\'9', True, BLACK)
            human_height_text_rect = human_height_text.get_rect(center=(196, 14))
            female_height_text = font.render('5\'3', True, BLACK)
            female_height_text_rect = female_height_text.get_rect(center=(400, 76))
            screen.blit(human_height_text, human_height_text_rect)
            screen.blit(female_height_text, female_height_text_rect)

            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(15)

        # Venice Simulation loop
        while simulationVenice is True:
            display_surface.fill(WHITE)

            # Main event loop
            for event in pygame.event.get():  # User did something
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:  # If user clicked close
                    # simulationVenice = False  # Flag that we are done so we exit this loop
                    pygame.quit()
                    sys.exit()

                # Switching screens based on which button the user clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if venice_back_button.over_button(pos) is True:
                        simulationVenice = False
                        homeScreen = True
                        current_year = 1993

                # Highlighting the buttons to light blue if motion is detected over the buttons
                if event.type == pygame.MOUSEMOTION:
                    if venice_back_button.over_button(pos) is True:
                        venice_back_button.color = LIGHT_BLUE
                    else:
                        venice_back_button.color = LIGHT_GREY

            water_height = 535
            display_surface.blit(venice, (-200, 0))
            newyork_back_button.draw(display_surface)
            keys = pygame.key.get_pressed()

            # Increasing year indicator
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

            # Increment the scale based on number of years
            scale_factor = (water_height - int(scale_venice_data[year_string]))

            # Display correct position of water
            display_surface.blit(real_ocean, (0, scale_factor))

            venice_back_button.draw(display_surface)

            # Updating everything we have drawn
            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(60)

        # New york simulation loop
        while simulationTwo is True:
            display_surface.fill(WHITE)

            # Main event loop
            for event in pygame.event.get():  # User did something
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:  # If user clicked close
                    # simulationTwo = False  # Flag that we are done so we exit this loop
                    pygame.quit()
                    sys.exit()

                # Switching screens based on which button the user clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if newyork_back_button.over_button(pos) is True:
                        simulationTwo = False
                        homeScreen = True
                        current_year = 1993

                # Highlighting the buttons to light blue if motion is detected over the buttons
                if event.type == pygame.MOUSEMOTION:
                    if newyork_back_button.over_button(pos) is True:
                        newyork_back_button.color = LIGHT_BLUE
                    else:
                        newyork_back_button.color = LIGHT_GREY

            water_height = 532
            display_surface.blit(new_york1, (0, 0))
            newyork_back_button.draw(display_surface)
            keys = pygame.key.get_pressed()

            # Updating year indicator
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

            # Increment the scale based on number of years
            scale_factor = (water_height - int(scale_newyork_data[year_string]))

            # Display correct position of water
            display_surface.blit(real_ocean, (0, scale_factor))

            if current_year == 2100:
                title_text = font3.render(
                    'This may not look like a significant change compared to the size', True, BLACK)
                title_text_rect = title_text.get_rect(center=(SCREENWIDTH / 2, 50))
                screen.blit(title_text, title_text_rect)
                title_text2 = font3.render(
                    'of the Statue of Liberty Island, but throughout time, as the water rises,',
                    True, BLACK)
                title_text_rect2 = title_text2.get_rect(center=(SCREENWIDTH / 2, 70))
                screen.blit(title_text2, title_text_rect2)
                title_text3 = font3.render(
                    'the water will begin to seep into the concrete foundation and '
                    'break it down, causing structural damage', True, BLACK)
                title_text_rect3 = title_text3.get_rect(center=(SCREENWIDTH / 2, 90))
                screen.blit(title_text3, title_text_rect3)

            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(60)

        # Amsterdam Simulation Loop
        while simulationThree is True:
            display_surface.fill(WHITE)

            # Main event loop
            for event in pygame.event.get():  # User did something
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:  # If user clicked close
                    # simulationThree = False  # Flag that we are done so we exit this loop
                    pygame.quit()
                    sys.exit()

                # Switching screens based on which button the user clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if amsterdam_back_button.over_button(pos) is True:
                        simulationThree = False
                        homeScreen = True
                        current_year = 1993

                # Highlighting the buttons to light blue if motion is detected over the buttons
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

            # Increment the scale based on number of years
            scale_factor = (water_height - int(scale_amsterdam_data[year_string]))

            # Display correct position of water
            display_surface.blit(real_ocean, (0, scale_factor))

            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)


if __name__ == '__main__':
    run_simulation()

    python_ta.check_all(config={
        'extra-imports': ['csv', 'Dict', 'List', 'pprint'],  # the names (strs) of imported modules
        'allowed-io': ['read_csv'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
