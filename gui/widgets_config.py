
import os, json, pygame
import tkinter as tk
from paths import *
from tkinter import filedialog
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from mutagen import File
from kivy.clock import Clock

def resource_path(relative_path):
    import sys
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

# Main Interface Class
class MainLayout(FloatLayout):
    _bgDeviceImage = BG_DEVICE_IMAGE
    _play_normal = StringProperty(BT_PLAY_IMAGE)
    _play_down = StringProperty(BT_PLAY_DOWN_IMAGE)
    _pause_normal = StringProperty(BT_PAUSE_IMAGE)
    _pause_down = StringProperty(BT_PAUSE_DOWN_IMAGE)
    _current_normal = StringProperty()
    _current_down = StringProperty()
    _btNextmImage = BT_NEXT_IMAGE
    _btNextmDownImage = BT_NEXT_DOWN_IMAGE
    _btPrevmImage = BT_PREVM_IMAGE
    _btPrevmDownImage = BT_PREVM_DOWN_IMAGE
    _btFolderImage = BT_FOLDER_IMAGE
    _btFolderDownImage = BT_FOLDER_DOWN_IMAGE
    _btRepeatImage = BT_REPEAT_IMAGE
    _btRepeatDownImage = BT_REPEAT_DOWN_IMAGE
    _imgLpImage = IMG_LP_IMAGE
    _imgNoCoverImage = IMG_NOCOVER_IMAGE
    _imgCoverBorderImage = IMG_COVERBORDER_IMAGE
    _imgBarThumbImage = IMG_BARTHUMB_IMAGE
    _coverFolder = COVER_DIR
    _musicFolder = MUSIC_DIR
    _musicList = [os.path.join(MUSIC_DIR, file) for file in os.listdir(MUSIC_DIR) if file.lower().endswith(('.mp3', '.ogg', '.wav'))]
    _d_path = resource_path(os.path.join('gui', 'default_path.json'))
    vinyl_angle = NumericProperty(0)

    def __init__(self, **kwargs):
        self._is_paused = True
        super().__init__(**kwargs)
        if os.path.exists(self._d_path):
            with open(self._d_path, 'r') as f:
                data = json.load(f)
                self._musicFolder = data.get('default_path', MUSIC_DIR)
        else:
            self._musicFolder = MUSIC_DIR
        self._musicList = [os.path.join(self._musicFolder, file)
                           for file in os.listdir(self._musicFolder)
                           if file.lower().endswith(('.mp3', '.ogg', '.wav'))]
        self.update_button_images()
        self._vinyl_anim = None
        pygame.mixer.init()
        self._current_music = ''
        self._user_dragging_slider = False
        self._music_start_time = 0
        self._repeat = False
        self._seek_offset = 0
        self._current_index = 0
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        Clock.schedule_interval(self.check_music_end, 0.1)
        Clock.schedule_interval(self.update_progress_bar, 1 / 2)
        Clock.schedule_once(self._set_filechooser_path, 0.5)

    # Function to set default music path
    def _set_filechooser_path(self, *args):
        try:
            if 'filechooser' in self.ids:
                self.ids.filechooser.path = self._musicFolder
        except Exception as e:
            pass

    # Function to toggle music loop feature
    def toggle_repeat(self, state):
        self._repeat = state == 'down'

    def check_music_end(self, dt):
        if not pygame.mixer.music.get_busy():
            if self._current_music and not self._is_paused:
                if self._repeat:
                    pygame.mixer.music.play()
                    self._seek_offset = 0
                    self._music_start_time = pygame.time.get_ticks() / 1000
                    self.ids.progress_bar.value = 0
                else:
                    self.next_music(1)

    def update_progress_bar(self, dt):
        if not self._user_dragging_slider:
            if pygame.mixer.music.get_busy():
                pos_ms = pygame.mixer.music.get_pos()
                if pos_ms == -1:
                    current_time = 0
                else:
                    current_time = (pos_ms / 1000.0) + self._seek_offset
                self.ids.progress_bar.value = current_time
            else:
                pass

    # Volume change function
    def on_volume_change(self, slider, value):
        adjusted_volume = value ** 3
        pygame.mixer.music.set_volume(adjusted_volume)

    # Vinyl animation functions
    def start_vinyl_rotation(self):
        if not self._vinyl_anim:
            self._vinyl_anim = Clock.schedule_interval(self.rotate_vinyl, 1/60)
    def stop_vinyl_rotation(self):
        if self._vinyl_anim:
            self._vinyl_anim.cancel()
            self._vinyl_anim = None
    def rotate_vinyl(self, dt):
        self.vinyl_angle = (self.vinyl_angle + 1) % 360

    # Function that return album name from a music file metadata
    @staticmethod
    def get_album(filepath):
        try:
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.mp3':
                audio = MP3(filepath, ID3=ID3)
                album = audio.get('TALB')
                if album:
                    return album.text[0]
            elif ext == '.ogg':
                audio = OggVorbis(filepath)
                album = audio.get('album')
                if album:
                    return album[0]
            elif ext == '.wav':
                audio = WAVE(filepath)
                album = audio.get('TALB') or audio.get('album')
                if album:
                    return album[0] if isinstance(album, list) else album
            else:
                audio = File(filepath)
                if audio:
                    album = audio.get('TALB') or audio.get('album')
                    if album:
                        return album[0] if isinstance(album, list) else album
            return "Álbum não encontrado"
        except Exception as e:
            return f"Error: {e}"

    # fuctions to set current music cover
    def set_cover(self, album_name):
        for cover_file in os.listdir(self._coverFolder):
            cover_name_no_ext = os.path.splitext(cover_file)[0]
            if album_name.lower() == cover_name_no_ext.lower():
                full_path = os.path.join(self._coverFolder, cover_file)
                self.ids.album_cover.source = full_path
                return
        self.ids.album_cover.source = 'assets/capas/default.jpg'
    def music_selected_cover(self, filepath):
        album_name = self.get_album(filepath)
        self.set_cover(album_name)

    # Function to update play/puse button images
    def update_button_images(self):
        if self._is_paused:
            self._current_normal = self._play_normal
            self._current_down = self._play_down
        else:
            self._current_normal = self._pause_normal
            self._current_down = self._pause_down
        self.ids.play_pause_button.canvas.ask_update()

    # Filechooser Select function
    def file_select(self, filechooser, selection):
        self._musicList = [
            os.path.join(self.ids.filechooser.path, file)
            for file in os.listdir(self.ids.filechooser.path)
            if file.lower().endswith(('.mp3', '.ogg', '.wav'))]
        if not selection:
            return
        selected_file = selection[0]
        if selected_file != self._current_music:
            for index, file in enumerate(self._musicList):
                if file == selected_file:
                    self._current_music = file
                    self._current_index = index
                    break
            pygame.mixer.music.stop()
            self._is_paused = False
            pygame.mixer.music.load(self._current_music)
            try:
                audio = MP3(self._current_music)
                duration = audio.info.length
                self.ids.progress_bar.max = duration
            except:
                self.ids.progress_bar.max = 1
            self.ids.progress_bar.value = 0
            self._seek_offset = 0
            self._music_start_time = pygame.time.get_ticks() / 1000
            pygame.mixer.music.play()
            self.start_vinyl_rotation()
            self.update_button_images()
            self.music_selected_cover(self._current_music)

    # Time slider interaction functions
    def on_seek_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self._user_dragging_slider = False
            new_time = instance.value
            try:
                pygame.mixer.music.play(start=new_time)
                if self._is_paused:
                    pygame.mixer.music.pause()
                self._seek_offset = new_time
                self._music_start_time = pygame.time.get_ticks() / 1000
            except Exception as e:
                pass
    def on_seek_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self._user_dragging_slider = True
    def on_play_button_down(self):
        self.ids.play_pause_button.canvas.ask_update()

    # Play/pause music function, used by play button in .kv file 
    def play_music(self):
        if not self._current_music:
            return
        if self._is_paused:
            pygame.mixer.music.unpause()
            self._is_paused = False
        else:
            pygame.mixer.music.pause()
            self._is_paused = True
        if self._is_paused:
            self.stop_vinyl_rotation()
        else:
            self.start_vinyl_rotation()
        self.update_button_images()
        self.music_selected_cover(self._current_music)

    # Function to skip the current music, previous or next is set in 'note: int'
    def next_music(self, mode: int):
        if self._repeat:
            pygame.mixer.music.play()
            self._seek_offset = 0
            self._music_start_time = pygame.time.get_ticks() / 1000
            self.ids.progress_bar.value = 0
            return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        if mode == 1:
            self._current_index += 1
            if self._current_index >= len(self._musicList):
                self._current_index = 0
        else:
            self._current_index -= 1
            if self._current_index < 0:
                self._current_index = len(self._musicList) - 1
        self._current_music = self._musicList[self._current_index]
        try:
            filechooser = self.ids.filechooser
            filechooser.selection = [self._current_music]
            filechooser._update_files()
        except Exception as e:
            pass
        try:
            pygame.mixer.music.load(self._current_music)
            pygame.mixer.music.play()
            self._is_paused = False
        except Exception as e:
            ...
        self.ids.progress_bar.value = 0
        try:
            audio = MP3(self._current_music)
            self.ids.progress_bar.max = audio.info.length
        except:
            self.ids.progress_bar.max = 1
        self.music_selected_cover(self._current_music)
        self._seek_offset = 0
        self._music_start_time = pygame.time.get_ticks() / 1000
        self.start_vinyl_rotation()
        self.update_button_images()

    # Function to set default path
    def set_defaut_path(self):
        root = tk.Tk()
        root.withdraw()
        temp_path = filedialog.askdirectory()
        if temp_path:
            self._musicFolder = temp_path
            self._musicList = [os.path.join(self._musicFolder, file)
                            for file in os.listdir(self._musicFolder)
                            if file.lower().endswith(('.mp3', '.ogg', '.wav'))]
            self.ids.filechooser.path = self._musicFolder
            user_config_dir = os.path.join(os.path.expanduser('~'), '.minimalyst')
            os.makedirs(user_config_dir, exist_ok=True)
            json_save_path = os.path.join(user_config_dir, 'default_path.json')
            with open(json_save_path, 'w') as f:
                json.dump({'default_path': self._musicFolder}, f)