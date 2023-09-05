import os
import subprocess

      

def git_branch():
    arr =[]
    command = "git branch"
    result = subprocess.run(command, capture_output=True, text=True)
    text = result.stdout
    if text != "":
      branches = text.split('\n')
      for i in branches:
          if i != "":
            arr.append([i[2:],0])
    
    return arr

    




functions = {
    "git_branch":git_branch
}

