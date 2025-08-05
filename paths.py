import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sub-Directories
UI_DIR = os.path.join(BASE_DIR, 'gui')
RES_DIR = os.path.join(BASE_DIR, 'resource')
IMG_DIR = os.path.join(RES_DIR, 'img')
COVER_DIR = os.path.join(RES_DIR, 'covers')
MUSIC_DIR = os.path.join(BASE_DIR, 'default_library')

# .kv Files
MAIN_KV = os.path.join(UI_DIR, 'minimalyst.kv')

## Graphics
# Background
BG_DEVICE_IMAGE = os.path.join(IMG_DIR, 'bg_device_image.png')
# Images
IMG_LP_IMAGE = os.path.join(IMG_DIR, 'img_lp.png')
IMG_NOCOVER_IMAGE = os.path.join(IMG_DIR, 'img_nocover.png')
IMG_COVERBORDER_IMAGE = os.path.join(IMG_DIR, 'img_coverborder.png')
IMG_BARTHUMB_IMAGE = os.path.join(IMG_DIR, 'img_barthumb.png')
# # Button Images
BT_PLAY_IMAGE = os.path.join(IMG_DIR, 'bt_playpause.png')
BT_PLAY_DOWN_IMAGE = os.path.join(IMG_DIR, 'bt_playpause_down.png')
BT_PAUSE_IMAGE = os.path.join(IMG_DIR, 'bt_pause.png')
BT_PAUSE_DOWN_IMAGE = os.path.join(IMG_DIR, 'bt_pause_down.png')
BT_NEXT_IMAGE = os.path.join(IMG_DIR, 'bt_nextm.png')
BT_NEXT_DOWN_IMAGE = os.path.join(IMG_DIR, 'bt_nextm_down.png')
BT_PREVM_IMAGE = os.path.join(IMG_DIR, 'bt_prevm.png')
BT_PREVM_DOWN_IMAGE = os.path.join(IMG_DIR, 'bt_prevm_down.png')
BT_FOLDER_IMAGE = os.path.join(IMG_DIR, 'bt_folder.png')
BT_FOLDER_DOWN_IMAGE = os.path.join(IMG_DIR, 'bt_folder_down.png')
BT_REPEAT_IMAGE = os.path.join(IMG_DIR, 'bt_repeat.png')
BT_REPEAT_DOWN_IMAGE = os.path.join(IMG_DIR, 'bt_repeat_down.png')