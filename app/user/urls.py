from django.urls import path, include

from rest_framework.routers import Route

from app.urls import router
from . import views

app_name = 'user'

router.routes += [
    # User View Route
    Route(
        url=r'^user{trailing_slash}$',
        mapping={
            'get': 'view_user',
            'post': 'create_user',
        },
        name='user-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # User Detail Route
    Route(
        url=r'user{trailing_slash}{lookup}{trailing_slash}$',
        mapping={
            'get': 'view_user_by_id',
            'patch': 'update_user_by_id',
            'delete': 'destroy_user_by_id'
        },
        name='user-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),
]

router.register('user', views.UserViewSet)
router.register('user', views.UserDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.AuthTokenViewSet.as_view(), name='auth-token')
]
