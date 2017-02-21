import pkgutil

NAMESPACE_PREFIX = 'engine.'
MODULE_PREFIX = NAMESPACE_PREFIX + 'modules.'


def class_from_string(module_name, class_name):
    """
    Imports a python module and returns a class within that module

    :param module_name: Python module from which load the class
    :param class_name: class to load
    :return: said class
    """
    # Import dinamico
    module = __import__(module_name, fromlist=[class_name])

    # Se obtiene la clase del modulo importado
    class_ = getattr(module, class_name)

    return class_


def _load_module(step_name, module_directory):
    """
    Dynamically loads and returns a module from the framework

    :param step_name: Step to which the module belongs
    :param module_directory: directory where the module resides
    :return: said module
    """
    generic_module_class_name = "Module"

    module_name = MODULE_PREFIX + "{}.{}.module".format(step_name, module_directory)
    gen_module = class_from_string(module_name, generic_module_class_name)

    # Obtiene el modulo fijandose cual de las subclases de Module es la buscada
    module = [m for m in _get_all_subclasses(gen_module)
              if m.__module__.startswith(MODULE_PREFIX + "{}.{}".format(step_name, module_directory))][0]

    return module


def load_module(step_name, module_directory, **kwargs):
    """
    Returns an instance of a module from the framework initialized with the received kwargs

    :param step_name: Step to which the module belongs
    :param module_directory: directory where the module resides
    :param kwargs: initializations params for the module
    :return: initialized module
    """
    return _load_module(step_name, module_directory)(**kwargs)


def load_step(step_name, **kwargs):
    """
    Returns an instance of a step from the framework initialized with the received kwargs

    :param step_name: the name of the step
    :param kwargs: initializations params
    :return: initialized step
    """
    module_name = NAMESPACE_PREFIX + "workflow.steps"
    step = class_from_string(module_name, step_name)

    # Se retorna el step creado con los atrs que reciba el constructor
    return step(**kwargs)


"""""""""""""""""""""""""""""""""""""""
LIST
"""""""""""""""""""""""""""""""""""""""


def list_modules(step_name, project_id=None):
    """
    Lists all modules within a step including their required config

    :param step_name: Step to get the modules from
    :param project_id: Required to load some configs from some modules
    :return: list of modules with their config
    """
    module = __import__(MODULE_PREFIX + step_name, fromlist=[str(step_name)])

    modules = pkgutil.iter_modules(module.__path__)

    modules_data = []

    for m in modules:
        if not m[2]:
            continue
        # m[2] indica si es una carpeta, m[1] es el nombre del modulo
        mod_instance = _load_module(step_name, m[1])

        modules_data.append({
            'id': m[1],
            'value': m[1],
            'label': mod_instance.pretty_name(),
            'name': mod_instance.pretty_name(),
            'config': mod_instance.config_json(project_id=project_id)
        })

    return modules_data


def _get_all_subclasses(cls):
    """
    Gets all subclasses from a class

    :param cls: class from which get subclasses
    :return: list of cls' sublcasses
    """
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(_get_all_subclasses(subclass))

    return all_subclasses
