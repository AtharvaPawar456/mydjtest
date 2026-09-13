from django.shortcuts import render

from ..models import EarnTask


def activeEarnTasksView(request):
    """
    Displays all active EarnTask records in descending timestamp order.
    io: request -> renders 'active_earn_tasks.html' with tasks context
    """
    try:
        activeTasks = EarnTask.objects.filter(estatus="active").order_by('-timestamp')
    except Exception as error:
        activeTasks = []
        print("Error fetching EarnTasks:", error)

    return render(request, 'earnTasks/active_earn_tasks.html', {'tasks': activeTasks})
