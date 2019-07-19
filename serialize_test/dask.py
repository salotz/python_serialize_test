"""Helper functions for dask serializers."""

from distributed.protocol.serialize import dask_dumps, dask_loads
from distributed.protocol.utils import pack_frames, unpack_frames

def dumps(obj):
  return pack_frames(dask_dumps(obj)[1])

def loads(serial):
  return unpack_frames(dask_loads(serial))

def dump(obj, fh):
    fh.write(dumps(obj))

def load(fh):
    return loads(fh)
