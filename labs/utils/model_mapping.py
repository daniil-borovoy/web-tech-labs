from django.apps import apps


def create_model_mapping():
    model_mapping = {}

    # Iterate through all installed apps
    app_config = apps.get_app_config("labs")
    for model in app_config.get_models():
        # Map the model name to the model class
        model_mapping[model._meta.model_name] = model

    return model_mapping


def get_all_model_meta_names():
    model_meta_names = []

    # Iterate through all installed apps
    app_config = apps.get_app_config("labs")
    for model in app_config.get_models():
        # Get and store the model's meta name
        model_meta_names.append(model._meta.model_name)

    return model_meta_names
