package hw1

/**
 * Написать реализацию длинной арифметики с методами +, -, *, /.
 */
class BigInteger {
  var buffer : Array[Int] = null
  var positive : Boolean = true

  def this(str : String) {
    this
    var size = 0
    if (str(0) == '-') {
      positive = false
      size = str.size - 1
    } else {
      positive = true
      size = str.size
    }
    var idx = 0
    val delta = if (positive) 0 else 1
    buffer = new Array[Int](size)
    while (idx < size) {
      buffer(size - idx - 1) = Char.char2int( str.charAt(idx + delta) ) - 48
      if (buffer(size - idx - 1) > 9 || buffer(size - idx - 1) < 0 ) throw new NumberFormatException()
      idx += 1
    }
  }

  def this (num : Int) {
    this
    var value = num
    if (num < 0) {
      positive = false
      value *= -1
    }
    var size = 1
    var temp = 10
    while (temp <= value) {
      size += 1
      temp *= 10
    }
    buffer = new Array[Int](size)
    temp = 0
    while (value != 0) {
      buffer(temp) = (value % 10)
      value /= 10
      temp += 1
    }
  }

  def +(that : BigInteger) : BigInteger = {
    val temp : BigInteger = new BigInteger()
    if (positive == that.positive) {
      temp.positive = positive
      temp.buffer = sum(this.buffer, that.buffer)
    } else {
      if (less(that.buffer, this.buffer)) {
        temp.positive = positive
        temp.buffer = subtr (this.buffer, that.buffer)
      } else if (less(this.buffer, that.buffer)) {
        temp.positive = that.positive
        temp.buffer = subtr (that.buffer, this.buffer)
      } else {
        temp.positive = true
        temp.buffer = new Array[Int](1)
      }
    }
    temp
  }

  def -(that : BigInteger) : BigInteger = {
    val temp : BigInteger = new BigInteger()
    if (this.positive != that.positive) {
      temp.positive = this.positive
      temp.buffer = sum(this.buffer, that.buffer)
    } else {
      if (less(that.buffer, this.buffer)) {
        temp.positive = this.positive
        temp.buffer = subtr(this.buffer, that.buffer)
      } else if (less(this.buffer, that.buffer)) {
        temp.positive = !that.positive
        temp.buffer = subtr (that.buffer, this.buffer)
      } else {
        temp.positive = true
        temp.buffer = new Array[Int](1)
      }
    }
    temp
  }

  def *(that : BigInteger) : BigInteger = {
    val temp : BigInteger = new BigInteger()
    if (this.positive == that.positive) temp.positive = true
    else temp.positive = false

    val thisSize = getSizeWithoutZeros(this.buffer)
    val thatSize = getSizeWithoutZeros(that.buffer)
    temp.buffer = new Array[Int](thisSize + thatSize)
    for (i <- 0 until thisSize) {
      for (j <- 0 until thatSize) {
        temp.buffer(i + j) = this.buffer(i) * that.buffer(j) + temp.buffer(i + j)
      }
    }
    temp.buffer = normalize(temp.buffer)
    temp
  }

  def /(that : BigInteger) : BigInteger = {
    if (getSizeWithoutZeros(that.buffer) == 1 && that.buffer(0) == 0) throw new ArithmeticException("Divide by zero")
    if (less(this.buffer, that.buffer)) return  new BigInteger(0)
    val temp : BigInteger = new BigInteger()
    if (this.positive == that.positive) temp.positive = true
    else temp.positive = false

    temp.buffer = new Array[Int](getSizeWithoutZeros(this.buffer))
    var idx = getSizeWithoutZeros(this.buffer) - 1
    var curValue = new BigInteger(0)
    while (idx >= 0) {
      curValue *= new BigInteger(10)
      curValue.buffer(0) = this.buffer(idx)
      if (!less(curValue.buffer, that.buffer)) {
        var x = 0
        var l = 0
        var r = 10
        while (l <= r) {
          val m = (l + r) >> 1
          var cur = new BigInteger(m)
          cur *= that
          if (!less(curValue.buffer, cur.buffer)) {
            x = m
            l = m + 1
          } else r = m - 1
        }
        temp.buffer(idx) = x
        curValue.buffer = subtr(curValue.buffer, (that * new BigInteger(x)).buffer)
      }
      idx -= 1
    }

    temp
  }

  private def sum(a : Array[Int], b : Array[Int]) : Array[Int] = {
    val aSize = getSizeWithoutZeros(a)
    val bSize = getSizeWithoutZeros(b)
    val temp : Array[Int] = new Array[Int](Math.max(aSize, bSize) + 1)
    var i = 0
    while (i < Math.min(aSize, bSize)) {
      temp(i) = a(i) + b(i)
      i += 1
    }
    while (i < aSize) {
      temp(i) = a(i)
      i += 1
    }
    while (i < bSize) {
      temp(i) = b(i)
      i += 1
    }
    normalize(temp)
  }

  private def subtr(a : Array[Int], b : Array[Int]) : Array[Int] = {
    val aSize = getSizeWithoutZeros(a)
    val bSize = getSizeWithoutZeros(b)
    val temp : Array[Int] = new Array[Int](aSize)
    var i = 0
    while (i < Math.min(aSize, bSize)) {
      temp(i) = a(i) - b(i)
      i += 1
    }
    while (i < aSize) {
      temp(i) = a(i)
      i += 1
    }
    normalize(temp)
  }

  private def normalize(a : Array[Int]) : Array[Int] = {
    for (i <- 0 until a.size-1) {
      while (a(i) >= 10) {
        a(i) -= 10
        a(i+1) += 1
      }
      while (a(i) < 0) {
        a(i) += 10
        a(i+1) -= 1
      }
    }
    a
  }

  private def less(a : Array[Int], b : Array[Int]) : Boolean = {
    var idx1 = getSizeWithoutZeros(a) - 1
    var idx2 = getSizeWithoutZeros(b) - 1
    if (idx1 < idx2) return true
    if (idx1 > idx2) return false
    while (idx1 >= 0) {
      if (a(idx1) < b(idx2)) return true
      if (a(idx1) > b(idx2)) return false
      idx1 -= 1
      idx2 -= 1
    }
    false
  }

  private def getSizeWithoutZeros(buffer : Array[Int]) : Int = {
    var idx = buffer.size - 1
    while (idx > 0 && buffer(idx) == 0) idx -= 1
    idx + 1
  }

  override def toString : String = {
    val builder = new StringBuilder()
    if (!positive) builder.append('-')
    var idx = getSizeWithoutZeros(buffer) - 1
    while (idx >= 0) {
      builder.append(buffer(idx))
      idx -= 1
    }
    builder.toString()
  }
}
