import re

from PySide6.QtCore import QProcess
from ansi2html import Ansi2HTMLConverter
import os
import signal
from enum import Enum

from core.config import Config


class JobType(Enum):
    SCAN = 0
    ATTACHED_PROGRAM = 1


class Job(QProcess):
    def __init__(self):
        super().__init__()
        self.stdout = self.stderr = self.output_text = ""
        self.readyReadStandardOutput.connect(self.stdoutEvent)
        self.readyReadStandardError.connect(self.stderrEvent)
        self.previous_state = None

    def stdoutEvent(self):
        stdout = self.readAllStandardOutput()
        decoded = stdout.data().decode()

        self.stdout += decoded
        self.output_text += decoded

    def stderrEvent(self):
        stderr = self.readAllStandardError()
        decoded = stderr.data().decode()

        self.stderr += decoded
        self.output_text += decoded

    @staticmethod
    def convert_raw_output_to_html(cmdline: str, content: str):
        conv = Ansi2HTMLConverter()
        if cmdline:
            output = f'$ {cmdline}\n{content}'
        else:
            if content.startswith('<span style="color: white;'):  # Compatibility with databases created through previous versions of QtRecon
                return content
            else:
                output = content

        try:
            html = conv.convert(output)
        except ValueError:
            html = conv.convert(output.replace(chr(0), ""))

        return re.sub('.body_foreground {.*}', f".body_foreground {{ color: #BBBBBB; font-family: {Config.get()['user_prefs']['monospaced_fonts']} }}", html)

    def get_output_text(self):
        return self.convert_raw_output_to_html(f"{self.program()} {" ".join(self.arguments())}", self.output_text)

    # Unused for now
    def get_stdout_only(self):
        return self.stdout

    # Unused for now
    def get_stderr_only(self):
        return self.stderr

    def pause(self):
        if self.state() != QProcess.ProcessState.NotRunning:
            os.kill(self.pid(), signal.SIGSTOP)
            self.previous_state = self.state()
            self.setProcessState(QProcess.ProcessState.NotRunning)

    def resume(self):
        if self.previous_state:
            self.setProcessState(self.previous_state)
            self.previous_state = None
            os.kill(self.pid(), signal.SIGCONT)
