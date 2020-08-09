# python built-ins
import json, os, pathlib, pickle, time
from functools import reduce
# dependencies
from gooey import Gooey, GooeyParser
from jsonmerge import merge
from colored import stylize, colored, fg, attr
# local, written for this app
import jsontools, actionbatchrequests, usermessages

__author__ = 'Zach Brewer'
__email__ = 'zbrewer@cisco.com'
__version__ = '0.32.0'
__license__ = 'Cisco Sample Code License, Version 1.1'

# set default files and json schema
menufile = 'menu.pkl' # pickled menu file
configfile = 'defaults.json' # optional config file
schemadir = 'schemas' # directory for schemas
schemafile = 'action-batch-default.json'  # schemafile used as template for joining JSON payloads and options
debug = False

# load menu file from pickled file (very long, seperated for readability and modularity)
with open(menufile, 'rb') as f:
    menudata = pickle.load(f)

# setup parser settings
parser = GooeyParser() 
@Gooey(
    advanced=True,
    show_success_modal=False,
    richtext_controls=True,
    terminal_font_size=14,
    progress_regex=r'^Action batch \d{10,20} is still processing\. API call count: \d{1,20}$',
    disable_progress_bar_animation=False,
    auto_start=False,
    default_size=(685, 815),
    optional_cols=1,
    required_cols=2,
    program_name=f'Meraki Action Batcher (v{__version__})',
    clear_before_run=True,
    image_dir='images',
    menu=menudata
    )


# function to load default values from configfile defined in 1st section of this app
def load_defaults():
    if os.path.isfile(configfile):
        with open(configfile) as defaults_file:
            gui_defaults = json.load(defaults_file)
    else:
        gui_defaults = 'None'
    return gui_defaults

# check for schemafile with specific filename and path
actionbatch_schema = jsontools.schemafile_check(schemadir, schemafile)

########## END SETUP AND DEFAULTS ##########



########## BEGIN HELPER FUNCTIONS & CLASSES ##########

# allows us to get deeply nested dict keys using . notation else returns none
# e.g. print(deep_get(dictname, 'common.apikey'))
# dict.get only works with top level keys/items
# we need the return None like dict.get for deeply nested dict items
def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

# used for comparing 2 conditions with simple lists.  Right now used for ActionBatchStatus command.
# will likely make it more generic in the future for re-usability
def compare_batches(batchstatus, batchstatus_data):
    # generic lists to hold comparison ActionBatch IDs (e.g. error vs. noerrors, confirmed vs. unconfirmed, etc.)
    compare1 = []
    compare2 = []

    if batchstatus == 'Confirmed/UnConfirmed Action Batches':
        condition1 = 'confirmed'
        condition2 = 'unconfirmed'
        for data in batchstatus_data:
            if data['confirmed']:
                compare1.append(data['id'])
            elif not data['confirmed']:
                compare2.append(data['id'])
        print(stylize(f'{condition1} action batches (by ID):', usermessages.ok_formatting))
        print(*compare1, sep=',')
        print('\n')
        print(stylize(f'{condition2} action batches (by ID):', usermessages.ok_formatting))
        print(*compare2, sep=',')

    elif batchstatus == 'Completed/Incomplete Action Batches':
        condition1 = 'completed'
        condition2 = 'incomplete'
        for data in batchstatus_data:
            if (data['status']['completed']):
                compare1.append(data['id'])
            elif not (data['status']['completed']):
                compare2.append(data['id'])
        print(f'{condition1} action batches (by ID):')
        print(*compare1, sep=',')
        print('\n')
        print(f'{condition2} action batches (by ID):')
        print(*compare2, sep=',')

    elif batchstatus == 'Failed Action Batches':
        condition1 = 'failed'
        condition2 = 'successful'
        for data in batchstatus_data:
            if (data['status']['failed']):
                compare1.append(data['id'])
            elif not (data['status']['failed']):
                compare2.append(data['id'])
        print(f'{condition1} action batches (by ID):')
        print(*compare1, sep=',')
        print('\n')
        print(f'{condition2} action batches (by ID):')
        print(*compare2, sep=',')
    
    return condition1, condition2, compare1, compare2

# Helper function to check the completion status of an asynchronous action batch
def checkstatus(apikey, orgid, batchid):
    (ok, data) = actionbatchrequests.get_action_batch(apikey, orgid, batchid)
    if ok and data['status']['completed'] and not data['status']['failed']:
        print(f'Action batch {batchid} completed!')
        return 1
    elif ok and data['status']['failed']:
        print(f'Action batch {batchid} failed with errors {data["status"]["errors"]}!')
        return -1
    elif ok and not data['confirmed']:
        print(f'Action batch {batchid} has not been confirmed.  Update the Action Batch with a confirmed status.')
        return -2
    elif ok and not data['status']['completed'] and not data['status']['failed']:
         return -3
    else:
        return 0
######### END HELPER FUNCTIONS ##########
    

######### BEGIN ACTIONBATCHREQUESTS FUNCTIONS FOR API CALLS ##########
def createactionbatch(cmd_args):
    apikey = cmd_args['apikey'].replace('\n', '').replace(' ', '')
    orgid = cmd_args['orgid'].replace('\n', '').replace(' ', '')
    jsonfiles = []
    jsonfiles = str.split(cmd_args['jsonfiles'], ':')
    confirmed = cmd_args['confirmed']
    synchronous = cmd_args['synchronous']
    exportfile = cmd_args['exportfile']
    prettyprint = cmd_args['prettyprint']

    #define our json header based upon user input:
    jsonhead = {
    "confirmed": confirmed,
    "synchronous": synchronous,
    }

    # pass our jsonfiles to the jsontools module we wrote.  
    # keeps track of .all_jsonfiles, .invalid_jsonfiles, .valid_jsonfiles, and allows us to merge JSON
    working_json = jsontools.JSONTools(jsonfiles=jsonfiles)

    # if there are ANY invlaid JSON files then pass the full list of JSON files to function that notifies the user
    # otherwise merge all JSON and call the Meraki Dashboard API
    if working_json.invalid_jsonfiles:
        usermessages.invalid_json_usermessage(working_json.all_jsonfiles)
    else:
        # passes all valid JSON to the mergejson object in the JSONTools class instance
        # this merges the JSON from all files in order and builds a payload.  Also creates the exportfile if it is not an empty string
        jsonpayload = working_json.mergejson(head=jsonhead, schema=actionbatch_schema, exportfile=exportfile)
        
        # make our API call with the payload
        apicall_success, createbatch_data = actionbatchrequests.create_action_batch(apikey, orgid, confirmed, synchronous, jsonpayload)

        # test for bad API call and a space returned as the data
        if not apicall_success and createbatch_data == ' ':
            usermessage = usermessages.api_error_nostatus(apikey, orgid)
            print(usermessage)
        
        # test for failed API call (and attempt to print API error message)
        elif not apicall_success:
            usermessage = usermessages.api_error_status(apikey, orgid, createbatch_data)
            print(usermessage)
        
        # success
        elif apicall_success:
            print(json.dumps(createbatch_data, indent=4)) if prettyprint else print(createbatch_data)
        
def updateactionbatch(cmd_args):
    apikey = cmd_args['apikey'].replace('\n', '').replace(' ', '')
    orgid = cmd_args['orgid'].replace('\n', '').replace(' ', '')
    batchid = cmd_args['batchid'].replace('\n', '').replace(' ', '')
    confirmed = cmd_args['confirmed']
    synchronous = cmd_args['synchronous']
    prettyprint = cmd_args['prettyprint']

    apicall_success, updatebatch_data = actionbatchrequests.update_action_batch(apikey, orgid, batchid, confirmed, synchronous)

    # test for bad API call and a space returned as the data
    if not apicall_success and updatebatch_data == ' ':
        usermessage = usermessages.api_error_nostatus(apikey, orgid)
        print(usermessage)
    
    # test for failed API call (and attempt to print API error message)
    elif not apicall_success:
        usermessage = usermessages.api_error_status(apikey, orgid, updatebatch_data)
        print(usermessage)
    
    # success
    elif apicall_success:
        print(json.dumps(updatebatch_data, indent=4)) if prettyprint else print(updatebatch_data)

def getorgactionbatch(cmd_args):
    apikey = cmd_args['apikey'].replace('\n', '').replace(' ', '')
    orgid = cmd_args['orgid'].replace('\n', '').replace(' ', '')
    prettyprint = cmd_args['prettyprint']

    # make API call
    apicall_success, orgbatch_data = actionbatchrequests.get_org_action_batches(apikey, orgid)

    # test for bad API call and a space returned as the data
    if not apicall_success and orgbatch_data == ' ':
        usermessage = usermessages.api_error_nostatus(apikey, orgid)
        print(usermessage)

    # test for successful API call but no Action Batches returned for org given
    elif apicall_success and not orgbatch_data:
        usermessage = usermessages.api_org_nullbatches(apikey, orgid)
        print(usermessage)

    # test for failed API call (and attempt to print API error message)
    elif not apicall_success:
        usermessage = usermessages.api_error_status(apikey, orgid, orgbatch_data)
        print(usermessage)
    
    # success
    else:
        print(json.dumps(orgbatch_data, indent=4)) if prettyprint else print(orgbatch_data)

def getactionbatch(cmd_args):
    apikey = cmd_args['apikey'].replace('\n', '').replace(' ', '')
    orgid = cmd_args['orgid'].replace('\n', '').replace(' ', '')
    batchid = cmd_args['batchid'].replace('\n', '').replace(' ', '')
    prettyprint = cmd_args['prettyprint']

    # make API call
    apicall_success, batch_data = actionbatchrequests.get_action_batch(apikey, orgid, batchid)

    # test for bad API call and a space returned as the data
    if not apicall_success and batch_data == ' ':
        usermessage = usermessages.api_error_nostatus(apikey, orgid, batchid)
        print(usermessage)

    # test for failed API call (and attempt to print API error message)
    elif not apicall_success:
        usermessage = usermessages.api_error_status(apikey, orgid, batch_data, batchid)
        print(usermessage)

    else:
        print(json.dumps(batch_data, indent=4)) if prettyprint else print(batch_data)

def batchstatus(cmd_args):
    apikey = cmd_args['apikey'].replace('\n', '').replace(' ', '')
    orgid = cmd_args['orgid'].replace('\n', '').replace(' ', '')
    batchstatus = cmd_args['batchstatus']
    prettyprint = cmd_args['prettyprint']
    
    # make our API call
    apicall_success, batchstatus_data = actionbatchrequests.get_org_action_batches(apikey, orgid)
    
    # test for bad API call and a space returned as the data
    if not apicall_success and batchstatus_data == ' ':
        usermessage = usermessages.api_error_nostatus(apikey, orgid)
        print(usermessage)

    # test for successful API call but no Action Batches returned for org given
    elif apicall_success and not batchstatus_data:
        usermessage = usermessages.api_org_nullbatches(apikey, orgid)
        print(usermessage)

    # test for failed API call (and attempt to print API error message)
    elif not apicall_success:
        usermessage = usermessages.api_error_status(apikey, orgid)
        print(usermessage)
    
    else:
        if prettyprint:
            print(json.dumps(batchstatus_data, indent=4))
        else:
            pass

        # call compare_batches function and assign 4 vars based upon return
        condition1, condition2, compare1, compare2 = compare_batches(batchstatus, batchstatus_data)
        print('\n')
        print(stylize(f'Summary: This org has {len(compare1)} {condition1} Action Batches and {len(compare2)} {condition2} Action Batches\n', usermessages.info_formatting))
        print(stylize('Use PrettyPrint option to show matching Action Batches with detail.', usermessages.info_formatting))

def deleteactionbatches(cmd_args):
    apikey = cmd_args['apikey'].replace('\n', '').replace(' ', '')
    orgid = cmd_args['orgid'].replace('\n', '').replace(' ', '')
    all_batchid = cmd_args['batchid'].replace('\n', '').replace(' ', '')
    batchids = []
    batchids = str.split(cmd_args['batchid'], ',')
    
    for batchid in batchids:
        apicall_success, delbatches_data = actionbatchrequests.delete_action_batch(apikey, orgid, batchid)
        print(
        stylize('\n_______________________________________________________\n', usermessages.bold_formatting, usermessages.reset_formatting) +

        stylize('\nAttempting to delete BatchID: ', usermessages.info_formatting, usermessages.reset_formatting) +
        stylize((batchid), usermessages.info_formatting, usermessages.reset_formatting) + '\n'
        )

        # test for bad API call and a space returned as the data
        if not apicall_success and delbatches_data == ' ':
            usermessage = usermessages.api_error_nostatus(apikey, orgid, batchid=batchid)
            print(usermessage)

        # deletebatch API call returns no data (null) when successful
        elif apicall_success and delbatches_data == '':
            usermessage = usermessages.api_delsuccess(apikey, orgid, batchid=batchid)
            print(usermessage)

        # test for failed API call (and attempt to print API error message)
        elif not apicall_success:
            usermessage = usermessages.api_error_status(apikey, orgid, delbatches_data, batchid=batchid)
            print(usermessage)

        else:
            print(delbatches_data)

def checkuntilcomplete(cmd_args):
    apikey = cmd_args['apikey'].replace('\n', '').replace(' ', '')
    orgid = cmd_args['orgid'].replace('\n', '').replace(' ', '')
    batchid = cmd_args['batchid'].replace('\n', '').replace(' ', '')
    maxtries = cmd_args['maxtries']
    apicount=1

    # keep trying for maxtries defined by user
    # 1 = successful action batch, -1 = failed with errors, -2 = not confirmed yet,
    # -3 = hasn't been processed by actionbatch API yet (confirmed but pending)
    for i in range(maxtries):
        # call our helper function to check the status of the action batch and return int based on status
        status = checkstatus(apikey, orgid, batchid)        
        if status == 1:
            break
        elif status == -1:
            break
        elif status == -2:
            break
        elif status == -3:
            print(f'Action batch {batchid} is still processing. API call count: {apicount}')
        
        os.sys.stdout.flush()
        time.sleep(1)
        apicount += 1
######### END API CALL FUNCTIONS ##########


######### BEGIN MAIN GUI AND GOOEY PARSERS ##########
def main():
    parser = GooeyParser(description='Simple Tool To Create, Delete, and Check Meraki Action Batches')
    subs = parser.add_subparsers(help='commands', dest='command')

##### Create Action Batch Parser #####
    createbatch_parser = subs.add_parser(
        'CreateActionBatch',
        help='Given API key, OrgID, and JSON Payload File(s), creates a new action batch'
    )

    createbatch_parser.add_argument( 
        metavar='API Key',
        help='Your Meraki API Key', 
        action='store',
        type=str,
        dest='apikey',
        default=deep_get(load_defaults(), 'common.apikey')
    )

    createbatch_parser.add_argument(
        metavar='Org ID',
        help='OrgID for Action Batch', 
        action='store',
        type=str,
        dest='orgid',
        default=deep_get(load_defaults(), 'common.orgid')
    )
    
    createbatch_parser.add_argument(
        metavar='JSON Action(s)',
        help='JSON file(s) containing actions to perform in new action batch.  Multiple files will be combined into one action Batch. ' +
        'See Meraki Action Batch documentation and help file for this app on how to construct JSON (both in Help Menu)',
        dest='jsonfiles',
        widget='MultiFileChooser',
        gooey_options={
                        'wildcard':
                            'JSON (*.json)|*.JSON|'
                            "All files (*.*)|*.*",
                            'message': "pick folder"
                        },
        default=deep_get(load_defaults(), 'other.createactionbatch.json_actionfile_path')
    )

    createbatch_parser.add_argument(
        '--Confirm', 
        metavar='Confirm Action Batch',
        help='Confirm the existing action batch. ' + 
        'Batches are not executed until confirmed is set. Once a batch is confirmed it cannot be deleted. ' +
        'Defined but unconfirmed batches will be automatically deleted after 1 week.',
        action='store_true',
        dest='confirmed',
        #default=deep_get(load_defaults(), 'other.updateactionbatch.confirm')
    )
    
    createbatch_parser.add_argument(
        '--Synchronous',
        metavar='Synchronous',
        help='Run the actions in the existing batch in synchronous mode instead of Asynchronous default. ' +
        'There can be at most 20 actions in synchronous batch.',
        action='store_true',
        dest='synchronous',
        #default=deep_get(load_defaults(), 'other.updateactionbatch.synchronous')
    )

    createbatch_parser.add_argument(
        '--prettyprint',
        metavar='Indent (pretty print) JSON output',
        help='Pretty print JSON output to screen',
        action='store_true',
        dest='prettyprint',
        #default=deep_get(load_defaults(), 'common.prettyprint')
    )

    createbatch_parser.add_argument(
        '--ExportFile',
        metavar='Export File',
        help='File to export full JSON sent to Meraki Dashboard.  Multiple payload files will be combined into one file',
        widget='FileSaver',
        dest='exportfile',
        default=deep_get(load_defaults(), 'other.createactionbatch.exportfile_path')
    )

##### Update Action Batch Parser #####

    updatebatch_parser = subs.add_parser(
        'UpdateActionBatch',
        help='Given API key, OrgID, and BatchID, updates a given action batch'
    )

    updatebatch_parser.add_argument( 
        metavar='API Key',
        help='Your Meraki API Key', 
        action='store',
        type=str,
        dest='apikey',
        default=deep_get(load_defaults(), 'common.apikey')
    )

    updatebatch_parser.add_argument(
        metavar='Org ID',
        help='OrgID for Action Batch ', 
        action='store',
        type=str,
        dest='orgid',
        default=deep_get(load_defaults(), 'common.orgid')
    )
    
    updatebatch_parser.add_argument( 
        metavar='Batch ID',
        help='Individual Batch ID to update', 
        type=str,
        action='store',
        dest='batchid',
        default=deep_get(load_defaults(), 'common.batchid')
    )

    updatebatch_parser.add_argument(
        '--Confirm', 
        metavar='Confirm Action Batch',
        help='Confirm the existing action batch. ' + 
        'Batches are not executed until confirmed is set. Once a batch is confirmed it cannot be deleted. ' +
        'Defined but unconfirmed batches will be automatically deleted after 1 week.',
        action='store_true',
        dest='confirmed',
        #default=deep_get(load_defaults(), 'other.updateactionbatch.confirm')
    )
    
    updatebatch_parser.add_argument(
        '--Synchronous',
        metavar='Synchronous',
        help='Run the actions in the existing batch in synchronous mode instead of Asynchronous default. ' +
        'There can be at most 20 actions in synchronous batch.',
        action='store_true',
        dest='synchronous',
        #default=deep_get(load_defaults(), 'other.updateactionbatch.synchronous')
    )

    updatebatch_parser.add_argument(
        '--prettyprint',
        metavar='Indent (pretty print) JSON output',
        help='Pretty print JSON output to screen',
        action='store_true',
        dest='prettyprint',
        #default=deep_get(load_defaults(), 'common.prettyprint')
    )

##### Get Org Action Batch Parser #####

    getorgbatch_parser = subs.add_parser(
        'GetOrgActionBatch',
        help='Given API key and OrgID, returns all Action Batches for that Org'
    )

    getorgbatch_parser.add_argument(
        metavar='API Key',
        help='Your Meraki API Key', 
        action='store',
        type=str,
        dest='apikey',
        default=deep_get(load_defaults(), 'common.apikey')
    )
    
    getorgbatch_parser.add_argument( 
        metavar='Org ID',
        help='OrgID for Action Batch', 
        action='store',
        type=str,
        dest='orgid',
        default=deep_get(load_defaults(), 'common.orgid')
    )

    getorgbatch_parser.add_argument(
        '--prettyprint',
        metavar='Indent (pretty print) JSON output',
        help='Pretty print JSON output to screen',
        action='store_true',
        dest='prettyprint',
        #default=deep_get(load_defaults(), 'common.prettyprint')
    )

##### Get Action Batch Parser #####

    getbatch_parser = subs.add_parser(
        'GetActionBatch',
        help='Given API key and ActionBatchID, returns individual action batch information'
    )

    getbatch_parser.add_argument( 
        metavar='API Key',
        help='Your Meraki API Key', 
        action='store',
        type=str,
        dest='apikey',
        default=deep_get(load_defaults(), 'common.apikey')
    )

    getbatch_parser.add_argument( 
        metavar='Org ID',
        help='OrgID for Action Batch', 
        action='store',
        type=str,
        dest='orgid',
        default=deep_get(load_defaults(), 'common.orgid')
    )

    getbatch_parser.add_argument( 
        metavar='Batch ID',
        help='Individual Batch ID to check status', 
        action='store',
        type=str,
        dest='batchid',
        default=deep_get(load_defaults(), 'common.batchid')
    )

    getbatch_parser.add_argument(
        '--prettyprint',
        metavar='Indent (pretty print) JSON output',
        help='Pretty print JSON output to screen',
        action='store_true',
        dest='prettyprint',
        #default=deep_get(load_defaults(), 'common.prettyprint')
    )

##### Batch By Status Action Batch Parser #####

    batchstatus_parser = subs.add_parser(
        'ActionBatchStatus',
        help='Given API key and OrgID, returns action batches by status (errors, confirmed, etc).  Action batches are not committed until confirmed'
    )

    batchstatus_parser.add_argument( 
        metavar='API Key',
        help='Your Meraki API Key', 
        action='store',
        type=str,
        dest='apikey',
        default=deep_get(load_defaults(), 'common.apikey')
    )

    batchstatus_parser.add_argument( 
        metavar='Org ID',
        help='OrgID for Action Batch ', 
        action='store',
        type=str,
        dest='orgid',
        default=deep_get(load_defaults(), 'common.orgid')
    )

    batchstatus_parser.add_argument(
        metavar='Action Batch Status Condition to Check',
        help='Action Batch Status Condition to Check',
        dest='batchstatus',
        widget='Dropdown',
        choices=['Confirmed/UnConfirmed Action Batches', 'Completed/Incomplete Action Batches', 'Failed Action Batches']
    )

    batchstatus_parser.add_argument(
        '--prettyprint',
        metavar='Indent (pretty print) JSON output',
        help='Pretty print JSON output to screen',
        action='store_true',
        dest='prettyprint',
        #default=deep_get(load_defaults(), 'common.prettyprint')
    )

##### Delete Action Batches Parser #####

    deletebatches_parser = subs.add_parser(
        'DeleteActionBatches',
        help='Given API key, OrgID, and BatchID, deletes one or more action batches'
    )

    deletebatches_parser.add_argument( 
        metavar='API Key',
        help='Your Meraki API Key', 
        action='store',
        type=str,
        dest='apikey',
        default=deep_get(load_defaults(), 'common.apikey')
    )

    deletebatches_parser.add_argument( 
        metavar='Org ID',
        help='OrgID for Action Batch ', 
        action='store',
        type=str,
        dest='orgid',
        default=deep_get(load_defaults(), 'common.orgid')
    )

    deletebatches_parser.add_argument( 
        metavar='Batch IDs',
        help='One or more Batch IDs to delete seperated by commas',
        action='store',
        type=str,
        dest='batchid'
    )

##### Check Until Action Batch Is Completed Parser #####

    checkuntilcomplete_parser = subs.add_parser(
        'CheckUntilComplete',
        help='Given API key, OrgID, and BatchID, updates a given action batch'
    )

    checkuntilcomplete_parser.add_argument( 
        metavar='API Key',
        help='Your Meraki API Key', 
        action='store',
        type=str,
        dest='apikey',
        default=deep_get(load_defaults(), 'common.apikey')
    )

    checkuntilcomplete_parser.add_argument( 
        metavar='Org ID',
        help='OrgID for Action Batch', 
        action='store',
        type=str,
        dest='orgid',
        default=deep_get(load_defaults(), 'common.orgid')
    )

    checkuntilcomplete_parser.add_argument( 
        metavar='Batch ID',
        help='Individual Batch ID Monitor', 
        action='store',
        type=str,   
        dest='batchid',
        default=deep_get(load_defaults(), 'common.batchid')
    )
    
    checkuntilcomplete_parser.add_argument( 
        '--maxtries',
        metavar='Maximum Number of Tries (API Calls)',
        help='Maximum number of tries to call API before stopping. (Default is 10)',
        action='store',
        type=int,   
        dest='maxtries',
        default=10,
        gooey_options={
            'validator': {
                'test': '0 < int(user_input)',
                'message': 'Must be greater than 0'
            }
        }
    )
    ########## END PARSER DEFINITIONS ##########


    ########## BEGIN CMD PARSER FUNCTION CALLS ##########

    cmd_args = vars(parser.parse_args())
    # Call function based upon user cmd used in GUI
    if debug:
        print(cmd_args)
    elif cmd_args['command'] == 'CreateActionBatch':
        createactionbatch(cmd_args)
    elif cmd_args['command'] == 'UpdateActionBatch':
        updateactionbatch(cmd_args)
    elif cmd_args['command'] == 'GetOrgActionBatch':
        getorgactionbatch(cmd_args)
    elif cmd_args['command'] == 'GetActionBatch':
        getactionbatch(cmd_args)
    elif cmd_args['command'] == 'ActionBatchStatus':
        batchstatus(cmd_args)
    elif cmd_args['command'] == 'DeleteActionBatches':
        deleteactionbatches(cmd_args)
    elif cmd_args['command'] == 'CheckUntilComplete':
        checkuntilcomplete(cmd_args)
    else:
        print(f'Error:  No command received.  Arguments passed:\n {cmd_args}')
    ########## END MAIN() ##########

if __name__ == '__main__':
    main()