package hw2

import scala.util.matching.Regex._
import java.util.IllegalFormatException

/**
 * (*) Implement class Complex(re: Double, im: Double). It should contain following operators: +, -, *, /, ^.
 * Override toString, equals, hashCode methods. Complex companion should contain I constant. And possibility
 * to write code like Re(z), Im(z). Also add methods conjugation, sqrt, abs. Add auxiliary constructor from String.
 * It should be possible to use all operators with other numeric types on the left and on the right side (probably
 * with import). Note that for every task part you can write code with any implementation and complexity (like two
 * sqrt values or one). All of this is up to you.
 */
class Complex(val re : Double, val im : Double) {

	def this(str : String) {
		this(Complex.parseRe(str), Complex.parseIm(str))
	}

	def +(that : Complex) : Complex = {
		new Complex(this.re + that.re, this.im + that.im)
	}

	def -(that : Complex) : Complex = {
		new Complex(this.re - that.re, this.im - that.im)
	}

	def *(that : Complex) : Complex = {
		new Complex(this.re * that.re - this.im * that.im,
					this.im * that.re + this.re * that.im)
	}

	def /(that : Complex) : Complex = {
		new Complex((this.re * that.re + this.im * that.im) / (that.re * that.re + that.im * that.im),
					(this.im * that.re - this.re * that.im) / (that.re * that.re + that.im * that.im) )
	}

	def ^(n : Double) : Complex = {
		val zn = math.pow(abs, n)
		val phin = math.atan(im / re) * n
		new Complex(zn * math.cos(phin), zn * math.sin(phin))
	}

	override def toString() : String = {
		if (re == 0 && im == 0) "0.0" else
			(if (re != 0) re + (if (im > 0) "+" else "") else "") + (if (im != 0) im + "i" else "")
	}

	override def equals(that : Any) : Boolean  = {
		that match {
			case c:Complex => this.re == c.re && this.im == c.im
			case _ => false
		}
	}

	override def hashCode : Int = {
		re.hashCode + im.hashCode
	}

	def conjugation() : Complex = {
		new Complex(re, -im)
	}

	def abs() : Double = {
		math.sqrt(re * re + im * im)
	}

	def sqrt() : Complex = {
		val a = math.sqrt((re + abs) / 2)
		val b = (if (im < 0) -1 else 1) * math.sqrt((-re + abs) / 2)
		new Complex(a, b)
	}
}

object Complex {
	def I : Complex = new Complex(0, 1)

	def Re(c : Complex) : Double = c.re

	def Im(c : Complex) : Double = c.im

	def parseRe(str : String) : Double = {
		val regex = "([0-9]+[.]?[0-9]*)(i)?".r
		val (res : String, i : String) = regex.findFirstMatchIn(str) match {
			case Some(x : Match) => (x.group(1), if (x.group(2) == null) "" else x.group(2))
			case None => throw new RuntimeException("The string is not complex number.")
		}

		if (i == "") res.toDouble else 0.0
	}

	def parseIm(str : String) = {
		val regex = "([0-9]+[.]?[0-9]*)i".r
		val res:String = regex.findFirstMatchIn(str) match {
			case Some(x:Match) => x.group(1)
			case None => "0.0"
		}

		res.toDouble
	}
}