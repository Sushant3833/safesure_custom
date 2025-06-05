// Copyright (c) 2025, sushant and contributors
// For license information, please see license.txt

frappe.query_reports["BOM Custom Report"] = {
	"filters": [
        {
            fieldname: "bom",
            label: "BOM",
            fieldtype: "MultiSelectList",
            get_data: function(txt) {
                return frappe.db.get_link_options("BOM", txt);
            },
            reqd: 1
        }
    ]
};
