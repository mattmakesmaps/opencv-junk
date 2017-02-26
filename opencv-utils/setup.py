from setuptools import setup

setup(name='opencv-utils',
      version='0.1',
      description='opencv-utils',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='opencv',
      url='https://github.com/mattmakesmaps/opencv-junk',
      license='MIT',
      packages=['opencv-utils'],
      install_requires=[
          'tqdm',
      ],
      scripts=['bin/delete_dupes.py', 'bin/extract_frames.py'],
      include_package_data=True,
      zip_safe=False)
