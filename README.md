# iTerm2 Workspace Tabs Script

Quickly open iTerm2 windows with predefined tabs, split panes, and commands — configured per project via a simple JSON file.

## Setup

1. Clone this repo into your iTerm2 Scripts directory:

   ```bash
   git clone git@github.com:OrenSayag/iterm2-tabs-script.git \
     ~/Library/Application\ Support/iTerm2/Scripts
   ```

2. Copy the example config and customize it:

   ```bash
   cp workspaces-example.json workspaces.json
   ```

3. Edit `workspaces.json` with your own workspaces (see [Configuration](#configuration)).

## Usage

```bash
# Open a workspace
./workspace.sh my-project

# List available workspaces
./workspace.sh -l

# Show help
./workspace.sh -h
```

## Configuration

`workspaces.json` defines your workspaces. Each workspace has a name and an array of tabs:

```json
{
  "my-project": {
    "tabs": [
      {
        "title": "ui",
        "top": ["cd ~/projects/my-project", "npm run dev"]
      },
      {
        "title": "api",
        "top": ["cd ~/projects/my-project", "npm run start:api"],
        "bottom": ["cd ~/projects/my-project", "tail -f logs/app.log"]
      }
    ]
  }
}
```

| Field    | Description                                              |
| -------- | -------------------------------------------------------- |
| `title`  | Tab name displayed in iTerm2                             |
| `top`    | Commands to run in the main (or top) pane                |
| `bottom` | *(optional)* Commands to run in a horizontal split pane  |

## Dependencies

- [iTerm2](https://iterm2.com/) with Python API enabled
- Python 3
