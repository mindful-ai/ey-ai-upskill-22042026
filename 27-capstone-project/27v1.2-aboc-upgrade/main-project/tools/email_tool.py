from langchain.tools import tool

@tool
def send_email_tool(message: str) -> str:
    """
    Send a notification email with the given message.
    """
    print("\n📧 EMAIL SENT:", message)
    return "Email sent"