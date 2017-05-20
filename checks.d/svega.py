#
# Sangoma Vega Agent for DataDog
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

            ## MFCR2 DATA  
            # An authorised request.
            r = s.get('http://'+instance['host']+'/vsconfig?sid=0&form_name=95&dont_need_uri_decode=1&cli_command=mfcr2%20status')
            vega_data = r.text

            mfcr2_results = vega_data.split('\n')

            mfcr2_total_channels =0 
            mfcr2_inuse_channels = 0
            mfcr2_available_channels = 0
            mfcr2_blocked_channels = 0
            mfcr2_disconnected_channels = 0

            for chan in mfcr2_results:
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
            
            self.gauge('svega.'+instance['name']+'.mfcr2.total.channels',mfcr2_total_channels)
            self.gauge('svega.'+instance['name']+'.mfcr2.inuse.channels',mfcr2_inuse_channels)
            self.gauge('svega.'+instance['name']+'.mfcr2.available.channels',mfcr2_available_channels)
            self.gauge('svega.'+instance['name']+'.mfcr2.blocked.channels',mfcr2_blocked_channels)
            self.gauge('svega.'+instance['name']+'.mfcr2.disconnected.channels',mfcr2_disconnected_channels)

            ## Close session
            p.close()
            r.close()
            s.close()