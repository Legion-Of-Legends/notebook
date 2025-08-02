import os
import re
import datetime as dt
from bs4 import BeautifulSoup

with open("../Tasks/README.md") as f:
    task_tracker = f.read()

# filter data
task_time = dt.datetime.strptime(task_tracker.split("## Date:")[1].strip().split("\n")[0].strip(), "%d %B, %Y").date()
task_date = task_time.day
task_month = task_time.month
task_year = task_time.year
next_day = dt.datetime.now() + dt.timedelta(days=1)

member_data_all = task_tracker.split("\n")[2:]
member_data = {}
member_name_github = {}
count = 0
while count < len(member_data_all):
    if member_data_all[count].startswith("##"):
        member_name = member_data_all[count].split("##")[1].strip().split("]")[0].strip()[1:]
        member_github = member_data_all[count].split("##")[1].strip().split("(")[1].strip()[:-1]
        member_name_github[member_name] = member_github
        member_task={}
        for i in range(count + 1, len(member_data_all)):
            if member_data_all[i].startswith("##"):
                break
            elif member_data_all[i].startswith("|--") or member_data_all[i].startswith("|Tasks") or member_data_all[i].strip() == "":
                continue
            else:
                task = member_data_all[i].strip().split("|")
                member_task[task[1].strip()] = (True if "[x]" in task[2].strip().lower() else False)
                # member_task[task[0].strip()] = task[1].strip()
        member_data[member_name] = member_task
    count += 1

# Create directory for reports if it doesn't exist
file_route = f"../Reports/{task_year}/{task_time.strftime("%B")}.md"
os.makedirs(os.path.dirname(file_route), exist_ok=True)
if not os.path.exists(file_route):
    with open(file_route, "w") as f:
        f.write("")

# Getting previous report
previous_report = {}
with open(file_route, "r") as f:
    previous_report_file = f.read()
    if previous_report_file.strip()=="":
        f.close()
    else:
        tbody = BeautifulSoup(previous_report_file, "html.parser").find("tbody")
        current_member = None
        for row in tbody.find_all("tr"):
            cells = row.find_all("td")
            if 'rowspan' in cells[0].attrs:
                current_member = cells[0].text.strip()
                data = {
                   "task": cells[1].text.strip(),
                   "total": cells[2].text.strip(),
                   "completed": cells[3].text.strip(),
                   "incompleted": cells[4].text.strip()
                 }   
                previous_report[current_member] = [data]
            else:
                data = {
                    "task": cells[0].text.strip(),
                    "total": (cells[1].text.strip()),
                    "completed": (cells[2].text.strip()),
                    "incompleted": (cells[3].text.strip())
                }
                previous_report[current_member].append(data)



# Merging previous report with current data
Merged_Data = {}
for member, tasks in member_data.items():
    Merged_Data[member] = []
    if member in previous_report:
        for task, completed in tasks.items():
            if task in [i["task"] for i in previous_report[member]]:
                previous_task = next((item for item in previous_report[member] if item['task'] == task), None)
                if previous_task:
                    total = int(previous_task['total']) + 1
                    completed_count = int(previous_task['completed']) + (1 if completed else 0)
                    incompleted_count = int(previous_task['incompleted']) + (0 if completed else 1)
                    Merged_Data[member].append({
                        "task": task,
                        "total": total,
                        "completed": completed_count,
                        "incompleted": incompleted_count
                    })
                else:
                    Merged_Data[member].append({
                        "task": task,
                        "total": 1,
                        "completed": 1 if completed else 0,
                        "incompleted": 0 if completed else 1
                    })
            else:
                Merged_Data[member].append({
                    "task": task,
                    "total": 1,
                    "completed": 1 if completed else 0,
                    "incompleted": 0 if completed else 1
                })
    else:
        for task, completed in tasks.items():
            Merged_Data[member].append({
                "task": task,
                "total": 1,
                "completed": 1 if completed else 0,
                "incompleted": 0 if completed else 1
            })





# Getting data from tasks according to Task Setter.md
with open("../Tasks/Task Setter.md", "r") as f:
    data=f.read().split("\n")
    count=0
    task_setter_data={}
    while count<len(data):
        current_line=data[count]
        if current_line.startswith("##"):
            username = current_line.split("##")[1].strip().split("]")[0].strip()[1:]
            user_tasks={}
            for i in range(count+1, len(data)):
                inline_data=data[i]
                if inline_data.startswith("##"):
                    break
                elif inline_data.startswith("|Task") or inline_data.startswith("|-") or not inline_data.strip():
                    continue
                else:
                    inline_data=[j.strip() for j in inline_data.split("|")][1:-1]
                    task_data={
                            "from":inline_data[1],
                            "to":inline_data[2],
                            "off_days":int(inline_data[3]) if inline_data[3]!='-' else 0,
                            "on_days":int(inline_data[4]) if inline_data[4]!='-' else 1,
                            "weekoff":[k.lower() for k in inline_data[5].split(',')] if inline_data[5]!='-' else None,
                            "status":inline_data[6],
                            "description":inline_data[7]
                            }
                    user_tasks[inline_data[0]]=task_data
                task_setter_data[username]=user_tasks
        count+=1



# Writing the report to a markdown file

with open(file_route, "w") as f:
    f.write(f"# Task Tracker Report for {task_time.strftime('%B %Y')}\n\n")
    table_data = """
    <table>
    <thead>
    <tr>
        <th>Member</th>
        <th>Task</th>
        <th>Total Days</th>
        <th>Completed</th>
        <th>Incompleted</th>
        <th>Description</th>
    </tr>
    </thead>\n
    <tbody>
    """
    for member, tasks in Merged_Data.items():
        taskbody = ""
        task_count = 0
        for task in tasks:
            if task_count == 0:
                taskbody += f"""
                <tr>
                <td rowspan="{len(tasks)}"><a href="{member_name_github[member]}">{member}</a></td>
                <td>{task['task']}</td>
                <td>{task['total']}</td>
                <td>{task['completed']}</td>
                <td>{task['incompleted']}</td>
                <td>{task_setter_data[member][task['task']]['description']}</td>
                </tr>\n
                """
                task_count += 1
                continue
            taskbody += f"""
            <tr>
            <td>{task['task']}</td>
            <td>{task['total']}</td>
            <td>{task['completed']}</td>
            <td>{task['incompleted']}</td>
            <td>{task_setter_data[member][task['task']]['description']}</td>
            </tr>\n
            """
            task_count += 1
        table_data += taskbody
    table_data += """
        </tbody>
        </table>
        """
    table_data = '\n'.join(re.sub(r'^\s+', '', line) for line in table_data.splitlines())
    f.write(table_data)







# Reseting the task file

def parse_date_safe(date_str, fmt="%d.%m.%Y"):
    try:
        return dt.datetime.strptime(date_str, fmt)
    except ValueError:
        return None

def validity_check(test_task_data):
    if test_task_data["from"]=='-' or test_task_data["to"]=='-':
        pass
    elif parse_date_safe(test_task_data["from"])==None:
        return [False, "❌Invalid From Date"]
    elif parse_date_safe(test_task_data["to"])==None:
        return [False, "❌Invalid To Date"]
    elif parse_date_safe(test_task_data["from"])>parse_date_safe(test_task_data["to"]):
       return [False, "❌To date should be after From Date"]
    elif parse_date_safe(test_task_data["from"])>next_day:
        return [False, f"Will start after{(next_day-parse_date_safe(test_task_data['from'])).days} day/s"]
    elif parse_date_safe(test_task_data["to"])<next_day:
        return [False, "Task Expired"]

    elif not is_on_day(base_date_str=writting_task["from"], check_date_str=next_day, off_days=writting_task["off_days"], on_days=writting_task["on_days"]):
        return [False, "On/Off Break Day"]

    elif (writting_task["weekoff"]!=None and next_day.strftime("%a").lower() in writting_task["weekoff"]):
        return [False, "WeekOff Day"]
    return [True, "✅"]


def is_on_day(base_date_str, check_date_str, off_days, on_days):
    base_date = dt.datetime.strptime(base_date_str, "%d.%m.%Y").date() if base_date_str!="-" else dt.datetime.now().date()
    check_date = check_date_str.date()
    cycle_length = off_days + on_days
    days_passed = (check_date - base_date).days
    if days_passed < 0:
        return False
    day_in_cycle = days_passed % cycle_length
    return day_in_cycle >= off_days


with open("../Tasks/README.md", "w") as f:
    new_write = f"## Date: {next_day.strftime('%d %B, %Y')}\n\n"
    for i in task_setter_data.keys():
        max_len=0
        for j in task_setter_data[i].keys():
            if max_len<len(j):
                max_len=len(j)
        new_write+=f"\n## [{i}]({member_name_github[i]})\n|Tasks{' '*(max_len-5)} |Completed{' '*19}|\n|{'-'*max_len}-|{'-'*28}|\n"
        for j in task_setter_data[i].keys():
            writting_task=task_setter_data[i][j]
            task_validity_check=validity_check(task_setter_data[i][j])
            # if writting_task["from"]!="-":
            #     if next_day<parse_date_safe(writting_task["from"]):
            #         continue
            # if writting_task["to"]!="-":
            #     if next_day>parse_date_safe(writting_task["to"]):
            #         continue
            # if not is_on_day(base_date_str=writting_task["from"], check_date_str=next_day, off_days=writting_task["off_days"], on_days=writting_task["on_days"]):
            #     continue
            # if writting_task["weekoff"]!=None:
            #     if next_day.strftime("%a").lower() in writting_task["weekoff"]:
            #         continue
            if not validity_check(task_setter_data[i][j])[0]:
                continue
            new_write+=f"|{j}{' '*(max_len-len(j))} | <ul><li> [ ] done</li></ul>|\n"
    f.write(new_write)



# Resetting the setter file


with open("../Tasks/Task Setter.md", "w") as f:
    new_setter_write=""
    for i in task_setter_data.keys():
        max_task_title_len: int=0
        max_date_len: int=10
        max_description_len: int=13
        max_status_len: int=8
        max_weekoff_len: int=12
        for j in task_setter_data[i].keys():
            if max_task_title_len<len(j):
                max_task_title_len=len(j)
            current_description_len=len(task_setter_data[i][j]["description"])
            if max_description_len<current_description_len:
                max_description_len=current_description_len
            current_weekoff_len=len(task_setter_data[i][j]["weekoff"])*4+2 if task_setter_data[i][j]["weekoff"] else 0
            if max_weekoff_len<current_weekoff_len:
                max_weekoff_len=current_weekoff_len
            current_status_len=len(task_setter_data[i][j]["status"])
            if max_status_len<current_status_len:
                max_status_len=current_status_len
        new_setter_write+=f"\n## [{i}]({member_name_github[i]})\n|Tasks{' '*(max_task_title_len-5)}|Form{' '*(max_date_len-4)}|To{' '*(max_date_len-2)}|Offdays |Ondays |Weekday Off{' '*(max_weekoff_len-12)} |Status{" "*(max_status_len-6)}|Description{' '*(max_description_len-11)}|\n|{'-'*max_task_title_len}|{'-'*max_date_len}|{'-'*max_date_len}|{'-'*8}|{'-'*7}|{'-'*max_weekoff_len}|{'-'*max_status_len}|{'-'*max_description_len}|\n"
        for j in task_setter_data[i].keys():
            current_weekoff=','.join(task_setter_data[i][j]["weekoff"]) if task_setter_data[i][j]['weekoff'] else ' '
            new_setter_write+=f"|{j}{" "*(max_task_title_len-len(j))}|{task_setter_data[i][j]['from']}{' '*(max_date_len-len(task_setter_data[i][j]['from']))}|{task_setter_data[i][j]['to']}{' '*(max_date_len-len(task_setter_data[i][j]['to']))}|{task_setter_data[i][j]['off_days']}{' '*7}|{task_setter_data[i][j]['on_days']}{' '*6}|{current_weekoff}{' '*(max_weekoff_len-len(current_weekoff))}|{validity_check(task_setter_data[i][j])[1]}|{task_setter_data[i][j]['description']}{' '*(max_description_len-len(task_setter_data[i][j]['description']))}|\n"
    f.write(new_setter_write)


