from setuptools import setup, find_packages

setup(
    name='misp',
    author='deresz',
    version='1.0',
    author_email='deresz@gmail.com',
    description='Maltego transforms for Malware Information Sharing Platform',
    license='GPL',
    packages=find_packages('src'),
    package_dir={ '' : 'src' },
    zip_safe=False,
    package_data={
        '' : [ '*.gif', '*.png', '*.conf', '*.mtz', '*.machine' ] # list of resources
    },
    install_requires=[
        'canari'
    ],
    dependency_links=[
        # custom links for the install_requires
    ]
)
