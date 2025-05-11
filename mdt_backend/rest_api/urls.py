from django.urls import path, include


urlpatterns = [
    path('accounts/', include('rest_api.accounts.urls')),
    path('', include('rest_api.bot.urls')),
]