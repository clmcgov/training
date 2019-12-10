
from pathlib import Path
from pdb import set_trace

import pandas as pd
import xlrd

# every column with dtype (change as needed)
DTYPES = {
    'Actual Irrigation':    'float32',
    'CCf':                  'float32',
    'Canopy Cover':         'float32',
    'DOY':                  'uint16',
    'ETc Bowen':            'float32',
    'ETr LIRF':             'float32',
    'Growth Stage':         'category',
    'Ks':                   'float32',
    'Precip':               'float32',
    'Proj SWD - 1050 mm':   'float32',
    'Proj SWD - RZ':        'float32',
    'Red Avail Water':      'float32',
    'Residue Cover':        'float32',
    'Root Zone Depth':      'uint16',
    'SWD (15)':             'float32',
    'SWD (30)':             'float32',
    'SWD (60)':             'float32',
    'SWD (90)':             'float32',
    'TEW':                  'float32',
    'Tot Avail Water':      'float32',
    'a':                    'float32',
    'b':                    'float32',
    'c':                    'float32',
    'drip hose offset':     'float32',
    'fc_15':                'float32',
    'fc_30':                'float32',
    'fc_60':                'float32',
    'fc_90':                'float32',
    'fc_120':               'float32',
    'fc_150':               'float32',
    'fc_200':               'float32'}

def main(path):
    path = Path(path)
    with xlrd.open_workbook(path) as book:
        site_records, tmnt_records = read_raw_records(book)
        site_constants = read_raw_site_constants(book)
        tmnt_constants = read_raw_tmnt_constants(book)
    return site_constants, site_records, tmnt_constants, tmnt_records

def read_raw_tmnt_constants(book):
    # read the first chunk of constants in horizontal table
    df1 = pd.read_excel(book, sheet_name='Raw Data', header=None, skiprows=224,
        nrows=2, usecols=range(13), index_col=0)
    # set future row labels
    df1.columns = ['SWB_0.9', 'CWSIB_0.9', 'DANS_0.9', 'CWSIT_0.9',
        'CWSIT_0.65', 'CWSIB_0.65', 'SWB_0.65', 'DANS_0.65', 'CWSIT_0.4',
        'SWB_0.4', 'DANS_0.4', 'CWSIB_0.4']
    # naming a column index is strange
    df1.index.name = None
    # make it vertical
    df1 = df1.transpose()
    # read the second chunk of stacked pivot tables
    df2 = df2 = pd.read_excel(book, sheet_name='Raw Data', header=None,
        skiprows=227, index_col=0, usecols=[0,1])
    res = []
    # one block for each treatment
    for n in range(12):
        # start index of block
        n = n * 12
        # get the header row and extract the treatment name
        tmnt = df2.iloc[n].name.split(' ')[1]
        # get the rest of the block and transpose
        data = df2.iloc[(n + 1):(n + 8)].T
        # set the treatment name
        data['tmnt'] = tmnt
        # as usual, drop the column index name
        data.columns.name = None
        # add to our collection
        res.append(data)
    # combine collected frames and set index on new treatment name column
    res = pd.concat(res).set_index('tmnt')
    # rename each fc depth with fc_ prefix for greater clarity
    res.columns = ['fc_{}'.format(c) for c in res.columns]
    set_dtypes(res)
    return res

def read_raw_site_constants(book):
    # skip down to be top of the chunk
    skip = list(range(197))
    # skip extra white space
    skip.append(200)
    # skip over records
    skip.extend(range(205, 220))
    # read remaining rows, limit number
    df = pd.read_excel(book, sheet_name='Raw Data', header=None, skiprows=skip,
        nrows=25, index_col=0, usecols=1)
    # drop units
    df = df.T.rename(columns={
        'TEW (mm)': 'TEW',
        'drip hose offset (ratio)': 'drip hose offset',
        'Tot Avail Water (%FC)': 'Tot Avail Water',
        'Red Avail Water (%TAW)': 'Red Avail Water'})
    # add spatial key
    df['site'] = 'LIRF'
    # spatial key only
    df = df.set_index('site')
    # don't need named column index
    df.columns.name = None
    # set dtypes
    set_dtypes(df)
    return df

def read_raw_records(book):
    # skip empty/non-data rows
    skip = [0, 1, 5, 18, 31, 33, 35, 37, 50]
    # start of repeating empty row sequence
    n = 55
    # sequence repeats for each treatment
    for i in range(12):
        # add empty row numbers to skip
        skip.extend(n + j for j in range(8))
        # set n to n + 12
        n += 12
    # add additional non-target rows
    skip.extend(range(195, 206))
    # read relevant rows and transpose
    df = pd.read_excel(book, sheet_name='Raw Data', header=0, skiprows=skip,
        nrows=215, index_col=0).transpose()
    # get site records
    site = df[['DOY', 'Root Zone Depth (mm)', 'Precip (mm)', 'ETr LIRF (mm/d)',
        'ETc Bowen (mm/d)']]
    # get treatment (ninja turtles?) records
    tmnt = df[df.columns.difference(site.columns)]
    # get rid of column index name (gained in transposition)
    tmnt.columns.name = None
    # get list of tuples of (treatment, new column, old column)]
    cols = []
    for col in tmnt.columns:
        # drop units if there are any, regardless of order
        split = [x for x in col.split(' ') if x and not x in ('(%)', '(mm)')]
        # separate treatment and column names, add underscores to columns
        cols.append((split[-1], ' '.join(split[:-1]), col))
    # convert cols to dataframe
    cols = pd.DataFrame(cols)
    # temporary container for dataframe parts
    tmp = []
    # group by treatment name
    for name, frame in cols.groupby(0):
        # build dictionary of {old: new} column names
        names = dict(frame[[2, 1]].to_records(index=False))
        # get and rename columns from the big frame
        tmp.append(tmnt[frame[2]].rename(columns=names).assign(tmnt=name))
    # reassign tmnt and set/sort index
    tmnt = pd.concat(tmp).set_index('tmnt', append=True).sort_index()
    # make sure datetime column of index has a name
    tmnt.index.names = ['datetime', 'tmnt']
    # use correct data types
    set_dtypes(tmnt)
    # drop units from site columns and add underscores
    cols = {
        c: ' '.join(c.split(' ')[:-1])
        for c in site.columns if c != 'DOY'}
    # set site name
    site['site'] = 'LIRF'
    # rename site columns ans set index
    site = site.rename(columns=cols).set_index('site', append=True)
    # don't need name for columns index
    site.columns.name = None
    # make sure datetime is named correctly
    site.index.names = ['datetime', 'site']
    # set site dtypes
    set_dtypes(site)
    # return tuple
    return site, tmnt

def set_dtypes(df):
    for col in df.columns:
        df[col] = df[col].astype(DTYPES[col])
