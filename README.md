# ⚓️ What is Kube-Palamar?

[Türkçe](README_TR.md) | English

`kube-palamar` is a tool that allows you to easily "moor" (scale down to 0 replicas) and "unmoor" (scale back up to original replica count) your Kubernetes resources such as Deployments, StatefulSets, and DaemonSets.

The name "Palamar" comes from the Turkish word for a mooring rope used to tie ships to a dock, symbolizing the act of safely "parking" your applications to rest.

## 🎯 Project Status

**Current Version:** Python scripts (active)  
**Future Plan:** Go CLI tool + Web UI (in planning phase)

This repository currently contains Python scripts for scaling up/down resources in Kubernetes namespaces. A CLI written in Go and a web interface will be added in the future.

---

## 📋 Requirements

- Python 3.x
- Kubernetes cluster access (kubeconfig must be configured)
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🚀 Usage

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/ruchany13/kube-palamar.git
cd kube-palamar

# Setup - Install required packages
./cluster.sh setup
```

### 2. Adding Annotations (Optional)
If you want to start your resources in a specific order, add the `order` annotation:

```bash
kubectl annotate deployment <deployment-name> -n <namespace> "order=<order_number>"
kubectl annotate statefulset <statefulset-name> -n <namespace> "order=<order_number>"
kubectl annotate daemonset <daemonset-name> -n <namespace> "order=<order_number>"
```

**Example:**
```bash
kubectl annotate deployment nginx-deployment -n production "order=1"
kubectl annotate statefulset mysql-sts -n production "order=2"
```

Alternatively, you can prepare `order.txt` file with all annotation commands and run:
```bash
./cluster.sh annotate
```

### 3. Scaling Down Namespace

Scales all resources in the namespace to 0 replicas and stores the current replica counts as annotations:

```bash
./cluster.sh down <namespace>
```

**Example:**
```bash
./cluster.sh down production
```

**What it does:**
- Scales Deployments to 0 replicas
- Scales StatefulSets to 0 replicas
- Disables DaemonSets using node selectors
- Stores the current replica count of each resource as a `replica_annotate` annotation

### 4. Scaling Up Namespace

Restores a previously scaled-down namespace to its original replica counts:

```bash
./cluster.sh up <namespace>
```

**Example:**
```bash
./cluster.sh up production
```

**What it does:**
- Reads original replica counts from the `replica_annotate` annotation
- Starts resources sequentially based on the `order` annotation
- Restores Deployments, StatefulSets, and DaemonSets to their previous state

---

## 📁 Project Structure

```
kube-palamar/
├── cluster.sh              # Main wrapper script - use this for all operations
├── down_cluster.py         # Python script to scale down namespace
├── up_cluster.py           # Python script to scale up namespace
├── requirements.txt        # Python dependencies
├── order.txt               # Namespace ordering file (optional)
└── README.md
```

---

## 🔍 Features

### ✅ Current (Python)
- ✅ Scale down/up Deployments
- ✅ Scale down/up StatefulSets
- ✅ Disable/enable DaemonSets
- ✅ Store replica counts as annotations
- ✅ Sequential startup support (order annotation)
- ✅ Namespace-based operations
- ✅ Simple shell wrapper for easy usage

### 🔜 Future (Go + Web UI)
- 🔜 Performant CLI written in Go
- 🔜 Visual management with web interface
- 🔜 Multi-namespace support
- 🔜 Automatic rollback
- 🔜 Scheduling and automation features

---

## 🎯 Quick Start

```bash
# 1. Setup
./cluster.sh setup

# 2. Scale down a namespace (saves current state)
./cluster.sh down production

# 3. Scale up the namespace (restores previous state)
./cluster.sh up production
```

---

## ⚠️ Important Notes

1. **First Usage:** You must run `./cluster.sh down <namespace>` first to save the current replica counts, then use `./cluster.sh up <namespace>` to restore them.
2. **Annotation Requirement:** The up script requires resources to have the `replica_annotate` annotation (automatically added by down script).
3. **DaemonSet Behavior:** DaemonSets are managed using node selectors instead of replica counts.
4. **Kubeconfig:** Scripts use the default kubeconfig (`~/.kube/config`).

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit a pull request.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Developer

**Ruchan Yalçın**  
- GitHub: [@ruchany13](https://github.com/ruchany13)
- Website: [www.ruchan.dev](https://www.ruchan.dev)
- Email: ruchany13@gmail.com

---

⭐️ If you like this project, don't forget to give it a star!