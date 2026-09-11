import sys
import os
import subprocess

print("=========================================================================")
print("⚠️ WARNING: update_images.py is now DEPRECATED for sequential image mapping.")
print("The '1.jpg, 2.jpg' sequential enforcement has been removed to allow ")
print("custom image names to be uploaded and managed via J-Hub Studio.")
print("=========================================================================")
print("Running validate_book.py instead to check integrity...\n")

if os.path.exists("validate_book.py"):
    subprocess.run([sys.executable, "validate_book.py"])
else:
    print("validate_book.py not found in current directory.")
