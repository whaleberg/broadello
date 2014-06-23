from distutils.core import setup

setup(name='broadello',
      version='1.0',
      description='live from the broadello website',
      author='Louis Bergelson',
      author_email='louisb@broadinstitute.org',
      packages=['broadello'], requires=['jinja2'],
     )
