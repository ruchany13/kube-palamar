# Developed by Ruchan Yalçın
# ruchany13@gmail.com

from kubernetes import client, config
import time
import sys

# Load kubeconfig
config.load_kube_config()
v1 = client.AppsV1Api()

#choosen_ns = "wordpress"
choosen_ns = sys.argv[1]

def progress_bar2(count, total, status=''):
    bar_len = 60
    if count == None:
        count = 0
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def progress_bar(current, total, bar_length=60):
    if current == None:
        current = 0
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    print(f"\rProgress: [{arrow}{spaces}] {int(round(percent * 100))}%", end="")


object_list = []

# Add deployments info in namespace to list with dictionary 
get_deployment_from_ns = v1.list_namespaced_deployment(choosen_ns)
for i in get_deployment_from_ns.items:
    i_dict = {}
    i_ns = i.metadata.namespace
    i_name = i.metadata.name
    i_kind = "deploy"
    i_order = i.metadata.annotations["order"]
    i_replica = i.metadata.annotations["replica_annotate"]
    i_dict['order'] = i_order
    i_dict['namespace'] = i_ns
    i_dict['kind'] = i_kind
    i_dict['name'] = i_name
    i_dict['replica'] = i_replica
    object_list.append(i_dict)

# Add statefulset info in namespace to list with dictionary 
get_sts_from_ns = v1.list_namespaced_stateful_set(choosen_ns)

for i in get_sts_from_ns.items:
    i_dict = {}
    i_ns = i.metadata.namespace
    i_name = i.metadata.name
    i_kind = "sts"
    i_order = i.metadata.annotations["order"]
    i_replica = i.metadata.annotations["replica_annotate"]
    i_dict['order'] = i_order
    i_dict['namespace'] = i_ns
    i_dict['kind'] = i_kind
    i_dict['name'] = i_name
    i_dict['replica'] = i_replica
    object_list.append(i_dict)

# Add daemonset info in namespace to list with dictionary 
get_daemonset_from_ns = v1.list_namespaced_daemon_set(choosen_ns)

for i in get_daemonset_from_ns.items:
    i_dict = {}
    i_ns = i.metadata.namespace
    i_name = i.metadata.name
    i_kind = "daemonset"
    i_order = i.metadata.annotations["order"]
    i_dict['order'] = i_order
    i_dict['namespace'] = i_ns
    i_dict['kind'] = i_kind
    i_dict['name'] = i_name
    object_list.append(i_dict)

# Operation part
count = 0
for count in range(0,500):
    for k8s_object in object_list:
        if count == int(k8s_object["order"]):
            
        #------------ Deployment ----------------#   
            if k8s_object["kind"] == "deploy":
                get_replica_counts_deployment_call = v1.read_namespaced_deployment(name=k8s_object["name"], namespace=k8s_object["namespace"])
                
                print("Order:",k8s_object["order"],"\tName:",get_replica_counts_deployment_call.metadata.name,"\tType:",k8s_object["kind"])
                annotations = [
                            {
                            'op': 'replace',  
                            'path': '/spec/replicas',
                            'value': int(k8s_object["replica"])
                            }
                            ]

                v1.patch_namespaced_deployment(name=k8s_object["name"], namespace=k8s_object["namespace"], body=annotations)
                ready_replicas = v1.read_namespaced_deployment(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status.ready_replicas
                while int(k8s_object["replica"]) != ready_replicas:
                    ready_replicas = v1.read_namespaced_deployment(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status.ready_replicas
                    progress_bar(ready_replicas, int(k8s_object["replica"]))
                    time.sleep(3)
                print()
        #------------- Statefulset --------------#
                
            elif k8s_object["kind"] == "sts":
                get_replica_counts_sts_call = v1.read_namespaced_stateful_set(name=k8s_object["name"], namespace=k8s_object["namespace"])
                print("Order:",k8s_object["order"],"\tName:",get_replica_counts_sts_call.metadata.name,"\tType:",k8s_object["kind"])
                
                annotations = [
                        {
                        'op': 'replace', 
                        'path': '/spec/replicas',
                        'value': int(k8s_object["replica"])
                        }
                    ]

                v1.patch_namespaced_stateful_set(name=k8s_object["name"], namespace=k8s_object["namespace"], body=annotations)
                annotate_replica = int(k8s_object["replica"])
                ready_replicas = v1.read_namespaced_stateful_set(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status.ready_replicas
                while int(k8s_object["replica"]) != ready_replicas:
                    ready_replicas = v1.read_namespaced_stateful_set(name=k8s_object["name"],namespace=k8s_object["namespace"]).status.ready_replicas
                    progress_bar(ready_replicas, int(k8s_object["replica"]))
                    time.sleep(3)
                    
        #------------- DaemonSet ----------------#
            elif k8s_object["kind"] == "daemonset":
                get_replica_counts_daemonset_call = v1.read_namespaced_daemon_set(name=k8s_object["name"], namespace=k8s_object["namespace"])                  
                print("Order:",k8s_object["order"],"\tName:",get_replica_counts_daemonset_call.metadata.name,"\tType:",k8s_object["kind"])
                
                desired_pod = v1.read_namespaced_daemon_set(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status.desired_number_scheduled
                annotations = [
                            {
                              'op': 'remove', 
                              'path': '/spec/template/spec/nodeSelector/non-existing',
                              'value': { 'non-existing' : 'false'}
                            }
                          ]
                # if for pass to up daemonset
                if desired_pod == 0 :
                    v1.patch_namespaced_daemon_set(name=k8s_object["name"], namespace=k8s_object["namespace"], body=annotations)
                
                # have to wait desired pod number 0 to target deifinition
                time.sleep(5)                
                
                desired_pod = v1.read_namespaced_daemon_set(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status.desired_number_scheduled
                current_pod = v1.read_namespaced_daemon_set(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status.current_number_scheduled
                
                while current_pod != desired_pod:
                  print(v1.read_namespaced_daemon_set(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status)
                  
                  current_pod = v1.read_namespaced_daemon_set(name=k8s_object["name"],namespace=k8s_object["namespace"] ).status.current_number_scheduled
                  progress_bar(current_pod,desired_pod )
                  time.sleep(3)
                print()