# coding: utf-8
'''Setup sdroptim package.'''
from codecs import open
from setuptools import setup, find_packages

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name             = 'ejkm',
    version          = '0.2.0',
    packages         = find_packages(),
    description      = 'EDISON Jupyter Kernel Management',
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    license          = '',
    author           = 'Jeongcheol Lee',
    author_email     = 'jclee@kisti.re.kr',
    url              = 'https://github.com/jclee0333/ejkm',
    entry_points={
        'console_scripts': [
            'ejkm=ejkm:main',  # 'ejkm'은 실행할 명령어, 'ejkm:main'은 ejkm.py의 main 함수를 가리킵니다.
        ],
    },
    #download_url     = 'Git에 저장된 whl 배포용 압축파일',
    classifiers      = ['Programming Language :: Python :: 3.6',
                        'Intended Audience :: Korea Institute of Science and Technology Information',
                        'License :: MIT License']
    )
