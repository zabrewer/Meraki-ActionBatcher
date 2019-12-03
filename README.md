# Meraki ActionBatcher
-----------------  

- [Introduction](#Introduction)
- [About Meraki Action Batches](#Meraki-Action-Batches)
- [Installation](#Installation)
    - [Compiling To Executable](#Compiling-to-Executable)
- [Use](#Use)
    - [Warning!](#Warning!)
    - [Action Batcher Operations Overview](#Action-Batcher-Operations-Overview)
        - [Action Batcher Operations - Create Action Batch](Action-Batcher-Operations-Create-Action-Batch)
        - [Action Batcher Operations - Update Action Batch](Action-Batcher-Operations-Update-Action-Batch)
    - [Creating Actions](Creating-Actions)
        - Creating Actions using JSON
        - Using Action Tools to Create Actions (for Action Batches)

<img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/CreateActionBatch.png" align="center" height="250" width="450"/>

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

# Installation

## Requirements

Meraki ActionBatcher should work on Python 3.5 or greater.  In addition to modules distributed with ActionBatcher, ActionBatcher depends on the [Gooey](https://pypi.org/project/Gooey/) and [JSONMerge](https://pypi.org/project/jsonmerge/) external packages.  Both can be installed via the included requirements.txt file

## Install using a virtual environment

Note: For mac, replace "python" with "python3" and for both platforms, make sure the output of python -v is 3.5 or greater.

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

## Compiling to an Executable
(Coming Soon)

# Use

## Warning!
After an Action Batch has been confirmed, it ***CANNOT BE DELETED***.  

This tool can make mass changes to a production environment.  Please make sure you understand the Meraki Dashboard and Meraki Action Batch APIs well before using this application.  The license file provided with this software absolves all parties of issues, accidental or otherwise.

*If you want to test most functions (except for create and update), you can do so in the Meraki developer sandbox which is Read-Only.*

1) Sign up for a [Cisco DevNet Account](https://developer.cisco.com)
2) [Login through this link](https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology)
3) Scroll to the bottom left for the Read-Only Dashboard API key.

## Prerequisites

Before working with action batches, you must have an API Key and know the OrgID.  

* [Documentation for enabling the API key for an account](  https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API)
* The OrgID(s), NetworkIDs, and other relative information can be retrieved using Python, cURL, the [Meraki Dashboard Postman Collection](http://postman.meraki.com/), and many other ways
* [Cisco Devnet](https://developer.cisco.com/meraki/) is a good place to start if you are new to the Meraki Dashboard API.

## Action Batcher Operations Overview

Most of the Action Batcher operations mirror the Action Batch API.  

| Operation    | Description    | Screenshot |
|:----------------------|-----------|------|
| Create Action Batch  |  Creates a new Action Batch for the given org |  <img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/CreateActionBatch.png"/>|
| Update Action Batch   | Updates an existing Action Batch |  <img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/UpdateActionBatch.png"/>|
| GetOrg Action Batch | Get all Action Batches for a given Org | <img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/GetOrgActionBatch.png"/>|
| Get Action Batch  | Get the details of a single action batch |  <img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/GetActionBatch.png"/>   |
| Action Batch Status  | Get Action Batches that match a given criteria (Confirmed/Unconfirmed, Complete/Incomplete, Failed) |  <img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/ActionBatchStatus.png"/>  | 
| Delete Action Batches | Deletes an Action Batch (Unconfirmed status only) | <img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/DeleteActionBatches.png"/> | 
| Check Until Complete | Keep checking a given Action Batch until it is complete | <img src="https://github.com/zabrewer/Meraki-ActionBatcher/blob/master/assets/CheckUntilComplete.png"/> |

## Action Batcher Operations - Create Action Batch

* **Create An Action Batch** - Creates a new Action Batch for the given org
    * 

## Config File

* Use

* License

* Contributing

* Changelog


    * about Meraki Action Batched
    * about this Tool

* Installation
    * dependeinces
* Use
    * config file
    * payloads

* Example use cases
    * 

License