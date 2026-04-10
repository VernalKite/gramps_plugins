colour_diapason = [ # correlates with person's age
    (0,  "#545FFF"),   # infancy (0-1 years)
    (2,  "#00DDFF"),   # childhood (2-12 years)
    (13, "#FEFFEE"),   # puberty (13-18 years)
    (19, "#FFF0A2"),   # adolescence (19-23 years)
    (24, "#FFE853"),   # youth (24-35 years)
    (36, "#FF9022"),   # adulthood (36-59 years)
    (60, "#FF0000"),   # senescence (60+ years)
]


def colour_chooser(age):
    for minimum_age, colour in reversed(colour_diapason):
        if age >= minimum_age:
            return colour

def diffusion_calculator(profile_completeness):
    return min((profile_completeness - 1) // 20 + 3.0, 7.0)

def cairo_rgb(hex):
    hex = hex.strip("#")
    return tuple((int(hex[i:i+2], 16) / 255 for i in (0, 2, 4)))