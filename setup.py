from distutils.core import setup


setup(
    name="apews",
    version="0.1",
    description="""
    A simple interface for the Attempto Parsing Engine web service
    """,
    author="Giulio Petrucci",
    author_email="giulio -DOT- petrucci -AT- gmail -DOT- com",
    url="https://github.com/petrux/APE-WS",
    packages=['apews'],
    install_requires=['requests>=2.3.0'])
