from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()


# https://pypi.org/project/mkdocs-open-in-new-tab/
setup(
    name='mkdocs-open-in-new-tab',
    version='1.0.3',
    description='MkDocs plugin to open outgoing links and PDFs in new tab.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='mkdocs plugin, open in new tab, mkdocs, plugin, relative links, links',
    url='https://github.com/JakubAndrysek/mkdocs-open-in-new-tab',
    author='Jakub Andrýsek',
    author_email='email@kubaandrysek.cz',
    license='MIT',
    python_requires='>=3.7',
    install_requires=['mkdocs'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'open-in-new-tab = open_in_new_tab.plugin:OpenInNewTabPlugin',
        ]
    },
)
