# Quick and easy Deidentificaiton tool.  
### Written by Dirk Colbry 01-24-2024

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
