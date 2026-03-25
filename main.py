import turtle
import math
import random
import time
import colorsys
import json
import os

WIN_W:  int = 900
WIN_H:  int = 750
SAVE_FILE: str = os.path.join(os.path.dirname(__file__), "spirograph_saves.json")

PATTERNS: dict = {
    "1":  {"name": "🦋 Butterfly",       "key": "butterfly"},
    "2":  {"name": "🌸 Flower",           "key": "flower"},
    "3":  {"name": "🌌 Galaxy Spiral",    "key": "galaxy"},
    "4":  {"name": "🌀 Hypnotic Vortex",  "key": "vortex"},
    "5":  {"name": "🌹 Rose Curve",       "key": "rose"},
    "6":  {"name": "⭐ Star Burst",        "key": "starburst"},
    "7":  {"name": "🌊 Ocean Waves",      "key": "ocean"},
    "8":  {"name": "❄️  Snowflake",        "key": "snowflake"},
    "9":  {"name": "🕷️  Spider Web",       "key": "spiderweb"},
    "10": {"name": "💎 Crystal Gem",       "key": "crystal"},
    "11": {"name": "🔮 Magic Portal",      "key": "portal"},
    "12": {"name": "🎠 Carousel",          "key": "carousel"},
    "13": {"name": "🌈 Rainbow Storm",     "key": "rainbow"},
    "14": {"name": "🐚 Nautilus Shell",    "key": "nautilus"},
    "15": {"name": "🎆 Fireworks",         "key": "fireworks"},
}

BG_COLORS: dict = {
    "butterfly":  "#0A0A1A",
    "flower":     "#0D0A05",
    "galaxy":     "#000008",
    "vortex":     "#050005",
    "rose":       "#0A0005",
    "starburst":  "#000A0A",
    "ocean":      "#000A12",
    "snowflake":  "#030310",
    "spiderweb":  "#050505",
    "crystal":    "#030010",
    "portal":     "#000A05",
    "carousel":   "#0A0508",
    "rainbow":    "#030303",
    "nautilus":   "#050A08",
    "fireworks":  "#000000",
}


def save_last_pattern(pattern_key: str) -> None:
    with open(SAVE_FILE, "w") as f:
        json.dump({"last_pattern": pattern_key,
                   "timestamp": time.strftime("%Y-%m-%d %H:%M")}, f, indent=2)


def load_last_pattern() -> str:
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_pattern", "")
    return ""


def setup_screen(bg: str = "#000000") -> turtle.Screen:
    screen = turtle.Screen()
    screen.title("🎨  Turtle Spirograph Generator")
    screen.setup(width=WIN_W, height=WIN_H)
    screen.bgcolor(bg)
    screen.tracer(0)
    return screen


def make_pen(color: str = "white", speed: int = 0,
             width: int = 1) -> turtle.Turtle:
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.color(color)
    pen.pensize(width)
    pen.speed(0)  
    return pen


def make_writer() -> turtle.Turtle:
    w = turtle.Turtle()
    w.hideturtle()
    w.penup()
    w.speed(0)
    return w


hsv_to_rgb = lambda h, s, v: colorsys.hsv_to_rgb(h, s, v)

cycle_hue = lambda step, total, offset=0.0: ((step / total) + offset) % 1.0

hue_list = lambda n, offset=0.0: [((i / n) + offset) % 1.0 for i in range(n)]

def hue_color(hue: float, sat: float = 1.0, val: float = 1.0) -> tuple:
    return colorsys.hsv_to_rgb(hue, sat, val)

def gradient_colors(n: int, start_hue: float = 0.0,
                    end_hue: float = 1.0) -> list:
    return [
        colorsys.hsv_to_rgb(start_hue + (end_hue - start_hue) * i / n, 0.9, 1.0)
        for i in range(n)
    ]


def show_menu(screen: turtle.Screen) -> str:

    menu_pen = make_writer()
    menu_pen.color("#FF69B4")
    menu_pen.goto(0, WIN_H // 2 - 55)
    menu_pen.write("🎨  SPIROGRAPH GENERATOR", align="center",
                   font=("Courier", 22, "bold"))

    menu_pen.color("#CCCCCC")
    menu_pen.goto(0, WIN_H // 2 - 90)
    menu_pen.write("Choose a pattern to draw:", align="center",
                   font=("Courier", 12, "normal"))

    keys   = list(PATTERNS.keys())
    half   = len(keys) // 2 + len(keys) % 2
    col_x  = [-220, 110]
    start_y = WIN_H // 2 - 125

    for col in range(2):
        for row in range(half):
            idx = col * half + row
            if idx >= len(keys):
                break
            k   = keys[idx]
            pat = PATTERNS[k]
            hue = (idx / len(keys))
            r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
            menu_pen.color(r, g, b)
            menu_pen.goto(col_x[col], start_y - row * 28)
            menu_pen.write(f"{k:>2}. {pat['name']}",
                           align="left", font=("Courier", 11, "bold"))

    # Last pattern hint
    last = load_last_pattern()
    if last:
        last_name = next((p["name"] for p in PATTERNS.values()
                          if p["key"] == last), "")
        menu_pen.color("#888888")
        menu_pen.goto(0, -WIN_H // 2 + 55)
        menu_pen.write(f"Last drawn: {last_name}",
                       align="center", font=("Courier", 10, "normal"))

    menu_pen.color("#FF69B4")
    menu_pen.goto(0, -WIN_H // 2 + 30)
    menu_pen.write("Enter a number (1–15) or 0 for RANDOM",
                   align="center", font=("Courier", 11, "normal"))

    screen.update()

    valid = set(PATTERNS.keys()) | {"0"}
    while True:
        ans = screen.textinput("Pattern Select",
                               "Enter pattern number (1-15) or 0 for random:")
        if ans is None:
            ans = "0"
        ans = ans.strip()
        if ans in valid:
            if ans == "0":
                ans = random.choice(list(PATTERNS.keys()))
            menu_pen.clear()
            return PATTERNS[ans]["key"]

def draw_label(pen: turtle.Turtle, name: str) -> None:
    pen.color("#FF69B4")
    pen.goto(0, -WIN_H // 2 + 18)
    pen.write(f"  {name}  ", align="center",
              font=("Courier", 13, "bold"))
    pen.goto(0, -WIN_H // 2 + 8)
    pen.color("#444444")
    pen.write("Press ENTER for menu  |  R for random  |  ESC to quit",
              align="center", font=("Courier", 9, "normal"))


def draw_butterfly(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    pen.penup()
    layers = 3
    offsets: list = [i / layers for i in range(layers)]

    for offset in offsets:
        pen.pensize(1)
        steps = 800
        first = True
        for i in range(steps + 1):
            theta = 2 * math.pi * i / steps * 10
            r = (math.e ** (math.sin(theta))
                 - 2 * math.cos(4 * theta)
                 + math.sin((2 * theta - math.pi) / 24) ** 5)
            scale = 90
            x = scale * r * math.cos(theta)
            y = scale * r * math.sin(theta)

            hue = cycle_hue(i, steps, offset)
            pen.color(hue_color(hue, 0.85, 1.0))

            if first:
                pen.goto(x, y); pen.pendown(); first = False
            else:
                pen.goto(x, y)

        pen.penup()
        if i % 99999 == 0:
            screen.update()

    screen.update()


def draw_flower(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    petals_list: list = [6, 8, 12, 5, 9]   # list of petal counts
    colors_list: list = gradient_colors(len(petals_list), 0.0, 0.85)

    for layer, (petals, col) in enumerate(zip(petals_list, colors_list)):
        R  = 80 + layer * 25
        r  = R / petals
        d  = r * 0.9
        steps = 600
        first = True
        pen.pensize(1)

        for i in range(steps + 1):
            t   = 2 * math.pi * i / steps * petals
            x   = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
            y   = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
            hue = cycle_hue(i, steps, layer / len(petals_list))
            pen.color(hue_color(hue, 0.9, 1.0))

            if first:
                pen.goto(x, y); pen.pendown(); first = False
            else:
                pen.goto(x, y)

            if i % 99999 == 0:
                screen.update()

        pen.penup()

    pen.goto(0, 0); pen.pendown()
    for i in range(361):
        angle = math.radians(i)
        pen.color(hue_color(i / 360, 1.0, 1.0))
        pen.goto(22 * math.cos(angle), 22 * math.sin(angle))
    pen.penup()
    screen.update()


def draw_galaxy(pen: turtle.Turtle, screen: turtle.Screen) -> None:
    star_positions: set = set()
    pen.pensize(1)
    for _ in range(80):
        sx = random.randint(-WIN_W // 2 + 20, WIN_W // 2 - 20)
        sy = random.randint(-WIN_H // 2 + 20, WIN_H // 2 - 20)
        pos = (sx // 5 * 5, sy // 5 * 5)
        if pos not in star_positions:
            star_positions.add(pos)
            brightness = random.uniform(0.4, 1.0)
            pen.color(brightness, brightness, brightness)
            pen.goto(sx, sy)
            pen.dot(random.choice([1, 1, 1, 2]))

    arms = 3
    for arm in range(arms):
        arm_offset = (2 * math.pi / arms) * arm
        steps = 500
        pen.penup()

        for i in range(steps):
            t     = i / steps * 4 * math.pi
            r     = 4 * t + 5
            x     = r * math.cos(t + arm_offset)
            y     = r * 0.55 * math.sin(t + arm_offset)

            angle = math.radians(15)
            rx    = x * math.cos(angle) - y * math.sin(angle)
            ry    = x * math.sin(angle) + y * math.cos(angle)

            hue = 0.65 + (i / steps) * 0.35   # blue → pink
            pen.color(hue_color(hue, 0.8, 1.0))
            pen.pensize(max(1, 3 - int(i / steps * 2.5)))

            if i == 0:
                pen.goto(rx, ry); pen.pendown()
            else:
                pen.goto(rx, ry)

            if i % 99999 == 0:
                screen.update()

        pen.penup()

    for radius in range(18, 0, -1):
        hue = 0.75 + radius / 60
        pen.color(hue_color(hue % 1.0, 0.6, 1.0))
        pen.goto(0, -radius // 2)
        pen.pendown()
        pen.circle(radius)
        pen.penup()
    screen.update()


def draw_vortex(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    sides   = 4
    count   = 120
    size    = 320
    angle   = 89.5
    pen.pensize(1)

    for i in range(count):
        hue = cycle_hue(i, count)
        pen.color(hue_color(hue, 1.0, 1.0))
        pen.pendown()
        for _ in range(sides):
            pen.forward(size)
            pen.right(360 / sides)
        pen.right(angle - 360 / sides)
        size  -= 1.7
        if size <= 0:
            break
        if i % 99999 == 0:
            screen.update()

    screen.update()


def draw_rose(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    configs: tuple = (
        (3,   0.00),
        (5,   0.15),
        (7,   0.30),
        (4,   0.55),
        (6,   0.70),
        (8,   0.85),
    )

    for k, hue_start in configs:
        steps  = 500
        scale  = 160
        pen.pensize(1)
        first  = True

        for i in range(steps + 1):
            theta = 2 * math.pi * i / steps * k
            r     = scale * math.cos(k * theta / k)
            x     = r * math.cos(theta)
            y     = r * math.sin(theta)
            hue   = cycle_hue(i, steps, hue_start)
            pen.color(hue_color(hue, 0.95, 1.0))

            if first:
                pen.goto(x, y); pen.pendown(); first = False
            else:
                pen.goto(x, y)

        pen.penup()
        screen.update()


def draw_starburst(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    sizes: list = [s for s in range(30, 290, 22)]
    neon_hues: list = hue_list(len(sizes), 0.05)

    pen.goto(0, 0)
    for idx, (size, hue) in enumerate(zip(sizes, neon_hues)):
        points = 5 + idx          
        angle  = 360 / points
        skip   = (points // 2) + 1 if points % 2 == 0 else points // 2

        pen.color(hue_color(hue, 0.95, 1.0))
        pen.pensize(max(1, 2 - idx // 5))
        pen.goto(size, 0)
        pen.pendown()

        for _ in range(points * 2 + 1):
            pen.goto(0, 0)
            pen.goto(size * math.cos(math.radians(_ * angle * skip)),
                     size * math.sin(math.radians(_ * angle * skip)))

        pen.penup()
        pen.setheading(pen.heading() + 7)
        if idx % 99999 == 0:
            screen.update()

    screen.update()


def draw_ocean(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    configs: list = [
        (3, 2, 0.00, 0.55),
        (5, 4, 0.30, 0.60),
        (7, 6, 0.60, 0.50),
        (4, 3, 0.10, 0.65),
        (6, 5, 0.50, 0.45),
        (2, 1, 0.80, 0.58),
        (8, 7, 0.20, 0.52),
    ]

    for fx, fy, phase, base_hue in configs:
        steps = 500
        A, B  = 200, 170
        pen.pensize(1)
        first = True

        for i in range(steps + 1):
            t   = 2 * math.pi * i / steps
            x   = A * math.sin(fx * t + phase * math.pi)
            y   = B * math.sin(fy * t)
            hue = cycle_hue(i, steps, base_hue)
            pen.color(hue_color(hue, 0.9, 1.0))

            if first:
                pen.goto(x, y); pen.pendown(); first = False
            else:
                pen.goto(x, y)

        pen.penup()
        screen.update()


def draw_snowflake(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    def branch(length: float, depth: int, hue: float) -> None:
        if depth == 0 or length < 3:
            pen.color(hue_color(hue, 0.4, 1.0))
            pen.pendown()
            pen.forward(length)
            pen.backward(length)
            pen.penup()
            return
        pen.pendown()
        pen.forward(length * 0.35)
        pen.penup()
        for side_angle in [60, -60]:
            pen.right(side_angle)
            branch(length * 0.45, depth - 1, (hue + 0.04) % 1.0)
            pen.left(side_angle)
        pen.pendown()
        pen.forward(length * 0.30)
        pen.penup()
        for side_angle in [60, -60]:
            pen.right(side_angle)
            branch(length * 0.35, depth - 1, (hue + 0.04) % 1.0)
            pen.left(side_angle)
        pen.pendown()
        pen.forward(length * 0.35)
        pen.backward(length)
        pen.penup()

    scales: list  = [220, 160, 100, 60]  
    centers: list = [(0, 0), (-180, 120), (180, 120), (0, -160)]

    for scale, (cx, cy) in zip(scales, centers):
        for arm in range(6):
            pen.goto(cx, cy)
            pen.setheading(arm * 60)
            hue = (arm / 6 + scale / 1000) % 1.0
            pen.pensize(max(1, scale // 80))
            branch(scale, 3, 0.58 + hue * 0.1)

        screen.update()


def draw_spiderweb(pen: turtle.Turtle, screen: turtle.Screen) -> None:
    spokes    = 12
    rings     = 20
    max_r     = 280
    pen.pensize(1)

    for s in range(spokes):
        angle = math.radians(s * 360 / spokes)
        pen.color(hue_color(0.33, 0.7, 0.5))
        pen.goto(0, 0)
        pen.pendown()
        pen.goto(max_r * math.cos(angle), max_r * math.sin(angle))
        pen.penup()

    for ring in range(1, rings + 1):
        r   = ring * max_r / rings
        hue = 0.28 + (ring / rings) * 0.1
        sat = 0.8
        val = 0.3 + (ring / rings) * 0.7
        pen.color(hue_color(hue, sat, val))
        pen.pensize(1)
        first = True

        for s in range(spokes + 1):
            angle = math.radians(s * 360 / spokes)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            if first:
                pen.goto(x, y); pen.pendown(); first = False
            else:
                pen.goto(x, y)

        pen.penup()
        if ring % 99999 == 0:
            screen.update()

    for _ in range(40):
        s     = random.randint(0, spokes - 1)
        frac  = random.uniform(0.1, 0.95)
        angle = math.radians(s * 360 / spokes)
        r     = frac * max_r
        pen.goto(r * math.cos(angle), r * math.sin(angle))
        pen.color(0.7, 1.0, 0.9)
        pen.dot(random.choice([3, 4, 5]))

    screen.update()


def draw_crystal(pen: turtle.Turtle, screen: turtle.Screen) -> None:
    gem_configs: tuple = (
        (6,  250, 5,  0.70),
        (8,  220, 4,  0.75),
        (12, 190, 3,  0.80),
        (16, 160, 2,  0.65),
        (24, 130, 1,  0.60),
        (5,  100, 7,  0.85),
    )

    for points, scale, rot_step, hue_start in gem_configs:
        layers = max(6, 18 // rot_step)
        for layer in range(layers):
            angle_offset = layer * rot_step
            hue = (hue_start + layer / layers * 0.15) % 1.0
            pen.color(hue_color(hue, 0.8, 0.9 - layer / layers * 0.4))
            pen.pensize(1)
            first = True

            for i in range(points + 1):
                angle = math.radians(i * 360 / points + angle_offset)
                x = scale * math.cos(angle)
                y = scale * math.sin(angle)
                if first:
                    pen.goto(x, y); pen.pendown(); first = False
                else:
                    pen.goto(x, y)

            pen.penup()
        screen.update()


def draw_portal(pen: turtle.Turtle, screen: turtle.Screen) -> None:
    total_steps = 1200
    pen.pensize(1)
    pen.goto(0, -5)
    pen.pendown()

    for i in range(total_steps):
        t     = i / total_steps * 8 * math.pi
        r     = 5 + t * 11
        wobble = math.sin(t * 6) * 8 + math.cos(t * 3) * 5
        x     = (r + wobble) * math.cos(t)
        y     = (r + wobble) * math.sin(t)
        hue   = cycle_hue(i, total_steps, 0.40)
        pen.color(hue_color(hue, 0.9, 1.0))

        if r > WIN_W * 0.55:
            break
        pen.goto(x, y)

        if i % 99999 == 0:
            screen.update()

    pen.penup()
    screen.update()


def draw_carousel(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    horses: list = [
        (7, 3, 6, 0.00, 35),
        (5, 2, 4, 0.12, 35),
        (8, 3, 7, 0.25, 32),
        (6, 4, 5, 0.40, 38),
        (9, 4, 8, 0.55, 30),
        (7, 2, 6, 0.68, 34),
        (5, 3, 4, 0.80, 36),
        (8, 5, 7, 0.92, 33),
    ]

    num       = len(horses)
    positions: list = [
        (170 * math.cos(math.radians(i * 360 / num)),
         170 * math.sin(math.radians(i * 360 / num)))
        for i in range(num)
    ]

    for (R, r, d, hue, scale), (cx, cy) in zip(horses, positions):
        steps = 400
        pen.pensize(1)
        first = True

        for i in range(steps + 1):
            t  = 2 * math.pi * i / steps * R
            x  = cx + scale * ((R - r) * math.cos(t) + d * math.cos((R - r) / r * t))
            y  = cy + scale * ((R - r) * math.sin(t) - d * math.sin((R - r) / r * t))
            h  = cycle_hue(i, steps, hue)
            pen.color(hue_color(h, 0.9, 1.0))

            if first:
                pen.goto(x, y); pen.pendown(); first = False
            else:
                pen.goto(x, y)

        pen.penup()
        screen.update()


def draw_rainbow(pen: turtle.Turtle, screen: turtle.Screen) -> None:
    layers = 8
    for layer in range(layers):
        steps   = 700
        pen.pensize(1)
        pen.goto(0, 0)
        pen.pendown()
        twist = layer * (math.pi / layers)

        for i in range(steps):
            t   = i / steps * 10 * math.pi
            r   = t * 19
            x   = r * math.cos(t + twist)
            y   = r * math.sin(t + twist)
            if abs(x) > WIN_W // 2 - 20 or abs(y) > WIN_H // 2 - 20:
                break
            hue = cycle_hue(i, steps, layer / layers)
            pen.color(hue_color(hue, 1.0, 1.0))
            pen.goto(x, y)

        pen.penup()
        if layer % 99999 == 0:
            screen.update()

    screen.update()


def draw_nautilus(pen: turtle.Turtle, screen: turtle.Screen) -> None:

    phi    = (1 + math.sqrt(5)) / 2   
    total  = 6 * math.pi
    steps  = 800
    pen.pensize(2)

    prev_x, prev_y = 0.0, 0.0
    for i in range(steps + 1):
        t   = total * i / steps
        r   = 5 * math.exp(0.15 * t)
        x   = r * math.cos(t)
        y   = r * math.sin(t)

        if abs(x) > WIN_W // 2 - 20 or abs(y) > WIN_H // 2 - 20:
            break

        frac = i / steps
        hue  = 0.08 + frac * 0.25  
        sat  = 0.7 + frac * 0.2
        pen.color(hue_color(hue, sat, 1.0))

        if i == 0:
            pen.goto(x, y); pen.pendown()
        else:
            pen.goto(x, y)

        if i % 99999 == 0:
            screen.update()

    pen.penup()

    chambers = 10
    for c in range(chambers):
        t_start = total * c / chambers
        t_end   = total * (c + 1) / chambers
        r_start = 5 * math.exp(0.15 * t_start)
        r_end   = 5 * math.exp(0.15 * t_end)
        hue     = 0.08 + (c / chambers) * 0.25
        pen.color(hue_color(hue, 0.6, 0.8))
        pen.pensize(1)
        pen.goto(r_start * math.cos(t_start),
                 r_start * math.sin(t_start))
        pen.pendown()
        pen.goto(r_end   * math.cos(t_end),
                 r_end   * math.sin(t_end))
        pen.penup()

    screen.update()


def draw_fireworks(pen: turtle.Turtle, screen: turtle.Screen) -> None:
    bursts: list = [
        {"cx":   0, "cy":  120, "rays": 24, "r": 180, "hue": 0.00},
        {"cx": -200, "cy":  60, "rays": 18, "r": 130, "hue": 0.33},
        {"cx":  200, "cy":  60, "rays": 20, "r": 140, "hue": 0.55},
        {"cx":  -80, "cy": -80, "rays": 30, "r": 160, "hue": 0.75},
        {"cx":  100, "cy": -90, "rays": 16, "r": 120, "hue": 0.15},
        {"cx":    0, "cy": -30, "rays": 36, "r": 200, "hue": 0.88},
    ]

    for burst in bursts:
        cx, cy = burst["cx"], burst["cy"]
        rays   = burst["rays"]
        r      = burst["r"]
        h0     = burst["hue"]

        for ray in range(rays):
            angle = math.radians(ray * 360 / rays)
            for seg in range(20):
                frac = seg / 20
                x0   = cx + r * frac       * math.cos(angle)
                y0   = cy + r * frac       * math.sin(angle)
                x1   = cx + r * (frac+0.05)* math.cos(angle)
                y1   = cy + r * (frac+0.05)* math.sin(angle)
                hue  = (h0 + frac * 0.15) % 1.0
                pen.color(hue_color(hue, 1.0, 1.0 - frac * 0.6))
                pen.pensize(max(1, 3 - int(frac * 3)))
                pen.goto(x0, y0); pen.pendown()
                pen.goto(x1, y1); pen.penup()

        for _ in range(rays):
            angle  = random.uniform(0, 2 * math.pi)
            length = random.uniform(r * 0.5, r * 1.1)
            sx     = cx + length * math.cos(angle)
            sy     = cy + length * math.sin(angle)
            hue    = (h0 + random.uniform(0, 0.2)) % 1.0
            pen.color(hue_color(hue, 0.8, 1.0))
            pen.goto(sx, sy)
            pen.dot(random.choice([2, 2, 3]))

        screen.update()

def draw_pattern(key: str, screen: turtle.Screen) -> None:
    bg = BG_COLORS.get(key, "#000000")
    screen.bgcolor(bg)
    screen.update()

    pen = make_pen()
    pen.goto(0, 0)

    dispatch: dict = {
        "butterfly": draw_butterfly,
        "flower":    draw_flower,
        "galaxy":    draw_galaxy,
        "vortex":    draw_vortex,
        "rose":      draw_rose,
        "starburst": draw_starburst,
        "ocean":     draw_ocean,
        "snowflake": draw_snowflake,
        "spiderweb": draw_spiderweb,
        "crystal":   draw_crystal,
        "portal":    draw_portal,
        "carousel":  draw_carousel,
        "rainbow":   draw_rainbow,
        "nautilus":  draw_nautilus,
        "fireworks": draw_fireworks,
    }

    if key in dispatch:
        dispatch[key](pen, screen)

    label_pen = make_writer()
    name = next((p["name"] for p in PATTERNS.values() if p["key"] == key), key)
    draw_label(label_pen, name)
    screen.update()

    save_last_pattern(key)


def main() -> None:
    screen = setup_screen("#000000")
    screen.colormode(1.0)   

    running      = [True]
    go_menu      = [True]
    go_random    = [False]

    def on_enter():
        go_menu[0] = True

    def on_r():
        go_random[0] = True

    def on_esc():
        running[0] = False

    screen.onkey(on_enter, "Return")
    screen.onkey(on_r,     "r")
    screen.onkey(on_r,     "R")
    screen.onkey(on_esc,   "Escape")
    screen.listen()

    while running[0]:
        if go_random[0]:
            key = random.choice(list(PATTERNS.values()))["key"]
            go_random[0] = False
            go_menu[0]   = False
            screen.clearscreen()
            screen.colormode(1.0)
            screen.onkey(on_enter, "Return")
            screen.onkey(on_r,     "r")
            screen.onkey(on_r,     "R")
            screen.onkey(on_esc,   "Escape")
            screen.listen()
            draw_pattern(key, screen)

        elif go_menu[0]:
            go_menu[0] = False
            screen.clearscreen()
            screen.colormode(1.0)
            screen.bgcolor("#030308")
            screen.onkey(on_enter, "Return")
            screen.onkey(on_r,     "r")
            screen.onkey(on_r,     "R")
            screen.onkey(on_esc,   "Escape")
            screen.listen()

            key = show_menu(screen)
            screen.clearscreen()
            screen.colormode(1.0)
            screen.onkey(on_enter, "Return")
            screen.onkey(on_r,     "r")
            screen.onkey(on_r,     "R")
            screen.onkey(on_esc,   "Escape")
            screen.listen()
            draw_pattern(key, screen)

        else:
            screen.update()
            time.sleep(0.05)

    screen.bye()


if __name__ == "__main__":
    main()