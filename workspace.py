#!/usr/bin/env python3

import iterm2
import AppKit
import json
import sys
import os

bundle = "com.googlecode.iterm2"
if not AppKit.NSRunningApplication.runningApplicationsWithBundleIdentifier_(bundle):
    AppKit.NSWorkspace.sharedWorkspace().launchApplication_("iTerm")

# Get workspace name from command line argument or environment variable
workspace_name = None
if len(sys.argv) > 1:
    workspace_name = sys.argv[1]
elif "ITERM_WORKSPACE" in os.environ:
    workspace_name = os.environ["ITERM_WORKSPACE"]

if not workspace_name:
    print("Usage: workspace.py <workspace-name>")
    print("   or: ITERM_WORKSPACE=<name> workspace.py")
    print("\nAvailable workspaces:")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "workspaces.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    for name in sorted(config.keys()):
        print(f"  - {name}")
    sys.exit(1)

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "workspaces.json")

with open(config_path, "r") as f:
    config = json.load(f)

if workspace_name not in config:
    print(f"Error: Workspace '{workspace_name}' not found in configuration.")
    print("\nAvailable workspaces:")
    for name in sorted(config.keys()):
        print(f"  - {name}")
    sys.exit(1)

workspace = config[workspace_name]
window_title = workspace_name
tabs = workspace["tabs"]


async def main(connection):
    app = await iterm2.async_get_app(connection)

    window = await iterm2.Window.async_create(connection)

    await window.async_set_title(window_title)
    window = app.current_terminal_window

    async def create_tab(tab_config, is_first_tab):
        async def send_commands(commands):
            for command in commands:
                await session.async_send_text(command + "\n")

        tab = window.current_tab if is_first_tab else await window.async_create_tab()
        await tab.async_set_title(tab_config["title"])

        session = tab.current_session
        await send_commands(tab_config["top"])
        if "bottom" in tab_config:
            await session.async_split_pane(vertical=False)
            session = tab.current_session
            await send_commands(tab_config["bottom"])

    for tab_config in tabs:
        await create_tab(tab_config, tab_config == tabs[0])

    async def resize_window():
        await window.async_set_fullscreen(True)

    await resize_window()


iterm2.run_until_complete(main)
