#!/usr/bin/env python

import os

import click
import datapackage
import pandas as pd


@click.command
@click.argument('input_path', 'output_path')
def plots(input_path, output_path='/pfs/out'):
    dp = datapackage.DataPackage(descriptor=os.path.join(input_path,
                                                         'datapackage.json'))
    for r in dp.descriptor['resources']:
        df = pd.read_csv(r['path'])
        fig = df.plot().get_figure()
        fig.savefig(os.path.join(output_path, '{}.png'.format(r['name'])))


if __name__ == '__main__':
    plots()
