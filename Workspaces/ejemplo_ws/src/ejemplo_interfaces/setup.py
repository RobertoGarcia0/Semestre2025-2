from setuptools import find_packages, setup

package_name = 'ejemplo_interfaces'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robousr',
    maintainer_email='roberto.gar.1748@gmail.com',
    description='TODO: Package description',
    license='mit',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "nodo_publicador = ejemplo_interfaces.publicador:main",
            "nodo_suscriptor = ejemplo_interfaces.suscriptor:main",
            "nodo_publicador_personalizado = ejemplo_interfaces.publicador_personalizado:main",
            "nodo_suscriptor_personalizado = ejemplo_interfaces.suscriptor_personalizado:main",
            "nodo_cliente = ejemplo_interfaces.cliente:main",
            "nodo_servidor = ejemplo_interfaces.servidor:main"
        ],
    },
)
