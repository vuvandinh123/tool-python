from setuptools import setup

setup(
    name="resize-images",
    version="0.1.0",
    py_modules=["main"],
    install_requires=[
        "Pillow>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "resize-images = main:main",
        ],
    },
)
