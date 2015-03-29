package hw2

import java.util
import java.util.ArrayList
import java.util.Collections

class A {
  def foo() {
    println ("A::foo")
  }
}

class B() {
  def bar() {
    println ("B::bar")
  }
}

class C() {
  def ccc() {
    println ("C::ccc")
  }
}

object Main {
  /**
   * Написать три конверсии A => B, A => C, B => C лишь двумя implicit функциями.
   */
  implicit def A2B[T <% A](t : T) = new B()
  implicit def B2C[T <% B](t : T) = new C()

  /**
   * Расширить java.util.ArrayList методами map, flatMap, foreach, filter, sorted.
   */
  implicit class RichArrayList[T](list : ArrayList[T])
  {
    def foreach (f : T => Unit) {
      for (i <- 0 until list.size()) f(list.get(i))
    }

    def map[E](f : T => E) : ArrayList[E] = {
      val res = new util.ArrayList[E]()
      for (i <- 0 until list.size()) res.add(f(list.get(i)))
      res
    }

    def flatMap[E](f : T => ArrayList[E]) : ArrayList[E] = {
      val res = new util.ArrayList[E]()
      for (i <- 0 until list.size()) res.addAll(f(list.get(i)))
      res
    }

    def filter (p : T => Boolean) : util.ArrayList[T] = {
      val res = new util.ArrayList[T]()
      for (i <- 0 until list.size()) if (p(list.get(i))) res.add(list.get(i))
      res
    }

    def sorted(implicit ord : math.Ordering[T]) : ArrayList[T] = {
      val l = new ArrayList[T]
      l.addAll(list)
      Collections.sort(l, ord)
      l
    }
  }
  
  //3 
  implicit def int2complex[T <% Double](i: T) = new Complex(i, 0)
  
  def main(args : Array[String]) {
    val x : Int => Int = _ + 1
    val y : (Int, Int) => Int = _ + _
    def foo(x : Int, y : Int) = x + y
    //val z = foo(_, 1)
    println(y(1, 3))
    
    def sum(x : Int)(implicit y : Int) = x + y
    implicit val one = 1
    implicit val two = 3
    
  }

}

