# ---------------------------------------------------- IMPORTS ----------------------------------------------------

from libqtile import layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook
from libqtile.log_utils import logger
import subprocess
import os

# --------------------------------------------------- KEYBINDS ----------------------------------------------------

mod = "mod4"                                                                                       # Super Key

keys = [
    Key([mod], "h", lazy.layout.left()),                                                           # Focus Window
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),                                          # Move Window
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    Key([mod, "control"], "h", lazy.layout.grow_left()),                                           # Grow Window
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    Key([mod], "Return", lazy.spawn("alacritty")),                                                 # Terminal
    Key([mod], "b", lazy.spawn("firefox")),                                                    # Browser
    Key([mod], "z", lazy.spawn("zeditor")),                                                        # Zed
    Key([mod], "s", lazy.spawn("spotify")),                                                        # Spotify
    Key([mod], "n", lazy.spawn("nautilus")),                                                       # File Explorer
    Key([mod], "Space", lazy.spawn("rofi -show drun")),                                                       # File Explorer
    Key([], "Print", lazy.spawn("sh /home/yermalouski/.config/rofi/screenshot.sh")),                                                       # File Explorer


    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),                                     # Stack Split Toggle
    Key([mod], "Tab", lazy.next_layout()),                                                         # Toggle Layouts
    Key([mod], "q", lazy.window.kill()),                                                           # Kill Window
    Key([mod], "f", lazy.window.toggle_fullscreen()),                                              # Fullscreen
    Key([mod], "t", lazy.window.toggle_floating()),                                                # Toggle Floating
    Key([mod, "control"], "r", lazy.reload_config()),                                              # Reload Qtile
    Key([mod, "control"], "q", lazy.shutdown()),                                                   # Exit Qtile
    Key([mod], "r", lazy.spawncmd()),                                                              # Spawn Window
]

# ---------------------------------------------------- ??????? ----------------------------------------------------

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


# -------------------------------------------------- WORKSPACES ---------------------------------------------------

groups = [Group(i) for i in "1234"]                                                               # Amount Defined

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#ffffff", "#ffffff"], border_width=0, margin = 10),
    layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=20,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [Screen()]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="eww"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "Qtile"

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["xrandr", "--output", "HDMI-1", "--mode", "1920x1080", "--rate", "75", "--primary"])
    subprocess.Popen(["xrandr", "--output", "DP-3", "--mode", "1920x1080", "--rate", "144", "--rotate", "right", "--left-of", "HDMI-1"])
    subprocess.Popen(["eww", "open", "bar"])
    subprocess.Popen(["picom"])
    subprocess.Popen(["dunst"])
    subprocess.Popen(["feh", "--bg-scale", "/home/yermalouski/Documents/Wallpapers/wallpaper.jpg"])
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])
    subprocess.Popen(["openvpn", "--config", "/home/yermalouski/.ssh/profiles/client.ovpn"])

@hook.subscribe.client_new
def float_eww(window):
    if window.get_wm_class() == ('eww', 'eww'):
        window.floating = True
        window.cmd_bring_to_front()
        window.cmd_focus()
