from os.path import dirname
from pathlib import PurePath
from typing import AbstractSet, Optional

from pynvim import Nvim
from std2.pathlib import longest_common_path

from ...fs.cartographer import new
from ...fs.ops import ancestors
from ...settings.types import Settings
from ...state.next import forward
from ...state.types import State
from ..types import Stage


def new_current_file(
    nvim: Nvim, state: State, settings: Settings, current: str
) -> Optional[Stage]:
    """
    New file focused in buf
    """

    parents = ancestors(current)
    if state.root.path in parents:
        paths: AbstractSet[str] = parents if state.follow else set()
        index = state.index | paths
        new_state = forward(
            state, settings=settings, index=index, paths=paths, current=current
        )
        return Stage(new_state)
    else:
        return None


def new_root(nvim: Nvim, state: State, settings: Settings, new_cwd: str) -> State:
    index = state.index | {new_cwd}
    root = new(new_cwd, index=index)
    selection = {path for path in state.selection if root.path in ancestors(path)}
    return forward(
        state, settings=settings, root=root, selection=selection, index=index
    )


def maybe_path_above(
    nvim: Nvim, state: State, settings: Settings, path: str
) -> Optional[State]:
    root = state.root.path
    if PurePath(path).is_relative_to(root):
        return None
    else:
        lcp = longest_common_path(path, root)
        new_cwd = str(lcp) if lcp else dirname(path)
        return new_root(nvim, state=state, settings=settings, new_cwd=new_cwd)
