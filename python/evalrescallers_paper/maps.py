#!/usr/bin/env python3

import os
import argparse
import subprocess
import textwrap

import matplotlib
matplotlib.use('Agg')

# Note need this installed:
# sudo apt-get install python3-mpltoolkits.basemap
# for import Basemap to work
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from evalrescallers import ten_k_validation_data

from evalrescallers_paper import svg


mykrobe_colour = '#7fc97f'
validate_colour = '#beaed4'
test_colour = '#fdc086'


def make_map_no_donuts(outfile, europe=False):
    if europe:
        world_map = Basemap(llcrnrlon=-10, llcrnrlat=36, urcrnrlon=23, urcrnrlat=59, resolution='i')
    else:
        world_map = Basemap(llcrnrlon=-140, llcrnrlat=-60,urcrnrlon=160,urcrnrlat=70)
    world_map.drawmapboundary(fill_color='aliceblue', linewidth=0)
    world_map.fillcontinents(color='lightgray', lake_color='aliceblue')
    world_map.drawcountries(color="darkgray")
    plt.savefig(outfile)
    plt.close()


def donut_plot(values, outfile, country):
    colours = [mykrobe_colour, validate_colour, test_colour]
    fig = plt.figure(figsize=(5,5))
    circle=plt.Circle( (0,0), 0.7, color='white')
    plt.pie(values, colors=colours, counterclock=False, startangle=90)
    plt.text(0, 0, str(sum(values)), horizontalalignment='center', verticalalignment='center', fontsize=55)

    if country in {'Canada', 'Russia', 'Pakistan', 'Thailand', 'Belgium', 'Swaziland'}:
        y_text = -1.01
        valign = 'top'
    else:
        y_text = 1.01
        valign = 'bottom'
    plt.text(0, y_text, country, horizontalalignment='center', verticalalignment=valign, fontsize=60)

    p=plt.gcf()
    p.gca().add_artist(circle)
    plt.savefig(outfile, transparent=True)
    plt.close()


def make_counts(all_counts):
    '''all_counts should be counts dictionary made by samples_table.make_samples_tsv()'''
    europe_countries = {
        'Belgium',
        'Germany',
        'Italy',
        'Netherlands',
        'Serbia',
        'Spain',
        'UK',
    }

    europe_counts = {x: all_counts[x] for x in europe_countries}
    world_counts = {x: all_counts[x] for x in all_counts if x not in europe_countries}
    world_counts['Europe'] = {'test': 0, 'train': 0, 'validate': 0}
    for x in europe_counts:
        for k in world_counts['Europe']:
            world_counts['Europe'][k] += europe_counts[x][k]

    return world_counts, europe_counts


def make_donuts(counts_dict, outprefix):
    files = {}
    for country in counts_dict:
        outfile = f'{outprefix}.{country}.svg'.replace(' ', '_')
        files[country] = outfile
        values = [counts_dict[country][x] for x in ['train', 'validate', 'test']]
        donut_plot(values, outfile, country)

    return files


def make_map_with_donuts(counts, outprefix, europe=False, debug=False):
    donut_coords = {
        'Australia': (369,193),
        'Belgium': (195,123),
        'Canada': (88,91),
        'China': (330,123),
        'Germany': (255,120),
        'Italy': (285,207),
        'Netherlands': (210,105),
        'Pakistan': (288,132),
        'Peru': (115,180),
        'Russia': (314,91),
        'Serbia': (372,194),
        'Sierra Leone': (190,150),
        'South Africa': (233,201),
        'Spain': (110,230),
        'Swaziland': (258,210),
        'Thailand': (328,143),
        'UK': (131,96),
        'Uzbekistan': (282,114),
        'Europe': (210,110),
    }
    no_donuts_svg = f'{outprefix}.tmp.svg'
    final_svg = f'{outprefix}.svg'
    final_pdf = final_svg.replace('.svg', '.pdf')
    donut_files = make_donuts(counts, outprefix)
    make_map_no_donuts(no_donuts_svg, europe=europe)

    with open(no_donuts_svg) as f:
        svg_lines = [x.rstrip() for x in f]
    assert svg_lines[-1] == '</svg>'
    last_svg_line = svg_lines.pop()

    # line to point to Swaziland
    if not europe:
        svg_lines.append('<line x1="280" y1="230" x2="262" y2="212" style="stroke:rgb(0,0,0);stroke-width:1" />')

    for country in donut_files:
        x, y = donut_coords[country]
        filename = os.path.abspath(donut_files[country])
        svg_lines.append(f'<image x="{x}" y="{y}" width="32" height="32" xlink:href="file:{filename}"></image>')


    svg_lines.append(last_svg_line)
    with open(final_svg, 'w') as f:
        print(*svg_lines, sep='\n', file=f)

    svg.svg2pdf(final_svg, final_pdf)

    if not debug:
        os.unlink(no_donuts_svg)
        os.unlink(final_svg)
        for filename in donut_files.values():
            os.unlink(filename)


def make_legend(outprefix, debug=False):
    svg_file = f'{outprefix}.svg'
    pdf_file = f'{outprefix}.pdf'
    s = r'''        <svg height="70pt" width="70pt">
        <text x="10" y="11">Dataset</text>
        <circle cx="11" cy="30" r="10" stroke="black" stroke-width="0.5" fill="''' + mykrobe_colour + r'''" />
        <text x="23" y="35">Training</text>
        <circle cx="11" cy="55" r="10" stroke="black" stroke-width="0.5" fill="''' + validate_colour + r'''" />
        <text x="23" y="60">Validation</text>
        <circle cx="11" cy="80" r="10" stroke="black" stroke-width="0.5" fill="''' + test_colour + r'''" />
        <text x="23" y="85">Test</text>
        </svg>'''

    with open(svg_file, 'w') as f:
        print(textwrap.dedent(s), file=f)

    svg.svg2pdf(svg_file, pdf_file)
    if not debug:
        os.unlink(svg_file)


def make_maps(outprefix, country_counts, debug=False):
    world_outprefix = f'{outprefix}.world'
    europe_outprefix = f'{outprefix}.europe'
    make_legend(f'{outprefix}.legend', debug=debug)
    world_counts, europe_counts = make_counts(country_counts)
    make_map_with_donuts(world_counts, world_outprefix, europe=False, debug=debug)
    make_map_with_donuts(europe_counts, europe_outprefix, europe=True, debug=debug)

