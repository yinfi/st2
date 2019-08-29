import glob
import os

from invoke import Collection, exceptions, run, task

import fixate
from .. import git_tasks
import install


# COMPONENTS := $(shell ls -a | grep ^st2 | grep -v .egg-info)
# COMPONENTS_RUNNERS := $(wildcard contrib/runners/*)
# COMPONENTS_WITH_RUNNERS := $(COMPONENTS) $(COMPONENTS_RUNNERS)
# COMPONENT_SPECIFIC_TESTS := st2tests st2client.egg-info
# COMPONENTS_TEST := $(foreach component,$(filter-out $(COMPONENT_SPECIFIC_TESTS),$(COMPONENTS_WITH_RUNNERS)),$(component))
@task
def sdist(ctx):
    # Copy over shared dist utils modules which is needed by setup.py
    for component in glob.glob("contrib/runners/*"):
        run("cp -f scripts/dist_utils.py {component}/dist_utils.py".format(component=component))
        try:
            run("scripts/write-headers.sh {component}/dist_utils.py".format(component=component))
        except exceptions.Failure:
            break

    # Copy over CHANGELOG.RST, CONTRIBUTING.RST and LICENSE file to each component directory
    #@for component in $(COMPONENTS_TEST); do\
    #   test -s $$component/README.rst || cp -f README.rst $$component/; \
    #   cp -f CONTRIBUTING.rst $$component/; \
    #   cp -f LICENSE $$component/; \
    #done


@task(sdist, install.runners, default=True)
def requirements(ctx):
    # Generate all requirements to support current CI pipeline.
    fixate.requirements(ctx)

    # Fix for Travis CI race
    run("pip install \"six==1.12.0\"")

    # Fix for Travis CI caching issue
    if os.environ.get('TRAVIS_EVENT_TYPE'):
        run("pip uninstall \"pytz\" || echo \"pytz not installed\"")
        run("pip uninstall \"python-dateutil\" || echo \"python-dateutil not installed\"")
        run("pip uninstall \"orquesta\" || echo \"orquesta not installed\"")

    # Install requirements
    install.requirements(ctx)

    # Install st2common package to load drivers defined in st2common setup.py
    # NOTE: We pass --no-deps to the script so we don't install all the
    # package dependencies which are already installed as part of "requirements"
    # make targets. This speeds up the build
    install.st2common_develop(ctx)

    # Note: We install prance here and not as part of any component
    # requirements.txt because it has a conflict with our dependency (requires
    # new version of requests) which we cant resolve at this moment
    install.prance(ctx)

    # Install st2common to register metrics drivers
    # NOTE: We pass --no-deps to the script so we don't install all the
    # package dependencies which are already installed as part of "requirements"
    # make targets. This speeds up the build
    install.st2common_develop(ctx)

    # Some of the tests rely on submodule so we need to make sure submodules are check out
    git_tasks.submodule.update(ctx)


namespace = Collection()
namespace.add_task(sdist)
namespace.add_task(requirements)
namespace.add_collection(fixate)
namespace.add_collection(install)
