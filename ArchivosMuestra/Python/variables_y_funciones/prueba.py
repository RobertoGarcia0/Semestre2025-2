#!/usr/bin/env python3
"""
Este es un código de conceptos básicos
"""
x = 6
y = "Hola"
z = {1,2,3,57,32}
variable_char = 'a'

class TestClass():
  """
  Clase de prueba
  """
  x = 3
  y = "Adios"
  def test_func(self):
    """
    Función de prueba
    """
    print(x)
    print(self.x)
  def second_func(self):
    if x == self.x:
      self.test_func()
    elif y == self.y:
      pass
    for i in range(5):
      print(i)
  def third_func(self):
    lista_2 = ['a', 'b', 'c', 9, "sd"]
    lista_2.append('q')
    lista_2.remove('a')
    print(lista_2)
    conjunto = {1,2,3}
    print(conjunto)
    dicc = {"nombre": "Adan", "edad":"100"}
    print(dicc["nombre"])
    tupla = (1,2,3)
    a, b, c = (1,2,3)
    _, _, c = (1,2,3)
    print(c)
  def fourth_func(self, a, b, c, d, e, *args, **kwargs):
    if len(args) > 0:
      print("Hay {} argumentos adicionales".format(len(args)))
      print("Hay " + str(len(args)) + " argumentos adicionales")      
      for i in args:
        print(i)
    else:
      print("Sin argumentos adicionales")
    for key, value in kwargs.items():
      print(key)
      print(value)

test_obj = TestClass()
#test_obj.second_func()
#test_obj.third_func()
test_obj.fourth_func(a=4,c=5,b=7,e=6,d=9, f = 100)
