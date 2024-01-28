import json
import os
import sys

from PySide6.QtWidgets import QMessageBox


class Config():
    config = None
    config_template_filename = "conf.json.example"
    config_filename = "conf.json"
    default_configuration_loaded = False
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
        file_path = os.path.realpath(os.path.dirname(__file__))
        root_path = os.path.realpath(os.path.dirname(file_path))
        with open(f'{root_path}/{Config.config_filename}', 'w') as f:
            f.write(configuration)

    @staticmethod
    def load_config(use_default_configuration = False, load_previous_conf_if_current_fails = False):
        if use_default_configuration:
            Config.default_configuration_loaded = True
            configuration_file_to_use = Config.config_template_filename
        else:
            configuration_file_to_use = Config.config_filename

        file_path = os.path.realpath(os.path.dirname(__file__))
        root_path = os.path.realpath(os.path.dirname(file_path))

        try:
            with open(f'{root_path}/{configuration_file_to_use}', 'r') as f:
                conf = json.load(f)
        except FileNotFoundError as e:
            if use_default_configuration:
                print(f"Default configuration file not found: {e}. Exiting.")
                sys.exit(1)
            else:
                print(f"Configuration file not found: {e}. Falling back to default example configuration.")
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
                os.mkdir(Config.config['paths'][path])

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
    def get() -> dict:
        if Config.config is None:
            Config.load_config()
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