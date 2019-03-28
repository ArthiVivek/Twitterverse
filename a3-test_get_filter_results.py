import unittest
import twitterverse_functions as tf


class TestGetFilterResults(unittest.TestCase):

    def test_get_filter_results_name_includes(self):
        """ Test get_filter_results using the name_includes filter in
        filter_dict. """

        data_file = open('data.txt', 'r')
        twitter_dict = tf.process_data(data_file)
        data_file.close()

        actual = tf.get_filter_results(twitter_dict, ['tomCruise', \
        'PerezHilton'], {'name_includes': 'tomCruise'})
        expected = ['tomCruise']
        self.assertEqual(actual, expected)

    def test_get_filter_results_location_includes(self):
        """ Test get_filter_results using the location_includes filter in
        filter_dict. """

        data_file = open('data.txt', 'r')
        twitter_dict = tf.process_data(data_file)
        data_file.close()

        actual = tf.get_filter_results(twitter_dict, ['tomCruise', \
        'PerezHilton'], {'location_includes': 'Hollywood, California'})
        expected = ['PerezHilton']
        self.assertEqual(actual, expected)

    def test_get_filter_results_location_includes(self):
        """ Test get_filter_results using the following filter in filter_dict.
        """

        data_file = open('data.txt', 'r')
        twitter_dict = tf.process_data(data_file)
        data_file.close()

        actual = tf.get_filter_results(twitter_dict, ['tomCruise', \
        'PerezHilton', 'tomfan'], {'follower': 'katieH'})
        expected = ['tomCruise', 'PerezHilton']
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
