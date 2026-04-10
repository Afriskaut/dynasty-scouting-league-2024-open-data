"""
afriskaut_utils.py
──────────────────
Utility functions for plotting Afriskaut event data.

Usage in notebook:
    from afriskaut_utils import load_match, load_events, build_plot_data, plot_events
"""

import json
import os

import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd


# ── Constants ──────────────────────────────────────────────────────────────
PITCH_LENGTH = 497
PITCH_WIDTH  = 328
GOAL_WIDTH   = int(round(7.32 / 68 * PITCH_WIDTH))   # ≈ 35 units
GOAL_DEPTH   = 12


# ── I/O ────────────────────────────────────────────────────────────────────

def load_match(match_dir: str) -> dict:
    """Load match.json from a match directory."""
    with open(os.path.join(match_dir, "match.json")) as f:
        return json.load(f)


def load_events(match_dir: str) -> pd.DataFrame:
    """Load events.jsonl from a match directory into a DataFrame."""
    events = []
    with open(os.path.join(match_dir, "events.jsonl")) as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return pd.DataFrame(events)


def load_all_events(datasets_path: str) -> pd.DataFrame:
    """
    Load events from every match in the datasets folder.
    Adds a 'match_id' column to each event row.
    """
    all_events = []
    for mid in sorted(os.listdir(datasets_path)):
        events_path = os.path.join(datasets_path, mid, "events.jsonl")
        if not os.path.exists(events_path):
            continue
        with open(events_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    event = json.loads(line)
                    event["match_id"] = mid
                    all_events.append(event)
    return pd.DataFrame(all_events)


# ── Time helpers ───────────────────────────────────────────────────────────

def to_seconds(t) -> int:
    """Convert HH:MM:SS timestamp string to total seconds."""
    try:
        h, m, s = str(t).split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)
    except Exception:
        return 0


def halftime_midpoint(match: dict) -> float:
    """
    Return the timestamp (seconds) that divides first and second half,
    derived from first_half_end_time and second_half_start_time in match metadata.
    """
    first_half_end    = to_seconds(match.get("first_half_end_time",    "00:45:00"))
    second_half_start = to_seconds(match.get("second_half_start_time", "01:00:00"))
    return (first_half_end + second_half_start) / 2


# ── Match metadata helpers ─────────────────────────────────────────────────

def parse_direction(match: dict) -> tuple[str, str]:
    """
    Returns (home_dir, away_dir) for the first half.
    'ltr' = attacking left-to-right, 'rtl' = right-to-left.
    """
    def normalise(s):
        s = str(s).lower().replace(" ", "").replace("-", "")
        return "ltr" if ("left" in s or s in ("ltr",)) else "rtl"

    if "home_team_starting_direction" in match and "away_team_starting_direction" in match:
        return normalise(match["home_team_starting_direction"]), normalise(match["away_team_starting_direction"])
    elif "team_starting_direction" in match:
        home = normalise(match["team_starting_direction"])
        return home, ("rtl" if home == "ltr" else "ltr")

    print("⚠️  No direction field found in match.json — defaulting: home=ltr, away=rtl")
    return "ltr", "rtl"


def readable_color(hex_color: str, fallback: str) -> str:
    """
    Return hex_color unless it is too light to see on a dark background,
    in which case return fallback.
    """
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return fallback if (0.299 * r + 0.587 * g + 0.114 * b) > 200 else hex_color
    except Exception:
        return fallback


def team_colors(match: dict) -> tuple[str, str]:
    """Return (home_color, away_color) safe for plotting on dark backgrounds."""
    home = readable_color(match.get("home_team_color", "#00d4ff"), "#00d4ff")
    away = readable_color(match.get("away_team_color", "#ff6b35"), "#ff6b35")
    return home, away


# ── Coordinate helpers ─────────────────────────────────────────────────────

def get_coords(row, x_col="event_start_x", y_col="event_start_y") -> tuple:
    """Cast coordinate fields to float. Returns (None, None) on failure."""
    try:
        return float(row[x_col]), float(row[y_col])
    except (TypeError, ValueError):
        return None, None


def build_plot_data(
    events: pd.DataFrame,
    match: dict,
    x_col:    str = "event_start_x",
    y_col:    str = "event_start_y",
    time_col: str = "event_start_time",
    team_col: str = "team_id",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = {x_col, y_col, team_col, time_col}
    missing  = required - set(events.columns)
    if missing:
        raise ValueError(
            f"Missing columns in events DataFrame: {missing}\n"
            f"Available: {list(events.columns)}"
        )

    if events.empty:
        raise ValueError(
            f"No events found to plot.\n"
            f"Available event types: {list(events['event_type'].unique()) if 'event_type' in events.columns else 'unknown'}"
        )

    home_team_id = str(match.get("home_team", ""))

    plot_data = events.copy()
    coords = plot_data.apply(lambda r: pd.Series(get_coords(r, x_col, y_col)), axis=1)
    coords.columns = ["x_norm", "y_norm"]
    plot_data = pd.concat([plot_data, coords], axis=1)
    plot_data = plot_data.dropna(subset=["x_norm", "y_norm"])

    is_home     = plot_data[team_col].astype(str).str.strip() == home_team_id
    home_events = plot_data[is_home]
    away_events = plot_data[~is_home]

    return home_events, away_events


# ── Pitch drawing ──────────────────────────────────────────────────────────

def draw_pitch(ax, match: dict, length=PITCH_LENGTH, width=PITCH_WIDTH):
    """
    Draw a standard Afriskaut pitch on ax, including goalposts,
    penalty boxes, six-yard boxes, centre circle, arcs, and corner flags.
    Adds H1 direction labels for each team below the goal lines.
    """
    home_dir_h1, away_dir_h1 = parse_direction(match)
    home_color, away_color   = team_colors(match)
    home_name = match.get("home_team_string", "Home")
    away_name = match.get("away_team_string", "Away")
    goal_y    = (width - GOAL_WIDTH) / 2

    ax.set_facecolor("#2d7a2d")
    ax.set_xlim(-GOAL_DEPTH - 5, length + GOAL_DEPTH + 5)
    ax.set_ylim(width + 5, -5)

    # Pitch outline
    ax.add_patch(patches.Rectangle(
        (0, 0), length, width,
        linewidth=2, edgecolor="white", facecolor="none", zorder=2
    ))

    # Halfway line
    ax.axvline(x=length / 2, color="white", linewidth=1.5, zorder=2)

    # Centre circle & spot
    ax.add_patch(plt.Circle(
        (length / 2, width / 2), radius=46,
        color="white", fill=False, linewidth=1.5, zorder=2
    ))
    ax.plot(length / 2, width / 2, "o", color="white", markersize=3, zorder=3)

    # Penalty boxes
    box_depth = int(round(16.5 / 105 * length))
    box_width = int(round(40.3 / 68  * width))
    box_y     = (width - box_width) / 2
    for bx in [0, length - box_depth]:
        ax.add_patch(patches.Rectangle(
            (bx, box_y), box_depth, box_width,
            linewidth=1.5, edgecolor="white", facecolor="none", zorder=2
        ))

    # Six-yard boxes
    six_depth = int(round(5.5 / 105 * length))
    six_width = int(round(18.3 / 68  * width))
    six_y     = (width - six_width) / 2
    for bx in [0, length - six_depth]:
        ax.add_patch(patches.Rectangle(
            (bx, six_y), six_depth, six_width,
            linewidth=1, edgecolor="white", facecolor="none", zorder=2
        ))

    # Penalty spots
    pen_x = int(round(11 / 105 * length))
    ax.plot(pen_x,          width / 2, "o", color="white", markersize=3, zorder=3)
    ax.plot(length - pen_x, width / 2, "o", color="white", markersize=3, zorder=3)

    # Penalty arcs
    ax.add_patch(patches.Arc(
        (pen_x, width / 2), width=92, height=92,
        angle=0, theta1=305, theta2=55,
        color="white", linewidth=1.5, zorder=2
    ))
    ax.add_patch(patches.Arc(
        (length - pen_x, width / 2), width=92, height=92,
        angle=0, theta1=125, theta2=235,
        color="white", linewidth=1.5, zorder=2
    ))

    # Goalposts
    for gx, anchor_x in [(0, -GOAL_DEPTH), (length, length)]:
        ax.add_patch(patches.Rectangle(
            (anchor_x, goal_y), GOAL_DEPTH, GOAL_WIDTH,
            linewidth=2, edgecolor="white", facecolor="#ffffff",
            alpha=0.15, zorder=1
        ))
        ax.plot([anchor_x, anchor_x + GOAL_DEPTH], [goal_y, goal_y],
                color="white", linewidth=2, zorder=3)
        ax.plot([anchor_x, anchor_x + GOAL_DEPTH], [goal_y + GOAL_WIDTH, goal_y + GOAL_WIDTH],
                color="white", linewidth=2, zorder=3)
        post_x = anchor_x if gx == length else anchor_x + GOAL_DEPTH
        ax.plot([post_x, post_x], [goal_y, goal_y + GOAL_WIDTH],
                color="white", linewidth=2.5, zorder=3)

    # Corner flags
    for cx, cy in [(0, 0), (length, 0), (0, width), (length, width)]:
        ax.add_patch(plt.Circle(
            (cx, cy), radius=5,
            color="white", fill=False, linewidth=1, zorder=2
        ))

    # H1 direction labels
    h1_home_arrow = "attacking →" if home_dir_h1 == "ltr" else "← attacking"
    h1_away_arrow = "attacking →" if away_dir_h1 == "ltr" else "← attacking"
    ax.text(60,  width + 3, f"{home_name}  {h1_home_arrow}  (H1)",
            ha="center", va="top", color=home_color,
            fontsize=7.5, alpha=0.85, style="italic")
    ax.text(length - 60, width + 3, f"(H1)  {h1_away_arrow}  {away_name}",
            ha="center", va="top", color=away_color,
            fontsize=7.5, alpha=0.85, style="italic")

    ax.set_aspect("equal")
    ax.axis("off")


# ── Main plot function ─────────────────────────────────────────────────────

def plot_events(
    match: dict,
    home_events: pd.DataFrame,
    away_events: pd.DataFrame,
    event_label: str = "Events",
    logo_path: str   = "Afriskaut.png",
):
    """
    Render a pitch map for a given set of home and away events.

    Parameters
    ----------
    match        : dict from match.json
    home_events  : DataFrame returned by build_plot_data (home slice)
    away_events  : DataFrame returned by build_plot_data (away slice)
    event_label  : label shown in title (e.g. 'Pass', 'Shot')
    logo_path    : path to Afriskaut.png for credit watermark
    """
    home_name  = match.get("home_team_string", "Home")
    away_name  = match.get("away_team_string", "Away")
    home_goals = match.get("home_goals", "")
    away_goals = match.get("away_goals", "")
    home_color, away_color = team_colors(match)

    fig = plt.figure(figsize=(16, 11), facecolor="#1a1a2e")
    ax  = fig.add_axes([0.05, 0.12, 0.90, 0.76])

    draw_pitch(ax, match)

    ax.scatter(
        home_events["x_norm"], home_events["y_norm"],
        color=home_color, s=50, alpha=0.85, zorder=4,
        label=f"{home_name} ({len(home_events)})"
    )
    ax.scatter(
        away_events["x_norm"], away_events["y_norm"],
        color=away_color, s=50, alpha=0.85, zorder=4,
        label=f"{away_name} ({len(away_events)})"
    )

    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.055),
        ncol=2,
        frameon=True,
        framealpha=0.2,
        facecolor="#1a1a2e",
        edgecolor="white",
        fontsize=11,
        markerscale=1.5,
        labelcolor="white"
    )

    # Title block
    fig.text(0.5, 0.93,
             f"{home_name}  {home_goals} – {away_goals}  {away_name}",
             ha="center", va="top",
             color="white", fontsize=15, fontweight="bold")
    fig.text(0.5, 0.895,
             f"{event_label} map  ·  {match.get('date', '')}",
             ha="center", va="top",
             color="#aaaaaa", fontsize=10)

    # Logo
    try:
        logo    = mpimg.imread(logo_path)
        logo_ax = fig.add_axes([0.83, 0.01, 0.12, 0.07])
        logo_ax.imshow(logo)
        logo_ax.axis("off")
    except FileNotFoundError:
        fig.text(0.92, 0.02, "Afriskaut", ha="right", va="bottom",
                 color="#aaaaaa", fontsize=9, style="italic")

    plt.show()
    print(
        f"Plotted {len(home_events) + len(away_events)} '{event_label}' events  "
        f"({len(home_events)} home · {len(away_events)} away)"
    )
