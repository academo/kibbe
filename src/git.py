from pathlib import Path
import subprocess


def get_worktree_list():
    raw_list = subprocess.getoutput("git worktree list --porcelain")
    worktrees = []
    raw_list = raw_list.split("\n")

    current = {}
    for item in raw_list:
        if not item:
            worktrees.append(current)
            current = {}
            continue

        [name, value] = item.split(" ")
        current[name] = value

    return worktrees


def get_worktree_list_flat(incomplete=""):
    final = []
    try:
        worktrees = get_worktree_list()
        for tree in worktrees:
            if not incomplete or (
                incomplete and tree["worktree"].startswith(incomplete)
            ):
                final.append(tree["worktree"])
    except ValueError:
        pass

    return final


def find_existing_worktree(path_name):
    worktrees = get_worktree_list()
    existing_worktree = {}
    for tree in worktrees:
        path = Path(tree["worktree"])
        if path.name == path_name:
            existing_worktree = tree
            break

    return existing_worktree
