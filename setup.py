from distutils.core import setup
import glob

NAME='agora-probes'
NAGIOSPLUGINS='/usr/libexec/agora-monitoring/probes/agora'


setup(name=NAME,
      version='0.1',
      license='AGPL 3.0',
      author='GRNET',
      author_email='angelakis@grnet.gr',
      description='Package includes probes for Agora',
      platforms='noarch',
      long_description='''
      This package includes probes for Agora.
      Currently it supports the following components:
        - Agora Health Check
      ''',
      url='https://eosc.agora.grnet.gr/',
      data_files=[(NAGIOSPLUGINS, glob.glob('src/*'))],
      packages=['agora_probes'],
      package_dir={'agora_probes': 'modules/'},
)
