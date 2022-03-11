from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='PyILP',
    url='https://github.com/danyvarghese/PyILP/PyILP',
    author='Dany Varghese',
    author_email='dany.incito@gmail.com',
    # Needed to actually package something
    packages=['PyILP'],
    # Needed for dependencies
    install_requires=['numpy','pyswip'],
    # *strongly* suggested for sharing
    version='0.0.1',
    # The license can be anything you like
    license='unlicense',
    zip_safe=False,
)
