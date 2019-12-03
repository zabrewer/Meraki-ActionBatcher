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
pip install -r requirements.txt

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
| Update Action Batch   |     CheckBox |  <img src="https://github.com/chriskiehl/GooeyImages/raw/images/readme-images/f538c850-07c5-11e5-8cbe-864badfa54a9.png"/>|
| GetOrg Action Batch |        CheckBox | <img src="https://github.com/chriskiehl/GooeyImages/raw/images/readme-images/f538c850-07c5-11e5-8cbe-864badfa54a9.png"/>|
| Get Action Batch  |      CheckBox|  <img src="https://github.com/chriskiehl/GooeyImages/raw/images/readme-images/f538c850-07c5-11e5-8cbe-864badfa54a9.png"/>   |
| Action Batch Status  |       TextCtrl |  <img src="https://github.com/chriskiehl/GooeyImages/raw/images/readme-images/f54e9f5e-07c5-11e5-86e5-82f011c538cf.png"/>  | 
| Delete Action Batches |              DropDown &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | <img src="https://github.com/chriskiehl/GooeyImages/raw/images/readme-images/f53ccbe4-07c5-11e5-80e5-510e2aa22922.png"/> | 
| Check Until Complete | RadioGroup | <img src="https://github.com/chriskiehl/GooeyImages/raw/images/readme-images/f553feb8-07c5-11e5-9d5b-eaa4772075a9.png"/>
|choice &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|        DropDown | <img src="https://github.com/chriskiehl/GooeyImages/raw/images/readme-images/f54e4da6-07c5-11e5-9e66-d8e6d7f18ac6.png"/> |


## Action Batcher Operations - Create Action Batch

* **Create An Action Batch** - Creates a new Action Batch for the given org
    * 


| Create Action Batch | Update Action Batch | Get Org Action Batch | Get Action Batch | Action Batch Status | Delete Action Batches | Check Until Complete |
|-------------|---------------|---------------|--------------|----------------|----------------|----------------|
| <img src="https://cloud.githubusercontent.com/assets/1408720/7950190/4414e54e-0965-11e5-964b-f717a7adaac6.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950189/4411b824-0965-11e5-905a-3a2b5df0efb3.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950192/44165442-0965-11e5-8edf-b8305353285f.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950188/4410dcce-0965-11e5-8243-c1d832c05887.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950191/4415432c-0965-11e5-9190-17f55460faf3.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950191/4415432c-0965-11e5-9190-17f55460faf3.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950191/4415432c-0965-11e5-9190-17f55460faf3.jpg"> | 

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