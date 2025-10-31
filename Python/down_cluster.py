# Updated by Ruchan Yalçın
# ruchany13@gmail.com

from kubernetes import client, config
import sys

config.load_kube_config()
v1 = client.AppsV1Api()

choosen_ns = sys.argv[1]
choosen_ns = [choosen_ns]

#choosen_ns = ['wordpress']

# set replica number to 0 
def scale_down_replica(ns,name,kind):
    annotations = {"spec":{"replicas": 0}}
    
    if kind == "deployment":
        v1.patch_namespaced_deployment(name=name, namespace=ns, body=annotations)
    elif kind == "statefulset":
        v1.patch_namespaced_stateful_set(name=name, namespace=ns, body=annotations)
    elif kind == 'daemonset':
        annotations = {"spec": {"template": {"spec": {"nodeSelector": {"non-existing": "true"}}}}}
        v1.patch_namespaced_daemon_set(name=name, namespace=ns, body=annotations)

    

def add_replica_count_annotate(kind,ns,name,replica_count):
    annotations = {"metadata":{"annotations":{"replica_annotate": replica_count}}}
    
    if kind == "deployment":
        v1.patch_namespaced_deployment(name=name, namespace=ns, body=annotations)
    elif kind == "statefulset":
        v1.patch_namespaced_stateful_set(name=name, namespace=ns, body=annotations)
        
        
def get_replica_counts(ns,kind):
    replica_counts_list = []
    if kind == 'deployment':
        get_replica_counts_call = v1.list_namespaced_deployment(ns)
    elif kind == 'statefulset':
        get_replica_counts_call = v1.list_namespaced_stateful_set(ns)
    elif kind == 'daemonset':
        get_replica_counts_call = v1.list_namespaced_daemon_set(ns)
    
    if kind == 'daemonset':
        for i in get_replica_counts_call.items:
            i_dict = {}
            i_ns = ns
            i_kind = kind
            i_name = i.metadata.name
            i_dict['namespace'] = i_ns
            i_dict['kind'] = i_kind
            i_dict['name'] = i_name
            replica_counts_list.append(i_dict)
            scale_down_replica(i_ns,i_name,i_kind)
    else:
            
        for i in get_replica_counts_call.items:
            i_dict = {}
            i_ns = ns
            i_kind = kind
            i_name = i.metadata.name
            i_currrent_replcount = i.spec.replicas
            i_dict['namespace'] = i_ns
            i_dict['kind'] = i_kind
            i_dict['name'] = i_name
            i_dict['replica_count'] = i_currrent_replcount
            replica_counts_list.append(i_dict)
            add_replica_count_annotate(kind=i_kind, ns=i_ns, name=i_name, replica_count=str(i_currrent_replcount))
            scale_down_replica(i_ns,i_name,i_kind)
            
    return replica_counts_list



output=""

for ns in choosen_ns:
    output += f'######## Namespace: {ns} ########\n'
    
    output += f'---StatefulSets---\n'
    stss = get_replica_counts(ns,'statefulset')
    for sts in stss:
        output += f"Namespace: {sts['namespace']}, Kind: {sts['kind']}, Name: {sts['name']}, Count: {sts['replica_count']}\n"
    
    output += f'---Deployments---\n'
    deploys = get_replica_counts(ns,'deployment')
    for deploy in deploys:
        output += f"Namespace: {deploy['namespace']}, Kind: {deploy['kind']}, Name: {deploy['name']}, Count: {deploy['replica_count']}\n"
    
    output += f'---Daemonset---\n'
    daemonsets = get_replica_counts(ns,'daemonset')
    for daemonset in daemonsets:
        output += f"Namespace: {daemonset['namespace']}, Kind: {daemonset['kind']}, Name: {daemonset['name']}\n"

print(output)
