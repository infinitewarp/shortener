from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import uri_to_iri
from django.views.decorators.csrf import csrf_exempt

from .forms import LinkForm
from .models import Link


@csrf_exempt
def home_page(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid():
            target = form.cleaned_data['url']
            """
            NOTE It would be nice to use a builtin function like get_or_create,
            but get_or_create blows up if finds more than one. We don't really
            care if there is more than one; we just want the *first* one.
            """
            try:
                link = Link.objects.filter(url=target)[0]
            except IndexError:
                link = Link.objects.create(url=target)

            return redirect('preview', link.token)

    else:
        form = LinkForm()

    return render(request, 'form.html', {'form': form})


def preview(request, token):
    pk = decode_token_to_pk(token)
    link = get_object_or_404(Link, pk=pk)
    token_uri = reverse('token_redirect', args=[token])
    short_url = request.build_absolute_uri(token_uri)
    short_iri = uri_to_iri(short_url)  # this is the more human-readable form
    full_iri = uri_to_iri(link.url)  # this is the more human-readable form
    context = {
        'token': token,
        'short_iri': short_iri,
        'short_url': short_url,
        'full_url': link.url,
        'full_iri': full_iri,
        'characters_saved': len(full_iri) - len(short_iri),
    }
    return render(request, 'preview.html', context)


def token_redirect(request, token):
    pk = decode_token_to_pk(token)
    link = get_object_or_404(Link, pk=pk)
    return HttpResponsePermanentRedirect(link.url)


def decode_token_to_pk(token):
    try:
        return settings.CONVERTER.decode(token)
    except IndexError:
        # IndexError may be raised if the token has an unsupported character
        return None
    except ValueError:
        # ValueError may be raised if the token can't be converted.
        return None
