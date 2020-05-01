import sys
from fv3util import capture_stream
import logging
from functools import wraps
from mpi4py import MPI

logger = logging.getLogger(f"fv3gfs({MPI.COMM_WORLD.rank})")

CAPTURE = True


def _log_bytes(b):
    for line in b.decode("UTF-8").split("\n"):
        if "WARNING" in line:
            logger.warn(line)
        elif "NOTE" in line:
            logger.info(line)
        elif "FATAL" in line:
            logger.critical(line)
        elif line == "":
            pass
        else:
            logger.debug(line)


def _captured_stream(func):
    @wraps(func)
    def myfunc(*args, **kwargs):
        if CAPTURE:
            with capture_stream(sys.stdout) as out_io, capture_stream(
                sys.stderr
            ) as err_io:
                out = func(*args, **kwargs)
            _log_bytes(out_io.getvalue())
            _log_bytes(err_io.getvalue())
        else:
            out = func(*args, **kwargs)
        return out

    return myfunc


def capture_fortran_output():
    """Turns on the fortran output capturing feature

    See ``show_fortran_output``.
    """
    # capture stderr and stdout of fortran code
    global CAPTURE
    CAPTURE = True


def show_fortran_output():
    """Disables the fortran output capturing feature
    
    See ``capture_fortran_output``.
    """
    global CAPTURE
    CAPTURE = False
