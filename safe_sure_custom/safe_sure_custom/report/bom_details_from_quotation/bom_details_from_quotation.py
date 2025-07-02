# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        {"label": "Item", "fieldname": "item_code", "fieldtype": "HTML", "width": 300},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Description", "fieldname": "description", "fieldtype": "Data", "width": 300},
        {"label": "Make", "fieldname": "custom_brand", "fieldtype": "Data", "width": 150},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 80},
        {"label": "Brand Discount", "fieldname": "custom_brand_discount", "fieldtype": "Float", "width": 120},
        {"label": "Standard Company Price", "fieldname": "custom_standard_company_price", "fieldtype": "Currency", "width": 150},
        {"label": "Unit Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 100}
    ]

    result = []

    quotation = filters.get("quotation")
    if not quotation:
        return columns, []

    quotation_items = frappe.get_all("Quotation Item",
        filters={"parent": quotation},
        fields=["item_code", "item_name", "description", "custom_bom", "qty", "rate", "amount"],
        order_by="idx"
    )

    for q_item in quotation_items:
        if not q_item.custom_bom:
            continue

        # Header for BOM from Quotation
        result.append({
            "item_code": f"<b>★ BOM: {q_item.custom_bom}</b>",
            "item_name": q_item.item_name,
            "description": q_item.description,
            "custom_brand": "",
            "custom_brand_discount": "",
            "custom_standard_company_price": "",
            "qty": q_item.qty,
            "rate": q_item.rate,
            "amount": q_item.amount
        })

        # Add its BOM items (bold), and recurse for bom_no
        add_bom_items(result, q_item.custom_bom, indent=1, bold=True)

    return columns, result


def add_bom_items(result, bom_name, indent=1, bold=False):
    items = frappe.get_all("BOM Item",
        filters={"parent": bom_name},
        fields=[
            "item_code", "item_name", "description",
            "custom_brand", "custom_model", "custom_brand_discount",
            "custom_standard_company_price", "qty", "rate", "amount", "bom_no"
        ],
        order_by="idx"
    )

    for item in items:
        item_code = ("&nbsp;&nbsp;" * indent) + item.item_code
        if bold:
            item_code = f"<b>{item_code}</b>"

        result.append({
            "item_code": item_code,
            "item_name": item.item_name,
            "description": item.description,
            "custom_brand": item.custom_brand,
            "custom_brand_discount": item.custom_brand_discount,
            "custom_standard_company_price": item.custom_standard_company_price,
            "qty": item.qty,
            "rate": item.rate,
            "amount": item.amount
        })

        if item.bom_no:
            # Sub BOM header
            result.append({
                "item_code": ("&nbsp;&nbsp;" * (indent + 1)) + f"<b>▶ Sub BOM: {item.bom_no}</b>",
                "item_name": "",
                "description": "",
                "custom_brand": "",
                "custom_brand_discount": "",
                "custom_standard_company_price": "",
                "qty": "",
                "rate": "",
                "amount": ""
            })

            # Recurse to sub BOM
            add_bom_items(result, item.bom_no, indent=indent + 2, bold=False)
