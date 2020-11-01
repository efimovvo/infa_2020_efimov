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


class Ball():
    def __init__(self, x=30, y=450):
        """ Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        g = 1 # Gravity acceleration

        self.x += self.vx
        self.y += self.vy + g / 2
        self.vy += g
        self.live -= 0.3
        
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
            print(self.vy)
            self.vy *= -0.7
            print(self.vy)

    def delete(self):
        canv.delete(self.id)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        distance = ((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5
        if distance <= (self.r + obj.r):
            hit = True
        else:
            hit = False
        return hit


class Gun():
    def __init__(self):
        """ Конструктор класса Gun

        Args:
        """
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
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
        """Прицеливание. Зависит от положения мыши."""
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
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target():
    def __init__(self):
        """ Конструктор класса Target

        Args:
        """
        self.x = 0
        self.y = 0
        self.r = 0
        self.points = 0
        self.live = 1
        self.vx = 0
        self.vy = 0
        self.id = canv.create_oval(0,0,0,0)
        self.id_points = canv.create_text(30,30,text = self.points,font = '28')
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        r = self.r = rnd(10, 50)
        x = self.x = rnd((screen_size[0] * 6)//8, screen_size[0] - (r * 3)//2)
        y = self.y = rnd((screen_size[1] * 1)//2, screen_size[1] - (r * 3)//2)

        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        self.live = 0
        canv.itemconfig(self.id_points, text=self.points)


target = Target()
screen = canv.create_text(400, 300, text='', font='28')
gun = Gun()
bullet = 0
balls = []


def new_game(event=''):
    global gun, target, screen, balls, bullet
    target.new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', gun.fire2_start)
    canv.bind('<ButtonRelease-1>', gun.fire2_end)
    canv.bind('<Motion>', gun.targetting)

    time_interval = 0.02
    target.live = 1
    while target.live or balls:
        for ball in balls:
            if ball.live <= 0:
                ball.delete()
                balls.remove(ball)
            else:
                ball.move()
                ball.set_coords()
                #print(target.live)
                if ball.hittest(target) and target.live:
                    print(target.live)
                    target.hit()
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