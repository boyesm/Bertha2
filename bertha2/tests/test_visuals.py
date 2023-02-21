import unittest
from unittest import TestCase

from bertha2.visuals import *

if __name__ == '__main__':
    unittest.main()


class Test(TestCase):
    def test_process_title(self):
        self.assertEqual("I can't ****ing believe this is happening,...", process_title(
            "I can't fucking believe this is happening, what the fuck is wrong with people these days?"))
        self.assertEqual("What the **** did you just ****ing say abo...", process_title(
            "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals..."))
        self.assertEqual("This is such a ****ing waste of my time, I...", process_title(
            "This is such a fucking waste of my time, I have better things to do than deal with this bullshit."))

    '''
    def test_update_playing_next(self):
        self.fail()

    def test_update_onscreen_visuals_from_state(self):
        self.fail()

    def test_update_visual_state_with_new_video(self):
        self.fail()

    def test_update_visual_state_with_new_bertha_status(self):
        self.fail()

    def test_visuals_process(self):
        self.fail()
    '''
