from setuptools import setup, find_packages

setup(
    name = 'pyfinancialdata',
    version = '0.1',
    author = 'Max Williams',
    author_email = 'futuresharks@gmail.com',
    license = 'GPLv3',
    description = 'Intraday financial data files for backtesting or analysis',
    package_data = {
        'pyfinancialdata': [
            'data/cryptocurrencies/*/*/*csv',
            'data/currencies/*/*/*/*.csv',
            'data/stocks/*/*/*.csv'
        ],
    },
    packages = [
        'pyfinancialdata',
    ],
    install_requires = [
        'pandas'
    ],
    classifiers = [
        'Environment :: Console',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
