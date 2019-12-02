from jsonmerge import merge
import json
import os

# function to check for for JSON schemafile
# call with something like actionbatch_schema = schemafile_check('/path/to/folder', 'schemafile.jsoh')
def schemafile_check(schemadir, schemafile):
    schemapath = os.path.join(schemadir, schemafile)
    try:
        with open(schemapath) as schemastream:
            schema = json.load(schemastream)
    except:
        print(f'Error:  JSON schema file not found.  Path to file relative to this exe/script is "{schemapath}"')
        exit(0)
    return schema

class JSONTools:
    """Class to take 1 or more JSON files, check their validity, combine them, and write them to a new file if the user chose to do so in GUI"""
    def __init__(self, jsonfiles):
        self.jsonfiles = jsonfiles
        all_jsonfiles = {}
        
        # return a dictionary of both invalid and valid json files
        for file in jsonfiles:
            with open(file, 'rb') as jsonfile:
                try:
                    json_data = json.loads(jsonfile.read())
                    all_jsonfiles.update( {file : 'Valid JSON'} )
                except ValueError:
                    all_jsonfiles.update( {file : 'Invalid JSON'} )
        
        # return a list of only valid files
        valid_jsonfiles = []
        for key, value in all_jsonfiles.items():
            if value == 'Valid JSON':
                valid_jsonfiles.append(key)
        
        # return a list of only invalid files
        invalid_jsonfiles = []
        for key, value in all_jsonfiles.items():
            if value == 'Invalid JSON':
                invalid_jsonfiles.append(key)

        self.all_jsonfiles = all_jsonfiles
        self.valid_jsonfiles = valid_jsonfiles
        self.invalid_jsonfiles = invalid_jsonfiles

    def mergejson(self, head, schema, exportfile):
        data = {}

        # load all the JSON files and merge them with jsonmerge.merge, use the schema loaded from schema/skeletonchema
        for file in self.valid_jsonfiles:
            with open(file, 'rb') as jsonfile:
                jsondata = json.loads(jsonfile.read())
                data.update(merge(data, jsondata, schema))

        # Update dict with merged data and prepend our header (head) using our loaded JSON schema
        if head is not None:
            combined_json = merge(head, data, schema)
        else:
            combined_json = data
        
        # write to export file if it is defined
        if exportfile is not '':
            exportjson(exportfile, combined_json)
        else:
            pass
        
        # return the entire payload as expected by ActionBatch API (confirmed + sync + actions)
        return combined_json

# seperated from main class for reusability
def exportjson(exportfile, json):             
    indentedjson = json.dumps(json, indent=4)
    jsonoutfile = open(exportfile, 'w')
    jsonoutfile.write(indentedjson)
    jsonoutfile.close()

