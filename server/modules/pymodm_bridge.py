import os
import inspect
import sys
from pymodm.queryset import QuerySet as Queryset

"""
Bridges Pymodm classes with pydatic classes
"""


class PymodmPydanticBridge:
    PYTANTIC_MODULE_DIR = "models"
    PYMORM_MODULE_DIR = "database"

    @classmethod
    def pydatic_to_pymodm(cls, class_, target_class: str):
        if isinstance(class_, list):
            instances = []
            for obj in class_:
                instance = cls._find_model_pymorm(target_class)
                instances.append(instance(**vars(obj)))
            return instances
        instance = cls._find_model_pymorm(target_class)
        return instance(**vars(class_))

    @classmethod
    def pymodm_to_pydantic(cls, class_, target_class: str):
        if isinstance(class_, Queryset):
            data = list(class_)
            instances = []
            for class_ in data:
                instance = cls._find_model_pydantic(target_class) # must import per iteration
                instance = instance(**class_.to_son().to_dict())
                instances.append(instance)
            if len(instances) == 1:
                return instances[0]
            else:
                return instances
        else:
            instance = cls._find_model_pydantic(target_class)
            return instance(**class_.to_son().to_dict())

    @classmethod
    def _find_model_pydantic(cls, class_):
        model_files = os.listdir(cls.PYTANTIC_MODULE_DIR)
        for file in model_files:
            file = file.split('.')[0]
            obj = cls._import(f'{cls.PYTANTIC_MODULE_DIR}.{file}.{class_}')
            if obj and callable(obj):
                return obj
        raise ImportError("Module not found. Please make sure Pydantic and ORM Classes share the same name")

    @classmethod
    def _find_model_pymorm(cls, class_):
        model_files = os.listdir(cls.PYMORM_MODULE_DIR)
        for file in model_files:
            file = file.split('.')[0]
            obj = cls._import(f'{cls.PYMORM_MODULE_DIR}.{file}.{class_}')
            if obj and callable(obj):
                return obj
        raise ImportError("Module not found. Please make sure Pydantic and ORM Classes share the same name")

    @staticmethod
    def _import(module):
        components = module.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            try:
                mod = getattr(mod, comp)
            except AttributeError: # if fails to get module
                return False
        return mod