import pandas as pd
import boto3
from botocore.exceptions import ClientError
count = 0
sl = []
el = []


ch = input("Which format is your email list in? (enter the number)\n1. CSV\n2. Txt\n")

if ch == "1":
  filepath = input("enter your email adresses source file path\n")
  col = input("Which column is the are the emails located?\n")
  data = pd.read_csv(filepath)
  emails = data.iloc[:, (int(col)-1)].values
  lis = []
  RECIPIENT = []
  for x in emails:
    if len(lis) == 50:
        RECIPIENT.append(lis)
        lis = []
    lis.append(x)
  
  if len(lis) != 0:
    RECIPIENT.append(lis)
    lis = []

elif ch == "2":
    filepath = input("enter your email adresses source file path\n")
    with open(filepath, 'r') as fp:
        lis = []
        RECIPIENT = []
        for line in fp:
            if len(lis) == 50:
                RECIPIENT.append(lis)
                lis.clear()
            lis.append(line.strip('\n'))
        if len(lis) != 0:
            RECIPIENT.append(lis)
            lis.clear
          
else:
  print ("Invalid response.. try again later")
  exit()
# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
bodypath = input("what is the file part of your html email?\n")

SENDER = input("What is your sender info format[ SENDER_NAME <sender_email> ]\n")

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.


# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the 
# ConfigurationSetName=CONFIGURATION_SET argument below.
#CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = input("Enter your region\n")

# The subject line for the email.
SUBJECT = input("What is the subject of your email\n")

# The email body for recipients with non-HTML email client
            
# The HTML body of the email.
BODY_HTML = ""
with open(bodypath, 'r') as hp:
  for line in hp:
    BODY_HTML = BODY_HTML + line
  hp.close()  
 # The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

# Try to send the email.
for batch in RECIPIENT:
    count = count + 1
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'BccAddresses': 
                    batch,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
        el.append("Bacth" + str(count) + "Faild")
    else:
        sl.append("Bacth" + str(count) + "SUccess")
        print("Email sent! Message ID:"),
        print(response['MessageId'])

with open('success.txt', 'w') as s:
    for line in sl:
        s.write(line)
        s.write('\n')
s.close()

with open('error.txt', 'w') as p:
    for line in el:
        p.write(line)
        p.write('\n')
p.close()