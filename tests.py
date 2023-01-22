import os
import pathlib

import pytest

pytest.main(['--cov', '--cov-report', 'xml'])
