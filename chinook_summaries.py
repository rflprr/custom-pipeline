#!/usr/bin/env python

import os

import click
import datapackage
import pandas as pd


@click.command()
@click.argument('input_path')
@click.option('-o', '--output_path', default='/pfs/out')
def chinook_summaries(input_path, output_path='/pfs/out'):
    dp = datapackage.DataPackage(descriptor=os.path.join(input_path,
                                                         'datapackage.json'))

    dp_out = datapackage.DataPackage()
    dp_out.descriptor['name'] = 'chinook-summary'
    dp_out.descriptor['title'] = 'chinook-summary'
    dp_out.descriptor['description'] = 'Summary Stats from Chinook DB'
    dp_out.descriptor['x-visibility'] = 'PRIVATE'
    dp_out.descriptor['licenses'] = [
        {'name': 'Other'}
    ]
    dp_out.descriptor['resources'] = []
    for r in dp.descriptor['resources']:
        print('Processing {} with format {}'.format(
            r['path'],
            r['format']))
        if r.get('format', '') == 'csv':
            print('Attempting stats for {} with format {}'.format(
                r['path'],
                r['format']))
            df = pd.read_csv(os.path.join(dp.base_path, r['path']))
            try:
                stats = df.describe()
                plot_name = os.path.basename('{}.txt'.format(r['name']))
                with open(os.path.join(output_path, plot_name), 'w') as f:
                    f.write(str(stats))
                dp_out.descriptor['resources'].append({
                    'name': plot_name,
                    'path': plot_name})
                print('Done generating stats for {} with format {}'.format(
                    r['path'],
                    r['format']))
            except:
                print('Failed to generate stats for {} with format {}'.format(
                    r['path'],
                    r['format']))

    with open(os.path.join(output_path, 'datapackage.json'), 'w') as f:
        f.write(dp_out.to_json())


if __name__ == '__main__':
    chinook_summaries()
