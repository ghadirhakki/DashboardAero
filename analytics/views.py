from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(["GET"])
def chart_data(request):
    labels = ["January", "February", "March", "April", "May", "June", "July"]
    chartLabel = "Graph avancement projet"
    chartdata = [0, 25, 50, 75, 100]
    data = {
        "labels": labels,
        "chartLabel": chartLabel,
        "chartdata": chartdata,
    }
    return Response(data)
