import csv
from datetime import datetime
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from core.models import ImageModel, Alert
from django.db import transaction


from planning.views import proj_list
from core.forms import FileForm, ImageForm
from finance.models import FinanceModel, FinanceModelSerializer
from planning.models import (
    PhaseModel,
    ProjectModel,
    TaskModel,
)


def home(request):
    alerts = Alert.objects.all()
    return render(request, "registration/login.html", {"alerts": alerts})


def upload_image(request):
    alerts = Alert.objects.all()

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = ImageForm()

    return render(request, "img_upload.html", {"img_form": form, "alerts": alerts})


def upload_file(request):
    alerts = Alert.objects.all()
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

                    mt_engag = (
                        float("".join(filter(str.isdigit, row["MT_ENGAGEMENT"])))
                    ) / 100
                    mt_recep = (
                        float("".join(filter(str.isdigit, row["MT_RECEPTION"])))
                    ) / 100

                    proj = ProjectModel.objects.filter(reference=eng).first()
                    if proj is not None and proj.cost is None:
                        proj.cost = mt_engag
                        proj.save()

                    FinanceModel.objects.update_or_create(
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

                    else:
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

    return render(request, "file_upload.html", {"form": form, "alerts": alerts})


def dir_dashboard(request):
    if request.method == "GET":
        alerts = Alert.objects.all()
        all_projects = ProjectModel.objects.all()
        total_projects = ProjectModel.objects.count()
        num_proj_retard = len(alerts)
        num_proj_sans_retard = total_projects - num_proj_retard
        images = ImageModel.objects.all()

    return render(
        request,
        "dir_dash.html",
        {
            "all_projects": all_projects,
            "total_projects": total_projects,
            "alerts": alerts,
            "num_proj_retard": num_proj_retard,
            "num_proj_sans_retard": num_proj_sans_retard,
            "images": images,
        },
    )


def cp_dashboard(request):
    alerts = Alert.objects.all()

    return render(
        request,
        "cp_dash.html",
        {
            "alerts": alerts,
        },
    )


def tech_dashboard(request):
    alerts = Alert.objects.all()

    return render(
        request,
        "tech_dash.html",
        {
            "alerts": alerts,
        },
    )


def phases_per_proj(request, ref):
    if request.method == "GET":
        alerts = Alert.objects.all()
        proj_phases = PhaseModel.objects.filter(project_related__reference=ref)
        images = ImageModel.objects.filter(project_ref=ref)

        return render(
            request,
            "proj_template.html",
            {
                "proj_phases": proj_phases,
                "ref": ref,
                "images": images,
                "alerts": alerts,
            },
        )


@api_view(["GET"])
def chart_proj_pie(request, ref):
    today = date.today()
    alerts = Alert.objects.all()
    # Filter phases by project reference
    proj_phases = PhaseModel.objects.filter(project_related__reference=ref)
    proj = ProjectModel.objects.filter(reference=ref).first()

    proj_start = proj.start
    proj_end = proj.end

    cost_per_day = (
        proj.cost / (proj_end - proj_start).days
        if (proj.end - proj.start).days != 0
        else 0
    )

    phases_cost = {
        phase.name: {
            "date": phase.end,
            "cost": ((phase.end - phase.start).days) * cost_per_day,
        }
        for phase in proj_phases
    }

    # Determine current phase based on today's date and project start/end dates
    current_phase = None

    for phase in proj_phases:
        if phase.start <= today <= phase.end:
            current_phase = phase.name
            break

    current_task = None

    for t in TaskModel.objects.filter(project_related=proj):
        if t.start <= today <= t.end:
            current_task = t.name
            break

    if current_task is None:
        current_task = "No sub-tasks for this phase "

    # Find phases that have passed and phases that will follow
    phases = {phase.name: phase.pk for phase in proj_phases}
    passed_phases = [phase.name for phase in proj_phases if phase.end < today]

    phases_start = [phase.start for phase in proj_phases]
    phases_end = [phase.end for phase in proj_phases]
    upcoming_phases = [phase.name for phase in proj_phases if phase.start >= today]

    if current_phase is not None:
        upcoming_phases.insert(0, current_phase)

    total_phases = len(passed_phases) + len(upcoming_phases)
    passed_percentage = (
        (len(passed_phases) / total_phases) * 100 if total_phases != 0 else 0
    )
    upcoming_percentage = (
        (len(upcoming_phases) / total_phases) * 100 if total_phases != 0 else 0
    )

    # financial records per project for valeur acquise
    records = FinanceModel.objects.filter(engagement=ref)

    fin_records_dates = [rec.date_operation for rec in records]
    fin_records_mt_reception = [rec.mt_reception for rec in records]
    fin_records = {
        rec.reception: {
            "date": rec.date_operation,
            "cost": rec.mt_reception,
        }
        for rec in records
    }

    total_fin_records_cost = sum(record["cost"] for record in fin_records.values())
    if total_fin_records_cost < proj.cost:
        # Create a new Alert instance
        with transaction.atomic():
            # Using get_or_create to create or update Alert instance
            alert_msg = " en retard ! "

            # Get or create the Alert instance
            alert, created = Alert.objects.get_or_create(
                msg=alert_msg,
                proj_related=proj,
                vp=passed_percentage,
                va=(total_fin_records_cost / proj.cost) * 100,
            )

            # Update the fields if the Alert was not created
            if not created:
                alert.save()

    data = {
        "current_phase": current_phase,
        "current_task": current_task,
        "passed_phases": passed_phases,
        "phases_start": phases_start,
        "upcoming_phases": upcoming_phases,
        "total_phases": total_phases,
        "phases": phases,
        "passed_percentage": passed_percentage,
        "upcoming_percentage": upcoming_percentage,
        "ref": ref,
        "proj_start": proj_start,
        "proj_end": proj_end,
        "phases_cost": phases_cost,
        "fin_records": fin_records,
        # "fin_records_mt_reception": fin_records_mt_reception,
    }
    return Response(data)


# (VA, VP et CR) va acquise, va planifiée, cout réel
