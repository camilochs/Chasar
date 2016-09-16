from setuptools import setup, find_packages
setup(
    name='chasar',
    version='0.0.2',
    description='Simple distributed system for monitoring.',
    author='Camilo Chacon Sartori',
    author_email='camilochs@gmail.com',
    license='MIT',
    packages=["masternode", "clientnode"],
    package_dir={'': 'src/core'},
    install_requires=["pyzmq", "psutil", "future", "netifaces"],
    scripts=['src/core/chasar'],
    include_package_data=True

)