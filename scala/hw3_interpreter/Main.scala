package hw3_interpreter

/**
 * Написать интерпретируемый язык программирования. Синтаксис и все остальное дело вашего вкуса. Базовая спецификация следующая:
 * 1. Динамически типизируемый. У целых и вещественных чисел нет переполнения.
 * 2. Можно объявлять целые, вещественные и стоковые литералы.
 * 3. Можно объявлять переменные и функции. В функциях можно задавать значения по умолчанию.
 * 4. Можно эти переменные и функции вызывать.
 * 5. Можно создавать структуры без наследования. Просто данные, и возможно какие-то методы.
 */
object Main {
  def main(args: Array[String]) {
    val evaluator = new EvaluateVisitor()
    val globalCtx = new Context()

    while (true) {
      readLine("> ") match {
        case null => return
        case "exit" => return
        case "reset" => globalCtx.reset
        case "" =>
        case stmt => {
          try {
            val result = evaluator.eval(stmt, globalCtx)
						println(result._1)
          } catch {
            case e: RuntimeException => System.err.println(e.getMessage)
          }
        }
      }
    }
  }
}
