import traceback, yaml
d = yaml.safe_load(open('openenv.yaml'))
for t in d.get('tasks', []):
    gpath = t.get('grader', 'MISSING')
    print(f'Task {t.get("id")}: grader={gpath}')
    if ':' in str(gpath):
        try:
            mod, cls = gpath.rsplit(':', 1)
            import importlib
            score = float(getattr(importlib.import_module(mod), cls)().grade(None))
            print(f'  -> {score} {"OK" if 0 < score < 1 else "FAIL"}')
        except Exception as e:
            traceback.print_exc()
            print(f'  -> CRASHED (validator gets 0.0)')
    else:
        print(f'  -> WRONG FORMAT')
