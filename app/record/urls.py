from django.urls import path, include

from rest_framework.routers import Route

from app.urls import router
from . import views

app_name = 'record'

router.routes += [
    # Medical History View Route
    Route(
        url=r'^record{trailing_slash}medical{trailing_slash}history'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_medical_history',
            'post': 'create_medical_history'
        },
        name='medical_history-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Medical History Detail View Route
    Route(
        url=r'^record{trailing_slash}medical{trailing_slash}history'
            r'{trailing_slash}{lookup}{trailing_slash}$',
        mapping={
            'get': 'view_medical_history_by_id',
            'patch': 'update_medical_history_by_id',
            'delete': 'destroy_medical_history_by_id'
        },
        name='medical_history-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),

    # Visit View Route
    Route(
        url=r'^record{trailing_slash}visit{trailing_slash}$',
        mapping={
            'get': 'view_visit',
            'post': 'create_visit'
        },
        name='visit-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Visit Detail Route
    Route(
        url=r'^record{trailing_slash}visit{trailing_slash}{lookup}'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_visit_by_id',
            'patch': 'update_visit_by_id',
            'delete': 'delete_visit_by_id'
        },
        name='visit-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),

    # Prescription View Route
    Route(
        url=r'^record{trailing_slash}prescription{trailing_slash}$',
        mapping={
            'get': 'view_prescription',
            'post': 'create_prescription'
        },
        name='prescription-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Prescription Detail Route
    Route(
        url=r'^record{trailing_slash}prescription{trailing_slash}{lookup}'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_prescription_by_id',
            'patch': 'update_prescription_by_id',
            'delete': 'destroy_prescription_by_id'
        },
        name='prescription-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),

    # Allergy View Route
    Route(
        url=r'^record{trailing_slash}allergy{trailing_slash}$',
        mapping={
            'get': 'view_allergy',
            'post': 'create_allergy'
        },
        name='allergy-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Allergy Detail Route
    Route(
        url=r'^record{trailing_slash}allergy{trailing_slash}{lookup}'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_allergy_by_id',
            'patch': 'update_allergy_by_id',
            'delete': 'destroy_allergy_by_id'
        },
        name='allergy-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    )
]

urlpatterns = [
    path('', include(router.urls))
]

router.register('record', views.MedicalHistoryViewSet)
router.register('record', views.MedicalHistoryDetailViewSet)
router.register('record', views.PrescriptionViewSet)
router.register('record', views.PrescriptionDetailViewSet)
router.register('record', views.VisitViewSet)
router.register('record', views.VisitDetailViewSet)
router.register('record', views.AllergyViewSet)
router.register('record', views.AllergyDetailViewSet)
