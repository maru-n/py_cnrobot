#!/usr/env/python

import unittest
import util


class TestCNRobotUtil(unittest.TestCase):

    def setUp(self):
        self.sample_filename = "sampledata.spike"
        pass

    def test_load_data(self):
        data = util.load_data(self.sample_filename)
        print data

if __name__ == '__main__':
    unittest.main()
