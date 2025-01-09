import logging

from dataweave.antlr.JavaParserListener import JavaParserListener


class MethodExtractor(JavaParserListener):

    def __init__(self, method_name, token_stream):
        self.method_name = method_name
        self.token_stream = token_stream
        self.method_content = None

    def enterMethodDeclaration(self, ctx):
        print(f"Context Type: {type(ctx)}")
        if hasattr(ctx, 'identifier'):
            method_name_node = ctx.identifier()
            if method_name_node and method_name_node.getText() == self.method_name:
                start_index = ctx.start.tokenIndex
                stop_index = ctx.stop.tokenIndex
                self.method_content = self.token_stream.getText(start_index, stop_index)
                logging.info(f"Extracted Method: {self.method_name}")
                logging.info(f"Content:\n{self.method_content}")




