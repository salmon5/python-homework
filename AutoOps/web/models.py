from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

# Create your models here.

class IDC(models.Model):
    '''机房表'''
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name

class Business(models.Model):
    '''应用厂商表'''
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name

class AppCompany(models.Model):
    """应用厂商表"""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Host(models.Model):
    """主机列表"""
    hostname = models.CharField(max_length=64)
    instance_name = models.CharField(max_length=64)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.PositiveSmallIntegerField(default=22)
    username = models.CharField(max_length=64)
    db_username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=True, null=True)
    db_password = models.CharField(max_length=128, blank=True, null=True)
    database_type_choices = ((0, 'oracle 10g'), (1, 'oracle 11g'), (2, 'oracle 12c'), (3, 'mysql'))
    database_type = models.SmallIntegerField(choices=database_type_choices,default=0)
    os_type_choices = ((0,'Linux'),(1,'windows'),(2,'AIX'))
    os_type = models.SmallIntegerField(choices=os_type_choices,default=0)
    opatch_version = models.CharField(max_length=64)
    idc = models.ForeignKey("IDC",on_delete=models.CASCADE)
    business = models.ForeignKey("Business",on_delete=models.CASCADE)
    appcompany = models.ForeignKey("AppCompany",on_delete=models.CASCADE)

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.ip_addr


# class RemoteUser(models.Model):
#     """存储远程用户名密码（主机的密码）"""
#     username = models.CharField(max_length=64)
#     auth_type_choices = ((0,'ssh/password'),(1,'ssh/key'))
#     auth_type = models.SmallIntegerField(choices=auth_type_choices,default=0)
#     password = models.CharField(max_length=128,blank=True,null=True)
#
#     def __str__(self):
#         return "%s(%s)%s" %( self.username,self.get_auth_type_display(),self.password)
#
#     class Meta:
#         unique_together = ('username','auth_type','password')   #联合唯一

# class BindHost(models.Model):
#     """绑定远程主机和远程用户的对应关系"""
#     host = models.ForeignKey("Host",on_delete=models.CASCADE)
#     remote_user = models.ForeignKey("RemoteUser",on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "%s -> %s" %(self.host,self.remote_user)
#     class Meta:
#         unique_together = ("host","remote_user")     #联合唯一

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )

    # bind_hosts = models.ManyToManyField("BindHost",blank=True)
    # host_groups = models.ManyToManyField("HostGroup",blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Session(models.Model):
    '''生成用户操作session id '''
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    #bind_host = models.ForeignKey('BindHost',on_delete=models.CASCADE)
    bind_host = models.ForeignKey('Host',on_delete=models.CASCADE)
    tag = models.CharField(max_length=128,default='n/a')
    closed = models.BooleanField(default=False)
    cmd_count = models.IntegerField(default=0) #命令执行数量
    stay_time = models.IntegerField(default=0, help_text="每次刷新自动计算停留时间",verbose_name="停留时长(seconds)")
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return '<id:%s user:%s bind_host:%s>' % (self.id,self.user.email,self.bind_host.host)
    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'

class Task(models.Model):
    """批量任务记录表"""
    user = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    task_type_choices = ((0,'cmd'),(1,'file_transfer'))
    task_type = models.SmallIntegerField(choices=task_type_choices)
    content = models.TextField(verbose_name="任务内容")
    hosts = models.ManyToManyField("Host")
    date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.task_type,self.content)


class TaskLogDetail(models.Model):
    task = models.ForeignKey("Task",on_delete=models.CASCADE)
    # bind_host = models.ForeignKey("BindHost",on_delete=models.CASCADE)
    bind_host = models.ForeignKey("Host",on_delete=models.CASCADE)
    result = models.TextField()

    status_choices = ((0,'success'),(1,'failed'),(2,'init'))
    status = models.SmallIntegerField(choices=status_choices)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return "%s %s" %(self.bind_host,self.status)