from distutils.core import setup
import glob

NAME='agora-probes'
NAGIOSPLUGINS='/usr/libexec/argo-monitoring/probes/agora'

def get_ver():
    try:
        for line in open(NAME+'.spec'):
            if "Version:" in line:
                return line.split()[1]
    except IOError:
        print "Make sure that %s is in directory"  % (NAME+'.spec')
	sys.exit(1)

setup(name=NAME,
      version=get_ver(),
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
