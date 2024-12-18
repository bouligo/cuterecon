import json
import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QMessageBox


class Config():
    config = None
    config_template_filename = "conf.json.example"
    config_filename = "conf.json"
    config_root_path = ""
    default_configuration_loaded = False
    default_configuration = {  # Contains default options that might be missing from existing user configurations
        'user_prefs' :  {'monospaced_fonts': 'Hack, DejaVu Sans Mono, Droid Sans Mono, Courier, Monospace Regular'},
        'screenshots': {"engine": "qt", "interval" : 15, "dst_folder" : "/home/user/Images/", "work_folder" : "/tmp/", "pixel_threshold_different_images" : 500, "check_locked_screen": True, "check_locked_screen_cmd" : "dbus-send --session --dest=org.freedesktop.ScreenSaver --type=method_call --print-reply --reply-timeout=20000 /org/freedesktop/ScreenSaver org.freedesktop.ScreenSaver.GetActive", "check_locked_screen_cmd_result" : "boolean true", "screenshot_cmd" : "/usr/bin/spectacle -nfb -o %%%OUTPUT%%%", "ignore_if_active_window": True, "convert_png_to_jpg" : True, "include_processes" : True, "include_ocr" : False, "processes_blacklist" : ["systemd", "kthreadd", "dbus-send", "Xorg", "sddm-helper", "(sd-pam)", "startplasma-x11", "dbus-daemon", "xdg-desktop-portal", "xdg-document-portal", "xdg-permission-store", "fusermount3", "ksmserver", "kded5", "kwin_x11", "kglobalaccel5", "dconf-service", "plasmashell", "kactivitymanagerd", "gmenudbusmenuproxy", "polkit-kde-authentication-agent-1", "at-spi-bus-launcher", "plasma-browser-integration-host", "Socket Process", "Privileged Cont", "WebExtensions", "Utility Process", "plasma-browser-integration-host", "zsh", "script", "Isolated Web Co", "smbnotifier", "kioslave5", "vim", "agent", "yakuake", "kscreen_backend_launcher", "xdg-desktop-portal-kde", "org_kde_powerdevil", "pulseaudio", "kaccess", "pipewire", "keepassxc", "DiscoverNotifier", "kiod5", "chrome_crashpad_handler", "Web Content", "kio-fuse", "dolphin", "obexd", "wireplumber", "xembedsniproxy", "gsettings-helper", "chromium", "signal-desktop", "Discord", "electron", "fsnotifier", "RDD Process"], "processes_ppid_blacklist" : [1, 2]},
        'nmap_options': {'ports': "T:-,U:53,161,631", 'type': "-sS", 'speed': "-T3", 'additional_args': "-v --min-rate 500", 'skip_host_discovery': False, 'version_probing': True, 'default_scripts': True, 'os_detection': True, 'tcp_and_udp': True}
    }
    conf_structure = {
        "paths": {
            "nmap_output_dir": str
        },
        "core_binaries": {
            "nmap": {
                "binary": str,
                "args": list
            },
            "terminal": {
                "binary": str,
                "args": list
            },
            "graphical_su": {
                "binary": str,
                "args": list
            }
        },
        "user_binaries": dict,
        "ports_associations": dict,
        "autorun": dict,
        "user_prefs": {
            "enable_autorun": bool,
            "enable_autorun_on_xml_import": bool,
            "confirm_before_tab_removal": bool,
            "dev_null_as_stdin": bool,
            "remove_nmap_xml_files_after_scan": bool,
            "delete_logs_on_save": bool,
            "autosave": bool,
            "autosave_interval": int,
            "preferred_interfaces": list,
            "preferred_lport": int
        },
        "user_variables": dict
    }

    @staticmethod
    def save_config():
        configuration = json.dumps(Config.config, indent=4)
        with open(f'{Config.config_root_path}/{Config.config_filename}', 'w') as f:
            f.write(configuration)

    @staticmethod
    def load_config(use_default_configuration = False, load_previous_conf_if_current_fails = False):
        if (value := os.environ.get("XDG_CONFIG_HOME")) and (path := Path(value)).is_absolute():  # Checking if XDG_CONFIG_HOME exists
            root_config_folder = path / "qtrecon"
        else:
            root_config_folder = Path.home() / ".config/qtrecon"
        Config.config_root_path = root_config_folder

        if use_default_configuration:
            Config.default_configuration_loaded = True
            configuration_file_to_use = Config.config_template_filename
            root_config_folder = os.path.realpath(os.path.dirname(os.path.realpath(os.path.dirname(__file__))))  # Taking default lconfig file next to binary
        else:
            configuration_file_to_use = Config.config_filename

        if not os.path.isdir(Config.config_root_path) and os.path.isfile(Config.config_root_path):
            os.remove(Config.config_root_path)
        try:
            os.mkdir(Config.config_root_path)
        except FileExistsError:
            pass

        try:
            with open(f'{root_config_folder}/{configuration_file_to_use}', 'r') as f:
                conf = json.load(f)
        except FileNotFoundError as e:
            if use_default_configuration:
                print(f"Default configuration file not found: {e}. Exiting.")
                sys.exit(1)
            else:
                print(f"Configuration file not found: {e}. Falling back to default example configuration, and creating a new configuration file in {root_config_folder}/{configuration_file_to_use}.")
                Config.load_config(use_default_configuration = True)
                return
        except json.decoder.JSONDecodeError as e:
            QMessageBox.information(None, "Error while parsing configuration file", f"Invalid configuration file: {e}")
            if not load_previous_conf_if_current_fails:
                sys.exit(2)
            else:
                return

        if Config.check_config_structure(Config.conf_structure, conf):
            Config.config = conf
        else:
            print("The configuration is a valid json, but the data inside has an unexpected format or is missing mandatory options.")
            if not load_previous_conf_if_current_fails:
                sys.exit(3)

        # Creating non-existant paths
        for path in Config.config['paths']:
            if os.access(Config.config['paths'][path], os.F_OK): # Check for existence
                if os.path.isdir(Config.config['paths'][path]):
                    if not os.access(Config.config['paths'][path], os.R_OK) or \
                    not os.access(Config.config['paths'][path], os.W_OK) or \
                    not os.access(Config.config['paths'][path], os.X_OK):
                        print(f"Work folder {Config.config['paths'][path]} doesn't have proper rights (RWX) for current user.")
                        sys.exit(4)
                else:
                    print(f"Work folder {Config.config['paths'][path]} already exists as a file on this filesystem. Delete it or specify another path in the configuration.")
                    sys.exit(5)
            else:
                try:
                    os.mkdir(Config.config['paths'][path])
                except FileExistsError:
                    pass
                except PermissionError:
                    print(f"Work folder {Config.config['paths'][path]} doesn't exist on this filesystem and cannot be created (permission issue). Specify another path in the configuration.")
                    sys.exit(6)

    @staticmethod
    def check_binaries() -> dict:
        ret = {'not_found': [], 'not_executable': []}
        for binary_type in ['core_binaries', 'user_binaries']:
            for binary in Config.config[binary_type]:
                if not os.path.isfile(Config.config[binary_type][binary]['binary']):
                    ret['not_found'].append(Config.config[binary_type][binary]['binary'])
                elif not os.access(Config.config[binary_type][binary]['binary'], os.X_OK):
                    ret['not_executable'].append(Config.config[binary_type][binary]['binary'])
        return ret

    @staticmethod
    def get() -> dict:  # Todo: add default values when not specified in the loaded configuration
        if Config.config is None:
            Config.load_config()

        for first_level_key in Config.default_configuration:
            if first_level_key not in Config.config.keys():
                Config.config[first_level_key] = Config.default_configuration[first_level_key]
            else:
                for key in Config.default_configuration[first_level_key].keys():
                    if key not in Config.config[first_level_key].keys():
                        Config.config[first_level_key][key] = Config.default_configuration[first_level_key][key]

        return Config.config

    @staticmethod
    def set(keys: list, value):
        if Config.config is None:
            Config.load_config()

        current_node = Config.config
        for key in keys:
            if type(current_node[key]) == dict:
                current_node = current_node[key]
            else:
                current_node[key] = value

    @staticmethod
    def check_config_structure(structure: dict, config: dict) -> bool:
        if isinstance(structure, dict) and isinstance(config, dict):
            # struct is a dict of types or other dicts
            # print(structure, config)
            return all(k in config and Config.check_config_structure(structure[k], config[k]) for k in structure)
        if isinstance(structure, list) and isinstance(config, list):
            # struct is list in the form [type or dict]
            # print(structure, config)
            return all(Config.check_config_structure(structure[0], c) for c in structure)
        elif isinstance(structure, type):
            # struct is the type of conf
            # print(structure, config)
            return isinstance(config, structure)
        else:
            # struct is neither a dict, nor list, not type
            return False