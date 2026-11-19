"""Ghostty-grade ANSI & TrueColor terminal renderer for Fantasia.

Provides crisp 24-bit RGB palette, rounded borders, AURYN dual-snake glyphs,
pill badges, and window framing reminiscent of modern GPU terminals.
"""

import sys
import shutil
from typing import List, Optional


class Color:
    """TrueColor (24-bit ANSI) escape sequence helper."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Palette
    OBSIDIAN = (12, 14, 20)      # #0c0e14 - deep Ghostty background
    PANEL = (20, 24, 34)         # #141822 - terminal panel surface
    INK = (232, 236, 242)        # #e8ecf2 - crisp alabaster text
    MUTED = (120, 130, 145)      # #788291 - steel secondary
    BORDER = (46, 54, 70)        # #2e3646 - subtle window borders
    GOLD = (212, 175, 55)        # #d4af37 - AURYN primary gold
    GOLD_LIGHT = (243, 229, 171) # #f3e5ab - AURYN highlight
    ORACLE_CYAN = (72, 201, 176) # #48c9b0 - Southern Oracle teal
    ORACLE_BLUE = (0, 210, 255)  # #00d2ff - Sphinx beam
    NOTHING_VOID = (224, 86, 253)# #e056fd - The Nothing magenta
    VOID_DARK = (48, 25, 52)     # #301934 - entropy deep shade
    GREEN = (80, 200, 120)       # emerald badge
    AMBER = (245, 166, 35)       # warm warning
    RED = (255, 95, 87)          # macOS red dot

    @classmethod
    def fg(cls, r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    @classmethod
    def bg(cls, r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m"

    @classmethod
    def paint(cls, text: str, rgb: tuple, bold: bool = False, dim: bool = False) -> str:
        prefix = cls.fg(*rgb)
        if bold:
            prefix += cls.BOLD
        if dim:
            prefix += cls.DIM
        return f"{prefix}{text}{cls.RESET}"


class Glyphs:
    """Unicode box drawing and Fantasia / Ghostty symbolic glyphs."""
    AURYN_PAIR = "∞"
    AURYN_SNAKES = "ᚢᛟᚢ"
    DOT = "•"
    ARROW_RIGHT = "→"
    ARROW_UP_RIGHT = "↗"
    ORACLE_EYE = "◉"
    SPHINX = "🜚"
    NOTHING_PARTICLE = "░"
    NOTHING_DENSE = "▓"
    CORNER_TL = "╭"
    CORNER_TR = "╮"
    CORNER_BL = "╰"
    CORNER_BR = "╯"
    LINE_H = "─"
    LINE_V = "│"
    SPLIT_L = "├"
    SPLIT_R = "┤"
    SPLIT_T = "┬"
    SPLIT_B = "┴"
    CROSS = "┼"


class GhosttyRenderer:
    """Renders stylized terminal UI frames, headers, and status cards."""

    def __init__(self, stream=None):
        self._stream = stream

    @property
    def stream(self):
        return self._stream if self._stream is not None else sys.stdout

    @property
    def term_width(self) -> int:
        return min(shutil.get_terminal_size((88, 24)).columns, 110)

    def hr(self, char: str = Glyphs.LINE_H, color=Color.BORDER) -> None:
        line = char * (self.term_width - 2)
        print(Color.paint(line, color), file=self.stream)

    def banner(self, active_tab: str = "Ivory Tower") -> None:
        """Render top Ghostty window bar with macOS controls and Fantasia title."""
        w = self.term_width
        dots = (
            Color.paint("●", Color.RED) + " " +
            Color.paint("●", Color.AMBER) + " " +
            Color.paint("●", Color.GREEN)
        )
        tabs = [
            ("Ivory Tower", active_tab == "Ivory Tower"),
            ("Oracle Gate", active_tab == "Oracle Gate"),
            ("The Void", active_tab == "The Void"),
        ]
        tab_rendered = []
        for name, active in tabs:
            if active:
                tab_rendered.append(Color.paint(f"[{name}]", Color.GOLD, bold=True))
            else:
                tab_rendered.append(Color.paint(f" {name} ", Color.MUTED))

        top_line = (
            Color.paint(Glyphs.CORNER_TL + Glyphs.LINE_H * (w - 2) + Glyphs.CORNER_TR, Color.BORDER)
        )
        print(top_line, file=self.stream)

        # Header row
        bar_content = f" {dots}   " + " ".join(tab_rendered)
        title = Color.paint("FANTASIA // CLI", Color.INK, bold=True)
        # Approximate plain text width calculation
        plain_len = 16 + sum(len(t[0]) + 4 for t in tabs) + len("FANTASIA // CLI")
        spacing = max(2, w - plain_len - 6)
        row = f"{Color.paint(Glyphs.LINE_V, Color.BORDER)} {bar_content}{' ' * spacing}{title} {Color.paint(Glyphs.LINE_V, Color.BORDER)}"
        print(row, file=self.stream)

        sep = Color.paint(Glyphs.SPLIT_L + Glyphs.LINE_H * (w - 2) + Glyphs.SPLIT_R, Color.BORDER)
        print(sep, file=self.stream)

    def auryn_header(self, entropy_ratio: float = 0.05) -> None:
        """Display the ornate talisman header and inscription."""
        w = self.term_width
        auryn_art = [
            "          .---.             .---.          ",
            "         /     \\           /     \\         ",
            "        |   ()  \\_________/  ()   |        ",
            "         \\       \\  AURYN  /     /         ",
            "          `---'---'       `---'---'          ",
        ]
        gold = Color.GOLD
        gold_lt = Color.GOLD_LIGHT
        print(Color.paint("  " + "═" * (w - 4), gold, dim=True), file=self.stream)
        print(Color.paint("   ✦  D O   W H A T   T H O U   W I L T  ✦", gold_lt, bold=True), file=self.stream)
        print(Color.paint("      auryn token governor · southern oracle v0.1.0", Color.MUTED), file=self.stream)
        print(Color.paint("  " + "─" * (w - 4), Color.BORDER), file=self.stream)

    def card(self, title: str, body: List[str], tag: str = "ORACLE", color=Color.ORACLE_CYAN) -> None:
        """Render a Ghostty-styled bordered card with badge tag."""
        w = self.term_width
        badge = Color.paint(f"[{tag}]", color, bold=True)
        header_text = f" {badge} {Color.paint(title, Color.INK, bold=True)} "
        pad_len = max(2, w - len(f" [{tag}] {title} ") - 4)
        top = (
            Color.paint(Glyphs.CORNER_TL + Glyphs.LINE_H * 2, Color.BORDER) +
            header_text +
            Color.paint(Glyphs.LINE_H * pad_len + Glyphs.CORNER_TR, Color.BORDER)
        )
        print(top, file=self.stream)

        for line in body:
            avail = w - 6
            wrapped = line[:avail]
            spacing = max(0, avail - len(wrapped))
            print(
                f"{Color.paint(Glyphs.LINE_V, Color.BORDER)}  {Color.paint(wrapped, Color.INK)}{' ' * spacing}  {Color.paint(Glyphs.LINE_V, Color.BORDER)}",
                file=self.stream
            )

        bot = Color.paint(Glyphs.CORNER_BL + Glyphs.LINE_H * (w - 2) + Glyphs.CORNER_BR, Color.BORDER)
        print(bot, file=self.stream)

    def footer(self, status: str = "READY", entropy: float = 0.04) -> None:
        """Render bottom status bar with telemetry."""
        w = self.term_width
        sep = Color.paint(Glyphs.SPLIT_L + Glyphs.LINE_H * (w - 2) + Glyphs.SPLIT_R, Color.BORDER)
        print(sep, file=self.stream)

        entropy_bar = self._entropy_bar(entropy)
        status_badge = Color.paint(f" ● {status} ", Color.GREEN, bold=True)
        nothing_badge = Color.paint(f"NOTHING ENTROPY: {entropy:.1%}", Color.NOTHING_VOID)
        
        info = f" {status_badge}  {nothing_badge} {entropy_bar}"
        raw_len = len(f"  {status}   NOTHING ENTROPY: {entropy:.1%} [||||||||||] ")
        spacing = max(2, w - raw_len - len("auryn: bound ") - 4)
        bot_content = f"{info}{' ' * spacing}{Color.paint('auryn: bound', Color.GOLD)}"

        print(f"{Color.paint(Glyphs.LINE_V, Color.BORDER)}{bot_content} {Color.paint(Glyphs.LINE_V, Color.BORDER)}", file=self.stream)
        bot_line = Color.paint(Glyphs.CORNER_BL + Glyphs.LINE_H * (w - 2) + Glyphs.CORNER_BR, Color.BORDER)
        print(bot_line, file=self.stream)

    def _entropy_bar(self, entropy: float, width: int = 12) -> str:
        fill = int(entropy * width)
        empty = width - fill
        filled_str = Color.paint("■" * fill, Color.NOTHING_VOID)
        empty_str = Color.paint("·" * empty, Color.MUTED)
        return f"[{filled_str}{empty_str}]"
