from unittest import TestCase, skipIf

from bertha2.settings import status_text_obs_source_id, playing_video_obs_source_id
from bertha2.utils.obs import *

is_obs_open = input("Is OBS open and are presets loaded? (y/n)")
skip_tests = False
if is_obs_open != "y":
    skip_tests = True


@skipIf(skip_tests, "OBS is not open")
class Test(TestCase):
    # https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#requests

    def test_update_obs_text_source_value(self):
        response = update_obs_text_source_value(status_text_obs_source_id, "this is a test string!!!")
        self.assertTrue(response.ok())
        # TODO: check if value stored in the obs source is the value that should be there.

    def test_update_obs_video_source_value(self):
        response = update_obs_video_source_value(playing_video_obs_source_id, "video_filepath")
        self.assertTrue(response.ok())
        # TODO: check if value stored in the obs source is the value that should be there.
