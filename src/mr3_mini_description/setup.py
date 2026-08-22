from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mr3_mini_description'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.stl')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),   
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Matheus Lino',
    maintainer_email='matheus.vlino@gmail.com',
    description='URDF and meshes for the MR-3 Mini palletizing robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)