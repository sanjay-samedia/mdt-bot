from django.db.models import Count, Avg

from apps.bot.models import BotInstance, VisitLog


def get_bot_analytics(bot_instance_id):
    bot_instance = BotInstance.objects.get(id=bot_instance_id)
    logs = VisitLog.objects.filter(bot_instance=bot_instance)
    return {
        'total_visits': bot_instance.visits_sent,
        'success_rate': bot_instance.success_rate,
        'average_stay_time': logs.aggregate(Avg('stay_time'))['stay_time__avg'] or 0,
        'success_count': logs.filter(success=True).count(),
        'failure_count': logs.filter(success=False).count()
    }