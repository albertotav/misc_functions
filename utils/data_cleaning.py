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

def normalize_string(string, case = None):
    """Return string without special characters.
    
    UPPERCASE if case = 'upper' or 'uppercase'

    lowercase if case = 'lower' or 'lowercase'
    """
    dict_special_char ={
    'â':'a','ã':'a','á':'a','à':'a','ä':'a',
    'Â':'A','Ã':'A','Á':'A','À':'A','Ä':'A',
    'ê':'e','é':'e','è':'e','ë':'e',
    'Ê':'E','É':'E','È':'E','Ë':'E',
    'í':'i','ì':'i','ï':'i',
    'Í':'I','Ì':'I','Ï':'I',
    'ô':'o','õ':'o','ó':'o','ò':'o','ö':'o',
    'Ô':'O','Õ':'O','Ó':'O','Ò':'O','Ö':'O',
    'ú':'u','ù':'u','ü':'u',
    'Ú':'U','Ù':'U','Ü':'U',
    'ç':'c','Ç':'C',
    '¹':'1','²':'2','³':'3',
    'ª':'','º':'','°':'',
    '£':'','¢':'','¬':'','§':'',
    '^':'','´':'','`':'','~':'','¨':'',
    ':':'_',';':'_','.':'_',',':'_','<':'_','>':'_',
    '+':'','=':'',
    ' ':'_','.':'','/':'_','__':'_',
    '!':'','?':'','@':'_','$':'','%':'','#':'','&':'','*':'_',
    '(':'_',')':'_','[':'_',']':'_','{':'_','}':'_',
    }
    excess_underscore ={
        '_____': '_',
        '____':'_',
        '___':'_',
        '__':'_',
    }
    # Remove special characters
    for key in dict_special_char.keys():
        string = string.replace(key, str(dict_special_char[key]))
    # Remove excessive underscore
    for key in excess_underscore.keys():
        string = string.replace(key, str(excess_underscore[key]))
    # Remove underscore from start/end of string
    if string[0] == '_':
        string = string[1:]
    if string[-1] == '_':
        string = string[:-1]
    # Set upper or lowercase
    if case == 'upper' or case == 'uppercase':
        return string.upper()
    if case == 'lower' or case == 'lowercase':
        return string.lower()
    return string