# HDUPT 登录脚本

## 运行环境

* python 3.8.6
* tesseract v5.0.0-alpha.20201127

## 使用方法

### 方法一: 修改 `login.py`

1. 将主函数按照以下示例修改, 填入 `账号` 和 `密码`

   ```python
   if __name__ == '__main__':
      HduLogin('username', 'password')
      # HduLogin()
   ```

1. 命令行运行脚本

    ```
    $ python login.py
    ```

### 方法二: 添加命令行参数

1. 命令行运行脚本, 添加 `账号` 和 `密码`

    ```
    $ python login.py username password
    ```
