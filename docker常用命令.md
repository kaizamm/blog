---
title: docker 常用命令
---

### docker image的导出有两种方法：
+ 方法一：docker save -o 导出的镜像名.tar 本地镜像名。后期使用该镜像，docker load -i 导出的镜像名.tar
```
$docker save -o centos.tar centos:latest #导出，用repository:tag可以导出镜像的元数据，若用images id则会丢失元数据，即在REPOSITORY和TAG的地方显示none。
$ls
centos.tar
$docker load -i centos.tar  #导入镜像
$docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
centos              latest              dcb7b7451a2b        3 months ago        196.7 MB
```
+ 方法二：docker push 镜像名

### 容器导出导入
1. 容器导出为tar包
```
$docker export -o container.tar db49ebf163ec
  $ls
  container.tar
```
2. 从容器导出的tar包导入成镜像，由于是导入的镜像，故需自己定义元数据，即镜像名和tag需自已定义。
 语法： cat 导出的tar包 | docker import - 镜像名：tag
```
  $cat container.tar | docker import - myimage/kaiz:1.0
  $docker images
  REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
  myimage/kaiz        1.0                 2169ac7d4e01        28 seconds ago      196.7 MB
```
3. 从导入的镜像启动容器
`$docker run -d 2169ac7d4e01 /bin/bash`

### 宿主机与容器之间的文件复制
从宿主机文件到容器
+ 通过docker inspect 查看挂载的路径，后从宿主机复制
+ $docker cp /root/bb db49ebf163ec:/

从容器到宿主机
+ $docker cp db49ebf163ec:/root/file.txt .

> 查看不同layers的命令是docker history 不是docker inspect

## docker --help
```bash
Usage: docker [OPTIONS] COMMAND [arg...]
Commands:

    attach    Attach to a running container
    build     Build an image from a Dockerfile
    commit    Create a new image from a containers changes
    cp        Copy files/folders between a container and the local filesystem
    create    Create a new container
    diff      Inspect changes on a containers filesystem
    events    Get real time events from the server
    exec      Run a command in a running container
    export    Export a containers filesystem as a tar archive
    history   Show the history of an image
    images    List images
    import    Import the contents from a tarball to create a filesystem image
    info      Display system-wide information
    inspect   Return low-level information on a container or image
    kill      Kill a running container
    load      Load an image from a tar archive or STDIN
    login     Register or log in to a Docker registry
    logout    Log out from a Docker registry
    logs      Fetch the logs of a container
    network   Manage Docker networks
    pause     Pause all processes within a container
    port      List port mappings or a specific mapping for the CONTAINER
    ps        List containers
    pull      Pull an image or a repository from a registry
    push      Push an image or a repository to a registry
    rename    Rename a container
    restart   Restart a container
    rm        Remove one or more containers
    rmi       Remove one or more images
    run       Run a command in a new container
    save      Save an image(s) to a tar archive
    search    Search the Docker Hub for images
    start     Start one or more stopped containers
    stats     Display a live stream of container(s) resource usage statistics
    stop      Stop a running container
    tag       Tag an image into a repository
    top       Display the running processes of a container
    unpause   Unpause all processes within a container
    version   Show the Docker version information
    volume    Manage Docker volumes
    wait      Block until a container stops, then print its exit code
```

## docker run --help
```bash
Commands:

  -a, --attach=[]                 Attach to STDIN, STDOUT or STDERR
  --add-host=[]                   Add a custom host-to-IP mapping (host:ip)
  --blkio-weight=0                Block IO (relative weight), between 10 and 1000
  --cpu-shares=0                  CPU shares (relative weight)
  --cap-add=[]                    Add Linux capabilities
  --cap-drop=[]                   Drop Linux capabilities
  --cgroup-parent=                Optional parent cgroup for the container
  --cidfile=                      Write the container ID to the file
  --cpu-period=0                  Limit CPU CFS (Completely Fair Scheduler) period
  --cpu-quota=0                   Limit CPU CFS (Completely Fair Scheduler) quota
  --cpuset-cpus=                  CPUs in which to allow execution (0-3, 0,1)
  --cpuset-mems=                  MEMs in which to allow execution (0-3, 0,1)
  -d, --detach=false              Run container in background and print container ID
  --device=[]                     Add a host device to the container
  --disable-content-trust=true    Skip image verification
  --dns=[]                        Set custom DNS servers
  --dns-opt=[]                    Set DNS options
  --dns-search=[]                 Set custom DNS search domains
  -e, --env=[]                    Set environment variables
  --entrypoint=                   Overwrite the default ENTRYPOINT of the image
  --env-file=[]                   Read in a file of environment variables
  --expose=[]                     Expose a port or a range of ports
  --group-add=[]                  Add additional groups to join
  -h, --hostname=                 Container host name
  --help=false                    Print usage
  -i, --interactive=false         Keep STDIN open even if not attached
  --ipc=                          IPC namespace to use
  --kernel-memory=                Kernel memory limit
  -l, --label=[]                  Set meta data on a container
  --label-file=[]                 Read in a line delimited file of labels
  --link=[]                       Add link to another container
  --log-driver=                   Logging driver for container
  --log-opt=[]                    Log driver options
  --lxc-conf=[]                   Add custom lxc options
  -m, --memory=                   Memory limit
  --mac-address=                  Container MAC address (e.g. 92:d0:c6:0a:29:33)
  --memory-reservation=           Memory soft limit
  --memory-swap=                  Total memory (memory + swap), '-1' to disable swap
  --memory-swappiness=-1          Tuning container memory swappiness (0 to 100)
  --name=                         Assign a name to the container
  --net=default                   Set the Network for the container
  --oom-kill-disable=false        Disable OOM Killer
  -P, --publish-all=false         Publish all exposed ports to random ports
  -p, --publish=[]                Publish a container's port(s) to the host
  --pid=                          PID namespace to use
  --privileged=false              Give extended privileges to this container
  --read-only=false               Mount the container's root filesystem as read only
  --restart=no                    Restart policy to apply when a container exits
  --rm=false                      Automatically remove the container when it exits
  --security-opt=[]               Security Options
  --sig-proxy=true                Proxy received signals to the process
  --stop-signal=SIGTERM           Signal to stop a container, SIGTERM by default
  -t, --tty=false                 Allocate a pseudo-TTY
  -u, --user=                     Username or UID (format: <name|uid>[:<group|gid>])
  --ulimit=[]                     Ulimit options
  --uts=                          UTS namespace to use
  -v, --volume=[]                 Bind mount a volume
  --volume-driver=                Optional volume driver for the container
  --volumes-from=[]               Mount volumes from the specified container(s)
  -w, --workdir=                  Working directory inside the container
```
