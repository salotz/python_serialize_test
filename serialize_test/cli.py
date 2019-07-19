import time
import tempfile

import click

import numpy as np
import pandas as pd

# protocols
import pickle

import dill
import cloudpickle
import joblib

import serialize_test.dask as dask

N_REPLICATES = 3

def test_to_file(obj, dump_func, load_func):

    dump_times = []
    load_times = []

    for rep in range(N_REPLICATES):


        f = tempfile.TemporaryFile()

        dump_start = time.time()
        dump_func(obj, f)
        dump_end = time.time()

        f.seek(0)

        load_start = time.time()
        obj = load_func(f)
        load_end = time.time()

        dump_times.append(dump_end - dump_start)
        load_times.append(load_end - load_start)

    return dump_times, load_times

@click.command()
@click.argument('obj-file', nargs=1, type=click.Path(exists=True))
def main(obj_file):

    protocols = (
        ('pickle', pickle.dump, pickle.load),
        ('dill', dill.dump, dill.load),
        ('cloudpickle', cloudpickle.dump, cloudpickle.load),
        ('joblib', joblib.dump, joblib.load),
        ('dask', dask.dump, dask.load),
    )

    with open(obj_file, 'rb') as rf:
        obj = pickle.load(rf)

    timings_columns = ('protocol', 'avg. dump', 'avg. load',)
    timings_rows = []
    for prot_name, dump_func, load_func in protocols:

        prot_failed = False
        try:
            dump_times, load_times = test_to_file(obj, dump_func, load_func)
        except:
            click.echo("the {} protocol does not support this object type".format(prot_name))
            prot_failed = True

        if prot_failed:
            row = {
                'protocol' : prot_name,
                'avg. dump' : np.nan,
                'avg. load' : np.nan,
            }

        else:
            row = {
                'protocol' : prot_name,
                'avg. dump' : np.mean(dump_times),
                'avg. load' : np.mean(load_times),
            }

        timings_rows.append(row)

    timings_df = pd.DataFrame(timings_rows, columns=timings_columns)

    click.echo(timings_df)




if __name__ == "__main__":

    main()
