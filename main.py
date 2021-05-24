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
		self.main_menu=main_scene.MainScene('Pic to Dot &/Monsters', ['Ranking', 'Battle', 'Chara list', 'Chara create'])
		self.match_select_panel=match_select_scene.MainScene(['Random/Rate matching', 'Private/Create room', 'Computer/ '])
		self.image_create_panel=image_create_scene.ImageCreateScene()
		self.image_list_panel=image_list_scene.ImageListScene()
		self.match_panel=match_scene.MatchScene()
		self.local_match_panel=local_match_scene.MatchScene()
		self.online_match_panel=online_match_scene.MatchScene()
		self.ranking_panel=ranking_scene.ImageListScene()
		self.set_texture()
		self.set_edge()
		
		if csv_tools.savedata_reader() == None:
			csv_tools.savedata_writer(uuid.uuid4(), 0)
		
		# BGM
		self.set_bgm()
		self.show_main_menu()
		self.main_bgm.play()
		
	def set_bgm(self):
		self.main_bgm=sound.Player('./music/dont-hero.wav')
		self.main_bgm.number_of_loops=-1
		self.main_bgm.volume=0.3
		self.battle_bgm=sound.Player('./music/cyrf_energy.wav')
		self.battle_bgm.number_of_loops=-1
		self.battle_bgm.volume=0.1
		
	def play_main_bgm(self):
		if not self.main_bgm.playing:
			self.main_bgm.play()
			
	def play_battle_bgm(self):
		if not self.battle_bgm.playing:
			self.battle_bgm.play()
	
	def stop_main_bgm(self):
		if self.main_bgm.playing:
			self.main_bgm.stop()
			
	def stop_battle_bgm(self):
		if self.battle_bgm.playing:
			self.battle_bgm.stop()
		
	def set_texture(self):
		self.main_texture=Texture(image_tools.path_to_UIimage('./image/800x600.jpeg'))
		self.battle_texture = Texture(image_tools.path_to_UIimage('./image/IMG_0274.jpeg'))
		self.black_bg=SpriteNode(color='#000000', size=self.size, position=self.size*0.5, parent=self)
		self.back_ground=SpriteNode(self.main_texture, position=self.size*0.5, parent=self)
		self.set_back_ground_scale()
			
	def set_back_ground_scale(self):
		if self.size.w / self.size.h <= 1334 / 750:		
			#self.back_ground.scale = self.size.w / self.back_ground.size.w
			self.back_ground.scale = self.size.w / 800
		else:
			#self.back_ground.scale = self.size.h / self.back_ground.size.h
			self.back_ground.scale = self.size.h / 600
	
	def did_change_size(self):
		self.black_bg.size=self.size
		self.black_bg.position=self.size*0.5
		self.back_ground.position=self.size*0.5
		self.set_back_ground_scale()
		
		edge_height=(self.back_ground.size.h*self.back_ground.scale)*0.5
		self.up_out_bg.position=(self.size.w*0.5, self.size.h*0.5+edge_height)
		self.up_out_bg.size=(self.size.w, (self.size.h-self.back_ground.size.h)*0.5)
		self.down_out_bg.position=(self.size.w*0.5, self.size.h*0.5-edge_height)
		self.down_out_bg.size=(self.size.w, (self.size.h-self.back_ground.size.h)*0.5)

	def set_edge(self):
		edge_height=(self.back_ground.size.h*self.back_ground.scale)*0.5
		self.up_out_bg=SpriteNode(color='#000000', position=(self.size.w*0.5, self.size.h*0.5+edge_height), anchor_point=(0.5, 0.0), parent=self, size=(self.size.w, self.size.h))
		self.down_out_bg=SpriteNode(color='#000000', position=(self.size.w*0.5, self.size.h*0.5-edge_height), anchor_point=(0.5, 1.0), parent=self, size=(self.size.w, self.size.h))

	def show_main_menu(self):
		self.present_modal_scene(self.main_menu)
			
	def show_match_select_panel(self):
		try:
			if not len(csv_tools.image_data_reader())==0:
				self.present_modal_scene(self.match_select_panel)
			else:
				self.back_main_menu()
				console.alert("No image is available.")
		except:
			pass
		
	def show_ranking_panel(self):
		try:
			if not csv_tools.record_reader('ranking') == 'False':
				self.present_modal_scene(self.ranking_panel)
				self.ranking_panel.load_scene.alpha=1.0
				self.ranking_panel.action_load()
				Thread(target = self.set_ranking, daemon=True).start()
			else:
				console.alert("No data.")
		except:
			pass
	
	def set_ranking(self):
		try:
			if not self.ranking_panel.reset():
				self.back_main_menu()
				console.alert("Not connected to internet.")
			else:	
				self.ranking_panel.set_images()
				self.ranking_panel.action_fade_out()
		except:
			pass
	
	def show_image_create_panel(self):
		self.present_modal_scene(self.image_create_panel)
		self.image_create_panel.reset()
		try:
			if not self.image_create_panel.image_set():
				self.back_main_menu()
				console.alert("Don't select image.")
		except:
			pass
	
	def show_image_list_panel(self):
		try:
			if not len(csv_tools.image_data_reader())==0:
				self.present_modal_scene(self.image_list_panel)
				self.image_list_panel.reset()
			else:
				self.back_main_menu()
				console.alert("No image is available.")
		except:
			pass
	
	def show_match_panel(self):
		Thread(target = self.match_change_panel, args=(self.match_panel,), daemon=True).start()
		
	def match_change_panel(self, match_panel):
		#BGM
		self.stop_main_bgm()
		
		#match_select_panel_暗転
		self.back_ground.texture=None
		
		#macth_panel_明転
		self.present_modal_scene(match_panel)
		match_panel.menu_panel.fade_scene = SpriteNode(color='#000000', size=self.size, position=self.size*0.5,  parent=match_panel.menu_panel, alpha=1.0)
		match_panel.menu_panel.fade_scene.run_action(Action.fade_to(0.0, 0.5))
		match_panel.rematch()
		self.back_ground.texture=self.battle_texture
		self.set_back_ground_scale()
		time.sleep(0.5)
		
			
	def show_local_match_panel(self):
		try: 
			self.present_modal_scene(self.local_match_panel)
			if not self.local_match_panel.rematching():
				self.show_match_select_panel()
				console.alert("Not connected to internet.")
			else:
				self.back_ground.texture=self.battle_texture
				self.set_back_ground_scale()
		except:
			pass
		
	def show_online_match_panel(self):
		try:
			self.present_modal_scene(self.online_match_panel)
			if not self.online_match_panel.rematching():
				self.show_match_select_panel()
				console.alert("Not connected to internet..")
			else:
				self.back_ground.texture=self.battle_texture
				self.set_back_ground_scale()
		except :
			pass
		
	def online_match_change_panel(self, match_panel):
		#BGM
		self.stop_main_bgm()
		
		#match_select_panel_暗転
		self.back_ground.texture=None
		#macth_panel_明転
		self.present_modal_scene(match_panel)
		match_panel.fade_scene = SpriteNode(color='#000000', size=self.size, position=self.size*0.5,  parent=match_panel, alpha=1.0)
		self.back_ground.texture=self.main_texture
		self.set_back_ground_scale()		
		match_panel.fade_scene.run_action(Action.fade_to(0.0, 0.5))
		time.sleep(0.5)
		
		#BGM
		self.play_battle_bgm()
		
	def menu_button_selected(self, title):
		#self.dismiss_modal_scene()
		if title == 'Chara create':
			sound.play_effect('ui:click1', volume=1.0)
			self.show_image_create_panel()
		elif title=='Chara list':
			sound.play_effect('ui:click1', volume=1.0)
			self.show_image_list_panel()
		elif title=='Ranking':		
			sound.play_effect('ui:click1', volume=1.0)
			self.show_ranking_panel()
		elif title=='Battle':		
			sound.play_effect('ui:click1', volume=1.0)
			self.show_match_select_panel()
		elif title=='Computer':
			sound.play_effect('ui:click1', volume=1.0)
			self.show_match_panel()
		elif title=='Private':
			sound.play_effect('ui:click1', volume=1.0)
			self.show_local_match_panel()
		elif title=='Random':
			sound.play_effect('ui:click1', volume=1.0)
			self.show_online_match_panel()
		else:
			pass
			
	def back_main_menu(self):
		sound.play_effect('ui:click1', volume=1.0)
		self.show_main_menu()

	def back_main_from_battle(self):	
		Thread(target = self.thread_back_main_menu, daemon=True).start()
		
	def thread_back_main_menu(self):
		sound.play_effect('ui:click1', volume=1.0)
		
		#明転
		self.show_main_menu()
		self.main_menu.fade_scene = SpriteNode(color='#000000', size=self.size, position=self.size*0.5,  parent=self.main_menu, alpha=1.0)
		self.main_menu.fade_scene.run_action(Action.fade_to(0.0, 0.5))
		self.back_ground.texture=self.main_texture
		self.set_back_ground_scale()
		time.sleep(0.5)
		
		#BGM
		self.play_main_bgm()

# Run the game:
if __name__ == '__main__':
	run(Game(), LANDSCAPE)
