'''
Quick and easy Deidentificaiton tool.  
Written by Dirk Colbry 01-24-2024

This set of very simple functions can help DID a csv file. The idea is that you first create a lookup table consisting of usernames and "fake" usernames. In this case the facke usernames are just "user_XX" where XX is a uniqe number.  The lookup table is saved as a file so that different csv files can use the same lookup.  Here is how we create a lookup table and save it as a "SECRET" csv file:

    # Get the usernames from the input data file
    df = pd.read_csv('First contact - Attempt Details.csv')
    usernames = set(df['Username'])
    
    # Make sure the usernames is a list of ALL usernames in all files.  
    lookup_table = DID.makeLookup(usernames)
    DID.dict2LU(lookup_table).to_csv('did_data.csv') # Save out lookup table

Once you have a lookup table you don't want to change it so the answers are consistat between CSV files.  Now we can deidentify the data using code similar to the following

    # Deidentify data
    filename = 'First contact - Attempt Details.csv'
    df = pd.read_csv('First contact - Attempt Details.csv')
    df['FirstName'] = 'DID'
    df['LastName'] = 'DID'
    
    # Now the important part. Read in the table and replace the usernames
    lookup_table = DID.LU2dict(pd.read_csv('did_data.csv')) 
    result_df = DID.use_dict_lookup(df, lookup_table, 'Username')
    
    # Save the file using a new prefix.
    result_df.to_csv(f"DID_{filename}")

That is basdically it.  Notice in the above example we also cleared out other data that could be used for identification.  

'''
import random
import pandas as pd

def dict2LU(lookup_table):
    '''Make a pandas username lookup table from a dictionary lookup table'''
    return pd.DataFrame(list(lookup_table.items()), columns=['Original_Name', 'DID_Name'])

def LU2dict(input_df): 
    '''Make a dictary username lookup table from a pandas lookup table'''
    # Converting DataFrame to dictionary
    result_dict = dict(zip(input_df['Original_Name'], input_df['DID_Name']))
    return result_dict

def updateLookup(names, newnames, prefix='user'):
    '''PLACEHOLDER. Tool to check and add names to list, right now we assume everyone is there'''
    help(updateLookup)
    pass

def use_dict_lookup(df, replacement_dict,column_name = 'username'):
    '''Replace values in the specified column of a dataframe using the lookup dictionary'''
    df[column_name] = df[column_name].map(replacement_dict)
    return df

def use_df_lookup(df, replacement_dict, column_name = 'username'):
    '''PLACEHOLDER. Replace values in the specified column of a dataframe using the lookup dataframe'''
    help(use_df_lookup)
    pass

def makeLookup(names, prefix='user'):
    '''Make a lookup table from a list of names. You also have an option to adjust the user prefix'''
    lookup_table = dict()
    names = list(names)
    random.shuffle(names)
    index = 0
    for name in names:
        lookup_table[name] = f"user_{index:03}"
        index +=1
    return lookup_table