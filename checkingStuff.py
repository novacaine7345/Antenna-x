from ansys.aedt.core import Hfss  # or the app you use
app = Hfss(version="2025.2", non_graphical=True)  # example - adjust if you use Desktop()

print("AEDT running? project:", getattr(app, "project_name", None), "design:", getattr(app, "design_name", None))
print("desktop handle:", getattr(app, "_desktop", None))
vm = app.variable_manager
print("has _variable_dict?:", hasattr(vm, "_variable_dict"), "value:", repr(getattr(vm, "_variable_dict", None)))

# Safe refresh attempt (diagnostic)
desktop = getattr(app, "_desktop", None)
try:
    res = vm._get_var_list_from_aedt(desktop)   # diagnostic only
    print("_get_var_list_from_aedt returned:", res)
    print("vm.variables:", vm.variables)
except Exception as e:
    print("refresh failed:", repr(e))
