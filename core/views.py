import csv
from datetime import datetime
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date


from planning.views import proj_list
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


def phases_per_proj(request, ref):
    if request.method == "GET":
        proj = ProjectModel.objects.filter(reference=ref)
        proj_phases = PhaseModel.objects.filter(project_related__reference=ref)
        return render(
            request,
            "dashboards/proj_template.html",
            {
                "proj_phases": proj_phases,
                "ref": ref,
            },
        )


@api_view(["GET"])
def chart_data(request, ref):
    proj = ProjectModel.objects.filter(reference=ref).first()
    today = date.today()

    # Filter phases by project reference
    proj_phases = PhaseModel.objects.filter(project_related__reference=ref)

    # Determine current phase based on today's date and project start/end dates
    current_phase = None
    for phase in proj_phases:
        if phase.start <= today <= phase.end:
            current_phase = phase.name
            break

    # Find phases that have passed and phases that will follow
    passed_phases = [phase.name for phase in proj_phases if phase.end < today]
    upcoming_phases = [phase.name for phase in proj_phases if phase.start >= today]

    if current_phase is not None:
        upcoming_phases.append(current_phase)

    chartLabel = "Graph avancement projet"
    chartdata = [0, 25, 50, 75, 100]

    data = {
        "current_phase": current_phase,
        "passed_phases": passed_phases,
        "upcoming_phases": upcoming_phases,
        "chartLabel": chartLabel,
        "chartdata": chartdata,
        "ref": ref,
    }
    return Response(data)
