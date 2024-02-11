import csv
from datetime import datetime
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.forms import FileForm
from finance.models import FinanceModel, FinanceModelSerializer
from planning.models import (
    PhaseModel,
    ProjectModel,
    TaskModel,
)

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
            csv_file = request.FILES.get("file")
            file_type = request.POST.get("type")
            proj_ref = request.POST.get("project_ref")

            if not csv_file:
                return HttpResponseBadRequest("Missing file")

            if file_type == "BudgetFile":

                csv_reader = csv.DictReader(
                    csv_file.read().decode("latin-1").splitlines(), delimiter=";"
                )

                for row in csv_reader:

                    date_op = datetime.strptime(
                        row["TO_DATE(DATE_OPERATION)"], "%d/%m/%Y %H:%M"
                    ).date()

                    eng = row["ENGAG"].replace("/", "_").replace(" ", "")

                    mt_engag = float("".join(filter(str.isdigit, row["MT_ENGAGEMENT"])))
                    mt_recep = float("".join(filter(str.isdigit, row["MT_RECEPTION"])))

                    FinanceModel.objects.create(
                        date_operation=date_op,
                        reception=row["RECEPTION"],
                        engagement=eng,
                        fournisseur=row["FOURNISSEUR"],
                        shipment_num=row["SHIPMENT_NUM"],
                        devise=row["DEVISE"],
                        receptionnaire=row["RECEPTIONNAIRE"],
                        mt_engagement=mt_engag,
                        objet=row["OBJET"],
                        mt_reception=mt_recep,
                    )
                form.save()

            elif file_type == "PlanningFile":

                csv_reader = csv.DictReader(
                    csv_file.read().decode("latin-1").splitlines(), delimiter=","
                )

                for row in csv_reader:

                    start_date = datetime.strptime(row["Start"], "%a %m/%d/%y").date()
                    end_date = datetime.strptime(row["Finish"], "%a %m/%d/%y").date()

                    if row["Outline Level"] == "0":
                        current_proj, bool = ProjectModel.objects.get_or_create(
                            reference=proj_ref,
                            start=start_date,
                            end=end_date,
                        )

                    elif row["Outline Level"] == "1":
                        current_phase, bool = PhaseModel.objects.get_or_create(
                            project_related=current_proj,
                            name=row["Name"],
                            start=start_date,
                            end=end_date,
                        )

                    elif row["Outline Level"] >= "1":
                        TaskModel.objects.create(
                            project_related=current_proj,
                            phase_related=current_phase,
                            name=row["Name"],
                            start=start_date,
                            end=end_date,
                        )

                form.save()

    else:
        form = FileForm()

    return render(request, "file_upload.html", {"form": form})


def dir_dashboard(request):
    if request.method == "GET":
        all_projects = ProjectModel.objects.all()
    return render(request, "dashboards/dir_dash.html", {"all_projects": all_projects})
