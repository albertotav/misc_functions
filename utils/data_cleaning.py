"""Collection of data cleaning functions.
"""

import pandas as pd

def translate_month_pt(df):
  """Translates month strings in Portuguese to English in a pd.DataFrame.
  For example: ‘Dezembro’ to ‘december’ and ‘Dez’ to ‘dec’.
  The input month is case insensitive and always return months in lowercase.
  WARNING: Will translate every string in the DataFrame that matches a month name or initials.
  Input columns with only dates as string.

  :param pd.DataFrame df: DataFrame columns with string dates in Portuguese.

  :returns: DataFrame with translated string dates
  :rtype: pd.DataFrame
  """
  df = df.replace(to_replace={
      '(?i)Janeiro':'january', '(?i)Jan':'jan',
      '(?i)Fevereiro':'february', '(?i)Fev':'feb',
      '(?i)Março':'march', '(?i)Mar':'mar',
      '(?i)Abril':'april', '(?i)Abr':'apr',
      '(?i)Maio':'may', '(?i)Mai':'may',
      '(?i)Junho':'june', '(?i)Jun':'jun',
      '(?i)Julho':'july', '(?i)Jul':'jul',
      '(?i)Agosto':'august', '(?i)Ago':'aug',
      '(?i)Setembro':'september', '(?i)Set':'set',
      '(?i)Outubro':'october', '(?i)Out':'oct',
      '(?i)Novembro':'november', '(?i)Nov':'nov',
      '(?i)Dezembro':'december', '(?i)Dez':'dec',}, regex=True)
  return df