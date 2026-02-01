# Quickstart

To enter the python environment:
```sh
source ./env/bin/activate
# To make sure you have all the latest packages,
# run this whenever new packages are added by others:
pip install -r requirements.txt
```

Python can safely be run from here. You can install packages for this repo
using:

```sh
pip install my_package
```

To exit the environment:
```sh
deactivate
```

## Managing dependencies

When you install new packages, you should update `requirements.txt` so others
can install the same versions. To do this:

```sh
pip freeze > requirements.txt
```

This will capture the exact versions of all installed packages in your virtual
environment. Other users can then run:

```sh
pip install -r requirements.txt
```

to replicate your environment exactly.

