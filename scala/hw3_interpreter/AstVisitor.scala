package hw3_interpreter

trait AstVisitor {
  def visit(node: AstInt, ctx: Context): (AstNode, Context)
  def visit(node: AstDouble, ctx: Context): (AstNode, Context)
  def visit(node: AstLiteral, ctx: Context): (AstNode, Context)
  def visit(node: AstIdentifier, ctx: Context): (AstNode, Context)
  def visit(node: AstStruct, ctx: Context): (AstNode, Context)
  def visit(node: AstVariable, ctx: Context): (AstNode, Context)
  def visit(node: AstAssign, ctx: Context): (AstNode, Context)
  def visit(node: AstFunction, ctx: Context): (AstNode, Context)
  def visit(node: AstCall, ctx: Context): (AstNode, Context)
  def visit(node: AstBinaryOp, ctx: Context): (AstNode, Context)
  def visit(node: AstUnaryOp, ctx: Context): (AstNode, Context)
  def visit(node: AstStructField, ctx: Context): (AstNode, Context)
  def visit(node: AstStructAssignField, ctx: Context): (AstNode, Context)
  def visit(node: AstReturn, ctx: Context): (AstNode, Context)
  def visit(node: AstBlock, ctx: Context): (AstNode, Context)
}
