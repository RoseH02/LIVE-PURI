
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from base.views import recipe_list, recipe_detail



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher

]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # base is your main app
    path('recipes/', recipe_list, name='recipes'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
)