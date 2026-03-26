#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/workspace.py"
CONFIG_FILE="$SCRIPT_DIR/workspaces.json"

show_help() {
    echo "Usage: workspace.sh <workspace-name>"
    echo ""
    echo "Open an iTerm2 workspace with predefined tabs and commands."
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -l, --list     List all available workspaces"
    echo ""
    echo "Examples:"
    echo "  workspace.sh shila-leads"
    echo "  workspace.sh my-mor"
}

list_workspaces() {
    echo "Available workspaces:"
    if command -v jq &> /dev/null; then
        jq -r 'keys[]' "$CONFIG_FILE" | sort | sed 's/^/  - /'
    else
        python3 -c "import json; print('\n'.join(sorted(json.load(open('$CONFIG_FILE')).keys())))" | sed 's/^/  - /'
    fi
}

if [[ $# -eq 0 ]]; then
    show_help
    echo ""
    list_workspaces
    exit 1
fi

case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
    -l|--list)
        list_workspaces
        exit 0
        ;;
    *)
        exec python "$PYTHON_SCRIPT" "$1"
        ;;
esac
