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
    r = s.get('http://'+vega_ip+'/vsconfig?sid=0&form_name=95&dont_need_uri_decode=1&cli_command=show%20ports')
    #print r.text
    vega_data = r.text
    p.close()
    r.close()
    s.close()


fxo_results = vega_data.split('\n')

fxo_total_channels =0
fxo_inuse_channels = 0
fxo_available_channels = 0
fxo_blocked_channels = 0
fxo_disconnected_channels = 0

for chan in fxo_results:
    #print(chan)
    if "ready" in chan or "busy" in chan or "offline" in chan:
        chan_data = chan.split()
        print(chan_data)

        if len(chan_data) > 2:
            if "ready" in chan_data[4] :
                fxo_available_channels += 1
            if "busy" in chan_data[4] :
                fxo_inuse_channels += 1
            if "offline" in chan_data[4] :
                fxo_disconnected_channels += 1
        fxo_total_channels += 1

print('Total FXO Channels')
print(fxo_total_channels)

print('FXO InUse Channels')
print(fxo_inuse_channels)

print('FXO Available Channels')
print(fxo_available_channels)

print('FXO Disconnected Channels')
print(fxo_disconnected_channels)