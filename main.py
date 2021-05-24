# coding: utf-8

from scene import *
import console
import sound
import uuid
import time
from threading import (Event, Thread)

from Panel import main_scene, image_create_scene, image_list_scene, match_scene, local_match_scene, online_match_scene, match_select_scene, ranking_scene
from Tools import csv_tools, image_tools

class Game(Scene):
	def setup(self):
		self.main_menu = main_scene.MainScene('Pic to Dot &/Monsters', ['Ranking', 'Battle', 'Chara list', 'Chara create'])
		self.match_select_panel = match_select_scene.MainScene(['Random/Rate matching', 'Private/Create room', 'Computer/ '])
		self.image_create_panel = image_create_scene.ImageCreateScene()
		self.image_list_panel = image_list_scene.ImageListScene()
		self.match_panel = match_scene.MatchScene()
		self.local_match_panel = local_match_scene.MatchScene()
		self.online_match_panel = online_match_scene.MatchScene()
		self.ranking_panel = ranking_scene.ImageListScene()

# Run the game:
if __name__ == '__main__':
	run(Game(), LANDSCAPE)
