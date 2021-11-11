# TAS-autofill
This is a python script for automatically filling in the TAS system of the University of Twente. Note that using this tool is at your own risk. Filling in your password in a plain text file is serious security risk and it is recommended you delete the password afterwards.

# Usage
1. Download and unzip the latest release
1. Add your email, password and the OFI number of your project to settings.yaml inside folder that you just unzipped.
1. Run autofiller.exe
1. When you are asked to approve access to your account on your phone, approve
1. Autofill will now automatically fill in a predefined number of hours every day until it runs into a week which has no empty days
1. If it encounters any holidays or partial days of, it will fill in as many hours are need to get to this predefined number of hours
