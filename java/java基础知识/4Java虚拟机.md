
# java虚拟机

JDK >> JRE >> JVM

## 字节码
Java字节码，一次编写  到处执行
每一份代码的Java字节码相同，jvm根据不同的操作系统（本质是不同版本的jvm），将Java字节翻译成不同的机器码来执行。
从软件层面屏蔽不同操作系统在底层硬件与操作指令的区别



## jvm 内存模型主要组成部分
公共区：堆 执行引擎 方法区
线程私有： 程序计数器，线程栈，本地线程栈

## 程序计数器
线程私有，因为java程序时多线程的，在线程切换需要保存一下当前线程执行的代码行数，当线程切回来的时候能够恢复线程

## 虚拟机栈、
线程私有，线程由栈帧组成，每个函数都是一个栈帧，由四部分组成：变量表（保存基本数据类型与对象的地址），操作数栈，返回值地址，动态链接。

## 本地线程栈
线程私有，与线程栈类似，当执行C语言代码时 使用的栈。native  

## 堆
线程公有的区域，分为新生代与老年代（1：2）,新生代分为 eden s0，s1区，首先，当eden区满时发生 小GC，收集的对象放入s0区


## 


