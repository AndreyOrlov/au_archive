package hw1

/**
 * Найти GCD чисел a и b, а также коэффициенты линейного представления GCD числами a и b.
 */
object GCD {
  def gcd(a : Int, b : Int) : (Int, Int, Int) = {
    if (a == 0) (b, 0, 1)
    else {
      val (d, x1, y1) = gcd(b % a, a)
      (d, y1 -(b/a)*x1, x1)
    }
  }
}
