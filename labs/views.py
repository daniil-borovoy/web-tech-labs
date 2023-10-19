from django.shortcuts import render

from .handlers import (
    handle_lab_1,
    handle_lab_1_2,
    handle_lab_2,
    default_handler,
    handle_lab_3,
)


def index(request):
    return render(request, "home.html")


def info(request):
    return render(request, "info.html")


def render_lab(request, lab_number):
    match lab_number:
        case "1":
            return handle_lab_1(request, lab_number)
        case "1_2":
            return handle_lab_1_2(request, lab_number)
        case "2":
            return handle_lab_2(request, lab_number)
        case "3":
            return handle_lab_3(request, lab_number)
        case _:
            return default_handler(request, lab_number)
