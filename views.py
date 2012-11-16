# Create your views here.
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from django.views.decorators.cache import cache_page

#from . import settings
from . models import GuidebookPost, GuidebookCategory, GuidebookPostImages
from . forms import GuidebookEditForm, ImageUploadForm
from common.utils import log
from location.models import Country, City


def get_categories():
    return GuidebookCategory.objects.get_query_set()

def get_countries( category = None ):
#    log( category )
    if category:
        cots = GuidebookPost.objects.filter( category = category ).values_list( 'country' ).distinct()
    else:
        cots = GuidebookPost.objects.values_list( 'country' ).distinct()
#    log( cots )
    countries = Country.objects.filter( pk__in = cots )
#    log( countries )
    return countries

def get_posts( category = None, country = None, city = None, page = None ):
    posts = GuidebookPost.objects.filter( status = 'active' )

    if category:
        posts = posts.filter( category = category )

    if country:
        posts = posts.filter( country = country )

    if city:
        posts = posts.filter( city = city )

    paginator = Paginator( posts, 7 )

    try:
        posts = paginator.page( page )
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page( 1 )
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page( paginator.num_pages )

    return posts

def home( request, country = None, city = None, page = None ):

    log( 'guidebook home' )

    countries = get_countries()
    categories = get_categories()
    posts = get_posts( country = country, city = city, page = page )

    data = {
        'countries' : countries,
        'categories' : categories,
        'posts' : posts,
    }

    return render( request, 'guidebook/home.html', data )


def category( request, id, slug = None, country = None, city = None, page = None ):

    id = int( id )

    try:
        category = GuidebookCategory.objects.get( pk = id )
    except GuidebookCategory.DoesNotExist:
        raise Http404

    if category.slug() != slug:
        return redirect( 'guidebook-category', id = id, slug = category.slug(), permanent = True )

    countries = get_countries( category )
    categories = get_categories()
    posts = get_posts( category = category, country = country, city = city, page = page )

    data = {
        'category':category,
        'posts':posts,
        'categories':categories,
        'countries' : countries,
    }

    return render( request, 'guidebook/home.html', data )

def post( request, id, slug = None ):
    id = int( id )

    try:
        post = GuidebookPost.objects.get( pk = id )
    except GuidebookPost.DoesNotExist:
        raise Http404

    if post.slug() != slug:
        return redirect( 'guidebook-post', id = id, slug = post.slug(), permanent = True )

    data = {
        'post':post,
        'categories':GuidebookCategory.objects.all(),
    }

    return render( request, 'guidebook/post.html', data )


@login_required
def add( request ):
    if request.session.get( 'guidebook-draft-id', '' ) and int( request.session['guidebook-draft-id'] ) > 0:
        return redirect( 'guidebook-edit', id = request.session['guidebook-draft-id'] )
    else:
        post = GuidebookPost( status = 'draft', author = User.objects.get( pk = request.user.id ) )
        post.save()
        request.session['guidebook-draft-id'] = post.id
        return redirect( 'guidebook-edit', id = post.id )

@login_required
def edit( request, id ):
    id = int( id )

    try:
        post = GuidebookPost.objects.get( pk = id )
    except GuidebookPost.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = GuidebookEditForm( request.POST, instance = post )
        if form.is_valid:
            form.save()
            post.status = 'active'
            post.save()

            del request.session['guidebook-draft-id'];

            return redirect( 'guidebook-post', id = id )
        else:
            form = GuidebookEditForm( request.POST, instance = post )
    else:
        form = GuidebookEditForm( instance = post )

    images = GuidebookPostImages.objects.filter( post = post )

    data = {
        'post':post,
        'form':form,
        'image_upload_form':ImageUploadForm( initial = {'post':post} ),
        'images':images,
    }
    return render( request, 'guidebook/edit.html', data )

def file( request ):

    post = GuidebookPostImages.objects.get( pk = 1 )

    if request.method == "POST":
        form = ImageUploadForm( request.POST, request.FILES )
        if form.is_valid:
            form.save()
    else:
        form = ImageUploadForm( initial = {'post':post} )


    images = GuidebookPostImages.objects.filter( post = 1 )

    data = {
        'form':form,
        'images':images,
    }
    return render( request, 'guidebook/file.html', data )
