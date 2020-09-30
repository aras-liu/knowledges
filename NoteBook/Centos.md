CentOS7中“ONBOOT”已设置为“yes”但开机后ens33不会自启动解决方案
1. 执行下面的命令，将导致ifconfig出现ens33，但没有ip地址
ifconfig ens33 up
2. 执行下面的命令
systemctl stop NetworkManager
ifup ens33
3. 重启网络
systemctl restart network.service
4. 此时执行ifconfig发现ens33已经有了ip地址
5. 最后一步：永久关闭NetworkManager，保证下次开机ens33会自启动
systemctl disable NetworkManager
分类: Linux
