# ---------------------------------------------------- IMPORTS ----------------------------------------------------

from libqtile import layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook
import subprocess
import os

# --------------------------------------------------- KEYBINDS ----------------------------------------------------

mod = "mod4"                                                                                        # Super Key
groups = [Group(i) for i in "1234"]                                                                 # Workspaces

keys = [
# APPS
    Key([mod], "Return", lazy.spawn("alacritty")),                                                  # Terminal
    Key([mod], "b", lazy.spawn("firefox")),                                                         # Browser
    Key([mod], "z", lazy.spawn("zeditor")),                                                         # Zed
    Key([mod], "s", lazy.spawn("spotify")),                                                         # Spotify
    Key([mod], "e", lazy.spawn("nautilus")),                                                        # File Explorer
    Key([mod], "Space", lazy.spawn("rofi -show drun")),                                             # List Menu
    Key([], "Print", lazy.spawn("sh /home/yermalouski/.config/rofi/screenshot.sh")),                # Screenshot

# VOLUME
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%")),                     # Raise 5%
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%")),                     # Lower 5%
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle")),                           # Mute Volume

# GENERAL
    Key([mod], "q", lazy.window.kill()),                                                            # Kill Window
    Key([mod], "f", lazy.window.toggle_fullscreen()),                                               # Fullscreen
    Key([mod, "control"], "r", lazy.reload_config()),                                               # Reload Qtile
    Key([mod, "control"], "q", lazy.shutdown()),                                                    # Exit Qtile
    Key([mod], "Tab", lazy.next_layout()),                                                          # Toggle Layouts
    Key([mod], "t", lazy.window.toggle_floating()),                                                 # Toggle Floating
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),                                      # Stack Split Toggle

# FOCUS
    Key([mod], "h", lazy.layout.left()),                                                            # Focus Window
    Key([mod], "l", lazy.layout.right()),                                                           # ---
    Key([mod], "j", lazy.layout.down()),                                                            # ---
    Key([mod], "k", lazy.layout.up()),                                                              # ---
    Key([mod], "c", lazy.layout.next()),                                                            # Cycle Focus

# WINDOW MOVEMENT
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),                                           # Move Window
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),                                          # ---
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),                                           # ---
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),                                             # ---

# WINDOW RESIZING
    Key([mod, "control"], "h", lazy.layout.grow_left()),                                            # Grow Window
    Key([mod, "control"], "l", lazy.layout.grow_right()),                                           # ---
    Key([mod, "control"], "j", lazy.layout.grow_down()),                                            # ---
    Key([mod, "control"], "k", lazy.layout.grow_up()),                                              # ---
    Key([mod], "n", lazy.layout.normalize()),                                                       # Reset Window Sizes
]

# WORKSPACES
for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen()),                                      # Select Workspace
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),            # Move Window to Workspace
        ]
    )

# FLOATING DRAGGING
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),  # Drag Floating Window
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),          # Set Floating Size
    Click([mod], "Button2", lazy.window.bring_to_front()),                                          # Bring Floating to Front
]

# ---------------------------------------------------- LAYOUTS ----------------------------------------------------

# NORMAL
layouts = [
    layout.Columns(border_focus_stack=["#ffffff", "#ffffff"], border_width=0, margin = 10),         # Columns
    layout.Max(border_width=0, margin = 10),                                                        # Fullscreen
    layout.Matrix(border_width=0, margin = 10),                                                     # Even
]

# FLOATING
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="eww"),
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

# -------------------------------------------------- PARAMETERS ---------------------------------------------------

widget_defaults = dict(font="sans", fontsize=20, padding=3)                                         # Default Fonts
extension_defaults = widget_defaults                                                                # ---
screens = [Screen()]                                                                                # Qtile Bar
wmname = "Qtile"                                                                                    # WM Name
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False

# --------------------------------------------------- AUTOSTART ---------------------------------------------------

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["xrandr", "--output", "eDP-1", "--mode", "1920x1080", "--rate", "60"])        # Laptop Display
    subprocess.Popen(["xrandr", "--output", "DP-1-5-5", "--mode", "1920x1080", "--rate", "75"])     # Desktop Display
    subprocess.Popen(["picom"])                                                                     # Compositor
    subprocess.Popen(["polybar", "laptop"])                                                         # Laptop Bar
    subprocess.Popen(["polybar", "desktop"])                                                        # Desktop Bar
    subprocess.Popen(["dunst"])                                                                     # Notifications
    subprocess.Popen(["feh", "--bg-scale", "/home/yermalouski/Documents/Wallpapers/wallpaper.jpg"]) # Background
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])                                      # Mouse Pointer
    subprocess.Popen(["openvpn", "--config", "/home/yermalouski/.ssh/profiles/client.ovpn"])        # VPN
