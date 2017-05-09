from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-odps-auth',
    description='ODPS Auth plugin for HTTPie.',
    long_description=open('README.md').read().strip(),
    version='0.2.1',
    author='Cheng YiChao',
    author_email='onesuperclark@gmail.com',
    license='MIT',
    url='https://github.com/onesuper/httpie-hmac-auth',
    download_url='https://github.com/onesuper/httpie-hmac-auth',
    py_modules=['httpie_odps_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_odps_auth = httpie_odps_auth:OdpsAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
