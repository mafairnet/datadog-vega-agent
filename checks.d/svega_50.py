#
# Sangoma Vega 50 Agent for DataDog
# By mafairnet [Miguel Angel Torres Govea]
#

import requests
from checks import AgentCheck

class SvegaCheck(AgentCheck):

    def check(self, instance):

        if 'host' not in instance:
            self.log.error('host not defined, skipping')
        if 'name' not in instance:
            self.log.error('name not defined, skipping')
        if 'user' not in instance:
            self.log.error('user not defined, skipping')
            return
        if 'secret' not in instance:
            self.log.error('manager_secret not defined, skipping')
            return

        # Fill in your details here to be posted to the login form.
        payload = {
            'username': instance['user'],
            'password': instance['secret']
        }

        ## CONNECT
        ## Use 'with' to ensure the session context is closed after use.
        with requests.Session() as s:
            p = s.post('http://'+instance['host']+'/vs_login', data=payload)

            ## FXO DATA  
            # An authorised request.
            r = s.get('http://'+instance['host']+'/vsconfig?sid=0&form_name=95&dont_need_uri_decode=1&cli_command=show%20ports')
            vega_data = r.text

            fxo_results = vega_data.split('\n')

            fxo_total_channels =0 
            fxo_inuse_channels = 0
            fxo_available_channels = 0
            fxo_blocked_channels = 0
            fxo_disconnected_channels = 0

            for chan in fxo_results:
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
            
            self.gauge('svega.'+instance['name']+'.fxo.total.channels',fxo_total_channels)
            self.gauge('svega.'+instance['name']+'.fxo.inuse.channels',fxo_inuse_channels)
            self.gauge('svega.'+instance['name']+'.fxo.available.channels',fxo_available_channels)
            self.gauge('svega.'+instance['name']+'.fxo.disconnected.channels',fxo_disconnected_channels)

            ## Close session
            p.close()
            r.close()
            s.close()