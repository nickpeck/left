import os
import sys
import inspect
import runpy


def get_mod_path():
    file_path = inspect.getfile(inspect.currentframe())
    return os.path.dirname(file_path)


def print_usage_and_exit():
    print("""
    Automated test runner for python-left.
    Usage:
    python -m lefttest <app_module> <test_module>
    
    eg. python -m lefttest sampleapp sampleapp.tests""")
    exit(1)


if len(sys.argv) < 3:
    print_usage_and_exit()

app_module = sys.argv[1]
os.environ['LEFT_TESTRUNNER_MODULE'] = sys.argv[2]
addon_path = os.environ.get("LEFT_ADDON_PATH", '')
test_runner_addon_dir = os.path.join(get_mod_path(), 'addon')
os.environ["LEFT_ADDON_PATH"] = ";".join([addon_path, test_runner_addon_dir]) if addon_path else test_runner_addon_dir
sys.path.append(os.getcwd())
runpy.run_module(app_module)
