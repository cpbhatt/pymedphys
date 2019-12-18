import functools
import os
import pathlib
import platform
import shutil
import subprocess
import tempfile
import typing
import zipfile

import pymedphys

HERE: pathlib.Path = pathlib.Path(__file__).parent.resolve()

# https://stackoverflow.com/a/39110
def file_contents_replace(file_path, pattern, subst):
    fh, abs_path = tempfile.mkstemp()
    with open(fh, "w") as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    os.remove(file_path)
    shutil.move(abs_path, file_path)


if platform.system() == "Windows":
    EXECUTION_PREPEND: typing.List[str] = []
else:
    EXECUTION_PREPEND = ["wine"]


# def call_embedded_python(embedded_python_dir, *args):
#     embedded_python_exe = embedded_python_dir.joinpath("python.exe")
#     to_be_called = [str(item) for item in EXECUTION_PREPEND + [embedded_python_exe] + list(args)]
#     print(to_be_called)
#     subprocess.check_call(to_be_called, cwd=embedded_python_dir)


def main(args):
    cwd = pathlib.Path(os.getcwd())
    build = cwd.joinpath("build")
    python = build.joinpath("python")

    if platform.system() != "Windows":
        compat_python = f"Z:{pathlib.PureWindowsPath(python)}"
    else:
        compat_python = python

    if args.clean:
        shutil.rmtree(build, ignore_errors=True)

    miniconda_install_exe = pymedphys.data_path("miniconda.exe")

    install_miniconda = EXECUTION_PREPEND + [
        miniconda_install_exe,
        "/InstallationType=JustMe",
        "/RegisterPython=0",
        "/S",
        "/AddToPath=0",
        f"/D={compat_python}",
    ]

    print(install_miniconda)

    subprocess.check_call(install_miniconda)

    # embedded_python_dir = build.joinpath("python")
    # copied_notebooks_dir = build.joinpath("notebooks")

    # notebooks_dir = cwd.joinpath("notebooks")
    # requirements_txt = cwd.joinpath("requirements.txt")

    # if not notebooks_dir.exists():
    #     raise ValueError(
    #         "Need to have a `notebooks` directory where this command is called"
    #     )

    # if not requirements_txt.exists():
    #     raise ValueError(
    #         "Need to have a `requirements.txt` file where this command is called"
    #     )

    # embedded_python_path = pymedphys.data_path("python-windows-64-embedded.zip")

    # with zipfile.ZipFile(embedded_python_path, "r") as zip_obj:
    #     zip_obj.extractall(embedded_python_dir)

    # try:
    #     shutil.copytree(notebooks_dir, copied_notebooks_dir)
    # except FileExistsError:
    #     pass

    # get_pip_path = pymedphys.data_path("get-pip.py")
    # call_embedded_python(embedded_python_dir, get_pip_path)

    # python_path_file = next(embedded_python_dir.glob("python*._pth"))

    # temp_python_path_file = f"{python_path_file}.temp"
    # file_contents_replace(python_path_file, "#import site", "import site")

    # call_embedded_python(embedded_python_dir, "-m", "pip", "--version")

    # os.rename(python_path_file, temp_python_path_file)
    # call_embedded_python(
    #     embedded_python_dir,
    #     "-m",
    #     "pip",
    #     "install",
    #     "-r",
    #     requirements_txt,
    #     "--no-warn-script-location",
    # )
    # os.rename(temp_python_path_file, python_path_file)

    # call_embedded_python(
    #     embedded_python_dir,
    #     "-c",
    #     "import pymedphys._jupyterlab.main; pymedphys._jupyterlab.main.get_build()",
    # )

    # build_files_to_copy = ["package.json", "yarn.lock"]
    # build_dirs_to_copy = ["src"]

    # for file_to_copy in build_files_to_copy:
    #     try:
    #         shutil.copy2(HERE.joinpath(file_to_copy), build.joinpath(file_to_copy))
    #     except FileExistsError:
    #         pass

    # for dirs_to_copy in build_dirs_to_copy:
    #     try:
    #         shutil.copytree(HERE.joinpath(dirs_to_copy), build.joinpath(dirs_to_copy))
    #     except FileExistsError:
    #         pass

    # subprocess.check_call(["yarn"], cwd=build)
    # subprocess.check_call(["yarn", "dist"], cwd=build)

    # final_exe = cwd.joinpath("JupyterLab Setup.exe")
    # try:
    #     final_exe.unlink()
    # except FileNotFoundError:
    #     pass

    # shutil.copy2(build.joinpath("release", "JupyterLab Setup 0.0.0.exe"), final_exe)
