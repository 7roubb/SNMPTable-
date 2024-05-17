Simple Network Management Protocol (SNMP) is a widely used protocol in network management systems. 
It allows administrators to monitor and manage network performance, find and solve network issues, 
and plan for network growth. SNMP works by sending messages, called protocol data units (PDUs), 
to different parts of a network. SNMP-compliant devices, called agents, 
store data about themselves in Management Information Bases (MIBs) and return this data to the SNMP requesters.


#Command Lines to install SNMP :
  sudo apt update 
  sudo apt install snmpd
  
  


Configure SNMP on RHEL 7
  Follow these steps:
    Set up a minimal configuration by issuing the following command:
      cd /etc/snmp
      cp -p snmpd.conf snmpd.conf.dist
      echo "rocommunity public">snmpd.conf
      echo "syslocation here" >>snmpd.conf
      echo "syscontact root@localhost" >>snmpd.conf
  Activate at boot and start the SNMP service by issuing the following command:
      systemctl enable snmpd && systemctl start snmpd
  Execute a simple test by issuing the following command:
      snmpwalk -v 1 -c public -O e 127.0.0.1SNMPv2-MIB::sysDescr.0 = STRING: Linux rhel7.example.com 3.10.0-54.0.1.el7.x86_64 #1 SMP Tue Nov 26 16:51:22 EST 2013 x86_64SNMPv2-MIB::sysObjectID.0 = OID: NET-SNMP-MIB::netSnmpAgentOIDs.10
  For more information about how to add viewing rights for HostResources-MIB and UCD-SNMP-MIB, see the snmpd.conf file, or check online for information about how to set up read permissions.


 
