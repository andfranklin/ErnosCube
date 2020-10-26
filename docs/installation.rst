.. highlight:: shell

.. role:: bash(code)
   :language: bash

============
Installation
============


Stable release
--------------

To install ErnosCube, run this command in your terminal:

.. code-block:: console

  pip install ErnosCube

This is the preferred method to install ErnosCube, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for ErnosCube can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

  git clone git://github.com/andfranklin/ErnosCube

Or download the `tarball`_:

.. code-block:: console

  curl  -OL https://github.com/andfranklin/ErnosCube/tarball/master

You can install ErnosCube once you have a copy of the source by:

.. code-block:: console

  pip install .

.. _Github repo: https://github.com/andfranklin/ErnosCube
.. _tarball: https://github.com/andfranklin/ErnosCube/tarball/master


For Developers
--------------

First, create a virtual environment to isolate the packages that ErnosCube depends on
from your globally installed packages. By doing this you can make changes
without mucking up the installed version of the package.


.. code-block:: console

  python -m venv env


Then activate it. If you're on Windows, run:

.. code-block:: console

  env\Scripts\activate.bat

If you're on Unix or MacOS, run:

.. code-block:: console

  env/bin/activate

Finally, install the package in editable mode. When the virtual environemnt is
activated any changes you make to the code will automatically be reflected
in the installation.

.. code-block:: console

  pip install -e .

This should be more robust than the base version of CoolProp. If desired you
can install the dev and test requirements by:

.. code-block:: console

  pip install -r requirements_test.txt
  pip install -r requirements_dev.txt

These are useful if you're debugging issues related to CI, or if you want more
details from testing.


Testing
-------

To run tests:

.. code-block:: console

  pytest test


To run a subset of tests

.. code-block:: console

  pytest <path/to/tests>

It's possible to rerun test that failed first or only the tests that failed.
These commands correspond to :bash:`--failed-first` (:bash:`--ff`) and
:bash:`--last-failed` (:bash:`--lf`), respectively. If you are developing tests
you can choose to run the new tests first with :bash:`--new-first`
(:bash:`--nf`). To stop the test runner after the first failure use :bash:`-x`.
To run tests in parallel use :bash:`-n <number of jobs>`.

By default, pytest captures anything that is printed during tests. This is nice
because it keeps the screen clean when you're running tests. If you want to
output anything that is printed during the test use :bash:`-s`. Another useful
command is :bash:`--pdb`. This opens a debugger right before the error in the
test that failed. These pytest commands and many others can be specified at
the command line by:

.. code-block:: console

  python setup.py test --addopts <command>

or,

.. code-block:: console

  pytest <command>

See `pytest`_ for more information.

.. _pytest: https://docs.pytest.org/en/latest/

Coverage
--------

To get a coverage report use the command:

.. code-block:: console

  python setup.py test coverage

To get a more detailed html coverage report:

.. code-block:: console

  python setup.py test coverage_html