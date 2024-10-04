### Overview

---

This document provides an example of how to execute a custom Ansible strategy module. The custom strategy module, `Control`, is not a command-line tool but an Ansible object (Python code) designed for asynchronous playbook execution.

This repository includes a FastAPI-based application (web service) that enables the execution of the developed `Control` strategy module. The execution structure is as follows.

### Quick start

---

1. Create Docker Containers
    
    The working directory is `example/docker`. (Navigate to the directory before proceeding)
    
    - Run the `docker-compose.yml` file in the directory:
        
        ```bash
        ! docker-compose up -d
        ```
        
2. SSH Key Exchange
    - Generate SSH key (if the key does not exist in the local environment)
        
        ```bash
        ! ssh-keygen
        ```
        
    - Copy SSH key
        
        ```bash
        # The port numbers for the containers are 220 (vm1) and 221 (vm2). The password is 'test1234'.
        ! ssh-copy-id -p 220 root@localhost
        ! ssh-copy-id -p 221 root@localhost
        ```
        
    - Verify container access
        
        ```bash
        ! ssh -p 220 root@localhost # Verify successful connection
        ! ssh -p 221 root@localhost # Verify successful connection
        ```
        
3. Run the Application (Web Service)
    
    The working directory is the `project root (./)`. (Navigate to the directory before proceeding)
    
    - Execute the `main.py` function.
        
        ```bash
        python main.py
        ```
        
    - Access `localhost:8080/docs` to verify.
        ![img.png](img.png)