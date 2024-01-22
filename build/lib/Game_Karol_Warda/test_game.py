"""File used for testing game
"""

import unittest
import Game_Karol_Warda.Constants as Constants
import pygame
import pygame.locals
import subprocess
from time import sleep

class TestGame(unittest.TestCase):
    def test_files(self):
        # test if asstes are loaded
        return self.assertTrue(Constants.ASSET_DICT)
    
    def test_run(self): # smoke test
        pygame.init()
        process = subprocess.Popen(['python', 'Game.py'])
        process.terminate()
        sleep(1)

        process.wait()
        self.assertEqual(process.returncode, 1)
    

if __name__ == "__main__":
    unittest.main()
