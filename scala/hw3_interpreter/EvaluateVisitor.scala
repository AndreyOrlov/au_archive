package hw3_interpreter


class EvaluateVisitor extends AstVisitor{
  val parser = new LangParser()

  def eval(stmt: String, ctx: Context): (AstNode, Context) = runStmt(parser.getAst(stmt), ctx)

  def runStmt(node: AstNode, ctx: Context) = node.visit(this, ctx)

  def visit(node: AstInt, ctx: Context): (AstNode, Context) = (node, ctx)

  def visit(node: AstDouble, ctx: Context): (AstNode, Context) = (node, ctx)

  def visit(node: AstLiteral, ctx: Context): (AstNode, Context) = (node, ctx)

  def visit(node: AstStruct, ctx: Context): (AstNode, Context) = {
    val fields: List[(String, AstNode)] = node.args.map(_ match {
      case AstAssign(id, astNode) => astNode.visit(this, ctx) match {
        case (v, ctx) => (id, v)
      }
      case AstIdentifier(id) => (id, null)
      case _ => throw new RuntimeException ("Wrong parameter of struct")
    })
    ctx.put(node.id, (node, fields))
    (node, ctx)
  }

  def visit(node: AstVariable, ctx: Context): (AstNode, Context) = {
    ctx.get(node.id) match {
      case Some(v) => (v._1, ctx)
      case None => throw new RuntimeException("Variable is not found")
    }
  }

  def visit(node: AstAssign, ctx: Context): (AstNode, Context) = {
    node.expr.visit(this, ctx) match {
      case (node1, ctx2) => {
        ctx2.put(node.id, (node1, null))
        (node1, ctx2)
      }
    }
  }

  def visit(node: AstFunction, ctx: Context): (AstNode, Context) = {
    val params: List[(String, AstNode)] = node.params.map { node => node match {
      case AstAssign(id, astNode) => (id, astNode)
      case AstIdentifier(id) => (id, null)
      case _ => throw new RuntimeException ("wrong expression")
    }}
    ctx.put(node.id, (node.body, params))
    (node, ctx)
  }

  def visit(node: AstCall, ctx: Context): (AstNode, Context) = {
    ctx.get(node.id) match {
      case Some((body, params)) => {
        val funCtx = new Context(ctx.values)
        if (node.params.size > params.size)
          throw new RuntimeException ("wrong number of parameters")
        var i = 0
        while (i < params.size) {
          params(i) match {
            case (id, null) =>
              if (i < node.params.size)
                funCtx.put(id, (node.params(i).visit(this, ctx)._1, null))
              else
                throw new RuntimeException("Parameter is not defined")
            case (id, node1) => if (i < node.params.size)
                funCtx.put(id, (node.params(i).visit(this, ctx)._1, null))
              else
                funCtx.put(id, (node1.visit(this, ctx)._1, null))
            case a => throw new RuntimeException ("AstCall node error")
          }
          i += 1
        }
        body.visit(this, funCtx)
      }
      case None => throw new RuntimeException ("Function is not exists")
    }
  }

  def visit(node: AstBinaryOp, ctx: Context): (AstNode, Context) = node match{
    case AstBinaryOp(leftExpr, rightExpr, op) => {
      val (left, ctx2) = leftExpr.visit(this, ctx)
      val (right, ctx3) = rightExpr.visit(this, ctx2)
      left match {
        case AstInt(l) => right match {
          case AstInt(r) => (AstInt(calc(l, r, op)), ctx3)
          case AstDouble(r) => (AstDouble(calc(BigDecimal(l), r, op)), ctx3)
          case _ => throw new RuntimeException("Binary operations supports only for numbers now.")
        }
        case AstDouble(l) => right match {
          case AstInt(r) => (AstDouble(calc(l, BigDecimal(r), op)), ctx3)
          case AstDouble(r) => (AstDouble(calc(l, r, op)), ctx3)
          case _ => throw new RuntimeException("Binary operations supports only for numbers now.")
        }
        case _ => throw new RuntimeException("Binary operations supports only for numbers now.")
      }
    }
  }

  //TODO: Find generative solution
  private def calc(left: BigInt, right: BigInt, op: String):BigInt = {
    op match {
      case "+" => left + right
      case "-" => left - right
      case "*" => left * right
      case "/" => left / right
      case _ => throw new RuntimeException("Operation is not supported")
    }
  }
  private def calc(left: BigDecimal, right: BigDecimal, op: String):BigDecimal = {
    op match {
      case "+" => left + right
      case "-" => left - right
      case "*" => left * right
      case "/" => left / right
      case _ => throw new RuntimeException("Operation is not supported")
    }
  }


  def visit(node: AstUnaryOp, ctx: Context): (AstNode, Context) = node.op match {
    case "-" => node.visit(this, ctx) match {
      case (AstInt(v), ctx2) => (AstInt(-v), ctx2)
      case (AstDouble(v), ctx2) => (AstDouble(-v), ctx2)
      case _ => throw new RuntimeException("Operation is not supported for this type")
    }
    case _ => throw new RuntimeException("Operation is not supported")
  }

  def visit(node: AstIdentifier, ctx: Context): (AstNode, Context) = ctx.get(node.id) match {
    case Some(v) => v match {
      case (node, nodes) => (node, ctx)
    }
    case None => throw new RuntimeException("Id not found")
  }

  def visit(node: AstStructField, ctx: Context): (AstNode, Context) = ctx.get(node.id) match {
    case Some((AstStruct(_,_), list)) => list.find( _._1 == node.field) match {
      case Some((_, node1)) => (node1, ctx)
      case None => throw new RuntimeException ("Field not found")
    }
    case _ => throw new RuntimeException ("Struct not found")
  }

  def visit(node: AstReturn, ctx: Context): (AstNode, Context) = node.expr match {
    case Some(expr) => expr.visit(this, ctx)
    case None => null
  }

  def visit(node: AstStructAssignField, ctx: Context): (AstNode, Context) = {
    ctx.get(node.id) match {
      case Some (s) => s._2.find(_._1 == node.field) match {
        case Some(p) => ctx.put(node.id, (s._1, s._2.map {
          elem => if (elem._1 == node.field) node.expr.visit(this, ctx) match {
            case (node, ctx) => (elem._1, node)
          }
            else elem
          }))
          (node.expr, ctx)
        case None => throw new RuntimeException("Field not found")
      }
      case None => throw new RuntimeException("Struct not found")
    }

  }

  def visit(node: AstBlock, ctx: Context): (AstNode, Context) = {
    var i = 0
    while (i < node.stmts.size) {
      node.stmts(i) match {
        case AstReturn(expr) => expr match {
          case Some(e) => return e.visit(this, ctx)
          case None => return (null, ctx)
        }
        case node => node.visit(this, ctx)
      }
      i += 1
    }
    (null, ctx)
  }
}