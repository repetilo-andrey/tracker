from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def timing(request, page_slug):
    """Show pages"""
    template = 'pages/' + page_slug + '.html'
    return render(request, template)
