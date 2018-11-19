from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import Domain
from .postgres import Postgres

import bleach

def index(request):
    domains_list = Domain.objects.order_by('hostname')[:5]
    # output = ', '.join([d.hostname for d in domains_list])
    # return HttpResponse(output)
    template = loader.get_template('public_webmail/domain_list.html')
    context = {
        'domains_list': domains_list,
    }
    return HttpResponse(template.render(context, request))

def all_emails(request):
    postgres = Postgres()
    postgres_emails = postgres.get_all_emails()
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

def domain_emails(request, domain):
    #TODO: Check if is registered domain

    postgres = Postgres()
    postgres_emails = postgres.get_domain_emails(domain)
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

def full_address_emails(request, domain, username):
    #TODO: Check if is registered domain

    postgres = Postgres()
    postgres_emails = postgres.get_full_address_emails(domain, username)
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