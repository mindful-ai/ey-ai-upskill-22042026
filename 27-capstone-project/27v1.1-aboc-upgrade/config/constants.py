"""
Global constants and business rules for ABOC system
"""

# ================================
# 💰 Finance Rules
# ================================

# Maximum amount allowed for auto-approval
APPROVAL_THRESHOLD = 500000

# Hard upper limit (beyond which always reject)
MAX_ALLOWED_AMOUNT = 1000000


# ================================
# 🏢 Vendor Rules
# ================================

APPROVED_VENDORS = [
    "VendorA",
    "VendorB",
    "VendorC"
]


# ================================
# 📦 Default PO Values
# ================================

DEFAULT_ITEM = "Sensors"
DEFAULT_QUANTITY = 50


# ================================
# 🧠 RAG Settings
# ================================

# Number of documents to retrieve
RAG_TOP_K = 3


# ================================
# 🧪 Demo Settings
# ================================

# Toggle human approval (for UI/API mode)
ENABLE_HUMAN_APPROVAL = True

# Auto-approve when running via API/UI
AUTO_APPROVE_FOR_API = True


# ================================
# ⚙️ LLM Settings (fallback usage)
# ================================

DEFAULT_TEMPERATURE = 0.2


# ================================
# 📊 Logging / Debug
# ================================

ENABLE_VERBOSE_LOGGING = True