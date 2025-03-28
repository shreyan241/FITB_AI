"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from profiles.api.endpoints.resume import router as resume_router
from profiles.api.endpoints.profile import router as profile_router
from profiles.api.endpoints.education import router as education_router
from profiles.api.endpoints.work_experience import router as work_experience_router
from profiles.api.endpoints.skill import router as skill_router
from profiles.api.endpoints.social_link import router as social_link_router
from profiles.api.endpoints.equal_employment import router as equal_employment_router
from profiles.utils.logger.logging_config import logger

api = NinjaAPI(
    title="FITB AI API",
    version="1.0.0",
    description="""
    FITB AI Backend API.
    """,
    csrf=False,  # Disabled CSRF for API
    urls_namespace='api',
    docs_url='/docs/' if settings.DEBUG else None,
    openapi_url='/openapi.json' if settings.DEBUG else None,
)

# Add routers with versioned paths
api.add_router("/v1/profiles/", profile_router)
api.add_router("/v1/profiles/", resume_router)
api.add_router("/v1/profiles/", education_router)
api.add_router("/v1/profiles/", work_experience_router)
api.add_router("/v1/profiles/", skill_router)
api.add_router("/v1/profiles/", social_link_router)
api.add_router("/v1/profiles/", equal_employment_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)