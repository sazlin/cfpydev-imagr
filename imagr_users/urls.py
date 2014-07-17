from django.conf.urls import url, patterns, include
from django.views.generic.base import TemplateView
from registration.backends.default.views import ActivationView
from registration.backends.default.views import RegistrationView
from imagr_users.forms import ImagrUserRegistrationForm
from imagr_users.views import logout
from django.contrib import auth


urlpatterns = patterns('',
    url(r'^activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'
        ),
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/$',
        RegistrationView.as_view(form_class=ImagrUserRegistrationForm),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'
        ),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'
        ),
        name='registration_disallowed'),
    (r'', include('registration.auth_urls')),
    url(r'^login/$',
        auth.views.login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
)