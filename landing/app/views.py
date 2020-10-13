from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    param = request.GET.get('from-landing')
    if param:
        counter_click.update({param})
        print(param)
    print(sum(counter_click.values()))
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    param = request.GET.get('ab-test-arg')
    counter_show.update({param})
    if param == 'test':
        return render(request, 'landing_alternate.html')
    elif param == 'original':
        return render(request, 'landing.html')
    else:
        return render(request, 'index.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        test_lable = counter_click['test'] / counter_show['test']
    except:
        test_lable = 0.0
    try:
        original_lable = counter_click['original'] / counter_show['original']
    except:
        original_lable = 0.0
    return render(request, 'stats.html', context={
        'test_conversion': test_lable,
        'original_conversion': original_lable,
    })
