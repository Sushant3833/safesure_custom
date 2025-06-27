// Copyright (c) 2025, sushant and contributors
// For license information, please see license.txt

frappe.query_reports["BOM Details from Quotation"] = {
	"filters": [
		{
            fieldname: "quotation",
            label: "Quotation",
            fieldtype: "Link",
            options: "Quotation",
            reqd: 1
        }

	]
};
