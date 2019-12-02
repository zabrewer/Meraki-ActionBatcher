# used by actionbatch-util.py to re-use messages to the user (bad API call, etc)
# will probably merge to a class or single function
from colored import stylize, colored, fg, attr

# setup our user message output styles
error_formatting = fg('red_3a') + attr('bold')
warning_formatting = fg('dark_orange') + attr('bold')
ok_formatting = fg('green') + attr('bold')
info_formatting = fg('blue') + attr('bold')
bold_formatting = attr('bold')
reset_formatting = attr('reset')

# for general API errors (errors returned by Dashboard API)
def api_error_status(apikey, orgid, data, batchid):
    base_usermessage = (
        stylize('API call to Dashboard was not successful, attempting to print errors reported by Meraki Dashboard: ', bold_formatting, reset_formatting) +
        stylize((data), error_formatting) + '\n\n' +
        stylize('API Key Value: ', bold_formatting) +
        stylize((apikey), info_formatting) + '\n' +
        stylize('OrgID Value: ', bold_formatting) +
        stylize((orgid), info_formatting)
        )

    if batchid == None:
        usermesage = base_usermessage

    
    else:
        batchmessage = stylize('BatchID Value: ', bold_formatting) + stylize((batchid), info_formatting)
        usermessage = base_usermessage + '\n' + batchmessage
    
    return usermessage

# for failed dashboard API call and no data returned (or space returned)
# common for mistyped apikey/orgid
def api_error_nostatus(apikey, orgid, batchid=None):
    base_usermessage = (
        stylize('API call to Dashboard was not successful and no status was returned by the server', error_formatting) + '\n\n' +
        stylize('The most common cause of this error is a mistyped/copied API Key or Org ID.', bold_formatting) + '\n\n' +
        stylize('In the case of individual Batch IDs, it is also possible that the ActionBatch has been deleted, does not exist, or was mistyped', error_formatting) + '\n\n' +
        stylize('API Key Value: ', bold_formatting) + stylize((apikey), info_formatting) + '\n' +
        stylize('OrgID Value: ', bold_formatting) + stylize((orgid), info_formatting, reset_formatting)
        )

    if batchid == None:
        usermessage = base_usermessage
    
    else:
        batchmessage = stylize('BatchID Value: ', bold_formatting) + stylize((batchid), info_formatting)
        usermessage = base_usermessage + '\n' + batchmessage
    
    return usermessage

def api_org_nullbatches(apikey, orgid):
    usermessage = (
        'No action batches found for ' +
        stylize('Organization ID: ', bold_formatting) + 
        stylize((orgid), info_formatting) + '\n\n' + 
        'Maybe submit one or more in this app with ' + 
        stylize('CreateActionBatch', bold_formatting) + '?'
        )
    
    return usermessage

def api_delsuccess(apikey, orgid, batchid):
    usermessage = (
        stylize('API call to dashboard API was successful, ' +
        'and no data was returned', ok_formatting, reset_formatting) + '\n' +
        stylize('This is common for a successful delete action batch request.', ok_formatting, reset_formatting) + '\n\n' +
        stylize('To verify batch was deleted, run GetOrgActionbatches or GetActionBatch', ok_formatting, reset_formatting) + '\n\n' +

        stylize('API Key Value: ', bold_formatting, reset_formatting) +
        stylize((apikey), info_formatting, reset_formatting) + '\n' +
        stylize('OrgID Value: ', bold_formatting, reset_formatting) +
        stylize((orgid), info_formatting, reset_formatting) + '\n' +
        stylize('BatchID Value: ', bold_formatting, reset_formatting) +
        stylize((batchid), info_formatting, reset_formatting)
        )
    return usermessage

# Display list of invalid json files (and valid ones) to the user
# used by createactionbatch function
def invalid_json_usermessage(testvalid_json_filelist):
    print(stylize('The action was not completed because one or more of the payload files contained invalid JSON.', info_formatting))
    print(stylize('(Export files are ignored when there is invalid JSON)\n', info_formatting))
    for key, value in testvalid_json_filelist.items():
        if value == 'Invalid JSON':
            print(stylize('Invalid JSON File:', error_formatting))
            print(stylize(key, error_formatting))

        elif value == 'Valid JSON':
            print(stylize('Valid JSON File:', ok_formatting))
            print(stylize(key, ok_formatting))
        else:
            pass