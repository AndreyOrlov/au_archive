package hw1

/**
 * Написать быструю сортировку массива.
 */
object QSortJavaStyle {
  private def sort[T <% Ordered[T]](array : Array[T], l : Int, r : Int) : Unit = {
    val p = array(r)
    var i = l;
    var j = r
    while (i <= j) {
      while (array(i) < p) i += 1
      while (array(j) > p) j -= 1
      if (i <= j) {
        val t = array(i);
        array(i) = array(j);
        array(j) = t
        i += 1
        j -= 1
      }
    }
    if (l < j) sort(array, l, j)
    if (j < r) sort(array, i, r)
  }

  def qsort[T <% Ordered[T]](array : Array[T]) : Unit = {
    sort(array, 0, array.length - 1)
  }
}

object QSortScalaStyle {
  def qsort[T <% Ordered[T]](array : Array[T]) : Array[T] = {
    if (array.size < 2)
      array
    else {
      qsort(array.filter(_ < array(0))) ++ array.filter(_ == array(0)) ++ qsort(array.filter(_ > array(0)))
    }
  }
}
