from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render

from .main import predict
from .models import Riddle, Option


def index(request):
    context = {"message": "her"}
    if request.method == 'POST' and request.FILES['csvdata']:
        csvdata = request.FILES['csvdata']
        fs = FileSystemStorage()
        filename = fs.save(csvdata.name, csvdata)
        uploaded_file_url = fs.url(filename)
        try:
            res = predict(uploaded_file_url)
        except FileNotFoundError:
            res = "file not found"
        data = [[i,v] for i,v in enumerate(res.open)]
        print(data)
        context = {
            'uploaded_file_url': uploaded_file_url,
            'res': res.to_html(),
            'values': data
        }
        return render(request, 'index.html', context)
    return render(request, "index.html", context)


def detail(request, riddle_id):
    return render(request, "answer.html", {"riddle": get_object_or_404(Riddle, pk=riddle_id)})


def answer(request, riddle_id):
    riddle = get_object_or_404(Riddle, pk=riddle_id)
    try:
        option = riddle.option_set.get(pk=request.POST['option'])
    except (KeyError, Option.DoesNotExist):
        return render(request, 'answer.html', {'riddle': riddle, 'error_message': 'Option does not exist'})
    else:
        if option.correct:
            return render(request, "index.html", {"latest_riddles": Riddle.objects.order_by('-pub_date')[:5],
                                                  "message": "Nice! Choose another one!"})
        else:
            return render(request, 'answer.html', {'riddle': riddle, 'error_message': 'Wrong Answer!'})
