from .models import Subject, YearGroup


def all_categories(request):

    subjects = Subject.objects.all()
    year_groups = YearGroup.objects.all()

    context = {
        'all_subjects': subjects,
        'all_year_groups': year_groups
    }

    return context
