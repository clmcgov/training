'''
Today we'll start working with tabular data. Pandas is going to be the go-to
tool for that. If you're familiar with R, pandas should feel familiar to you.
As an example, we'll start parsing the 2019 water balance sheet.

This is going to be ugly and that's okay -- we don't want to invest a ton of
time in this because we really only need to do it once. We do want to make it so
that we can do it exactly the same way again, so that we can easily chase down
any problems we might run into later. We don't care if it's fast and we don't
care if it's pretty. It just needs to work and have good comments.

On that note, I've tried to make this a sort of "stream of consciousness"
lesson. I've never parsed one of these completely before, so I'm just going to
start working and write down my entire process as I go. As always, the goal
today is to teach a process, not a task.

>>> import pandas as pd

>>> from pathlib import Path

>>> path = Path('~/Documents/WaterBalance Corn19.xlsx')

>>> pd.read_excel(path)
...
    Note: SWD values, if measured before irrigation and the same day as irrigation was applied must be added to the spreadsheet the day before the irrigation event (day before actual measurement).  ...         Unnamed: 182
0                                        Water Balance                                                                                                                                                ...                  NaN
1                                                 Date                                                                                                                                                ...  2019-11-11 00:00:00
2                                                  DOY                                                                                                                                                ...                  315
3                                 Root Zone Depth (mm)                                                                                                                                                ...                 1050
4                                                  NaN                                                                                                                                                ...                  NaN
..                                                 ...                                                                                                                                                ...                  ...
365                                                200                                                                                                                                                ...                  NaN
366                                                NaN                                                                                                                                                ...                  NaN
367                                                NaN                                                                                                                                                ...                  NaN
368                                                NaN                                                                                                                                                ...                  NaN
369                                             Yields                                                                                                                                                ...                  NaN
<BLANKLINE>
[370 rows x 183 columns]

That's definitely not what we want. Let's see how we can refine our statement.

>>> help(pd.read_excel)

Well that's a lot. Let's review some of the arguments:

sheet_name : str, int, list, or None, default 0
    Strings are used for sheet names. Integers are used in zero-indexed
    sheet positions. Lists of strings/integers are used to request
    multiple sheets. Specify None to get all sheets.

    Available cases:

    * Defaults to ``0``: 1st sheet as a `DataFrame`
    * ``1``: 2nd sheet as a `DataFrame`
    * ``"Sheet1"``: Load sheet with name "Sheet1"
    * ``[0, 1, "Sheet5"]``: Load first, second and sheet named "Sheet5"
      as a dict of `DataFrame`
    * None: All sheets.

Since we aren't specifying any value for sheet_name, it will take on the
default value of 0, meaning that the function will read the first sheet only.
For now that's okay, since we'll work on reading the raw data to start, but
we'll eventually need to change this argument. We'll pass this explicitly so our
code is more clear, and will thow an error if the sheet is missing or misnamed.

header : int, list of int, default 0
    Row (0-indexed) to use for the column labels of the parsed
    DataFrame. If a list of integers is passed those row positions will
    be combined into a ``MultiIndex``. Use None if there is no header.

By default, we're using the first row as the header. Looking at the sheet, we
can see that the first row has only one column that contains a bunch of text --
our output makes more sense now. Let's try passing header=None, since our column
names are really all in the first column right now, and not the first row.

>>> pd.read_excel(path, sheet_name='Raw Data', header=None)
...
                                                   0    ...                  182
0    Note: SWD values, if measured before irrigatio...  ...                  NaN
1                                        Water Balance  ...                  NaN
2                                                 Date  ...  2019-11-11 00:00:00
3                                                  DOY  ...                  315
4                                 Root Zone Depth (mm)  ...                 1050
..                                                 ...  ...                  ...
366                                                200  ...                  NaN
367                                                NaN  ...                  NaN
368                                                NaN  ...                  NaN
369                                                NaN  ...                  NaN
370                                             Yields  ...                  NaN
<BLANKLINE>
[371 rows x 183 columns]

Okay... we're closer. Looking at the sheet, the first two rows don't actually
contain any tabular data, so we probably want to skip them. Let's look at
another argument:

skiprows : list-like
    Rows to skip at the beginning (0-indexed).

Convenient! We'll skip the first two rows by passing [0, 1]

>>> df = pd.read_excel(path, sheet_name='Raw Data', header=None, skiprows=[0, 1])

>>> df
                          0                    1    ...                  181                  182
0                        Date  2019-05-14 00:00:00  ...  2019-11-10 00:00:00  2019-11-11 00:00:00
1                         DOY                  134  ...                  314                  315
2        Root Zone Depth (mm)                   50  ...                 1050                 1050
3                         NaN                  NaN  ...                  NaN                  NaN
4    Canopy Cover (%) SWB_0.9                    0  ...                    0                    0
..                        ...                  ...  ...                  ...                  ...
364                       200               12.308  ...                  NaN                  NaN
365                       NaN              191.797  ...                  NaN                  NaN
366                       NaN               246.75  ...                  NaN                  NaN
367                       NaN                  NaN  ...                  NaN                  NaN
368                    Yields                  NaN  ...                  NaN                  NaN
<BLANKLINE>
[369 rows x 183 columns]

Better, but we're not quite there. Let's transpose our table so that like values
are in columns, rather than rows. This will allow us to set a datatype on each
column and represent the data as contiguous arrays, which we know is
desirable.

>>> df.transpose()
...
                     0    1                     2    3    ...      365     366  367     368
0                   Date  DOY  Root Zone Depth (mm)  NaN  ...      NaN     NaN  NaN  Yields
1    2019-05-14 00:00:00  134                    50  NaN  ...  191.797  246.75  NaN     NaN
2    2019-05-15 00:00:00  135                    50  NaN  ...      NaN     NaN  NaN     NaN
3    2019-05-16 00:00:00  136                    50  NaN  ...      NaN     NaN  NaN     NaN
4    2019-05-17 00:00:00  137                    50  NaN  ...      NaN     NaN  NaN     NaN
..                   ...  ...                   ...  ...  ...      ...     ...  ...     ...
178  2019-11-07 00:00:00  311                  1050  NaN  ...      NaN     NaN  NaN     NaN
179  2019-11-08 00:00:00  312                  1050  NaN  ...      NaN     NaN  NaN     NaN
180  2019-11-09 00:00:00  313                  1050  NaN  ...      NaN     NaN  NaN     NaN
181  2019-11-10 00:00:00  314                  1050  NaN  ...      NaN     NaN  NaN     NaN
182  2019-11-11 00:00:00  315                  1050  NaN  ...      NaN     NaN  NaN     NaN
<BLANKLINE>
[183 rows x 369 columns]

Better still! Unfortunately, we can see that our column names are appearing as
values, with an integer index on both our columns and our rows. Let's take a
look at another argument:

index_col : int, list of int, default None
    Column (0-indexed) to use as the row labels of the DataFrame.
    Pass None if there is no such column.  If a list is passed,
    those columns will be combined into a ``MultiIndex``.  If a
    subset of data is selected with ``usecols``, index_col
    is based on the subset.

We can use this argument to set the first column as our row labels. That way,
when we transpose the dataframe, they will become our column labels.

>>> df = pd.read_excel(path, sheet_name='Raw Data', header=None, skiprows=[0, 1],
...     index_col=0).transpose()

>>> df
...
0         Date  DOY Root Zone Depth (mm)  NaN  ...      NaN     NaN  NaN Yields
1   2019-05-14  134                   50  NaN  ...  191.797  246.75  NaN    NaN
2   2019-05-15  135                   50  NaN  ...      NaN     NaN  NaN    NaN
3   2019-05-16  136                   50  NaN  ...      NaN     NaN  NaN    NaN
4   2019-05-17  137                   50  NaN  ...      NaN     NaN  NaN    NaN
5   2019-05-18  138                   50  NaN  ...      NaN     NaN  NaN    NaN
..         ...  ...                  ...  ...  ...      ...     ...  ...    ...
178 2019-11-07  311                 1050  NaN  ...      NaN     NaN  NaN    NaN
179 2019-11-08  312                 1050  NaN  ...      NaN     NaN  NaN    NaN
180 2019-11-09  313                 1050  NaN  ...      NaN     NaN  NaN    NaN
181 2019-11-10  314                 1050  NaN  ...      NaN     NaN  NaN    NaN
182 2019-11-11  315                 1050  NaN  ...      NaN     NaN  NaN    NaN
<BLANKLINE>
[182 rows x 369 columns]

Oh wow! Now we know that column and row labels are basically interchangable.
Let's revisit our decision to pass header=None -- if we allow the 'date' row
to be our header, then our transposed dataframe will have dates as row labels,
which seems like a good idea.

>>> df = pd.read_excel(path, sheet_name='Raw Data', header=0, skiprows=[0, 1],
...     index_col=0).transpose()

>>> df
...
Date        DOY Root Zone Depth (mm)  NaN Canopy Cover (%) SWB_0.9  ...      NaN     NaN  NaN Yields
2019-05-14  134                   50  NaN                        0  ...  191.797  246.75  NaN    NaN
2019-05-15  135                   50  NaN                        0  ...      NaN     NaN  NaN    NaN
2019-05-16  136                   50  NaN                        0  ...      NaN     NaN  NaN    NaN
2019-05-17  137                   50  NaN                        0  ...      NaN     NaN  NaN    NaN
2019-05-18  138                   50  NaN                        0  ...      NaN     NaN  NaN    NaN
...         ...                  ...  ...                      ...  ...      ...     ...  ...    ...
2019-11-07  311                 1050  NaN                        0  ...      NaN     NaN  NaN    NaN
2019-11-08  312                 1050  NaN                        0  ...      NaN     NaN  NaN    NaN
2019-11-09  313                 1050  NaN                        0  ...      NaN     NaN  NaN    NaN
2019-11-10  314                 1050  NaN                        0  ...      NaN     NaN  NaN    NaN
2019-11-11  315                 1050  NaN                        0  ...      NaN     NaN  NaN    NaN
<BLANKLINE>
[182 rows x 368 columns]

Now we have empty columns where we used to have empty rows. Those were great for
human readability, but not so great for machines. We also have some columns with
no name and very little data -- we'll make a mental note to revisit that. Let's
get help on the dataframe's dropna method for now:

>>> help(df.dropna)

There are two parameters that we're interested in here:

axis : {0 or 'index', 1 or 'columns'}, default 0
    Determine if rows or columns which contain missing values are
    removed.

    * 0, or 'index' : Drop rows which contain missing values.
    * 1, or 'columns' : Drop columns which contain missing value.

    .. deprecated:: 0.23.0

       Pass tuple or list to drop on multiple axes.
       Only a single axis is allowed.

how : {'any', 'all'}, default 'any'
    Determine if row or column is removed from DataFrame, when we have
    at least one NA or all NA.

    * 'any' : If any NA values are present, drop that row or column.
    * 'all' : If all values are NA, drop that row or column.

Since we're trying to drop empty columns, we know our axis should be 1 and not
the default 0. We could also pass 'columns', but we'll need to use the axis
argument in a lot of methods and functions and passing a string isn't always an
option, so we should get used to integers. These correspond to the indices of
dimensions of the dataframe.

>>> df.shape
(182, 368)

Scrolling up, you'll see that our dataframe has 182 rows (position 0) and 368
columns(position 1).

Looking at the how argument, we'll definitely want to specify 'all', since the
default is 'any' and we only want to drop completely empty columns.

Let's see how that looks:

>>> df.dropna(axis=1, how='all')
...
Date        DOY Root Zone Depth (mm) Canopy Cover (%) SWB_0.9  ...     200      NaN     NaN
2019-05-14  134                   50                        0  ...  12.308  191.797  246.75
2019-05-15  135                   50                        0  ...     NaN      NaN     NaN
2019-05-16  136                   50                        0  ...     NaN      NaN     NaN
2019-05-17  137                   50                        0  ...     NaN      NaN     NaN
2019-05-18  138                   50                        0  ...     NaN      NaN     NaN
...         ...                  ...                      ...  ...     ...      ...     ...
2019-11-07  311                 1050                        0  ...     NaN      NaN     NaN
2019-11-08  312                 1050                        0  ...     NaN      NaN     NaN
2019-11-09  313                 1050                        0  ...     NaN      NaN     NaN
2019-11-10  314                 1050                        0  ...     NaN      NaN     NaN
2019-11-11  315                 1050                        0  ...     NaN      NaN     NaN
<BLANKLINE>
[182 rows x 315 columns]

Perfect, but this brings us back to those nameless columns -- apparently there
are quite a few of them. Let's look back to the sheet. Starting at row 196,
things get funny. We start to have a mix of global constants (197-205), row-
major timestamped records (all of the above), treatment constants (224-226),
etc. Really, we have a number of tables on one sheet. How many?

Let's break down what we've got into some general categories. In this sheet, all
data pertains either to the entire experiment or a particular treatment. So,
that's one way we do it. We'll call them "site" data and "treatment" data.
Additionally, some data are timestamped ("records") while other data are not
("constants").

That leaves us with four potential tables, each separated from the others in
time and/or space: site constants, site records, treatment constants, and
treatment records.

We're probably going to want to read the sheet a few times, looking for
different things each time. This isn't the most efficient approach, but what
we're doing is fundamentally inefficient -- clarity is more important here so
that any potential problems are easy to find, and the code will be easily
adaptable to sheets from other years that have slightly different formats.

There seems to be some significant overhead associated with opening excel files,
regardless of what or how much you read. To avoid this, we'll revisit the io
argument to the read_excel function:

io : str, ExcelFile, xlrd.Book, path object or file-like object
    Any valid string path is acceptable. The string could be a URL. Valid
    URL schemes include http, ftp, s3, and file. For file URLs, a host is
    expected. A local file could be: ``file://localhost/path/to/table.xlsx``.

    If you want to pass in a path object, pandas accepts any ``os.PathLike``.

    By file-like object, we refer to objects with a ``read()`` method,
    such as a file handler (e.g. via builtin ``open`` function)
    or ``StringIO``.

Note that in addition to a path, the read_excel method accepts a xlrd.Book.
We'll open one of those, and read from it as often as we need to, keeping in
mind that it will need to be closed at some point. How to get one?

>>> import xlrd

>>> help(xlrd.Book)

Looks like we need to use the open_workbook function.

>>> book = xlrd.open_workbook(path)

>>> help(book)

We don't need to know too much about this object, since we're just going to pass
it to the pandas read_excel method, but note the "release_resouces" method --
this is similar to a close() method, and we can see that it is indeed invoked
when the read_workbook function exits and was called as a conext manager.

Okay, what we've done so was a good start on reading records. Instead of
dropping null columns after transposing, let's be pickier about which rows we
read. We'll read all of the records together, since they all have the same
shape, and then break them out by site/treatment later.

We already know that we need to skip the first two rows. It's pretty easy to
see that we can also skip rows 5, 18, 31, 33, 35, 37 and 50. We'll initialize
our skip list with those rows.

>>> skip = [0, 1, 5, 18, 31, 33, 35, 37, 50]

After that there's a repeating pattern of four rows of data and eight empty
rows. There's one block like this for each treamment, so 12 blocks. We don't
want to do this all by hand. The repeating pattern starts at row 55, so we'll
initialize a counter there:

>>> n = 55

Next, for each set of twelve rows, we want to skip the first 8, and we want to
do it 12 times:

>>> for _ in range(12):
...     skip.extend(n + j for j in range(8))
...     n += 12

>>> skip
[0, 1, 5, 18, 31, 33, 35, 37, 50,
 55, 56, 57, 58, 59, 60, 61, 62, ... 187, 188, 189, 190, 191, 192, 193, 194]

Looking good. Now we need to skip everything from there to the growth stage
data

>>> skip.extend(range(195, 206))

That's done, and now there is nothing else of interest, so we want to skip the
rest of the sheet. Let's look at one more argument to read_excel:

nrows : int, default None
    Number of rows to parse.

This parameter is kind of funny. It doesn't include initial skipped rows, but
does include subsequent ones. Whatever -- trial and error shows us that 215 is
the right answer (read through to row 217, less the first two rows).

Let's give it a shot:

>>> df = pd.read_excel(book, sheet_name='Raw Data', header=0, skiprows=skip,
...     nrows=215, index_col=0).transpose()

>>> list(df.columns)
...
['DOY',
 'Root Zone Depth (mm)',
 'Canopy Cover (%) SWB_0.9',
 'Canopy Cover CWSIB_0.9 (%)',
 'Canopy Cover DANS_0.9 (%)',
 'Canopy Cover CWSIT_0.9 (%)',
 'Canopy Cover CWSIT_0.65 (%)',
 'Canopy Cover CWSIB_0.65 (%)',
 'Canopy Cover SWB_0.65 (%)',
 'Canopy Cover DANS_0.65 (%)',
 'Canopy Cover CWSIT_0.4 (%)',
 'Canopy Cover SWB_0.4  (%)',
 'Canopy Cover DANS_0.4 (%)',
 'Canopy Cover CWSIB_0.4 (%)',
 'Ks SWB_0.9',
 'Ks CWSIB_0.9',
 'Ks DANS_0.9',
 'Ks CWSIT_0.9',
 'Ks CWSIT_0.65',
 'Ks CWSIB_0.65',
 'Ks SWB_0.65',
 'Ks DANS_0.65',
 'Ks CWSIT_0.4',
 'Ks SWB_0.4',
 'Ks DANS_0.4',
 'Ks CWSIB_0.4',
 'ETr LIRF (mm/d)',
 'ETc Bowen (mm/d)',
 'Precip (mm)',
 'Actual Irrigation SWB_0.9 (mm)',
 'Actual Irrigation CWSIB_0.9 (mm)',
 'Actual Irrigation DANS_0.9 (mm)',
 'Actual Irrigation CWSIT_0.9 (mm)',
 'Actual Irrigation CWSIT_0.65 (mm)',
 'Actual Irrigation CWSIB_0.65 (mm)',
 'Actual Irrigation SWB_0.65 (mm)',
 'Actual Irrigation DANS_0.65 (mm)',
 'Actual Irrigation CWSIT_0.4 (mm)',
 'Actual Irrigation SWB_0.4 (mm)',
 'Actual Irrigation DANS_0.4 (mm)',
 'Actual Irrigation CWSIB_0.4 (mm)',
 'SWD (15) SWB_0.9 (%)',
 'SWD (30) SWB_0.9 (%)',
 'SWD (60) SWB_0.9 (%)',
 'SWD (90) SWB_0.9 (%)',
 'SWD (15) CWSIB_0.9 (%)',
 'SWD (30) CWSIB_0.9 (%)',
 'SWD (60) CWSIB_0.9 (%)',
 'SWD (90) CWSIB_0.9 (%)',
 'SWD (15) DANS_0.9 (%)',
 'SWD (30) DANS_0.9 (%)',
 'SWD (60) DANS_0.9 (%)',
 'SWD (90) DANS_0.9 (%)',
 'SWD (15) CWSIT_0.9 (%)',
 'SWD (30) CWSIT_0.9 (%)',
 'SWD (60) CWSIT_0.9 (%)',
 'SWD (90) CWSIT_0.9 (%)',
 'SWD (15) CWSIT_0.65 (%)',
 'SWD (30) CWSIT_0.65 (%)',
 'SWD (60) CWSIT_0.65 (%)',
 'SWD (90) CWSIT_0.65 (%)',
 'SWD (15) CWSIB_0.65 (%)',
 'SWD (30) CWSIB_0.65 (%)',
 'SWD (60) CWSIB_0.65 (%)',
 'SWD (90) CWSIB_0.65 (%)',
 'SWD (15) SWB_0.65 (%)',
 'SWD (30) SWB_0.65 (%)',
 'SWD (60) SWB_0.65 (%)',
 'SWD (90) SWB_0.65 (%)',
 'SWD (15) DANS_0.65 (%)',
 'SWD (30) DANS_0.65 (%)',
 'SWD (60) DANS_0.65 (%)',
 'SWD (90) DANS_0.65 (%)',
 'SWD (15) CWSIT_0.4 (%)',
 'SWD (30) CWSIT_0.4 (%)',
 'SWD (60) CWSIT_0.4 (%)',
 'SWD (90) CWSIT_0.4 (%)',
 'SWD (15) SWB_0.4 (%)',
 'SWD (30) SWB_0.4 (%)',
 'SWD (60) SWB_0.4 (%)',
 'SWD (90) SWB_0.4 (%)',
 'SWD (15) DANS_0.4 (%)',
 'SWD (30) DANS_0.4 (%)',
 'SWD (60) DANS_0.4 (%)',
 'SWD (90) DANS_0.4 (%)',
 'SWD (15) CWSIB_0.4 (%)',
 'SWD (30) CWSIB_0.4 (%)',
 'SWD (60) CWSIB_0.4 (%)',
 'SWD (90) CWSIB_0.4 (%)',
 'Growth Stage SWB_0.9',
 'Growth Stage CWSIB_0.9',
 'Growth Stage DANS_0.9',
 'Growth Stage CWSIT_0.9',
 'Growth Stage CWSIT_0.65',
 'Growth Stage CWSIB_0.65',
 'Growth Stage SWB_0.65',
 'Growth Stage DANS_0.65',
 'Growth Stage CWSIT_0.4',
 'Growth Stage SWB_0.4',
 'Growth Stage DANS_0.4',
 'Growth Stage CWSIB_0.4']

Perfect! Now we can split this dataframe into site and treatment columns.

>>> st = df[['DOY', 'Root Zone Depth (mm)', 'Precip (mm)', 'ETr LIRF (mm/d)',
...     'ETc Bowen (mm/d)']]

DataFrame columns define a number of methods associated with sets. We can
use the difference method to figure out which are plot columns.

>>> len(df.columns)
101

>>> len(df.columns.difference(st.columns))
96

>>> tx = df[df.columns.difference(st.columns)]

Okay -- site is done, but we've still got a fair bit of work to do. Right now,
treament is basically a stack of pivot tables, and we need to unpivot them all.
The first step will be extracting the treatment from the column name.

There are probably a lot of ways to do this, we're going to choose one. We'll
iterate through the columns, removing units from each. When that's done, the
last word in each column is the treament, and the remaining words are the new
column name. Each of the resulting tuples contains (treament, new column name,
old column name).

>>> tmp = []

>>> for c in tx.columns:
...     s = [x for x in c.split(' ') if not x in ('(%)', '(mm)')]
...     tmp.append((s[-1], '_'.join(s[:-1]), c))

>>> tmp
...
[('CWSIB_0.4', 'Actual_Irrigation', 'Actual Irrigation CWSIB_0.4 (mm)'),
 ('CWSIB_0.65', 'Actual_Irrigation', 'Actual Irrigation CWSIB_0.65 (mm)'),
 ('CWSIB_0.9', 'Actual_Irrigation', 'Actual Irrigation CWSIB_0.9 (mm)'),
 ('CWSIT_0.4', 'Actual_Irrigation', 'Actual Irrigation CWSIT_0.4 (mm)'),
 ('CWSIT_0.65', 'Actual_Irrigation', 'Actual Irrigation CWSIT_0.65 (mm)'),
 ('CWSIT_0.9', 'Actual_Irrigation', 'Actual Irrigation CWSIT_0.9 (mm)'),
 ('DANS_0.4', 'Actual_Irrigation', 'Actual Irrigation DANS_0.4 (mm)'),
 ('DANS_0.65', 'Actual_Irrigation', 'Actual Irrigation DANS_0.65 (mm)'),
 ('DANS_0.9', 'Actual_Irrigation', 'Actual Irrigation DANS_0.9 (mm)'),
 ('SWB_0.4', 'Actual_Irrigation', 'Actual Irrigation SWB_0.4 (mm)'),
 ('SWB_0.65', 'Actual_Irrigation', 'Actual Irrigation SWB_0.65 (mm)'),
 ('SWB_0.9', 'Actual_Irrigation', 'Actual Irrigation SWB_0.9 (mm)'),
 ('SWB_0.9', 'Canopy_Cover', 'Canopy Cover (%) SWB_0.9'),
 ('CWSIB_0.4', 'Canopy_Cover', 'Canopy Cover CWSIB_0.4 (%)'),
 ('CWSIB_0.65', 'Canopy_Cover', 'Canopy Cover CWSIB_0.65 (%)'),
 ('CWSIB_0.9', 'Canopy_Cover', 'Canopy Cover CWSIB_0.9 (%)'),
 ('CWSIT_0.4', 'Canopy_Cover', 'Canopy Cover CWSIT_0.4 (%)'),
 ('CWSIT_0.65', 'Canopy_Cover', 'Canopy Cover CWSIT_0.65 (%)'),
 ('CWSIT_0.9', 'Canopy_Cover', 'Canopy Cover CWSIT_0.9 (%)'),
 ('DANS_0.4', 'Canopy_Cover', 'Canopy Cover DANS_0.4 (%)'),
 ('DANS_0.65', 'Canopy_Cover', 'Canopy Cover DANS_0.65 (%)'),
 ('DANS_0.9', 'Canopy_Cover', 'Canopy Cover DANS_0.9 (%)'),
 ('', 'Canopy_Cover_SWB_0.4', 'Canopy Cover SWB_0.4  (%)'),
 ('SWB_0.65', 'Canopy_Cover', 'Canopy Cover SWB_0.65 (%)'),
 ('CWSIB_0.4', 'Growth_Stage', 'Growth Stage CWSIB_0.4'),
 ('CWSIB_0.65', 'Growth_Stage', 'Growth Stage CWSIB_0.65'),
 ('CWSIB_0.9', 'Growth_Stage', 'Growth Stage CWSIB_0.9'),
 ('CWSIT_0.4', 'Growth_Stage', 'Growth Stage CWSIT_0.4'),
 ('CWSIT_0.65', 'Growth_Stage', 'Growth Stage CWSIT_0.65'),
 ('CWSIT_0.9', 'Growth_Stage', 'Growth Stage CWSIT_0.9'),
 ('DANS_0.4', 'Growth_Stage', 'Growth Stage DANS_0.4'),
 ('DANS_0.65', 'Growth_Stage', 'Growth Stage DANS_0.65'),
 ('DANS_0.9', 'Growth_Stage', 'Growth Stage DANS_0.9'),
 ('SWB_0.4', 'Growth_Stage', 'Growth Stage SWB_0.4'),
 ('SWB_0.65', 'Growth_Stage', 'Growth Stage SWB_0.65'),
 ('SWB_0.9', 'Growth_Stage', 'Growth Stage SWB_0.9'),
 ('CWSIB_0.4', 'Ks', 'Ks CWSIB_0.4'),
 ('CWSIB_0.65', 'Ks', 'Ks CWSIB_0.65'),
 ('CWSIB_0.9', 'Ks', 'Ks CWSIB_0.9'),
 ('CWSIT_0.4', 'Ks', 'Ks CWSIT_0.4'),
 ('CWSIT_0.65', 'Ks', 'Ks CWSIT_0.65'),
 ('CWSIT_0.9', 'Ks', 'Ks CWSIT_0.9'),
 ('DANS_0.4', 'Ks', 'Ks DANS_0.4'),
 ('DANS_0.65', 'Ks', 'Ks DANS_0.65'),
 ('DANS_0.9', 'Ks', 'Ks DANS_0.9'),
 ('SWB_0.4', 'Ks', 'Ks SWB_0.4'),
 ('SWB_0.65', 'Ks', 'Ks SWB_0.65'),
 ('SWB_0.9', 'Ks', 'Ks SWB_0.9'),
 ('CWSIB_0.4', 'SWD_(15)', 'SWD (15) CWSIB_0.4 (%)'),
 ('CWSIB_0.65', 'SWD_(15)', 'SWD (15) CWSIB_0.65 (%)'),
 ('CWSIB_0.9', 'SWD_(15)', 'SWD (15) CWSIB_0.9 (%)'),
 ('CWSIT_0.4', 'SWD_(15)', 'SWD (15) CWSIT_0.4 (%)'),
 ('CWSIT_0.65', 'SWD_(15)', 'SWD (15) CWSIT_0.65 (%)'),
 ('CWSIT_0.9', 'SWD_(15)', 'SWD (15) CWSIT_0.9 (%)'),
 ('DANS_0.4', 'SWD_(15)', 'SWD (15) DANS_0.4 (%)'),
 ('DANS_0.65', 'SWD_(15)', 'SWD (15) DANS_0.65 (%)'),
 ('DANS_0.9', 'SWD_(15)', 'SWD (15) DANS_0.9 (%)'),
 ('SWB_0.4', 'SWD_(15)', 'SWD (15) SWB_0.4 (%)'),
 ('SWB_0.65', 'SWD_(15)', 'SWD (15) SWB_0.65 (%)'),
 ('SWB_0.9', 'SWD_(15)', 'SWD (15) SWB_0.9 (%)'),
 ('CWSIB_0.4', 'SWD_(30)', 'SWD (30) CWSIB_0.4 (%)'),
 ('CWSIB_0.65', 'SWD_(30)', 'SWD (30) CWSIB_0.65 (%)'),
 ('CWSIB_0.9', 'SWD_(30)', 'SWD (30) CWSIB_0.9 (%)'),
 ('CWSIT_0.4', 'SWD_(30)', 'SWD (30) CWSIT_0.4 (%)'),
 ('CWSIT_0.65', 'SWD_(30)', 'SWD (30) CWSIT_0.65 (%)'),
 ('CWSIT_0.9', 'SWD_(30)', 'SWD (30) CWSIT_0.9 (%)'),
 ('DANS_0.4', 'SWD_(30)', 'SWD (30) DANS_0.4 (%)'),
 ('DANS_0.65', 'SWD_(30)', 'SWD (30) DANS_0.65 (%)'),
 ('DANS_0.9', 'SWD_(30)', 'SWD (30) DANS_0.9 (%)'),
 ('SWB_0.4', 'SWD_(30)', 'SWD (30) SWB_0.4 (%)'),
 ('SWB_0.65', 'SWD_(30)', 'SWD (30) SWB_0.65 (%)'),
 ('SWB_0.9', 'SWD_(30)', 'SWD (30) SWB_0.9 (%)'),
 ('CWSIB_0.4', 'SWD_(60)', 'SWD (60) CWSIB_0.4 (%)'),
 ('CWSIB_0.65', 'SWD_(60)', 'SWD (60) CWSIB_0.65 (%)'),
 ('CWSIB_0.9', 'SWD_(60)', 'SWD (60) CWSIB_0.9 (%)'),
 ('CWSIT_0.4', 'SWD_(60)', 'SWD (60) CWSIT_0.4 (%)'),
 ('CWSIT_0.65', 'SWD_(60)', 'SWD (60) CWSIT_0.65 (%)'),
 ('CWSIT_0.9', 'SWD_(60)', 'SWD (60) CWSIT_0.9 (%)'),
 ('DANS_0.4', 'SWD_(60)', 'SWD (60) DANS_0.4 (%)'),
 ('DANS_0.65', 'SWD_(60)', 'SWD (60) DANS_0.65 (%)'),
 ('DANS_0.9', 'SWD_(60)', 'SWD (60) DANS_0.9 (%)'),
 ('SWB_0.4', 'SWD_(60)', 'SWD (60) SWB_0.4 (%)'),
 ('SWB_0.65', 'SWD_(60)', 'SWD (60) SWB_0.65 (%)'),
 ('SWB_0.9', 'SWD_(60)', 'SWD (60) SWB_0.9 (%)'),
 ('CWSIB_0.4', 'SWD_(90)', 'SWD (90) CWSIB_0.4 (%)'),
 ('CWSIB_0.65', 'SWD_(90)', 'SWD (90) CWSIB_0.65 (%)'),
 ('CWSIB_0.9', 'SWD_(90)', 'SWD (90) CWSIB_0.9 (%)'),
 ('CWSIT_0.4', 'SWD_(90)', 'SWD (90) CWSIT_0.4 (%)'),
 ('CWSIT_0.65', 'SWD_(90)', 'SWD (90) CWSIT_0.65 (%)'),
 ('CWSIT_0.9', 'SWD_(90)', 'SWD (90) CWSIT_0.9 (%)'),
 ('DANS_0.4', 'SWD_(90)', 'SWD (90) DANS_0.4 (%)'),
 ('DANS_0.65', 'SWD_(90)', 'SWD (90) DANS_0.65 (%)'),
 ('DANS_0.9', 'SWD_(90)', 'SWD (90) DANS_0.9 (%)'),
 ('SWB_0.4', 'SWD_(90)', 'SWD (90) SWB_0.4 (%)'),
 ('SWB_0.65', 'SWD_(90)', 'SWD (90) SWB_0.65 (%)'),
 ('SWB_0.9', 'SWD_(90)', 'SWD (90) SWB_0.9 (%)')]

Looks pretty good, but what happend with 'Canopy Cover SWB_0.4  (%)'? A close
looks shows that it's got a sneaky extra space. Let's see what happens when we
split this and drop the units:

>>> c = 'Canopy Cover SWB_0.4  (%)'

>>> [x for x in c.split(' ') if not x in ('(%)', '(mm)')]
...
['Canopy', 'Cover', 'SWB_0.4', '']

Uh-oh, it looks like splitting two spaces on a space returns an empty string
(''). This explains our problem. Fortunately, an empty string evaluates to
False when treated as a boolean.

>>> bool('')
False

We can add an extra condition to our comprehension to sort this out:

>>> [x for x in c.split(' ') if x and not x in ('(%)', '(mm)')]
['Canopy', 'Cover', 'SWB_0.4']

Let's try again.

>>> tmp = []

>>> for c in tx.columns:
...     s = [x for x in c.split(' ') if x and not x in ('(%)', '(mm)')]
...     tmp.append((s[-1], '_'.join(s[:-1]), c))

How do we use our newly corrected list of tuples? Let's make it a Dataframe.

>>> tmp = pd.DataFrame(tmp)

>>> tmp
...
             0                  1                                  2
0    CWSIB_0.4  Actual_Irrigation   Actual Irrigation CWSIB_0.4 (mm)
1   CWSIB_0.65  Actual_Irrigation  Actual Irrigation CWSIB_0.65 (mm)
2    CWSIB_0.9  Actual_Irrigation   Actual Irrigation CWSIB_0.9 (mm)
3    CWSIT_0.4  Actual_Irrigation   Actual Irrigation CWSIT_0.4 (mm)
4   CWSIT_0.65  Actual_Irrigation  Actual Irrigation CWSIT_0.65 (mm)
..         ...                ...                                ...
91   DANS_0.65           SWD_(90)             SWD (90) DANS_0.65 (%)
92    DANS_0.9           SWD_(90)              SWD (90) DANS_0.9 (%)
93     SWB_0.4           SWD_(90)               SWD (90) SWB_0.4 (%)
94    SWB_0.65           SWD_(90)              SWD (90) SWB_0.65 (%)
95     SWB_0.9           SWD_(90)               SWD (90) SWB_0.9 (%)
<BLANKLINE>
[96 rows x 3 columns]

Now we can use the dataframe's groupby method. This returns a pretty fancy
object, but to get an idea of how it works, we'll wrap it in a call to list
and get the first item:

>>> ex = list(tmp.groupby(0))[0]

>>> ex
...
('CWSIB_0.4',
             0                  1                                 2
 0   CWSIB_0.4  Actual_Irrigation  Actual Irrigation CWSIB_0.4 (mm)
 13  CWSIB_0.4       Canopy_Cover        Canopy Cover CWSIB_0.4 (%)
 24  CWSIB_0.4       Growth_Stage            Growth Stage CWSIB_0.4
 36  CWSIB_0.4                 Ks                      Ks CWSIB_0.4
 48  CWSIB_0.4           SWD_(15)            SWD (15) CWSIB_0.4 (%)
 60  CWSIB_0.4           SWD_(30)            SWD (30) CWSIB_0.4 (%)
 72  CWSIB_0.4           SWD_(60)            SWD (60) CWSIB_0.4 (%)
 84  CWSIB_0.4           SWD_(90)            SWD (90) CWSIB_0.4 (%))

We got a tuple of (group key, group).

Now what? For starters, we can pull out all of the columns pertaining to a
particular treatment as a dataframe:

>>> tx[ex[1][2]].columns
...
Index(['Actual Irrigation CWSIB_0.4 (mm)', 'Canopy Cover CWSIB_0.4 (%)',
       'Growth Stage CWSIB_0.4', 'Ks CWSIB_0.4', 'SWD (15) CWSIB_0.4 (%)',
       'SWD (30) CWSIB_0.4 (%)', 'SWD (60) CWSIB_0.4 (%)',
       'SWD (90) CWSIB_0.4 (%)'],
      dtype='object', name='Date')

That's not super helpful yet, since we want to bring all of the treatments
together. We can use our group to create a helpful dictionary:

We can use the to_records method to transfrom the last two columns into a
collection of tuples of (old name, new name).

>>> ex[1][[2, 1]].to_records(index=False)
...
rec.array([('Actual Irrigation CWSIB_0.4 (mm)', 'Actual_Irrigation'),
           ('Canopy Cover CWSIB_0.4 (%)', 'Canopy_Cover'),
           ('Growth Stage CWSIB_0.4', 'Growth_Stage'),
           ('Ks CWSIB_0.4', 'Ks'), ('SWD (15) CWSIB_0.4 (%)', 'SWD_(15)'),
           ('SWD (30) CWSIB_0.4 (%)', 'SWD_(30)'),
           ('SWD (60) CWSIB_0.4 (%)', 'SWD_(60)'),
           ('SWD (90) CWSIB_0.4 (%)', 'SWD_(90)')],
          dtype=[('2', 'O'), ('1', 'O')])

If we pass this to the dictionary constructor, we get something pretty nice
that we can use to rename the columns in our smaller dataframe:

>>> names = dict(ex[1][[2, 1]].to_records(index=False))

>>> names
{'Actual Irrigation CWSIB_0.4 (mm)': 'Actual_Irrigation',
 'Canopy Cover CWSIB_0.4 (%)': 'Canopy_Cover',
 'Growth Stage CWSIB_0.4': 'Growth_Stage',
 'Ks CWSIB_0.4': 'Ks',
 'SWD (15) CWSIB_0.4 (%)': 'SWD_(15)',
 'SWD (30) CWSIB_0.4 (%)': 'SWD_(30)',
 'SWD (60) CWSIB_0.4 (%)': 'SWD_(60)',
 'SWD (90) CWSIB_0.4 (%)': 'SWD_(90)'}

Neat, now let's use this to generate a renamed dataframe:

>>> tx[ex[1][2]].rename(columns=names)
...
Date       Actual_Irrigation Canopy_Cover Growth_Stage Ks SWD_(15) SWD_(30) SWD_(60) SWD_(90)
2019-05-14               NaN            0          NaN  1      NaN      NaN      NaN      NaN
2019-05-15               NaN            0     Planting  1      NaN      NaN      NaN      NaN
2019-05-16               NaN            0          NaN  1      NaN      NaN      NaN      NaN
2019-05-17               NaN            0          NaN  1      NaN      NaN      NaN      NaN
2019-05-18               NaN            0          NaN  1      NaN      NaN      NaN      NaN
...                      ...          ...          ... ..      ...      ...      ...      ...
2019-11-07               NaN            0          NaN  1      NaN      NaN      NaN      NaN
2019-11-08               NaN            0          NaN  1      NaN      NaN      NaN      NaN
2019-11-09               NaN            0          NaN  1      NaN      NaN      NaN      NaN
2019-11-10               NaN            0          NaN  1      NaN      NaN      NaN      NaN
2019-11-11               NaN            0          NaN  1      NaN      NaN      NaN      NaN
<BLANKLINE>
[182 rows x 8 columns]

That's pretty good -- it's got the correct column names. Unfortunately we have
nothing to idenify the treatment. We'll use the assign method to deal with this,
and then append that column to our index.

>>> tx[ex[1][2]].rename(columns=names).assign(tx=ex[0]) \
    .set_index('tx', append=True)
...
Date       Actual_Irrigation Canopy_Cover Growth_Stage Ks SWD_(15) SWD_(30) SWD_(60) SWD_(90)         tx
2019-05-14               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-15               NaN            0     Planting  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-16               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-17               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-18               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
...                      ...          ...          ... ..      ...      ...      ...      ...        ...
2019-11-07               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-11-08               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-11-09               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-11-10               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-11-11               NaN            0          NaN  1      NaN      NaN      NaN      NaN  CWSIB_0.4
<BLANKLINE>
[182 rows x 9 columns]

Well, a lot of stuff has happened. Let's bring it together again:

>>> res = []

>>> for name, frame in tmp.groupby(0):
...     cols = dict(frame[[2, 1]].to_records(index=False))
...     res.append(tx[frame[2]].rename(columns=cols).assign(tx=name))

For the record, this is the wrong way to use a groupby, but we're just trying
to get through this. It works, so it's right for us.

>>> [x.shape for x in res]
...
[(182, 9), (182, 9), (182, 9), (182, 9), (182, 9), (182, 9), (182, 9),
 (182, 9), (182, 9), (182, 9), (182, 9), (182, 9)]

Finally, using pandas' concat function, we can unify the frames.

>>> tx = pd.concat(res)

>>> tx
...
Date       Actual_Irrigation Canopy_Cover Growth_Stage        Ks SWD_(15) SWD_(30) SWD_(60) SWD_(90)         tx
2019-05-14               NaN            0          NaN         1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-15               NaN            0     Planting         1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-16               NaN            0          NaN         1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-17               NaN            0          NaN         1      NaN      NaN      NaN      NaN  CWSIB_0.4
2019-05-18               NaN            0          NaN         1      NaN      NaN      NaN      NaN  CWSIB_0.4
...                      ...          ...          ...       ...      ...      ...      ...      ...        ...
2019-11-07               NaN            0          NaN  0.619361      NaN      NaN      NaN      NaN    SWB_0.9
2019-11-08               NaN            0          NaN  0.614724      NaN      NaN      NaN      NaN    SWB_0.9
2019-11-09               NaN            0          NaN   0.61055      NaN      NaN      NaN      NaN    SWB_0.9
2019-11-10               NaN            0          NaN         0      NaN      NaN      NaN      NaN    SWB_0.9
2019-11-11               NaN            0          NaN         0      NaN      NaN      NaN      NaN    SWB_0.9
<BLANKLINE>
[2184 rows x 9 columns]

Now we can add the treatment to our index and sort

>>> tx = tx.set_index('tx', append=True).sort_index()

>>> tx
...
Date                  Actual_Irrigation Canopy_Cover Growth_Stage Ks SWD_(15) SWD_(30) SWD_(60) SWD_(90)
           tx
2019-05-14 CWSIB_0.4                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIB_0.65               NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIB_0.9                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIT_0.4                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIT_0.65               NaN            0          NaN  1      NaN      NaN      NaN      NaN
...                                 ...          ...          ... ..      ...      ...      ...      ...
2019-11-11 DANS_0.65                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           DANS_0.9                 NaN            0          NaN  1      NaN      NaN      NaN      NaN
           SWB_0.4                  NaN            0          NaN  0      NaN      NaN      NaN      NaN
           SWB_0.65                 NaN            0          NaN  0      NaN      NaN      NaN      NaN
           SWB_0.9                  NaN            0          NaN  0      NaN      NaN      NaN      NaN
<BLANKLINE>
[2184 rows x 8 columns]

Before, it looked like the Date heading refered to the column of dates, but
keeping in mind that we transposed the rows into columns, we can see how pandas
thought it was the name of our column index.

>>> tx.columns.name
'Date'

We'll just set that to None to avoid confusion.

>>> tx.columns.name = None

Additionally, the date column of the index has no name. We'll fix it.

>>> tx.index.names = ['datetime', 'tx']

>>> tx
                      Actual_Irrigation Canopy_Cover Growth_Stage Ks SWD_(15) SWD_(30) SWD_(60) SWD_(90)
datetime   tx
2019-05-14 CWSIB_0.4                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIB_0.65               NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIB_0.9                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIT_0.4                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           CWSIT_0.65               NaN            0          NaN  1      NaN      NaN      NaN      NaN
...                                 ...          ...          ... ..      ...      ...      ...      ...
2019-11-11 DANS_0.65                NaN            0          NaN  1      NaN      NaN      NaN      NaN
           DANS_0.9                 NaN            0          NaN  1      NaN      NaN      NaN      NaN
           SWB_0.4                  NaN            0          NaN  0      NaN      NaN      NaN      NaN
           SWB_0.65                 NaN            0          NaN  0      NaN      NaN      NaN      NaN
           SWB_0.9                  NaN            0          NaN  0      NaN      NaN      NaN      NaN
<BLANKLINE>
[2184 rows x 8 columns]

Finally, let's see about data types

>>> tx.info()
<class 'pandas.core.frame.DataFrame'>
MultiIndex: 2184 entries, (2019-05-14 00:00:00, CWSIB_0.4) to (2019-11-11 00:00:00, SWB_0.9)
Data columns (total 8 columns):
Actual_Irrigation    240 non-null object
Canopy_Cover         2184 non-null object
Growth_Stage         168 non-null object
Ks                   2184 non-null object
SWD_(15)             324 non-null object
SWD_(30)             312 non-null object
SWD_(60)             312 non-null object
SWD_(90)             312 non-null object
dtypes: object(8)
memory usage: 144.5+ KB

Oh boy. The DataFrame is acting like a giant list -- everything has a dtype of
"object." That is to say that each column is an array of pointers, each of which
could be pointing at anything at all -- not good. With the exception of growth
stage, all of our columns are numeric.

>>> for col in tx.columns:
...     if col != 'Growth_Stage':
...         tx[col] = tx[col].astype('float32')

>>> tx.info()
...
<class 'pandas.core.frame.DataFrame'>
MultiIndex: 2184 entries, (2019-05-14 00:00:00, CWSIB_0.4) to (2019-11-11 00:00:00, SWB_0.9)
Data columns (total 8 columns):
Actual_Irrigation    240 non-null float32
Canopy_Cover         2184 non-null float32
Growth_Stage         168 non-null object
Ks                   2184 non-null float32
SWD_(15)             324 non-null float32
SWD_(30)             312 non-null float32
SWD_(60)             312 non-null float32
SWD_(90)             312 non-null float32
dtypes: float32(7), object(1)
memory usage: 84.8+ KB

Much better -- we've nearly halved our memory usage, and any numeric
calculations will be much faster. Normally pandas would infer all of this
pretty reliably, but the transposition messed things up.

We're going to need to do the same thing to site. We'll just make them all
floats.

>>> st = st.astype('float32')

We'll also set a key, just for good measure

>>> st['site'] = 'LIRF'

>>> st = st.set_index('site', append=True)

Well, now we've successfully read all of the records in this sheet. Let's write
a function to do it (see accompanying module). Now we turn to constants. For
this, we'll read the same sheet again, but in a different way. We'll start with
site constants.

We're not really interested in anything before row 197, so we can skip right
up to there.

>>> skip = list(range(197))

>>> skip.append(200)

>>> skip.extend(range(205, 220))

>>> df = pd.read_excel(book, sheet_name='Raw Data', header=None, skiprows=skip,
...     nrows=25, index_col=0, usecols=1)

Here again, nrows is fairly hard to know -- some guessing helps. usecols tells
pandas to use only column 1, since column 0 is the row index. As before, we
can go ahead and transpose and rename

>>> df = df.T.rename(columns={
...     'TEW (mm)': 'TEW',
...     'drip hose offset (ratio)': 'drip hose offset',
...     'Tot Avail Water (%FC)': 'Tot Avail Water',
...     'Red Avail Water (%FC)': 'Red Avail Water'})

We'll also set a site key, even though there's only one.

>>> df['site'] = 'LIRF'

And set the index

>>> df = df.set_index('site')

And drop the column index name

>>> df.columns.name = None

>>> df
...
      Residue Cover   TEW  drip hose offset     a       b     c  CCf  Tot Avail Water  Red Avail Water (%TAW)
site
LIRF            0.5  12.0               0.1  0.15  1.0125  0.96  0.8              0.5                     0.5

Now, we're finally ready to do plot constants. We have one transposed table
having to do with SWD (row 225 -- I don't know what it is), and then a
series of field capacity pivot tables (row 228).

It will be easiest to just read this in two chunks. We're all about easy here --
optimizing this would not make sense. We just want to figure out how to read it
reliably and repeatably once, and then hopefully we don't need to do it again.

>>> df = pd.read_excel(book, sheet_name='Raw Data', header=None, skiprows=224,
...     nrows=2, usecols=12, index_col=0)

In this case, usecols=12 means "use all the columns through 12," much as
skirows=224 means "start reading at 224." We get a warning that it's deprecated,
so let's read that and comply:

>>> df = pd.read_excel(book, sheet_name='Raw Data', header=None, skiprows=224,
...     nrows=2, usecols=range(13), index_col=0)

>>> df
...
                    1   2   3   4   5   6   7   8   9   10  11  12
0
Proj SWD - 1050 mm  10  10  10  10  10  10  10  10  10  10  10  10
Proj SWD - RZ        6   6   6   6   6   6   6   6   6   6   6   6


We have an integer columns index. Let's just set the names directly

>>> df.columns = ['SWB_0.9', 'CWSIB_0.9', 'DANS_0.9', 'CWSIT_0.9', 'CWSIT_0.65',
... 'CWSIB_0.65', 'SWB_0.65', 'DANS_0.65', 'CWSIT_0.4', 'SWB_0.4', 'DANS_0.4',
... 'CWSIB_0.4']

>>> df
...
                    SWB_0.9  CWSIB_0.9  DANS_0.9  CWSIT_0.9  CWSIT_0.65  CWSIB_0.65  SWB_0.65  DANS_0.65  CWSIT_0.4  SWB_0.4  DANS_0.4  CWSIB_0.4
0
Proj SWD - 1050 mm       10         10        10         10          10          10        10         10         10       10        10         10
Proj SWD - RZ             6          6         6          6           6           6         6          6          6        6         6          6


and drop the index name (it will become the columns) and transpose

>>> df.index.name = None

>>> df = df.T

>>> df
...
            Proj SWD - 1050 mm  Proj SWD - RZ
SWB_0.9                     10              6
CWSIB_0.9                   10              6
DANS_0.9                    10              6
CWSIT_0.9                   10              6
CWSIT_0.65                  10              6
CWSIB_0.65                  10              6
SWB_0.65                    10              6
DANS_0.65                   10              6
CWSIT_0.4                   10              6
SWB_0.4                     10              6
DANS_0.4                    10              6
CWSIB_0.4                   10              6

Finally, we can try to unravel those field capacity pivot tables. We'll start
by reading all of them, and then we can iterate over each group by indexing the
dataframe.

>>> df2 = pd.read_excel(book, sheet_name='Raw Data', header=None, skiprows=227,
...     index_col=0, usecols=1).dropna(how='all')

>>> df2
...
                    1
0
Tmnt SWB_0.9       FC
15               28.5
30            24.3249
60            22.3367
90            19.9075
...               ...
120           8.86368
150           9.45408
200            12.308
NaN           191.797
NaN            246.75
<BLANKLINE>
[120 rows x 1 columns]

Well, it turns out there was data hidden in those collapsed rows, so dropna
didn't drop them. Instead of that, we'll just iterate more carefully.

>>> df2 = pd.read_excel(book, sheet_name='Raw Data', header=None, skiprows=227,
...     index_col=0, usecols=[0,1])

>>> res = []

>>> for n in range(12):
...     n = n * 12
...     tmnt = df2.iloc[n].name.split(' ')[1]
...     data = df2.iloc[(n + 1):(n + 8)].T
...     data['tmnt'] = tmnt
...     data.columns.name = None
...     res.append(data)

>>> res = pd.concat(res).set_index('tmnt')

>>> res
...
               15       30       60       90       120      150      200
tmnt
SWB_0.9       28.5  24.3249  22.3367  19.9075  17.3394  15.0434     15.5
CWSIB_0.9       28  24.3683  22.2488  15.3617  11.5449  11.7571  14.2324
DANS_0.9        29  25.1059  23.4342  18.4654  14.0369  14.2444  14.0142
CWSIT_0.9    28.75  26.6649  20.6798  12.5412  13.3235  13.7356  14.7472
CWSIT_0.65    27.5  23.3105  17.4274  12.7539  9.43511  9.61608  13.0796
CWSIB_0.65   27.25  22.2235  19.6461  10.2077  9.68488   9.2947  15.0071
SWB_0.65     28.25  24.6111  17.0541  12.0277  8.59895  11.6431   13.576
DANS_0.65    27.25  20.3705  14.6262  9.87365  8.79927  9.42449  12.3999
CWSIT_0.4       27  20.9428  18.7871  11.5308  10.8711  10.6409  15.7986
SWB_0.4         27   26.104  20.9227  10.5291  11.1003  10.6428  14.4652
DANS_0.4     27.25  23.7911  18.5274   11.855  11.5128    10.85  13.5894
CWSIB_0.4   26.625  21.0661  17.7718  11.7817  8.86368  9.45408   12.308

The last thing we need to do here is rename the columns

>>> res.columns = ['fc_{}'.format(c) for c in res.columns]

And combine it with df

>>> res = pd.concat([res, df], axis=1)

>>> res
...
             fc_15    fc_30    fc_60    fc_90   fc_120   fc_150   fc_200  Proj SWD - 1050 mm  Proj SWD - RZ
tmnt
SWB_0.9       28.5  24.3249  22.3367  19.9075  17.3394  15.0434     15.5                  10              6
CWSIB_0.9       28  24.3683  22.2488  15.3617  11.5449  11.7571  14.2324                  10              6
DANS_0.9        29  25.1059  23.4342  18.4654  14.0369  14.2444  14.0142                  10              6
CWSIT_0.9    28.75  26.6649  20.6798  12.5412  13.3235  13.7356  14.7472                  10              6
CWSIT_0.65    27.5  23.3105  17.4274  12.7539  9.43511  9.61608  13.0796                  10              6
CWSIB_0.65   27.25  22.2235  19.6461  10.2077  9.68488   9.2947  15.0071                  10              6
SWB_0.65     28.25  24.6111  17.0541  12.0277  8.59895  11.6431   13.576                  10              6
DANS_0.65    27.25  20.3705  14.6262  9.87365  8.79927  9.42449  12.3999                  10              6
CWSIT_0.4       27  20.9428  18.7871  11.5308  10.8711  10.6409  15.7986                  10              6
SWB_0.4         27   26.104  20.9227  10.5291  11.1003  10.6428  14.4652                  10              6
DANS_0.4     27.25  23.7911  18.5274   11.855  11.5128    10.85  13.5894                  10              6
CWSIB_0.4   26.625  21.0661  17.7718  11.7817  8.86368  9.45408   12.308                  10              6

'''

if __name__ == '__main__':
    from doctest import testmod, NORMALIZE_WHITESPACE, ELLIPSIS, \
        IGNORE_EXCEPTION_DETAIL
    testmod(verbose=False, optionflags=NORMALIZE_WHITESPACE | ELLIPSIS
        | IGNORE_EXCEPTION_DETAIL)
