import subprocess


def svg2pdf(infile, outfile):
    subprocess.check_output(f'inkscape {infile} --export-pdf {outfile}', shell=True)


def svg_line(x1, y1, x2, y2, color, thickness):
       return ''.join([
           '<line ',
           'stroke="' + color + '" ',
           'stroke-width="' + str(thickness) + '" ',
           'x1="' + str(x1) + '" ',
           'y1="' + str(y1) + '" ',
           'x2="' + str(x2) + '" ',
           'y2="' + str(y2) + '" ',
           '/>'])


# coords  = list of tuples [(x1, y1), (x2, y2) ...]
def svg_polygon(coords, fill_colour, border_colour, border_width=1, opacity=-1):
    return_string = '<polygon points="' + ' '.join([str(x[0])+','+str(x[1]) for x in coords]) + '" ' \
            + 'fill="' + fill_colour + '" '

    if opacity != -1:
        return_string += 'fill-opacity="' + str(opacity) + '" '

    return_string += 'stroke="' + border_colour + '" ' \
            + 'stroke-width="' + str(border_width) + '" ' \
            + '/>'

    return return_string


# x1 y1 = top left corner. x2 y2 = bottom right corner
def svg_rectangle(x1, y1, x2, y2, fill_colour, border_colour, border_width=1, opacity=-1):
    coords = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    return svg_polygon(coords, fill_colour, border_colour, border_width=border_width, opacity=opacity)


def svg_text(x, y, text, fontsize, position='middle', writing_mode='lr', vertical=False, font_family='arial', vertical_align='bottom'):
    if vertical:
        vert = 'transform="rotate(-90,' + str(x) + ',' + str(y) + ')" '
    else:
        vert = ''

    return ''.join([
        '<text ',
        vert,
        'text-anchor="' + position + '" ',
        'font-size="' + str(fontsize) + '" ',
        'font-family="' + font_family + '" ',
        f'dominant-baseline="{vertical_align}" ',
        'writing-mode="' + writing_mode + '" ',
        'x="' + str(x) + '" ',
        'y="' + str(y) + '">',
        text,
        '</text>'])


def svg_circle(x, y, r, fill, stroke, stroke_width=1):
        return '<circle fill="' + fill + '" ' \
                + 'stroke="' + stroke + '" ' \
                + 'stroke-width="' + str(stroke_width) + '" ' \
                + 'cx="' + str(x) + '" ' \
                + 'cy="' + str(y) + '" ' \
                + 'r="' + str(r) + '" ' \
                + '/>'


def svg_ribbon(x1, y11, y12, x2, y21, y22, fill_colour, border_colour, border_width=1, opacity=-1):
    # Need to draw two bezier curves, same x coords, different y coords
    x_mid = 0.5 * (x1 + x2)
    y_mid1 = 0.5 * (y11 + y21)
    y_mid2 = 0.5 * (y12 + y22)
    opacity_string = '' if opacity == -1 else f';fill-opacity:{opacity}'

    return ''.join([
        '<path ',
        f'style="fill:{fill_colour};stroke:{border_colour}{opacity_string}" ',
        f'd="M{x1},{y11} C{x_mid},{y11} {x_mid},{y21} {x2},{y21} ', # top curve
        f'L{x2},{y22}', # right line
        f'C{x_mid},{y22} {x_mid},{y12} {x1},{y12}' # bottom curve
        ' Z" />',  # close the path
    ])
