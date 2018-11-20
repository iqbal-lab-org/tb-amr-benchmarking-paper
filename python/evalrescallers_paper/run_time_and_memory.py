import subprocess
import json


def json_to_tsv(json_dict, tsv_out):
    '''json_dict expected to be json object loaded from summary.json
    made by tb-amr-benchmarking pipeline'''
    with open(tsv_out, 'w') as f:
        print('Sample', 'Tool', 'RAM (MB)', 'Wall_clock (s)', sep='\t', file=f)

        for sample in sorted(json_dict):
            for tool, tool_dict in sorted(json_dict[sample].items()):
                if tool_dict['Success']:
                    ram_in_mb = round(tool_dict['time_and_memory']['ram'] / 1000, 2)
                    time_in_seconds = round(tool_dict['time_and_memory']['wall_clock_time'], 2)
                    print(sample, tool, ram_in_mb, time_in_seconds, sep='\t', file=f)


