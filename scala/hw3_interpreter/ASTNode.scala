package hw3_interpreter

import scala.collection.mutable

class Context {
  def this(map: mutable.Map[String, (AstNode, List[(String, AstNode)])]) = {
    this
    values ++= map
  }
  val values = new mutable.HashMap[String, (AstNode, List[(String, AstNode)])]()

  def get(key: String) = values.get(key)
  def put(key: String, value: (AstNode, List[(String, AstNode)])) = values.put(key, value)
  def reset = values.clear()
}

sealed abstract class AstNode {
  def visit(visitor: AstVisitor, ctx: Context): (AstNode, Context)
}

case class AstInt(v: BigInt) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
  override def toString = v.toString()
}

case class AstDouble(v: BigDecimal) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
  override def toString = v.toString()
}

case class AstLiteral(v: String) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
  override def toString = v
}

case class AstIdentifier(id: String) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit (this, ctx)
  override def toString = id
}

case class AstStruct(id: String, args: List[AstNode]) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
  override def toString = "struct " + id + "{ " + args + "}"
}

case class AstVariable(id: String) extends AstNode {
  def visit(visitor: AstVisitor, ctx:Context) = visitor.visit(this, ctx)
  override def toString = "var" + id
}

case class AstAssign(id: String, expr: AstNode) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
  override def toString = id + " = " + expr
}

case class AstFunction(id: String, params: List[AstNode], body: AstNode) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
  override def toString = "func " + id + "(" + params + ")"
}

case class AstCall(id: String, params: List[AstNode]) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
}

case class AstBinaryOp(left: AstNode, right: AstNode, op: String) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
}

case class AstUnaryOp(v: AstNode, op: String) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
}

case class AstStructField (id: String, field: String) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
  override def toString = id + "." + field
}

case class AstStructAssignField(id: String, field: String, expr: AstNode) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
}

case class AstReturn(expr: Option[AstNode]) extends AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
}

case class AstBlock(stmts: List[AstNode]) extends  AstNode {
  def visit(visitor: AstVisitor, ctx: Context) = visitor.visit(this, ctx)
}