from .models import Subject, YearGroup


def all_categories(request):

    subjects = Subject.objects.all()
    year_groups = YearGroup.objects.all()

    context = {
        'subjects': subjects,
        'year_groups': year_groups
    }

    return context
