import subprocess

#this for snmp table options
""""
-Cb 
    Displays only a brief heading. Any common prefix of the table field names will be deleted.

-CB 
    Does not use GETBULK requests to retrieve data, only GETNEXT.

-Cc CHARS 
    Print table in columns of CHARS characters width.

-Cf STRING 
    Uses the string STRING to separate table columns. With this option, each table entry will be printed in compact form, just with the string given to separate the columns (useful if you want to import it into a database). Otherwise it is printed in nicely aligned columns.

-Ch 
    Displays only the column headings.

-CH 
    Does not display the column headings.

-Ci 
    Prepends the index of the entry to all printed lines.

-Cr REPEATERS 
    For GETBULK requests, REPEATERS specifies the max-repeaters value to use. For GETNEXT requests, REPEATERS specifies the number of entries to retrieve at a time.

-Cw WIDTH 
    Specifies the width of the lines when the table is printed. If the lines will be longer, the table will be printed in sections of at most WIDTH characters.

"""

def fetch_snmp_table(community, ip):
    command = [
        'snmptable',
        '-v', '2c',
        '-c', community,
        '-Cl',
        '-CB',
        '-Ci',
        '-OX',
        '-Cb',
        '-Cc', '16',
        '-Cw', '64',
        ip,
        'ifTable'
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("SNMP Table Output:")
            print(result.stdout)
        else:
            print("Error running snmptable command:")
            print(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

def get_snmp_table_row_by_row(community, ip, start_oid):
    oid = start_oid

    while True:
        command = ['snmpgetnext', '-v2c', '-c', community, '-On', ip, oid]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            break

        output = result.stdout.strip()
        if not output:
            break

        print(output)

        oid = output.split()[0]

        if not oid.startswith(start_oid):
            break

def get_snmp_table_column_by_column(community, ip, start_oid):
    column_oids = [start_oid]
    column_data = []

    while column_oids:
        next_column_oids = []
        column_values = []

        for oid in column_oids:
            command = ['snmpgetbulk', '-v2c', '-c', community, '-Cr1', '-On', '-Cn1', '-Ct1', ip, oid]

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                print(f"Error: {result.stderr.strip()}")
                return

            output = result.stdout.strip()
            if not output:
                continue

            print(output)
            column_values.append(output)
            next_oid = output.split()[0]
            if next_oid.startswith(start_oid):
                next_column_oids.append(next_oid)

        column_oids = next_column_oids
        column_data.append(column_values)

    return column_data

# Main program
community = input("Enter SNMP Community String: ")
ip = input("Enter IP Address of SNMP Agent: ")
start_oid = '1.3.6.1.2.1.2.2'  # Starting OID for ifTable

while True:
    print("\nSelect an option:")
    print("1. Fetch SNMP Table")
    print("2. Get SNMP Table Row by Row")
    print("3. Get SNMP Table Column by Column")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        fetch_snmp_table(community, ip)
    elif choice == '2':
        get_snmp_table_row_by_row(community, ip, start_oid)
    elif choice == '3':
        get_snmp_table_column_by_column(community, ip, start_oid)
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")
