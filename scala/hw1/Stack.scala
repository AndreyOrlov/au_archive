package hw1

/**
 * Написать ковариантный неизменяемыый стэк с методами push, pop и toString.
 *
 */
abstract class Stack[+T] {
  def push[S >: T](x : S) : Stack[S] = new NonEmptyStack(x, this)
  def pop() : Stack[T]
  override def toString() : String
}
object EmptyStack extends Stack[Nothing] {
  def pop() = throw new NoSuchElementException("Stack is Empty")
  override def toString() : String = ""
}
class NonEmptyStack[+T](elem : T, oldStack : Stack[T]) extends Stack[T] {
  val top = elem
  def pop() = oldStack
  override def toString() : String = top.toString() + " " + pop.toString()
}