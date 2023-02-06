# Django - open source webový aplikační framework napsaný v Pythonu, 
# který se volně drží architektury Model-Pohled-Šablona (Model-View-Template).
# w3school tutorial: https://www.w3schools.com/django/index.php
# popis šablon:      https://docs.djangoproject.com/en/1.10/ref/templates/builtins/
# 
# Instalace:
# py.exe -m pip install -U django --user
#
# Standardní postup pro vytvoření projektu skriptem po instalaci knihovny Django do lokální instalace Pythonu:
# 1. Vytvoření projektu:
#     django-admin.exe startproject hello_world_project
#     Dostáváme tak k dispozici 2 soubory:
#       manage.py   – Script, který má na starosti správu projektu.
#       settings.py – Konfigurační script společný všem aplikacím v projektu.
# 2. Vyzkoušení běhu serveru:
#     python manage.py runserver
# 3. Vytvoření základní "kostry" aplikace:
#     python manage.py startapp (název aplikace)
#       vytvoří se tak adresář s názvem aplikace s následující strukturou:
#         views.py    – Obsahuje jednotlivé view funkce.
#         urls.py     – Obsahuje mapování URL na jednotlivá view.
#         models.py   – Obsahuje popis datového modelu aplikace.
#         tests.py    – Obsahuje jednotkové testy.
#         __init__.py – Dělá z aplikace balíček Pythonu.
# 4. Do settings.py do INSTALLED_APPS přidat název naší aplikace. Pak vytvořit v adresáři naší aplikace adresář templates a vyzkoušet, např.:

# Návod pro použití s Apache2:
#    https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/modwsgi/
