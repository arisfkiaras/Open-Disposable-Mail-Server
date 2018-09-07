from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import Domain

def index(request):
    domains_list = Domain.objects.order_by('hostname')[:5]
    # output = ', '.join([d.hostname for d in domains_list])
    # return HttpResponse(output)
    template = loader.get_template('public_webmail/index.html')
    context = {
        'domains_list': domains_list,
    }
    return HttpResponse(template.render(context, request))

    
def mails(request, email_domain, email_address):
    return HttpResponse("You want %s@%s." % (email_address, email_domain))

def mails_no_address(request, email_domain):
    # TODO: Check that domain is valid
    # TODO: Should generate random vanity name
    return redirect("./default")

def mails_no_domain(request):
    # TODO: Should get a domain from db
    domain = Domain.objects.order_by('hostname')[0]
    # TODO: Should generate random vanity name

    return redirect("./%s/default" % domain.hostname)