import logging
import random
from celery import group
from django.core.validators import URLValidator
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import BotUser
from apps.bot.models import BotInstance, Website, BotStatus
from rest_api.bot.serializers import BotInstanceSerializer, SimulateTrafficSerializer
from traffic_bot.traffic_bot_core import process_traffic_task


logger = logging.getLogger(__name__)


class BotInstanceViewSet(viewsets.ModelViewSet):
    queryset = BotInstance.objects.all()
    serializer_class = BotInstanceSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show instances belonging to the requesting user
        return BotInstance.objects.filter(bot_user__user=self.request.user).order_by('-created_at')[:10]

    def perform_create(self, serializer):
        # Automatically set the bot_user to the requesting user
        bot_user = BotUser.objects.get(user=self.request.user)
        serializer.save(bot_user=bot_user)

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())

    @action(detail=False, methods=['post'], serializer_class=SimulateTrafficSerializer)
    def simulate_traffic(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            bot_user = BotUser.objects.get(user=request.user)

            bot_name = serializer.validated_data['bot_name']
            website_name = serializer.validated_data['website_name']
            url = serializer.validated_data['url']
            requested_visits = serializer.validated_data['requested_visits']

            URLValidator()(url)
            website, created = Website.objects.get_or_create(url=url)
            if not created and website.name != website_name:
                website.name = website_name
                website.save()

            bot_instance = BotInstance.objects.create(
                name=bot_name,
                bot_user=bot_user,
                website=website,
                requested_visits=requested_visits,
                min_stay_time=1,
                max_stay_time=3,
                start_time=timezone.now(),
                status=BotStatus.RUNNING,
            )
            bot_instance_id = bot_instance.id

            # Dynamic chunk size: small tasks use smaller chunks for parallelism
            chunk_size = min(10000, max(10, requested_visits // 16))
            selenium_visits_left = requested_visits // 4
            tasks = []

            for i in range(0, requested_visits, chunk_size):
                visits = min(chunk_size, requested_visits - i)
                # use_selenium = selenium_visits_left > 0
                # if use_selenium:
                #     selenium_visits_left -= visits
                tasks.append(
                    process_traffic_task.s(bot_instance_id, website.url, visits, True)
                )

            print("tasks:", tasks)
            group(tasks).apply_async()

            return Response({
                "id": bot_instance_id,
                "bot_name": bot_name,
                "website": {'url': website.url, 'name': website_name},
                "requested_visits": requested_visits,
                "status": bot_instance.status,
                "start_time": timezone.now()
            }, status=status.HTTP_202_ACCEPTED)

        except ValidationError:
            return Response({"error": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'])
    def stop_traffic(self, request, pk=None):
        try:
            bot_instance = BotInstance.objects.get(id=pk, status=BotStatus.RUNNING)
            if bot_instance.status == BotStatus.STOPPED:
                return Response({"message": "Traffic already stopped."}, status=status.HTTP_200_OK)

            bot_instance.status = BotStatus.STOPPED
            # bot_instance.end_time = timezone.now()
            bot_instance.updated_at = timezone.now()
            bot_instance.save(update_fields=['status', 'updated_at'])

            return Response({"message": f"BotInstance {pk} traffic stopped."}, status=status.HTTP_200_OK)
        except BotInstance.DoesNotExist:
            return Response({"error": "BotInstance not found."}, status=status.HTTP_404_NOT_FOUND)

