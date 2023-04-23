# coding: utf-8

# In[ ]:

import glob
import gzip
import json
import os

JSON_DATA_DIR = "../../data/raw/"


# In[ ]:

#we removed all the encodes to utf-8 since we open the file in utf8 mode, also not sure where replacing tabs/ \
# is applicable

def parse_bio(bio_part):
    first_name, last_name = "None", "None"
    if bio_part["person"]["name"]["given-names"]:
        first_name = bio_part["person"]["name"]["given-names"]["value"] #.encode('utf-8').replace("\t", " ")
    if bio_part["person"]["name"]["family-name"]:
        last_name = bio_part["person"]["name"]["family-name"]["value"]  #.encode('utf-8').replace("\t", " ")
    if bio_part["person"]["biography"]["content"]:
        bio = bio_part["person"]["biography"]['content'] #.encode('utf-8').replace("\t", " ").replace("\n", " ")
        #used to be biography['value'] - unsure what value is supposed to be grabbed (2 instances)
    else: bio = "None"
    if bio_part["person"]["researcher-urls"]: 
        researcher_urls = [str(u['url']['value']).replace("\t", " ") for u in bio_part["person"]["researcher-urls"]["researcher-url"]]
    else: researcher_urls = "None"
    if bio_part["person"]["addresses"]: 
        if bio_part["person"]["addresses"]["address"]:
            country=[]
            countryL = bio_part["person"]["addresses"]["address"] #[0]["country"]["value"] #.replace("\t", " ")
            for dic in countryL:
                if not dic["country"]:
                    continue
                country.append(dic["country"]["value"])

            #ask kenny for help, not sure if dict is always in 0th position or not
            #need to check if multiple addresses can exist within "addresses" 
                    
        else: country = "None"
    else: country = "None"

    if bio_part["person"]['keywords']: #done
        keywords = [str(k["source"]["source-name"]['value'].encode('utf-8')) for k in bio_part["person"]['keywords']['keyword']]
    else: keywords = "None"
    
    return [first_name, last_name, str(bio), str(researcher_urls), str(country), str(keywords)]

def parse(filename):
    with open(filename, encoding="utf8") as data_file:
        data = json.load(data_file)

        #ID
        id = str(data["orcid-identifier"]['path'])

        #BIO
        if data['person']:
            bio_values = parse_bio(data)
        else:
            bio_values = ["None", "None", "None", "None", "None", "None"]
            
    int=0
    values=["first_name: ", "family_name: ", "biography: ", "urls: ", "country: ", "keywords: "]
    for val in bio_values:
        print()
        print("parse result "+ values[int])
        print(val)
        int+=1
    return bio_values, id

def parse_affiliations(file_name):
    f = json.load(open(file_name))
    f = f['orcid-profile']
    if not 'orcid-activities' in f or not f['orcid-activities']:
        return {}
    aff = f['orcid-activities'].get('affiliations',{})
    if not aff:
        return {}
    print()
    print("parse_affiliations result")
    return aff
    


# In[ ]:


# In[ ]:

parse('0000-0002-2032-5000.json')


# %%
