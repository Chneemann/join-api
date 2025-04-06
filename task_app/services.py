import uuid
from rest_framework.exceptions import APIException
from .models import SubTask, AssignedTask
from user_app.models import User

def create_or_update_subtasks(subtask_data, parent_task):
    current_subtasks = SubTask.objects.filter(task=parent_task)
    current_subtask_ids = {str(sub.id): sub for sub in current_subtasks} 

    new_subtasks_to_create = []
    subtasks_to_update = []
    new_subtask_ids = set()

    for sub_data in subtask_data:
        sub_id = sub_data.get('id')
        new_subtask_ids.add(str(sub_id))
        if sub_id and str(sub_id) in current_subtask_ids:
            subtask = current_subtask_ids[str(sub_id)]
            subtask.title = sub_data.get('title', subtask.title)
            subtask.status = sub_data.get('status', subtask.status)
            subtasks_to_update.append(subtask)
        else:
            new_subtasks_to_create.append(
                SubTask(
                    title=sub_data.get('title'),
                    status=sub_data.get('status'),
                    task=parent_task
                )
            )

    subtasks_to_delete = [
        sub_id for sub_id in current_subtask_ids if sub_id not in new_subtask_ids
    ]
    SubTask.objects.filter(id__in=subtasks_to_delete, task=parent_task).delete()

    SubTask.objects.bulk_create(new_subtasks_to_create)
    SubTask.objects.bulk_update(subtasks_to_update, ['title', 'status'])
            
def create_or_update_assignees(assignee_data, task):
    new_assignee_ids = {str(user["user_id"]) for user in assignee_data if "user_id" in user}

    current_assignees = AssignedTask.objects.filter(task=task).values_list('user_id', flat=True)
    current_assignee_ids = {str(assignee_id) for assignee_id in current_assignees}

    assignees_to_remove = current_assignee_ids - new_assignee_ids
    assignees_to_add = new_assignee_ids - current_assignee_ids

    AssignedTask.objects.filter(task=task, user_id__in=assignees_to_remove).delete()

    users_to_add = User.objects.filter(id__in=assignees_to_add)
    AssignedTask.objects.bulk_create(
        [AssignedTask(user=user, task=task) for user in users_to_add]
    )

def assign_users_to_task(user_ids, task):
    user_ids = [uuid.UUID(user["user_id"]) for user in user_ids if "user_id" in user]

    users = User.objects.filter(id__in=user_ids)
    found_user_ids = set(users.values_list('id', flat=True))
    missing_users = set(user_ids) - found_user_ids
 
    if missing_users:
        raise APIException(f"Users not found: {', '.join(map(str, missing_users))}") 

    AssignedTask.objects.bulk_create(
        [AssignedTask(user=user, task=task) for user in users]
    )

def create_subtasks(subtask_data, parent_task):
    if subtask_data:
        subtasks = [
            SubTask(title=sub['title'], status=sub['status'], task=parent_task)
            for sub in subtask_data
        ]
        SubTask.objects.bulk_create(subtasks)
    