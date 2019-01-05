const request = require('sync-request');
const AWSXRay = require('aws-xray-sdk-core');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));
AWS.config.update({region: process.env.AWS_REGION});
var ssm = new AWS.SSM();

const api_base = "https://api2.cloudcheckr.com/";
var cc_admin_access_key = '';

function processEvent(event, context, callback) {
    
    var masterPayerArr;
    try {
        var params = {
            Names: [
                'html_encoded_semicolon_separated_master_payers'
            ]
        };
        
        ssm.getParameters(params, function(err, data) {
            if (err) {
                console.log(err, err.stack); // an error occurred
                callback(err);
            } else if (data['Parameters'] == undefined) {
                callback("SSM was able to reach parameter store, but no parameter was found for the payer accounts.");
            } else {
                masterPayerArr = data['Parameters'][0]['Value'].split(',');

                var account_list;
                console.log(masterPayerArr);
                
                for (var masterPayerNum in masterPayerArr) {
                    var masterPayer = masterPayerArr[masterPayerNum];

                    var options = {
                        host: api_base,
                        path: 'api/billing.json/get_account_family?access_key=' + cc_admin_access_key + '&use_account=' + masterPayer
                    };

                    console.log('Getting the list of account families for ' + masterPayer + '...');
                    var response = request('GET', options['host'] + options['path']);
                    var response_array;

                    if (response.statusCode == 200) {
                        //console.log(response.body); // Show the response
                        response_array = JSON.parse(response.body);
                        //console.log(response_array);
                        if (response_array['UnmappedAccounts'].length === 0) {
                            console.log('No unmapped accounts found in ' + masterPayer + '.');
                            //callback(null, false); /* Indicates success with information returned to the caller. */
                        } else {
                            console.log('Unmapped accounts found in ' + masterPayer + '.');
                            
                            response_array['UnmappedAccounts'].forEach(function(entry) {
                                if (account_list == undefined) {
                                    account_list = entry;
                                } else {
                                    account_list += '\n' + entry;
                                }
                            });
                        }
                    } else {
                        console.log('Error: ' + response.statusCode + ' ' + response.body + '. Exiting...');
                        context.fail('Could not retrieve data from CloudCheckr');
                    }
                }
                            
                if (account_list != undefined && (event.notificationsBool === "true" || event.notificationsBool == undefined)) {
                    var ses = new AWS.SES();
                    
                    var params = {
                        Destination: {
                            BccAddresses: [], 
                            CcAddresses: [], 
                            ToAddresses: [
                                "something"
                            ]
                        }, 
                        Message: {
                            Body: {
                                Html: {
                                    Charset: "UTF-8", 
                                    Data: "Hello,<p>Some accounts were found in CloudCheckr which are not mapped to an Account Family. " 
                                    + "Mapping accounts to an account family is necessary for invoicing. These are the unmapped accounts:</p>"
                                    + "<p>" + account_list.replace(/\n/i, '<br />') + "</p>"
                                }, 
                                Text: {
                                    Charset: "UTF-8", 
                                    Data: "Hello,\n\nSome accounts were found in CloudCheckr which are not mapped to an Account Family. " 
                                    + "Mapping accounts to an account family is necessary for invoicing. These are the unmapped accounts:"
                                    + "\n\n" + account_list
                                }
                            }, 
                            Subject: {
                                Charset: "UTF-8", 
                                Data: "Unmapped CloudCheckr Accounts Found"
                            }
                        },
                        Source: "awsresell@jhctechnology.com"
                    };
                    ses.sendEmail(params, function(err, data) {
                        if (err) console.log(err, err.stack); // an error occurred
                        else     console.log(data);           // successful response
                    });
                }
            }
        });  
    } catch (e) {
        console.log(e);
        callback(1);
    }
}

exports.handler = (event, context, callback) => {
    "use strict";

    var params = {
        Names: [
            'cc_admin_access_key'
        ],
        WithDecryption: true
    };

    ssm.getParameters(params, function(err, data) {
        if (err) {
            console.log(err, err.stack); // an error occurred
            callback(err);
        } else if (data['Parameters'] == undefined) {
            console.log(data);
            callback("SSM was able to reach parameter store, but no parameter was found for the access key.");
        } else {
            cc_admin_access_key = data['Parameters'][0]['Value'];
            processEvent(event, context, callback);
        }
    });
};
