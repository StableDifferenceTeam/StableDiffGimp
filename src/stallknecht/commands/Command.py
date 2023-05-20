# Command Klasse,
# sodass alle Commands von dieser Klasse erben können

# basic properties für jeden Command

# Basic Command class, executable by the command runner
class Command:
    def __init__(self, **kwargs):
        self.command_metadata = kwargs
        self.status = "INITIALIZED"

    def run(self):
        self.status = "RUNNING"
        print("Command is running")


class StableDiffusionCommand(Command):

    uri = ""

    def __init__(self, command_metadata):
        super().__init__(self, command_metadata)
        self.url = urljoin("http://localhost:7860", self.uri)
        self.img = command_metadata["img"]

    def run(self):
        self.status = "RUNNING"
        print("Command is running")
        self.progress = 0.5
        self.status = "DONE"
