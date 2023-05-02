import inspect
import unittest
from unittest import TestCase, skip
from multiprocessing import Pipe

from bertha2.settings import visuals_nonempty_queue_header_message, visuals_empty_queue_next_up_message
from bertha2.visuals import *

if __name__ == '__main__':
    unittest.main()


class TestVisualsStatelessFunctions(TestCase):
    def test_process_title(self):
        self.assertEqual("I can't ****ing believe this is happening,...", process_title(
            "I can't fucking believe this is happening, what the fuck is wrong with people these days?"))
        self.assertEqual("What the **** did you just ****ing say abo...", process_title(
            "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals..."))
        self.assertEqual("This is such a ****ing waste of my time, I...", process_title(
            "This is such a fucking waste of my time, I have better things to do than deal with this bullshit."))

    @skip("undeveloped test case")
    def test_create_playing_next_string(self):

        # TODO: add a test case for new "is_video_currently_playing" flag in state

        queued_video_titles_case_1 = [
            "10 Surprising Facts About the Universe",
            "Cooking Tutorial: How to Make Delicious Brownies",
            "Exploring Abandoned Places: Haunted Mansion",
            "My Fitness Journey: How I Lost 20 Pounds in 2 Months",
            "Interview with a Celebrity: Behind the Scenes",
            "10 Life Hacks Everyone Should Know",
            "Travel Vlog: Exploring the Streets of Tokyo",
            "DIY Home Decor: How to Upcycle Old Furniture",
            "Top 5 Best Movies of the Year So Far",
            "Reacting to TikTok Trends: Hilarious Compilation"
        ]

        # INFO: inspect.cleandoc is needed to strip the indentation from the default python multiline string implementation
        expected_output_case_1 = inspect.cleandoc(f"""
        {visuals_nonempty_queue_header_message}
        1. Cooking Tutorial: How to Make Delicious Br...
        2. Exploring Abandoned Places: Haunted Mansion
        3. My Fitness Journey: How I Lost 20 Pounds i...
        4. Interview with a Celebrity: Behind the Scenes
        5 more video(s) queued...""")


        queued_video_titles_case_2 = []

        expected_output_case_2 = inspect.cleandoc(f"""
        {visuals_nonempty_queue_header_message}
        {visuals_empty_queue_next_up_message}
        """)

        self.assertEqual(expected_output_case_1, create_playing_next_string(queued_video_titles_case_1))
        self.assertEqual(expected_output_case_2, create_playing_next_string(queued_video_titles_case_2))

    @skip("undeveloped test case")
    def test_update_status_text(self):
        self.fail()

    @skip("undeveloped test case")
    def test_update_onscreen_visuals_from_state(self):
        self.fail()

    @skip("undeveloped test case")
    def test_update_visuals_state_with_new_video(self):
        self.fail()

    @skip("this is already tested")
    def test_update_visuals_state_with_new_bertha_status(self):
        self.fail()

@skip("fix state management")
class TestUpdateStatusText1(TestCase):
    # initialize_visuals_state()
    global visuals_state
    visuals_state = default_visuals_state
    print(default_visuals_state)

    def test_update_status_text_cooldown(self):
        visuals_state["is_bertha_on_cooldown"] = True
        print(visuals_state["currently_displayed_status_text"])
        update_status_text()
        print(visuals_state["currently_displayed_status_text"])
        # self.assertEqual()

@skip("fix state management")
class TestUpdateStatusText2(TestCase):
    global visuals_state
    visuals_state = default_visuals_state
    print(default_visuals_state)
    def test_update_status_text_empty_queue(self):
        print(f'testing {visuals_state["currently_displayed_status_text"]}')
        # update_status_text()

@skip("fix state management")
class TestUpdateStatusText3(TestCase):
    @skip("undeveloped test case")
    def test_update_status_text_nonempty_queue(self):
        update_status_text()


@skip("fix state management")
class TestUpdatePlayingNext(TestCase):
    global visuals_state
    visuals_state = default_visuals_state

    @skip("undeveloped test case")
    def test_update_playing_next(self):
        self.fail()

@skip("fix state management")
class TestVisualsStates1(TestCase):
    global visuals_state
    visuals_state = default_visuals_state
    def test_visuals_process_loop_state(self):
        # this test case tests that state is what it should be after each switch in hardware

        # TODO: these are horrible names.
        cv_parent_conn, cv_child_conn = Pipe()
        hv_child_conn, hv_parent_conn = Pipe()

        # initialize onscreen visuals
        print(visuals_state)
        update_onscreen_visuals_from_state()
        print(visuals_state)

        # add new converted video
        cv_parent_conn.send({
            "title": "some random youtube video title",
            "filepath": f"not/real/filepath",
        })

        visuals_process_loop([cv_child_conn, hv_child_conn])
        print(visuals_state)
        self.assertEqual(1, len(visuals_state["queued_video_metadata_objects"]))

        hv_parent_conn.send("playing")
        visuals_process_loop([cv_child_conn, hv_child_conn])
        print(visuals_state)
        self.assertEqual(True, visuals_state["is_video_currently_playing"])
        self.assertEqual(False, visuals_state["is_bertha_on_cooldown"])
        self.assertEqual("not/real/filepath", visuals_state["currently_playing_video_path"])

        hv_parent_conn.send("cooldown")
        visuals_process_loop([cv_child_conn, hv_child_conn])
        print(visuals_state)
        self.assertEqual(False, visuals_state["is_video_currently_playing"])
        self.assertEqual(True, visuals_state["is_bertha_on_cooldown"])
        self.assertEqual("", visuals_state["currently_playing_video_path"])

        hv_parent_conn.send("waiting")
        visuals_process_loop([cv_child_conn, hv_child_conn])
        print(visuals_state)
        self.assertEqual(False, visuals_state["is_video_currently_playing"])
        self.assertEqual(False, visuals_state["is_bertha_on_cooldown"])
        self.assertEqual("", visuals_state["currently_playing_video_path"])

@skip("fix state management")
class TestVisualsStates2(TestCase):
    visuals_state = default_visuals_state
    def test_visuals_process_loop_converter(self):

        # TODO: these are horrible names.
        cv_parent_conn, cv_child_conn = Pipe()
        hv_child_conn, hv_parent_conn = Pipe()

        # initialize onscreen visuals
        update_onscreen_visuals_from_state()

        n = 500

        for i in range(n):
            cv_parent_conn.send({
                "title": "some random youtube video title",
                "filepath": f"not/real/filepath",
            })
            visuals_process_loop([cv_child_conn, hv_child_conn])

        self.assertEqual(n, len(visuals_state["queued_video_metadata_objects"]))