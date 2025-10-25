from setuptools import setup

setup(
    name="rename-images",
    version="1.0.0",
    py_modules=["main"],
    install_requires=[
        "Pillow>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rename-images = main:main",
        ],
    },
)
