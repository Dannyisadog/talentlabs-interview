from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from .routes.auth import router as auth_router
from .routes.jobs import router as jobs_router

ninja_api = NinjaAPI()
ninja_api.add_router("/jobs/", jobs_router)
ninja_api.add_router("/auth/", auth_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/", ninja_api.urls),
]
