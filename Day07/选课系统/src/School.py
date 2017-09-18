'''
学校类
'''
import ClassRoom
import Course
import Student
import Teacher
class School(object):

    #初始化学校名称 学校地址 班级字典 课程字典 学生字典 讲师字典
    def __init__(self,name,address):
        self.sch_name = name
        self.sch_addr = address
        self.sch_classroom = {}
        self.sch_course = {}
        self.sch_teacher = {}
        self.sch_student = {}

    # 创建课程
    def create_course(self,course_name,course_price,course_cycle):
        course_obj = Course(course_name,course_price,course_cycle)   #实例化课程
        self.sch_course[course_name] = course_obj    #更新字典

    #查看课程信息
    def show_course_info(self):
        for course_name in self.sch_course:
            course_obj = self.sch_course[course_name]
            print("课程名称：[%s]\t 课程价格：[%s]\t 课程周期:[%s]\t" %(course_obj.course_name,course_obj.course_price,course_obj.course_cycle))

    # 创建班级
    def create_classroom(self,class_name,course_obj):
        classroom_obj = ClassRoom(class_name,course_obj)   #实例化班级
        self.sch_classroom[class_name] = classroom_obj     #更新字典

    # 查看班级信息
    def show_classroom_info(self):
        for class_name in self.sch_classroom:
            classroom_obj = self.sch_classroom[class_name]
            print("班级名称：[%s] 课程名称：[%s]\t" %(classroom_obj.class_name,classroom_obj.class_course.course_name))


    #创建讲师
    def create_teacher(self,teach_name,sex,age,salary,classroom_name,classroom_obj):
        teacher_obj = Teacher(teach_name,sex,age,salary)
        teacher_obj.add_teach_classroom(classroom_name,classroom_obj)
        self.sch_teacher[teach_name] = teacher_obj

    #更改讲师授课班级
    def modify_teacher_info(self,teach_name,classroom_name,classroom_obj):
        teacher_obj = self.sch_teacher[teach_name]
        teacher_obj.add_teach_classroom(classroom_name, classroom_obj)

    def show_teacher_info(self):
        for teach_name in self.sch_teacher:
            teach_obj = self.sch_teacher[teach_name]
            classroom_list = []
            for c in teach_obj.teach_classroom:
                classroom_list.append(c)
            print("讲师姓名：[%s] \t 讲师性别:[%s]\t 讲师年龄:[%s]\t 讲师工资[%s]\t 所带班级[%s]\t"
                  %(teach_obj.teach_name,teach_obj.teach_sex,teach_obj.teach_age,teach_obj.teach_salary,classroom_list))

    #创建学生




