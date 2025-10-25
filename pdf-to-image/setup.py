from setuptools import setup

setup(
    name="pdf-to-images",
    version="1.0.0",
    description="Tool chuyển PDF sang ảnh, có thể chia đôi trang, chọn định dạng và xem trước.",
    author="Vu Van Dinh",
    py_modules=["main"],
    install_requires=[
        "pdf2image>=1.16.0",
        "Pillow>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pdf-to-images = main:main",
        ],
    },
    python_requires=">=3.8",
)
