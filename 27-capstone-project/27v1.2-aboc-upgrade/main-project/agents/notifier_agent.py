from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from tools.email_tool import send_email_tool
from memory.long_term import store_po

console = Console()


def render_full_po(state):
    po = state["po"]

    # ======================
    # 📦 PO HEADER
    # ======================
    header = f"""
[bold]Purchase Order[/bold]

PO Number: {po['po_number']}
Date: {po['date']}
"""

    console.print(Panel(header, title="📄 PO Header", border_style="blue"))

    # ======================
    # 📦 ITEMS TABLE
    # ======================
    items_table = Table(title="📦 Item Details", box=box.ROUNDED)

    items_table.add_column("Item")
    items_table.add_column("Quantity")
    items_table.add_column("Unit Price")
    items_table.add_column("Total")

    for item in po["items"]:
        items_table.add_row(
            item["name"],
            str(item["quantity"]),
            str(item["unit_price"]),
            str(item["total"])
        )

    console.print(items_table)

    # ======================
    # 💰 TOTAL
    # ======================
    console.print(
        Panel(
            f"[bold]Total Amount:[/bold] {po['total_amount']} INR",
            border_style="green"
        )
    )

    # ======================
    # 🏢 VENDOR TABLE
    # ======================
    vendor = po.get("vendor_details", {})

    vendor_table = Table(title="🏢 Vendor Details", box=box.ROUNDED)

    vendor_table.add_column("Field")
    vendor_table.add_column("Value")

    for k, v in vendor.items():
        vendor_table.add_row(k.replace("_", " ").title(), str(v))

    console.print(vendor_table)

    # ======================
    # 📊 STATUS
    # ======================
    status = f"""
Finance: {'✔' if state['finance_ok'] else '✖'}
Compliance: {'✔' if state['compliance_ok'] else '✖'}
Validation: {'✔' if state['validation_ok'] else '✖'}
Approval: {'✔' if state['approved'] else '✖'}
"""

    console.print(Panel(status, title="📊 Status", border_style="cyan"))


def run(state: dict) -> str:
    po = state.get("po")

    if po:
        store_po(str(po))

    message = "PO processed"

    send_email_tool.invoke(message)

    # 🔥 Render full PO
    render_full_po(state)

    return message