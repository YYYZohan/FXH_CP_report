from setuptools import setup, find_namespace_packages

install_requires = [
    "requests",
    "numpy",
    "pandas",
    "wrapt",
    "SQLAlchemy",
    "mysql-connector-python",
    "toml",
    "pymysql",
    "sshtunnel",
    "psycopg2",
    "coloredlogs",
    "dingtalkchatbot"
]

setup(
    name='my_proj',
    version='0.1',
    python_requires='>=3.5, <4',
    packages=find_namespace_packages(include=['my_proj.*']),
    install_requires=install_requires
)