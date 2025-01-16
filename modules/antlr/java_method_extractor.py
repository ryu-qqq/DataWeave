from typing import List

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from modules.antlr.JavaLexer import JavaLexer
from modules.antlr.JavaParser import JavaParser
from modules.antlr.JavaParserListener import JavaParserListener
from modules.gpt.models.java_method_models import JavaMethod


class MethodExtractor(JavaParserListener):

    def __init__(self):
        self.methods = []

    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        method_name = ctx.identifier().getText()
        return_type = ctx.typeTypeOrVoid().getText()

        parameters = []
        if ctx.formalParameters():
            param_list = ctx.formalParameters().formalParameterList()
            if param_list:
                for param in param_list.formalParameter():
                    param_type = param.typeType().getText()
                    param_name = param.variableDeclaratorId().getText()
                    parameters.append({"type": param_type, "name": param_name})

        return_type_fields = {"type": return_type, "name": return_type, "filedJson": {}}

        self.methods.append(JavaMethod(
            method_name=method_name,
            return_type=return_type,
            parameters=parameters,
            return_type_fields=return_type_fields
        ))


class JavaMethodExtractor:

    def extract_method(self, code: str) -> List[JavaMethod]:
        input_stream = InputStream(code)
        lexer = JavaLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParser(token_stream)

        tree = parser.compilationUnit()

        extractor = MethodExtractor()
        walker = ParseTreeWalker()
        walker.walk(extractor, tree)

        return extractor.methods
