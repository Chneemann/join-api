from django.db import models
from django.utils.translation import gettext_lazy as _

class TaskCategory(models.TextChoices):
    TECHNICAL_TASK = 'Technical Task', _('Technical Task')
    USER_STORY = 'User Story', _('User Story')

class TaskPriority(models.TextChoices):
    LOW = 'low', _('Low')
    MEDIUM = 'medium', _('Medium')
    URGENT = 'urgent', _('Urgent')

class TaskStatus(models.TextChoices):
    TODO = 'todo', _('Todo')
    IN_PROGRESS = 'inProgress', _('In Progress')
    AWAIT_FEEDBACK = 'awaitFeedback', _('Await feedback')
    DONE = 'done', _('Done')