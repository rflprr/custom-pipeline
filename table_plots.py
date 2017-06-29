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

    dp_out = datapackage.DataPackage()
    dp_out['name'] = 'nba-plots'
    dp_out['title'] = 'nba-plots'
    dp_out['description'] = 'My NBA Plots'
    dp_out['x-visibility'] = 'PRIVATE'
    dp_out['licenses'] = [
        {'name': 'Other'}
    ]
    dp_out['resources'] = []
    for r in dp.descriptor['resources']:
        df = pd.read_csv(r['path'])
        fig = df.plot().get_figure()
        plot_name = '{}.png'.format(r['name'])
        fig.savefig(os.path.join(output_path, plot_name))
        dp_out['resources'].append({'name': plot_name, 'path': plot_name})

    with open(os.path.join(output_path, 'datapackage.json'), 'w') as f:
        f.write(dp_out.to_json())


if __name__ == '__main__':
    plots()
