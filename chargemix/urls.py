from django.urls import path
from rest_framework.routers import SimpleRouter
from chargemix import views

router = SimpleRouter()

router.register ('grade',            views.GradeViewSet)
router.register ('element',          views.ElementViewSet)
router.register ('product',          views.ProductViewSet)
router.register ('chargemix',        views.ChargemixViewSet)
router.register ('chargemixproduct', views.ChargemixProductViewSet)
router.register ('chargemixfetch',   views.ChargemixFetchViewSet, basename='chargemixfetch')

urlpatterns = router.urls