from unittest.mock import patch
from unittest.mock import MagicMock
import unittest
import shutil
from filecmp import dircmp
import os
import sys
sys.path.append(os.path.abspath(".."))

from src.Main import *

class MainTest(unittest.TestCase):
    TEST_DEST_DIR_TREE = os.path.join("testDestDirTree")
    TEST_SRC_DIR_TREE = os.path.join("testSrcDirTree")
    def tearDown(self) -> None:
        shutil.rmtree(self.TEST_DEST_DIR_TREE)
        os.mkdir(self.TEST_DEST_DIR_TREE)

    def test_should_be_create_mp3filename(self):
        mp4_file_name = "/user/temp/test.mp4"
        dest_directory = "/user/temp/"
        self.assertEqual(create_mp3_file_name(mp4_file_name, dest_directory), "/user/temp/test.mp3")

    @patch("src.Main.subprocess")
    def test_mp4_to_mp3(self, subprocess_stub:MagicMock):
        mp4_to_mp3("/temp/test/test.mp4", "/temp/music/test/")
        command = list(FFMPEG_COMMAND)
        command.extend(["/temp/test/test.mp4", "/temp/music/test/test.mp3"])
        subprocess_stub.run.assert_called_with(command)


    def test_should_be_same_directory_tree_except_mp4(self):
        create_directory_tree(self.TEST_SRC_DIR_TREE, self.TEST_DEST_DIR_TREE, None)
        self.check_should_be_same_directory_tree_without_mp4(self.TEST_SRC_DIR_TREE, self.TEST_DEST_DIR_TREE)

    def test_should_be_same_directory_tree_deep_except_mp4(self):
        create_directory_tree(self.TEST_SRC_DIR_TREE, self.TEST_DEST_DIR_TREE, None)
        self.check_should_be_same_directory_tree_deep_without_mp4(self.TEST_SRC_DIR_TREE, self.TEST_DEST_DIR_TREE)

    def check_should_be_same_directory_tree_deep_without_mp4(self, src_directory_path, dest_directory_path):
        self.check_should_be_same_directory_tree_without_mp4(src_directory_path, dest_directory_path)
        for name in os.listdir(src_directory_path):
            if(os.path.isdir(os.path.join(src_directory_path, name))):
                self.check_should_be_same_directory_tree_deep_without_mp4(os.path.join(src_directory_path, name), os.path.join(dest_directory_path, name))

    def check_should_be_same_directory_tree_without_mp4(self, src_directory_path, dest_directory_path):
        dcmp = dircmp(src_directory_path, dest_directory_path)
        for name in dcmp.left_only:
            self.assertIn("mp4", name)


if __name__ == '__main__':
    unittest.main()
