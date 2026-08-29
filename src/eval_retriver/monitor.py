import subprocess
import os

process = subprocess.Popen(
    ["python", "train.py"]
)

process.wait()

print("Training finished!")

os.system("taskkill /F /IM Code.exe")
os.system("shutdown /s /t 10")