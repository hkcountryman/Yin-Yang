import json
import unittest
from os import rename
from os.path import isfile
from pathlib import Path
from shutil import copyfile
from src import config

config_path = f"{Path.home()}/.config/yin_yang/yin_yang.json"


class ConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # if there already exists a backup, its likely because a test in failed in the past
        # do not override that backup
        if not isfile(config_path + 'yin_yang_backup.json'):
            # make a backup of the currently used config file
            copyfile(config_path, config_path.replace("yin_yang.json", "yin_yang_backup.json"))

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        # override the config file with the backup so that
        # these tests do not override the users preferences
        rename(config_path.replace("yin_yang.json", "yin_yang_backup.json"), config_path)

    def test_update_old_configs(self):
        desktops = ['kde', 'gtk', 'else']
        config_v2_1 = {
            "version": 2.1,
            "followSun": False,
            "latitude": "",
            "longitude": "",
            "schedule": False,
            "switchToDark": "20:0",
            "switchToLight": "7:0",
            "running": False,
            "theme": "",
            # "codeLightTheme": "Default Light+",
            # "codeDarkTheme": "Default Dark+",
            # "codeEnabled": False,
            "kdeLightTheme": "org.kde.breeze.desktop",
            "kdeDarkTheme": "org.kde.breezedark.desktop",
            "kdeEnabled": False,
            "gtkLightTheme": "",
            "gtkDarkTheme": "",
            "atomLightTheme": "",
            "atomDarkTheme": "",
            "atomEnabled": False,
            "gtkEnabled": False,
            "wallpaperLightTheme": "",
            "wallpaperDarkTheme": "",
            "wallpaperEnabled": False,
            "firefoxEnabled": False,
            "firefoxDarkTheme": "firefox-compact-dark@mozilla.org",
            "firefoxLightTheme": "firefox-compact-light@mozilla.org",
            "firefoxActiveTheme": "firefox-compact-light@mozilla.org",
            "gnomeEnabled": False,
            "gnomeLightTheme": "",
            "gnomeDarkTheme": "",
            "kvantumEnabled": False,
            "kvantumLightTheme": "",
            "kvantumDarkTheme": "",
            "soundEnabled": False,
            "test": True  # this is used for verification purpose
        }

        for desktop in desktops:
            config_v2_1["desktop"] = desktop

            with self.subTest('Updating the config should apply correct themes to the system plugin',
                              desktop=desktop):
                with open(config_path, "w+") as file:
                    json.dump(config_v2_1, file)

                config.load_config()

                # check that the correct config is loaded, not an actual unittest
                assert config.config["test"]

                plugin = 'kde' if desktop == 'kde' else 'gnome'
                settings = [
                    'Enabled',
                    'LightTheme',
                    'DarkTheme'
                ]
                for value in settings:
                    self.assertEqual(config_v2_1[plugin + value], config.config['system' + value],
                                     'Updating old config files should apply correct values')


if __name__ == '__main__':
    unittest.main()
