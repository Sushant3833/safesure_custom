# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        {"label": "Item", "fieldname": "item_code", "fieldtype": "HTML", "width": 300},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 250},
        {"label": "Make", "fieldname": "custom_brand", "fieldtype": "Data", "width": 150},
        # {"label": "Model Number", "fieldname": "custom_model", "fieldtype": "Data", "width": 150},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 80},
        {"label": "Unit Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 100}
    ]

    result = []

    selected_boms = filters.get("bom") or []
    if isinstance(selected_boms, str):
        import json
        selected_boms = json.loads(selected_boms)

    for idx, root_bom in enumerate(selected_boms):
        stack = [{
            "bom": root_bom,
            "indent": 0,
            "as_bom_header": 1,
            "is_first": 1
        }]

        while stack:
            entry = stack.pop()
            current_bom = entry.get("bom")
            indent = entry.get("indent", 0)
            as_bom_header = entry.get("as_bom_header")
            is_first = entry.get("is_first", 0)

            if as_bom_header:
                result.append({
                    "item_code": ("&nbsp;&nbsp;" * indent) + f"<b>▶ BOM: {current_bom}</b>",
                    "item_name": "",
                    "custom_brand": "",
                    # "custom_model": "",
                    "qty": "",
                    "rate": "",
                    "amount":""
                })

                items = frappe.get_all("BOM Item",
                    filters={"parent": current_bom},
                    fields=["item_code", "item_name", "custom_brand", "custom_model", "qty", "rate","amount", "bom_no"],
                    order_by="idx"
                )

                for item in reversed(items):
                    item_code_display = ("&nbsp;&nbsp;" * (indent + 1)) + item.item_code
                    if is_first:
                        item_code_display = f"<b>{item_code_display}</b>"

                    if item.bom_no:
                        stack.append({
                            "bom": item.bom_no,
                            "indent": indent + 2,
                            "as_bom_header": 1,
                            "is_first": 0
                        })

                    stack.append({
                        "row": {
                            "item_code": item_code_display,
                            "item_name": item.item_name,
                            "custom_brand": item.custom_brand,
                            # "custom_model": item.custom_model,
                            "qty": item.qty,
                            "rate": item.rate,
                            "amount":item.amount
                        }
                    })

            elif entry.get("row"):
                result.append(entry.get("row"))

    return columns, result
