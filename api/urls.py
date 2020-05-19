from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import teststores

urlpatterns = [
    path('login',views.login),
    path('getparameter',teststores.GetTestParameter.as_view()),
    path('identity_teststore',teststores.IdentifyStores.as_view()),
    path('store_summary',teststores.StoreSummary.as_view()),
    path('save_teststores',teststores.UploadTestStore.as_view()),
    path('parameter_list',teststores.Parameter.as_view()),
    path('identity_controlstore',teststores.IdentifyControlStore.as_view()),
    path('save_stage',teststores.SaveStage.as_view()),
    path('date_range',teststores.DateRange.as_view()),

    path('logout',views.logout.as_view()),
    path('load_savedata', teststores.LoadSaveData),
    path('delete_savedata/<int:pk>', teststores.Edit_TestStore.as_view()),
    path('load_savetest/<int:pk>', teststores.Edit_TestStore.as_view()), 
    path('getall_savedata', teststores.GetAllSavedData), 

	]

	