import copy
import filecmp
import json
import os
import shutil
import unittest

from evalrescallers_paper import summary_data_handler

modules_dir = os.path.dirname(os.path.abspath(summary_data_handler.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'summary_data_handler')


class TestSummaryDataHandler(unittest.TestCase):
    def test_fix_quinolones(self):
        '''test fix_quinolones'''
        summary_data = {
            "sample1": {
                "tool1": {
                    "Success": False,
                    "resistance_calls": {}
                },
                "tool2": {
                    "Success": True,
                    "resistance_calls": {
                        "Isoniazid": [["R", "gene1", "X42Y", {"conf": 42, "ref_depth": 0, "alt_depth": 9, "expected_depth": 11}]],
                        "Rifampicin": [["S", None, None, None]],
                        "Ciprofloxacin": [["R", "gene2", "A1B", {"conf": 43, "ref_depth": 1, "alt_depth": 10, "expected_depth": 11}]],
                        "Quinolones": [["R", "gene2", "A1B", {"conf": 43, "ref_depth": 1, "alt_depth": 10, "expected_depth": 11}]],
                    }
                },
            },
            "sample2": {
                "tool1": {
                    "Success": True,
                    "resistance_calls": {
                        "Quinolones": [["R", "gene2", "A1B", {"conf": 38, "ref_depth": 5, "alt_depth": 17, "expected_depth": 15}]],
                        "Ciprofloxacin": [["R", "gene2", "A1B", {"conf": 43, "ref_depth": 1, "alt_depth": 10, "expected_depth": 11}]],
                        "Isoniazid": [["S", None, None, None]],
                    }
                },
                "tool2": {
                    "Success": True,
                    "resistance_calls": {
                        "Ethambutol": [["S", None, None, None]],
                    }
                }
            }
        }

        expect = copy.deepcopy(summary_data)
        del expect['sample1']['tool2']['resistance_calls']['Quinolones']
        expect['sample2']['tool1']['resistance_calls']['Ciprofloxacin'] = expect['sample2']['tool1']['resistance_calls']['Quinolones']
        expect['sample2']['tool1']['resistance_calls']['Moxifloxacin'] = expect['sample2']['tool1']['resistance_calls']['Quinolones']
        expect['sample2']['tool1']['resistance_calls']['Ofloxacin'] = expect['sample2']['tool1']['resistance_calls']['Quinolones']
        summary_data_handler.SummaryDataHandler.fix_quinolones(summary_data, {"tool1"}, {"tool2"})
        self.assertEqual(expect, summary_data)


    def test_summary_json_to_metrics_and_var_call_counts(self):
        '''test summary_json_to_metrics_and_var_call_counts'''
        drugs = {
            'mykrobe': {'Isoniazid', 'Rifampicin'},
            '10k': {'Rifampicin', 'Pyrazinamide'},
        }

        json_file = os.path.join(data_dir, 'summary_json_to_metrics_and_var_call_counts.json')
        with open(json_file) as f:
            json_data = json.load(f)

        truth_pheno = {
            'sample1': {
                'dataset': 'mykrobe',
                'pheno': {'Isoniazid': 'R', 'Rifampicin': 'S'}
            },
            'sample2': {
                'dataset': 'mykrobe',
                'pheno': {'Isoniazid': 'R', 'Rifampicin': 'R'}
            },
            'sample3': {
                'dataset': '10k',
                'pheno': {'Rifampicin': 'S', 'Pyrazinamide': 'R'}
            },
            'sample4': {
                'dataset': '10k',
                'pheno': {'Rifampicin': 'S', 'Pyrazinamide': 'R'}
            },
            'sample5': {
                'dataset': '10k',
                'pheno': {'Rifampicin': 'R', 'Pyrazinamide': 'R'}
            },
        }

        got_tool_counts, got_variant_counts, got_conf_and_depths, got_regimen_counts = summary_data_handler.SummaryDataHandler.summary_json_to_metrics_and_var_call_counts(json_data, truth_pheno, drugs, 'tb')

        expect_tool_counts = {
            'mykrobe': {
                'Isoniazid': {
                    'tool1': {'TP': 2, 'FP': 0, 'TN': 0, 'FN': 0, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                    'tool2': {'TP': 1, 'FP': 0, 'TN': 0, 'FN': 0, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                },
                'Rifampicin': {
                    'tool1': {'TP': 1, 'FP': 0, 'TN': 1, 'FN': 0, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                    'tool2': {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 1, 'FAIL_R': 0, 'FAIL_S': 1, 'UNK_S': 0, 'UNK_R': 0},
                },
            },
            '10k': {
                'Rifampicin': {
                    'tool1': {'TP': 0, 'FP': 0, 'TN': 2, 'FN': 0, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                    'tool2': {'TP': 0, 'FP': 1, 'TN': 0, 'FN': 0, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 1, 'UNK_R': 0},
                },
                'Pyrazinamide': {
                    'tool1': {'TP': 1, 'FP': 0, 'TN': 0, 'FN': 1, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                    'tool2': {'TP': 1, 'FP': 0, 'TN': 0, 'FN': 1, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                },
            },
        }
        self.assertEqual(expect_tool_counts, got_tool_counts)

        expect_variant_counts = {
            'mykrobe': {
                'Isoniazid': {
                    'tool1': {'gene1.X42Y': {'TP': 1, 'FP': 0}, 'gene1.A1B': {'TP': 1, 'FP': 0}},
                    'tool2': {'gene1.A1B': {'TP': 1, 'FP': 0}},
                },
                'Rifampicin': {
                    'tool1': {'gene2.C1D;gene2.E2F': {'TP': 1, 'FP': 0}},
                    'tool2': {},
                },
            },
            '10k': {
                'Rifampicin': {
                    'tool1': {},
                    'tool2': {'gene2.I42M': {'TP': 0, 'FP': 1}},
                },
                'Pyrazinamide': {
                    'tool1': {'gene3.X10Y': {'TP': 1, 'FP': 0}},
                    'tool2': {'gene3.X10Y': {'TP': 1, 'FP': 0}},
                },
            },

        }
        self.assertEqual(expect_variant_counts, got_variant_counts)

        expect_conf_and_depths = {
            'mykrobe': {
                'Rifampicin': {},
                'Isoniazid': {
                    'tool1': {'TP': [(42, 0, 10, 11), (43, 0, 11, 11)], 'FP': [], 'TN': [], 'FN': []},
                    'tool2': {'TP': [(44, 0, 12, 11)], 'FP': [], 'TN': [], 'FN': []},
                },
            },
            '10k': {
                'Pyrazinamide': {
                    'tool1': {'TP': [(100, 2, 14, 11)], 'FP': [], 'TN': [], 'FN': []},
                    'tool2': {'TP': [(1001, 0, 5, 1100)], 'FP': [], 'TN': [], 'FN': []},
                },
                'Rifampicin': {'tool2': {'TP': [], 'FP': [(50, 1, 13, 11)], 'TN': [], 'FN': []}},
            },
        }
        self.assertEqual(expect_conf_and_depths, got_conf_and_depths)


        expect_regimen_counts = {
          '10k': {
            'sample3': {
              'phenos': {
                'tool1': {'Pyrazinamide': 'S', 'Rifampicin': 'S'},
                'tool2': {'Pyrazinamide': 'S', 'Rifampicin': 'R'},
                'truth': {'Pyrazinamide': 'R', 'Rifampicin': 'S'},
              },
              'regimens': {'tool1': None, 'tool2': 10, 'truth': None}
            },
            'sample4': {
              'phenos': {
                'tool1': {'Pyrazinamide': 'R', 'Rifampicin': 'S'},
                'tool2': {'Pyrazinamide': 'R', 'Rifampicin': None},
                'truth': {'Pyrazinamide': 'R', 'Rifampicin': 'S'},
              },
             'regimens': {'tool1': None, 'tool2': None, 'truth': None}
            }
          },
          'mykrobe': {
            'sample1': {
              'phenos': {
                'tool1': {'Isoniazid': 'R', 'Rifampicin': 'S'},
                'tool2': {},
                'truth': {'Isoniazid': 'R', 'Rifampicin': 'S'},
              },
              'regimens': {
                'tool1': None, 'tool2': None, 'truth': None}
            },
            'sample2': {
              'phenos': {
                'tool1': {'Isoniazid': 'R', 'Rifampicin': 'R'},
                'tool2': {'Isoniazid': 'R', 'Rifampicin': 'S'},
                'truth': {'Isoniazid': 'R', 'Rifampicin': 'R'},
              },
              'regimens': {'tool1': 11, 'tool2': None, 'truth': 11}
            }
          }
        }
        self.assertEqual(expect_regimen_counts, got_regimen_counts)


        # One call is "r" in the input json. Test the option lower_case_r_means_resistant=False)
        got_tool_counts, got_variant_counts, got_conf_and_depths, got_regimen_counts = summary_data_handler.SummaryDataHandler.summary_json_to_metrics_and_var_call_counts(json_data, truth_pheno, drugs, 'tb', lower_case_r_means_resistant=False)
        expect_tool_counts['mykrobe']['Isoniazid']['tool1']['TP'] -= 1
        expect_tool_counts['mykrobe']['Isoniazid']['tool1']['FN'] += 1
        del expect_variant_counts['mykrobe']['Isoniazid']['tool1']['gene1.X42Y']
        expect_conf_and_depths['mykrobe']['Isoniazid']['tool1']['FN'] = [(42, 0, 10, 11)]
        expect_conf_and_depths['mykrobe']['Isoniazid']['tool1']['TP'] = [(43, 0, 11, 11)]
        self.assertEqual(expect_tool_counts, got_tool_counts)
        self.assertEqual(expect_variant_counts, got_variant_counts)
        self.maxDiff = None
        self.assertEqual(expect_conf_and_depths, got_conf_and_depths)


    def test_add_all_counts_to_tools_counts(self):
        '''test add_all_counts_to_tools_counts'''
        tools_counts = {
            'mykrobe': {
                'drug1': {
                    'tool1': {'TP': 2, 'FP': 0, 'TN': 0, 'FN': 1, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 2},
                    'tool2': {'TP': 1, 'FP': 1, 'TN': 0, 'FN': 0, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 3},
                },
                'drug2': {
                    'tool1': {'TP': 1, 'FP': 1, 'TN': 2, 'FN': 3, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                    'tool2': {'TP': 1, 'FP': 0, 'TN': 0, 'FN': 1, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                },
            },
            '10k': {
                'drug2': {
                    'tool1': {'TP': 2, 'FP': 1, 'TN': 4, 'FN': 1, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                    'tool2': {'TP': 0, 'FP': 1, 'TN': 0, 'FN': 0, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 1},
                },
                'drug3': {
                    'tool1': {'TP': 1, 'FP': 1, 'TN': 0, 'FN': 1, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                    'tool2': {'TP': 1, 'FP': 0, 'TN': 1, 'FN': 0, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 1},
                },
            },
        }

        expect_all = {
            'drug1': {
                'tool1': {'TP': 2, 'FP': 0, 'TN': 0, 'FN': 1, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 2},
                'tool2': {'TP': 1, 'FP': 1, 'TN': 0, 'FN': 0, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 3},
            },
            'drug2': {
                'tool1': {'TP': 3, 'FP': 2, 'TN': 6, 'FN': 4, 'FAIL_R': 2, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                'tool2': {'TP': 1, 'FP': 1, 'TN': 0, 'FN': 1, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 1},
            },
            'drug3': {
                'tool1': {'TP': 1, 'FP': 1, 'TN': 0, 'FN': 1, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                'tool2': {'TP': 1, 'FP': 0, 'TN': 1, 'FN': 0, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 1},
            },
        }
        expect_tools_counts = copy.copy(tools_counts)
        expect_tools_counts['all'] = expect_all
        summary_data_handler.SummaryDataHandler.add_all_counts_to_tools_counts(tools_counts)
        self.assertEqual(expect_tools_counts, tools_counts)


    def test_add_all_variants_to_variant_counts(self):
        '''test add_all_variants_to_variant_counts'''
        variant_counts = {
            'mykrobe': {
                'drug1': {
                    'tool1': {'var1': {'TP': 1, 'FP': 0}, 'var2': {'TP': 1, 'FP': 0}},
                    'tool2': {'var3': {'TP': 1, 'FP': 0}},
                },
                'drug2': {
                    'tool1': {'var4': {'TP': 1, 'FP': 0}},
                    'tool2': {'var5': {'TP': 0, 'FP': 1}},
                },
            },
            '10k': {
                'drug2': {
                    'tool1': {'var4': {'TP': 0, 'FP': 1}},
                    'tool2': {},
                },
                'drug3': {
                    'tool1': {'var6': {'TP': 1, 'FP': 0}},
                    'tool2': {'var7': {'TP': 1, 'FP': 0}},
                },
            },
        }

        expect_all = {
            'drug1': {
                'tool1': {'var1': {'TP': 1, 'FP': 0}, 'var2': {'TP': 1, 'FP': 0}},
                'tool2': {'var3': {'TP': 1, 'FP': 0}},
            },
            'drug2': {
                'tool1': {'var4': {'TP': 1, 'FP': 1}},
                'tool2': {'var5': {'TP': 0, 'FP': 1}},
            },
            'drug3': {
                'tool1': {'var6': {'TP': 1, 'FP': 0}},
                'tool2': {'var7': {'TP': 1, 'FP': 0}},
            },
        }

        expect_variant_counts = copy.copy(variant_counts)
        expect_variant_counts['all'] = expect_all
        summary_data_handler.SummaryDataHandler.add_all_variants_to_variant_counts(variant_counts)
        self.assertEqual(expect_variant_counts, variant_counts)


    def test_write_accuracy_stats_file(self):
        '''test write_accuracy_stats_file'''
        tool_counts = {
            'mykrobe': {
                'drug1': {
                    'tool1': {'TP': 9, 'FP': 1, 'TN': 10, 'FN': 2, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 1},
                },
                'drug2': {
                    'tool2': {'TP': 10, 'FP': 0, 'TN': 3, 'FN': 0, 'FAIL_R': 1, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 0},
                },
            },
            '10k': {
                'drug3': {
                    'tool1': {'TP': 3, 'FP': 3, 'TN': 1, 'FN': 1, 'FAIL_R': 0, 'FAIL_S': 0, 'UNK_S': 0, 'UNK_R': 1},
                },
            },
        }

        expected_file = os.path.join(data_dir, 'write_accuracy_stats_file.tsv')
        tmp_file = 'tmp.write_accuracy_stats_file.tsv'
        summary_data_handler.SummaryDataHandler.write_accuracy_stats_file(tool_counts, tmp_file)
        self.assertTrue(filecmp.cmp(expected_file, tmp_file, shallow=False))
        os.unlink(tmp_file)

    def test_write_variant_counts_file_for_one_tool(self):
        '''test write_variant_counts_file_for_one_tool'''
        tmp_out = 'tmp.write_variant_counts_file_for_one_tool.tsv'
        variant_counts = {
            'mykrobe': {
                'drug1': {
                    'tool1': {'var1': {'TP': 1, 'FP': 0}, 'var2': {'TP': 1, 'FP': 0}},
                    'tool2': {'var3': {'TP': 1, 'FP': 0}},
                },
                'drug2': {
                    'tool1': {'var4': {'TP': 1, 'FP': 0}},
                    'tool2': {'var5': {'TP': 0, 'FP': 1}},
                },
            },
            '10k': {
                'drug2': {
                    'tool1': {'var4': {'TP': 0, 'FP': 1}},
                    'tool2': {},
                },
                'drug3': {
                    'tool1': {'var6': {'TP': 1, 'FP': 0}},
                    'tool2': {'var7': {'TP': 1, 'FP': 0}},
                },
            },
        }

        summary_data_handler.SummaryDataHandler.add_all_variants_to_variant_counts(variant_counts)
        summary_data_handler.SummaryDataHandler.write_variant_counts_file_for_one_tool(variant_counts, 'tool1', tmp_out)
        expect_file = os.path.join(data_dir, 'write_variant_counts_file_for_one_tool.tool1.tsv')
        self.assertTrue(filecmp.cmp(expect_file, tmp_out, shallow=False))
        summary_data_handler.SummaryDataHandler.write_variant_counts_file_for_one_tool(variant_counts, 'tool2', tmp_out)
        expect_file = os.path.join(data_dir, 'write_variant_counts_file_for_one_tool.tool2.tsv')
        self.assertTrue(filecmp.cmp(expect_file, tmp_out, shallow=False))
        os.unlink(tmp_out)



    def test_write_all_variant_counts_files(self):
        '''test write_all_variant_counts_files'''
        variant_counts = {
            'mykrobe': {
                'drug1': {
                    'tool1': {'var1': {'TP': 1, 'FP': 0}, 'var2': {'TP': 1, 'FP': 0}},
                    'tool2': {'var3': {'TP': 1, 'FP': 0}},
                },
                'drug2': {
                    'tool1': {'var4': {'TP': 1, 'FP': 0}},
                    'tool2': {'var5': {'TP': 0, 'FP': 1}},
                },
            },
            '10k': {
                'drug2': {
                    'tool1': {'var4': {'TP': 0, 'FP': 1}},
                    'tool2': {},
                },
                'drug3': {
                    'tool1': {'var6': {'TP': 1, 'FP': 0}},
                    'tool2': {'var7': {'TP': 1, 'FP': 0}},
                },
            },
        }
        tmp_prefix = 'tmp.write_all_variant_counts_files'
        summary_data_handler.SummaryDataHandler.add_all_variants_to_variant_counts(variant_counts)
        summary_data_handler.SummaryDataHandler.write_all_variant_counts_files(variant_counts, tmp_prefix)
        for tool in 'tool1', 'tool2':
            got_file = f'{tmp_prefix}.{tool}.tsv'
            self.assertTrue(os.path.exists(got_file))
            expect_file = os.path.join(data_dir, f'write_all_variant_counts_files.{tool}.tsv')
            self.assertTrue(filecmp.cmp(expect_file, got_file, shallow=False))
            os.unlink(got_file)


    def test_write_conf_file(self):
        '''test write_conf_file'''
        conf_counts = {
            'mykrobe': {
                'drug1': {
                    'tool1': {'TP': [(42, 0, 10, 50), (43, 1, 12, 50)], 'FP': [(1, 0, 1, 50), (4, 1, 2, 50), (3, 1, 3, 50)], 'TN': [(100, 1, 50, 50), (101, 2, 55, 50)], 'FN': [(6, 2, 3, 50)]},
                    'tool2': {'TP': [(44, 1, 20, 50)], 'FP': [], 'TN': [], 'FN': []},
                },
            },
            '10k': {
                'drug1': {
                    'tool1': {'TP': [(11, 1, 5, 50)], 'FP': [(8, 0, 4, 50)], 'TN': [(1, 0, 1, 50), (50, 0, 60, 50)], 'FN': [(4, 0, 5, 50)]},
                },
                'drug2': {'tool2': {'TP': [], 'FP': [(50, 10, 1000, 500)], 'TN': [], 'FN': []}},
            },
        }

        tmp_file = 'tmp.plots.write_conf_file.tsv'
        expected_file = os.path.join(data_dir, 'write_conf_file.tsv')
        summary_data_handler.SummaryDataHandler.write_conf_file(conf_counts, tmp_file)
        self.assertTrue(filecmp.cmp(expected_file, tmp_file, shallow=False))
        os.unlink(tmp_file)


    def test_write_regimen_counts_files(self):
        '''test write_regimen_counts_files'''
        regimen_counts = {
          '10k': {
            'sample3': {
              'phenos': {
                'tool1': {'Pyrazinamide': 'S', 'Rifampicin': 'S'},
                'tool2': {'Pyrazinamide': 'S', 'Rifampicin': 'R'},
                'truth': {'Pyrazinamide': 'R', 'Rifampicin': 'S'},
              },
              'regimens': {'tool1': None, 'tool2': 10, 'truth': None}
            },
            'sample4': {
              'phenos': {
                'tool1': {'Pyrazinamide': 'R', 'Rifampicin': 'S'},
                'tool2': {'Pyrazinamide': 'R', 'Rifampicin': None},
                'truth': {'Pyrazinamide': 'R', 'Rifampicin': 'S'},
              },
             'regimens': {'tool1': None, 'tool2': None, 'truth': None}
            }
          },
          'mykrobe': {
            'sample1': {
              'phenos': {
                'tool1': {'Isoniazid': 'R', 'Rifampicin': 'S'},
                'tool2': {},
                'truth': {'Isoniazid': 'R', 'Rifampicin': 'S'},
              },
              'regimens': {
                'tool1': None, 'tool2': None, 'truth': None}
            },
            'sample2': {
              'phenos': {
                'tool1': {'Isoniazid': 'R', 'Rifampicin': 'R'},
                'tool2': {'Isoniazid': 'R', 'Rifampicin': 'S'},
                'truth': {'Isoniazid': 'R', 'Rifampicin': 'R'},
              },
              'regimens': {'tool1': 10, 'tool2': None, 'truth': 10}
            }
          }
        }

        tmp_prefix = 'tmp.write_regimen_counts_files'
        summary_data_handler.SummaryDataHandler.write_regimen_counts_files(regimen_counts, tmp_prefix)
        for x in 'tool1', 'tool2', 'summary':
            got_file = f'{tmp_prefix}.{x}.tsv'
            expected_file = os.path.join(data_dir, f'write_regimen_counts_files.{x}.tsv')
            self.assertTrue(filecmp.cmp(expected_file, got_file, shallow=False))
            os.unlink(got_file)
        #expected_file = os.path.join(data_dir, 'write_regimen_counts_files.tsv')
        #self.assertTrue(filecmp.cmp(expected_file, tmp_file, shallow=False))


    def test_run_tb(self):
        '''test run on tb data'''
        infile = os.path.join(data_dir, 'run.tb.in.json')
        outprefix = 'tmp.summary_data_handler.tb.run'
        with open(infile) as f:
            json_data = json.load(f)
        p = summary_data_handler.SummaryDataHandler(json_data, 'tb')
        p.run(outprefix)
        expected_file = os.path.join(data_dir, 'run.tb.out.accuracy_stats.tsv')
        self.assertTrue(filecmp.cmp(expected_file, outprefix + '.accuracy_stats.tsv'))
        os.unlink(outprefix + '.accuracy_stats.tsv')
        expected_file = os.path.join(data_dir, 'run.tb.out.conf.tsv')
        self.assertTrue(filecmp.cmp(expected_file, outprefix + '.conf.tsv'))
        os.unlink(outprefix + '.conf.tsv')

        for x in '10k_predict', 'tool1', 'tool2', 'summary':
            got_file = f'{outprefix}.regimen_counts.{x}.tsv'
            expected_file = os.path.join(data_dir, f'run.tb.out.regimen_counts.{x}.tsv')
            self.assertTrue(filecmp.cmp(expected_file, got_file, shallow=False))
            os.unlink(got_file)

        for tool in 'tool1', 'tool2':
            got_file = f'{outprefix}.variant_counts.{tool}.tsv'
            self.assertTrue(os.path.exists(got_file))
            expect_file = os.path.join(data_dir, f'run.tb.out.variant_counts.{tool}.tsv')
            self.assertTrue(filecmp.cmp(expect_file, got_file, shallow=False))
            os.unlink(got_file)


    def test_run_staph(self):
        '''test run on staph data'''
        infile = os.path.join(data_dir, 'run.staph.in.json')
        outprefix = 'tmp.summary_data_handler.staph.run'
        with open(infile) as f:
            json_data = json.load(f)
        p = summary_data_handler.SummaryDataHandler(json_data, 'staph')
        p.run(outprefix)
        expected_file = os.path.join(data_dir, 'run.staph.out.accuracy_stats.tsv')
        self.assertTrue(filecmp.cmp(expected_file, outprefix + '.accuracy_stats.tsv'))
        os.unlink(outprefix + '.accuracy_stats.tsv')
        expected_file = os.path.join(data_dir, 'run.staph.out.conf.tsv')
        self.assertTrue(filecmp.cmp(expected_file, outprefix + '.conf.tsv'))
        os.unlink(outprefix + '.conf.tsv')
        for tool in 'tool1', 'tool2':
            got_file = f'{outprefix}.variant_counts.{tool}.tsv'
            self.assertTrue(os.path.exists(got_file))
            expect_file = os.path.join(data_dir, f'run.staph.out.variant_counts.{tool}.tsv')
            self.assertTrue(filecmp.cmp(expect_file, got_file, shallow=False))
            os.unlink(got_file)


