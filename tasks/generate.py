try:
     # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    # See https://stackoverflow.com/a/40984270 for a better Python3 only implementation
    from io import StringIO
import sys

from invoke import exceptions, run, task

import requirements


class Capturing(list):
    '''
    >>> with Capturing() as output:
    ...     print("Hello world!")
    >>> assert output == ["Hello world!"]
    >>> with Capturing(output) as output:
    ...     print("Foobar")
    >>> assert output == ["Hello world!", "Foobar"]
    '''
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


@task(requirements.install.fixed_requirements)
def config(ctx):
    # Don't eagerly import this module, because config_gen requires olso_config, which isn't
    # isn't installed if the requirements tasks haven't run yet
    # from tools import config_gen

    print("")
    print("================== config gen ====================")
    print("")
    with open('conf/st2.conf.sample', 'w+') as f:
        f.write('# Sample config which contains all the available options which the corresponding descriptions\n')
        f.write('# Note: This file is automatically generated using tools/config_gen.py - DO NOT UPDATE MANUALLY\n')
    run("python tools/config_gen.py >> conf/st2.conf.sample")
    # with Capturing() as output:
    #     config_gen.main(['tools/config_gen.py'])
    # for line in output:
    #     f.write(line)


@task
def api_spec(ctx):
    # Break an import cycle
    import lint
    lint.api_spec
    print("")
    print("================== Generate openapi.yaml file ====================")
    print("")
    with open('st2common/st2common/openapi.yaml', 'w+') as f:
        f.write('# NOTE: This file is auto-generated - DO NOT EDIT MANUALLY\n')
        f.write('# Edit st2common/st2common/openapi.yaml.j2 and then run\n')
        f.write('# invoke .generate-api-spec\n')
        f.write('# to generate the final spec file\n')
    run("st2common/bin/st2-generate-api-spec --config-file conf/st2.dev.conf >> st2common/st2common/openapi.yaml")


@task(config, api_spec, default=True)
def generate(ctx):
    pass
