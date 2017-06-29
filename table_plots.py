#!/usr/bin/env python

import os

import click
import datapackage
import pandas as pd


@click.command()
@click.argument('input_path')
@click.option('-o', '--output_path', default='/pfs/out')
def plots(input_path, output_path='/pfs/out'):
    dp = datapackage.DataPackage(descriptor=os.path.join(input_path,
                                                         'datapackage.json'))

    dp_out = datapackage.DataPackage()
    dp_out.descriptor['name'] = 'nba-plots'
    dp_out.descriptor['title'] = 'nba-plots'
    dp_out.descriptor['description'] = 'My NBA Plots'
    dp_out.descriptor['x-visibility'] = 'PRIVATE'
    dp_out.descriptor['licenses'] = [
        {'name': 'Other'}
    ]
    dp_out.descriptor['resources'] = []
    for r in dp.descriptor['resources']:
        if r.get('format', '') == 'csv':
            df = pd.read_csv(os.path.join(dp.base_path, r['path']))
            try:
                fig = df.plot().get_figure()
                plot_name = os.path.basename('{}.png'.format(r['name']))
                fig.savefig(os.path.join(output_path, plot_name))
                dp_out.descriptor['resources'].append({'name': plot_name, 'path':
                    plot_name})
            except:
                pass

    with open(os.path.join(output_path, 'datapackage.json'), 'w') as f:
        f.write(dp_out.to_json())


if __name__ == '__main__':
    plots()
