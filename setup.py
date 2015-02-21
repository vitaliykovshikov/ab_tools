from distutils.core import setup

setup(
    name='ab_tools',
    version='0.1',
    packages=['tools.tools'],
    url='',
    license='',
    author='Dr.bleedjent',
    author_email='dr.bleedjent',
    description='Crossapps tools for all Avtobazar Apps',
    install_requires=[
        "celery==3.1.17",
        "celery-haystack==0.8",
        "django-celery==3.1.16",
    ]
)
