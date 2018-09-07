from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import Domain
from .elastic import Elastic

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
    elastic = Elastic()
    documents = elastic.getDocuments()
    items = documents.items()
    items2 = {}
    for key, value in items:
        items2[key] = value

    items2 = items2["hits"]["hits"]

    items3 = []
    for hit in items2:
        items3.append(hit["_source"])

    
    emails = items3
    context = {
        'emails': emails,
    }
    template = loader.get_template('public_webmail/mail_list.html')

    return HttpResponse(template.render(context, request))

    #return HttpResponse("You want %s@%s.<br><br>%s" % (email_address, email_domain, items2))

def mails_no_address(request, email_domain):
    # TODO: Check that domain is valid
    # TODO: Should generate random vanity name
    return redirect("./default")

def mails_no_domain(request):
    # TODO: Should get a domain from db
    domain = Domain.objects.order_by('hostname')[0]
    # TODO: Should generate random vanity name

    return redirect("./%s/default" % domain.hostname)