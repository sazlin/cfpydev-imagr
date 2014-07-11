from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home_page'))

    return HttpResponseRedirect(reverse('user_login'))


def user_login(request):
    #source: http://www.tangowithdjango.com/book/chapters/login.html
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Account Inactive. Bummer :(")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)


def home_page(request):
    return HttpResponse("This is the home_page.")

"""
A "front page" that shows anonymous users something nice to encourage them to sign up (don't worry that we lack a means for them to sign up yet.  We'll add that soon).
A "home page" that shows logged-in users a list of their albums, with a representative image from each album
An "album page" that shows logged-in users a display of photos in a single album
A "photo page" that shows logged-in users a single photo along with details about it.
A "stream" page that shows users their most recent photos along with recent photos uploaded by friends or those they are following.
"""
