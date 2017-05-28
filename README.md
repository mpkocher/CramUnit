CramUnit
========

This library is a thin wrapper on *cram* testing framework to generate Xunit files. See [cram](https://bitbucket.org/brodie/cram/overview) for details.

As of [cram >= 0.7](https://bitbucket.org/brodie/cram/src/cb549264f752f3b009b1e742b9b0f3944e2e21f0/NEWS.rst?at=default&fileviewer=file-view-default), *cram* has added direct support for emitting XUnit output using **--xunit-file=PATH** flag. This output can be consumed by CI systems, such as jenkins or CircleCI.

Therefore, this library is largely unnecessary for most usecases. Moreover, the  added dependency on CramUnit doesn't provided enough value. **No further development is planned**.

For running directories, it's recommended to migrate to a `find my-dir -name "*.t"` and a call to *cram*. This will generate N XUnit files (which is different than *CramUnit* output of a single XUnit file).

The [implemenation might be useful](https://github.com/mpkocher/CramUnit/blob/master/cram_unit/crammer.py#L119) as an example of using the unittest library and dynamically adding test methods at runtime.


[![Build Status](https://travis-ci.org/mpkocher/CramUnit.svg?branch=master)](https://travis-ci.org/mpkocher/CramUnit)

Tool to generate Unittest/Xunit output from cram tests (i.e., files ending in `*.t`):

    $> python run_cram_unit.py /path/to/mytests --xunit nose_mytests.xml
