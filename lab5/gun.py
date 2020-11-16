from random import randrange as rnd, choice
import tkinter as tk
import math
import time

screen_size = (800, 600)

root = tk.Tk()
root.title('Gun game')
fr = tk.Frame(root)
root.geometry(str(screen_size[0]) + 'x' + str(screen_size[1]))
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

class Game_Object():
    def __init__(self, x=30, y=450, r=10, live=30, color='black'):
        """Game_Object class constructor 

        Args:
            x - initial object position in horizontal direction
            y - initial object position in vertical direction
            r - initial radius of object
            live - initial number of lives
            color - object color
        """
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.color = color
        self.live = live
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )

    def set_coords(self):
        """Redraw the object on the canvas after unit time interval.

        Args:
        """
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self, g=1, life_decresion=0.3):
        """Move the object on the canvas after unit time interval.
        
        This method describes object movement for unit time interval.
        It recalculates self.x and self.y according to velocities
            self.vx and self.vy and gravity acceleration g.
        Also it takes into account the walls along the screen borders.

        Args:
            g - gravity acceleration
        """

        self.live -= life_decresion
        self.x += self.vx
        self.y += self.vy + g / 2
        self.vy += g        
    
        if self.x + self.r > screen_size[0]:
            self.x = 2 * (screen_size[0] - self.r) - self.x
            self.vx *= -0.7
            self.vy *= 0.7
        if self.x - self.r < 0:
            self.x = 2 * self.r - self.x
            self.vx *= -0.7
            self.vy *= 0.7

        if self.y + self.r > screen_size[1]:
            self.vy -= g * (screen_size[1] - self.r - self.y) / (self.vy + g / 2)
            self.y = 2 * (screen_size[1] - self.r) - self.y
            self.vx *= 0.7
            self.vy *= -0.7
        if self.y - self.r < 0:
            self.y = 2*self.r - self.y
            self.vx *= 0.7
            self.vy *= -0.7


class Ball(Game_Object):
    def __init__(self, x=30, y=450):
        """Ball class constructor 

        Args:
            x - initial object position in horizontal direction
            y - initial object position in vertical direction
        """
        super().__init__(color=choice(['blue', 'green', 'red', 'brown']))

    def delete(self):
        """Delete the object form the canvas.

        Args:
        """
        canv.delete(self.id)

    def hittest(self, obj):
        """This function check did the ball hit the target.

        Args:
            obj: Target object which is checking hitting with.
        Returns:
            True/False - in case the hit happened/not happened.
        """

        distance = ((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5
        if distance <= (self.r + obj.r) and obj.live:
            hit = True
            obj.points += 1
        else:
            hit = False
        return hit


class Gun():
    def __init__(self):
        """Gun class constructor.

        Args:
        """
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.id = canv.create_line(20,450,50,420,width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Function is shooting by the ball.

        The shooting is happening after mouse button went up.
        Starting velocity components vx and vy depends on mouse position.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.angle = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Targetting depends on mouse position."""
        if event:
            self.angle = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.angle),
                    450 + max(self.f2_power, 20) * math.sin(self.angle)
                    )

    def power_up(self):
        """Increasing the power of current shoot if the mouse button pushed."""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target(Game_Object):
    def __init__(self, color='red'):
        """Target class constructor

        Args:
        """
        super().__init__(x=0, y=0, r=0, live=1, color=color)
        self.points = 0
        if color == 'red':
            self.id_points = canv.create_text(
                30, 30,
                text = 'Red: '+str(self.points),
                font = '28'
            )
        else:
            self.id_points = canv.create_text(
                30, 50,
                text = 'Green: '+str(self.points),
                font = '28'
            )
        self.new_target(color)

    def new_target(self, color='red'):
        """Function creates new target."""
        r = self.r = rnd(10, 50)
        x = self.x = rnd((screen_size[0] * 6)//8, screen_size[0] - (r * 3)//2)
        y = self.y = rnd((screen_size[1] * 1)//2, screen_size[1] - (r * 3)//2)

        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self):
        """Target beating."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.live = 0
        if self.color == 'red':
            canv.itemconfig(self.id_points,
                text = 'Red: '+str(self.points),
            )
        else:
            canv.itemconfig(self.id_points,
                text = 'Green: '+str(self.points),
            )


targets = [Target(), Target(color='green')]
screen = canv.create_text(400, 300, text='', font='28')
gun = Gun()
bullet = 0
balls = []


def new_game(event=''):
    global gun, target, screen, balls, bullet
    targets[0].new_target()
    targets[1].new_target(color='green')
    bullet = 0
    balls = []
    canv.bind('<Button-1>', gun.fire2_start)
    canv.bind('<ButtonRelease-1>', gun.fire2_end)
    canv.bind('<Motion>', gun.targetting)

    time_interval = 0.02
    for target in targets:
        target.live = 1
    while targets[0].live and targets[1].live or balls:
        for target in targets:
            target.move(g=0, life_decresion=0)
            target.set_coords()
        for ball in balls:
            if ball.live <= 0:
                ball.delete()
                balls.remove(ball)
            else:
                ball.move()
                ball.set_coords()
                if ball.hittest(targets[0]) or ball.hittest(targets[1]):
                    targets[0].hit()
                    targets[1].hit()
                    canv.bind('<Button-1>', '')
                    canv.bind('<ButtonRelease-1>', '')
                    message = 'Вы уничтожили цель за ' + str(bullet)
                    if 10 <= bullet <= 20 or 5 <= bullet % 10 <= 9 or bullet % 10 == 0:
                        message += ' выстрелов'
                    elif bullet % 10 == 1:
                        message += ' выстрел'
                    else:
                        message += ' выстрела'
                    canv.itemconfig(screen, text=message)
        canv.update()
        time.sleep(time_interval)
        gun.targetting()
        gun.power_up()
    canv.itemconfig(screen, text='')
    canv.delete(gun)
    root.after(750, new_game)


new_game()

root.mainloop()