"""Command-line interface for Fantasia.

A Ghostty-grade terminal AI operator modeled after The NeverEnding Story.
"""

import argparse
import sys
import time
from fantasia import __version__
from fantasia.auryn import Auryn
from fantasia.nothing import NothingGauge
from fantasia.oracle import SouthernOracle
from fantasia.ui import GhosttyRenderer, Color, Glyphs
from fantasia.agent import AtreyuAgent


def cmd_demo(args):
    """Run an interactive Ghostty-styled showcase of Fantasia."""
    r = GhosttyRenderer()
    r.banner(active_tab="Ivory Tower")
    r.auryn_header()

    r.card(
        title="AURYN TALISMAN ENGAGED",
        body=[
            "DO WHAT THOU WILT — The ouroboros twins guard your intent.",
            "Each wish shapes Fantasia while anchoring human memory against the void.",
            "Ghostty TrueColor terminal emulation active: 24-bit RGB palette.",
        ],
        tag="STATE",
        color=Color.GOLD,
    )

    print()
    oracle = SouthernOracle()
    res = oracle.consult("How do we rebuild Fantasia from a single grain of sand?")
    r.card(
        title="THE SOUTHERN ORACLE SPEAKS",
        body=[
            res["verdict"],
            f"Gate status: {res['gate']}",
            f"Inference provider: {res['provider']} ({res['model']})",
        ],
        tag="ORACLE",
        color=Color.ORACLE_CYAN,
    )

    print()
    gauge = NothingGauge()
    gauge.record_usage(14_200)
    state = gauge.assess()
    r.card(
        title="THE NOTHING / ENTROPY MONITOR",
        body=[
            f"Context budget: {state.used_tokens:,} / {state.total_tokens:,} tokens ({state.ratio:.1%})",
            f"Radar telemetry: {gauge.ascii_radar()}",
            f"Empress advice: {state.remedy}",
        ],
        tag="NOTHING",
        color=Color.NOTHING_VOID,
    )

    r.footer(status="READY", entropy=state.ratio)


def cmd_wish(args):
    """Grant a human wish through the AURYN talisman."""
    r = GhosttyRenderer()
    auryn = Auryn()
    wish = auryn.grant_wish(args.prompt)

    r.banner(active_tab="Ivory Tower")
    r.auryn_header()

    r.card(
        title=f"WISH RECORDED: {wish.wish_id}",
        body=[
            f"Prompt: {wish.prompt}",
            f"Talisman inscription: {Auryn.INSCRIPTION}",
            f"Remaining human anchors: {auryn.remaining_memory_anchor}",
            "Routing request to the Southern Oracle...",
        ],
        tag="AURYN",
        color=Color.GOLD,
    )

    oracle = SouthernOracle()
    res = oracle.consult(args.prompt)
    print()
    r.card(
        title="ORACLE MANIFESTATION",
        body=[res["verdict"], f"Provider: {res['provider']}"],
        tag="GRANTED",
        color=Color.ORACLE_CYAN,
    )
    r.footer(status="COMPLETE", entropy=0.08)


def cmd_oracle(args):
    """Directly consult the Southern Oracle."""
    r = GhosttyRenderer()
    oracle = SouthernOracle()
    r.banner(active_tab="Oracle Gate")
    
    query = " ".join(args.query)
    print(Color.paint(f"  Consulting the Sphinxes on: '{query}'...", Color.MUTED))
    time.sleep(0.1)

    res = oracle.consult(query)
    r.card(
        title="THE SPHINXES HAVE SPOKEN",
        body=[res["verdict"], f"Gate: {res['gate']}"],
        tag="ORACLE",
        color=Color.ORACLE_CYAN,
    )
    r.footer(status="SPHINX CLEAR", entropy=0.03)


def cmd_atreyu(args):
    """Dispatch the Atreyu agent on an autonomous scout task."""
    r = GhosttyRenderer()
    r.banner(active_tab="Ivory Tower")
    agent = AtreyuAgent()
    task = " ".join(args.task)

    print(Color.paint(f"  Atreyu mounts Artax to scout: '{task}'...", Color.GOLD))
    report = agent.scout(task)

    r.card(
        title=f"ATREYU RECONNAISSANCE REPORT",
        body=report.findings + [f"Verdict: {report.verdict}"],
        tag="SCOUT",
        color=Color.GREEN,
    )
    r.footer(status="SCOUT RETURNED", entropy=0.05)


def cmd_nothing(args):
    """Inspect The Nothing entropy gauge."""
    r = GhosttyRenderer()
    r.banner(active_tab="The Void")
    gauge = NothingGauge()
    if args.tokens:
        gauge.record_usage(args.tokens)
    else:
        gauge.record_usage(28_400)

    state = gauge.assess()
    r.card(
        title="THE NOTHING (DAS NICHTS) TELEMETRY",
        body=[
            f"Threat Level: {state.threat_level}",
            f"Context Allocated: {state.used_tokens:,} / {state.total_tokens:,} ({state.ratio:.1%})",
            f"Frontier Radar: {gauge.ascii_radar()}",
            f"Remedy Protocol: {state.remedy}",
        ],
        tag="VOID",
        color=Color.NOTHING_VOID,
    )
    r.footer(status="MONITOR ACTIVE", entropy=state.ratio)


def main():
    parser = argparse.ArgumentParser(
        prog="fantasia",
        description="A Ghostty-grade terminal AI operator modeled after The NeverEnding Story",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    # demo
    p_demo = subparsers.add_parser("demo", help="Render Ghostty-styled interactive showcase")
    p_demo.set_defaults(func=cmd_demo)

    # wish
    p_wish = subparsers.add_parser("wish", help="Submit a prompt wish to AURYN")
    p_wish.add_argument("prompt", type=str, help="The prompt or desire")
    p_wish.set_defaults(func=cmd_wish)

    # oracle
    p_oracle = subparsers.add_parser("oracle", help="Consult the Southern Oracle directly")
    p_oracle.add_argument("query", nargs="+", help="The question for the Sphinxes")
    p_oracle.set_defaults(func=cmd_oracle)

    # atreyu
    p_atreyu = subparsers.add_parser("atreyu", help="Dispatch autonomous Atreyu agent")
    p_atreyu.add_argument("task", nargs="+", help="The reconnaissance mission")
    p_atreyu.set_defaults(func=cmd_atreyu)

    # nothing
    p_nothing = subparsers.add_parser("nothing", help="Inspect The Nothing entropy gauge")
    p_nothing.add_argument("--tokens", type=int, default=None, help="Simulate observed tokens")
    p_nothing.set_defaults(func=cmd_nothing)

    args = parser.parse_args()

    if not args.command:
        # Default behavior: run demo
        cmd_demo(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
