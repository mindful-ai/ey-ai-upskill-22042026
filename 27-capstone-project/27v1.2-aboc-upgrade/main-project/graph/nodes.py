"""
LangGraph node wrappers with Rich console output (DICT-SAFE VERSION)
"""

from agents import (
    planner_agent,
    procurement_agent,
    finance_agent,
    compliance_agent,
    validator_agent,
    approval_agent,
    notifier_agent,
    vendor_agent
)

from memory.short_term import update_history

# 🔥 Rich imports
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


# ================================
# 🎨 UI Helpers
# ================================

def print_section(title):
    console.print(
        Panel(f"[bold cyan]{title}[/bold cyan]", expand=False)
    )


def display_po_preview(po):
    """
    Lightweight preview for structured PO (dict-safe)
    """
    if not isinstance(po, dict):
        console.print("[red]Invalid PO format[/red]")
        return

    table = Table(title="📦 PO Preview", box=box.ROUNDED)

    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("PO Number", str(po.get("po_number")))
    table.add_row("Vendor", str(po.get("vendor_name")))
    table.add_row("Total Amount", f"{po.get('total_amount')} INR")

    console.print(table)


# ================================
# 🧠 Nodes
# ================================

def planner_node(state):
    print_section("PLANNER")

    state["plan"] = planner_agent.run(state["user_input"])
    console.print(state["plan"])

    return state


def procurement_node(state):
    print_section("PROCUREMENT")

    state["po"] = procurement_agent.run(state["user_input"])

    # ✅ FIX: use dict-safe preview
    display_po_preview(state["po"])

    return state


def vendor_node(state):
    print_section("VENDOR ENRICHMENT")

    state["po"] = vendor_agent.run(state)

    # Optional preview after enrichment
    display_po_preview(state["po"])

    return state


def finance_node(state):
    print_section("FINANCE")

    state["finance_ok"] = finance_agent.run(state["po"])

    if state["finance_ok"]:
        console.print("[green]✅ Finance Approved[/green]")
    else:
        console.print("[red]❌ Finance Rejected[/red]")

    return state


def compliance_node(state):
    print_section("COMPLIANCE")

    state["compliance_ok"] = compliance_agent.run(state["po"])

    if state["compliance_ok"]:
        console.print("[green]✅ Compliance Passed[/green]")
    else:
        console.print("[red]❌ Compliance Failed[/red]")

    return state


def validator_node(state):
    print_section("VALIDATOR")

    state["validation_ok"] = validator_agent.run(state)

    if state["validation_ok"]:
        console.print("[green]✅ Validation Passed[/green]")
    else:
        console.print("[red]❌ Validation Failed[/red]")

    return state


def approval_node(state):
    print_section("APPROVAL")

    state["approved"] = approval_agent.run(state)

    if state["approved"]:
        console.print("[bold green]✔ Approved[/bold green]")
    else:
        console.print("[bold red]✖ Rejected[/bold red]")

    return state


def notifier_node(state):
    print_section("NOTIFIER")

    state["notification"] = notifier_agent.run(state)

    # Short-term memory
    state["history"] = update_history(state)

    console.print(
        Panel(
            state["history"],
            title="🧠 Session Summary",
            border_style="blue"
        )
    )

    return state