# Meraki ActionBatcher
-----------------  

- [Introduction](#Introduction)
- [About Meraki Action Batches](#Meraki-Action-Batches)
- [Installation](#Installation)
    - [Requirements](#Requirements)
    - [Installing to a Python Virtual Environment](#Installing-to-a-Python-Virtual-Environment)
    - [Compiling to an Executable](#Compiling-to-an-Executable)
- [Use](#Use)
    - [Warning!](#Warning!)
    - [Action Batcher Operations Overview](#action-batcher-operations-overview)
        - [Action Batcher Operations: Create Action Batch](#action-batcher-operations:-create-action-batch)
        - [Action Batcher Operations: Update Action Batch](#Action-Batcher-Operations:-Update-Action-Batch)
        - [Action Batcher Operations: GetOrg Action Batch](#Action-Batcher-Operations:-GetOrg-Action-Batch)
        - [Action Batcher Operations: Get Action Batch](#Action-Batcher-Operations:-Get-Action-Batch)
        - [Action Batcher Operations: Action Batch Status](#Action-Batcher-Operations:-Action-Batch-Status)
        - [Action Batcher Operations: Delete Action Batches](#Action-Batcher-Operations:-Delete-Action-Batches)
        - [Action Batcher Operations: Check Until Complete](#Action-Batcher-Operations:-Check-Until-Complete)
- [Creating Actions](Creating-Actions)
    - Creating Actions using JSON
    - Using Action Tools to Create Actions (for Action Batches)
- [Using Default Config File](Using-Default-Config-File)
- Changelog
- License
- Contributing


![Action Batcher](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/CreateActionBatchSmall.png)

# Introduction

Meraki Action Batcher is a Python-based GUI tool for creating, updating, verifying, deleting, and monitoring Meraki Action Batches.  Action Batcher simplifies interaction with the Meraki Action Batch API so that you can focus on individual actions.  This project is part of the [Meraki ActionBatch Tools](https://github.com/zabrewer/Meraki-ActionBatch-Tools) parent repo and can be used with the [Meraki Action Composer](https://github.com/zabrewer/Meraki-ActionComposer/) complimentary tool.

# Meraki Action Batches

In June 2019, Meraki announced Action Batches as a new way for making changes in bulk via the Meraki Dashboard API.  The obvious benefit of Action Batches is a way to navigate the Dashboard API rate limit of 5 calls per second (per individual Dashboard Org).  Depending on the requirements, authors of a given script or app sometimes had to navigate API with respective code (e.g. exponential backoff). 

With Action Batches we now have a way to scale changes to many devices (and/or networks) with fewer API caveats.  

![Action Batches](https://meraki.cisco.com/blog/wp-content/uploads/Action-BAtches-image.jpg)

From the Action Batch documentation:

* Action batches allow an API client to define a batch of write actions (**create, update, destroy,** etc.).
* Batches are run **atomically** (all or nothing, no partial success).
* Batches are run **asynchronously** by default. Smaller batches can be run **synchronously**.
* You can run up to **20 resources synchronously** in a single batch.
* A batch can consists of **up to 100 resources**.
* Limit of **5 concurrent running batches** at a time.
* A batch **should be completed within 10 minutes from confirmation**.
* Different types of resources and operations can be combined in a batch.
* The actions in a batch will be executed in the same order they are defined.
* ***Batches will not be executed until the confirmed property is set. Once a batch is confirmed it cannot be deleted. If a batch is defined but not confirmed it will be automatically deleted after one week.***

Please review the [Action Batch API documentation](https://developer.cisco.com/meraki/api/#/rest/guides/action-batches) to understand Action Batches.

[Back To Index](#Meraki-ActionBatcher)



# Installation

## Requirements

Meraki ActionBatcher requires Python 3.5 or greater.  In addition to modules distributed with ActionBatcher, ActionBatcher depends on the [Gooey](https://pypi.org/project/Gooey/) and [JSONMerge](https://pypi.org/project/jsonmerge/) external packages.  Both can be installed via the included requirements.txt file

## Installing to a Python Virtual Environment

Note: For Mac OSX, replace "python" with "python3" and for both platforms, make sure the output of python -v (or python3 -v) is 3.5 or greater.

**1. Clone this repository locally**
```
git clone https://github.com/zabrewer/Meraki-ActionBatcher.git
```
**2. Create the virtual environment**
```
python3 -m venv Meraki-ActionBatcher
```

**3. Change to the Meraki-ActionBatcher directory**
```
cd Meraki-ActionBatcher
```

**4. Activate the virtual environment**

For Windows
```
Scripts\activate.bat
```

For Mac
```
source bin/activate
```

**5. Satisfy dependencies by installing external packages**
```
pip install -r requirements.txt
```

**6. Launch ActionBatcher while in virtual environment**
```
python actionbatcher.py
```

To exit, close the ActionBatcher GUI window or cntrl+C at the command prompt.  To deactivate the virtual environment:

For Windows
```
Scripts\deactivate.bat
```

For Mac
```
deactivate
```
[Back To Index](#Meraki-ActionBatcher)


## Compiling to an Executable
(Coming Soon)

[Back To Index](#Meraki-ActionBatcher)


# Use

## Warning!
After an Action Batch has been confirmed, it ***CANNOT BE DELETED***.  

This tool can make mass changes to a production environment.  Please make sure you understand the Meraki Dashboard and Meraki Action Batch APIs well before using this application.  The license file provided with this software absolves all parties of issues, accidental or otherwise.

*If you want to test most functions (except for create and update), you can do so in the Meraki developer sandbox which is Read-Only.*

1) Sign up for a [Cisco DevNet Account](https://developer.cisco.com)
2) [Login through this link](https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology)
3) Scroll to the bottom left for the Read-Only Dashboard API key.

[Back To Index](#Meraki-ActionBatcher)

## Prerequisites

Before working with action batches, you must have an API Key and know the OrgID.  

* [Documentation for enabling the API key for an account](  https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API)
* The OrgID(s), NetworkIDs, and other relative information can be retrieved using Python, cURL, the [Meraki Dashboard Postman Collection](http://postman.meraki.com/), and many other ways
* [Cisco Devnet](https://developer.cisco.com/meraki/) is a good place to start if you are new to the Meraki Dashboard API.

[Back To Index](#Meraki-ActionBatcher)

## Action Batcher Operations Overview

Most of the Action Batcher operations mirror the Action Batch API.  

| Operation    | Description    | Screenshot |
|:----------------------|-----------|------|
| [Create Action Batch](#Action-Batcher-Operations:-Create-Action-Batch)  |  Creates a new Action Batch for the given org |  ![Create Action Batch](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/CreateActionBatch.png)|
| [Update Action Batch](#Action-Batcher-Operations:-Update-Action-Batch)   | Updates an existing Action Batch |  ![Action Batcher](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/UpdateActionBatch.png)|
| [GetOrg Action Batch](#Action-Batcher-Operations:-GetOrg-Action-Batch)| Get all Action Batches for a given Org | ![Action Batcher](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/GetOrgActionBatch.png)|
| [Get Action Batch](#Action-Batcher-Operations:-Get-Action-Batch)  | Get the details of a single action batch |  ![Action Batcher](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/GetActionBatch.png)   |
| [Action Batch Status](#Action-Batcher-Operations:-Action-Batch-Status)  | Get Action Batches that match a given criteria (Confirmed/Unconfirmed, Complete/Incomplete, Failed) |  ![Action Batcher](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/ActionBatchStatus.png)  | 
| [Delete Action Batches](#Action-Batcher-Operations:-Delete-Action-Batches) | Deletes an Action Batch (Unconfirmed status only) | ![Action Batcher](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/DeleteActionBatches.png) | 
| [Check Until Complete](#Action-Batcher-Operations:-Check-Until-Complete) | Keep checking a given Action Batch until it is complete | ![Action Batcher](https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/CheckUntilComplete.png) |

[Back To Index](#Meraki-ActionBatcher)


## Action Batcher Operations: Create Action Batch

Creates a new Action Batch for the given org

* **Required Arguments** 
    * *API Key*:  Your Meraki API Key
    * *Org ID*:  The Org ID in which you wish to create the new Action Batch
    * *JSON Action(s)*:  One or more JSON actions to submit to the ActionBatch API
        - One or MORE JSON files can be selected using CNTRL+Click (CMD+Click on Mac OSX)
        - All files are checked for valid JSON - if the JSON is invalid, ActionBatcher notes which files are invalid and tells the user
        - If all files are valid, they will be merged **in the order that they are clicked**.  Order of operation is important often when committing multiple actions to an Action Batch via the API (i.e. you can't update a switchport on an unclaimed switch)
        - See (Creating Action Batch JSON)[#Creating-Action-Batch-JSON] for information on how ActionBatcher expects the JSON to be formatted
* **Optional Arguments**
    * *Confirm Action Batch*:  Whether or not to confirm the Action Batch when it is first submitted
        - Action Batches are not executed until they are marked as confirmed
        - It is possible to use the UpdateActionBatch operation (outlined in the next section) to confirm an Action Batch
        - **Once confirmed Action Batch cannot be deleted!** 
        - *As Per Meraki Documentation*, Action Batches that have been submitted but not confirmed will be deleted by the API after **one week**
    * *Synchronous*:  Whether or not the Action Batch will be executed Synchronously or Asynchronously
        - Note that this setting can be updated/changed per Action Batch *until* the Action Batch has been confirmed
        - Only 20 resources (individual actions) can be run synchronously in a single batch
    * *Indent JSON Output*:  Whether or not to indent the JSON output to screen
    * *Export File*:  If defined, all actions are combined and written to this file.  Basically this is a dump of exactly what is sent to the Action Batch API


[Back To Index](#Meraki-ActionBatcher) | [Back To Operations Overview](#action-batcher-operations-overview)


## Action Batcher Operations: Update Action Batch

Updates an existing Action Batch

* **Required Arguments** 
    * *API Key*:  Your Meraki API Key
    * *Org ID*:  The Org ID for the Action Batch to be updated
    * *Batch ID*:  The Batch ID for the Action Batch to be updated (can get from GetOrgActionBatch operation or ActionBatchStatus)
* **Optional Arguments**
    * *Confirm Action Batch*:  Whether or not to confirm the Action Batch when it is as part of the update
    * *Synchronous*:  Whether or not the Action Batch will be executed Synchronously or Asynchronously
        - Note that this setting can be updated/changed per Action Batch *until* the Action Batch has been confirmed
        - Only 20 resources (individual actions) can be run synchronously in a single batch
    * *Indent JSON Output*:  Whether or not to indent the JSON output to screen

[Back To Index](#Meraki-ActionBatcher) | [Back To Operations Overview](#action-batcher-operations-overview)


## Action Batcher Operations: GetOrg Action Batch

JSON output for all Action Batches for a given Dashboard Organization (Org ID)

* **Required Arguments** 
    * *API Key*:  Your Meraki API Key
    * *Org ID*:  The Org ID
* **Optional Arguments**
    * *Indent JSON Output*:  Whether or not to indent the JSON output to screen

[Back To Index](#Meraki-ActionBatcher) | [Back To Operations Overview](#action-batcher-operations-overview)



## Action Batcher Operations: Get Action Batch

Detailed JSON output for an individual Action Batch

* **Required Arguments** 
    * *API Key*:  Your Meraki API Key
    * *Org ID*:  The Org ID
    * *Batch ID*:  The *Batch ID* to to retrieve (can get from GetOrgActionBatch operation or ActionBatchStatus)
* **Optional Arguments**
    * *Indent JSON Output*:  Whether or not to indent the JSON output to screen

[Back To Index](#Meraki-ActionBatcher) | [Back To Operations Overview](#action-batcher-operations-overview)



## Action Batcher Operations: Action Batch Status

Print a list of BatchIDs that match a given condition.

* **Required Arguments** 
    * *API Key*:  Your Meraki API Key
    * *Org ID*:  The Org ID
    * *Action Batch Status Condition to Check:*  Retrieve Action Batches that match one of the following:
        - Confirmed/Unconfirmed Action Batches
        - Completed/Incomplete Action Batches
        - Failed Action Batches
* **Optional Arguments**
    * *Indent JSON Output*:  Whether or not to indent the JSON output to screen

[Back To Index](#Meraki-ActionBatcher) | [Back To Operations Overview](#action-batcher-operations-overview)



## Action Batcher Operations: Delete Action Batches

Delete an **unconfirmed** Action Batch

* **Required Arguments** 
    * *API Key*:  Your Meraki API Key
    * *Org ID*:  The Org ID
    * *Batch ID*:  The *Batch ID* delete

[Back To Index](#Meraki-ActionBatcher) | [Back To Operations Overview](#action-batcher-operations-overview)



## Action Batcher Operations: Check Until Complete

Check a **confirmed** Action Batch until it is complete

* **Required Arguments** 
    * *API Key*:  Your Meraki API Key
    * *Org ID*:  The Org ID
    * *Batch ID*:  The *Batch ID* to check status
* **Optional Arguments**
    * *Maximum Number of Tries*: The maximum # of API calls to make before stopping
        - Default is 10 API Calls

[Back To Index](#Meraki-ActionBatcher) | [Back To Operations Overview](#action-batcher-operations-overview)



## Creating Actions


[Back To Index](#Meraki-ActionBatcher)

## Using Default Config File


[Back To Index](#Meraki-ActionBatcher)

* License

[Back To Index](#Meraki-ActionBatcher)

* Contributing

[Back To Index](#Meraki-ActionBatcher)
* Changelog

[Back To Index](#Meraki-ActionBatcher)
