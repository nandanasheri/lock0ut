from typing import Any
from datetime import datetime, timedelta
from collections import defaultdict

import sqlite3

DISTRACTORS = set([
    "linkedin",
    "tiktok",
    "reddit",
    "facebook",
    "youtube",
    "discord",
    "snapchat",
    "whatsapp",
    "instagram",
    "netflix",
    "amazon",
    "hbo",
    "zara"
])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    # This gives you name-bases access to columns in your database
    conn.row_factory = sqlite3.Row
    return conn

def distracting_sites_count():
    conn = get_db_connection()
    rows = conn.execute("SELECT destination_name FROM traffic").fetchall()
    hostnames = [row[0] for row in rows]
    distractor_packets = 0
    for hostname in hostnames:
          if any(distractor in hostname for distractor in DISTRACTORS):
              distractor_packets += 1
    return distractor_packets/len(hostnames) * 100

def get_overall_traffic() -> Any:
    conn = get_db_connection()
    rows = conn.execute("SELECT COUNT(id), destination_name from traffic GROUP BY destination_name ORDER BY COUNT(id) DESC").fetchall()
    packets_dict = []
    for row in rows:
        packets_dict.append((row[1], row[0]))

    return packets_dict

def get_sourceip_packets() -> Any:
    conn = get_db_connection()
    rows = conn.execute("SELECT src_ip, COUNT(id) from traffic GROUP BY src_ip")
    src_data = []
    for row in rows:
        src_data.append((row[0], row[1]))
    return src_data
'''
take last 10 minutes
find top 3 most visited domains
for each
{ time: "21:35", google.com: 385, chatgpt.com: 420 },
  { date: "2024-05-05", desktop: 481, mobile: 390 },
  { date: "2024-05-06", desktop: 498, mobile: 520 }
'''
def json_to_time_data() -> Any:
    conn = get_db_connection()
    rows = conn.execute("SELECT time, destination_name FROM traffic WHERE time >= datetime((SELECT MAX(time) FROM traffic), '-10 minutes') ORDER BY time;").fetchall()
  
    # Initialize a dictionary to hold time -> hostname counts
    time_data = defaultdict(lambda: defaultdict(int))

    # Process the rows
    for row in rows:
        time_str = row[0]  # The 'time' from the query
        hostname = row[1]  # The 'hostname' from the query
        
        # Extract only the hour and minute (HH:MM format)
        time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f').strftime('%H:%M')
        time_data[time][hostname] += 1
    
    flat_data = []
    for time, hosts in time_data.items():
        for hostname, count in hosts.items():
            flat_data.append((hostname, count))

    # Get the top 3 most visited domains overall
    top_domains = sorted(flat_data, key=lambda x: x[1], reverse=True)[:3]

    top_domain_names = []
    for i in top_domains:
        top_domain_names.append(i[0])

    result = {}
    for time, host in time_data.items():
        minute = time
        if minute not in result:
            result[minute] = {}
            result[minute][top_domain_names[0]] = 0
            result[minute][top_domain_names[1]] = 0
            result[minute][top_domain_names[2]] = 0
        for hostname, count in host.items():
            if hostname in top_domain_names:
                result[minute][hostname] = count
    return result
    

    






