from django.core import paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from allauth.account.views import PasswordChangeView
from .models import Spaces
from .forms import ContactUsForm, RegisterSpaceForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.text import slugify
# Create your views here.

class CustomPasswordChangeView(PasswordChangeView):
    success_url = '/accounts/password/reset/key/done'


def index(request):
    featured_spaces = Spaces.published.order_by('-created')[:5]
    return render(request, 'spaces/index.html', {'featured_spaces': featured_spaces})

def dashboard(request):
    object_list = Spaces.published.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        spaces = paginator.page(page)
    except PageNotAnInteger:
        spaces = paginator.page(1)
    except EmptyPage:
        spaces = paginator.page(paginator.num_pages)
    return render(request, 'spaces/dashboard.html', {'spaces': spaces, 'page': page, 'spacecount': object_list})

@login_required
def space_detail(request, space):
    space = get_object_or_404(Spaces, slug=space, status='published')
    space_tags_ids = space.facilities.values_list('id', flat=True)
    similar_spaces = Spaces.published.filter(facilities__in=space_tags_ids).exclude(id=space.id)
    similar_spaces = similar_spaces.annotate(same_tags=Count('facilities')).order_by('-same_tags', '-created')[:3]
    return render(request, 'spaces/detail.html', {'space': space, 'similar_spaces': similar_spaces})

def search(request):
    try:
        if 'state' in request.GET:
            state = request.GET['state']
            lga = None
            object_list = []
            stateCount = Spaces.published.filter(state__search=state).count()
            if 'lga' in request.GET:
                if request.GET['lga'] != '':
                    lga = request.GET['lga']
                    object_list = Spaces.published.filter(state__search=state, lga__search=lga)
                else:
                    object_list = Spaces.published.filter(state__search=state)
            else:
                object_list = Spaces.published.filter(state__search=state).order_by('created')
            if (not state) and (not lga):
                return redirect('spaces:dashboard')
            paginator = Paginator(object_list, 10)
            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
        else:
            return redirect('spaces:dashboard')
    except:
        return redirect('spaces:dashboard')
    return render(request, 'spaces/search.html', {'results': results, 'state': state, 'lga': lga, 'statecount': stateCount, 'lgacount': object_list})


@login_required
def register_space(request):
    if request.method == 'POST':
        f = RegisterSpaceForm(data=request.POST, files=request.FILES)
        if f.is_valid():
            new_space = f.save(commit=False)
            new_space.slug = slugify(new_space.name)
            new_space.save()
            f.save_m2m()
            return redirect('spaces:register_space_done')
    else:
        f = RegisterSpaceForm()
    return render(request, 'spaces/register_space.html', {'form': f})


@login_required
def register_space_done(request):
    return render(request, 'spaces/register_space_done.html')

def aboutus(request):
    return render(request, 'spaces/aboutus.html')

def contactus(request):
    if request.method == 'POST':
        f = ContactUsForm(request.POST)
        if f.is_valid():
            f.save()
            success = "Thank You! Your message has been submitted sucessfully. We'd get back to you shortly."
            return render(request, 'spaces/contactus.html', {'form': f, 'success': success})
    else:
        f = ContactUsForm()
    return render(request, 'spaces/contactus.html', {'form': f})