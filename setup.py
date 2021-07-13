import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setuptools.setup(
    # Metadata
    name='django-hcaptcha-field',
    version='1.0.0',
    license='BSD',
    author='Ties Jan Hefting',
    author_email='hello@tiesjan.com',
    description='Django hCaptcha Field provides a simple way to protect your Django forms using hCaptcha.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/tiesjan/django-hcaptcha-field',
    project_urls={
        'Bugs': 'https://github.com/tiesjan/django-hcaptcha-field/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
    ],

    # Options
    packages=setuptools.find_packages(exclude=('py_tests*',)),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.5',
    install_requires=(
        'Django>=2.2,<=4.0',
    )
)
