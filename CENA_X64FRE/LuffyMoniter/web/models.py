from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

# Create your models here.

class IDC(models.Model):
    '''机房表'''
    name = models.CharField(max_length=64,unique=True,verbose_name='机房')

    def __str__(self):
        return self.name

class Business(models.Model):
    '''应用厂商表'''
    name = models.CharField(max_length=64,unique=True,verbose_name='厂商')

    def __str__(self):
        return self.name

class AppCompany(models.Model):
    """应用厂商表"""
    name = models.CharField(max_length=64, unique=True,verbose_name='业务系统')

    def __str__(self):
        return self.name

class Host(models.Model):
    """主机列表"""
    hostname = models.CharField(max_length=64,verbose_name="主机名")
    instance_name = models.CharField(max_length=64,verbose_name="实例名")
    ip_addr = models.GenericIPAddressField(unique=True,verbose_name="IP地址")
    port = models.PositiveSmallIntegerField(default=22,verbose_name="端口号")
    db_port = models.PositiveSmallIntegerField(default=1521,null=True,verbose_name="DB端口号")
    username = models.CharField(max_length=64,verbose_name="用户名")
    db_username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=True, null=True)
    db_password = models.CharField(max_length=128, blank=True, null=True)
    database_type_choices = ((0, 'oracle 10g'), (1, 'oracle 11g'), (2, 'oracle 12c'), (3, 'mysql'))
    database_type = models.SmallIntegerField(choices=database_type_choices,default=0,verbose_name="数据库类型")
    os_type_choices = ((0,'Linux'),(1,'windows'),(2,'AIX'))
    os_type = models.SmallIntegerField(choices=os_type_choices,default=0,verbose_name="OS类型")
    opatch_version = models.CharField(max_length=64,verbose_name="补丁")
    idc = models.ForeignKey("IDC",on_delete=models.CASCADE,verbose_name="机房")
    business = models.ForeignKey("Business",on_delete=models.CASCADE,verbose_name="业务系统名称")
    appcompany = models.ForeignKey("AppCompany",on_delete=models.CASCADE,verbose_name="厂商")
    templates = models.ManyToManyField("Template", blank=True)  # A D E

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.ip_addr


class Tablespace(models.Model):
    name = models.CharField(max_length=64,blank=True)
    total_size = models.CharField(max_length=64,blank=True)
    free_size = models.CharField(max_length=64,blank=True)
    used_size = models.CharField(max_length=64,blank=True)
    time = models.TimeField('时间',auto_now_add=True)
    host = models.ForeignKey('Host',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ServiceIndex(models.Model):
    '''指标列表'''
    name = models.CharField(max_length=64) #Linux cpu idle
    key =models.CharField(max_length=64,unique=True) #idle
    data_type_choices = (
        ('int',"int"),
        ('float',"float"),
        ('str',"string")
    )
    data_type = models.CharField(u'指标数据类型',max_length=32,choices=data_type_choices,default='int')
    memo = models.CharField(u"备注",max_length=128,blank=True,null=True)

    def __str__(self):
        return "%s.%s" %(self.name,self.key)

class Service(models.Model):
    '''服务列表，一个服务对应多个指标，'''
    name = models.CharField(u'服务名称',max_length=64,unique=True)
    interval = models.IntegerField(u'监控间隔',default=60)
    plugin_name = models.CharField(u'插件名',max_length=64,default='n/a')
    items = models.ManyToManyField('ServiceIndex',verbose_name=u"指标列表",blank=True)
    has_sub_service = models.BooleanField(default=False,help_text=u"如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡") #如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡
    memo = models.CharField(u"备注",max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(u'模版名称',max_length=64,unique=True)
    services = models.ManyToManyField('Service',verbose_name=u"服务列表")
    #triggers = models.ManyToManyField('Trigger',verbose_name=u"触发器列表",blank=True)
    def __str__(self):
        return self.name


class CpuInfo(models.Model):
    ip = models.CharField(max_length=64,blank=True,verbose_name=u"IP地址")
    user = models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name=u"用户使用率")
    nice = models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name=u"NICE")
    system  = models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name=u"系统使用率")
    idle = models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name=u"空闲率")
    time = models.CharField(max_length=64,blank=True,null=True,verbose_name=u"采集时间")
    status = models.CharField(max_length=6,blank=True,verbose_name=u"状态")
    host = models.ForeignKey('Host',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

class MemInfo(models.Model):
    ip = models.CharField(max_length=64,blank=True,verbose_name=u"IP地址")
    MemTotal = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"总内存(Kb)")
    MemFree = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"未分配内存(Kb)")
    Buffers  = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"Buffers(Kb)")
    Cached = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"Cached(Kb)")
    SwapTotal = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"总Swap(Kb)")
    SwapFree = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"空闲swap(Kb)")
    SwapUsage_p = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"swap使用率")
    SwapUsage = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"已用swap(Kb)")
    MemUsage_p = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"内存使用率")
    MemUsage = models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name=u"已分配内存(Kb)")
    time = models.CharField(max_length=64,blank=True,null=True,verbose_name=u"采集时间")
    status = models.CharField(max_length=6,blank=True,verbose_name=u"状态")

    host = models.ForeignKey('Host',null=True,on_delete=models.CASCADE)

class Filesystem(models.Model):
    ip = models.CharField(max_length=64, blank=True, verbose_name=u"IP地址")
    mount_point = models.CharField(max_length=64,blank=True,verbose_name=u"挂载点")
    Total_size = models.PositiveIntegerField(verbose_name=u'总大小')
    used_size = models.PositiveIntegerField(verbose_name=u'已用')
    avail_size = models.PositiveIntegerField(verbose_name=u'剩余')
    time = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"采集时间")
    status = models.CharField(max_length=6,blank=True,verbose_name=u"状态")

    host = models.ForeignKey('Host',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.mount_point


class LoadInfo(models.Model):
    ip = models.CharField(max_length=64,blank=True,verbose_name=u"IP地址")
    runtime = models.CharField(max_length=64,blank=True,verbose_name=u"IP地址")
    users = models.CharField(max_length=64,blank=True,verbose_name=u"IP地址")
    load1  = models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name=u"Buffers(Kb)")
    load5  = models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name=u"Buffers(Kb)")
    load15  = models.DecimalField(max_digits=5, decimal_places=2,null=True,verbose_name=u"Buffers(Kb)")

    time = models.CharField(max_length=64,blank=True,null=True,verbose_name=u"采集时间")
    status = models.CharField(max_length=6,blank=True,verbose_name=u"状态")

    host = models.ForeignKey('Host',null=True,on_delete=models.CASCADE)