from PySide2.QtCore import QProcess
from ansi2html import Ansi2HTMLConverter
import os
import signal
from enum import Enum


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

    def get_output_text(self):
        command_line = f'<span style="color: white; font-size:15px">$ {self.program()} {" ".join(self.arguments())}</span>'

        conv = Ansi2HTMLConverter()
        return command_line + conv.convert(self.output_text)

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
