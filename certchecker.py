"""
Script to get SSL certificates
"""

import ssl
import yaml
import pandas as pd
import jinja2
import os
import re
from socket import gaierror
from rich import print
from cryptography import x509
from datetime import datetime
from yaml import FullLoader
import pandas as pd
import numpy as np

def get_ssl_certificate(hostname):
    """ Get SSL certificate """

    try:
        result = ssl.get_server_certificate((hostname, 443))
        cert = x509.load_pem_x509_certificate(result.encode('utf-8'))

        duration = cert.not_valid_after - datetime.now()
        return cert.serial_number, cert.subject.rfc4514_string(), cert.issuer.rfc4514_string(), cert.not_valid_before.strftime('%Y-%m-%d'), cert.not_valid_after.strftime('%Y-%m-%d'), duration.days
    
    except ssl.SSLError as err:
        return 0, "error", "error", "0000-00-00","0000-00-00", "ssl error"
    except gaierror as err:
        return 0, "error", "error", "0000-00-00","0000-00-00", "unresolvable fqdn"
    except ConnectionRefusedError as err:
        return 0, "error", "error", "0000-00-00","0000-00-00", "connection refused"
    except ConnectionResetError as err:
        return 0, "error", "error", "0000-00-00","0000-00-00", "connection reset"
    except OSError as err:
        return 0, "error", "error", "0000-00-00","0000-00-00", "connection error"

def main():
    """Main"""

    with open("fqdn_list.yml", 'r', encoding='UTF-8') as fp:
        fqdn_dict = yaml.load(fp, Loader=FullLoader)

    df = pd.DataFrame()
    device_count = 1

    row_list = []
    fqdn_list = []
    serial_list = []
    subject_list = []
    issuer_list = []
    start_list = []
    end_list = []
    validity_list = []

    for fqdn in fqdn_dict['fqdns']:
        print(fqdn)
        serial, subject, issuer, start, end, validity = get_ssl_certificate(fqdn)
        
        if isinstance(validity, int):
            if validity > 10:
                validity = f"{validity} days"
            else:
                validity = f"<div class=\"font\">{validity} days</div>"
                
        fqdn_list.append(fqdn)
        serial_list.append(serial)
        subject_list.append(subject)
        issuer_list.append(issuer)
        start_list.append(start)
        end_list.append(end)
        validity_list.append(validity)
        row_list.append(device_count)

        device_count = device_count + 1

    df['Row'] = row_list
    df['device'] = fqdn_list
    df['start'] = start_list
    df['end'] = end_list
    df['validity'] = validity_list
    df['subject'] = subject_list
    df['issuer'] = issuer_list
    df['serial'] = serial_list
    
    html_table = df.to_html()
    html_table = re.sub('<table border="1" class="dataframe">', '', html_table)
    html_table = re.sub('&lt;', '<', html_table)
    html_table = re.sub('&gt;', '>', html_table)

    # print(html_table)

    loader = jinja2.FileSystemLoader(os.getcwd())
    jenv = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template_table = jenv.get_template("template_html.j2")

    html_output = template_table.render(
        html_table=html_table
    )

    #print(html_output)

    f = open('certificate-info.html', "w", encoding='utf-8')
    f.write(html_output)
    f.close()

    
if __name__ == "__main__":
    main()



