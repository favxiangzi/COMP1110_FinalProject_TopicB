import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class MainModuleTests(unittest.TestCase):
    """Sample test cases for the main route-recommendation workflow.

    Each test below documents the user-facing behavior it protects.
    """

    def setUp(self) -> None:
        main.graph[:] = [[] for _ in range(len(main.STOP_NAMES))]
        main.build_graph()

    def test_build_graph_populates_expected_number_of_edges(self) -> None:
        """Purpose: verify the sample transport graph is built with all routes.

        This checks the graph contains the expected total edge count after setup.
        """
        total_edges = sum(len(edges) for edges in main.graph)
        self.assertEqual(total_edges, 40)

    def test_get_valid_stop_choice_retries_until_valid_input(self) -> None:
        """Purpose: verify invalid stop input is rejected and retried.

        The function should keep prompting until the user enters a valid stop number.
        """
        with patch("builtins.input", side_effect=["abc", "0", "14", "1"]):
            with redirect_stdout(io.StringIO()):
                choice = main.get_valid_stop_choice("Enter choice: ")

        self.assertEqual(choice, 0)

    def test_get_weights_default_selection(self) -> None:
        """Purpose: verify the default weight preset returns the documented values.

        This ensures users who choose option 1 get the standard 35/40/25 split.
        """
        with patch("builtins.input", side_effect=["1"]):
            with redirect_stdout(io.StringIO()):
                weights = main.get_weights()

        self.assertEqual(weights, (35.0, 40.0, 25.0))

    def test_get_weights_custom_selection(self) -> None:
        """Purpose: verify custom valid weights are accepted when they sum to 100.

        This documents the expected behavior for user-entered weight settings.
        """
        with patch("builtins.input", side_effect=["2", "30", "40", "30"]):
            with redirect_stdout(io.StringIO()):
                weights = main.get_weights()

        self.assertEqual(weights, (30.0, 40.0, 30.0))

    def test_compute_z_scores_prefers_better_route(self) -> None:
        """Purpose: verify route ranking prefers the route with better metrics.

        The test uses two sample routes and checks the higher-quality one scores higher.
        """
        preferred = main.Route(
            stops=[0, 1],
            modes=["Walk"],
            totalTime=10,
            totalCost=10,
            adjustedComfort=8,
        )
        slower = main.Route(
            stops=[0, 2],
            modes=["Bus"],
            totalTime=20,
            totalCost=20,
            adjustedComfort=4,
        )

        main.compute_z_scores([preferred, slower], 35, 40, 25)

        self.assertGreater(preferred.zScore, slower.zScore)

    def test_main_handles_same_start_and_destination(self) -> None:
        """Purpose: verify the CLI handles the same start and destination cleanly.

        The program should print the zero-cost/zero-time case instead of failing.
        """
        with patch("builtins.input", side_effect=["1", "1", "1", "n"]):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                main.main()

        output = buffer.getvalue()
        self.assertIn("Starting point and destination are the same.", output)


if __name__ == "__main__":
    unittest.main()
