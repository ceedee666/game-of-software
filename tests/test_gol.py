import unittest

import src.gol as gol


class TestGol(unittest.TestCase):
    def setUp(self):
        self.width = 4
        self.hight = 6
        self.g = gol.init_grid(self.width, self.hight)

    def test_init_grid(self):
        self.assertEqual(
            len(self.g), self.hight, f"The grid should have {self.hight} rows."
        )
        self.assertEqual(
            len(self.g[0]), self.width, f"The grid should have {self.width} columns."
        )
        self.assertFalse(
            any([any(line) for line in self.g]), "All cells should be dead."
        )

    def test_randomize(self):
        self.g = gol.randomize(self.g)
        self.assertTrue(
            any([any(line) for line in self.g]),
            "After randomizing, there should be alive cells in the grid.",
        )

    def test_neighbors(self):
        self.assertEqual(
            len(gol.neighbours(0, 0, self.g)),
            3,
            "The cell at Pos (0,0) should have 3 neighbors.",
        )
        self.assertEqual(
            len(gol.neighbours(1, 1, self.g)),
            8,
            "The cell at Pos (1,1) should have 3 neighbors.",
        )
        self.assertEqual(
            len(gol.neighbours(0, 1, self.g)),
            5,
            "The cell at Pos (0,1) should have 5 neighbors.",
        )

    def test_init_with_pattern(self):
        self.width = 10
        self.hight = 10

        self.g = gol.init_grid(self.width, self.hight)
        self.g = gol.init_with_pattern("glider", self.g)
        self.assertEqual(
            sum([sum(line) for line in self.g]),
            5,
            "After initializing the glider, there should be 5 alive cells.",
        )

        self.g = gol.init_grid(self.width, self.hight)
        self.g = gol.init_with_pattern("eight", self.g)
        self.assertEqual(
            sum([sum(line) for line in self.g]),
            12,
            "After initializing the eight, there should be 12 alive cells.",
        )

    def test_next_generation(self):
        # Test one cell
        self.g[0][0] = True
        self.g = gol.next_generation(self.g)
        self.assertFalse(
            any([any(line) for line in self.g]),
            "All cells should be dead.",
        )

        # Test blinker
        self.g = gol.init_grid(3, 3)
        self.g[0][1] = True
        self.g[1][1] = True
        self.g[2][1] = True

        self.g = gol.next_generation(self.g)
        self.assertEqual(
            sum([sum(line) for line in self.g]),
            3,
            "After one generation, there should be 3 alive cells.",
        )
        self.assertTrue(self.g[1][0], "Cell at (1,0) should be alive.")
        self.assertTrue(self.g[1][1], "Cell at (1,1) should be alive.")
        self.assertTrue(self.g[1][2], "Cell at (1,2) should be alive.")

        self.g = gol.next_generation(self.g)
        self.assertEqual(
            sum([sum(line) for line in self.g]),
            3,
            "After two generation, there should be 3 alive cells.",
        )
        self.assertTrue(self.g[0][1], "Cell at (0,1) should be alive.")
        self.assertTrue(self.g[1][1], "Cell at (1,1) should be alive.")
        self.assertTrue(self.g[2][1], "Cell at (2,1) should be alive.")


if __name__ == "__main__":
    unittest.main()
