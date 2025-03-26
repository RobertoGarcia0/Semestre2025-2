from setuptools import find_packages, setup

package_name = 'ejemplo_tortuga'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            "nodo_velocidad = ejemplo_tortuga.v0elocidad:main",
            "nodo_velocidad_parametros = ejemplo_tortuga.velocidad_parametros:main",
            "nodo_spawner = ejemplo_tortuga.spawner:main"
        ],
    },
)
