import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Sales Order": [
            {
                "fieldname": "shopify_shop",
                "fieldtype": "Data",
                "label": "Shopify Shop",
                "insert_after": "title",
                "no_copy": 1,
            },
            {
                "fieldname": "shopify_order_id",
                "fieldtype": "Data",
                "label": "Shopify Order ID",
                "insert_after": "shopify_shop",
                "no_copy": 1,
            },
            {
                "fieldname": "shopify_order_name",
                "fieldtype": "Data",
                "label": "Shopify Order Name",
                "insert_after": "shopify_order_id",
                "no_copy": 1,
            },
            {
                "fieldname": "shopify_financial_status",
                "fieldtype": "Data",
                "label": "Shopify Financial Status",
                "insert_after": "shopify_order_name",
                "no_copy": 1,
            },
            {
                "fieldname": "shopify_fulfillment_status",
                "fieldtype": "Data",
                "label": "Shopify Fulfillment Status",
                "insert_after": "shopify_financial_status",
                "no_copy": 1,
            },
        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            existing = frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]})
            if not existing:
                create_custom_field(doctype, field)
            else:
                cf = frappe.get_doc("Custom Field", existing)
                for key, value in field.items():
                    if key not in ("fieldname", "fieldtype"):
                        setattr(cf, key, value)
                cf.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.clear_cache(doctype=doctype)


def delete_custom_fields():
    custom_fields_to_delete = { "Sales Order": ["shopify_shop", "shopify_order_id", 
                                                "shopify_order_name","shopify_financial_status", "shopify_fulfillment_status"] }

    for doctype, fields in custom_fields_to_delete.items(): 
        for field_name in fields: 
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}): 
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True) 
                frappe.db.commit() 
                frappe.clear_cache(doctype=doctype)      