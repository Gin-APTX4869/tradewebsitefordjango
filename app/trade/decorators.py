from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest


def canonical(model):
    """
    Enforce a canonical URL for a resource.
    """
    def outer(view):
        def inner(request, id, slug=''):
            instance = get_object_or_404(model, pk=id)
            if not request.path == instance.get_absolute_url():
                return redirect(instance, permanent=True)
            return view(request, instance)
        return inner
    return outer


def ajax_required(f):
    """
    过滤非ajax请求
    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
