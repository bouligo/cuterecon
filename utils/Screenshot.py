#!/bin/env python3

import subprocess
import time
import os
from datetime import datetime
from PIL import Image, ImageChops
import sqlite3
import psutil
import sys


# Change me if running in standalone!
engine = "external" # external or qt
interval = 15 # in secs
dst_folder = "/home/bouligo/Images/" # Dest folder to store the compressed archive with all screenshots
work_folder = "/tmp/"
pixel_threshold_different_images = 500
check_locked_screen = True
check_locked_screen_cmd = "dbus-send --session --dest=org.freedesktop.ScreenSaver --type=method_call --print-reply --reply-timeout=20000 /org/freedesktop/ScreenSaver org.freedesktop.ScreenSaver.GetActive"
check_locked_screen_cmd_result = "boolean true"
screenshot_cmd = 'spectacle -nfb -o %%%OUTPUT%%%' # %%%OUTPUT%%% will be replaced with the correct path and filename
convert_png_to_jpg = True # If the capture tool only saves as png, convert to jpg immediately
include_processes = True
include_ocr = False
processes_blacklist = ['systemd', 'kthreadd', 'dbus-send', 'Xorg', 'sddm-helper', '(sd-pam)', 'startplasma-x11', 'dbus-daemon', 'xdg-desktop-portal', 'xdg-document-portal', 'xdg-permission-store', 'fusermount3', 'ksmserver', 'kded5', 'kwin_x11', 'kglobalaccel5', 'dconf-service', 'plasmashell', 'kactivitymanagerd', 'gmenudbusmenuproxy', 'polkit-kde-authentication-agent-1', 'at-spi-bus-launcher', 'plasma-browser-integration-host', 'Socket Process', 'Privileged Cont', 'WebExtensions', 'Utility Process', 'plasma-browser-integration-host', 'zsh', 'script', 'Isolated Web Co', 'smbnotifier', 'kioslave5', 'vim', 'agent', 'yakuake', 'kscreen_backend_launcher', 'xdg-desktop-portal-kde', 'org_kde_powerdevil', 'pulseaudio', 'kaccess', 'pipewire', 'keepassxc', 'DiscoverNotifier', 'kiod5', 'chrome_crashpad_handler', 'Web Content', 'kio-fuse', 'dolphin', 'obexd', 'wireplumber', 'xembedsniproxy', 'gsettings-helper', 'chromium', 'signal-desktop', 'Discord', 'electron', 'fsnotifier', 'RDD Process']
processes_ppid_blacklist = [1, 2]


# Functions
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


class Screenshot:
    previous_screenshots = []
    nb_of_screenshots = 0
    database = None

    def __init__(self, **kwargs):
        '''

        :param kwargs:
            engine: str ("qt" | "external"),
            dst_folder: str,
            work_folder: str,
            pixel_threshold_different_images: int,
            check_locked_screen_cmd: str,
            check_locked_screen_cmd_result: str,
            screenshot_cmd: str,
            check_locked_screen: bool,
            ignore_if_active_window: bool,
            convert_png_to_jpg: bool,
            include_processes: bool,
            include_ocr: bool
        '''
        self.__dict__.update(kwargs)

        self.begin_datetime = datetime.now()
        self.folder = self.work_folder + f"Autoscreen - {self.begin_datetime.year}{self.begin_datetime.month:02}{self.begin_datetime.day:02}_{self.begin_datetime.hour:02}{self.begin_datetime.minute:02}{self.begin_datetime.second:02}"
        os.mkdir(self.folder)
        if self.include_processes or self.include_ocr:
            self.create_DB()
            self.create_search_script()

    def create_DB(self):
        self.database = sqlite3.connect(f'{self.folder}/autoscreen.sqlite')
        self.database.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}  # get dict output (https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query)

        self.database.execute("CREATE TABLE processes(id integer primary key autoincrement not null, screenshot_file text, username text, pid integer not null, ppid integer not null, cwd text, name text, cmdline text)")
        self.database.commit()

    def create_search_script(self):
        search_script = """#!/bin/env python

import sqlite3
import os
import sys
import shutil

filename = 'autoscreen.sqlite'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} chunk_of_cmdline_or_process")
        sys.exit(1)

    request = sys.argv[1]

    if not os.path.isfile(filename) or not os.access(filename, os.R_OK):
        print(f'Database file "{filename}" not found.')
        sys.exit(1)

    try:
        db = sqlite3.connect(filename)
    except sqlite3.OperationalError as e:
        print(e)
        sys.exit(2)

    res = db.execute("SELECT DISTINCT screenshot_file FROM processes WHERE cmdline LIKE '%' || ? || '%'", (request,))
    screenshot_files = res.fetchall()

    if len(screenshot_files) == 0:
        print(f"No screenshot taken while a process containing '{request}' was found.")
        sys.exit(0)

    try:
        os.mkdir(request)
    except FileExistsError:
        pass

    print(f"Found {len(screenshot_files)} screenshots. Creating copies in dedicated folder '{request}'")
    for screenshot_file in screenshot_files:
        print(f"{screenshot_file[0]} -> {request}/{screenshot_file[0]}")
        shutil.copyfile(screenshot_file[0], request + '/' + screenshot_file[0])
"""
        with open(f'{self.folder}/search.py', 'w') as f:
            f.write(search_script)

    def save_archive(self):
        self.archive = f'{dst_folder}Autoscreen-{self.begin_datetime.year}{self.begin_datetime.month:02}{self.begin_datetime.day:02}_{self.begin_datetime.hour:02}{self.begin_datetime.minute:02}{self.begin_datetime.second:02}.tar.xz'
        cmd = ['tar', 'cJvpf', self.archive, '-C', self.folder, '.']
        tar_output = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        for line in tar_output.stdout:
            line = line.decode().strip()
            if not line or line == './':
                continue
            if any([line.endswith(item) for item in ['.jpg', '.png']]):
                yield {'stdout': line}

        for line in tar_output.stderr:
            yield {'stderr': line.decode().strip()}

        tar_output.stdout.close()
        tar_output.stderr.close()

        return_code = tar_output.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd)

    def take_screenshot(self) -> bool:
        _ = datetime.now()
        screenshot_filename_prefix = f'{self.folder}/Screenshot_{_.year}{_.month:02}{_.day:02}_{_.hour:02}{_.minute:02}{_.second:02}'
        screenshot_files = []

        # Checking lockscreen:
        if self.check_locked_screen:
            cmd = subprocess.Popen(self.check_locked_screen_cmd.split(), stdout=subprocess.PIPE)
            if any([self.check_locked_screen_cmd_result in line.decode() for line in cmd.stdout.readlines()]):
                return False

        # Taking screenshot
        if self.engine == 'qt':
            from PySide6.QtGui import QGuiApplication
            # If the number of screens (= screenshots) changed:
            if len(self.previous_screenshots) != len(QGuiApplication.screens()):
                self.previous_screenshots = [None] * len(QGuiApplication.screens())
                print(self.previous_screenshots)
            for i, screen in enumerate(QGuiApplication.screens()):
                original_pixmap = screen.grabWindow(0)
                if not original_pixmap.save(f"{screenshot_filename_prefix}-{i}.png"):
                    return False
                else:
                    screenshot_files.append(f"{screenshot_filename_prefix}-{i}.png")

        else:
            if len(self.previous_screenshots) == 0:
                self.previous_screenshots = [None]  # Let's consider there is only one screen ?
            subprocess.run([chunk.replace('%%%OUTPUT%%%', f"{screenshot_filename_prefix}.png") for chunk in self.screenshot_cmd.split()])
            screenshot_files.append(f"{screenshot_filename_prefix}.png")

        # Checking screenshots
        current_screenshots = []
        for screenshot_file in screenshot_files:
            if os.path.isfile(screenshot_file) and os.path.getsize(screenshot_file):
                # Checking if screenshot is different from previous one
                pil_img = Image.open(screenshot_file)
                pil_img_width, pil_img_height = pil_img.size
                try:
                    current_screenshots.append(pil_img.crop((61, 61, pil_img_width-61, pil_img_height - 61)))
                except OSError as e:
                    return False
            else:
                return False

        # for previous_screenshot, current_screenshot in zip(self.previous_screenshots, current_screenshots):
        for i, current_screenshot in enumerate(current_screenshots):
            # If more than X pixels different from previous screenshots
            if current_screenshot and (not self.previous_screenshots[i] or len(set(ImageChops.difference(current_screenshot, self.previous_screenshots[i]).getdata())) > self.pixel_threshold_different_images):
                self.nb_of_screenshots += 1
                self.previous_screenshots[i] = current_screenshot

                if self.convert_png_to_jpg:
                    subprocess.run(['magick', screenshot_files[i], screenshot_files[i].removesuffix('.png') + '.jpg'])
                    os.remove(screenshot_files[i])
                    screenshot_files[i] = screenshot_files[i].removesuffix('.png') + '.jpg'

                if self.include_processes:
                    for process in psutil.process_iter():
                        if process.ppid() not in self.processes_ppid_blacklist and process.name() not in self.processes_blacklist:
                            query_filename = screenshot_files[i].removeprefix(self.folder + '/')
                            try:
                                query_cwd = process.cwd()
                            except:
                                query_cwd = '?'

                            try:
                                query_cmd = ' '.join(process.cmdline())
                            except psutil.ZombieProcess:
                                query_cmd = "<zombie process>"

                            query = f"INSERT INTO processes (screenshot_file, username, pid, ppid, cwd, name, cmdline) VALUES (?, ?, ?, ?, ?, ?, ?)"
                            self.database.execute(query, (query_filename, process.username(), process.pid, process.ppid(), query_cwd, process.name(), query_cmd))
                            self.database.commit()

            else:
                os.remove(screenshot_files[i])
        return True


def main():
    from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

    screenshot_mgr = Screenshot(engine=engine,
                                dst_folder=dst_folder,
                                work_folder=work_folder,
                                pixel_threshold_different_images=pixel_threshold_different_images,
                                check_locked_screen_cmd=check_locked_screen_cmd,
                                check_locked_screen_cmd_result=check_locked_screen_cmd_result,
                                screenshot_cmd=screenshot_cmd,
                                check_locked_screen=check_locked_screen,
                                ignore_if_active_window=False,
                                convert_png_to_jpg=convert_png_to_jpg,
                                include_processes=include_processes,
                                include_ocr=include_ocr,
                                processes_blacklist=processes_blacklist,
                                processes_ppid_blacklist=processes_ppid_blacklist)

    progress = Progress(SpinnerColumn(spinner_name='bouncingBar'), *Progress.get_default_columns(), TimeElapsedColumn(), transient=True, auto_refresh=True)
    master_task = progress.add_task("Waiting until next screenshot...", total=interval)

    with progress:
        progress.console.print("Starting screenshot loop...")
        while True:
            try:
                progress.reset(master_task)
                progress.update(master_task, description="Screenshoting...")

                try:
                    screenshot_mgr.take_screenshot()
                except Exception as e:
                    progress.console.print(f"[red]Failed to save screenshot ![/red]")

                progress.update(master_task, description=f"{str(screenshot_mgr.nb_of_screenshots)} screenshots taken ({'{:.2f}'.format(get_dir_size(screenshot_mgr.folder) / 1024 / 1024)} Mo) in {int((datetime.now() - screenshot_mgr.begin_datetime).seconds / 60)} minutes!")

                # Tempo
                for i in range(interval):
                    time.sleep(1)
                    progress.advance(master_task)

            except KeyboardInterrupt:
                break

        progress.console.print(f"Finished ! I took {str(screenshot_mgr.nb_of_screenshots)} screenshots ({'{:.2f}'.format(get_dir_size(screenshot_mgr.folder) / 1024 / 1024)} Mo) in {int((datetime.now() - screenshot_mgr.begin_datetime).seconds / 60)} minutes!")

        progress.update(master_task, description="Saving database")
        progress.advance(master_task, interval)
        progress.update(master_task, visible=False)
        tar_task = progress.add_task("Creating archive file...", total=screenshot_mgr.nb_of_screenshots)

        try:
            for output in screenshot_mgr.save_archive():
                progress.advance(tar_task)
                if 'stdout' in output.keys():
                    progress.update(tar_task, description=f"Compressing {output['stdout']}...")
                if 'stderr' in output.keys():
                    progress.console.print(f"Compressing error: [red]{output['stderr']}[/red]")
        except Exception as e:
            progress.console.print(f"[red]An error occured when compressing screenshots into an archive file: {str(e)}[/red]")

        folder_size = get_dir_size(screenshot_mgr.folder)
        archive_size = int(os.stat(screenshot_mgr.archive).st_size)
        progress.console.print(f"Created archive {screenshot_mgr.archive} with {'{:.2f}'.format(archive_size * 100 / folder_size)}% of original size ({str(screenshot_mgr.nb_of_screenshots)} screenshots, {'{:.2f}'.format(archive_size / 1024 / 1024)} Mo instead of {'{:.2f}'.format(folder_size / 1024 / 1024)} Mo).")

if __name__ == '__main__':
    if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print("Edit the variables at the beginning of this script, and launch it without parameters")
    else:
        main()
