import os, math, datetime, cairo
from colors import colour_chooser, diffusion_calculator, cairo_rgb


months = [
    "january", "february", "march", "april", "may", "june", "july", 
    "august", "september", "october", "november", "december"
]


def render(persons, path):
    today = datetime.date.today()

    width = 4981
    height = 3508
    center_x = width / 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    background_path = os.path.join(os.path.dirname(__file__), "background.png")
    if os.path.exists(background_path):
        background = cairo.ImageSurface.create_from_png(background_path)
        background_width = background.get_width()
        background_height = background.get_height()
        context.save()
        context.scale(width / background_width, height / background_height)
        context.set_source_surface(background, 0, 0)
        context.paint()
        context.restore()
    else:
        context.set_source_rgb(0, 0, 0)
        context.paint()

    n = len(persons)
    turns = max(2, 1 + n // 12)
    radius_min = 60
    radius_max = min(width, height) / 2 - 120
    growth_coefficient = (radius_max - radius_min) / (2 * math.pi * turns)
    dot_radius = max(14, min(width, height) // 80)

    y_offsets = [
        (radius_min + growth_coefficient * (2 * math.pi * turns * i / max(n - 1, 1)))
        * math.sin(2 * math.pi * turns * i / max(n - 1, 1) - math.pi / 2)
        for i in range(n)
    ]
    angle_date_end = 2 * math.pi * turns + 0.25
    y_offsets.append(
        (radius_min + growth_coefficient * angle_date_end)
        * math.sin(angle_date_end - math.pi / 2)
    )
    center_y = height / 2 - (min(y_offsets) + max(y_offsets)) / 2

    positions = []
    for i in range(n):
        angle = 2 * math.pi * turns * i / max(n - 1, 1)
        radius = radius_min + growth_coefficient * angle
        positions.append((center_x + radius * math.cos(angle - math.pi / 2),
                          center_y + radius * math.sin(angle - math.pi / 2)))

    angle_max = 2 * math.pi * turns
    decor_dot_r = max(2, min(width, height) // 600)
    for j in range(0, 801):
        if j % 4 != 0:
            continue
        angle = angle_max * j / 800
        radius = radius_min + growth_coefficient * angle
        decor_dot_x = center_x + radius * math.cos(angle - math.pi / 2)
        decor_dot_y = center_y + radius * math.sin(angle - math.pi / 2)
        context.set_source_rgba(1, 1, 1, 0.45)
        context.arc(decor_dot_x, decor_dot_y, decor_dot_r, 0, 2 * math.pi)
        context.fill()

    for i, (_, age, is_alive, completeness_pct) in enumerate(persons):
        x, y = positions[i]
        r, g, b = cairo_rgb(colour_chooser(age))
        alpha = 1.0 if is_alive else 0.25

        glow_r = dot_radius * diffusion_calculator(completeness_pct)

        glow = cairo.RadialGradient(x, y, dot_radius, x, y, glow_r)
        glow.add_color_stop_rgba(0.0, r, g, b, alpha * 0.75)
        glow.add_color_stop_rgba(0.4, r, g, b, alpha * 0.30)
        glow.add_color_stop_rgba(1.0, r, g, b, 0.00)
        context.set_source(glow)
        context.arc(x, y, glow_r, 0, 2 * math.pi)
        context.fill()

        context.set_source_rgba(r, g, b, alpha)
        context.arc(x, y, dot_radius, 0, 2 * math.pi)
        context.fill()

    date_str = "%d %s %d" % (today.day, months[today.month - 1], today.year)
    font_size_date = min(width, height) // 38
    context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size_date)
    context.set_source_rgba(1, 1, 1, 0.70)
    angle_date = angle_max + 0.25
    for symbol in date_str:
        current_radius = radius_min + growth_coefficient * angle_date
        x = center_x + current_radius * math.cos(angle_date - math.pi / 2)
        y = center_y + current_radius * math.sin(angle_date - math.pi / 2)
        dxdangle = -current_radius * math.sin(angle_date - math.pi / 2) + growth_coefficient * math.cos(angle_date - math.pi / 2)
        dydangle =  current_radius * math.cos(angle_date - math.pi / 2) + growth_coefficient * math.sin(angle_date - math.pi / 2)
        angle = math.atan2(dydangle, dxdangle)
        context.save()
        context.translate(x, y)
        context.rotate(angle)
        context.move_to(0, 0)
        context.show_text(symbol)
        context.restore()
        text_extents = context.text_extents(symbol)
        advance = text_extents[4] if text_extents[4] > 0 else font_size_date * 0.55
        speed = math.sqrt(current_radius ** 2 + growth_coefficient ** 2)
        angle_date += (advance + font_size_date * 0.04) / speed

    surface.write_to_png(path)