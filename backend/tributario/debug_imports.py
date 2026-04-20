import sys
import os

print("PYTHONPATH:", sys.path)
print("Current Dir:", os.getcwd())

try:
    import tributario
    print("SUCCESS: Imported tributario")
    print("Tributario path:", tributario.__file__)
except Exception as e:
    print("FAILED: Import tributario:", e)

try:
    from tributario import views
    print("SUCCESS: Imported tributario.views")
except Exception as e:
    print("FAILED: Import tributario.views:", e)
