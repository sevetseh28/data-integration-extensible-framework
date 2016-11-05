def class_from_string(module_name, class_name):
    # Import dinamico
    module = __import__(module_name, fromlist=[class_name])

    # Se obtiene la clase del modulo importado
    class_ = getattr(module, class_name)

    return class_


def load_module(step_name, module_directory, **kwargs):
    generic_module_class_name = "Module"

    module_name = "engine.modules.{}.{}.module".format(step_name, module_directory)
    gen_module = class_from_string(module_name, generic_module_class_name)

    # Obtiene el modulo fijandose cual de las subclases de Module es la buscada
    module = [m for m in _get_all_subclasses(gen_module)
              if m.__module__.startswith("engine.modules.{}.{}".format(step_name, module_directory))][0]

    # Se retorna el modulo creado con los atrs que reciba el constructor
    return module(**kwargs)


def load_step(step_name, **kwargs):
    module_name = "engine.workflow.steps"
    step = class_from_string(module_name, step_name)

    # Se retorna el step creado con los atrs que reciba el constructor
    return step(**kwargs)


def _get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(_get_all_subclasses(subclass))

    return all_subclasses
