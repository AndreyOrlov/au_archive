package hw4_lazy

/**
 * Implementation of  deadlock because of lazy values
 */
object Main {
  def main(args: Array[String]) {
	  val temp = new DeadlockClass()
	  println(temp.c)
  }
}

class DeadlockClass {
  lazy val a = 5
  val b = (0 to 5).toList
  lazy val c = b.par.map(_ + a)
}