import os
import json
from textual.app import App
from textual import events
from textual.widgets import Header, Footer, Placeholder, ScrollView


def display():
    """Main display function"""
    SSTUIMain.MainApp.run()


class SSTUIMain(object):
    class MainApp(App):
        async def on_load(self, event: events.Load) -> None:
            """Bind keys with the app loads (but before entering application mode)"""
            await self.bind("q", "quit", "Quit")
            await self.bind("p", "preview", "Preview Page")
            await self.bind("n", "next", "Next Page")

        async def on_mount(self, event: events.Mount) -> None:
            """Create and dock the widgets."""

            # A scrollview to contain the content
            grid = await self.view.dock_grid(edge="left", name="left")
            grid.add_column(fraction=1, name="left", min_size=20)
            grid.add_column(size=30, name="center")
            grid.add_column(fraction=1, name="right")

            grid.add_row(fraction=1, name="top", min_size=2)
            grid.add_row(fraction=2, name="middle")
            grid.add_row(fraction=1, name="bottom")
            grid.add_row(fraction=1, name="a1")

            grid.add_areas(
                area1="left,top",
                area2="center,middle",
                area3="left-start|right-end,bottom-start|a1-end",
                area4="right,top-start|middle-end",
            )
            grid.place(
                area1=Placeholder(name="area1"),
                area2=Placeholder(name="area2"),
                area3=Placeholder(name="area3"),
                area4=Placeholder(name="area4"),
            )

            # Header / footer / dock
            await self.view.dock(Header(), edge="top")
            await self.view.dock(Footer(), edge="bottom")

            # Dock the body in the remaining space
            # await self.view.dock(body, edge="right")

    def __init__(self):
        self.config = None
        self.tileList = []
        self.currentTileIndex = 0

    def load_config(self):
        """Load configuration from current directory, or create a new one"""
        try:
            with open("config.json") as config_file:
                self.config = json.load(config_file)
                # load tiles
                for tile in self.config["tiles"]:
                    self.tileList.append(tile)
        except FileNotFoundError:
            with open('config.json', 'w') as f:
                config_template = {
                    "tiles": [
                        {
                            "title": "example",
                            "refreshInmillisecond": 5,
                            "durationInmillisecond": 10000,
                            "filePath": "examplePath/example.txt"
                        }
                    ]
                }
                json.dump(config_template, f, indent=4)
            os.mkdir("examplePath")
            with open('examplePath/example.txt', 'w') as f:
                f.write("""
This is an example file.
TUI project load this file and display it.
Use other tools to update this file.
AethLi/server_status_tui.
                """)
                print(
                    'config.json not found, create a default config.json, please edit it')
                print('now exit')
                exit()

    def switch(self):
        """Switch to next tile"""
        self.currentTileIndex += 1
        if self.currentTileIndex >= len(self.tileList):
            self.currentTileIndex = 0
        display()

    def main(self):
        """Main function"""
        self.load_config()
        display()


if __name__ == "__main__":
    """Main function"""
    m = SSTUIMain()
    m.main()
