import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Customer": [
             {
        "fieldname": "shopify_section",
        "fieldtype": "Section Break",
        "label": "Shopify",
        "insert_after": "loyalty_program_tier",
        "collapsible": 1,
    },
    {
        "fieldname": "shopify_shop",
        "fieldtype": "Data",
        "label": "Shopify Shop",
        "insert_after": "shopify_section",
        "read_only": 1,
        "no_copy": 1,
    },
    {
        "fieldname": "shopify_customer_id",
        "fieldtype": "Data",
        "label": "Shopify Customer ID",
        "insert_after": "shopify_shop",
        "read_only": 1,
        "unique": 1,
        "no_copy": 1,
    },
    {
        "fieldname": "shopify_email",
        "fieldtype": "Data",
        "label": "Shopify Email",
        "insert_after": "shopify_customer_id",
        "read_only": 1,
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
    custom_fields_to_delete = { "Customer": ["shopify_section", "shopify_shop", "shopify_customer_id","shopify_email"] }

    for doctype, fields in custom_fields_to_delete.items(): 
        for field_name in fields: 
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}): 
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True) 
                frappe.db.commit() 
                frappe.clear_cache(doctype=doctype)      