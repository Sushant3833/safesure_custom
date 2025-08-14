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

	],
    formatter: function (value, row, column, data, default_formatter) {
        let v = default_formatter(value, row, column, data);
    
        if (column.fieldname === "item_code" && data) {
          const pad = ((data.indent_level || 0) * 16); // pixels
          const weight = data.is_bold ? "font-weight:600;" : "";
          return `<span style="display:inline-block;padding-left:${pad}px;${weight}">${v}</span>`;
        }
    
        return v;
      }
};
