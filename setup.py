import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentry-alert-notifier-wish",
    version="0.0.68",
    author_email="asymons@wish.com",
    description="A notification system to alert developers of their outstanding sentry errors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ContextLogic/sentry-alert-notifier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
