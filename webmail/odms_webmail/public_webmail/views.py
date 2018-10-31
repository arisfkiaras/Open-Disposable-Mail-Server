from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import Domain
from .elastic import Elastic
from .postgres import Postgres

import bleach

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
    postgres = Postgres()
    postgres_emails = postgres.get_emails_all()
    emails = []
    for result in postgres_emails:
        email = {}
        email['id'] = result[0]
        email['from'] = result[1]
        email['to'] = "{}@{}".format(result[3], result[4])
        email['subject'] = result[5]
        email['time'] = result[6]
        emails.append(email)

    context = {
        'emails': emails,
    }
    template = loader.get_template('public_webmail/mail_list.html')
    return HttpResponse(template.render(context, request))

def mails_el(request, email_domain, email_address):
    elastic = Elastic()
    documents = elastic.getDocuments(from_doc=0, size_doc=100)
    
    items = documents.items()
    items2 = {}
    for key, value in items:
        items2[key] = value

    items2 = items2["hits"]["hits"]

    items3 = []
    for hit in items2:
        items3.append(hit["_source"])
    
    # emails = items3
    # print(emails)
    # # emails = [
    # #     {"from":"asd", "subject":"sd", "date":"2"},
    # #     {"from":"2", "subject":"1", "date":"4"}
    # # ]
    # context = {
    #     'emails': emails,
    # }
    # for email in context['emails']:
    #     email['subject'] = bleach.clean(email['content'])
    # template = loader.get_template('public_webmail/mail_list.html')
    emails = []
    for item in items3:
        email = {}
        email['from'] = bleach.clean(item['from'])
        email['subject'] = bleach.clean(item['subject'])
        email['timestamp'] = bleach.clean(item['timestamp'])
        emails.append(email)

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

def email_by_id(request, id):
    postgres = Postgres()
    # sanitize id here
    if not id.isdigit() or int(id) < 1 or int(id) > 999999:
        return HttpResponse("")

    try:
        email = postgres.get_email_content(id)[0]
    except:
        return HttpResponse("")
    # email2 = memoryview(email)
    # print(dir((email)))
    # print(bytes(email))
    return HttpResponse(email.tobytes(), content_type="text/plain")

def mails_no_domain(request):
    # TODO: Should get a domain from db
    domain = Domain.objects.order_by('hostname')[0]
    # TODO: Should generate random vanity name

    return redirect("./%s/default" % domain.hostname)