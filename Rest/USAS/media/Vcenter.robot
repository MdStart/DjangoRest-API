*** Settings ***
Library           ../../Users/nexii/Desktop/Ravi/work/Vcenter/VcenterOperations.py

*** Test Cases ***
test1
    Connect    183.82.41.58    root    Nexii@123
    Disconnect

connect_windows
    Connect Windows    192.168.5.167    nexii    nexii@    ride_test

list_of_datacenters
    Connect    183.82.41.58    root    Nexii@123
    ${list}    List Of Datacenters
    Log To Console    ${list}
    Disconnect

list_of_clusters
    Connect    183.82.41.58    root    Nexii@123
    ${list}    List Of Clusters
    Log To Console    ${list}
    Disconnect

cluster_exist_or_not
    Connect    183.82.41.58    root    Nexii@123
    ${status}    Cluster Exists Or Not    test2
    Log To Console    ${status}
    Disconnect

list_of_hosts_under_cluster
    Connect    183.82.41.58    root    Nexii@123
    ${list}    List Of Hosts Under Cluster    compute_cluster
    Log To Console    ${list}
    Disconnect

create_cluster
    Connect    183.82.41.58    root    Nexii@123
    ${name}    Create Cluster    Nexiilabs    ride_test2
    Log To Console    ${name}
    Disconnect

vm_snapshot
    Connect    183.82.41.58    root    Nexii@123
    Vm Snapshot    avinash    avi_snap7    ride testing snap
    Disconnect

vm_tools_upgrade
    Connect    183.82.41.58    root    Nexii@123
    Vmware Tools Upgrade    MBR-IAS3.11
    Disconnect

create_template
    Connect    183.82.41.58    root    Nexii@123
    Create Template    Nexiilabs    Nithya_test2    192.168.50.14    ride_temp1
    Disconnect

vm_to_different_datastore
    Connect    183.82.41.58    root    Nexii@123
    Vm To Different Datastore    ravi    192.168.50.11    datastore1
    Disconnect

clone_vm
    Connect    183.82.41.58    root    Nexii@123
    Clone Vm    Nexiilabs    mgmt_cluster    datastore1    Nithya_test2    ride_clone
    Disconnect
