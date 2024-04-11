#!/usr/bin/env python3.7

import iterm2

import AppKit
bundle = "com.googlecode.iterm2"
if not AppKit.NSRunningApplication.runningApplicationsWithBundleIdentifier_(bundle):
    AppKit.NSWorkspace.sharedWorkspace().launchApplication_("iTerm")

window_title = "project"


tabs = [
    {
        "title": "fe",
        "top": [
            "cd PATH_TO_FE_PROJECT",
        ],
        "bottom": [
            "cd PATH_TO_FE_PROJECT"
        ]
    },
    {
        "title": "be",
        "top": [
            "cd PATH_TO_BE_PROJECT",
        ],
        "bottom": [
            "cd PATH_TO_BE_PROJECT"
        ]
    },
    {
        "title": "server",
        "top": [
            "cd SOME_PATH",
        ],
        "bottom": [
            "cd SOME_PATH"
        ]
    },
]


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
        await session.async_split_pane(vertical=False)
        session = tab.current_session
        await send_commands(tab_config["bottom"])

    for tab_config in tabs:
        await create_tab(tab_config, tab_config == tabs[0])

    async def resize_window():
        await window.async_set_fullscreen(True)

    await resize_window()


iterm2.run_until_complete(main)
