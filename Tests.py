import unittest
from Classes.InputFile import InputFile, Cell, Timeframe
import numpy as np
import pandas as pd


class HIPANormalizeToOneTest(unittest.TestCase):

    def setUp(self):

        self.baseline_means = [1487081.8921335714, 767143.2721442856, 1302190.2019421428, 1113130.6746035714,
                               730617.289225, 727189.5820014286, 936338.2629921428, 836700.6484707142,
                               858294.0763600001, 574486.6794642857, 600562.2055735714, 537954.3985042857,
                               1172866.5845135713, 1485344.8824335714, 622592.5966892857, 322743.4487364285,
                               1320165.877627857, 373303.8651064286, 867237.4988342858, 954028.9279242856,
                               1092703.4592564288, 487314.5808435714, 1171332.1299921428, 521986.17593857145,
                               872894.6925192857, 1177744.4341307143, 733837.2835971429, 649010.5102799999,
                               659096.1782657143, 1615544.4767764283, 736935.1047107143, 630746.2065414286,
                               771146.2786028573, 551325.5801535713, 828896.3158521428, 824434.8758892856,
                               1342635.6592607142, 846031.2291607143, 839358.5765878572, 704612.856605,
                               2194129.325722143, 898577.7755135715, 64155.768782142855]

        self.data = InputFile(1, "sampleData/time_traces.txt", "", "", 0, list(), 0, list(), list(), list(),
                              list())
        self.data.stimulation_timeframes = [372]
        self.data.percentage_limit = 0.6
        self.data.read_time_traces_file()
        self.data.create_cells()
        self.data.calculate_minutes()
        self.data.calculate_baseline_mean()
        self.data.normalize_timeframes_with_to_ones()
        self.data.calculate_timeframe_maximum()
        self.data.calculate_threshold()
        self.data.detect_above_threshold()
        # self.data.

    def test_rows_and_column_count(self):
        self.assertEqual(len(self.data.content.columns), 43)
        for i in self.data.content.columns:
            self.assertEqual(len(self.data.content[i]), 1400)

    def test_created_cells(self):
        """
        Tests that each cell is created correctly
        """
        for cell in self.data.cells:
            # Test column count
            self.assertEqual(len(cell.timeframes.columns), 3)
            # Test rows count
            for i in self.data.content.columns:
                self.assertEqual(len(self.data.content[i]), 1400)

            self.assertEqual(cell.timeframes['Value'].dtype, float)
            # Check maximum minutes
            self.assertEqual(cell.timeframes['IncludingMinute'].max(), 90)
            self.assertEqual(cell.timeframes['IncludingMinute'][15], 0.0)
            self.assertEqual(cell.timeframes['IncludingMinute'][16], 1.0)

    def test_calculate_minutes(self):
        self.assertEqual(self.data.total_detected_minutes, 91)

    def test_cell_baseline_mean(self):
        """
        Checks each baseline mean, with pre calculated values, which are assumed to be correct
        """
        index = 0
        for cell in self.data.cells:
            self.assertEqual(cell.baseline_mean, self.baseline_means[index])
            index += 1

    def test_cell_normalization_to_one(self):
        """
        Tests that the greatest value is 1
        """
        for cell in self.data.cells:
            self.assertEqual(cell.normalized_timeframes['Value'].max(), 1)

    def test_cell_threshold_calculation(self):
        for cell in self.data.cells:
            self.assertEqual(cell.threshold, 0.6)

    def test_above_threshold_detection(self):
        for cell in self.data.cells:
            for value in cell.normalized_timeframes['Value']:
                if value > cell.threshold:
                    self.assertEqual()
        pass


class HIPANormalizeBaselineTest(unittest.TestCase):

    def setUp(self):
        self.baseline_means = [1487081.8921335714, 767143.2721442856, 1302190.2019421428, 1113130.6746035714,
                               730617.289225, 727189.5820014286, 936338.2629921428, 836700.6484707142,
                               858294.0763600001, 574486.6794642857, 600562.2055735714, 537954.3985042857,
                               1172866.5845135713, 1485344.8824335714, 622592.5966892857, 322743.4487364285,
                               1320165.877627857, 373303.8651064286, 867237.4988342858, 954028.9279242856,
                               1092703.4592564288, 487314.5808435714, 1171332.1299921428, 521986.17593857145,
                               872894.6925192857, 1177744.4341307143, 733837.2835971429, 649010.5102799999,
                               659096.1782657143, 1615544.4767764283, 736935.1047107143, 630746.2065414286,
                               771146.2786028573, 551325.5801535713, 828896.3158521428, 824434.8758892856,
                               1342635.6592607142, 846031.2291607143, 839358.5765878572, 704612.856605,
                               2194129.325722143, 898577.7755135715, 64155.768782142855]

        self.data = InputFile(1, "sampleData/time_traces.txt", "", "", 0, list(), 0, list(), list(), list(),
                              list())
        self.data.stimulation_timeframes = [372]
        self.data.percentage_limit = 0.6
        self.data.read_time_traces_file()
        self.data.create_cells()
        self.data.calculate_minutes()
        self.data.calculate_baseline_mean()
        self.data.normalize_timeframes_with_to_ones()
        self.data.calculate_timeframe_maximum()
        self.data.calculate_threshold()
        self.data.detect_above_threshold()
        # self.data.


if __name__ == '__main__':
    test_classes_to_run = [HIPANormalizeBaselineTest, HIPANormalizeToOneTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

