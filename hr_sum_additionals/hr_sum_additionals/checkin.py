from hrms.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
from hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules import get_the_rule
from frappe.utils import getdate , get_time
import frappe
from datetime import datetime , timedelta



class CustomCheckin(EmployeeCheckin):
    def before_validate(self):
        shift_type = self.shift
        shift_data = frappe.get_doc("Shift Type" , shift_type )
        late_penalty_after = shift_data.late_penalty_after
        self.custom_late_penalty_after = late_penalty_after
        self.custom_deduction = calculate_dif_time_and_date(self.time , late_penalty_after)
        self.custom_early_diiference = abs(calculate_dif_time_and_date(self.time,shift_data.end_time))

    def on_change(self):
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
