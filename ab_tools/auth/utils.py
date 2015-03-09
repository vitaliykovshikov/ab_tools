def activate_profile(profile):
    result = None
    if not profile.activation_key_expired():
        user = profile.user
        user.is_active = True
        user.save()
        profile.activation_key = profile.ACTIVATED
        profile.save()
        result = user
    return result