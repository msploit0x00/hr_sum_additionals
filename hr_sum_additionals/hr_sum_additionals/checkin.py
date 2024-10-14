from hrms.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
from hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules import get_the_rule
from frappe.utils import getdate , get_time , cint, get_datetime
import frappe
from datetime import datetime , timedelta
from frappe import _


from hrms.hr.doctype.shift_assignment.shift_assignment import (
	get_actual_start_end_datetime_of_shift,
)


class CustomCheckin(EmployeeCheckin):
    def before_validate(self):
        pass
    
    def validate(self):
       self.validate_duplicate_log()
       self.fetch_shift()
		# self.set_geolocation_from_coordinates()
        # shift_type = self.shift
        # shift_data = frappe.get_doc("Shift Type" , shift_type )
        # late_penalty_after = shift_data.late_penalty_after
        # self.custom_late_penalty_after = late_penalty_after
        # self.custom_deduction = calculate_dif_time_and_date(self.time , late_penalty_after)
        # device_log = self.device_log
        # if device_log:
        #     log = frappe.get_doc("Device Log", device_log)
        #     if log.punch == 1:

        #         self.custom_early_diiference = abs(calculate_dif_time_and_date(log.time,shift_data.end_time))

    def after_insert(self):
        employee = self.employee
        doctype = "Employee Checkin"
        datatime = self.time
        date = getdate(datatime)
        name = self.name
        get_the_rule (employee , date , doctype ,  name )



# def calculate_dif_time_and_date(futureDate1,timeNow):
#     futureDate = datetime.strptime(str(futureDate1), "%Y-%m-%d %H:%M:%S")
#     nowParts = datetime.strptime(str(timeNow), "%H:%M:%S").time()
#     nowDate = datetime(futureDate.year, futureDate.month, futureDate.day, int(nowParts.hour), int(nowParts.minute), int(nowParts.second))
#     timeDifference = (futureDate - nowDate)
#     totalAmount = (timeDifference.total_seconds() / 60) 
#     result = totalAmount / 60
#     print(result)
#     return result

# def calculate_dif_time_and_date(futureDate1, timeNow):
#     futureDate = datetime.strptime(futureDate1, "%Y-%m-%d %H:%M:%S")
#     nowParts = datetime.strptime(str(timeNow), "%H:%M:%S")
#     nowDate = datetime.combine(futureDate.date(), nowParts)
#     timeDifference = futureDate - nowDate
#     totalHours = timeDifference.total_seconds() / 3600
#     print(totalHours)
#     totalHoursStr = str(totalHours)
#     return totalHoursStr


def calculate_dif_time_and_date(futureDate1, timeNow):
    # # Ensure timeNow is a string
    # if not isinstance(timeNow, str):
    #     raise TypeError("timeNow should be a string in '%H:%M:%S' format.")
    
    futureDate = datetime.strptime(futureDate1, "%Y-%m-%d %H:%M:%S")
    
    nowParts = datetime.strptime(str(timeNow), "%H:%M:%S").time()
    
   
    nowDate = datetime.combine(futureDate.date(), nowParts)
    
   
    timeDifference = futureDate - nowDate
    
  
    totalHours = timeDifference.total_seconds() / 3600
    
    print(totalHours)
    return totalHours




def calculate_dif_time_and_date2(futureDate1, timeNow):
    futureDate = datetime.strptime(str(futureDate1), "%Y-%m-%d %H:%M:%S")
    nowParts = datetime.strptime(str(timeNow), "%H:%M:%S").time()
    nowDate = datetime(futureDate.year, futureDate.month, futureDate.day, nowParts.hour, nowParts.minute, nowParts.second)
    
    timeDifference = futureDate - nowDate
    total_hours = timeDifference.total_seconds() / 3600
    
    print(total_hours)
    return total_hours


def calculate_dif_time_and_date3(futureDate1, timeNow):
    # Parse the future date and time
    futureDate = datetime.strptime(futureDate1, "%d-%m-%Y %H:%M:%S")
    # Parse the current time
    nowParts = datetime.strptime(timeNow, "%H:%M:%S").time()
    
    # Combine the date part of futureDate with the nowParts time to create a datetime object
    combined_now = datetime.combine(futureDate.date(), nowParts)
    
    # Calculate the difference
    timeDifference = futureDate - combined_now
    # Convert the difference to total minutes
    total_minutes = timeDifference.total_seconds() / 60
    # Convert minutes to hours
    total_hours = total_minutes / 60
    
    # Print both minutes and hours for clarity
    print(f"Total difference: {total_minutes:.2f} minutes ({total_hours:.2f} hours)")
    
    return total_hours







def validate_duplicate_log(self):
		doc = frappe.db.exists(
			"Employee Checkin",
			{
				"employee": self.employee,
				"time": self.time,
				"name": ("!=", self.name),
				"log_type": self.log_type,
			},
		)
		if doc:
			doc_link = frappe.get_desk_link("Employee Checkin", doc)
			frappe.throw(
				_("This employee already has a log with the same timestamp.{0}").format("<Br>" + doc_link)
			)

def fetch_shift(self):
		shift_actual_timings = get_actual_start_end_datetime_of_shift(
			self.employee, get_datetime(self.time), True
		)
		if shift_actual_timings:
			if (
				shift_actual_timings.shift_type.determine_check_in_and_check_out
				== "Strictly based on Log Type in Employee Checkin"
				and not self.log_type
				and not self.skip_auto_attendance
			):
				frappe.throw(
					_("Log Type is required for check-ins falling in the shift: {0}.").format(
						shift_actual_timings.shift_type.name
					)
				)
			if not self.attendance:
				self.shift = shift_actual_timings.shift_type.name
				self.shift_actual_start = shift_actual_timings.actual_start
				self.shift_actual_end = shift_actual_timings.actual_end
				self.shift_start = shift_actual_timings.start_datetime
				self.shift_end = shift_actual_timings.end_datetime
		else:
			self.shift = None