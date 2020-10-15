revSpinDict={'Hurricane 3':'DHS Hurricane 3 (H3)',
             'Tenergy 05':'Butterfly Tenergy 05',
             'MXP':'Tibhar Evolution MX-P'}


import pandas as pd

def rubbers_conversion():

    """
    retrieve rubber names list from CSV

    return:
    revSpinDict: Dictionary that converts value to label
    revSpinDropdown: list of dictionary for each options in dropdown menu
    """
    path = './assets/rubber_names.csv'
    df = pd.read_csv(path)
    
    print(df.shape)
    
    revspin_dict = dict()
    dropdown_menu_list = []
    
    for row in df.iterrows():
        row_data = row[1]
        value = row_data['label']
        label = row_data['value']
        
        ## Load data into dictionary
        revspin_dict[value] = label

        ## Load data into list of dictionary
        tmp = {'label':label,'value':value}
        dropdown_menu_list.append(tmp)
    
    print("Dictionary Length: {}".format(len(revSpinDict.keys())))
    print("Dropdown Menu Length: {}".format(len(dropdown_menu_list)))

    return revspin_dict,dropdown_menu_list

if __name__=="__main__":
    revspin_dict,dropdown_menu_list = rubbers_conversion()
    #print(revspin_dict.keys())
    for cur in revspin_dict.keys():
        print(cur)


