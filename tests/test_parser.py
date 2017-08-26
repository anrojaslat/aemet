import os
import unittest

from src import parsers

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

STATIONS_IN_STATE = (
    '6302A', '6277B', '6381', '6364X', '6325O', '6329X', '6332X', '6291B',
    '6340X', '6367B', '6293X', '5060X', '5996B', '5973', '5906X', '5941X',
    '5911A', '5960', '6042I', '5983X', '5919X', '5910X', '5972X', '5950X',
    '6056X', '6001', '5995B', '5624X', '5598X', '5346X', '5394X', '5429X',
    '5402', '5427X', '5459X', '5470', '4267X', '5625X', '5361X', '5412X',
    '4263X', '5390Y', '5047E', '6272X', '5516D', '5530E', '5515X', '5051X',
    '6258X', '5582A', '6268X', '6268Y', '6267X', '6281X', '4560Y', '5858X',
    '4589X', '4527X', '4549Y', '4554X', '4608X', '4584X', '4541X', '4642E',
    '5860E', '4575X', '4622X', '5406X', '5298X', '5181D', '5164B', '5281X',
    '5038X', '5270B', '5279X', '5246', '5165X', '5210X', '5192', '6201X',
    '6127X', '6045X', '6106X', '6069X', '6143X', '6040X', '6058I', '6084X',
    '6375X', '6050X', '6156X', '6172O', '6155A', '6057X', '6083X', '6076X',
    '6213X', '6175X', '6032B', '6032X', '6088X', '6199B', '5733X', '5702X',
    '5835X', '5704B', '5641X', '5656', '5726X', '5654X', '5612B', '5891X',
    '5612X', '5796', '5998X', '5790Y', '5783'
)

STATES_IN_MAIN = (
    'and', 'arn', 'coo', 'can', 'clm', 'cle', 'cat', 'ceu', 'mel', 'mad',
    'nav', 'val', 'ext', 'gal', 'bal', 'rio', 'pva', 'ast', 'mur', 'and',
    'arn', 'coo', 'can', 'clm', 'cle', 'cat', 'ceu', 'mel', 'mad', 'nav',
    'val', 'ext', 'gal', 'bal', 'rio', 'pva', 'ast', 'mur'
)


def get_fixture_path(*x):
    return os.path.join(BASE_PATH, "fixtures", *x)


def read_file(path):
    with open(get_fixture_path(path)) as f:
        return "".join(f.readlines())


class TestMainParser(unittest.TestCase):
    def setUp(self):
        self.empty_file = read_file("empty.html")
        self.main_url_content = read_file("main.html")
        self.state_url_content = read_file("state.html")

    def test_main_parser_with_empty_file(self):
        state_parser = parsers.MainParser(self.empty_file)
        res = [state for state in state_parser.get_match()]
        self.assertEqual(res, [])
        self.assertEqual(len(res), 0)

    def test_main_parser_matches_state_regex(self):
        """ Should obtain the list of states in the fixture. """
        state_parser = parsers.MainParser(self.main_url_content)
        res = [state for state in state_parser.get_match()]
        self.assertEqual(set(res), set(STATES_IN_MAIN))
        self.assertEqual(len(res), len(STATES_IN_MAIN))

    def test_main_parser_doesnt_match_station_content(self):
        state_parser = parsers.MainParser(self.state_url_content)
        res = [state for state in state_parser.get_match()]
        self.assertEqual(res, [])
        self.assertEqual(len(res), 0)


class TestStateParser(unittest.TestCase):
    def setUp(self):
        self.empty_file = read_file("empty.html")
        self.main_url_content = read_file("main.html")
        self.state_url_content = read_file("state.html")

    def test_state_parser_with_empty_file(self):
        state_parser = parsers.StateParser(self.empty_file)
        res = [state for state in state_parser.get_match()]
        self.assertEqual(res, [])
        self.assertEqual(len(res), 0)

    def test_state_parser_doesnt_match_state_content(self):
        station_parser = parsers.StateParser(self.main_url_content)
        res = [station for station in station_parser.get_match()]
        self.assertEqual(res, [])
        self.assertEqual(len(res), 0)

    def test_state_parser_matches_station_regex(self):
        """ Should obtain the list of stations in the fixture. """
        station_parser = parsers.StateParser(self.state_url_content)
        res = [station for station in station_parser.get_match()]
        self.assertEqual(set(res), set(STATIONS_IN_STATE))
        self.assertEqual(len(res), len(STATIONS_IN_STATE))
