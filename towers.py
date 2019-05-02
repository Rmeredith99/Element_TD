import numpy as np 
import pygame
from math import ceil, atan2, pi, sin, cos

# Initializing tower graphics
tower_width = 64
buffer = 5

# Tower radius design
radius_img = pygame.image.load("game_art/tower_radius.png")

# Air towers
air_1 = pygame.image.load("game_art/air_tower_1.png")
air_1 = pygame.transform.scale(air_1, (tower_width, tower_width))
air_2 = pygame.image.load("game_art/air_tower_2.png")
air_2 = pygame.transform.scale(air_2, (tower_width, tower_width))
air_3 = pygame.image.load("game_art/air_tower_3.png")
air_3 = pygame.transform.scale(air_3, (tower_width, tower_width))

# Water towers
water_1 = pygame.image.load("game_art/water_tower_1.png")
water_1 = pygame.transform.scale(water_1, (tower_width, tower_width))
water_2 = pygame.image.load("game_art/water_tower_2.png")
water_2 = pygame.transform.scale(water_2, (tower_width, tower_width))
water_3 = pygame.image.load("game_art/water_tower_3.png")
water_3 = pygame.transform.scale(water_3, (tower_width, tower_width))

# Earth towers
earth_1 = pygame.image.load("game_art/earth_tower_1.png")
earth_1 = pygame.transform.scale(earth_1, (tower_width, tower_width))
earth_2 = pygame.image.load("game_art/earth_tower_2.png")
earth_2 = pygame.transform.scale(earth_2, (tower_width, tower_width))
earth_3 = pygame.image.load("game_art/earth_tower_3.png")
earth_3 = pygame.transform.scale(earth_3, (tower_width, tower_width))

# Fire towers
fire_1 = pygame.image.load("game_art/fire_tower_1.png")
fire_1 = pygame.transform.scale(fire_1, (tower_width, tower_width))
fire_2 = pygame.image.load("game_art/fire_tower_2.png")
fire_2 = pygame.transform.scale(fire_2, (tower_width, tower_width))
fire_3 = pygame.image.load("game_art/fire_tower_3.png")
fire_3 = pygame.transform.scale(fire_3, (tower_width, tower_width))

# Magic towers
magic_1 = pygame.image.load("game_art/magic_tower_1.png")
magic_1 = pygame.transform.scale(magic_1, (tower_width, tower_width))
magic_2 = pygame.image.load("game_art/magic_tower_2.png")
magic_2 = pygame.transform.scale(magic_2, (tower_width, tower_width))
magic_3 = pygame.image.load("game_art/magic_tower_3.png")
magic_3 = pygame.transform.scale(magic_3, (tower_width, tower_width))

# Spirit towers
spirit_1 = pygame.image.load("game_art/spirit_tower_1.png")
spirit_1 = pygame.transform.scale(spirit_1, (tower_width, tower_width))
spirit_2 = pygame.image.load("game_art/spirit_tower_2.png")
spirit_2 = pygame.transform.scale(spirit_2, (tower_width, tower_width))
spirit_3 = pygame.image.load("game_art/spirit_tower_3.png")
spirit_3 = pygame.transform.scale(spirit_3, (tower_width, tower_width))

############################################################
### Attack animations
air_2_1 = pygame.image.load("game_art/air_attack/2_1.png")
air_3_1 = pygame.image.load("game_art/air_attack/3_1.png")

water_2_1 = pygame.image.load("game_art/water_attack/2_1.png")
water_3_1 = pygame.image.load("game_art/water_attack/3_1.png")

earth_2_1 = pygame.image.load("game_art/earth_attack/2_1.png")
earth_3_1 = pygame.image.load("game_art/earth_attack/3_1.png")

fire_2_1 = pygame.image.load("game_art/fire_attack/2_1.png")
fire_2_2 = pygame.image.load("game_art/fire_attack/2_2.png")
fire_2_3 = pygame.image.load("game_art/fire_attack/2_3.png")
fire_2_4 = pygame.image.load("game_art/fire_attack/2_4.png")
fire_3_1 = pygame.image.load("game_art/fire_attack/3_1.png")
fire_3_2 = pygame.image.load("game_art/fire_attack/3_2.png")

magic_2_1 = pygame.image.load("game_art/magic_attack/2_1.png")
magic_3_1 = pygame.image.load("game_art/magic_attack/3_1.png")

spirit_2_1 = pygame.image.load("game_art/spirit_attack/2_1.png")
spirit_3_1 = pygame.image.load("game_art/spirit_attack/3_1.png")

def write_text(screen, text, x, y, color, size, font="Comic Sans Ms"):
    """
    [write_text] is an encapsulation of the text-writing process using
        the blit function on the given screen. Function parameters define
        the look of the text.
    """
    myfont = pygame.font.SysFont(font, size)
    textsurface = myfont.render(text, False, color)
    screen.blit(textsurface,(x, y))

def get_animation_center(angle_rad, h, w):
    """
    [get_animation_center] is the center of the actual image when it's
        tilted at an angle. This if for the purpose of aligning the
        image properly.
    """
    angle = angle_rad * 180 / pi
    if angle < 0:
        angle += 360.0

    # Calculating supplementary angles
    if angle > 90 and angle <= 180:
        angle_rad = pi - angle_rad
    elif angle > 180 and angle <= 270:
        angle_rad = pi + angle_rad
    elif angle > 270 and angle <= 360:
        angle_rad = -angle_rad
    else:
        angle_rad = angle_rad
 
    # Using supplementary angles, calculate center adjustment
    x_adjustment = int(w/2.0*cos(angle_rad) + h/2.0*sin(angle_rad))
    y_adjustment = int(w/2.0*sin(angle_rad) + h/2.0*cos(angle_rad))
    return x_adjustment, y_adjustment

class Tower:
    def __init__(self, x, y, level=1):
        self.x = x
        self.y = y
        self.range = 200
        self.damage = 50
        self.rate = 1
        self.targets = 1
        self.color = (0, 100, 255)
        self.half_width = 28
        self.cooldown = 0
        self.cost = self.get_cost()
        self.upgrade_cost = [50, 60]
        self.sell_back_rate = 0.8
        self.special_ability_text = "None"

        self.level = level
        self.max_level = 3
        self.tower_name = "Standard Tower"

    def draw(self, screen):
        """
        [draw] draws the tower on the provided screen.
        """
        pygame.draw.rect(screen, (100,100,100), 
        [int(self.x) - self.half_width, int(self.y) - self.half_width, self.half_width * 2, self.half_width * 2])
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.half_width * 2./3))

    def draw_circle(self, screen):
        """
        [draw_circle] draws a circle denoting the range of the tower.
            State will call this when a tower is selected
        """
        r = self.range
        circle = pygame.transform.scale(radius_img, (2*r, 2*r))
        screen.blit(circle, (self.x - r, self.y - r))
        
    def draw_info(self, screen, top_left_corner, purchased = False):
        """
        [draw_info] draws the info screen for this tower in the sidebar.
            Info varies depending on whether the tower has already been
            purchased. If not, no info about upgrades will be given and
            instead, info about the cost will be displayed.
        """
        corner_x, corner_y = top_left_corner
        width = int(corner_x / 7)

        h = 20
        spacing = 30
        w = 10
        size = 15
        if purchased:
            write_text(screen, str(self.tower_name), corner_x + w, corner_y + h, (0,0,0), size + 5)
            write_text(screen, "Damage: " + str(self.damage), corner_x + w, corner_y + h+spacing, (0,0,0), size)
            write_text(screen, "Range: " + str(self.range), corner_x + w, corner_y + h+2*spacing, (0,0,0), size)
            write_text(screen, "Attack Rate: " + str(self.rate), corner_x + w, corner_y + h+3*spacing, (0,0,0), size)
            write_text(screen, "Targets: " + str(self.targets), corner_x + w, corner_y + h+4*spacing, (0,0,0), size)
            write_text(screen, "Special: " + str(self.special_ability_text), corner_x + w, corner_y + h+5*spacing, (0,0,0), size)

            # Partition line
            pygame.draw.rect(screen, (0,0,0), [corner_x + 10, corner_y + h+6*spacing - 1, width - 20, 3])

            write_text(screen, "Level: " + str(self.level), corner_x + w, corner_y + h+7*spacing, (0,0,0), size)
            # TODO: Change upgrade cost to reflect actual cost of upgrade
            if self.level < self.max_level:
                write_text(screen, "Upgrade Cost: " + str(self.upgrade_cost[self.level - 1]), corner_x + w, corner_y + h+8*spacing, (0,0,0), size)
        else:
            write_text(screen, str(self.tower_name), corner_x + w, corner_y + h, (0,0,0), size + 5)
            write_text(screen, "Damage: " + str(self.damage), corner_x + w, corner_y + h+spacing, (0,0,0), size)
            write_text(screen, "Range: " + str(self.range), corner_x + w, corner_y + h+2*spacing, (0,0,0), size)
            write_text(screen, "Attack Rate: " + str(self.rate), corner_x + w, corner_y + h+3*spacing, (0,0,0), size)
            write_text(screen, "Targets: " + str(self.targets), corner_x + w, corner_y + h+4*spacing, (0,0,0), size)
            write_text(screen, "Special: " + str(self.special_ability_text), corner_x + w, corner_y + h+5*spacing, (0,0,0), size)

            # Partition line
            pygame.draw.rect(screen, (0,0,0), [corner_x + 10, corner_y + h+6*spacing - 1, width - 20, 3])

            write_text(screen, "Cost: " + str(self.cost), corner_x + w, corner_y + h+7*spacing, (0,0,0), size)

        # Upgrade button
        if purchased and self.level < self.max_level:
            w = 20
            h = 380   
            pygame.draw.rect(screen, (150,150,150), [corner_x + w, corner_y + h, width - 2*w, 70])
            pygame.draw.rect(screen, (0,200,0), [corner_x + w+5, corner_y + h+5, width - 2*(w+5), 60]) 
            write_text(screen, "Upgrade", corner_x + 50, corner_y + h+20, (255,255,255), 20)

        # Sell button
        if purchased:
            w = 20
            h = 300   
            pygame.draw.rect(screen, (150,150,150), [corner_x + w, corner_y + h, width - 2*w, 70])
            pygame.draw.rect(screen, (200,0,0), [corner_x + w+5, corner_y + h+5, width - 2*(w+5), 60]) 
            write_text(screen, "Sell", corner_x + 68, corner_y + h+20, (255,255,255), 20)

    def get_cost(self):
        """
        [get_cost] takes in a difficulty and returns a cost based on
            pre-calculated parameters including round data and tower
            details.
        """
        constant = 0.1
        speed = 145.0
        release = 0.67
        cost = constant * min(self.range, speed * release) / speed * self.damage * self.rate * min(self.targets, self.range / (speed * release) + 1)
        return ceil(cost)*10
        
    def sunk_cost(self):
        """
        [sunk_cost] returns the total amount of money that has been
            spent on this tower which includes initial cost and
            upgrades.
        """
        cost = self.cost
        if self.level > 1:
            cost += self.upgrade_cost[0]
        if self.level > 2:
            cost += self.upgrade_cost[1]
        return cost

    def update(self, time_delta):
        """
        [update] adds a given amount of time to the cooldown
            amount so that a tower can only attack at a given rate.
        """
        self.cooldown += time_delta

    def can_attack(self):
        """
        [can_attack] returns whether or not a tower has had enough
            cooldown time to attack again.
        """
        return self.cooldown >= (1.0 / self.rate)

    def attack(self):
        """
        [attack] is called when the tower is attacking an enemy.
            The actual attacking takes place in a method in State.
            This is just to reset self.cooldown.
        """
        self.cooldown = 0

    def get_attack_indices(self, distances, enemies):
        """
        [get_attack_indices] returns a list of enemy indices to attack.
            Replaces code in State so that different towers may attack
            a different number of enemies at once
        """
        if self.targets == 1:
            index = -1
            max_dist_traveled = -1
            for j, enemy in enumerate(enemies):
                if distances[j] <= self.range and enemy.dist_traveled > max_dist_traveled:
                    index = j
                    max_dist_traveled = enemy.dist_traveled

            if index != -1:
                return [index]
            else:
                return []

        elif self.targets < len(enemies):
            indices = []
            max_traveled = []
            for j, enemy in enumerate(enemies):
                if distances[j] <= self.range:
                    if len(max_traveled) == 0:
                        max_traveled.append((j, enemy.dist_traveled))
                    else:
                        # find where the current distance traveled places
                        dist = enemy.dist_traveled
                        for i in range(len(max_traveled)):
                            if dist > max_traveled[i][1]:
                                max_traveled.insert(i, (j, dist))
                                break
                            if i >= self.targets or i == len(max_traveled) - 1:
                                max_traveled.append((j, dist))
                                break

            for i in range(min(self.targets, len(max_traveled))):
                indices.append(max_traveled[i][0])

            return indices


        else: # If all enemies can be hit
            indices = []
            for j, enemy in enumerate(enemies):
                if distances[j] <= self.range:
                    indices.append(j)
            return indices

        


    def get_animation_sequence(self, kwargs=[]):
        """
        [get_animation_sequence] returns a list of functions that take in 
            a screen and x and y coordinates and draws an attack animation.
            Used in conjunction with the Animation class to display attacks.
            The return value should be thought of as a series of sprite 
            animations.
            The first two values in the tuple are start and end animation  
            sequences respectively. The third is the length of time for one
            loop of the animation to occur. The fourth is the total amount
            of time for the animation to run. This value should be set to 
            'None' when it's a bullet-like animation so that it only vanishes
            when it reaches the target
        """
        animation = [
            lambda screen, x, y : (pygame.draw.circle(screen, self.color, (int(x), int(y)), 10))
        ]
        end_animation = []
        return animation, end_animation, 0.3, None

    def upgrade(self):
        """
        [upgrade] increases the level of the tower and updates the data
            accordingly
        """
        if self.level < 3:
            self.level += 1

        self.adjust_for_level()

    def adjust_for_level(self):
        """
        [adjust_for_level] changes tower parameters according to the current
            tower level. To be implemented in the children classes.
        """
        raise NotImplementedError

    def get_effect(self):
        """
        [get_effect] returns start, middle, and end effects in a tuple which define
            how a tower's hit might change things in an enemy.
            Values are anonymous functions that take in an enemy and make 
            changes to them.
        """
        start = lambda x : None
        middle = lambda x, delta : None
        end = lambda x : None
        duration = 0
        return start, middle, end, duration
        

class Air_Tower(Tower):
    
    def __init__(self, x, y, level=1):
        Tower.__init__(self, x, y, level)
        self.adjust_for_level()
        self.color = (217, 229, 247)
        self.cost = 40
        self.upgrade_cost = [60, 150]
        self.drawings = [
            lambda x, y, screen : screen.blit(air_1, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(air_2, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(air_3, (x - tower_width // 2, y - tower_width // 2))
        ]
        self.type = "AIR"

    def adjust_for_level(self):
        if self.level == 1:
            self.range = 200
            self.damage = 50
            self.targets = 1
            self.rate = 1
            self.tower_name = "Air"
            
        elif self.level == 2:
            self.range = 250
            self.damage = 100
            self.targets = 1
            self.rate = 1.2
            self.tower_name = "Wind"
        else:
            self.range = 250
            self.damage = 100
            self.targets = 2
            self.rate = 2
            self.tower_name = "Storm"

    def draw(self, screen):
        self.drawings[self.level - 1](self.x, self.y, screen)

    def get_animation_sequence(self, kwargs=[]):
        if self.level > 1:
            if self.level == 2:
                image = air_2_1
            else:
                image = air_3_1
            h = 65
            w = 65
            animations = []
            frames = 8
            for i in range(frames):
                angle = i * 360.0 / frames
                if angle <= 180:
                    angle_rad = angle * pi / 180.0
                else:
                    angle_rad = angle * pi / 180.0 - 2 * pi
                x_adj, y_adj = get_animation_center(angle_rad, h, w)
                sprite = pygame.transform.scale(image, (w, h))
                sprite = pygame.transform.rotate(sprite, angle)
                animations.append(lambda screen, x, y, sprite=sprite, 
                x_adj=x_adj, y_adj=y_adj : screen.blit(sprite, (x - x_adj, y - y_adj)))
            
            return animations, [], 0.2, None

        else:
            return Tower.get_animation_sequence(self)

class Water_Tower(Tower):
    
    def __init__(self, x, y, level=1):
        Tower.__init__(self, x, y, level)
        self.adjust_for_level()
        self.color = (9, 85, 198)
        self.cost = 60
        self.upgrade_cost = [100, 160]
        self.drawings = [
            lambda x, y, screen : screen.blit(water_1, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(water_2, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(water_3, (x - tower_width // 2, y - tower_width // 2))
        ]
        self.type = "WATER"

    def adjust_for_level(self):
        if self.level == 1:
            self.range = 150
            self.damage = 60
            self.targets = 1
            self.rate = 1
            self.tower_name = "Water"
            
        elif self.level == 2:
            self.range = 200
            self.damage = 75
            self.targets = 1
            self.rate = 1.5
            self.tower_name = "Ice"
            self.special_ability_text = "Slows by 50%"
        else:
            self.range = 250
            self.damage = 125
            self.targets = 2
            self.rate = 1.5
            self.tower_name = "Glacier"
            self.special_ability_text = "Slows by 80%"

    def draw(self, screen):
        self.drawings[self.level - 1](self.x, self.y, screen)

    def get_animation_sequence(self, kwargs=[]):
        if self.level == 2:
            h = 110
            w = 110
            sprite = pygame.transform.scale(water_2_1, (w, h))
            animations = [lambda screen, x, y : screen.blit(sprite, (x - w // 2, y - h // 2))]
            return animations, [], 0.3, None
        if self.level == 3:
            h = 90
            w = 90
            start_x = kwargs[0]
            start_y = kwargs[1]
            end_x = kwargs[2]
            end_y = kwargs[3]

            angle_rad = atan2(-(end_y - start_y), end_x - start_x)
            angle = angle_rad * 180 / pi
            sprite = pygame.transform.scale(water_3_1, (w, h))
            sprite = pygame.transform.rotate(sprite, angle)
            x_adj, y_adj = get_animation_center(angle_rad, h, w)
            animation = [lambda screen, x, y : screen.blit(sprite, (x - x_adj, y - y_adj))]
            return animation, [], 0.3, None
        else:
            return Tower.get_animation_sequence(self)

    def get_effect(self):
        if self.level == 1:
            start = lambda x : None
            middle = lambda x, delta : None
            end = lambda x : None
            duration = 0
            return start, middle, end, duration

        elif self.level == 2:
            def start(enemy):
                enemy.speed *= 0.5
            middle = lambda x, delta : None
            def end(enemy):
                enemy.speed /= 0.5
            duration = 2.0
            return start, middle, end, duration

        else:
            def start(enemy):
                enemy.speed *= 0.2
            middle = lambda x, delta : None
            def end(enemy):
                enemy.speed /= 0.2
            duration = 3.0
            return start, middle, end, duration

class Earth_Tower(Tower):
    
    def __init__(self, x, y, level=1):
        Tower.__init__(self, x, y, level)
        self.adjust_for_level()
        self.color = (19, 160, 45)
        self.cost = 80
        self.upgrade_cost = [200, 500]
        self.drawings = [
            lambda x, y, screen : screen.blit(earth_1, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(earth_2, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(earth_3, (x - tower_width // 2, y - tower_width // 2))
        ]
        self.type = "EARTH"

    def adjust_for_level(self):
        if self.level == 1:
            self.range = 100
            self.damage = 100
            self.targets = 1
            self.rate = 1
            self.tower_name = "Earth" 
            
        elif self.level == 2:
            self.range = 150
            self.damage = 150
            self.targets = 2
            self.rate = 1.4
            self.tower_name = "Boulder"
        else:
            self.range = 200
            self.damage = 200
            self.targets = 3
            self.rate = 1.8
            self.tower_name = "Mountain"

    def get_animation_sequence(self, kwargs=[]):
        if self.level == 2:
            h = 90
            w = 90
            sprite = pygame.transform.scale(earth_2_1, (w, h))
            animations = [lambda screen, x, y : screen.blit(sprite, (x - w // 2, y - h // 2))]
            return animations, [], 0.3, None
        if self.level == 3:
            h = 100
            w = 100
            start_x = kwargs[0]
            start_y = kwargs[1]
            end_x = kwargs[2]
            end_y = kwargs[3]

            angle_rad = atan2(-(end_y - start_y), end_x - start_x)
            angle = angle_rad * 180 / pi
            sprite = pygame.transform.scale(earth_3_1, (w, h))
            sprite = pygame.transform.rotate(sprite, angle)
            x_adj, y_adj = get_animation_center(angle_rad, h, w)
            animation = [lambda screen, x, y : screen.blit(sprite, (x - x_adj, y - y_adj))]
            return animation, [], 0.3, None
        else:
            return Tower.get_animation_sequence(self)

    def draw(self, screen):
        self.drawings[self.level - 1](self.x, self.y, screen)

class Fire_Tower(Tower):
    
    def __init__(self, x, y, level=1):
        Tower.__init__(self, x, y, level)
        self.adjust_for_level()
        self.color = (196, 14, 1)
        self.cost = 100
        self.upgrade_cost = [200, 400]
        self.drawings = [
            lambda x, y, screen : screen.blit(fire_1, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(fire_2, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(fire_3, (x - tower_width // 2, y - tower_width // 2))
        ]
        self.type = "FIRE"

    def adjust_for_level(self):
        if self.level == 1:
            self.range = 200
            self.damage = 50
            self.targets = 1
            self.rate = 3
            self.tower_name = "Fire"
            
        elif self.level == 2:
            self.range = 200
            self.damage = 150
            self.targets = 1
            self.rate = 3
            self.tower_name = "Lightning"
        else:
            self.range = 200
            self.damage = 200
            self.targets = 2
            self.rate = 3
            self.tower_name = "Combustion"

    def draw(self, screen):
        self.drawings[self.level - 1](self.x, self.y, screen)

    def get_animation_sequence(self, kwargs=[]):
        if self.level == 2:
            start_x = kwargs[0]
            start_y = kwargs[1]
            end_x = kwargs[2]
            end_y = kwargs[3]

            dist = int(((start_x - end_x)**2 + (start_y - end_y)**2)**0.5)
            angle_rad = atan2(-(end_y - start_y), end_x - start_x)
            angle = angle_rad * 180 / pi

            w = dist
            h = 400

            x_adjustment, y_adjustment = get_animation_center(angle_rad, h, w)

            half_x = (start_x + end_x) // 2
            half_y = (start_y + end_y) // 2
            animations = []

            a = pygame.transform.scale(fire_2_1, (w, h))
            a = pygame.transform.rotate(a, angle)
            animations.append((lambda screen, x, y : screen.blit(a, (half_x - x_adjustment , half_y - y_adjustment))))
            b = pygame.transform.scale(fire_2_2, (w, h))
            b = pygame.transform.rotate(b, angle)
            animations.append((lambda screen, x, y : screen.blit(b, (half_x - x_adjustment , half_y - y_adjustment))))
            c = pygame.transform.scale(fire_2_3, (w, h))
            c = pygame.transform.rotate(c, angle)
            animations.append((lambda screen, x, y : screen.blit(c, (half_x - x_adjustment , half_y - y_adjustment))))
            d = pygame.transform.scale(fire_2_4, (w, h))
            d = pygame.transform.rotate(d, angle)
            animations.append((lambda screen, x, y : screen.blit(d, (half_x - x_adjustment , half_y - y_adjustment))))
            return animations, [], 0.15, 0.3

        if self.level == 3:
            # Start animation
            h = 80
            w = 80
            start_x = kwargs[0]
            start_y = kwargs[1]
            end_x = kwargs[2]
            end_y = kwargs[3]

            angle_rad = atan2(-(end_y - start_y), end_x - start_x)
            angle = angle_rad * 180 / pi
            sprite = pygame.transform.scale(fire_3_1, (w, h))
            sprite = pygame.transform.rotate(sprite, angle)
            x_adj, y_adj = get_animation_center(angle_rad, h, w)
            start_animation = [lambda screen, x, y, sprite=sprite : screen.blit(sprite, (x - x_adj, y - y_adj))]

            # End animation
            end_x = kwargs[2]
            end_y = kwargs[3]
            end_animation = []
            frames = 8
            for i in range(8):
                scale = int((i+1) * 200 / frames)
                sprite = pygame.transform.scale(fire_3_2, (scale, scale))
                end_animation.append(lambda screen, x, y, scale=scale, sprite=sprite : screen.blit(sprite, (end_x - scale // 2, end_y - scale // 2)))
            
            return start_animation, end_animation, 0.15, None

        else:
            return Tower.get_animation_sequence(self)

class Magic_Tower(Tower):
    
    def __init__(self, x, y, level=1):
        Tower.__init__(self, x, y, level)
        self.adjust_for_level()
        self.color = (114, 5, 173)
        self.cost = 300
        self.upgrade_cost = [500, 1000]
        self.drawings = [
            lambda x, y, screen : screen.blit(magic_1, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(magic_2, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(magic_3, (x - tower_width // 2, y - tower_width // 2))
        ]
        self.type = "MAGIC"

    def adjust_for_level(self):
        if self.level == 1:
            self.range = 150
            self.damage = 200
            self.targets = 1
            self.rate = 2
            self.tower_name = "Magic"
            
        elif self.level == 2:
            self.range = 175
            self.damage = 250
            self.targets = 2
            self.rate = 2.4
            self.tower_name = "Wizard"
        else:
            self.range = 200
            self.damage = 300
            self.targets = 3
            self.rate = 2.8
            self.tower_name = "Mystic"

    def draw(self, screen):
        self.drawings[self.level - 1](self.x, self.y, screen)

    def get_animation_sequence(self, kwargs=[]):
        if self.level >= 2:
            if self.level == 2:
                img = magic_2_1
            else:
                img = magic_3_1
            h = 90
            w = 90
            sprite = pygame.transform.scale(img, (w, h))
            animations = [lambda screen, x, y : screen.blit(sprite, (x - w // 2, y - h // 2))]
            return animations, [], 0.3, None
        else:
            return Tower.get_animation_sequence(self)

class Spirit_Tower(Tower):
    
    def __init__(self, x, y, level=1):
        Tower.__init__(self, x, y, level)
        self.adjust_for_level()
        self.color = (120, 120, 120)
        self.cost = 1000
        self.upgrade_cost = [2000, 3000]
        self.drawings = [
            lambda x, y, screen : screen.blit(spirit_1, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(spirit_2, (x - tower_width // 2, y - tower_width // 2)),
            lambda x, y, screen : screen.blit(spirit_3, (x - tower_width // 2, y - tower_width // 2))
        ]
        self.type = "SPIRIT"

    def adjust_for_level(self):
        if self.level == 1:
            self.range = 100
            self.damage = 500
            self.targets = 2
            self.rate = 1.5
            self.tower_name = "Spirit"
            
        elif self.level == 2:
            self.range = 200
            self.damage = 750
            self.targets = 3
            self.rate = 1.8
            self.tower_name = "Death"
        else:
            self.range = 300
            self.damage = 1000
            self.targets = 4
            self.rate = 2.1
            self.tower_name = "Deity"

    def draw(self, screen):
        self.drawings[self.level - 1](self.x, self.y, screen)

    def get_animation_sequence(self, kwargs=[]):
        if self.level == 2:
            h = 70
            w = 70
            sprite = pygame.transform.scale(spirit_2_1, (w, h))
            animations = [lambda screen, x, y : screen.blit(sprite, (x - w // 2, y - h // 2))]
            return animations, [], 0.3, None
        if self.level == 3:
            h = 60
            w = 60
            start_x = kwargs[0]
            start_y = kwargs[1]
            end_x = kwargs[2]
            end_y = kwargs[3]

            angle_rad = atan2(-(end_y - start_y), end_x - start_x)
            angle = angle_rad * 180 / pi
            sprite = pygame.transform.scale(spirit_3_1, (w, h))
            sprite = pygame.transform.rotate(sprite, angle)
            x_adj, y_adj = get_animation_center(angle_rad, h, w)
            animation = [lambda screen, x, y : screen.blit(sprite, (x - x_adj, y - y_adj))]
            return animation, [], 0.3, None
        else:
            return Tower.get_animation_sequence(self)
