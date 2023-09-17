# 安装

  pip install -r require.txt

# 修改MongoDB配置

  在 bin/util.sh 修改MongoDB配置。该文件仅用于测试

# dockerfile

  修改 镜像仓库。fastapi-base:v1.0 就是一个安装了 require.txt的镜像。

# k8s

  需要修改镜像仓库以及 config 与 secret

# 运行demo

  ```shell
  make dev
  ```

# 测试访问

  ```shell
  http :8000/demo/create name=13  # 得到ID
  http :8000/demo/query id=$ID
  http :8000/demo/update name=13 id=$ID
  http :8000/demo/list 1=1
  http :8000/demo/delete id=$ID
  ```
