def project_ref(request):
    ref = None
    if request.user.is_authenticated:
        if (
            request.user.groups.filter(name="Chef de projets").exists()
            or request.user.groups.filter(name="Technician").exists()
        ):
            # Assuming you have a Profile linked to the User model
            profile = request.user.profile
            if profile:
                ref = profile.proj.reference

    return {"ref": ref}
