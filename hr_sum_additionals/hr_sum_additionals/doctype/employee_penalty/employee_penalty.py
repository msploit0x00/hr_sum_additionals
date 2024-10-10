# Copyright (c) 2024, 1 and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules import get_the_rule



class EmployeePenalty(Document):
	def on_change(self):
		if self.docstatus == 1:
			get_the_rule(self.employee , self.penalty_date , "Employee Penalty" , self.name)
