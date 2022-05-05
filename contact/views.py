from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

from .forms import ContactForm


def contact(request):

    form = ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            try:
                send_mail(subject, content, from_email, ['nikipiki@exemple.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found!')
            messages.success(request, 'Message sent!')
            return redirect('home')

    context = {
        'form': form,
    }

    return render(request, 'contact/contact.html', context)

    