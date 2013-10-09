# The try/catch statement allows us to import django_yaaac outside any Django project.
try:
    from django_yaaac.manager import autocomplete
except:
    pass
