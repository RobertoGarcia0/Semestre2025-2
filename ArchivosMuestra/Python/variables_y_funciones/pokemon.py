#!/usr/bin/env python3
"""
Este archivo contiene las clases para
pokemons y sus ataques
"""
class Ataque():
  """Representa los ataques del pokemon"""
  def __init__(self, nombre:str, poder:int):
    """
    Inicialización del ataque
    Args: 
      nombre (str): Nombre del ataque
      poder  (int): Poder del ataque
    """
    self.nombre = nombre
    self.poder = poder

class Pokemon():
  """Representa un pokemon"""
  def __init__(self, nombre:str, nivel:int):
    """
    Inicialización del pokemon
    Args:
      nombre (str): Nombre del pokemon
      nivel  (int): Nivel del pokemon
    Returns:
      none
    """
    self.nombre = nombre
    self.nivel = nivel
    self.ataques = []
  def agregar_ataque(self, ataque:Ataque):
    """
    Método para agregar ataque
    Args: 
      ataque (Ataque): Ataque que voy a agregar
    Returns:
      none
    """
    self.ataques.append(ataque)
    print("Se agregó a {} el ataque {} con poder {}".format(self.nombre, ataque.nombre, ataque.poder))
  
