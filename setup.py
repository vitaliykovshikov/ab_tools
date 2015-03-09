from distutils.core import setup

setup(
    name='ab_tools',
    version='0.1',
    packages=['ab_tools.advert', 'ab_tools.firm'],
    url='',
    license='',
    author='Dr.bleedjent',
    author_email='dr.bleedjent',
    description='Crossapps tools for all Avtobazar Apps',
    install_requires=[
        'requests',
        'mongoengine',
        'django-registration==0.8',
    ]
)
