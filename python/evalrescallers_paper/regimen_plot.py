from collections import OrderedDict
import copy
import csv
import subprocess

from evalrescallers import who_treatment

from evalrescallers_paper import svg


def load_regimen_counts_tsv(infile, datasets):
    with open(infile) as f:
        all_data = {}
        reader = csv.DictReader(f,delimiter='\t')
        for d in reader:
            if d['Dataset'] in datasets and d['Truth_regimen'] != "NA":
                if d['Tool'] not in all_data:
                    all_data[d['Tool']] = {}
                if d['Called_regimen'] == "NA":
                    d['Called_regimen'] = 100

                truth, called = int(d['Truth_regimen'])-1, int(d['Called_regimen'])-1
                if truth not in all_data[d['Tool']]:
                    all_data[d['Tool']][truth] = {}
                all_data[d['Tool']][truth][called] = all_data[d['Tool']][truth].get(called, 0) + int(d['Count'])

    return all_data


def plot_one_tool(data, outfile, tool_name, ignore=None, y_scale=0.8):
    assert outfile.endswith('.svg')
    to_ignore = {}
    if ignore is not None:
        data = copy.deepcopy(data)
        for k1, k2 in ignore:
            if k1 in data and k2 in data[k1]:
                if k1 not in to_ignore:
                    to_ignore[k1] = {}
                to_ignore[k1][k2] = data[k1][k2]
                del data[k1][k2]
                if len(data[k1]) == 1:
                    del data[k1]

    for k in data:
        try:
            del data[k][99]
        except:
            pass

    colours = [
     '#f0e8e3',
     '#e2d3c9',
     '#f5cfb6',
     '#FDD49E',
     '#FDBB84',
     '#FCA964',
     '#FC8D59',
     '#E34A33',
     '#d81529',
     '#CE1256',
     '#980043',
     '#400013'
    ]

    truth_nodes = {}
    called_nodes = {}
    edges = []

    for truth in data:
        if truth not in truth_nodes:
            truth_nodes[truth] = {}

        for called in data[truth]:
            if called not in called_nodes:
                called_nodes[called] = {}

            truth_nodes[truth][called] = data[truth][called]
            called_nodes[called][truth] = data[truth][called]
            edges.append((truth, called, data[truth][called]))

    edges.sort()
    plot_width = 1050
    margin = 5

    drugs = OrderedDict([
        ('H', 'Isoniazid'),
        ('R', 'Rifampicin'),
        ('Z', 'Pyrazinamide'),
        ('E', 'Ethambutol'),
        ('Lfx', 'Levofloxacin'),
        ('Mfx', 'Moxifloxacin'),
        ('Gfx', 'Gatifloxacin'),
        ('S', 'Streptomycin'),
        ('Am', 'Amikacin'),
        ('Km', 'Kanamycin'),
        ('Cm', 'Capreomycin'),
        ('Eto', 'Ethionamide'),
        ('Cs', 'Cycloserine'),
        ('Trd', 'Terizidone'),
        ('Cfz', 'Clofazimide'),
        ('Lzd', 'Linezolid'),
        ('Bdq', 'Bedaquiline'),
        ('X', 'Para-aminosalicylate/Para-aminosalicylate-sodium, Prothionamide, Rifabutin, Rifapentine, High dose Isoniazid (if possible), and two or more of: Clofazimide, Linezolid, Thioacetazone, Amox-Clavulanate, Imipenem/Cilastatin, Meropenem'),
    ])

    regimen_to_drug = {
        1: {'req': ('H', 'R', 'Z', 'E')},
        2: {'req': ('R', 'Z', 'E', (1, 'Lfx', 'Mfx', 'Gfx'))},
        3: {'req': ('R', 'Z', 'E')},
        4: {'req': ('R', 'E', (1, 'Lfx', 'Mfx', 'Gfx'))},
        5: {'req': ('R', 'Z', (1, 'Lfx', 'Mfx', 'Gfx'))},
        6: {'req': ('R', 'Eto', (1, 'Lfx', 'Mfx', 'Gfx'), (1, 'Km', 'Am', 'Cm'))},
        7: {'req': ('R', 'Eto', (1, 'Lfx', 'Mfx', 'Gfx'), 'S')},
        8: {'req': ('H', 'R', 'E')},
        9: {'req': ('H', 'R', 'Z')},
        10: {'req': ('H', 'Bdq', 'Lzd', (1, 'Lfx', 'Mfx'), (1, 'Cs', 'Trd', 'Cfz'))},
        11: {'req': ('Bdq', 'Lzd', (1, 'Lfx', 'Mfx'), (1, 'Cs', 'Trd', 'Cfz'))},
        12: {'req': ('E', 'Z', (1, 'Am', 'S'), (1, 'Lfx', 'Mfx', 'Gfx'), 'Eto', 'Cs', 'Trd', 'X')},
    }

    regimen_to_pheno = {
        1: {'H': 'S', 'R': 'S', 'Z': 'S', 'E': 'S'},
        2: {'H': 'R', 'R': 'S', 'Z': 'S', 'E': 'S'},
        3: {'H': 'R', 'R': 'S', 'Z': 'S', 'E': 'S', 'Mfx': 'R'},
        4: {'H': 'R', 'R': 'S', 'Z': 'R', 'E': 'S'},
        5: {'H': 'R', 'R': 'S', 'Z': 'S', 'E': 'R'},
        6: {'H': 'R', 'R': 'S', 'Z': 'R', 'E': 'R'},
        7: {'H': 'R', 'R': 'S', 'Z': 'R', 'E': 'R', 'Km': 'R', 'Am': 'R', 'Cm': 'R', 'S': 'S'},
        8: {'H': 'S', 'R': 'S', 'Z': 'R', 'E': 'S'},
        9: {'H': 'S', 'R': 'S', 'Z': 'S', 'E': 'R'},
        10: {'R': 'R'},
        11: {'H': 'R', 'R': 'R'},
        12: {'H': 'R', 'R': 'R', 'Mfx': 'R'},
    }

    regimen_to_description = {
        1: "DS-TB",
        2: "Mono-H DR-TB",
        3: "Mono-H DR-TB",
        4: "H-Z DR-TB",
        5: "H-E DR-TB",
        6: "H-Z-E DR-TB",
        7: "H-Z-E DR-TB",
        8: "Mono-Z DR-TB",
        9: "Mono-E DR-TB",
        10: "RR-TB",
        11: "MDR-TB",
        12: "(pre-)XDR-TB",
    }

    drug_col_width = 26
    svg_lines = []
    x = 10
    headings_y = 20
    drug_to_x_centre = {}

    for drug in drugs:
        drug_to_x_centre[drug] = x + 0.5 * drug_col_width
        svg_lines.append(svg.svg_text(x + 0.5 * drug_col_width, headings_y, drug, 12, font_weight='bold', vertical_align='middle'))
        x += drug_col_width

    x += 80
    right_half_x_left  = x + 10
    node_to_edge_space = 50
    left_node_x = right_half_x_left + node_to_edge_space
    node_width = 20
    right_node_x = plot_width - node_to_edge_space - node_width - 75
    y_start = 40
    node_y_gap = 30
    svg_node_lines = []
    truth_nodes_y_tops = {}
    truth_nodes_y_bottoms = {}
    called_nodes_y_tops = {}
    called_nodes_y_bottoms = {}
    truth_node_to_y_centre = {}

    # Nodes on the left
    y = y_start
    svg_lines.append(svg.svg_text(left_node_x - 103, headings_y-7, 'Phenotype', 11, font_weight='bold', position='middle', font_family='arial', vertical_align='middle'))
    svg_lines.append(svg.svg_text(left_node_x - 103, headings_y+4, 'regimen', 11, font_weight='bold', position='middle', font_family='arial', vertical_align='middle'))
    svg_lines.append(svg.svg_text(left_node_x - 5, headings_y, 'Samples', 11, font_weight='bold', position='end', font_family='arial', vertical_align='middle'))
    svg_lines.append(svg.svg_text(right_node_x + 65, headings_y, 'Samples', 11, font_weight='bold', position='end', font_family='arial', vertical_align='middle'))
    svg_lines.append(svg.svg_text(right_node_x + 100, headings_y-7, tool_name, 11, font_weight='bold', position='middle', font_family='arial', vertical_align='middle'))
    svg_lines.append(svg.svg_text(right_node_x + 100, headings_y+4, 'regimen', 11, font_weight='bold', position='middle', font_family='arial', vertical_align='middle'))

    for node in regimen_to_drug:
        if node-1 not in truth_nodes:
            truth_nodes[node-1] = {}
        if node-1 not in called_nodes:
            called_nodes[node-1] = {}

    for node, node_counts in sorted(truth_nodes.items()):
        truth_nodes_y_tops[node] = y
        if len(node_counts) > 0:
            total_samples = sum(node_counts.values())
        else:
            total_samples = 0
        node_y_bottom = y + y_scale * total_samples
        truth_node_to_y_centre[node] = 0.5 * (y + node_y_bottom)
        svg_node_lines.append(svg.svg_rectangle(left_node_x, y, left_node_x + node_width, node_y_bottom,
            colours[int(node)], colours[int(node)], border_width=1))
        #svg_lines.append(svg.svg_text(left_node_x - 110, 0.5 * (y + node_y_bottom),
        #    who_treatment.regimens[node+1].definition, 11, position='start', font_family='arial', vertical_align='middle'))
        svg_lines.append(svg.svg_text(left_node_x - 103, 0.5 * (y + node_y_bottom) - 6, str(node+1), 11, font_weight='bold', position='middle', font_family='arial', vertical_align='middle'))
        svg_lines.append(svg.svg_text(left_node_x - 103, 0.5 * (y + node_y_bottom) + 6, regimen_to_description[node+1], 10, position='middle', font_family='arial', vertical_align='middle'))
        svg_lines.append(svg.svg_text(left_node_x - 5, 0.5 * (y + node_y_bottom),
            str(total_samples), 11, position='end', font_family='arial', vertical_align='middle'))

        if node in to_ignore:
            total_ignored = sum(to_ignore[node].values())
            svg_lines.append(svg.svg_text(left_node_x - 5, 0.5 * (y + node_y_bottom) + 12,
                f'(+{total_ignored})', 11, position='end', font_family='arial', vertical_align='middle'))

        y = node_y_bottom + node_y_gap
        truth_nodes_y_bottoms[node] = node_y_bottom

    y = y_start

    # Nodes on the right
    for node, node_counts in sorted(called_nodes.items()):
        called_nodes_y_tops[node] = y
        total_samples = sum(node_counts.values())
        node_y_bottom = y + y_scale * total_samples
        called_nodes_y_bottoms[node] = node_y_bottom
        svg_node_lines.append(svg.svg_rectangle(right_node_x, y, right_node_x + node_width, node_y_bottom,
            colours[int(node)], colours[int(node)], border_width=1))
        svg_lines.append(svg.svg_text(right_node_x + node_width + 3, 0.5 * (y + node_y_bottom),
            str(total_samples), 11, position='start', font_family='arial', vertical_align='middle'))
        svg_lines.append(svg.svg_text(right_node_x + 100, 0.5 * (y + node_y_bottom),
            str(node+1), 11, font_weight='bold', position='middle', font_family='arial', vertical_align='middle'))
        if node in to_ignore:
            total_ignored = sum(to_ignore[node].values())
            svg_lines.append(svg.svg_text(right_node_x + node_width + 3, 0.5 * (y + node_y_bottom) + 12,
                f'(+{total_ignored})', 11, position='start', font_family='arial', vertical_align='middle'))

        y = node_y_bottom + node_y_gap

    # Ribbons
    sample_total_counts = {'truth': {}, 'called': {}}

    for truth_node, called_node, samples in edges:
        if truth_node not in sample_total_counts['truth']:
            sample_total_counts['truth'][truth_node] = 0
        if called_node not in sample_total_counts['called']:
            sample_total_counts['called'][called_node] = 0

        y11 = truth_nodes_y_tops[truth_node] + y_scale * sample_total_counts['truth'][truth_node]
        sample_total_counts['truth'][truth_node] += samples
        y12 = truth_nodes_y_tops[truth_node] + y_scale * sample_total_counts['truth'][truth_node]
        y21 = called_nodes_y_tops[called_node] + y_scale * sample_total_counts['called'][called_node]
        sample_total_counts['called'][called_node] += samples
        y22 = called_nodes_y_tops[called_node] + y_scale * sample_total_counts['called'][called_node]
        svg_lines.append(svg.svg_ribbon(left_node_x + node_width, y11, y12, right_node_x, y21, y22,
            colours[int(truth_node)], colours[int(truth_node)], border_width=0.5, opacity=0.8))

    # Regimen circles and R/S
    svg_regimen_lines = []
    circle_radius = 0.1 * drug_col_width
    y_circle_R_S_offset = 7
    pheno_letters_lines = []

    for node, regime in regimen_to_drug.items():
        y_centre = truth_node_to_y_centre[node-1]
        y_circle_centre = y_centre + y_circle_R_S_offset
        y_R_or_S = y_centre - y_circle_R_S_offset

        for req_or_opt in regime:
            if req_or_opt not in regime:
                continue

            if req_or_opt == 'req':
                line_colour = 'black'
            else:
                line_colour = 'lightgrey'

            for drugs_tuple in regime[req_or_opt]:
                if type(drugs_tuple) is tuple:
                    x_min = float('Inf')
                    x_max = 0
                    to_append = []
                    number_of_lines = drugs_tuple[0]
                    if number_of_lines == 1:
                        lines_y = [y_circle_centre]
                        line_width = 1.5
                    else:
                        assert number_of_lines == 2
                        lines_y = [y_circle_centre - circle_radius / 2, y_circle_centre + circle_radius / 2]
                        line_width = 1

                    for drug in drugs_tuple[1:]:
                        to_append.append(svg.svg_circle(drug_to_x_centre[drug], y_circle_centre, 0.2 * drug_col_width, colours[node-1], line_colour, stroke_width=1))
                        x_min = min(x_min, drug_to_x_centre[drug])
                        x_max = max(x_max, drug_to_x_centre[drug])

                    for line_y in lines_y:
                        svg_regimen_lines.append(svg.svg_line(x_min, line_y, x_max, line_y, line_colour, line_width))
                    svg_regimen_lines.append(to_append)
                else:
                    svg_regimen_lines.append(svg.svg_circle(drug_to_x_centre[drugs_tuple], y_circle_centre, 0.2 * drug_col_width, colours[node-1], line_colour, stroke_width=1))

        for drug, pheno in regimen_to_pheno[node].items():
            pheno_letters_lines.append(svg.svg_text(drug_to_x_centre[drug], y_R_or_S, pheno, 10, vertical_align='middle'))

    # Make vertical lines to separate drugs
    #y_top = min(truth_nodes_y_tops.values())
    y_top = margin
    #y_bottom = max(truth_nodes_y_bottoms.values())
    y_bottom = y - margin
    for drug in drugs:
        x_pos = drug_to_x_centre[drug] - 0.5 * drug_col_width
        svg_lines.append(svg.svg_line(x_pos, y_top, x_pos, y_bottom, 'lightgrey', 1))
        if drug == 'X':
            x_pos = drug_to_x_centre[drug] + 0.5 * drug_col_width
            svg_lines.append(svg.svg_line(x_pos, y_top, x_pos, y_bottom, 'lightgrey', 1))

    # horizontal lines to separate regimens
    x_left = min(drug_to_x_centre.values()) - 0.5 * drug_col_width
    x_right = left_node_x
    y_top_line = truth_nodes_y_tops[0] - 10
    svg_lines.append(svg.svg_line(x_left, y_top, plot_width - margin, y_top, 'lightgrey', 1))
    svg_lines.append(svg.svg_line(x_left, y_top_line, plot_width - margin, y_top_line, 'lightgrey', 1))
    svg_lines.append(svg.svg_line(plot_width - margin, y_top, plot_width - margin, y_bottom, 'lightgrey', 1))
    svg_lines.append(svg.svg_line(x_left, y_bottom, plot_width - margin, y_bottom, 'lightgrey', 1))
    for i in range(0, len(truth_nodes_y_bottoms) - 1, 1):
        y_pos = 0.5 * (truth_nodes_y_bottoms[i] + truth_nodes_y_tops[i+1])
        svg_lines.append(svg.svg_line(x_left, y_pos, x_right, y_pos, 'lightgrey', 1))
        y_pos = 0.5 * (called_nodes_y_bottoms[i] + called_nodes_y_tops[i+1])
        svg_lines.append(svg.svg_line(right_node_x + node_width, y_pos, plot_width - margin, y_pos, 'lightgrey', 1))


    f = open(outfile, 'w')
    print(r'''<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC " -//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
    <svg width="''' + str(plot_width) + '" height="' + str(y) + '">', file=f)
    # plot nodes last so that borders are on top of ribbons and therefore still visible
    print(*svg_lines, svg_node_lines, svg_regimen_lines, pheno_letters_lines, sep='\n', file=f)
    print('</svg>', file=f)
    f.close()
    svg.svg2pdf(outfile, outfile.replace('.svg', '.pdf'))


