import copy


from evalrescallers_paper import common_data, maps


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


def svg_text(x, y, text, fontsize, position='middle', writing_mode='lr', vertical=False, font_family='arial'):
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
        'writing-mode="' + writing_mode + '" ',
        'x="' + str(x) + '" ',
        'y="' + str(y) + '">',
        text,
        '</text>'])


def make_plot(stats_dict, tools, drugs, outfile, first_line=False, ten_k=False, how_to_scale='not at all', susc_gap=None, susc_xticks=None, res_xticks=None, plot_gap_size=30):
    if susc_gap is not None:
        susc_gap_width = susc_gap[1] - susc_gap[0]
        stats_dict = copy.deepcopy(stats_dict)
        for drug in drugs:
            for tool in tools:
                if stats_dict[drug][tool]['TN'] > susc_gap[1]:
                    stats_dict[drug][tool]['TN'] -= susc_gap_width - plot_gap_size

    max_count_res_keys = ['FN', 'TP', 'UNK_R', 'FAIL_R']
    max_count_susc_keys = ['FP', 'TN', 'UNK_S', 'FAIL_S']
    sample_count = {}

    for drug in drugs:
        res_counts = set()
        susc_counts = set()
        for tool in tools:
            if tool == '10k_predict':
                continue
            res_count = sum([stats_dict[drug][tool][x] for x in max_count_res_keys])
            susc_count = sum([stats_dict[drug][tool][x] for x in max_count_susc_keys])
            res_counts.add(res_count)
            susc_counts.add(susc_count)
        assert len(res_counts) == len(susc_counts) == 1

        sample_count[drug] = {'res': res_counts.pop(), 'susc': susc_counts.pop()}

    max_count_res = max([sample_count[x]['res'] for x in sample_count])
    max_count_susc = max([sample_count[x]['susc'] for x in sample_count])
    centre_space = 20
    x_margin = 10

    if how_to_scale == 'not at all':
        total_width = 600
        total_bar_width = total_width - 2 * (centre_space + x_margin)
        susc_bar_width = total_bar_width * max_count_susc / (max_count_res + max_count_susc)
        res_bar_width = total_bar_width * max_count_res / (max_count_res + max_count_susc)
        x_centre = x_margin + susc_bar_width + centre_space
    elif how_to_scale == 'res susc independent':
        total_width = 1000
        total_bar_width = total_width - 2 * (centre_space + x_margin)
        susc_bar_width = 0.5 * total_bar_width
        res_bar_width = 0.5 * total_bar_width
        x_centre = total_width / 2
    elif how_to_scale == 'all to 100':
        total_width = 500
        total_bar_width = total_width - 2 * (centre_space + x_margin)
        susc_bar_width =  0.5 * total_bar_width - 40
        res_bar_width = 0.5 * total_bar_width - 40
        x_centre = total_width / 2


    bar_height = 13
    drug_spacer = 10
    x_susc_bar_left = x_centre - centre_space - susc_bar_width
    x_res_bar_right = x_centre + centre_space + res_bar_width

    y = 20

    svg_lines = []
    svg_lines.append(svg_text(0.5 * (x_susc_bar_left + x_centre - centre_space), y, 'Susceptible samples', 20))
    svg_lines.append(svg_text(0.5 * (x_centre + centre_space + x_res_bar_right), y, 'Resistant samples', 20))
    y = 45
    susc_tick_zeros = len(str(max_count_susc)) - 1
    susc_tick_gap = int('1' + '0' * susc_tick_zeros)
    susc_ticks = [-x for x in range(round(-max_count_susc, -susc_tick_zeros), 1, susc_tick_gap) if x > -max_count_susc]
    res_tick_zeros = len(str(max_count_res)) - 1
    res_tick_gap = int('1' + '0' * res_tick_zeros)
    res_ticks = list(range(0, round(max_count_res, -res_tick_zeros) + 1, res_tick_gap))

    if how_to_scale == 'all to 100':
        susc_ticks = [0, 0.25*max_count_susc, 0.5*max_count_susc, 0.75*max_count_susc, max_count_susc]
        res_ticks = [0, 0.25*max_count_res, 0.5*max_count_res, 0.75*max_count_res, max_count_res]
        susc_ticks_labels = ['0', '25', '50', '75', '100']
        res_ticks_labels = ['0', '25', '50', '75', '100']
    else:
        if susc_xticks is not None and susc_gap is not None:
            susc_ticks_labels = [str(x) for x in susc_xticks]
            susc_ticks = []
            for i in susc_xticks:
                if i < susc_gap[0]:
                    susc_ticks.append(i)
                else:
                    susc_ticks.append(i - (susc_gap_width - plot_gap_size))
        else:
            susc_ticks_labels = [str(x) for x in susc_ticks]

        if res_xticks is not None:
            res_ticks = res_xticks
        res_ticks_labels = [str(x) for x in res_ticks]

    svg_lines.append(svg_line(x_susc_bar_left, y, x_centre - centre_space, y, 'black', 1))
    svg_lines.append(svg_line(x_centre + centre_space, y, x_res_bar_right, y, 'black', 1))
    y_tick = y

    y += 5

    for drug in drugs:
        y_drug_top = y
        for tool in tools:
            if drug not in common_data.first_line_drugs and tool == '10k_predict':
                continue
            stats = stats_dict[drug][tool]
            y_bottom = y + bar_height
            if how_to_scale == 'all to 100':
                if sample_count[drug]['res'] == 0:
                    x_fail = x_fn = x_right = x_centre + centre_space
                else:
                    x_fail = x_centre + centre_space + res_bar_width * (stats['UNK_R'] + stats['FAIL_R']) / sample_count[drug]['res']
                    x_fn = x_fail + res_bar_width * (stats['FN'] / sample_count[drug]['res'])
                    x_right = x_centre + centre_space + res_bar_width
            else:
                x_fail = x_centre + centre_space + res_bar_width * ((stats['UNK_R'] + stats['FAIL_R']) / max_count_res)
                x_fn = x_fail + res_bar_width * (stats['FN'] / max_count_res)
                x_right = x_centre + centre_space + res_bar_width * (sample_count[drug]['res'] / max_count_res)
            svg_lines.append(svg_rectangle(x_centre + centre_space, y, x_fail, y_bottom, common_data.other_colours['UNK_R'], 'black'))
            svg_lines.append(svg_rectangle(x_fail, y, x_fn, y_bottom, common_data.other_colours['FN'], 'black'))
            svg_lines.append(svg_rectangle(x_fn, y, x_right, y_bottom, common_data.tool_colours[tool], 'black'))

            if how_to_scale == 'all to 100':
                if sample_count[drug]['susc'] == 0:
                    x_fail = x_fn = x_right = x_centre - centre_space
                else:
                    x_fail = x_centre - centre_space - susc_bar_width * ((stats['UNK_S'] + stats['FAIL_S']) / sample_count[drug]['susc'])
                    x_fp = x_fail - susc_bar_width * stats['FP'] / sample_count[drug]['susc']
                    x_left = x_centre - centre_space - susc_bar_width
            else:
                x_fail = x_centre - centre_space - susc_bar_width * ((stats['UNK_S'] + stats['FAIL_S']) / max_count_susc)
                x_fp = x_fail - susc_bar_width * (stats['FP'] / max_count_susc)
                x_left = x_centre - centre_space - susc_bar_width * (sample_count[drug]['susc'] / max_count_susc)
            svg_lines.append(svg_rectangle(x_fail, y, x_centre - centre_space, y_bottom, common_data.other_colours['UNK_S'], 'black'))
            svg_lines.append(svg_rectangle(x_fp, y, x_fail, y_bottom, common_data.other_colours['FN'], 'black'))
            svg_lines.append(svg_rectangle(x_left, y, x_fp, y_bottom, common_data.tool_colours[tool], 'black'))

            y += bar_height

        svg_lines.append(svg_text(x_centre, 0.5 * (y_drug_top + y) + 7, common_data.drug_abbreviations[drug], 15))
        if how_to_scale == 'all to 100':
            svg_lines.append(svg_text(x_susc_bar_left - 3, 0.5 * (y_drug_top + y) + 7, str(sample_count[drug]['susc']), 15, position='end'))
            svg_lines.append(svg_text(x_res_bar_right + 3, 0.5 * (y_drug_top + y) + 7, str(sample_count[drug]['res']), 15, position='start'))

        y += drug_spacer

    grid_lines = []

    for x, label in zip(res_ticks, res_ticks_labels):
        x_pos = x_centre + centre_space + res_bar_width * x / max_count_res
        svg_lines.append(svg_line(x_pos, y_tick-4, x_pos, y_tick, 'black', 1))
        svg_lines.append(svg_text(x_pos, y_tick-7, label, 15))
        grid_lines.append(svg_line(x_pos, y_tick, x_pos, y-drug_spacer, 'lightgray', 1))
    for x, label in zip(susc_ticks, susc_ticks_labels):
        x_pos = x_centre - centre_space - susc_bar_width * x / max_count_susc
        svg_lines.append(svg_line(x_pos, y_tick-4, x_pos, y_tick, 'black', 1))
        svg_lines.append(svg_text(x_pos, y_tick-7, label, 15))
        grid_lines.append(svg_line(x_pos, y_tick, x_pos, y-drug_spacer, 'lightgray', 1))

    if susc_gap is not None:
        svg_lines.append(r'''<defs>
    <linearGradient id="gradwhiteleft" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="50%" style="stop-color:rgb(255,255,255);stop-opacity:-1" />
      <stop offset="100%" style="stop-color:rgb(255,255,255);stop-opacity:1" />
    </linearGradient>
  </defs>''')
        svg_lines.append(r'''<defs>
    <linearGradient id="gradwhiteright" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="50%" style="stop-color:rgb(255,255,255);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(255,255,255);stop-opacity:-1" />
    </linearGradient>
  </defs>''')

        x_left = x_centre - centre_space - susc_bar_width * ((susc_gap[0] + plot_gap_size) / max_count_susc)
        x_right = x_centre - centre_space - susc_bar_width * (susc_gap[0] / max_count_susc)
        x_middle = 0.5 * (x_left + x_right)
        svg_lines.append(svg_rectangle(x_left, y_tick+1, x_middle, y+1, 'url(#gradwhiteleft)', 'white', border_width=0))
        svg_lines.append(svg_rectangle(x_middle, y_tick+1, x_right, y+1, 'url(#gradwhiteright)', 'white', border_width=0))
        svg_lines.append(svg_line(x_left+3, y_tick, x_right, y_tick, 'white', 1))
        svg_lines.append(svg_line(x_right-3, y_tick+3, x_right+3, y_tick-3, 'black', 1))
        svg_lines.append(svg_line(x_left, y_tick+3, x_left+6, y_tick-3, 'black', 1))


    with open(outfile, 'w') as f:
        print(r'''<?xml version="1.0" standalone="no"?>
        <!DOCTYPE svg PUBLIC " -//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
        <svg width="''' + str(total_width) + '" height="' + str(y) + '">', file=f)
        print(*grid_lines, sep='\n', file=f)
        print(*svg_lines, sep='\n', file=f)
        print('</svg>', file=f)

    maps.svg2pdf(outfile, outfile.replace('.svg', '.pdf'))


def make_legend(tools, outfile):
    font_size = 14
    square_len = 20
    y_space = 3
    svg_lines = []
    y = 5
    square_left = 5
    square_right = square_left + square_len
    total_width=200


    for tool in tools:
        svg_lines.append(svg_rectangle(square_left, y, square_right, y + square_len, common_data.tool_colours[tool], 'black'))
        svg_lines.append(svg_text(square_right + 5, y + square_len - 0.4 * font_size, tool, font_size, position='start'))
        y += square_len + y_space

    f = open(outfile, 'w')
    print(r'''<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC " -//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
    <svg width="''' + str(total_width) + '" height="' + str(y) + '">', file=f)
    print(*svg_lines, sep='\n', file=f)
    print('</svg>', file=f)
    f.close()
    maps.svg2pdf(outfile, outfile.replace('.svg', '.pdf'))


