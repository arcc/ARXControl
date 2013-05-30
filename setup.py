"""
ARXControl
----------

Package used to control the LoFASM ARX.

Links
`````

* `development version
  <http://github.com/arcc/ARXControl/>`_


"""
try:
    import multiprocessing
except ImportError:
    pass

from setuptools import setup


setup(
    name='ARXControl',
    version='0.2',
    url='http://github.com/arcc/ARXControl',
    #license='BSD',
    author='Anthony J. Ford',
    author_email='ford.anthonyj@gmail.com',
    description='LoFASM ARX control library',
    long_description=__doc__,
    packages=[
        'ARXControl',
    ],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'pyserial',
    ],
    tests_require=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
