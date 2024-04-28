from setuptools import setup, find_packages

setup(
    name='Al-HaQ',
    version='0.1.1',
    description='A fight for truth. A better democracy.  ',
    long_description='Fake news can spread up to 10 times faster than true reporting on social media. These often reach 100,000+ people within a few hours, and the implications can be devastating in spreading misinformation, even when corrected. AlHaq is a cross-platform service that tailors any user’s social media feed to amplify trusted information within their social network using quantum computing. AlHaq can detect fake news from a social media user, rank the trustedness of members in their social network, and adapt their social media feed to boost true news sources and filter disinformation.',
    author='[Ahmad], [Emanuel], [Ghada], [Mariam], [Omar], [Pablo], [Salma], [Savar], [Favour], [Akash]',
    author_email='akant1@asu.edu',
    url='https://github.com/Haq-Lense/Al-HaQ',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering",

    ],
    keywords='Quantum Computing, QUBO, Quantum ML, Optimization',
    install_requires=[
        "numpy",
        "qiskit",
        "amazon-braket-default-simulator",
        "amazon-braket-sdk",
    ],
    # extras_require={
    #     "dev": [
    #         "pytest>=3.7",
    #         "jupyterlab>=3.6.0",
    #         "mypy",
    #         "pylint",
    #         'mkdocs',
    #     ],
    # }
    # entry_points={
    #     'console_scripts': [
    #         # Add any console scripts here
    #     ],
    # },
    project_urls={
        "Documentation": "https://github.com/Haq-Lense/Al-HaQ",
        "Source Code": "https://github.com/Haq-Lense/Al-HaQ",
        "Tutorials": "https://github.com/Haq-Lense/Al-HaQ/tree/main/code",
        "Machine Learning": "https://github.com/Haq-Lense/Al-HaQ/tree/main/qml-simulation"
    },
)