from flask import Flask, request, jsonify
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

class Task:
    def xǁTaskǁ__init____mutmut_orig(self, id, title, description, completed=False) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
    def xǁTaskǁ__init____mutmut_1(self, id, title, description, completed=True) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
    def xǁTaskǁ__init____mutmut_2(self, id, title, description, completed=False) -> None:
        self.id = None
        self.title = title
        self.description = description
        self.completed = completed
    def xǁTaskǁ__init____mutmut_3(self, id, title, description, completed=False) -> None:
        self.id = id
        self.title = None
        self.description = description
        self.completed = completed
    def xǁTaskǁ__init____mutmut_4(self, id, title, description, completed=False) -> None:
        self.id = id
        self.title = title
        self.description = None
        self.completed = completed
    def xǁTaskǁ__init____mutmut_5(self, id, title, description, completed=False) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.completed = None
    
    xǁTaskǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskǁ__init____mutmut_1': xǁTaskǁ__init____mutmut_1, 
        'xǁTaskǁ__init____mutmut_2': xǁTaskǁ__init____mutmut_2, 
        'xǁTaskǁ__init____mutmut_3': xǁTaskǁ__init____mutmut_3, 
        'xǁTaskǁ__init____mutmut_4': xǁTaskǁ__init____mutmut_4, 
        'xǁTaskǁ__init____mutmut_5': xǁTaskǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTaskǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTaskǁ__init____mutmut_orig)
    xǁTaskǁ__init____mutmut_orig.__name__ = 'xǁTaskǁ__init__'

    def xǁTaskǁto_dict__mutmut_orig(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_1(self):
        return {
            "XXidXX": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_2(self):
        return {
            "ID": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_3(self):
        return {
            "id": self.id,
            "XXtitleXX": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_4(self):
        return {
            "id": self.id,
            "TITLE": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_5(self):
        return {
            "id": self.id,
            "title": self.title,
            "XXdescriptionXX": self.description,
            "completed": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_6(self):
        return {
            "id": self.id,
            "title": self.title,
            "DESCRIPTION": self.description,
            "completed": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_7(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "XXcompletedXX": self.completed,
        }

    def xǁTaskǁto_dict__mutmut_8(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "COMPLETED": self.completed,
        }
    
    xǁTaskǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTaskǁto_dict__mutmut_1': xǁTaskǁto_dict__mutmut_1, 
        'xǁTaskǁto_dict__mutmut_2': xǁTaskǁto_dict__mutmut_2, 
        'xǁTaskǁto_dict__mutmut_3': xǁTaskǁto_dict__mutmut_3, 
        'xǁTaskǁto_dict__mutmut_4': xǁTaskǁto_dict__mutmut_4, 
        'xǁTaskǁto_dict__mutmut_5': xǁTaskǁto_dict__mutmut_5, 
        'xǁTaskǁto_dict__mutmut_6': xǁTaskǁto_dict__mutmut_6, 
        'xǁTaskǁto_dict__mutmut_7': xǁTaskǁto_dict__mutmut_7, 
        'xǁTaskǁto_dict__mutmut_8': xǁTaskǁto_dict__mutmut_8
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTaskǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁTaskǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁTaskǁto_dict__mutmut_orig)
    xǁTaskǁto_dict__mutmut_orig.__name__ = 'xǁTaskǁto_dict'

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso", "id": new_task.id})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
             }

    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())

    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
    print(task)
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({"message": "Tarefa atualizada com sucesso"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)
