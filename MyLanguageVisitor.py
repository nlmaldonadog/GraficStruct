# Generated from MyLanguage.g4 by ANTLR 4.7
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by MyLanguageParser.

class MyLanguageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MyLanguageParser#commands.
    def visitCommands(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#command.
    def visitCommand(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#declaration.
    def visitDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#method.
    def visitMethod(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#methods.
    def visitMethods(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#var.
    def visitVar(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#vardos.
    def visitVardos(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#conditional.
    def visitConditional(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#postcond.
    def visitPostcond(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#repeat.
    def visitRepeat(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#printexpr.
    def visitPrintexpr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#printwhat.
    def visitPrintwhat(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#expr.
    def visitExpr(self, ctx):
        return self.visitChildren(ctx)


