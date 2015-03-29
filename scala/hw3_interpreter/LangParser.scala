package hw3_interpreter

import scala.util.parsing.combinator._
class LangParser extends JavaTokenParsers {
  def getAst(code: String): AstNode = {
    parseAll(program, code) match {
      case Success(node, in) => node
      case NoSuccess(msg, in) => throw new RuntimeException(msg)
    }
  }

  def keyword = "func" | "struct" | "return"

  val intregex = """(-?\d+)""".r
  def number = floatingPointNumber ^^ {
    case s => s match {
      case intregex(v) => AstInt(BigInt(v))
      case v => AstDouble(BigDecimal(v))
    }
  }

  def identifier = (not(keyword) ~> ident) ^^ AstIdentifier

  def literal = stringLiteral ^^ AstLiteral

  def converToBinary: PartialFunction[~[AstNode, List[~[String, AstNode]]], AstNode ] = {
    case left ~ list => if (list.isEmpty) left
      else list.foldLeft(left) {
      case (res, op ~ right) => AstBinaryOp(res, right, op)
    }
  }
  
  def expr: Parser[AstNode] = term ~ rep("+" ~ term | "-" ~ term) ^^ converToBinary
  
  def term: Parser[AstNode] = unary ~ rep("*" ~ unary | "/" ~ unary) ^^ converToBinary
  
  def unary: Parser[AstNode] = ref | "-" ~> ref ^^ Negate
  
  def ref: Parser[AstNode] = factor |||
    (identifier <~ "(") ~ repsep(expr, ",") <~ ")" ^^ { case fun ~ params => AstCall(fun.id, params) } |||  
  (identifier <~ ".") ~ identifier ^^ {
      case AstIdentifier(id) ~ AstIdentifier(field) => AstStructField(id, field)
    }
    
  def factor: Parser[AstNode] = number | identifier | "(" ~> expr <~ ")"
  
  def Negate(expr: AstNode): AstNode = AstUnaryOp(expr, "-")

  def structDef: Parser[AstNode] =  ("struct" ~> identifier <~ "{") ~ (repsep(args, ",") <~ "}") ^^ {
    case id ~ args =>  AstStruct(id.id, args)
  }

  def funcDef: Parser[AstFunction] = (((("func" ~> identifier) <~ "(") ~ repsep(args, ",")) <~ ")") ~ block ^^ {
    case fun ~ params ~ body => AstFunction(fun.id, params, body)
  }

  def args: Parser[AstNode] = assignment | identifier

  def assignment: Parser[AstNode] = (expr <~ "=") ~ expr ^^ {
    case AstIdentifier(id) ~ expression => AstAssign(id, expression)
    case AstStructField(id, field) ~ expression => AstStructAssignField(id, field, expression)
  }


  def returnStmt: Parser[AstReturn] = "return" ~> (expr?) ^^ {
    case expression => AstReturn(expression)
  }
  def stmt: Parser[AstNode] = assignment | funcDef | structDef | returnStmt |
                              expr | identifier | literal | number | block

  def block: Parser[AstBlock] = "{" ~> repsep(stmt, ";") <~ "}" ^^ {
    case stmts => AstBlock(stmts)
  }

  def program: Parser[AstNode] = stmt
}
