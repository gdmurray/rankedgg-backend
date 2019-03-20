from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'dropdown/operator_list', OperatorDropdownOptions.as_view(), name='dropdown-operator-list'),
    url(r'^operators$', OperatorListView.as_view(), name='operator-list')
    # url(r'^api/', include('operators.urls', namespace='operators')),
]
