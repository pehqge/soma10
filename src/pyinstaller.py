import PyInstaller.__main__
import os

base_path = os.path.abspath(os.path.dirname(__file__))

PyInstaller.__main__.run([
    'main.py',
    '--windowed',
    '--noconsole',
    f'--icon={os.path.join(base_path, "icon.icns")}',
    f'--add-data={os.path.join(base_path, "board.py")}:.',
    f'--add-data={os.path.join(base_path, "card_deck.py")}:.',
    f'--add-data={os.path.join(base_path, "game_controller.py")}:.',
    f'--add-data={os.path.join(base_path, "game_interface.py")}:.',
    f'--add-data={os.path.join(base_path, "interface.py")}:.',
    f'--add-data={os.path.join(base_path, "main_controller.py")}:.',
    f'--add-data={os.path.join(base_path, "menu_interface.py")}:.',
    f'--add-data={os.path.join(base_path, "notification_manager.py")}:.',
    f'--add-data={os.path.join(base_path, "player.py")}:.',
    f'--add-data={os.path.join(base_path, "ui_tools.py")}:.',
    f'--add-data={os.path.join(base_path, "config")}:config',
    f'--add-data={os.path.join(base_path, "dog")}:dog',
    f'--add-data={os.path.join(base_path, "assets")}:assets',
])