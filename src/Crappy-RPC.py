import os
import time
import psutil
import pypresence
import subprocess


# Configuration
EXTENSION_MAPPING = {
    ".py": ("python", "Editing a .py file!"),
    ".rb": ("ruby", "Editing a .rb file!"),
    ".js": ("javascript", "Editing a .js file!"),
    ".java": ("java", "Editing a .java file!"),
    ".c": ("c", "Editing a .c file!"),
    ".cpp": ("cpp", "Editing a .cpp file!"),
    ".cs": ("c-sharp", "Editing a .cs file!"),
    ".sh": ("bash", "Editing a .sh file!"),
    ".json": ("json", "Editing a .json file!"),
    ".html": ("html", "Editing an .html file!"),
    ".css": ("css", "Editing a .css file!"),
    ".php": ("php", "Editing a .php file!"),
    ".xml": ("xml", "Editing an .xml file!"),
    ".md": ("markdown", "Editing a .md file!"),
    ".rs": ("r", "Editing an .r file!"),
}

APPLICATION_ID = '...' # <-- Bot Application ID here
APP_NAME = 'xed'
UPDATE_INTERVAL = 15


class XedPresence:
    def __init__(self, application_id):
        self.application_id = application_id
        self.rpc = pypresence.Presence(application_id)
        self.rpc.connect()
        self.large_image = None
        self.small_image = None
        self.large_text = None
        self.small_text = None
        self.start_time = time.time()

    def is_app_running(self, app_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == app_name:
                return True
        return False

    def get_app_info(self, app_name):
        try:
            output = subprocess.check_output(['xdotool', 'search', '--class', app_name], text=True)
            window_ids = output.strip().split()
            window_names = []
            for window_id in window_ids:
                output = subprocess.check_output(['xdotool', 'getwindowname', window_id], text=True)
                window_name = output.strip()
                window_names.append(window_name)
            if window_names:
                return window_names[-1]  # Return the last element
            else:
                return []
        except subprocess.CalledProcessError:
            return []

    def update_state(self):
        if self.is_app_running(APP_NAME):
            open_file = self.get_app_info(APP_NAME)
            if open_file:
                base_file_name = os.path.basename(open_file.split()[0])
                self.large_image = "coding_lol"
                self.large_text = "IDE: XED"
                self.details = "Activity: Coding!"
                self.state = 'Open File: ' + open_file

                file_extension = os.path.splitext(base_file_name)[1]
                self.small_image, self.small_text = EXTENSION_MAPPING.get(file_extension, ("generic_file", "Editing a random file!"))
            else:
                self.details = "Activity: Coding!"
                self.state = "No file opened - Idle"
                self.small_image = None
                self.small_text = None
        else:
            self.details = "Activity: Nothing!"
            self.state = "Might be AFK or Chatting"
            self.large_image = "dexechii_main"
            self.large_text = "Idle :3"
            self.small_image = "pan_small"
            self.small_text = "Pan UwU"

    def run(self):
        try:
            print("Rich Presence Started")
            while True:
                self.update_state()
                self.rpc.update(
                    details=self.details,
                    state=self.state,
                    large_image=self.large_image,
                    small_image=self.small_image,
                    large_text=self.large_text,
                    small_text=self.small_text,
                    start=self.start_time,
                )
                time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\nExited Rich Presence")


if __name__ == "__main__":
    xed_presence = XedPresence(APPLICATION_ID)
    xed_presence.run()
