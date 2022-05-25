from django.urls import path
from rest_framework.routers import SimpleRouter
from chargemix import views

router = SimpleRouter()

router.register ('grade',            views.GradeViewSet)
router.register ('element',          views.ElementViewSet)
router.register ('product',          views.ProductViewSet)
router.register ('chargemix',        views.ChargemixViewSet)
router.register ('chargemixproduct', views.ChargemixProductViewSet)

urlpatterns = router.urls

urlpatterns.append (path('chargemixfetch/<int:pk>/', views.chargemix_full_object_fetch))