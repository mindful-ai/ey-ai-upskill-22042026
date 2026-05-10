**Purchase Order (PO)**

**Vendor Information:**
- Vendor Name: VendorA
- Vendor Address: (To be filled)
- Contact Person: (To be filled)
- Contact Number: (To be filled)
- Email: (To be filled)

**Order Details:**
- **Item 1:**
  - Item Name: (To be filled)
  - Quantity: (To be filled)
  - Unit Price: (To be filled)
  - Total Amount: (To be calculated)

**Total Order Value:** 500000 INR

**Payment Terms:**
- Payment Method: (To be filled)
- Payment Due Date: (To be filled)

**Delivery Details:**
- Delivery Address: (To be filled)
- Delivery Date: (To be filled)

**Additional Notes:**
- (To be filled)


----------------------------------------------------------------------------------------------

TASK:

The above is the current purchase order format. Add a database agent that will connect to
a database and fetch the vendor information, order details, etc to be added into the purchase order

----------------------------------------------------------------------------------------------

TASK:

When working with UI, diasable approval using ENABLE_HUMAN_APPROVAL in constants.py



TASK:

Scenario: Create a PO for 20 components from VendorB under 800000 INR

- Add LangSmith and trace the agents
- Fix issues with finanace agent
**PO Number:** PO-001
**Date:** 29 April 2026
**Vendor:** VendorB

**Item Details:**

| **Item** | **Quantity** | **Unit Price (INR)** | **Total Amount (INR)** |
| --- | --- | --- | --- |
| Components | 20 | 40000 | 800000 |

**Total Amount:** 800000 INR | Approved: True *** WRONG!! ***

----------------------------------------------------------------------------------------

Study compliance agent:

📜 Compliance Decision: BASED ON THE PROVIDED POLICIES, I WILL VALIDATE THE VENDOR VALIDITY AND APPROVAL RULES.

**VENDOR VALIDITY:**
THE VENDOR DETECTED IS VENDORA. ACCORDING TO POLICY 80 AND POLICY 60, VENDORA IS A VALID VENDOR FOR PURCHASES UNDER 580000 INR AND 560000 INR RESPECTIVELY. SINCE THE TOTAL AMOUNT OF THE PO IS 400,000 INR, WHICH IS LESS THAN BOTH LIMITS, VENDORA IS A VALID VENDOR FOR THIS PURCHASE.

**APPROVAL RULES:**
SINCE VENDORA IS A VALID VENDOR, THE PURCHASE IS ALLOWED UNDER POLICY 80 AND POLICY 60. THEREFORE, THE APPROVAL RULES ARE SATISFIED.

**DECISION:**
PASS

**REASON:**
VENDORA IS A VALID VENDOR FOR PURCHASES UNDER 580000 INR AND 560000 INR, AND THE TOTAL AMOUNT OF THE PO IS WITHIN THESE LIMITS.