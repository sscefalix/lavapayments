from setuptools import setup

with open("readme.md", "r", encoding="utf-8") as readme:
    readme_text = readme.read()

setup(
    name="lavapayments",
    version="1.0.2",
    description="Библиотека для работы с Бизнес API Lava.ru",
    long_description=readme_text,
    packages=["lavapayments"],
    author_email="dimabykov189@gmail.com",
    zip_safe=False,
    requires=["aiohttp"],
    python_requires=">=3.8",
    long_description_content_type="text/markdown"
)
