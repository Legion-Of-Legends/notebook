import datetime as dt
with open("../Tasks/README.md") as f:
    task_tracker = f.read()

# filter data
task_time = dt.datetime.strptime(task_tracker.split("## Date:")[1].strip().split("\n")[0].strip(), "%d %B, %Y").date()
task_date = task_time.day
task_month = task_time.month
task_year = task_time.year
next_day = task_time + dt.timedelta(days=1)

member_data_all = task_tracker.split("\n")[2:]
member_data = {}
count = 0
while count < len(member_data_all):
    if member_data_all[count].startswith("##"):
        member_name = member_data_all[count].split("##")[1].strip()
        member_task={}
        for i in range(count + 1, len(member_data_all)):
            if member_data_all[i].startswith("##"):
                break
            elif member_data_all[i].startswith("|--") or member_data_all[i].startswith("|Tasks ") or member_data_all[i].strip() == "":
                continue
            else:
                task = member_data_all[i].strip().split("|")
                member_task[task[1].strip()] = task[2].strip()
                # member_task[task[0].strip()] = task[1].strip()
        member_data[member_name] = member_task
    count += 1

print(member_data_all)
print('\n\n',member_data)

with open("task_tracker.md", "w") as f:
    f.write(f"# Task Tracker for {task_date:02d}-{task_month:02d}-{task_year}\n\n")
    f.write(f"## Date: {next_day.day} {next_day.strftime('%B')}, {next_day.year}\n\n")
    for member, tasks in member_data.items():
        f.write(f"## {member}\n")
        f.write("| Task | Status |\n")
        f.write("|------|--------|\n")
        for task, status in tasks.items():
            f.write(f"| {task} | {status} |\n")
        f.write("\n")  # Add a newline after each member's tasks

