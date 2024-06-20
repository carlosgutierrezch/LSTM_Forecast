import setuptools

with open('readme.md','r',encoding='utf-8') as f:
    long_description= f.read()
    
__version__='0.0.0'

REPO_NAME= 'LSTM-Forecast'
AUTHOR_USER_NAME= 'AETNA-68'
SRC_REPO= 'TimeSeriesForecast'
AUTHOR_EMAIL='aetna68corp@gmail.com'

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description='Ml app',
    long_description=long_description,
    long_description_content='text/markdown',
    url=f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}',
    project_urls={
        'Bug tracker':f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues'
    },
    package_dir={'':'src'},
    packages = setuptools.find_packages(where='src')
)   