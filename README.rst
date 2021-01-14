Overview
========
This is a python tool that queries the Open Targets REST API endpoint `/public/association/filter <https://platform-api.opentargets.io/v3/platform/public/association/filter>`_ and retrieves ``association_score.overall`` for a given target or disease id.
Print target_id, disease_id, association_score.overall as well as minimum, maximum, average, standard deviation values of ``association_score.overall``.

Description
===========
Here are the contents of the project.

.. code-block:: shell

  $ git ls-tree -r --name-only main
  README.rst
  association_analysis/__init__.py
  association_analysis/interface.py
  association_analysis/query_api.py
  association_analysis/utils.py
  config.yml
  requirements.txt
  tests/test_interface.py
  tests/test_query_api.py
  tests/test_utils.py

``README.rst`` is this file.

The ``association_analysis`` package contains 3 modules:

1. functions implementing the command line logic are in ``interface.py``.
2. functions using the API endpoint and its json data are in ``query_api.py``.
3. functions of more independent logic are found in ``utils.py``.

``config.yml`` groups static parameters in a single place separated from the code.

``requirements.txt`` lists packages with *fixed* versions to build the environment with.

Finally, we find in ``tests/`` tests for each module.

Installation
============
Using docker
-----------------
For this step, this docker version is used, it can matter:

.. code-block:: shell

  $ docker --version
  Docker version 19.03.13, build 4484c46d9d

First, clone this repository.

.. code-block:: shell

  git clone git@github.com:leagleag/association_score_ot.git

In the repository, the image ``analysis_ubuntu`` is built. You can expect the
image to weight ~800 MB and the building process to take ~160 s.

.. code-block:: shell

  docker build -t analysis_ubuntu -f Dockerfile .

That is it. Our favorite program can be run such as:

.. code-block:: shell

  docker run analysis_ubuntu -d Orphanet_399
  docker run analysis_ubuntu -t ENSG00000197386

Using virtualenv and pip3
-------------------------
.. code-block:: shell

  git clone git@github.com:leagleag/association_score_ot.git
  cd association_score_ot
  virtualenv opentargets_env
  source opentargets_env/bin/activate (if using gitbash: source opentargets_env/Scripts/activate)
  pip3 install -r requirements.txt

The program can be run using:

.. code-block:: language

  python association_analysis/interface.py -t ENSG00000197386

Testing and coverage
====================
Tests can be run with:

.. code-block:: shell

  python -m pytest -cov

We can get coverage using:

.. code-block:: shell

  python -m pytest --cov=association_analysis tests/

Output:

.. code-block:: text

  ============================= test session starts =============================
  platform win32 -- Python 3.6.5, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: C:\Users\User\Desktop\open_targets\association_score_ot
  plugins: cov-2.10.1
  collected 20 items

  tests\test_interface.py .........                                        [ 45%]
  tests\test_query_api.py ........                                         [ 85%]
  tests\test_utils.py ...                                                  [100%]

  ----------- coverage: platform win32, python 3.6.5-final-0 -----------
  Name                                Stmts   Miss  Cover
  -------------------------------------------------------
  association_analysis\interface.py      31      3    90%
  association_analysis\query_api.py      25      0   100%
  association_analysis\utils.py          13      3    77%
  -------------------------------------------------------
  TOTAL                                  69      6    91%


  ============================= 20 passed in 2.44s ==============================

Running examples
================
Querying association scores for a given target id.

.. code-block:: shell

  python association_analysis/interface.py -t ENSG00000197386

Output:

.. code-block:: language

  Found 1330 scores:
       target.id       disease.id  association_score.overall
  ENSG00000197386      EFO_0009386                   1.000000
  ENSG00000197386      EFO_0005774                   1.000000
  ENSG00000197386      EFO_0000618                   1.000000
  ENSG00000197386    MONDO_0002025                   1.000000
  ENSG00000197386      EFO_0000677                   1.000000
  .... trimmed ....
  ENSG00000197386      EFO_0009609                   0.006000
  ENSG00000197386       HP_0004326                   0.004000
  ENSG00000197386      EFO_1001482                   0.004000
  ENSG00000197386      EFO_1000653                   0.004000
  ENSG00000197386      EFO_0000637                   0.004000
  Scores statistics:
  min     0.004000
  max     1.000000
  mean    0.227706
  std     0.206736

Querying association scores for a given disease id.

.. code-block:: shell

  python association_analysis/interface.py -d Orphanet_399

Output:

.. code-block:: shell

  Found 758 scores:
     target.id    disease.id  association_score.overall
  ENSG00000197386  Orphanet_399                   1.000000
  ENSG00000165646  Orphanet_399                   1.000000
  ENSG00000198785  Orphanet_399                   1.000000
  ENSG00000273079  Orphanet_399                   1.000000
  ENSG00000183454  Orphanet_399                   1.000000
  .... trimmed ....
  ENSG00000090266  Orphanet_399                   0.004000
  ENSG00000086232  Orphanet_399                   0.004000
  ENSG00000077782  Orphanet_399                   0.004000
  ENSG00000023228  Orphanet_399                   0.004000
  ENSG00000006062  Orphanet_399                   0.004000
  Scores statistics:
  min     0.004000
  max     1.000000
  mean    0.088074
  std     0.163132


Notes
======
On environments
---------------
The environment was fabricated using ``virtualenv`` and ``pip3``.

.. code-block:: shell

  virtualenv ot_env
  source ot_env/bin/activate (gitbash: source ot_env/Scripts/activate)
  pip3 install -U pytest
  pip3 install pandas
  pip3 install requests
  pip3 install PyYAML
  pip3 install responses
  pip3 freeze > requirements.txt
  deactivate

To load the environment using ``requirements.txt``:

.. code-block:: shell

  virtualenv ot_env
  source ot_env/bin/activate (gitbash: source ot_env/Scripts/activate)
  pip3 install -r requirements.txt

On requests error handling
--------------------------
We assumed the network is nice but there are ways to handle exceptions when using requests. More details `here <https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions>`_.


4. add formatters
- use black https://github.com/psf/black; atom: python-black
- we can add a pre-hook with black to get the tag https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/
