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
with open("../Tasks/README.md", "w") as f:
    # replace the date with the next day in task_tracker
    task_tracker = task_tracker.replace(f"## Date: {task_time.strftime('%d %B, %Y')}", f"## Date: {next_day.strftime('%d %B, %Y')}").replace("[x]", "[ ]").replace("[X]", "[ ]")  # Resetting all tasks to incompleted
    print(task_tracker)
    f.write(task_tracker)
