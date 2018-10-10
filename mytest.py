# coding:utf-8


class Myclass(object):
    def __init__(self):
        pass

    def edit(self):
        return 1
    edit.dsc = '给方法绑定属性'
    def register(self):
        temp = []
        temp.append(Myclass.edit)
        return temp
    def register2(self):
        temp = ['edit',]
        return temp


class Test(object):
    def __init__(self,myclass):
        self.myclass = myclass

    def test_edit(self):
        t2 = self.myclass.edit()
        print t2
myclass = Myclass()
t1 = myclass.register()
# t = Test(myclass)
# t.test_edit()
t2 = t1[0]
print t2(myclass)   # 注意未绑定方法必须传入实例对象,否则报错：unbound method edit() must be called with Myclass instance as first argument (got nothing instead)

t3 = myclass.register2()
t4 = getattr(myclass,t3[0])
print t4(), t4.__name__, t4.dsc

