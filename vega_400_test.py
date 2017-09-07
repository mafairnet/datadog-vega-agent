#!/usr/bin/python
import requests

vega_ip = "0.0.0.0" 

vega_data = ""

# Fill in your details here to be posted to the login form.
payload = {
    'username': 'user',
    'password': 'pass'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('http://'+vega_ip+'/vs_login', data=payload)
    # print the html returned or something more intelligent to see if it's a successful login page.
    #print p.text

    # An authorised request.
    r = s.get('http://'+vega_ip+'/vsconfig?sid=0&form_name=95&dont_need_uri_decode=1&cli_command=mfcr2%20status')
    #print r.text
    vega_data = r.text
    p.close()
    r.close()
    s.close()


mfcr2_results = vega_data.split('\n')

#mfcr2_total_channels = len(mfcr2_results)-33
#print mfcr2_total_channels

mfcr2_total_channels =0 
mfcr2_inuse_channels = 0
mfcr2_available_channels = 0
mfcr2_blocked_channels = 0
mfcr2_disconnected_channels = 0

for chan in mfcr2_results:
    #print(chan)
    if "0x00" in chan or "BLOCK" in chan or "ANSWER" in chan or "IDLE" in chan:
        chan_data = chan.split()
        print(chan_data)
        if len(chan_data) > 2:
            if "IDLE" in chan_data[6] and "IDLE" in chan_data[7] :
                mfcr2_available_channels += 1
            if "ANSWER" in chan_data[6] or "ANSWER" in chan_data[7] :
                mfcr2_inuse_channels += 1
            if "BLOCK" in chan_data[6] or "BLOCK" in chan_data[7] :
                mfcr2_blocked_channels += 1
            if "0x00" in chan_data[6] or "0x00" in chan_data[7] :
                mfcr2_disconnected_channels += 1
            mfcr2_total_channels += 1

print('Total MFCR2 Channels')
print(mfcr2_total_channels)

print('MFCR2 InUse Channels')
print(mfcr2_inuse_channels)

print('MFCR2 Available Channels')
print(mfcr2_available_channels)

print('MFCR2 Blocked Channels')
print(mfcr2_blocked_channels)

print('MFCR2 Disconnected Channels')
print(mfcr2_disconnected_channels)
