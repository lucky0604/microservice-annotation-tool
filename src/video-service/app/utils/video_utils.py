# -*- coding: utf-8 -*-
"""
@Time    : 11/9/20 10:25 AM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : video_utils.py
@Desc    : Description about this file
"""
import ast
from collections import namedtuple
import importlib
import sys
import traceback
import subprocess
import os

Import = namedtuple('Import', ['module', 'name', 'alias'])


def parse_imports(source_code: str):
    root = ast.parse(source_code)
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module
        else:
            continue

        for n in node.names:
            yield Import(module, n.name, n.asname)


def import_modules(source_code: str):
    results = {}
    imports = parse_imports(source_code)
    for import_ in imports:
        module = import_.module if import_.module else import_.name
        loaded_module = importlib.import_module(module)

        if not import_.name == module:
            loaded_module = getattr(loaded_module, import_.name)
        if import_.alias:
            results[import_.alias] = loaded_module
        else:
            results[import_.name] = loaded_module
    return results


class InterpreterError(Exception):
    pass


def execute_python_code(source_code, global_vars = None, local_vars = None):
    try:
        exec(source_code, global_vars, local_vars)
    except SyntaxError as err:
        error_class = err.__class__.__name__
        details = err.args[0]
        line_number = err.lineno
        raise InterpreterError('{} at line {}: {}'.format(error_class, line_number, details))
    except AssertionError as err:
        error_class = err.__class__.__name__
        raise InterpreterError('{}'.format(error_class))
    except Exception as err:
        error_class = err.__class__.__name__
        details = err.args[0]
        _, _, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        raise InterpreterError('{} at line {}: {}'.format(error_class, line_number, details))


def av_scan_paths(**paths):
    if 'yes' == os.environ.get('CLAM_AV'):
        command = ['clamscan', '--no-summary', '-i', '-o']
        command.extend(paths)
        res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode:
            raise Exception('CLAM AV ERROR')
