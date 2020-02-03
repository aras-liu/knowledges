# maven配置

## 下载安装maven （确保jdk已经安装）

    1. http://maven.apache.org/download.cgi 下载maven
    2. 解压并将bin目录添加至path环境变量
    3. 确保jdk已经安装，有JAVA_HOME环境变量
    4. 打开终端`mvn -v`

```
>mvn -v
Apache Maven 3.6.3 (cecedd343002696d0abb50b32b541b8a6ba2883f)
Maven home: D:\Program Files\apache-maven-3.6.3\bin\..
Java version: 1.8.0_221, vendor: Oracle Corporation, runtime: D:\Program Files\Java\jre1.8.0_221
Default locale: zh_CN, platform encoding: GBK
OS name: "windows 10", version: "10.0", arch: "amd64", family: "windows"
```

安装成功

## 配置mvn

通常修改解压目录下 `conf/settings.xml`文件

1. 修改本地本地仓库位置  
在`<localRepository>`标签内添加自己的本地位置路径  
```sh
<localRepository>D:\.m2\repository</localRepository>
```
2. 修改maven默认jdk版本
```
<profile>     
    <id>JDK-1.8</id>       
    <activation>       
        <activeByDefault>true</activeByDefault>       
        <jdk>1.8</jdk>       
    </activation>       
    <properties>       
        <maven.compiler.source>1.8</maven.compiler.source>       
        <maven.compiler.target>1.8</maven.compiler.target>       
        <maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>       
    </properties>       
</profile>
```
3. 添加镜像仓库
```
<!-- 阿里云仓库 -->
<mirror>
    <id>alimaven</id>
    <mirrorOf>central</mirrorOf>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/repositories/central/</url>
</mirror>

<!-- 中央仓库1 -->
<mirror>
    <id>repo1</id>
    <mirrorOf>central</mirrorOf>
    <name>Human Readable Name for this Mirror.</name>
    <url>http://repo1.maven.org/maven2/</url>
</mirror>

<!-- 中央仓库2 -->
<mirror>
    <id>repo2</id>
    <mirrorOf>central</mirrorOf>
    <name>Human Readable Name for this Mirror.</name>
    <url>http://repo2.maven.org/maven2/</url>
</mirror>
```
