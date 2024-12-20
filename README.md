# computer_vision

## Setup

```sh
# NOTE: if running ploomber <0.16, remove the --create-env argument
ploomber install --create-env
# activate environment (unix)
source {path-to-venv}/bin/activate
# activate environment (windows cmd.exe)
{path-to-venv}\Scripts\activate.bat
# activate environment (windows PowerShell)
{path-to-venv}\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.lock.txt


cd data
mkdir video
add video # "Cam1", "Cam2", "Cam3", "Cam4"
```

## Code editor integration

- If using Jupyter, [click here](https://docs.ploomber.io/en/latest/user-guide/jupyter.html)
- If using VSCode, PyCharm, or Spyder, [click here](https://docs.ploomber.io/en/latest/user-guide/editors.html)

## Running the pipeline

```sh
ploomber build # run the pipeline
ploomber plot  # plot the pipeline
ploomber scaffold
```

## Help

- Need help? [Ask us anything on Slack!](https://ploomber.io/community)
