# java 内存调优

# 相关指令

## jps
- -l 输出主类全名或jar路径
- -q 输出LVMID
- -m 输出jvm启动时传递给main的参数
- -v 输出jvm启动时显示指定的jvm参数


## 面试题

### 能否对JVM调优，让几乎不发生full GC（或很长时间才发生一次 full GC）

动态年龄判断机制
