from django.shortcuts import render


def charges_form(request):
    return render(request, "charges_form.html")
