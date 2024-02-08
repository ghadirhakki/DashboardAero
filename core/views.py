import csv
from datetime import datetime
from django.shortcuts import render

from django.views.generic import TemplateView, CreateView

from core.forms import FileForm
from finance.models import FinanceModel

# Create your views here.


def home(request):
    return render(
        request,
        "home.html",
    )


def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"].read().decode("latin-1").splitlines()
            csv_reader = csv.DictReader(csv_file, delimiter=";")

            for row in csv_reader:

                date_op = datetime.strptime(
                    row["TO_DATE(DATE_OPERATION)"], "%d/%m/%Y %H:%M"
                ).date()

                mt_engag = float("".join(filter(str.isdigit, row["MT_ENGAGEMENT"])))
                mt_recep = float("".join(filter(str.isdigit, row["MT_RECEPTION"])))

                FinanceModel.objects.create(
                    date_operation=date_op,
                    reception=row["RECEPTION"],
                    engagement=row["ENGAG"],
                    fournisseur=row["FOURNISSEUR"],
                    shipment_num=row["SHIPMENT_NUM"],
                    devise=row["DEVISE"],
                    receptionnaire=row["RECEPTIONNAIRE"],
                    mt_engagement=mt_engag,
                    objet=row["OBJET"],
                    mt_reception=mt_recep,
                )
            form.save()

    else:
        form = FileForm()

    return render(request, "file_upload.html", {"form": form})
