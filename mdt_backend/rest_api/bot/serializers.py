from rest_framework import serializers
from apps.accounts.models import BotUser
from apps.bot.models import Website, BotInstance


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'url', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BotInstanceSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()
    bot_user = serializers.PrimaryKeyRelatedField(queryset=BotUser.objects.all(), required=False)
    # time_taken = serializers.CharField(read_only=True, source='time_taken')

    class Meta:
        model = BotInstance
        fields = [
            'id', 'name', 'bot_user', 'website', 'requested_visits', 'visits_sent', 'successful_visits',
            'start_time', 'end_time', 'min_stay_time', 'max_stay_time', 'status',
            'success_rate', 'created_at', 'updated_at', 'time_taken'
        ]
        read_only_fields = [
            'visits_sent', 'successful_visits', 'start_time', 'end_time', 'status', 'success_rate',
            'created_at', 'updated_at', 'time_taken'
        ]

    def create(self, validated_data):
        website_data = validated_data.pop('website')
        # Check if website exists, create if it doesn't
        website, _ = Website.objects.get_or_create(
            url=website_data['url'],
            defaults={'name': website_data['name']}
        )
        bot_instance = BotInstance.objects.create(
            website=website,
            **validated_data
        )
        return bot_instance

    def validate(self, data):
        if data['max_stay_time'] < data['min_stay_time']:
            raise serializers.ValidationError(
                "Maximum stay time cannot be less than minimum stay time."
            )
        return data


class SimulateTrafficSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=256)
    website_name = serializers.CharField(max_length=128, required=False)
    bot_name = serializers.CharField(max_length=128, required=False)
    requested_visits = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if not data.get('website_name'):
            data['website_name'] = data['url'].split('//')[-1].split('/')[0]

        if not data.get('bot_name'):
            data['bot_name'] = data['url'].split('//')[-1].split('/')[0]

        return data


class SimulateTrafficResponseSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer(read_only=True)

    class Meta:
        model = BotInstance
        fields = (
            'id', 'name', 'bot_user', 'website', 'requested_visits', 'visits_sent',
            'start_time', 'end_time', 'status', 'created_at', 'updated_at'
        )
