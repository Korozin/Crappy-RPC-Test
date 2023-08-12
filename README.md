# Crappy-RPC-Test

Decided to play around with custom RPC using the pypresence module. The result is probably pretty unstable.

## How it works

First you initialize the Class with your bot's Application ID, and use the Class's `run()` method to start the rpc.

To determine what state the status is set to it will use the method `is_app_running()` to make sure `xed` is running. If not, it'll display as such. However, if it is- it'll use the `get_app_info()` method which uses the `xdotool` command to fetch the window name from xed's current process (this includes the file name, and path it's open in). The class will then display that information on your activity status.

There's also a dictonary for mapping images / text to certain file typings.

PS: You can use image URLs instead of actual Bot Image Keys if you choose to do so.

## Disclaimer

This script isn't that good. I'm pretty sure it only works on Linux (because of xdotool, and obviously xed). If you want a smaller example, I'll put one below.

```python
import time
import psutil
import pypresence


APPLICATION_ID = '...' # <-- Bot Application ID here
UPDATE_INTERVAL = 15


class RPC:
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

    def update_state(self):
        if self.is_app_running("<program_name>"):
            self.details = "detail text"
            self.state = "state text"
            self.large_image = "large image key / url"
            self.large_text = "large image text"
            self.small_image = "small image key / url"
            self.small_text = "small image text"
        elif self.is_app_running("<program_name>"):
            # ...
            # You get the idea.
        else:
            self.details = "detail text"
            self.state = "state text"
            self.large_image = "large image key / url"
            self.large_text = "large image text"
            self.small_image = "small image key / url"
            self.small_text = "small image text"

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
    rich_presence = RPC(APPLICATION_ID)
    rich_presence.run()
```

That should work cross-platform. The only reason the xed one is so weird is because I wanted it to show what file was being edited.
